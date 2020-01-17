from entity import Entity

class Wall(Entity):
	def __init__(self,x,y,size):
		Entity.__init__(self,x,y,size,"wall",
						gravity=False)

class Platform(Entity):
	def __init__(self,x,y,size):
		Entity.__init__(self,x,y,size,"platform",
						gravity=False)