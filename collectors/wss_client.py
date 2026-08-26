import asyncio
import json
import logging
import websockets
import os

logger = logging.getLogger(__name__)

class WSSClient:
    def __init__(self, url: str, on_message_callback):
        self.url = url
        self.on_message_callback = on_message_callback
        self.is_running = False

    async def start(self):
        self.is_running = True
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://sortenabet.bet.br"
        }
        
        while self.is_running:
            try:
                async with websockets.connect(self.url, extra_headers=headers) as ws:
                    logger.info("Conectado ao WebSocket da plataforma!")
                    while self.is_running:
                        message = await ws.recv()
                        await self.on_message_callback(message)
            except Exception as e:
                logger.error(f"Erro no WSS: {e}. Reconectando em 5s...")
                await asyncio.sleep(5)

    def stop(self):
        self.is_running = False
