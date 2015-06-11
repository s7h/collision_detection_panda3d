from panda3d.core import AmbientLight,DirectionalLight
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Material
from panda3d.core import TextNode
import sys
class UI(DirectObject):
	def __init__(self):
		
		self.root = render.attachNewNode("Root")

		# This code puts the standard title and instruction text on screen
    		self.title = OnscreenText(text="Ball In Maze",
                              		style=1, fg=(1,1,1,1),
                              		pos=(0.7,-0.95), scale = .07)
    		self.instructions = OnscreenText(text="Press Esc to Quit",
                                     		pos = (-1.3, .95), fg=(1,1,1,1),
                                     		align = TextNode.ALeft, scale = .05)
		self.central_msg = OnscreenText(text="",
      				pos = (0, 0), fg=(1, 1, 0, 1),
      				scale = .1
    						)
    		self.central_msg.hide()
    
    		self.accept("escape", sys.exit)        # Escape quits
    		base.disableMouse()                    # Disable mouse-based camera control
    		camera.setPosHpr(0, 0, 25, 0, -90, 0)  # Place the camera

    		# Load the maze and place it in the scene
    		self.maze = loader.loadModel("models/maze")
    		self.maze.reparentTo(render)

		# Load the ball and attach it to the scene
    		# It is on a root dummy node so that we can rotate the ball itself without
    		# rotating the ray that will be attached to it
    		self.ballRoot = render.attachNewNode("ballRoot")
    		self.ball = loader.loadModel("models/ball")
    		self.ball.reparentTo(self.ballRoot)
		# This section deals with lighting for the ball. Only the ball was lit
    		# because the maze has static lighting pregenerated by the modeler
    		ambientLight = AmbientLight("ambientLight")
    		ambientLight.setColor(Vec4(.55, .55, .55, 1))
    		directionalLight = DirectionalLight("directionalLight")
    		directionalLight.setDirection(Vec3(0, 0, -1))
    		directionalLight.setColor(Vec4(0.375, 0.375, 0.375, 1))
    		directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
    		self.ballRoot.setLight(render.attachNewNode(ambientLight))
    		self.ballRoot.setLight(render.attachNewNode(directionalLight))
    
    		# This section deals with adding a specular highlight to the ball to make
    		# it look shiny
    		m = Material()
    		m.setSpecular(Vec4(1,1,1,1))
    		m.setShininess(96)
    		self.ball.setMaterial(m, 1)
	def show_message(self, message=''):
    		if message:
      			self.central_msg.setText(message)
      			self.central_msg.show()
    		else:
      			self.central_msg.hide()



		

