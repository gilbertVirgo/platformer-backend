import asyncio
import websockets
import json
import sys
from game import Game

dataDebug = False

async def recieve(websocket,debug):
	data = await websocket.recv()
	if debug: print("DATA RECIEVED:",data,"FROM:",websocket.remote_address)
	return data

async def socketHandle(websocket,path):
	print("socketHandle entered:",websocket.remote_address)
	SOCKETS.add(websocket)
	print("Awaiting id")
	data = await recieve(websocket,dataDebug)
	data = json.loads(data)
	data = data["data"]
	print("Got id",data["id"])

	print("Adding player:",data["id"])
	game.addPlayer(data["id"])
	print("Player added")

	present = True
	while present:
		try:
			data = await recieve(websocket,dataDebug)
			data = json.loads(data)
			data = data["data"]
			game.updatePlayer(data["id"],data["profile"])
			if dataDebug: print(data)
		except ConnectionResetError:
			SOCKETS.remove(websocket)
			present = False
			game.removePlayer(websocket.remote_address)
			websocket.close()
		except:
			print("Error",sys.exc_info())

@asyncio.coroutine
async def GameLoop(ticks):

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

		if ticks: print("tick")
		await asyncio.sleep(1/30)

if __name__ == "__main__":

	if "-m" in sys.argv:
		print("Movement data debug mode on")
		movementDebug = True
	else:
		movementDebug = False

	if "-t" in sys.argv:
		print("Tick mode on")
		ticks = True
	else:
		ticks = False

	if "-r" in sys.argv:
		print("Data recieved debug mode on")
		dataDebug = True
	else:
		dataDebug = False

	SOCKETS = set()
	game = Game(None,debug=movementDebug)
	print("Game object initiated")

	asyncio.ensure_future(GameLoop(ticks))

	start_server = websockets.serve(socketHandle,"0.0.0.0",1234)
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()