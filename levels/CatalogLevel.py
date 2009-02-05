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

        self.backgroundMusic = app.music['bg-6']
        # Arranges the available objects, but doesn't do scaling
        
        #Row 1
        makeCrate(app, 'A Crate', self.offset + ogre.Vector3(140, 1, 20))
        makeBall(app, 'A Ball', self.offset + ogre.Vector3(130, 1, 20))
        makeBarbell(app, 'A Barbell', self.offset + ogre.Vector3(120, 1, 20))
        makeBell(app, 'A Bell', self.offset + ogre.Vector3(110, 1, 20))
        makeRupee(app, "A Rupee", self.offset + ogre.Vector3(100,3,20))
        
        makePlatform(app, 'A Platform', self.offset + ogre.Vector3(80, 1,20))
        makeTiltingPlatform(app, "A Tilting Platform", self.offset + ogre.Vector3(70, 1,20))
        makeIcePlatform(app, 'An Ice Platform', self.offset + ogre.Vector3(60, 1, 20))
        makeTiltRamp(app, "A Tilting Ramp", self.offset + ogre.Vector3(50,0,20))
        makeInnerWall(app, "An InnerWall", self.offset + ogre.Vector3(40,0,20))
        makeInnerWall(app, "An InnerWall", self.offset + ogre.Vector3(30,0,20), 45)
        
        #Row 2
        makeOnOffRamp(app, 'An On Off Ramp', self.offset + ogre.Vector3(140, 1, 0))
        makeStraightRamp(app, 'A Straight Ramp', self.offset + ogre.Vector3(120, 1, 0))
        makeUpDownRamp(app, 'An Up Down Ramp', self.offset + ogre.Vector3(100, 1, 0))
        makeCornerRamp(app, 'A Corner Ramp', self.offset + ogre.Vector3(80, 1, 0))
        makeOnOffRamp(app, 'An On Off Ramp turned', self.offset + ogre.Vector3(60, 1, 0), 45)
        makeBridge(app, 'A bridge', self.offset + ogre.Vector3(50, 2.5, 0))
        makeBowlingPin(app, "A Bowling Pin", self.offset + ogre.Vector3(40, 0, 0))
        makeCone(app, "A Cone", self.offset + ogre.Vector3(30,0,0))
        makeGear(app, "A Gear", self.offset + ogre.Vector3(0,0,0))
        
        
        #Row 3
        makeDomino(app, "A Domino", self.offset + ogre.Vector3(140,1,-20))
        makeDomino(app, "A Domino Turned", self.offset + ogre.Vector3(120,1,-20), 90)
        makeUnlockKey(app, self.offset + ogre.Vector3(100,2,-20))
        makeSwingingDoors(app, self.offset + ogre.Vector3(80,1,-20))
        makeDonut(app, "A Donut", self.offset + ogre.Vector3(60,2,-20))
        makePlank(app, "A Plank", self.offset + ogre.Vector3(50,1,-20))
        makeBallBearing(app, "A Ball Bearing", self.offset + ogre.Vector3(40,2,-20))
        makeBell(app, 'A Bell', self.offset + ogre.Vector3(30, 1, -20))
        
               
        
        
        

                

    def unload(self, app):
        pass
