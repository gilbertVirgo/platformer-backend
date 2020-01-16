import json
from entity import Entity

class Player(Entity):
	def __init__(self,ip,x=200,y=200):

		Entity.__init__(self,x,y,(32,64),"player")
		self.ip = ip

		# LEFT RIGHT UP DOWN ATTACK PICKUP
		self.buttons = {"up":False,
						"left":False,
						"down":False,
						"right":False,
						"attack":False,
						"pickup":False}

	def update(self,keys):
		self.buttons = json.loads(keys)

	# def tick():
	# 	if self.buttons.up:
	# 		self.y += 10
	# 	if self.buttons.left:
	# 		self.x -= 10
	# 	if self.buttons.right:
	# 		self.x += 10
	# 	if self.buttons.down:
	# 		self.y += 10
	# 	if self.buttons.attack:
	# 		pass
	# 	if self.buttons.pickup:
	# 		pass

