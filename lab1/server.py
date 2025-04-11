import asyncio
import websockets

connected_clients = set()

async def handle_client(*args):
    websocket = args[0]
    # Eğer path parametresi gelmişse, onu al; gelmemişse None yapıyoruz
    path = args[1] if len(args) > 1 else None
    
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("Sunucu çalışıyor: ws://localhost:8765")
    await server.wait_closed()

asyncio.run(start_server())
