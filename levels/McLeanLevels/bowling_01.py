import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

        makeOnOffRamp (app,"Ramp1",self.offset + ogre.Vector3(0,0,-42))
        makeUpDownRamp (app,"Ramp2",self.offset + ogre.Vector3(0,0,-38))

        for i in range(-30,20,4):
            makeIcePlatform(app, "Icy1%i"%i, self.offset + ogre.Vector3(2,4.5,i))
        for i in range(-30,20,4):
            makeIcePlatform(app, "Icy2%i"%i, self.offset + ogre.Vector3(-2,4.5,i))
        #for i in range(-30,20,4):
        #    makeIcePlatform(app, "Icy3%i"%i, self.offset + ogre.Vector3(-4,2,i))

        for i in range (22,38,4):
            for j in range (8,-12,-4):
                makeIcePlatform(app,"Icy4%d"%j, self.offset + ogre.Vector3(j,4.5,i))

        lock = makeLevelLock(app, self.offset)

        c = makeUnlockKey(app, self.offset + ogre.Vector3 (-4,6.5,33))
        c.quant = 8
        c.key = lock
        lock.sources.append(c)
                          
        c = makeUnlockKey(app, self.offset + ogre.Vector3(4,6.5,33))
        c.quant = 8
        c.key = lock
        lock.sources.append(c)

        (leftDoor, rightDoor) = makeSwingingDoors(app,
                         self.offset + ogre.Vector3 (0,0,50))
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)
        
        self.backgroundMusic = app.music['bg-5']

        makeBowlingCrate (app,
                   "BowlingPin1",
                   self.offset + ogre.Vector3 (0,6.5,21))

        makeBowlingCrate (app,
                   "BowlingPin2",
                   self.offset + ogre.Vector3 (2,6.5,24))

        makeBowlingCrate (app,
                   "BowlingPin3",
                   self.offset+ogre.Vector3 (-2,6.5,24))

        makeBowlingCrate (app,
                   "BowlingPin4",
                   self.offset+ogre.Vector3 (0,6.5,27))

        makeBowlingCrate (app,
                   "BowlingPin5",
                   self.offset+ogre.Vector3 (-4,6.5,27))

        makeBowlingCrate (app,
                   "BowlingPin6",
                   self.offset+ogre.Vector3 (4,6.5,27))

        makeBowlingCrate (app,
                   "BowlingPin7",
                   self.offset+ogre.Vector3 (-2,6.5,30))

        makeBowlingCrate (app,
                   "BowlingPin8",
                   self.offset+ogre.Vector3 (2,6.5,30))

        makeBowlingCrate (app,
                   "BowlingPin9",
                   self.offset+ogre.Vector3 (-6,6.5,30))

        makeBowlingCrate (app,
                   "BowlingPin10",
                   self.offset+ogre.Vector3 (6,6.5,30))

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
    c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
                             
    c.geom.setUserData(c.id)
    c.friction = 10

    return c

def makeBowlingCrate(app, name, offset, angle=0):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    offset = offset + ogre.Vector3(0, 1.25, 0)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "BowlingPin.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)
    #c.ent.setScale(4, 4, 4)

    #sub = c.ent.getSubEntity(0)
    #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)
    

    c.node.setPosition(offset)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    c.node.setScale(0.4, 0.5, 0.3)

    ei = OgreOde.EntityInformer (c.ent, ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(0.5, app._world, app._space)
    #c.body.setDamping(2,2)
    #c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    mass = OgreOde.BoxMass(0.1, c.geom.getSize())

    c.geom.setUserData(c.id)
    c.body.setMass(mass)
    c.friction = 50

    return c
