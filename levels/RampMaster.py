import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):
#    def __init__(self, levelId):
#        BaseLevel.__init__(self, levelId)
##
##
##    def __del__(self):
##        BaseLevel.__del__(self)
##

    def load(self, app):
        self.backgroundMusic = app.music['bg-3']

        makeOnOffRamp(app, 'onramp', self.offset + ogre.Vector3(32, 0, -32))
        makeUpDownRamp(app, 'up', self.offset + ogre.Vector3(32, 0, -28))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(32, 2, -25))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(32, 2, -23))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(32, 2, -21))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(32, 2, -19))
        makeCornerRamp(app, 'corner', self.offset + ogre.Vector3(32, 2, -16))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(29, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(27, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(25, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(23, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(21, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(19, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(17, 2, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(15, 2, -16), 90)
        makeUpDownRamp(app, 'upmore', self.offset + ogre.Vector3(12, 2, -16), -90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(9, 4, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(7, 4, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(5, 4, -16), 90)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(3, 4, -16), 90)
        makeCornerRamp(app, 'corner', self.offset + ogre.Vector3(0, 4, -16), -90)
        makeUpDownRamp(app, 'up', self.offset + ogre.Vector3(0, 4, -20), 180)
        makeUpDownRamp(app, 'up', self.offset + ogre.Vector3(0, 6, -24), 180)
        makeUpDownRamp(app, 'up', self.offset + ogre.Vector3(0, 8, -28), 180)
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(0, 10, -31))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(0, 10, -33))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(0, 10, -35))
        makeStraightRamp(app, 'straight', self.offset + ogre.Vector3(0, 10, -37))
        
        (leftdoor, rightdoor) = makeSwingingDoors(app, 
                          self.offset + ogre.Vector3(0,0,50))
        
        myLock = makeLevelLock(app, self.offset)
        
        leftdoor.lock(app._world, myLock)
        rightdoor.lock(app._world, myLock)
        
        key = makeUnlockKey(app, 
                            self.offset + ogre.Vector3(0,12,-40),
                            lock = myLock)

        
        
        
        
        
    
    def unload(self):
        pass