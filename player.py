from entity import Entity

class Player(Entity):
	def __init__(self,ip,x=200,y=200):

		Entity.__init__(self,x,y,(32,64),"player")
		self.ip = ip

		# LEFT RIGHT UP DOWN ATTACK PICKUP
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

	def update(self,keys):
		self.buttons = keys

	def tick(self,walls,projectiles):

		for p in projectiles:
			if self.isCollidingWith(p):
				self.dead = True
				p.dead = True

		if self.buttons["jump"]:
			if not self.held["jump"]:
				self.velocity[1] -= 10
				self.held["jump"] = True
		else:
			self.held["jump"] = False

		if self.buttons["left"]:
			if not self.held["left"]:
				self.velocity[0] -= 10
				self.held["left"] = True
				self.facing = "left"
		else:
			self.held["left"] = False
			self.velocity[0] += 10

		if self.buttons["right"]:
			if not self.held["right"]:
				self.velocity[0] += 10
				self.held["right"] = True
				self.facing = "right"
		else:
			self.held["right"] = False
			self.velocity[0] -= 10

		if self.buttons["down"]:
			if not self.held["down"]:
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

		Entity.tick(self,walls)

