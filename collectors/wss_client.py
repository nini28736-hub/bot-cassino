import asyncio
import os
from aiohttp import web

class WSSClient:
    def __init__(self, url: str = None, data_queue: asyncio.Queue = None):
        self.data_queue = data_queue
        # A Square Cloud injeta a porta na variavel PORT
        self.port = int(os.getenv("PORT", 8080))

    async def handle_incoming_data(self, request):
        """Recebe as rodadas enviadas da sua maquina local"""
        try:
            payload = await request.text()
            if payload and self.data_queue:
                await self.data_queue.put(payload)
                print(f"📩 Dado recebido via Bridge Local: {payload[:100]}...")
            return web.Response(text="OK", status=200)
        except Exception as e:
            print(f"Erro ao processar pacote da Bridge: {e}")
            return web.Response(text="Error", status=500)

    async def start(self):
        app = web.Application()
        app.router.add_post('/data', self.handle_incoming_data)
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        print(f"🟢 Receptor HTTP ativo na porta {self.port}! Aguardando dados do seu computador...")
        await site.start()
        
        # Mantem o loop ativo
        while True:
            await asyncio.sleep(3600)
