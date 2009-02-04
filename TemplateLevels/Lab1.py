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
        print 'Loaded Level Lab1'

        self.backgroundMusic = app.music['bg-3']

        crate = makeCrate(app, 'Lab1 Crate', self.offset + ogre.Vector3(0, 2, 0))
        crate.sound = app.sounds['bell-0']


    def unload(self, app):
        pass
