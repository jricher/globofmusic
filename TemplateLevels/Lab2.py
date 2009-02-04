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
        print 'Loaded Level Lab2'

        self.backgroundMusic = app.music['bg-3']

        crate = makeMetalCrate(app, 'Lab2 Crate', self.offset + ogre.Vector3(0, 1.3, 0))
        crate.sound = app.sounds['perc-3']
        crate2 = makeMetalCrate(app, 'Lab2 Crate2', self.offset + ogre.Vector3(0, 3.8, 0))
        
        
        platform = makePlatform(app, "Lab2 Platform", self.offset + ogre.Vector3(0,5,-30) )
        platform.sound = app.sounds['tone-7']
        
        


    def unload(self, app):
        pass
