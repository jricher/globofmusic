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
        print 'Loaded Level Lab1'
        # app is just a handle for the game engines
        # middle of platform is at 0, 0, 0 (self.offset)
        # dimensions of arena are around 45
        # doors are at Z +- 45, y is altitude
        for count in range(1, 17):
            if(count % 3 == 0):
                makeTiltingPlatform(app, "thing", self.offset + ogre.Vector3((count * 5) - 40, (count * 1.5) - 1, 0), sound = 'bell-3');                
            else:
                makePlatform(app, "thing", self.offset + ogre.Vector3((count * 5) - 40, count * 1.5, 0), sound = 'bell-3');

        lock = makeLevelLock(app, self.offset)

        (ldoor, rdoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0,0, 50))
        #ldoor.lock(app._world, lock) # without app._world there is no tie to a physics engine
        #rdoor.lock(app._world, lock)

        makeUnlockKey(app, self.offset + ogre.Vector3(35, 30, -10), lock = lock)
        makeUnlockKey(app, self.offset + ogre.Vector3(35, 30, 10), lock = lock)
        makeUnlockKey(app, self.offset + ogre.Vector3(-30, 20, -29), lock = lock)

        self.backgroundMusic = app.music['bg-4']

#        makeExecutiveToy(app, "", self.offset + ogre.Vector3(20, 0, -20))

#        makeBell(app, "", self.offset + ogre.Vector3(20, 3, -20))

#        for count in range (1, 30):
#            crate = makeCrate(app, "thing", self.offset + ogre.Vector3(-(count * 2.1) + 30, count * .2, -30))
#            crate.body.sleep()
#            crate = makeCrate(app, "thing", self.offset + ogre.Vector3(-(count * 2.1) + 30, count * .2, -27.8))
#            crate.body.sleep()
            

#        height = 0;
#        for count in range (1, 30):
#            if(count % 3 == 0):
#                height = height + 1
#            crate = makeCrate(app, "thing", self.offset + ogre.Vector3(-(count * 2.1) + 30, height * 1.5, -30))
#            crate.body.sleep()
#            crate = makeCrate(app, "thing", self.offset + ogre.Vector3(-(count * 2.1) + 30, height * 1.5, -27.8))
#            crate.body.sleep()
#            if(height > 2):
#                crate = makeCrate(app, "thing", self.offset + ogre.Vector3(-(count * 2.1) + 30, (height * 1.5) - 2.6, -29))
#                crate.body.sleep()
        

#        makeMyMetalCrate(app, "", self.offset + ogre.Vector3(5, 1, 0), 2.5, 1)

# sliding ice cubes
        makeIceCube(app, "", self.offset + ogre.Vector3(20, 6, -20))
        makeIceCube(app, "", self.offset + ogre.Vector3(20, 56, -20))
        makeIceCube(app, "", self.offset + ogre.Vector3(20, 106, -20))
        makeIceCube(app, "", self.offset + ogre.Vector3(20, 156, -20))
        makeIceCube(app, "", self.offset + ogre.Vector3(20, 206, -20))
        makeIceCube(app, "", self.offset + ogre.Vector3(20, 256, -20))
        makeUpDownRamp(app, "", self.offset + ogre.Vector3(20, 0, -20), 90)



#        for count in range(0, 6):
#            for count2 in range(0, 4):
#                crate = makeCrate(app, "thing", self.offset + ogre.Vector3((count2 + 5) - 10, 550 + (count * 100), 40))

#        makePlatform(app, 'Platform one', self.offset + ogre.Vector3(0, 1.5, -30))
#        makePlatform(app, 'Platform one', self.offset + ogre.Vector3(0, 3, -25))
#        makePlatform(app, 'Platform one', self.offset + ogre.Vector3(0, 4.5, -20))
#        makePlatform(app, 'Platform one', self.offset + ogre.Vector3(0, 6, -15))
#        makePlatform(app, 'Platform one', self.offset + ogre.Vector3(0, 8, -10))
#        makePlatform(app, 'Platform one', self.offset + ogre.Vector3(0, 10, -0))
#        makeDomino(app,"d1", self.offset + ogre.Vector3(0,10.25,0))

    def unload(self, app):
        pass

