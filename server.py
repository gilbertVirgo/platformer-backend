import asyncio
import websockets
import logging
from threading import Thread

SOCKETS = set()

async def recieve(websocket):
	data = await websocket.recv()
	print("DATA RECIEVED:",data,"FROM:",websocket.remote_address)

async def socketHandle(websocket,path):
	print("socketHandle entered:",websocket.remote_address)
	SOCKETS.add(websocket)
	while True:
		await recieve(websocket)

@asyncio.coroutine
async def GameLoop():
	while True:
		for websocket in SOCKETS:
			await websocket.send("tick")
		await asyncio.sleep(1)

asyncio.ensure_future(GameLoop())

start_server = websockets.serve(socketHandle,"0.0.0.0",1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()