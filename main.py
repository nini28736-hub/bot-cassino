import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from collectors.wss_client import WSSClient
from database.db import DatabaseManager
from bot.handlers import router as bot_router
from bot.middlewares import LicenseMiddleware

load_dotenv()

async def main():
    bot_token = os.getenv("BOT_TOKEN")
    wss_url = os.getenv("WSS_URL")

    if not bot_token:
        raise ValueError("BOT_TOKEN nao configurado nas variaveis de ambiente!")

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    db = DatabaseManager()

    dp.include_router(bot_router)
    dp.message.outer_middleware(LicenseMiddleware())

    data_queue = asyncio.Queue()
    wss_client = WSSClient(url=wss_url, data_queue=data_queue)

    print("🚀 Iniciando Bot e escuta do WebSocket...")

    # Executa o polling do Telegram e o WebSocket simultaneamente
    await asyncio.gather(
        dp.start_polling(bot, db=db),
        wss_client.connect()
    )

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
