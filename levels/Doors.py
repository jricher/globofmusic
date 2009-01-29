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
        
        
        key = MultiPartLock()

        c = makeUnlockKey(app, self.offset + ogre.Vector3(0, 2, 10), sound='key-1')
        c.quant = 8
        c.key = key
        key.sources.append(c)
    
        (leftDoor, rightDoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0, 0, 50))
    #    leftDoor.lock(app._world)
        rightDoor.lock(app._world)
        key.doors.append(leftDoor)
        key.doors.append(rightDoor)
        
        def areaClear():
            scn = app.sceneManager
            root = scn.getRootSceneNode()
            overlay = ogre.OverlayManager.getSingleton().getByName('AreaClearOverlay')
            overlay.show()  
            c = Container("StartArrow")
            c.particleSystem = scn.createParticleSystem('arrow', 'Examples/njrGreenyNimbus')
            c.particleSystem.setKeepParticlesInLocalSpace(True)
            
            c.node = root.createChildSceneNode("StartArrow")
            c.node.setPosition(self.offset + ogre.Vector3(0,0,-50))
        
            c.node.attachObject(c.particleSystem)
            particles["StartArrow"] = c
    
        key.unlockCallback = areaClear


    def unload(self, app):
        pass
