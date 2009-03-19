import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'


        self.backgroundMusic = app.music['bg-3']

    
        makePlatform(
            app,
            'A Platform',
            self.offset + ogre.Vector3(12, 1, 0))

        (leftDoor, rightDoor) = makeSwingingDoors(app,
                                self.offset + ogre.Vector3(0, 0, 50))

        lock = makeLevelLock(app, self.offset)

        c = makeUnlockKey(app, self.offset + ogre.Vector3(-18, 15, 15))
        c.key = lock
        c.sound = app.sounds['key-2']
        lock.sources.append(c)

        c = makeUnlockKey(app, self.offset + ogre.Vector3(4, 1, 40))
        c.key = lock
        c.sound = app.sounds['key-3']
        lock.sources.append(c)

        # leftDoor.lock(app._world, lock)
        # rightDoor.lock(app._world, lock)

        makeGear(app, 'A Gear', self.offset + ogre.Vector3(20,0,20))

        makeMGear(app, 'a Gear', self.offset + ogre.Vector3(-18,1,-15), -0.2, 1.4)
        makeMGear(app, 'b Gear', self.offset + ogre.Vector3(-18,6,-15), +0.4, 1.1)
        makeMGear(app, 'c Gear', self.offset + ogre.Vector3(-18,11,-15), -0.6, 0.8)

        c = makeMetalCrate(app,
                           'My Metal Crate',
                            self.offset + ogre.Vector3(-20, 5, 20))

        mass = OgreOde.BoxMass(1.0, c.geom.getSize())
        c.body.setMass(mass)
        c.friction = 1

        makeDonut(
            app,
            'C Donut',
            self.offset + ogre.Vector3(12, 6, 14))

        makeDonut(
            app,
            'd Donut',
            self.offset + ogre.Vector3(20,3,20))

        makeBowlingPin(
            app,
            'Bowling Pin front center',
            self.offset + ogre.Vector3(0,0,25))

        makeBowlingPin(
            app,
            'Bowling Pin second row left',
            self.offset + ogre.Vector3(-2,0,2))

        makeBowlingPin(
            app,
            'Bowling Pin second row right',
            self.offset + ogre.Vector3(02,0,-2))

        makeBridge(
            app,
            'A bridge',
            self.offset + ogre.Vector3(8, 2, -8))
        
    def unload(self, app):
        pass


        
def makeIcePlatform(app, name, offset, material='platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
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

def makeMGear(app, name, offset, velocity=1.0, size=1.0):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    offset = offset + ogre.Vector3(0,1.5,0) 

    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Gear.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setScale(size, size, size)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (0.5, ei.getSize())
    #mass.setDensity(0.025, ei.getSize())
    mass.setDensity(0.1, ei.getSize())
    c.body.setMass(mass)
    c.body.setDamping(1,1)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)
    
    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_Y)
    c.joint.setAnchor(offset)
    
    #c.body.setAngularDamping(1000)  # Make it  slow down
    c.body.setAngularVelocity(ogre.Vector3().NEGATIVE_UNIT_Y*velocity);
    
    c.geom.setUserData(c.id)

    return c
