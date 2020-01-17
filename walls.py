from entity import Entity

class Wall(Entity):
	def __init__(self,x,y,size,uid):
		Entity.__init__(self,x,y,size,"wall",uid,
						gravity=False)

class Platform(Entity):
	def __init__(self,x,y,size,uid,sprite=None):
		Entity.__init__(self,x,y,size,"platform",uid,
						gravity=False,sprite=None)