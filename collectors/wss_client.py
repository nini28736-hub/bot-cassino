import asyncio
import os
import websockets

class WSSClient:
    def __init__(self, url: str = None, data_queue: asyncio.Queue = None):
        self.url = url or os.getenv("WSS_URL")
        self.data_queue = data_queue
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://sortenabet.bet.br"
        }

    async def connect(self):
        if not self.url:
            print("Erro: WSS_URL nao configurada no .env / Square Cloud.")
            return

        while True:
            try:
                # Tenta conexao no websockets v13+
                async with websockets.connect(
                    self.url,
                    additional_headers=self.headers,
                    ping_interval=20,
                    ping_timeout=10
                ) as ws:
                    print("🟢 Conectado ao WebSocket do Bac Bo (Evolution)!")
                    
                    async for message in ws:
                        print(f"📩 Dado do Bac Bo: {message[:120]}...")
                        if self.data_queue:
                            await self.data_queue.put(message)

            except TypeError:
                try:
                    async with websockets.connect(
                        self.url,
                        extra_headers=self.headers,
                        ping_interval=20,
                        ping_timeout=10
                    ) as ws:
                        print("🟢 Conectado ao WebSocket do Bac Bo (Evolution)!")
                        
                        async for message in ws:
                            print(f"📩 Dado do Bac Bo: {message[:120]}...")
                            if self.data_queue:
                                await self.data_queue.put(message)
                    except Exception as e:
                        print(f"Erro WSS: {e}. Reconectando em 5s...")
                        await asyncio.sleep(5)

            except Exception as e:
                print(f"Erro WSS: {e}. Reconectando em 5s...")
                await asyncio.sleep(5)

    async def start(self):
        await self.connect()
