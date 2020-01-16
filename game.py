from player import Player
from entity import Entity
from projectiles import *
import json

class Game():
	def __init__(self,map):
		self.map = map
		self.entities = []
		self.players = {}
		self.walls = [Entity(0,480,(400,50),"wall",gravity=False),
					  Entity(480,0,(50,480),"wall",gravity=False)]
		self.projectiles = []

	def addPlayer(self,ip):
		self.players[ip] = Player(ip,200,200)
		self.entities += [self.players[ip]]

	def removePlayer(self,ip):
		del self.players[ip]

	def isPlayer(self,ip):
		if self.players[ip]:
			return True
		else:
			return False

	def updatePlayer(self,ip,data):
		if self.isPlayer(ip):
			self.players{ip}.update(data)

	def tick(self):
		for e in self.entities:
			if e.dead = False:
				e.tick(self.walls,self.projectiles)
			else:
				del e

	def returnRender(self):
		ret = []
		for e in self.entities:
			ret += [{"type":e.type,
					 "x":e.x,
					 "y":e.y,
					 "bottom":e.bottom,
					 "right":e.right
					 "sounds":e.sounds}]
		return json.dumps({"type":"render","data":ret})