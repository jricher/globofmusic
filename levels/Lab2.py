import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *

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

        crate = makeCrate(app, 'Lab2 Crate', self.offset + ogre.Vector3(0, 2, 0))
        crate.sound = app.sounds['bell-lo-0']
        
        platform = makeTiltingPlatform(app, "Lab2 Platform", self.offset + ogre.Vector3(-5,5,0) )
        platform.sound = app.sounds['neutron-0']


    def unload(self, app):
        pass
