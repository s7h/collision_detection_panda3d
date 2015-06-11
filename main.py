
import direct.directbase.DirectStart
from graphics import UI
from collision import Collision
from action import Action
class Game():
	def __init__(self):
		self.ui = UI()
		self.col = Collision(self.ui)
		self.act = Action(self.ui,self.col)
		self.act.start()
		
w = Game()
run()
