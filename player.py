from entity import Entity

class Player(Entity):
	def __init__(self,ip,x=200,y=200):

		Entity.__init__(self,x,y,(32,64),"player")
		self.ip = ip

		# LEFT RIGHT UP DOWN ATTACK INTERACT
		self.buttons = {"jump":False,
						"left":False,
						"down":False,
						"right":False,
						"attack":False,
						"interact":False}

		self.held = {"jump":False,
					 "left":False,
					 "down":False,
					 "right":False,
					 "attack":False,
					 "interact":False}

		self.facing = "right"
		self._movementModifier = 10
		self._jumpModifier = 30

	def update(self,keys,debug=False,**kwargs):
		if debug: print("player:",keys)
		self.buttons = keys

	def tick(self,walls,projectiles,debug=False,**kwargs):

		# if debug: self._printinfo()
		
		for p in projectiles:
			if self.isCollidingWith(p):
				self.dead = True
				p.dead = True

		# For left and right:
		# If pushed and was not previously pushed:
		# 	Add movementModifier in appropriate direction
		# 	Note as currently pushed
		# 	Change facing direction
		# If not pushed:
		# 	if both directions are held:
		#		take away movement modifier

		if self.buttons["left"]:
			if not self.held["left"]:
				if debug: print("left down")
				self.velocity[0] -= self._movementModifier
				self.held["left"] = True
				self.facing = "left"
		else:
			if self.held["left"] and self.held["right"]:
				self.velocity[0] += self._movementModifier
			elif self.held["left"]:
				self.velocity[0] = 0
			self.held["left"] = False

		if self.buttons["right"]:
			if not self.held["right"]:
				if debug: print("right down")
				self.velocity[0] += self._movementModifier
				self.held["right"] = True
				self.facing = "right"
		else:
			if self.held["right"] and self.held["left"]:
				self.velocity[0] -= self._movementModifier
			elif self.held["right"]:
				self.velocity[0] = 0
			self.held["right"] = False

		if self.buttons["jump"]:
			if not self.held["jump"] and self.onGround:
				if debug: print("jump down")
				self.velocity[1] -= self._jumpModifier
				self.held["jump"] = True
				self.onGround = False
		else:
			self.held["jump"] = False

		if self.buttons["down"]:
			if not self.held["down"]:
				if debug: print("down down")
				self.held["down"] = True
		else:
			self.held["down"] = False

		if self.buttons["attack"]:
			if not self.held["attack"]:
				pass
				self.held["attack"] = True
		else:
			self.held["attack"] = False

		if self.buttons["interact"]:
			if not self.held["interact"]:
				pass
				self.held["interact"] = True
		else:
			self.held["interact"] = False

		collisions = Entity.tick(self,walls,debug=debug)

		if collisions["right"] and self.held["right"]:
			self.held["right"] = False
		if collisions["left"] and self.held["left"]:
			self.held["left"] = False