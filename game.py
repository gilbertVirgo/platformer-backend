from player import Player
from entity import Entity
import json

class Game():
	def __init__(self,map):
		self.map = map
		self.entities = []
		self.players = {}
		self.walls = [Entity(0,480,(400,50),"wall",gravity=False),
					  Entity(480,0,(50,480),"wall",gravity=False)]

	def addPlayer(self,ip):
		self.players[ip] = Player(ip,200,200)
		self.entities += [self.players[ip]]

	def removePlayer(self,ip):
		self.entities.remove(self.players[ip])
		del self.players[ip]

	def isPlayer(self,ip):
		if self.players[ip]:
			return True
		else:
			return False

	def tick(self):
		for e in self.entities:
			e.tick(self.walls)

	def returnRender(self):
		ret = []
		for e in self.entities:
			ret += [{"type":e.type,
					 "x":e.x,
					 "y":e.y,
					 "bottom":e.bottom,
					 "right":e.right}]
		return json.dumps({"type":"render","data":ret})