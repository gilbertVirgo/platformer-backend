import asyncio
import websockets
import json
import sys
from game import Game

DATA_DEBUG = False
SOCKETS = set()

async def recieve(websocket,debug):
	data = await websocket.recv()
	if debug: print("DATA RECIEVED:",data,"FROM:",websocket.remote_address)
	return data

async def socketHandle(websocket,path): # DATA_DEBUG is GLOBAL because you can't pass parameters to socketHandle
	print("socketHandle entered:",websocket.remote_address)
	SOCKETS.add(websocket)
	print("Awaiting id")
	data = await recieve(websocket,DATA_DEBUG) 
	data = json.loads(data)
	data = data["data"]
	print("Got id",data["id"])

	socketID = data["id"] # LOCAL variable to keep socket id

	print("Adding player:",data["id"])
	GAME.addPlayer(data["id"])
	print("Player added")

	present = True
	while present:
		try:
			data = await recieve(websocket,DATA_DEBUG)
			data = json.loads(data)
			data = data["data"]
			GAME.updatePlayer(data["id"],data["profile"])
			if DATA_DEBUG: print(data)
		except (ConnectionResetError, websockets.exceptions.ConnectionClosed):
			present = False
		except:
			print("Error",sys.exc_info())

	SOCKETS.remove(websocket)
	GAME.removePlayer(socketID)
	print("Player",socketID,"left")
	websocket.close()

@asyncio.coroutine
async def GameLoop(ticks,movementDebug):
	continueGame = True

	print("Loop entering")

	while continueGame:
		ret = GAME.returnRender()
		for websocket in SOCKETS:
			try:
				await websocket.send(ret)
			except KeyboardInterrupt:
				continueGame = False
			except:
				# connection is probably closed, do nothing as that's handled in socketHandle
				pass

		GAME.tick()

		if ticks: print("tick")
		await asyncio.sleep(1/30)

	print("Exiting")
	sys.exit()

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
		DATA_DEBUG = True
	else:
		DATA_DEBUG = False

	mapFile = open("levels/template.json")
	mapFileContents = mapFile.readlines()
	mapFile.close()
	"".join(mapFileContents)
	gameMap = json.loads("".join(mapFileContents))

	try:
		gameMap["size"]
		gameMap["entities"]
		GAME = Game(gameMap,debug=movementDebug)
		print("Game object initiated")
		continueGame = True

	except KeyError:
		continueGame = False
		print("Invalid map")

	asyncio.ensure_future(GameLoop(ticks,movementDebug))

	start_server = websockets.serve(socketHandle,"0.0.0.0",1234)
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()