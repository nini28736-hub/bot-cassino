import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from database.db import DatabaseManager
from collectors.wss_client import WSSClient
from engine.strategies import ColorPatternStrategy, SequenceBreakStrategy
from engine.ensemble import DecisionEngine
from bot.middlewares import LicenseMiddleware
from bot.handlers import router as bot_router

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def process_signals(data_queue: asyncio.Queue, engine: DecisionEngine, bot: Bot, db: DatabaseManager):
    history = []
    while True:
        result = await data_queue.get()
        history.append(result)
        if len(history) > 100:
            history.pop(0)

        decision = await engine.evaluate(history)
        if decision["signal"]:
            logging.info(f"Sinal gerado: {decision['signal']}")

        data_queue.task_done()

async def main():
    bot_token = os.getenv("BOT_TOKEN")
    wss_url = os.getenv("WSS_URL")

    db = DatabaseManager()
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    dp.update.middleware(LicenseMiddleware())
    dp.include_router(bot_router)

    strategies = [ColorPatternStrategy(), SequenceBreakStrategy()]
    engine = DecisionEngine(strategies=strategies, consensus_threshold=70.0)

    data_queue = asyncio.Queue()
    wss_client = WSSClient(url=wss_url, data_queue=data_queue)

    await asyncio.gather(
        dp.start_polling(bot, db=db),
        wss_client.start(),
        process_signals(data_queue, engine, bot, db)
    )

if __name__ == "__main__":
    asyncio.run(main())