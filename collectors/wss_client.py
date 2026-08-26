import asyncio
import json
import logging
import websockets

class WSSClient:
    def __init__(self, url: str, data_queue: asyncio.Queue):
        self.url = url
        self.data_queue = data_queue
        self.is_running = False

    async def start(self):
        self.is_running = True
        while self.is_running:
            try:
                async with websockets.connect(self.url) as ws:
                    logging.info("WebSocket conectado.")
                    while self.is_running:
                        message = await ws.recv()
                        data = json.loads(message)
                        if "result" in data:
                            await self.data_queue.put(data["result"])
            except Exception as e:
                logging.error(f"Erro WSS: {e}. Reconectando em 5s...")
                await asyncio.sleep(5)