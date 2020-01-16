from player import Player
from entity import Entity
from projectiles import *
import json

class Game():
	def __init__(self,map,debug=False):
		"""Game object that handles all entities

		Args:
			map (:obj:`list` of :obj:`dict`): List of entities represented by dictionaries
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
		self.walls = [Entity(0,480,(480,50),"wall",gravity=False),
					  Entity(480,0,(50,480),"wall",gravity=False)]
		self.projectiles = []

		self.debug = debug

	def addPlayer(self,ip):
		self.players[ip] = Player(ip,200,200)
		self.entities += [self.players[ip]]

	def removePlayer(self,ip):
		del self.players[ip]

	def isPlayer(self,ip):
		if self.players[ip] != None:
			return True
		else:
			return False

	def updatePlayer(self,ip,data):
		if self.isPlayer(ip):
			print("game:",data)
			self.players[ip].update(data,self.debug)

	def tick(self):
		for e in self.entities:
			if e.dead == False:
				e.tick(self.walls,self.projectiles,debug=self.debug)
			else:
				del e


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
							 "x":e.x,
							 "y":e.y,
							 "bottom":e.bottom,
							 "right":e.right}]
			for x in e.sounds: retSounds += [x]
			e.clearSounds()

		return json.dumps({"type":"render","data":{"entities":retEntities,"sounds":retSounds}})