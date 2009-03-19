import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

        sideShift=0

        self.backgroundMusic = app.music['bg-2']

        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(sideShift+-30,0,10), angle=90)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(sideShift+-26,2,10), angle=90)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(sideShift+-22,4,10), angle=90)
        makeUpDownRamp(app, "name", self.offset + ogre.Vector3(sideShift+-18,6,10), angle=90)
 
        makeGear(app,"name",self.offset+ogre.Vector3(sideShift+0,5,10))

        
        
        for i in range(-20,0,2):
            makeDomino(app,"name",self.offset+ogre.Vector3(sideShift+0,9.3,-22-i),angle=-15)
        for i in range(0,10,2):
            makeDomino(app,"name",self.offset+ogre.Vector3(sideShift+0,9+2+0.5*i,-22-i))
        makeBell(app,"name",self.offset+ogre.Vector3(sideShift+0,9+8.5,-22-12))
        
        lock2=makeLevelLock(app,self.offset)
        c2 = makeUnlockKey(app,self.offset+ogre.Vector3(sideShift+0,9+10,-22-16.7))
        c2.quant=8
        c2.key=lock2
        lock2.sources.append(c2)
        (leftDoor, rightDoor) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,0,46))
        leftDoor.lock(app._world,lock2)
        rightDoor.lock(app._world,lock2)



##        for i in range(0,6):
##            for j in range (0,5):
##                makeDomino(app,"name",self.offset+ogre.Vector3(30+2*j,1+i,0+2*i),angle=5)
##
##        makePlatform(app,"name",self.offset+ogre.Vector3(33,8,5+2*i))
##        c = makeUnlockKey(app,self.offset+ogre.Vector3(33,10,5+2*i))
##        c.quant=8
##        c.key=lock2
##        lock2.sources.append(c)
       
    def unload(self, app):
        pass
