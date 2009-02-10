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
        
        
        lock = makeLevelLock(app, self.offset)

        c = makeUnlockKey(app, self.offset + ogre.Vector3(0, 2, 10), sound='key-1')
        c.quant = 8
        c.key = lock
        lock.sources.append(c)
    
        (leftDoor, rightDoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0, 0, 50))
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)
        #key.doors.append(leftDoor)
        #key.doors.append(rightDoor)
        
        def snow(level):
            if ("Snow" not in particles):
                scn = app.sceneManager
                root = scn.getRootSceneNode()
                c = Container("Snow")
                c.particleSystem = scn.createParticleSystem('snow', 'Snow')
                c.particleSystem.setKeepParticlesInLocalSpace(True)
                
                c.node = root.createChildSceneNode("Snow")
                #c.node = self.player.node.createChildSceneNode("Snow")  #for extra kicks, attach to the player
                #c.node.setPosition(0, 0, 375)
                print "Snow: ", level.cameraAnchor.x, level.cameraAnchor.y, level.cameraAnchor.z
                c.node.setPosition(level.cameraAnchor + ogre.Vector3(0,0,25))
                
                c.node.attachObject(c.particleSystem)
                
                particles["Snow"] = c
        self.startLevelCallback = snow 
        
        def stopSnow(level):
            if ("Snow" in particles):
                scn = app.sceneManager
                root = scn.getRootSceneNode()
                c = particles["Snow"]
                scn.destroyParticleSystem(c.particleSystem)
                del c.particleSystem
                scn.destroySceneNode(c.node.getName())
                del particles["Snow"]
        self.stopLevelCallback = stopSnow


    def unload(self, app):
        pass
