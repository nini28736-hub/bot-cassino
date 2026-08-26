import asyncio
import os
import websockets

class WSSClient:
    def __init__(self, url: str = None, data_queue: asyncio.Queue = None):
        self.url = url or os.getenv("WSS_URL")
        self.data_queue = data_queue
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://sortenabet.bet.br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    async def _send_keepalive(self, ws):
        """Envia pings em texto plano a cada 15s para manter a conexao viva sem dar erro 1011"""
        while True:
            await asyncio.sleep(15)
            try:
                await ws.send("ping")
            except Exception:
                break

    async def connect(self):
        if not self.url:
            print("Erro: WSS_URL nao configurada.")
            return

        while True:
            try:
                # ping_interval=None impede o envio de pings nativos rejeitados pelo servidor
                try:
                    async with websockets.connect(
                        self.url,
                        additional_headers=self.headers,
                        ping_interval=None
                    ) as ws:
                        print("🟢 Conexao estabilizada e recebendo dados!")
                        ping_task = asyncio.create_task(self._send_keepalive(ws))
                        try:
                            async for message in ws:
                                if self.data_queue:
                                    await self.data_queue.put(message)
                        finally:
                            ping_task.cancel()
                except TypeError:
                    async with websockets.connect(
                        self.url,
                        extra_headers=self.headers,
                        ping_interval=None
                    ) as ws:
                        print("🟢 Conexao estabilizada e recebendo dados!")
                        ping_task = asyncio.create_task(self._send_keepalive(ws))
                        try:
                            async for message in ws:
                                if self.data_queue:
                                    await self.data_queue.put(message)
                        finally:
                            ping_task.cancel()

            except Exception as e:
                print(f"Erro WSS: {e}. Reconectando em 5s...")
                await asyncio.sleep(5)

    async def start(self):
        await self.connect()
