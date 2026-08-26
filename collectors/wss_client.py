import asyncio
import json
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
            print("Erro: WSS_URL nao configurada.")
            return

        # Pacote de autoria/inicialização do jogo
        init_payload = {
            "brand_key": "427279c5",
            "cid": 3,
            "device_id": "8030a756-a2bc-497e-8c2f-5e0d6d932668",
            "label_key": "4742f935-4586-487c-97a0-2dc10a19b4c7",
            "label_name": "4742f935-4586-487c-97a0-2dc10a19b4c7",
            "page": "https://sortenabet.bet.br/magic-roulette",
            "session_id": "051fc5c0-73ff-4682-b41b-95fbee29bd0c",
            "simulation_mode": False,
            "tracker_version": "1.3.503"
        }

        while True:
            try:
                # Tenta conexao no websockets v13+
                async with websockets.connect(
                    self.url,
                    additional_headers=self.headers,
                    ping_interval=None
                ) as ws:
                    print("🟢 Conectado! Enviando handshake inicial...")
                    await ws.send(json.dumps(init_payload))
                    print("✅ Handshake enviado! Aguardando rodadas do jogo...")

                    async for message in ws:
                        print(f"📩 Dado recebido do jogo: {message}")
                        if self.data_queue:
                            await self.data_queue.put(message)

            except TypeError:
                # Fallback para versoes anteriores do websockets
                try:
                    async with websockets.connect(
                        self.url,
                        extra_headers=self.headers,
                        ping_interval=None
                    ) as ws:
                        print("🟢 Conectado! Enviando handshake inicial...")
                        await ws.send(json.dumps(init_payload))
                        print("✅ Handshake enviado! Aguardando rodadas do jogo...")

                        async for message in ws:
                            print(f"📩 Dado recebido do jogo: {message}")
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
