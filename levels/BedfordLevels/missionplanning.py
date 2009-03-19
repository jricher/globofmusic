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
##   def __del__(self):
##        BaseLevel.__del__(self)
##

    def load(self, app):
        print 'Loaded Level Lab1'
        #makePlatform(app, 'gazook', self.offset + ogre.Vector3(35, 3, 12))
        #makeCrate(app, 'box', self.offset + ogre.Vector3(12, 0, -14))
        (leftdoor, rightdoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0, 0, 50))
        lock = makeLevelLock(app, self.offset)
        leftdoor.lock(app._world, lock)
        rightdoor.lock(app._world, lock)
        key1 = makeUnlockKey(app,
                            self.offset + ogre.Vector3(-15, 10, -15),
                            lock = lock)
        key2 = makeUnlockKey(app,
                            self.offset + ogre.Vector3(30, 8, 4),
                            lock = lock)
        self.backgroundMusic = app.music['bg-6']
        #makeLeadCrate(app, 'metalbox', self.offset + ogre.Vector3(10, 2, 30))
        #makeGear(app, 'pin', self.offset + ogre.Vector3(5, 5, 5))
        #makeIcyPlatform(app, 'icyhot', self.offset + ogre.Vector3(2, 2, -10))
        #makeBall(app, 'bally', self.offset + ogre.Vector3(15, 2, -20))
        #makeBridge(app, 'bridge1', self.offset + ogre.Vector3(25, 2, -20))

        makeOnOffRamp(app, 'ramp0', self.offset + ogre.Vector3(0, 0, -35))
        makeStraightRamp(app, 'ramp1', self.offset + ogre.Vector3(0, 0, -32))
        makeStraightRamp(app, 'ramp2', self.offset + ogre.Vector3(0, 0, -30))
        makeTiltRamp(app, 'ramp3', self.offset + ogre.Vector3(0, 0, -26))
        makeStraightRamp(app, 'ramp4', self.offset + ogre.Vector3(0, 6, -22))
        makeStraightRamp(app, 'ramp5', self.offset + ogre.Vector3(0, 6, -20))
        makeStraightRamp(app, 'ramp6', self.offset + ogre.Vector3(0, 6, -18))
        makeCornerRamp(app, 'ramp7', self.offset + ogre.Vector3(0, 6, -15))
        makeStraightRamp(app, 'ramp8', self.offset + ogre.Vector3(-3, 6, -15), 90)
        makeStraightRamp(app, 'ramp8', self.offset + ogre.Vector3(-5, 6, -15), 90)

        makeDomino(app, 'dom1', self.offset + ogre.Vector3(30, 1, 12))
        makeDomino(app, 'dom2', self.offset + ogre.Vector3(30, 2, 10))
        makeDomino(app, 'dom3', self.offset + ogre.Vector3(30, 3, 8))
        makeDomino(app, 'dom3', self.offset + ogre.Vector3(30, 4, 6))
        
    def unload(self, app):
        pass

def makeIcyPlatform(app, name, offset, material= 'Icy-', sound=None):
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
    
    # set the initial material
    c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
        c.geom.setUserData(c.id)
    c.friction = 10
    return c

def makeLeadCrate(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Fireable(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Cube.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)
    #c.ent.setScale(4, 4, 4)

    sub = c.ent.getSubEntity(0)
    #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door
    sub.materialName = 'Examples/Chrome' # look like a door

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)

    c.node.setPosition(offset)

    c.node.setScale(2, 2.5, 2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(0.15, app._world, app._space)
    c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    c.friction = 2
    
    return c
