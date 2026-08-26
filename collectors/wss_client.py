import asyncio
import os
import websockets
from websockets.exceptions import ConnectionClosed

# Link padrao da Evolution caso a variavel de ambiente nao seja detectada
DEFAULT_WSS_URL = "wss://sortenabet.evo-games.com/public/bacbo/player/game/SortenaBacBo0001/socket?messageFormat=json&tableConfig=txpifq7wh56aauyb&EVOSESSIONID=tyoiqqrorafexvh3ua7duvyxhwj3bzowd04dceac74a5357c112bf14d2ff75d284726000fb6e71d2f&instance=ryd5qc-tyoiqqrorafexvh3-txpifq7wh56aauyb&client_version=6.20260826.73623.64628-72eea7188b-r2"

class WSSClient:
    def __init__(self, url: str = None, data_queue: asyncio.Queue = None):
        self.url = url or os.getenv("WSS_URL") or DEFAULT_WSS_URL
        self.data_queue = data_queue
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://sortenabet.bet.br"
        }

    async def connect(self):
        while True:
            try:
                try:
                    async with websockets.connect(
                        self.url,
                        additional_headers=self.headers,
                        ping_interval=20,
                        ping_timeout=10
                    ) as ws:
                        print("🟢 Conectado com sucesso ao WebSocket do Bac Bo (Evolution)!")
                        async for message in ws:
                            print(f"🎲 Evento do Bac Bo: {message[:120]}...")
                            if self.data_queue:
                                await self.data_queue.put(message)

                except TypeError:
                    async with websockets.connect(
                        self.url,
                        extra_headers=self.headers,
                        ping_interval=20,
                        ping_timeout=10
                    ) as ws:
                        print("🟢 Conectado com sucesso ao WebSocket do Bac Bo (Evolution)!")
                        async for message in ws:
                            print(f"🎲 Evento do Bac Bo: {message[:120]}...")
                            if self.data_queue:
                                await self.data_queue.put(message)

            except ConnectionClosed as e:
                print(f"🔄 Conexao encerrada pela Evolution ({e.code}). Reconectando em 3s...")
                await asyncio.sleep(3)
            except Exception as e:
                print(f"Erro WSS: {e}. Reconectando em 5s...")
                await asyncio.sleep(5)

    async def start(self):
        await self.connect()
