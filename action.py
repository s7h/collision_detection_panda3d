from panda3d.core import Material,LRotationf,NodePath  
from direct.showbase.DirectObject import DirectObject
from direct.interval.FunctionInterval import Func,Wait
from direct.interval.MetaInterval import Sequence,Parallel
from direct.task.Task import Task
from direct.interval.LerpInterval import LerpFunc
from panda3d.core import Vec3,Vec4,BitMask32
ACCEL = 70         # Acceleration in ft/sec/sec
MAX_SPEED = 5      # Max speed in ft/sec
MAX_SPEED_SQ = MAX_SPEED ** 2  # Squared to make it easier to use lengthSquared
                               # Instead of length
UP = Vec3(0,0,1)   # We need this vector a lot, so its better to just have one
                   # instead of creating a new one every time we need it

class Action(DirectObject):

	ui = None 
	cTrav = None
	cHandler = None
	col = None
  	def __init__(self,ui,col):
		# Some constants for the program
		
		self.ui = ui
		self.cTrav = col.cTrav
		self.cHandler = col.cHandler
		self.col = col
	def start(self):
    		# The maze model also has a locator in it for where to start the ball
    		# To access it we use the find command
		
    		startPos = self.ui.maze.find("**/start").getPos()
    		self.ui.ballRoot.setPos(startPos)   # Set the ball in the starting position
    		self.ballV = Vec3(0,0,0)         # Initial velocity is 0
    		self.accelV = Vec3(0,0,0)        # Initial acceleration is 0
    
    		# For a traverser to actually do collisions, you need to call
    		# traverser.traverse() on a part of the scene. Fortunatly, base has a
    		# task that does this for the entire scene once a frame. This sets up our
    		# traverser as the one to be called automatically
    		base.cTrav = self.cTrav

    		# Create the movement task, but first make sure it is not already running
    		taskMgr.remove("rollTask")
    		self.mainLoop = taskMgr.add(self.rollTask, "rollTask")
    		self.mainLoop.last = 0

    	# This is the task that deals with making everything interactive
  	def rollTask(self, task):
    		# Standard technique for finding the amount of time since the last frame
    		dt = task.time - task.last
    		task.last = task.time
	
    		# If dt is large, then there has been a # hiccup that could cause the ball
    		# to leave the field if this functions runs, so ignore the frame
    		if dt > .2: return Task.cont   

    		# The collision handler collects the collisions. We dispatch which function
    		# to handle the collision based on the name of what was collided into
    		for i in range(self.cHandler.getNumEntries()):
      			entry = self.cHandler.getEntry(i)
      			name = entry.getIntoNode().getName()
			print(name)
      			if   name == "wall_collide":   self.wallCollideHandlerAction(entry)
      			elif name == "ground_collide": self.groundCollideHandlerAction(entry)
      			elif name == "loseTrigger":    self.loseGame(entry)

    			# Read the mouse position and tilt the maze accordingly
    		if base.mouseWatcherNode.hasMouse():
      			mpos = base.mouseWatcherNode.getMouse() # get the mouse position
      			self.ui.maze.setP(mpos.getY() * -10)
      			self.ui.maze.setR(mpos.getX() * 10)

    		# Finally, we move the ball
    		# Update the velocity based on acceleration
    		self.ballV += self.accelV * dt * ACCEL
    		# Clamp the velocity to the maximum speed
    		if self.ballV.lengthSquared() > MAX_SPEED_SQ:
      			self.ballV.normalize()
      			self.ballV *= MAX_SPEED
    		# Update the position based on the velocity
    		self.ui.ballRoot.setPos(self.ui.ballRoot.getPos() + (self.ballV * dt))
		
    		# This block of code rotates the ball. It uses something called a quaternion
    		# to rotate the ball around an arbitrary axis. That axis perpendicular to
    		# the balls rotation, and the amount has to do with the size of the ball
    		# This is multiplied on the previous rotation to incrimentally turn it.
    		prevRot = LRotationf(self.ui.ball.getQuat())
    		axis = UP.cross(self.ballV)
    		newRot = LRotationf(axis, 45.5 * dt * self.ballV.length())
    		self.ui.ball.setQuat(prevRot * newRot)
    
    		return Task.cont       # Continue the task indefinitely

	# If the ball hits a hole trigger, then it should fall in the hole.
	# This is faked rather than dealing with the actual physics of it.
	def loseGame(self, entry):
    		# The triggers are set up so that the center of the ball should move to the
    		# collision point to be in the hole
    		toPos = entry.getInteriorPoint(render)
    		taskMgr.remove('rollTask')  # Stop the maze task

    		# Move the ball into the hole over a short sequence of time. Then wait a
    		# second and call start to reset the game
    		Sequence(
      		  Parallel(
      		  LerpFunc(self.ui.ballRoot.setX, fromData = self.ui.ballRoot.getX(),
               	  toData = toPos.getX(), duration = .1),
      		LerpFunc(self.ui.ballRoot.setY, fromData = self.ui.ballRoot.getY(),
               	  toData = toPos.getY(), duration = .1),
      		LerpFunc(self.ui.ballRoot.setZ, fromData = self.ui.ballRoot.getZ(),
                  toData = self.ui.ballRoot.getZ() - .9, duration = .2)),
		Func(self.ui.show_message, "Try Again!"),
      		Wait(1),
		Func(self.ui.show_message, ""),
      		Func(self.start)).start()
	def groundCollideHandlerAction(self, colEntry):
    		# Set the ball to the appropriate Z value for it to be exactly on the ground
    		newZ = colEntry.getSurfacePoint(render).getZ()
    		self.ui.ballRoot.setZ(newZ+.4)
    		print("coll")	
    		# Find the acceleration direction. First the surface normal is crossed with
    		# the up vector to get a vector perpendicular to the slope
    		norm = colEntry.getSurfaceNormal(render)
    		accelSide = norm.cross(UP)
    		# Then that vector is crossed with the surface normal to get a vector that
    		# points down the slope. By getting the acceleration in 3D like this rather
    		# than in 2D, we reduce the amount of error per-frame, reducing jitter
    		self.accelV = norm.cross(accelSide)

	# This function handles the collision between the ball and a wall
  	def wallCollideHandlerAction(self, colEntry):
    		# First we calculate some numbers we need to do a reflection
    		norm = colEntry.getSurfaceNormal(render) * -1 # The normal of the wall
    		curSpeed = self.ballV.length()                # The current speed
    		inVec = self.ballV / curSpeed                 # The direction of travel
    		velAngle = norm.dot(inVec)                    # Angle of incidance
    		hitDir = colEntry.getSurfacePoint(render) - self.ui.ballRoot.getPos()
    		hitDir.normalize()                            
    		hitAngle = norm.dot(hitDir)   # The angle between the ball and the normal
    		print("done")	
    		# Ignore the collision if the ball is either moving away from the wall
    		# already (so that we don't accidentally send it back into the wall)
    		# and ignore it if the collision isn't dead-on (to avoid getting caught on
    		# corners)
   		if velAngle > 0 and hitAngle > .995:
      		# Standard reflection equation
      			reflectVec = (norm * norm.dot(inVec * -1) * 2) + inVec
        
      			# This makes the velocity half of what it was if the hit was dead-on
      			# and nearly exactly what it was if this is a glancing blow
      			self.ballV = reflectVec * (curSpeed * (((1-velAngle)*.5)+.5))
      			# Since we have a collision, the ball is already a little bit buried in
      			# the wall. This calculates a vector needed to move it so that it is
      			# exactly touching the wall
      			disp = (colEntry.getSurfacePoint(render) -
              			colEntry.getInteriorPoint(render))
      			newPos = self.ui.ballRoot.getPos() + disp
      			self.ui.ballRoot.setPos(newPos)

  		# Finally, create an instance of our class and start 3d rendering
	


