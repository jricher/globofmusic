import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS
import math

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
        print 'Loaded Level JamMeD'
        makeBouncyPlatform(app, "Jammed platform 1", self.offset + ogre.Vector3(40, 1, 0))
        makePlatform(app, "Jammed platform 2", self.offset + ogre.Vector3(34, 3, 0))
        makePlatform(app, "Jammed platform 3", self.offset + ogre.Vector3(28, 4, 0))
        makePlatform(app, "Jammed platform 4", self.offset + ogre.Vector3(22, 5, 0))
        makeBouncyPlatform(app, "Jammed platform 5", self.offset + ogre.Vector3(16, 6, 0))

        #crate = makeCrate(app, "Jammed crate", self.offset + ogre.Vector3(0, 6, 0))
        #plank = makePlank(app, "plank", self.offset + ogre.Vector3(0, 6, 0), angle=30)

        #metalCrate = makeHeavyMetalCrate(app, "Jammed crate", self.offset + ogre.Vector3(0, 0, 0))
        (leftD, rightD) = makeSwingingDoors(app, self.offset + ogre.Vector3(0,0,50))
        lock = makeLevelLock(app, self.offset + ogre.Vector3(0,0,50))
        leftD.lock(app._world, lock)
        rightD.lock(app._world, lock)

        # circle of heavy crates
        Pi = 3.14159265359
        increment = .25
        spread = 20.2
        i = 0.0
        j = 0
        while i < (2*Pi - 0.2):
            x = -15 + spread*math.cos(i)
            z = -15 + spread*-math.sin(i)
            print "i: %s - %s %s" % (i, x, z)

            if (j % 4 == 1):
                c = makeUnlockKey(app, self.offset + ogre.Vector3(x, 12.9, z), sound='key-' + str(j%4), lock=lock)
                c.quant = 8

            if (i == 3.75):
                lcrate = makeLightMetalCrate(app, "crate", self.offset + ogre.Vector3(x, 0, z))
                lcrate.sound = app.sounds['bell-2']
                i = i + increment
                j = j + 1
                continue
            if (i == 1.25):
                crate = makeHeavyMetalCrate(app, "crate", self.offset + ogre.Vector3(x, 0, z), "clouds")
            else:
                crate = makeHeavyMetalCrate(app, "crate", self.offset + ogre.Vector3(x, 0, z))


            crate.sound = app.sounds['bell-1']
            crate.bouncy = 0.7
            crate.joint = OgreOde.FixedJoint(app._world)
            crate.joint.attach(crate.body)
            i = i + increment
            j = j + 1

        
        #makeBell(app, "bell 1", self.offset + ogre.Vector3(-15, 3, -15))
        
        fakeKey = makeUnlockKey(app, self.offset + ogre.Vector3(-15, 2, -15))
        fakeKey.quant = 8

        c = makeUnlockKey(app, self.offset + ogre.Vector3(16, 10, 20), sound='key-1', lock=lock)
        c.quant = 8

        br = makeBridge(app, "BridgeToKey", self.offset + ogre.Vector3(16,8, 12))
        
        #pl = makePlank(app, 'firstPlank', self.offset + ogre.Vector3(0, 5, 0), sound='bell-4')

        pl = makePlank(app, 'firstPlank', self.offset + ogre.Vector3(16, 8, 6), sound='bell-4')
        pl.joint = OgreOde.FixedJoint(app._world)
        pl.joint.attach(pl.body)

        makeIcePlatform(app, "ice", self.offset + ogre.Vector3(42, 3, 20))


def unload(self, app):
        pass

def makeIcePlatform(app, name, offset, material='platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'IceChunk.mesh')
    c.node = root.createChildSceneNode(name)
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

    c.friction = 100

    return c

def makeHeavyMetalCrate(app, name, offset, color='Chrome'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    offset = offset + ogre.Vector3(0, 5, 0)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Cube.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)

    sub = c.ent.getSubEntity(0)
    sub.materialName = 'Examples/' + color # look like a monolith

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)

    c.node.setPosition(offset)

    c.node.setScale(4, 10, 4)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(1000.0, app._world, app._space)
    #c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    c.friction = 100   
    
    return c

def makeLightMetalCrate(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    offset = offset + ogre.Vector3(0, 5, 0)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Cube.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)

    sub = c.ent.getSubEntity(0)
    sub.materialName = 'Examples/clouds' # look like a monolith

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)

    c.node.setPosition(offset)

    c.node.setScale(4, 10, 4)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(10.0, app._world, app._space)
    #c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    c.friction = 100   
    
    return c

class BouncePlatform(Platform):
    def __init__(self, name = None, materialName = None, restartable = False, key = None):
        #self.friction = 100
        self.bouncy = 0.7
        Platform.__init__(self, name, materialName, restartable, key)
    def __del__(self):
        if not Platform:
            return
        Platform.__del__(self)

    def collide(self, other, contact, normal, lm):
        contact.setCoulombFriction(self.friction)    # walls are pretty slick
        contact.setBouncyness(self.bouncy)
        if isinstance(other, Player):
            other.body.addForce(ogre.Vector3().UNIT_Y*400)
        Platform.collide(self, other, contact, normal, lm)
        return True

    def collideWith(self, other, contact, normal, lm):
        contact.setCoulombFriction(self.friction)    # walls are pretty slick
        contact.setBouncyness(self.bouncy)
        if isinstance(other, Player):
            other.body.addForce(ogre.Vector3().UNIT_Y*400)

        Platform.collideWith(self, other, contact, normal, lm)
        return True
    
def makeBouncyPlatform(app, name, offset, material='platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = BouncePlatform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'platform.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    # set the initial material
    c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
                             

    c.geom.setUserData(c.id)

    return c
