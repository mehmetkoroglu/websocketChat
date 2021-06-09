import asyncio
import websockets
import time
import json

connected = set()
kisiler = []

async def server(websocket, path):
    connected.add(websocket)
    i = 0
    try:
        async for veriler in websocket:  # veriler send ile gelen her veri(client ve message)
            if veriler[0] == "_":  # Client ise
                kisiler.append(veriler)  # listeye ekle
                for conn in connected:  # Client list
                    for i in range(len(kisiler)):
                        await conn.send(kisiler[i])
                        print(kisiler[i])
                        i = i + 1
                i = 0
            else:  # Message ise
                for conn in connected:
                    if conn != websocket:
                        await conn.send(veriler)
                        print(veriler)
    finally:
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
