import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import * #Glob libraries
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

        makePlatform(app, "OctoPlatform", self.offset + ogre.Vector3(40,2,-10))
        makePlatform(app, "OctoPlatform2", self.offset + ogre.Vector3(30,2,-10))
        makePlatform(app, "OctoPlatform3", self.offset + ogre.Vector3(20,2,-10))

        makeIcePlatform(app, "IcyPlatform1", self.offset + ogre.Vector3(10, 2, -10))
        makeIcePlatform(app, "IcyPlatform1", self.offset + ogre.Vector3(0, 2, -10))
#        makeIcePlatform(app, "IcyPlatform1", self.offset + ogre.Vector3(10, 2, 0))
#        makeIcePlatform(app, "IcyPlatform1", self.offset + ogre.Vector3(10, 2, -10))
#        makeIcePlatform(app, "IcyPlatform1", self.offset + ogre.Vector3(0, 2, 0))
        
        makeMetalCrate(app, 'Crate1', self.offset + ogre.Vector3(10,4,-30))
        makeMetalCrate(app, 'Crate2', self.offset + ogre.Vector3(10,3,-30))
        makeMetalCrate(app, 'Crate3', self.offset + ogre.Vector3(10,2,-30))
        makeMetalCrate(app, 'Crate4', self.offset + ogre.Vector3(10,1,-30))
        makeMetalCrate(app, 'Crate5', self.offset + ogre.Vector3(15,4,-30))
        makeMetalCrate(app, 'Crate6', self.offset + ogre.Vector3(15,3,-30))
        makeMetalCrate(app, 'Crate7', self.offset + ogre.Vector3(15,2,-20))

        makeGear(app, 'gear1', self.offset + ogre.Vector3(-15, 0, -25))

        makeDonut(app, 'donut1', self.offset + ogre.Vector3(-15, 4, -25))

        crate8 = makeMetalCrate(app, 'Crate8', self.offset + ogre.Vector3(22,2,-20))
#        mass = OgreOde.BoxMass(30.0, crate8.geom.getSize())
#        crate8.body.setMass(mass)
#        crate8.friction = 10

        makeBridge(app, 'bridge', self.offset + ogre.Vector3(10,2.2,10))

        for j in range( 1, 21, 2):
            for i in range(0, 20, 2):
                c = makeCone(app, 'cone%d-%d'%(i,j), self.offset + ogre.Vector3( 20 + i, 0, j))
                c.body.sleep()
                c = makeCone(app, 'cone%d-%d'%(-i,-j), self.offset + ogre.Vector3( -20 - i, 0, j))
                c.body.sleep()
                
        
        makeUpDownRamp(app, 'UpDown1', self.offset + ogre.Vector3(5,0, 5), angle=30, material = 'IcePlatform-', sound=None)
        doors = makeSwingingDoors(app, self.offset + ogre.Vector3(0,0,50))
        leftDoor = doors[0]
        rightDoor = doors[1]

        lock = makeLevelLock(app, self.offset)
        lock2 = makeLevelLock(app, self.offset + ogre.Vector3(0,0,1))

        c = makeUnlockKey(app, self.offset + ogre.Vector3(10,4,10), sound = 'key-0')
        c.quant = 8
        c.key = lock
        lock.sources.append(c)
        
        c2 = makeUnlockKey(app, self.offset + ogre.Vector3(0,2,4), sound = 'perc-1')
        c2.quant = 8
        c2.key = lock
        lock.sources.append(c2)
        
        c3 = makeUnlockKey(app, self.offset + ogre.Vector3(0,2,41.25), sound = 'perc-2')
        c3.quant = 8
        c3.key = lock
        lock.sources.append(c3)
        
        c4 = makeUnlockKey(app, self.offset + ogre.Vector3(-15, 2, -25), sound = 'perc-3')
        c4.quant = 8
        c4.key = lock2
        lock2.sources.append(c4)
        
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock2)

        makeRupee(app, 'rupee1', self.offset + ogre.Vector3(23,0,-20))


        self.backgroundMusic = app.music['bg-5']

        makeUpDownRamp(app, 'UpDown2', self.offset + ogre.Vector3(0,0, 30), angle=30, material = 'IcePlatform-', sound=None)

        makeDomino(app, 'D1', self.offset + ogre.Vector3(0,0,45), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D2', self.offset + ogre.Vector3(2.5,0,40), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D3', self.offset + ogre.Vector3(-2.5,0,40), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D4', self.offset + ogre.Vector3(5,0,45), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D5', self.offset + ogre.Vector3(-5,0,45), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D6', self.offset + ogre.Vector3(3.75,0,42.5), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D7', self.offset + ogre.Vector3(-3.75,0,42.5), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D8', self.offset + ogre.Vector3(1.25,0,47.5), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D9', self.offset + ogre.Vector3(-1.25,0,47.5), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D8', self.offset + ogre.Vector3(1.125,0,46.25), angle=0, material = 'Domino-', sound=None)
        makeDomino(app, 'D9', self.offset + ogre.Vector3(-1.125,0,46.25), angle=0, material = 'Domino-', sound=None)
        
    def unload(self, app):
        pass


def makeIcePlatform(app, name, offset, material='IcePlatform-', sound=None):
    scn = app.sceneManager #Manages scene graph - holds reference to objects where they are and what things exist
                            # all visuals tied to scene manager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'iceChunk.mesh') #refers to artists' file
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)  # this parameter is actually the absolute coordinate
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)

    c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    c.friction = 20
    c.geom.setUserData(c.id)    #Hang onto the id.  Use this for friction, etc.


        
    return c
    
