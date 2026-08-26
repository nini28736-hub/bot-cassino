import asyncio
import json
import os
import time
import uuid
import websockets

class WSSClient:
    def __init__(self, url: str = None, data_queue: asyncio.Queue = None):
        self.url = url or os.getenv("WSS_URL")
        self.data_queue = data_queue
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://sortenabet.bet.br"
        }

    async def _keepalive(self, ws):
        """Envia o heartbeat oficial (cid: 1) a cada 20 segundos para manter a conexao ativa"""
        while True:
            await asyncio.sleep(20)
            ping_payload = {
                "cid": 1,
                "ts": int(time.time() * 1000),
                "uuid": str(uuid.uuid4())
            }
            try:
                await ws.send(json.dumps(ping_payload))
            except Exception:
                break

    async def connect(self):
        if not self.url:
            print("Erro: WSS_URL nao configurada.")
            return

        init_payload = {
            "brand_key": "427279c5",
            "cid": 3,
            "device_id": str(uuid.uuid4()),
            "label_key": "4742f935-4586-487c-97a0-2dc10a19b4c7",
            "label_name": "4742f935-4586-487c-97a0-2dc10a19b4c7",
            "page": "https://sortenabet.bet.br/magic-roulette",
            "session_id": str(uuid.uuid4()),
            "simulation_mode": False,
            "tracker_version": "1.3.504"
        }

        while True:
            try:
                init_payload["ts"] = int(time.time() * 1000)
                init_payload["uuid"] = str(uuid.uuid4())

                async with websockets.connect(
                    self.url,
                    additional_headers=self.headers,
                    ping_interval=None
                ) as ws:
                    print("🟢 Conectado! Enviando handshake inicial...")
                    await ws.send(json.dumps(init_payload))
                    print("✅ Handshake enviado! Mantendo conexao viva com cid: 1...")

                    ping_task = asyncio.create_task(self._keepalive(ws))

                    try:
                        async for message in ws:
                            print(f"📩 Dado recebido do jogo: {message}")
                            if self.data_queue:
                                await self.data_queue.put(message)
                    finally:
                        ping_task.cancel()

            except TypeError:
                try:
                    init_payload["ts"] = int(time.time() * 1000)
                    init_payload["uuid"] = str(uuid.uuid4())

                    async with websockets.connect(
                        self.url,
                        extra_headers=self.headers,
                        ping_interval=None
                    ) as ws:
                        print("🟢 Conectado! Enviando handshake inicial...")
                        await ws.send(json.dumps(init_payload))
                        print("✅ Handshake enviado! Mantendo conexao viva com cid: 1...")

                        ping_task = asyncio.create_task(self._keepalive(ws))

                        try:
                            async for message in ws:
                                print(f"📩 Dado recebido do jogo: {message}")
                                if self.data_queue:
                                    await self.data_queue.put(message)
                        finally:
                            ping_task.cancel()
                except Exception as e:
                    print(f"Erro WSS: {e}. Reconectando em 5s...")
                    await asyncio.sleep(5)

            except Exception as e:
                print(f"Erro WSS: {e}. Reconectando em 5s...")
                await asyncio.sleep(5)

    async def start(self):
        await self.connect()
