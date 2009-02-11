import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Level Lab1'

        makeCrate(app, 'Lab1 Crate', self.offset + ogre.Vector3(0, 2, 0))
        makePlatform(app, "A Platform", self.offset + ogre.Vector3(0,1,10))
        makeBell(app, "A Bell", self.offset + ogre.Vector3(0,1,30))


    def unload(self, app):
        pass
