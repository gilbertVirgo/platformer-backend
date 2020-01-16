from entity import Entity

class Bullet(Entity):
	def __init__(self,x,y,velocity):
		Entity.__init__(self,x,y,(8,4),"bullet",gravity=False,velocity=velocity,destroyOnWall=True)