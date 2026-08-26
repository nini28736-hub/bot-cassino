import websockets
import json
import os

WSS_URL = os.getenv("WSS_URL")

# Cabeçalhos obrigatórios para o servidor da Cactus Gaming liberar o bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://sortenabet.bet.br"
}

async def connect_to_game():
    # Adicione o parâmetro extra_headers na conexão
    async with websockets.connect(WSS_URL, extra_headers=headers) as websocket:
        print("Conectado com sucesso ao WebSocket!")
        while True:
            response = await websocket.recv()
            print("Dado recebido:", response)
