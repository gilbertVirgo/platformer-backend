
class Entity():
	def __init__(self,x,y,size,entType,
				 gravity=True,
				 velocity=[0,0],
				 destroyOnImpact=False,
				 mod=None):
		self.x = x
		self.y = y
		self.right = size[0] + self.x
		self.bottom = size[1] + self.y
		self.size = size

		# Types:
		# player
		# wall
		# bullet

		self.type = entType
		self.gravity = gravity
		self.velocity = [0,0]
		self.destroyOnImpact = destroyOnImpact
		self.dead = False
		self.sounds = []
		self.onGround = False
		self.mod = mod

	def _printinfo(self):
		print({"type":self.type,
			 "x":self.x,
			 "y":self.y,
			 "bottom":self.bottom,
			 "right":self.right,
			 "velocity":self.velocity,
			 "onGround":self.onGround})

	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
		self.right += self.velocity[0]
		self.bottom += self.velocity[1]

	def modVelocity(self,x,y):
		self.velocity[0] += x
		self.velocity[1] += y

	def clearSounds(self):
		self.sounds = []

	def tick(self,walls,debug=False,**kwargs):
		"""
		
		Returns:
			(dict): collisions 
		"""
		# if debug: self._printinfo()

		if self.gravity:
			self.modVelocity(0,1)

		collision = False
		collisions = {"top":False,
					  "right":False,
					  "bottom":False,
					  "left":False}

		# collisions
		if walls != None and self.type not in ["wall","platform"]:
			newTL = [self.x+self.velocity[0], self.y+self.velocity[1]]
			newBR = [self.right+self.velocity[0], self.bottom+self.velocity[1]]

			for w in walls:

				# if either entity corner is between wall's x, or entity is fully around wall's x
				if ((newTL[0] > w.x and newTL[0] < w.right) or 
					(newBR[0] > w.x and newBR[0] < w.right) or
					(newTL[0] <= w.x and newBR[0] >= w.right)):

					# entity top colliding
					if ((newTL[1] < w.bottom and self.y >= w.bottom)):
						
						if debug: print("\nCollision: 1")
						if debug: w._printinfo()
						if debug: self._printinfo()

						self.y = w.bottom
						self.bottom = w.bottom + self.size[1]
						self.velocity[1] = 0
						collisions["top"] = True

						newTL[1] = self.y
						newBR[1] = self.bottom

						if debug: self._printinfo()
						if debug: print()

					# entity bottom colliding
					if ((newBR[1] > w.y and self.bottom <= w.y)):
						
						if debug: print("\nCollision: 2")
						if debug: w._printinfo()
						if debug: self._printinfo()

						self.y = w.y - self.size[1]
						self.bottom = w.y
						self.velocity[1] = 0
						collisions["bottom"] = True

						newTL[1] = self.y
						newBR[1] = self.bottom

						if debug: self._printinfo()
						if debug: print()

				# if either entity corner is between wall's y, or entity is fully around wall's y
				if ((newTL[1] > w.y and newTL[1] < w.bottom) or 
					(newBR[1] > w.y and newBR[1] < w.bottom) or 
					(newTL[1] <= w.y and newBR[1] >= w.bottom)):

					# entity left colliding
					if (newTL[0] < w.right and self.x >= w.right):

						if debug: print("\nCollision: 3")
						if debug: w._printinfo()
						if debug: self._printinfo()

						self.x = w.right
						self.right = w.right + self.size[0]
						self.velocity[0] = 0
						collisions["left"] = True

						newTL[0] = self.x
						newBR[0] = self.right

						if debug: self._printinfo()
						if debug: print()

					# entity right colliding
					if (newBR[0] > w.x and self.right <= w.x):
						
						if debug: print("\nCollision: 4")
						if debug: w._printinfo()
						if debug: self._printinfo()

						self.x = w.x - self.size[0]
						self.right = w.x
						self.velocity[0] = 0
						collisions["right"] = True

						newTL[0] = self.x
						newBR[0] = self.right

						if debug: self._printinfo()
						if debug: print()


		if not all(value == False for value in collisions.values()):
			if self.destroyOnImpact: 
				self.dead = True

		if collisions["bottom"]:
			self.onGround = True
		else:
			self.onGround = False

		self.move()
		return collisions

	def isCollidingWith(self,entity):
		if (((self.x > e.x and self.x < e.right) or (self.right > e.x and self.x < e.right)) and
			((self.y > e.y and self.y < e.bottom) or (self.bottom > e.y and self.y < e.bottom))):
			return True
		else:
			return False

