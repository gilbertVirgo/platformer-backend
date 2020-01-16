import asyncio
import websockets
from game import Game

SOCKETS = set()
game = Game(None)
print("Game object initiated")

async def recieve(websocket):
	data = await websocket.recv()
	print("DATA RECIEVED:",data,"FROM:",websocket.remote_address)

async def socketHandle(websocket,path):
	print("socketHandle entered:",websocket.remote_address)
	SOCKETS.add(websocket)

	print("Adding player")
	game.addPlayer(websocket.remote_address)
	print("Player added")

	present = True
	while present:
		try:
			data = await recieve(websocket)
			print(data)
		except:
			SOCKETS.remove(websocket)
			present = False
			game.removePlayer(websocket.remote_address)
			websocket.close()

@asyncio.coroutine
async def GameLoop():

	print("Loop entering")
	while True:
		ret = game.returnRender()
		for websocket in SOCKETS:
			try:
				await websocket.send(ret)
			except:
				# connection is probably closed, do nothing as that's handled in socketHandle
				pass

		game.tick()

		# print("tick")
		await asyncio.sleep(1/30)

asyncio.ensure_future(GameLoop())

start_server = websockets.serve(socketHandle,"0.0.0.0",1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()