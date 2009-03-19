import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        scn = app.sceneManager
        root = scn.getRootSceneNode()
        print 'Loaded DryMetaHumor Level'

        self.backgroundMusic = app.music['bg-4']

        makePlatform(
            app,
            'Fred1',
            self.offset + ogre.Vector3(20, 3, 0),
            sound='perc-0')

        makeCrate(
            app,
            'Joe1',
            self.offset + ogre.Vector3(20, 3, 0))
        

        makePlatform(
            app,
            'Fred2',
            self.offset + ogre.Vector3(24, 6, 4),
            sound='perc-1')

        makeBall(
            app,
            'Joe2',
            self.offset + ogre.Vector3(24, 6, 4) )

        makePlatform(
            app,
            'Fred3',
            self.offset + ogre.Vector3(20, 9, 8),
            sound='perc-2')

        makeDonut(
            app,
            'Joe3',
            self.offset + ogre.Vector3(20, 9.5, 8) )

        makePlatform(
            app,
            'Fred4',
            self.offset + ogre.Vector3(16, 12, 4),
            sound='perc-3')

        makeBarbell(
            app,
            'Joe4',
            self.offset + ogre.Vector3(16, 12, 4))

        makePlatform(
            app,
            'Fred5',
            self.offset + ogre.Vector3(20, 15, 0),
            sound='perc-4')

        c = makeMetalCrate(
            app,
            'Joe6',
            self.offset + ogre.Vector3(20, 15, 0))
        mass = OgreOde.BoxMass(1, c.geom.getSize())
        c.body.setMass(mass)
        
        makePlatform(
            app,
            'Fred6',
            self.offset + ogre.Vector3(24, 18, -4),
            sound='perc-5')

        makeBowlingPin(
            app,
            'Joe5',
            self.offset + ogre.Vector3(24, 18, -4))

        makePlatform(
            app,
            'Fred7',
            self.offset + ogre.Vector3(20, 21, -8),
            sound='bell-2')

        makeDomino(
            app,
            'Joe7',
            self.offset + ogre.Vector3(20, 21.25, -8),
            angle=45)

        makePlatform(
            app,
            'Fred8',
            self.offset + ogre.Vector3(16, 24, -4),
            sound='bell-3')

##        makeCrate(
##            app,
##            'Joe8',
##            self.offset + ogre.Vector3(16, 24, -4))

        (leftDoor, rightDoor) = makeSwingingDoors(
            app, self.offset + ogre.Vector3(0,0,50))

        lock1 = makeItemLock(app, self.offset)
        key1 = makeUnlockKey(app, self.offset + ogre.Vector3(16, 25.5, -4))
        key1.quant = 8
        key1.key = lock1
        lock1.sources.append(key1)

        # Particle system for first key
        
        c = Container("FirstKey")
        c.particleSystem = scn.createParticleSystem('firstKey', 'Examples/PurpleFountain')
        c.particleSystem.setKeepParticlesInLocalSpace(True)
        c.node = root.createChildSceneNode("FirstKey")
        c.node.setPosition(self.offset + ogre.Vector3(16, 0, -4))
        c.node.attachObject(c.particleSystem)
        particles["FirstKey"] = c

        for n in range(8):
            makeIcePlatform(
                app,
                'icy' + `n`,
                self.offset + ogre.Vector3(-20, 7, -20 + 4*n))

        makeUpDownRamp(
            app,
            'Ramp',
            self.offset + ogre.Vector3(-20,0,-28))

        domino = makeLockingDomino(
            app,
            'Domino',
            self.offset + ogre.Vector3(-20,2.5,-26))

        # write the unlockCallback function to turn off the purple fountain
        def unlockCallback():
            if ("FirstKey" in particles):
                scn = app.sceneManager
                root = scn.getRootSceneNode()
                c = particles["FirstKey"]
                scn.destroyParticleSystem(c.particleSystem)
                del c.particleSystem
                scn.destroySceneNode(c.node.getName())
                del particles["FirstKey"]
        # end of unlockCallback function
        domino.unlockCallback = unlockCallback

        makeIcePlatform(
            app,
            'Wall',
            self.offset + ogre.Vector3(-20, 8, -28))

##        makeBallBearing(
##            app,
##            'Hack',
##            self.offset + ogre.Vector3(-20, 8, -26))

        domino.lock(app._world, lock1)

        lock2 = makeLevelLock(app, self.offset)
        key2 = makeUnlockKey(app, self.offset + ogre.Vector3(-20, 9, 12))
        key2.quant = 8
        key2.key = lock2
        lock2.sources.append(key2)
        
        leftDoor.lock(app._world, lock2)
        rightDoor.lock(app._world, lock2)

    def unload(self, app):
        pass

def makeIcePlatform(app, name, offset, material='IcePlatform-', sound=None):
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
    
class LockingDomino(Domino):
    def __init__(self, name, angle=0.0, materialName = None):
        Domino.__init__(self, name, angle, materialName)
        self.locks = []
        self.locked = False
        
    def lock(self, _world, key):
        # create fixed joint to form a lock
        l = OgreOde.FixedJoint(_world)
        l.attach(self.body)
        self.locks.append(l)
        if key:
            key.doors.append(self)
        self.locked = True
        
    def unlock(self):
        '''
        once unlocked, cant be re-locked
        '''
        del self.locks[:]
        self.locked = False
        if(hasattr(self, 'unlockCallback')):
            self.unlockCallback()

    def collide(self, other, contact, normal, lm):
        if self.locked and isinstance(other, Player):
            lm.overlay = ogre.OverlayManager.getSingleton().getByName('DoorLockedOverlay')
            lm.overlay.show()
            lm.overlayTimeout = 1
            return Fireable.collide(self, other, contact, normal, lm)
        else:
            Domino.collide(self, other, contact, normal, lm)

    def collideWith(self, other, contact, normal, lm):
        if self.locked and isinstance(other, Player):
            lm.overlay = ogre.OverlayManager.getSingleton().getByName('DoorLockedOverlay')
            lm.overlay.show()
            lm.overlayTimeout = 1
            return Fireable.collideWith(self, other, contact, normal, lm)
        else:
            Domino.collideWith(self, other, contact, normal, lm)
        
def makeLockingDomino(app, name, offset, angle=0, material = 'Domino-', sound=None):
    scn = app.sceneManager
    rootNode = scn.getRootSceneNode()
    name = name + str(offset)

    # make dominoes float properly
    offset = offset + ogre.Vector3(0, 2.1, 0)

    c = LockingDomino(name, angle, materialName = material)
    #self.dominoes.append(c.id)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Domino.mesh")
    c.ent.setCastShadows(True)
    c.node = rootNode.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)
    c.startPosition = offset
    c.node.setPosition(offset)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    #ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale())) #< -- this one works for some reason
    #ei = OgreOde.EntityInformer (c.ent, c.node._getFullTransform())
    ei = OgreOde.EntityInformer (c.ent)
    
    c.body = ei.createSingleDynamicBox(5.0,app._world, app._space)
    c.body.setDamping(2,2)
    c.geom = c.body.getGeometry(0)
    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(quat.xAxis())

    c.joint.setAnchor(offset + ogre.Vector3(0, -2, 0)) # The joint needs to be below the domino, instead of in the middle

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['perc-%d' % random.randrange(6)]

    c.geom.setUserData(c.id)

    c.setMaterial()

    return c

def makeItemLock(app, offset):
    lock = MultiPartLock()

    lock.unlockCallback = nullCallback()
        
    return lock

def nullCallback():
    pass
