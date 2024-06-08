import asyncio
import websockets


async def connect_to_server():
    async with websockets.connect("ws://13.53.158.82:9000") as websocket:
        await websocket.send("Hello, Server!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.run(connect_to_server())