def makeMyMetalCrate(app, name, offset, height, mass):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    offset = offset + ogre.Vector3(0, height / 2, 0);
    
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
    c.body = ei.createSingleDynamicBox(mass, app._world, app._space)
    c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id) # without this the user does not physically interact
    
    return c

def makeIceCube(app, name, offset, material='Icy-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Cube.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setScale(2, 2, 2)
    c.node.setPosition(offset + ogre.Vector3(0, 1, 0))
    c.node.attachObject(c.ent)
    c.setMaterial()

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(30, app._world, app._space)
#    c.body.sleep()
    c.geom = c.body.getGeometry(0); # we can use this because it the box is a primative (as opposed to a triangle mesh)
#    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

#    c.ent.setUserObject(c.geom) # only necessary for static triangle meshes
    

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
                             
    c.geom.setUserData(c.id)

    c.friction = 10

    return c

def makeExecutiveToy(app, name, offset, angle=0):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    def makeMyBallBearing(app, name, offset):
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

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.body = ei.createSingleDynamicSphere(15.0, app._world, app._space)

        c.geom = c.body.getGeometry(0)

        c.geom.setUserData(c.id)

        return c
    ball1 = makeMyBallBearing(app, name, offset + ogre.Vector3(0, 1.1, -4.2))
    ball1.body.setDamping(0, 0)
    ball1.friction = 10
    ball1.bouncy = 10
    ball1.joint = OgreOde.HingeJoint(app._world)
    ball1.joint.attach(ball1.body)
    ball1.joint.setAxis(ogre.Vector3().UNIT_X)
    ball1.joint.setAnchor(ogre.Vector3(0, 20, 0) + offset + ogre.Vector3(0, 0, -4.2))
    
    ball2 = makeMyBallBearing(app, name, offset + ogre.Vector3(0, 1.1, -2.1))
    ball2.body.setDamping(0, 0)
    ball2.friction = 10
    ball2.bouncy = 10
#    ball2.body.setMass(mass)
    ball2.joint = OgreOde.HingeJoint(app._world)
    ball2.joint.attach(ball2.body)
    ball2.joint.setAxis(ogre.Vector3().UNIT_X)
    ball2.joint.setAnchor(ogre.Vector3(0, 20, 0) + offset + ogre.Vector3(0, 0, -2.1))

    ball3 = makeMyBallBearing(app, name, offset + ogre.Vector3(0, 1.1, 0))
    ball3.body.setDamping(0, 0)
    ball3.friction = 10
    ball3.bouncy = 10
#    ball3.body.setMass(mass)
    ball3.joint = OgreOde.HingeJoint(app._world)
    ball3.joint.attach(ball3.body)
    ball3.joint.setAxis(ogre.Vector3().UNIT_X)
    ball3.joint.setAnchor(ogre.Vector3(0, 20, 0) + offset + ogre.Vector3(0, 0, 0))

    ball4 = makeMyBallBearing(app, name, offset + ogre.Vector3(0, 1.1, 2.1))
    ball4.body.setDamping(0, 0)
    ball4.friction = 10
    ball4.bouncy = 10
#    ball4.body.setMass(mass)
    ball4.joint = OgreOde.HingeJoint(app._world)
    ball4.joint.attach(ball4.body)
    ball4.joint.setAxis(ogre.Vector3().UNIT_X)
    ball4.joint.setAnchor(ogre.Vector3(0, 20, 0) + offset + ogre.Vector3(0, 0, 2.1))

    ball5 = makeMyBallBearing(app, name, offset + ogre.Vector3(0, 1.1, 4.2))
    ball5.body.setDamping(0, 0)
    ball5.friction = 10
    ball5.bouncy = 10
#    ball5.body.setMass(mass)
    ball5.joint = OgreOde.HingeJoint(app._world)
    ball5.joint.attach(ball5.body)
    ball5.joint.setAxis(ogre.Vector3().UNIT_X)
    ball5.joint.setAnchor(ogre.Vector3(0, 20, 0) + offset + ogre.Vector3(0, 0, 4.2))

    
    
