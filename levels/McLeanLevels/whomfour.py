import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        xx = 0
        xy = 5
        xz = 0

        print 'Loaded Blank Level'

        self.backgroundMusic = app.music['bg-1']

        c = makeMetalCrate(app, 
                           "A Metal Crate",
                           self.offset + ogre.Vector3(5, 1, -27))

        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(25, app._world, app._space)
        c.friction = 125

#        makeCrate(app, 
#                "A Crate",
#                self.offset + ogre.Vector3(10, 0, -20))
        
        makeBell(app, 
                "A Bell",
                self.offset + ogre.Vector3(xx, xy, xz))
        
        # Make Guard Planks
        makeInnerWall(app, 
                "A Wall",
                self.offset + ogre.Vector3(42.5,0.2,20),
                180)
        
        makeInnerWall(app, 
                "A Wall",
                self.offset + ogre.Vector3(39,0.2,27),
                90)

#        makeSmBallBearing(app,
#                "a bearing",
#                self.offset + ogre.Vector3(30, 0.2, 30))

        # Walled Key
        lock = makeLevelLock(app, self.offset)
        c = makeUnlockKey(app, self.offset + ogre.Vector3(43,1.5,23), sound = 'key-0')
        c.key = lock
        lock.sources.append(c)

        # BK
        c = makeUnlockKey(app, self.offset + ogre.Vector3(xx,xy+1,xz), sound = 'key-1')
        c.key = lock
        lock.sources.append(c)

#        c = makeUnlockKey(app, self.offset + ogre.Vector3(20 ,5,20),  sound = 'key-3')
#        c.key = lock
#        lock.sources.append(c)

        (leftDoor, rightDoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0,0,50))
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)

def unload(self, app):
        pass


def makeIcePlatform(app, name, offset, material="IcePlatform-", sound=None):
        scn = app.sceneManager
        root = scn.getRootSceneNode()
        name = name + str(offset)

        c = Platform(name = name, materialName = material)
        containers[c.id] = c
        c.ent = scn.createEntity(name, 'IceChunk.mesh')
        c.node = root.createChildSceneNode(offset)
        c.node.setPosition(offset)
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

        c.geom.setUserData(c.id)

        return c

def makeSmBallBearing(app, name, offset):
    scn = app.sceneManager
    rootNode = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "BallBearing.mesh")
    c.ent.setCastShadows(True)
    c.node = rootNode.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)
    c.node.setPosition(offset)
    c.node.setScale(0.5,0.5,0.5)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.body = ei.createSingleDynamicSphere(10.0, app._world, app._space)

    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)

    return c




