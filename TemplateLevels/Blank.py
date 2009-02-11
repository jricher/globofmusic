import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

    def unload(self, app):
        pass
