import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded MBLevel Level'

        self.backgroundMusic = app.music['bg-6']

        #if ("pendulum starter" not in containers):
        c = makePendulumStarterBall(app,
            "pendulum starter",
            self.offset + ogre.Vector3(0, 13, -40))   

        # Newton's Cradle
        for z in range(1, 5):
                c = makePendulumBall(app,
                "pendulum ball",
                self.offset + ogre.Vector3(0, 3, -30 + 2 * z))


        domSound = 'perc-%d' % random.randrange(6)
        print 'Selected domino sound is ' + domSound
        makeDomino(app,
                   "d1",
                   self.offset + ogre.Vector3(0, 0.5, 0),
                   80, sound = domSound)
        makeDomino(app,
                   "d2",
                   self.offset + ogre.Vector3(2, 0.25, 0),
                   90, sound = domSound)
        makeDomino(app,
                   "d3",
                   self.offset + ogre.Vector3(4, 0.25, 0),
                   100, sound = domSound)
        makeDomino(app,
                   "d4",
                   self.offset + ogre.Vector3(6, 0.25, 0),
                   110, sound = domSound)
        makeDonut(app,
                   "donut",
                   self.offset + ogre.Vector3(-6, 1, -20))
        makeTiltRamp(app,
                        "tiltRamp",
                        self.offset + ogre.Vector3(15, .1, 5))
        makeMetalCrate(app, "metal crate", 
                        self.offset + ogre.Vector3(40, 1, 0))
        # "scatter" assignment
        (leftDoor, rightDoor) = makeSwingingDoors(app,
                        self.offset + ogre.Vector3(0, 0, 50))
        lock = makeLevelLock(app, self.offset)
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)
        key = makeUnlockKey(app, self.offset + ogre.Vector3(15, 5, 15))
        key.key = lock
        lock.sources.append(key)

    def unload(self, app):
        pass




def makePendulumBall(app, name, offset, material='platform-0', sound=None):
        scn = app.sceneManager
        root = scn.getRootSceneNode()
        name = name + str(offset)

        c = Container(name = name)
        containers[c.id] = c
        c.ent = scn.createEntity(name, 'BallBearing.mesh')
        c.ent.setCastShadows(True)
        c.node = root.createChildSceneNode(name)
        c.node.setPosition(offset)
        c.node.attachObject(c.ent)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.body = ei.createSingleDynamicSphere(1.0, app._world, app._space)
        c.geom = c.body.getGeometry(0)
        c.bouncy = 1.0
        c.friction = 1
        c.body.setDamping(0, 0)
        c.geom.setUserData(c.id)

        c.joint = OgreOde.HingeJoint(app._world)
        c.joint.attach(c.body)
        c.joint.setAxis(ogre.Vector3().UNIT_X)
        c.joint.setAnchor(ogre.Vector3(0, 10, 0) + offset)

        c.ent.setUserObject(c.geom)

        if sound:
            c.sound = app.sounds[sound]
        else:
            pass

        return c

def makePendulumStarterBall(app, name, offset, material='platform-0', sound=None):
        scn = app.sceneManager
        root = scn.getRootSceneNode()
        name = name + str(offset)

        c = Container(name = name)
        containers[c.id] = c
        c.ent = scn.createEntity(name, 'BallBearing.mesh')
        c.ent.setCastShadows(True)
        c.node = root.createChildSceneNode(name)
        c.node.setPosition(offset)
        c.node.attachObject(c.ent)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.body = ei.createSingleDynamicSphere(1.0, app._world, app._space)
        c.bouncy = 1.0
        c.friction = 1
        c.body.setDamping(0, 0)
        c.geom = c.body.getGeometry(0)
        c.geom.setUserData(c.id)

        c.joint = OgreOde.HingeJoint(app._world)
        c.joint.attach(c.body)
        c.joint.setAxis(ogre.Vector3().UNIT_X)
        c.joint.setAnchor(ogre.Vector3(0, 0, 10) + offset)

        c.ent.setUserObject(c.geom)

        if sound:
            c.sound = app.sounds[sound]
        else:
            pass

        return c




