import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

        self.backgroundMusic = app.music['bg-4']

        for i in range(0,4):
            for j in range(0,i):
                makeMetalCrate(app,"name",self.offset + ogre.Vector3(0,j*2,-37+i*3))

        makePlatform(app,"name",self.offset + ogre.Vector3(0,16.5,-17))
        makePlatform(app,"name",self.offset + ogre.Vector3(0,11,-22))


##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,0,-44), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,2,-40), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,4,-36), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,6,-32), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,8,-28), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,10,-24), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,12,-20), angle=0)
##        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,14,-16), angle=0)
        makeBridge(app, "name", self.offset + ogre.Vector3(0,16.5,-8.5))
        makeTiltingPlatform(app,"name",self.offset + ogre.Vector3(0,15.5,0))

        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,0,44), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,2,40), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,4,36), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,6,32), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,8,28), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,10,24), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,12,20), angle=180)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(0,14,16), angle=180)
        makeBridge(app, "name", self.offset + ogre.Vector3(0,16.5,8.5))



        (leftDoor2, rightDoor2) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,0,3.7))
        lock2=makeLevelLock(app,self.offset)
        c2 = makeUnlockKey(app,self.offset+ogre.Vector3(0,1,0))
        c2.quant=8
        c2.key=lock2
        lock2.sources.append(c2)
        leftDoor2.lock(app._world,lock2)
        rightDoor2.lock(app._world,lock2)

        (leftDoor3, rightDoor3) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,4.2,3.7))
        leftDoor3.lock(app._world,None)
        rightDoor3.lock(app._world,None)

##        (leftDoor3, rightDoor3) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,0,-3.5))
##        leftDoor3.lock(app._world,None)
##        rightDoor3.lock(app._world,None)
##        (leftDoor3, rightDoor3) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,4.2,-3.5))
##        leftDoor3.lock(app._world,None)
##        rightDoor3.lock(app._world,None)

        makeInnerWall(app,"name",self.offset + ogre.Vector3(-8,0,0),90)
        makeInnerWall(app,"name",self.offset + ogre.Vector3(8,0,0),90)
        makeInnerWall(app,"name",self.offset + ogre.Vector3(-6.1,0,-3.7),0)
        makeInnerWall(app,"name",self.offset + ogre.Vector3(0,0,-3.7),0)
        makeInnerWall(app,"name",self.offset + ogre.Vector3(6.1,0,-3.7),0)


        (leftDoor, rightDoor) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,0,50))
        leftDoor.lock(app._world,lock2)
        rightDoor.lock(app._world,lock2)

       
    def unload(self, app):
        pass
