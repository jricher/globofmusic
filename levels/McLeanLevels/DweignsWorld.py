import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

        self.backgroundMusic = app.music['bg-2']
        
        lock = makeLevelLock(app, self.offset)
        c = makeUnlockKey(app,
                          self.offset + ogre.Vector3(0,4,0),
                          sound = 'tone-1')
        c.quant = 8
        c.key = lock
        lock.sources.append(c)
        
        c = makeUnlockKey(app,
                          self.offset + ogre.Vector3(40, 12, 0),
                          sound = 'tone-0')
        c.quant = 8
        c.key = lock
        lock.sources.append(c)

        (leftDoor, rightDoor) = makeSwingingDoors(app,
                         self.offset + ogre.Vector3(0, 0, 50))
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)
        
        makeOnOffRamp(app, "ramp1",
                      self.offset + ogre.Vector3(0, 0, -10),
                      angle = 10, material = 'platform0-', sound = 'key-3')
        makeTiltingPlatform(app, "ramp2",
                      self.offset + ogre.Vector3(10, 0, -10),
                      material = 'platform0-', sound = 'key-1')        
        makePlatform(app,
                     "dweigns_platform1",
                     self.offset + ogre.Vector3(40, 7, 0),
                     material = 'platform0-',
                     sound = 'perc-2')
        makePlatform(app,
                     "dweigns_platform3",
                     self.offset + ogre.Vector3(40, 3, 8),
                     material = 'platform0-',
                     sound = 'perc-3')

        c = makeMetalCrate(app,
                      "dweigns_crate3",
                      self.offset + ogre.Vector3(25, 5, 0))
        mass = OgreOde.BoxMass(0.1, c.geom.getSize())
        c.body.setMass(mass)
        c.friction = 1
        
        makeMetalCrate(app,
                      "dweigns_crate4",
                      self.offset + ogre.Vector3(15, 5, 0))

        makeBowlingPin(app,
                       "bp1",
                       self.offset + ogre.Vector3(4,0,-40))
        makeBowlingPin(app,
                       "bp2",
                       self.offset + ogre.Vector3(-4,0,-40))
        makeBowlingPin(app,
                       "bp1",
                       self.offset + ogre.Vector3(0,0,-35))        
        makeRupee(app,
                  "bridge1",
                  self.offset + ogre.Vector3(-40,3,5))
        makeBallBearing(app,
                        "ball1",
                        self.offset + ogre.Vector3(0, 20, -10))
        makeDonut(app, "donut1",
                  self.offset + ogre.Vector3(-20,2,0))
    def unload(self, app):
        pass
