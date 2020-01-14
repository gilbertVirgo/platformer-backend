import asyncio
import websockets

async def recieve(websocket):
	data = websocket.recv()
	print(data)
	await websocket.send("ping pong")

async def GameLoop(websocket,path):
	print("GameLoop entered")
	while True:
		await recieve(websocket,path)
		print("executed")

print("1")
start_server = websockets.serve(GameLoop,"0.0.0.0",1235)
print("1")
asyncio.get_event_loop().run_until_complete(start_server)
print("1")
asyncio.get_event_loop().run_forever()
print("1")