import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Catalog import *

class Level(BaseLevel):
    def __init__(self, levelId):
        BaseLevel.__init__(self, levelId)
        self.wide = True
        
        
    def load(self, app):
        print 'Loaded Object Catalog'

        self.backgroundMusic = app.music['bg-3']
        # Arranges the available objects, but doesn't do scaling
        
        #Row 1
        makeCrate(app, 'A Crate', self.offset + ogre.Vector3(140, 5, 20))
        makePlatform(app, 'A Platform', self.offset + ogre.Vector3(130, 5,20))
        makeTiltingPlatform(app, "A Tilting Platform", self.offset + ogre.Vector3(120, 5,20))
        makeIcePlatform(app, 'An Ice Platform', self.offset + ogre.Vector3(100, 5, 20))
        
        #Row 2
        makeOnOffRamp(app, 'An On Off Ramp', self.offset + ogre.Vector3(140, 5, 0))
        makeStraightRamp(app, 'A Straight Ramp', self.offset + ogre.Vector3(130, 5, 0))
        makeUpDownRamp(app, 'An Up Down Ramp', self.offset + ogre.Vector3(120, 5, 0))
        makeCornerRamp(app, 'A Corner Ramp', self.offset + ogre.Vector3(110, 5, 0))
        
        #Row 3
        makeDomino(app, "A Domino", self.offset + ogre.Vector3(140,5,-20), 0)
        makeDomino(app, "A Domino Turned", self.offset + ogre.Vector3(130,5,-20), 90)
        makeUnlockKey(app, self.offset + ogre.Vector3(120,5,-20))
        makeSwingingDoors(app, self.offset + ogre.Vector3(100,5,-45))
        

    def unload(self, app):
        pass