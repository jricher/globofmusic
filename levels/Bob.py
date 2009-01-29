import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):
    def __init__(self, levelId):
        BaseLevel.__init__(self, levelId)
        #self.wide = True
##
##
##    def __del__(self):
##        BaseLevel.__del__(self)
##

    def load(self, app):
        print 'Loaded Level Bob'

        self.backgroundMusic = app.music['bg-5']

        crate = makeCrate(app, 'Bob Crate', self.offset + ogre.Vector3(0, 2, 0))
        crate.sound = app.sounds['bell-5']

        #platform = makeIcePlatform(app, 'Bob Platform', self.offset + ogre.Vector3(10, 1, 0))
        #platform.sound = app.sounds['key-1']

        makeOnOffRamp(app, 'onoff', self.offset + ogre.Vector3(10, 0, -20))
        makeStraightRamp(app, 's1', self.offset + ogre.Vector3(10, 0, -17))
        makeStraightRamp(app, 's2', self.offset + ogre.Vector3(10, 0, -15))
        makeUpDownRamp(app, 'updown0', self.offset + ogre.Vector3(10, 0, -12))
        makeUpDownRamp(app, 'updown1', self.offset + ogre.Vector3(10, 2, -8))
        makeUpDownRamp(app, 'updown2', self.offset + ogre.Vector3(10, 4, -4))
        makeUpDownRamp(app, 'updown3', self.offset + ogre.Vector3(10, 6, 0))
        makeCornerRamp(app, 'corner', self.offset + ogre.Vector3(10, 8, 4))
        

    def unload(self, app):
        pass



    
