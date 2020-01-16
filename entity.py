
class Entity():
	def __init__(self,x,y,size,entType,
				 gravity=True,
				 velocity=[0,0],
				 destroyOnWall=False):
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
		self.destroyOnWall = destroyOnWall
		self.dead = False

	def _printinfo(self):
		print({"type":self.type,
			 "x":self.x,
			 "y":self.y,
			 "bottom":self.bottom,
			 "right":self.right,
			 "velocity":self.velocity})

	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
		self.right += self.velocity[0]
		self.bottom += self.velocity[1]

	def modVelocity(self,x,y):
		self.velocity[0] += x
		self.velocity[1] += y

	def tick(self,walls,**kwargs):
		self._printinfo()

		if self.gravity:
			self.modVelocity(0,1)

		collision = False

		# collision
		if walls != None and self.type != "wall":
			newTL = [self.x+self.velocity[0],self.y+self.velocity[1]]
			newBR = [self.right+self.velocity[0],self.bottom+self.velocity[1]]

			for w in walls:

				# check if collided with up down left right in order, don't combine

				# if either corner is between wall's x corners
				if ((newTL[0] > w.x and newTL[0] < w.right) or (newBR[0] > w.x and newBR[0] < w.right) and
					# and old position is above or below wall
					(self.y > w.bottom or self.bottom < w.y)):

					# top colliding
					if (newTL[1] < w.bottom and newTL[1] > w.y):print("\nCollision: 1")
						self._printinfo()
						self.y = w.bottom
						self.bottom = w.bottom + self.size[1]
						self.velocity[1] = 0
						collision = True
						self._printinfo()
						print()

						if self.destroyOnWall: self.dead = True

					# bottom colliding
					if (newBR[1] < w.bottom and newBR[1] > w.y):

						print("\nCollision: 2")
						self._printinfo()
						self.y = w.y - self.size[1]
						self.bottom = w.y
						self.velocity[1] = 0
						collision = True
						self._printinfo()
						print()

						if self.destroyOnWall: self.dead = True

				# if either corner is between wall's y corners
				if ((newTL[1] > w.y and newTL[1] < w.bottom) or (newBR[1] > w.y and newBR[1] < w.bottom) and
					# and old position is left or right of wall
					(self.x > w.right or self.right < w.x)):
					# entity left colliding
					if (newTL[0] < w.right and newTL[0] > w.x):

						print("\nCollision: 3")
						self._printinfo()
						self.x = w.right
						self.right = w.right + self.size[0]
						self.velocity[0] = 0
						collision = True
						self._printinfo()
						print()

						if self.destroyOnWall: self.dead = True

					# entity right colliding
					if (newBR[0] < w.right and newBR[0] > w.x):
						
						print("\nCollision: 4")
						self._printinfo()
						self.x = w.x - self.size[0]
						self.right = w.x
						self.velocity[0] = 0
						collision = True
						self._printinfo()
						print()

						if self.destroyOnWall: self.dead = True

		self.move()

	def isCollidingWith(self,entity):
		if (((self.x > e.x and self.x < e.right) or (self.right > e.x and self.x < e.right)) and
			((self.y > e.y and self.y < e.bottom) or (self.bottom > e.y and self.y < e.bottom))):
			return True
		else:
			return False

