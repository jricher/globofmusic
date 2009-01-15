import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *

class Level(BaseLevel):
    def __init__(self, levelId):
        BaseLevel.__init__(self, levelId)
##
##
##    def __del__(self):
##        BaseLevel.__del__(self)
##

    def load(self, app):
        print 'Loaded Level Bob'

        self.backgroundMusic = app.music['bg-3']

        crate = makeCrate(app, 'Bob Crate', self.offset + ogre.Vector3(0, 2, 0))
        crate.sound = app.sounds['bell-lo-0']


    def unload(self, app):
        pass
