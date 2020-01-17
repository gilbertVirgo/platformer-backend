from player import Player
from entity import Entity
from projectiles import *
from walls import *
import json

class Game():
	def __init__(self,gameMap,debug=False):
		"""Game object that handles all entities

		Args:
			gameMap (dict): Dictionary of all relevant map information
			debug (bool): Runs game in debug mode

		Attributes:
			entities (:obj:`list` of :obj:`Entity`): List of all entities
			players (dict of :obj:`Player`): Dictionary of all players, keys are ip/port combinations
			walls (:obj:`list` of  :obj:`Entity`): List of all walls, generated from `map` arg
			projectiles (:obj:`list of :obj:`Entity`): List of bullet entities
			debug (bool): Determines if game is run in debug mode
		
		"""
		self.entities = []
		self.players = {}
		self.walls = []
		self.projectiles = []
		self.gameMap = gameMap

		self.debug = debug
		self.uidCounter = 0
		self.processLevel()

	def makeUID(self):
		self.uidCounter += 1
		return self.uidCounter

	def processLevel(self):
		print("gameMap, size:",self.gameMap["size"])
		print(self.gameMap)
		size = self.gameMap["size"]

		self.walls += [Wall(-50,-50,[50,size[1]+100],self.makeUID()),			 			# Left wall
					   Wall(-50,-50,[size[0]+100,50],self.makeUID()),			 			# Top wall
					   Wall(-50,size[1],[size[0]+100,50],self.makeUID()),			 		# Bottom wall
					   Wall(size[0],-50,[50,size[1]+100],self.makeUID())]					# Right wall

		for e in self.gameMap["entities"]:
			if e["type"] == "platform":
				self.walls += [Platform(e["x"],e["y"],
										[int(e["size"][0]),int(e["size"][1])],
										self.makeUID(),
										sprite=e["sprite"])]

		for e in self.walls:
			e._printinfo()


	def addPlayer(self,ip):
		self.players[ip] = Player(ip,self.makeUID(),200,200)
		self.entities += [self.players[ip]]

	def removePlayer(self,ip):
		print("deleting",ip)
		self.entities.remove(self.players[ip])
		del self.players[ip]

	def isPlayer(self,ip):
		if self.players[ip] != None:
			return True
		else:
			return False

	def updatePlayer(self,ip,data):
		if self.isPlayer(ip):
			self.players[ip].update(data,self.debug)

	def tick(self):
		for e in self.entities:
			if e.dead == False:
				e.tick(self.walls,self.projectiles,debug=self.debug)
			else:
				del e
			if e.type == "player":
				if e.shot == True:
					e.shot = False
					if e.facing == "left":
						pass



	def returnRender(self):
		"""Returns all data required by client to render screen, and also removes sounds from enitities

		Args:
			None

		Returns:
			Json string in the format {"type":"render","data":{"entities":all_entities,"sounds":all_sounds}} 
		
		"""

		retEntities = []
		retSounds = []

		for e in self.entities:
			retEntities += [{"type":e.type,
							 "uid":e.uid,
							 "x":e.x,
							 "y":e.y,
							 "bottom":e.bottom,
							 "right":e.right,
							 "size":e.size,
							 "sprite":e.sprite}]
			for x in e.sounds: retSounds += [x]
			e.clearSounds()
		# print (retEntities)
		return json.dumps({"type":"render","data":{"entities":retEntities,"sounds":retSounds}})