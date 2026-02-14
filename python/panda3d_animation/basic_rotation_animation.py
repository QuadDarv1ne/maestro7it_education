#!/usr/bin/env python
"""
Basic Rotation Animation Example
Demonstrates simple rotation animation using tasks
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.core import loadPrcFileData
import math

class BasicRotationAnimation(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Set window title
        loadPrcFileData('', 'window-title Basic Rotation Animation')
        
        # Disable mouse control to use our own camera
        self.disableMouse()
        
        # Create a cube
        try:
            self.cube = self.loader.loadModel("models/box")
        except:
            # Create a simple cube if model not found
            from panda3d.core import CardMaker
            cm = CardMaker("cube")
            cm.setFrame(-1, 1, -1, 1)
            self.cube = self.render.attachNewNode(cm.generate())
        self.cube.reparentTo(self.render)
        self.cube.setPos(0, 10, 0)
        self.cube.setColor(1, 0, 0, 1)  # Red color
        
        # Create another object to demonstrate different animation
        try:
            self.sphere = self.loader.loadModel("models/sphere")
        except:
            # Create a simple circle if model not found
            from panda3d.core import CardMaker
            cm = CardMaker("circle")
            cm.setFrame(-0.5, 0.5, -0.5, 0.5)
            self.sphere = self.render.attachNewNode(cm.generate())
        self.sphere.reparentTo(self.render)
        self.sphere.setPos(3, 10, 0)
        self.sphere.setColor(0, 0, 1, 1)  # Blue color
        
        # Set up the scene
        self.setBackgroundColor(0.2, 0.2, 0.4, 1)  # Dark blue background
        
        # Add a task to rotate the objects
        self.taskMgr.add(self.rotate_objects, "rotate_objects")
        
        # Position the camera
        self.camera.setPos(0, -15, 5)
        self.camera.lookAt(0, 0, 0)
        
        print("Basic Rotation Animation Running...")
        print("Press ESC to exit")
    
    def rotate_objects(self, task):
        # Rotate the cube around its Y-axis
        self.cube.setH(task.time * 50)  # Rotate 50 degrees per second
        
        # Rotate the sphere around its X-axis
        self.sphere.setP(task.time * 30)  # Rotate 30 degrees per second
        
        # Make the sphere also rotate around the center (orbital motion)
        angle = task.time * 0.5  # Slow orbital rotation
        radius = 3
        self.sphere.setX(math.sin(angle) * radius)
        self.sphere.setY(10 + math.cos(angle) * radius)
        
        return task.cont

# Run the application
if __name__ == "__main__":
    app = BasicRotationAnimation()
    app.run()