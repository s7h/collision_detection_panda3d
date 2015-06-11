# DETECTING , HANDLING AND RESPONDING TO COLLISIONS IN A MAZE GAME

This project is a work of Shao Zhang and Phil Saltzman; however, my team did a little tweak and redesigned 3D models in Blender and some 2D graphics in Photoshop for better UI. 


Collision plays an important role when it comes to 3D gaming. From simple 3D billiards game to sophisticated RPG games, collisions are everywhere. Collision detection allows for two objects to bump into each other and react. This includes not only sending messages for events, but also to keep the objects from passing through each other. Collision detection is a very powerful tool for immersion, but it is somewhat complex.

In this project a labyrinth-style game is used as an example to show how collisions are detected, handled and responded to in a 3D world. There are two ways to go about collision detection. One is to create special collision geometry, such as spheres and polygons, to determine collisions. The other is to allow collisions against all geometry. While the first is somewhat more complex and takes more effort to implement, it is much faster to execute and is a better long-term solution. For quick-and-dirty applications, though, collision with geometry can be a fine solution.

This project will demonstrate how collision detection works in panda3D and provide a simple implementation of its use. Panda3D is a 3D engine: a library of subroutines for 3D rendering and game development. We will use a high level programming language, Python to implement the game.



### Dependencies : ###

* Panda3D Game Engine
* TkInter GUI package
* Pygame cross-platform module
* PIL (Python Imaging Library)



### How to Run the project : ###

To run the project firstly install the panda3d SDK from [Panda3d.org](https://www.panda3d.org/download.php?sdk) for your respective platform. Then install all the dependencies that I have mentioned above.

Run the play.py file as follows

```
$> python play.py
```

![Screenshot](http://i58.tinypic.com/2chkklc.png)

Title Screen Soundtrack: 9-bit Expedition : [Lifeformed](https://lifeformed.bandcamp.com/)

