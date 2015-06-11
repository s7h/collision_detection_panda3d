# Author: Shao Zhang, Phil Saltzman
# Last Updated: 5/2/2005
# 
# This tutorial shows how to detect and respond to collisions. It uses solids
# create in code and the egg files, how to set up collision masks, a traverser,
# and a handler, how to detect collisions, and how to dispatch function based
# on the collisions. All of this is put together to simulate a labyrinth-style
# game

from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Material,LRotationf,NodePath
from panda3d.core import BitMask32
from graphics import UI
from action import Action
class Collision():
  def __init__(self,ui):
	
    self.ui = ui;
   
    # Most times, you want collisions to be tested against invisible geometry
    # rather than every polygon. This is because testing against every polygon
    # in the scene is usually too slow. You can have simplified or approximate
    # geometry for the solids and still get good results.
    # 
    # Sometimes you'll want to create and position your own collision solids in
    # code, but it's often easier to have them built automatically. This can be
    # done by adding special tags into an egg file. Check maze.egg and ball.egg
    # and look for lines starting with <Collide>. The part is brackets tells
    # Panda exactly what to do. Polyset means to use the polygons in that group
    # as solids, while Sphere tells panda to make a collision sphere around them
    # Keep means to keep the polygons in the group as visable geometry (good
    # for the ball, not for the triggers), and descend means to make sure that
    # the settings are applied to any subgroups.
    # 
    # Once we have the collision tags in the models, we can get to them using
    # NodePath's find command

    # Find the collision node named wall_collide
    self.walls = self.ui.maze.find("**/wall_collide")

    # Collision objects are sorted using BitMasks. BitMasks are ordinary numbers
    # with extra methods for working with them as binary bits. Every collision
    # solid has both a from mask and an into mask. Before Panda tests two
    # objects, it checks to make sure that the from and into collision masks
    # have at least one bit in common. That way things that shouldn't interact
    # won't. Normal model nodes have collision masks as well. By default they
    # are set to bit 20. If you want to collide against actual visable polygons,
    # set a from collide mask to include bit 20
    # 
    # For this example, we will make everything we want the ball to collide with
    # include bit 0
    self.walls.node().setIntoCollideMask(BitMask32.bit(0))
    # CollisionNodes are usually invisible but can be shown. Uncomment the next
    # line to see the collision walls
    # self.walls.show()

    # We will now find the triggers for the holes and set their masks to 0 as
    # well. We also set their names to make them easier to identify during
    # collisions
    self.loseTriggers = []
    for i in range(6):
      trigger = self.ui.maze.find("**/hole_collide" + str(i))
      trigger.node().setIntoCollideMask(BitMask32.bit(0))
      trigger.node().setName("loseTrigger")
      self.loseTriggers.append(trigger)
      # Uncomment this line to see the triggers
      # trigger.show()

    # Ground_collide is a single polygon on the same plane as the ground in the
    # maze. We will use a ray to collide with it so that we will know exactly
    # what height to put the ball at every frame. Since this is not something
    # that we want the ball itself to collide with, it has a different
    # bitmask.
    self.mazeGround = self.ui.maze.find("**/ground_collide")
    self.mazeGround.node().setIntoCollideMask(BitMask32.bit(1))
    
    
    # Find the collison sphere for the ball which was created in the egg file
    # Notice that it has a from collision mask of bit 0, and an into collison
    # mask of no bits. This means that the ball can only cause collisions, not
    # be collided into
    self.ballSphere = self.ui.ball.find("**/ball")
    self.ballSphere.node().setFromCollideMask(BitMask32.bit(0))
    self.ballSphere.node().setIntoCollideMask(BitMask32.allOff())

    # No we create a ray to start above the ball and cast down. This is to
    # Determine the height the ball should be at and the angle the floor is
    # tilting. We could have used the sphere around the ball itself, but it
    # would not be as reliable
    self.ballGroundRay = CollisionRay()     # Create the ray
    self.ballGroundRay.setOrigin(0,0,10)    # Set its origin
    self.ballGroundRay.setDirection(0,0,-1) # And its direction
    # Collision solids go in CollisionNode
    self.ballGroundCol = CollisionNode('groundRay') # Create and name the node
    self.ballGroundCol.addSolid(self.ballGroundRay) # Add the ray
    self.ballGroundCol.setFromCollideMask(BitMask32.bit(1)) # Set its bitmasks
    self.ballGroundCol.setIntoCollideMask(BitMask32.allOff())
    # Attach the node to the ballRoot so that the ray is relative to the ball
    # (it will always be 10 feet over the ball and point down)
    self.ballGroundColNp = self.ui.ballRoot.attachNewNode(self.ballGroundCol)
    # Uncomment this line to see the ray
    # self.ballGroundColNp.show()

    # Finally, we create a CollisionTraverser. CollisionTraversers are what
    # do the job of calculating collisions
    self.cTrav = CollisionTraverser()
    # Collision traverservs tell collision handlers about collisions, and then
    # the handler decides what to do with the information. We are using a
    # CollisionHandlerQueue, which simply creates a list of all of the
    # collisions in a given pass. There are more sophisticated handlers like
    # one that sends events and another that tries to keep collided objects
    # apart, but the results are often better with a simple queue
    self.cHandler = CollisionHandlerQueue()
    # Now we add the collision nodes that can create a collision to the
    # traverser. The traverser will compare these to all others nodes in the
    # scene. There is a limit of 32 CollisionNodes per traverser
    # We add the collider, and the handler to use as a pair
    self.cTrav.addCollider(self.ballSphere, self.cHandler)
    self.cTrav.addCollider(self.ballGroundColNp, self.cHandler)

    # Collision traversers have a built in tool to help visualize collisions.
    # Uncomment the next line to see it.
    # self.cTrav.showCollisions(render)
    
    
    # Finally, we call start for more initialization
    

  
  # This function handles the collision between the ray and the ground
  # Information about the interaction is passed in colEntry
  
  

