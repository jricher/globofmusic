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
        self.backgroundMusic = app.music['bg-1']
        makePlatform(app, "Testing #1", self.offset + ogre.Vector3(0,1,-40))
        makeCrate(app, "A Crater", self.offset + ogre.Vector3(-10,0,10))
        makeCrate(app, "A Crated", self.offset + ogre.Vector3(-10,0,20))
        (leftdoor, rightdoor) = makeSwingingDoors(app,self.offset + ogre.Vector3(0,0,50))
        myLock = makeLevelLock(app, self.offset + ogre.Vector3(20,0,20))
        leftdoor.lock(app._world, myLock)
        rightdoor.lock(app._world, myLock)

        metalCrate = makeMetalCrate(app, "MetalCreate 1", self.offset + ogre.Vector3(0,1.25,20))
##        makeBell(app,"Bell",self.offset + ogre.Vector3(0,1,0))
        makeGear(app,"Gear",self.offset + ogre.Vector3(2,1,0))
        key = makeUnlockKey(app, self.offset + ogre.Vector3(0,2,26), lock = myLock)
        makeIcePlatform(app,"Ice Platform", self.offset + ogre.Vector3(-20,0,2))
        makeBallBearing(app,'Bearing',self.offset + ogre.Vector3(40,1,0))
        makeCone(app,'Cone',self.offset + ogre.Vector3(30,1,0))
        makeDumbbell(app, 'Barbell',self.offset + ogre.Vector3(30,1,6))

    def unload(self, app):
        pass
    
def makeIcePlatform(app, name, offset, angle=0, material="Icy-", sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    print 'Making Ice Platform:  ' + '  @  ' + str(offset)
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
                  
def makeDumbbell(app, name, offset, angle=0):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    name = name + str(offset)

    offset = offset + ogre.Vector3(0, 1, 0)

    c = Barbell(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Barbell.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    #ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    #ei = OgreOde.EntityInformer(c.ent, ogre.Matrix4.getScale(c.node.getScale()))
    ei = OgreOde.EntityInformer(c.ent)
    
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
##    mass = OgreOde.BoxMass (1.0, ei.getSize()) ## TODO: make it the sphere mass
    mass = OgreOde.CapsuleMass(0.05, 2.0, ogre.Vector3().UNIT_X, 5.0)
    mass.setDensity(0.5, 2.0, ogre.Vector3().UNIT_X, 5.0)
##    mass.setDensity(1.0, ei.getSize())
    c.body.setMass(mass)
    c.body.setDamping(2,2)
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)

    c.body.setPosition(offset)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.body.setOrientation(quat)
    

    c.geom.setUserData(c.id)
    
    c.friction = 400

    return c    
