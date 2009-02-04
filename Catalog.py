import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *

def makeArena(app, offset, i, wide, angle=0):

    scn = app.sceneManager
    root = scn.getRootSceneNode()

    print 'Making arena: ' + str(i) + ' @ ' + str(offset)
    
    # set up the arena floors
    floor = ArenaFloor('ArenaFloor%d' % i, i)
    containers[floor.id] = floor
    if wide:
        floor.ent = scn.createEntity('ArenaFloor%d' % i, 'WideArenaFloor.mesh')
    else:
        floor.ent = scn.createEntity('ArenaFloor%d' % i, 'ArenaFloor.mesh')
    floor.node = root.createChildSceneNode('ArenaFloor%d' % i)
    floor.node.setPosition(offset)
    floor.node.attachObject(floor.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    floor.node.setOrientation(quat)

    floor.ent.setCastShadows(False)
    
    # set the floor color properly
    sub = floor.ent.getSubEntity(0)
    sub.materialName = 'Floor%d' % ((i) % 4)
    
    # copied from SimpleScenes_TriMesh, there's probably a much more efficient way to do this
    ei = OgreOde.EntityInformer(floor.ent, floor.node._getFullTransform())
    floor.geom = ei.createStaticTriangleMesh(app._world, app._space)
    floor.ent.setUserObject(floor.geom)
    
    floor.geom.setUserData(floor.id)

    # make some walls
    wall = ArenaWalls('ArenaWall%d' % i, i)
    containers[wall.id] = wall
    if wide:
        wall.ent = scn.createEntity('ArenaWall%d' % i, 'WideArenaWalls.mesh')
    else:
        wall.ent = scn.createEntity('ArenaWall%d' % i, 'ArenaWalls.mesh')
    wall.node = root.createChildSceneNode('ArenaWall%d' % i)
    wall.node.setPosition(offset)
    wall.node.attachObject(wall.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    wall.node.setOrientation(quat)

    wall.ent.setCastShadows(False)
    
    # copied from SimpleScenes_TriMesh, there's probably a much more efficient way to do this
    ei = OgreOde.EntityInformer(wall.ent, wall.node._getFullTransform())
    wall.geom = ei.createStaticTriangleMesh(app._world, app._space)
    wall.ent.setUserObject(wall.geom)
    
    wall.geom.setUserData(wall.id)

    #makeBlockingWall(app, offset + ogre.Vector3(0, 210, 50), i)

    return Arena(floor, wall, i)

def makeBlockingWall(app, offset, i):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Container('Big Wall %d' % i)
    containers[c.id] = c
    c.ent = scn.createEntity(c.name, "BlockingWall.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(False)

    #sub = c.ent.getSubEntity(0)
    #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)

    c.node.setPosition(offset)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.geom = ei.createSingleStaticBox(app._world, app._space)
    #c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    
    return c

def makeCrate(app, name, offset, angle=0):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    offset = offset + ogre.Vector3(0, 1.25, 0)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Cube.mesh")
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
    c.node.setScale(2, 2.5, 2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(0.5, app._world, app._space)
    #c.body.setDamping(2,2)
    #c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    
    return c

def makeMetalCrate(app, name, offset):
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
    c.body = ei.createSingleDynamicBox(1.5, app._world, app._space)
    c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    
    return c


def makeStartRoom(app, offset, i):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    # start room

    floor = ArenaFloor('StartRoomFloor', i)
    containers[floor.id] = floor
    floor.ent = scn.createEntity('StartRoomFloor', 'ArenaEndFloor.mesh')
    floor.node = root.createChildSceneNode('StartRoomFloor')
    floor.node.setPosition(offset)
    floor.node.setOrientation(ogre.Quaternion(ogre.Degree(180), ogre.Vector3().UNIT_Y)) #flip it around
    floor.node.attachObject(floor.ent)
    floor.ent.setCastShadows(False)

    ei = OgreOde.EntityInformer(floor.ent, floor.node._getFullTransform())
    floor.geom = ei.createStaticTriangleMesh(app._world, app._space)
    floor.ent.setUserObject(floor.geom)

    # set the floor color properly
    sub = floor.ent.getSubEntity(0)
    sub.materialName = 'EndFloor'
    
    floor.geom.setUserData(floor.id)

    # walls
    walls = ArenaWalls('StartRoomWalls', i)
    containers[walls.id] = walls
    walls.ent = scn.createEntity('StartRoomWalls', 'ArenaEndWalls.mesh')
    walls.node = root.createChildSceneNode('StartRoomWalls')
    walls.node.setPosition(offset)
    walls.node.setOrientation(ogre.Quaternion(ogre.Degree(180), ogre.Vector3().UNIT_Y)) #flip it around
    walls.node.attachObject(walls.ent)
    walls.ent.setCastShadows(False)

    ei = OgreOde.EntityInformer(walls.ent, walls.node._getFullTransform())
    walls.geom = ei.createStaticTriangleMesh(app._world, app._space)
    walls.ent.setUserObject(walls.geom)

    walls.geom.setUserData(walls.id)
    
    #Starting Room platform
    lock = makeLevelLock(app, offset)

    c = makeUnlockKey(app, offset + ogre.Vector3(0, 2, -10), sound='key-0')
    c.quant = 8

    c = makeUnlockKey(app, offset + ogre.Vector3(0, 2, 10), sound='key-1', lock=lock)
    c.quant = 8

    c = makeUnlockKey(app, offset + ogre.Vector3(10, 2, 0), sound='key-2')
    c.quant = 8

    #makeBarbell(app, "A Domino", offset + ogre.Vector3(-10,10,0), 0)

    c = makeUnlockKey(app, offset + ogre.Vector3(-10, 2, 0), sound='key-3')
    c.quant = 8

    (leftDoor, rightDoor) = makeSwingingDoors(app, offset + ogre.Vector3(0, 0, 24.5))
    leftDoor.lock(app._world, lock)
    rightDoor.lock(app._world, lock)
    
    return Arena(floor, walls, i)
    

def makeEndRoom(app, offset, i):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    

    
    floor = ArenaFloor('EndRoomFloor', i)
    containers[floor.id] = floor
    floor.ent = scn.createEntity('EndRoomFloor', 'ArenaEndFloor.mesh')
    floor.node = root.createChildSceneNode('EndRoomFloor')
    floor.node.setPosition(offset)
    floor.node.attachObject(floor.ent)
    floor.ent.setCastShadows(False)

    ei = OgreOde.EntityInformer(floor.ent, floor.node._getFullTransform())
    floor.geom = ei.createStaticTriangleMesh(app._world, app._space)
    floor.ent.setUserObject(floor.geom)

    # set the floor color properly
    sub = floor.ent.getSubEntity(0)
    sub.materialName = 'EndFloor'
    
    floor.geom.setUserData(floor.id)

    # walls
    walls = ArenaWalls('EndRoomWalls', i)
    containers[walls.id] = walls
    walls.ent = scn.createEntity('EndRoomWalls', 'ArenaEndWalls.mesh')
    walls.node = root.createChildSceneNode('EndRoomWalls')
    walls.node.setPosition(offset)
    walls.node.attachObject(walls.ent)
    walls.ent.setCastShadows(False)

    ei = OgreOde.EntityInformer(walls.ent, walls.node._getFullTransform())
    walls.geom = ei.createStaticTriangleMesh(app._world, app._space)
    walls.ent.setUserObject(walls.geom)

    walls.geom.setUserData(walls.id)

    return Arena(floor, walls, i)
    

def makePlatform(app, name, offset, material='platform0-', sound=None):
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

def makeTiltingPlatform(app, name, offset, material='platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Cup.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (20.0, ei.getSize())
    mass.setDensity(5.0, ei.getSize())
    c.body.setMass(mass)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)

    c.joint = OgreOde.BallJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAnchor(offset)

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    return c

def makeSwingingDoors(app, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    doors = []

    
    ## Create a door hinged on the left hand side
    c = Door('left door')
    containers[c.id] = c
    c.ent = scn.createEntity("Left_Door:" + str(offset),"door.mesh")
    c.ent.setCastShadows(True)

    c.node = root.createChildSceneNode(c.ent.getName())

    c.node.attachObject(c.ent)
    c.node.setPosition(ogre.Vector3(4,2.5,0) + offset)
    c.node.setScale(4,1,2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(20.0, app._world, app._space)
    c.body.setDamping(0,2)
    c.geom = c.body.getGeometry(0)

    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_Y)
    c.joint.setAnchor(ogre.Vector3(7.5,2.5,0) + offset)
    
    c.geom.setUserData(c.id)

    doors.append(c)

    

    ## Create a door hinged on the right hand side
    c = Door('right door')
    containers[c.id] = c
    c.ent = scn.createEntity("Right_Door:" + str(offset),"door.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)

    c.node = root.createChildSceneNode(c.ent.getName())

    c.node.attachObject(c.ent)
    c.node.setPosition(ogre.Vector3(-4.1,2.5,0) + offset)
    c.node.setScale(4,1,2)
    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(20.0, app._world, app._space)
    c.body.setDamping(0,2)
    c.geom = c.body.getGeometry(0)

    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_Y)
    c.joint.setAnchor(ogre.Vector3(-7.6,2.5,0) + offset)
    
    c.geom.setUserData(c.id)
    
    doors.append(c)


    return doors


def makeUnlockKey(app, offset, sound='key-0', lock=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    name = 'Key:' + str(offset)

    c = Key(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Key.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (5.0, ei.getSize()) ## TODO: make it the sphere mass
    mass.setDensity(5.0, ei.getSize())
    c.body.setMass(mass)

    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)

    c.body.setPosition(offset)
    c.body.wake()

    velocity = ogre.Vector3(random.random(), random.random(), random.random())
    velocity.normalise()
    c.body.setAngularVelocity(velocity)

    c.joint = OgreOde.BallJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAnchor(offset)

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['key-%d' % random.randrange(4)]

    if lock:
        c.key = lock
        lock.sources.append(c)

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    return c


def makeIcePlatform(app, name, offset, angle=0, material = None, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'IceChunk.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    c.friction = 10

    return c

    
def makeCornerRamp(app, name, offset, angle=0, material = 'platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'CornerRamp.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['perc-%d' % random.randrange(6)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    return c

    
def makeStraightRamp(app, name, offset, angle=0, material = 'platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'StraightRamp.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    return c

    
def makeUpDownRamp(app, name, offset, angle=0, material = 'platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'UpDownRamp.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['perc-%d' % random.randrange(6)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    return c

    
def makeOnOffRamp(app, name, offset, angle=0, material = 'platform0-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'OnOffRamp.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['perc-%d' % random.randrange(6)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    return c
    
def makeDomino(app, name, offset, angle=0, material = 'Domino-', sound=None):
    scn = app.sceneManager
    rootNode = scn.getRootSceneNode()
    name = name + str(offset)

    # make dominoes float properly
    offset = offset + ogre.Vector3(0, 2.1, 0)

    c = Domino(name,angle, materialName = material)
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
    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
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

def makeBall(app, name, offset):

    scn = app.sceneManager
    rootNode = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Ball.mesh")
    c.ent.setCastShadows(True)
    c.node = rootNode.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)
    c.node.setPosition(offset)

    ei = OgreOde.EntityInformer(c.ent, ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicSphere(10.0, app._world, app._space)

    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)

    return c


def makeBarbell(app, name, offset, angle=0):
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

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (5.0, ei.getSize()) ## TODO: make it the sphere mass
    mass.setDensity(5.0, ei.getSize())
    c.body.setMass(mass)

    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)

    c.body.setPosition(offset)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.body.setOrientation(quat)
    
    c.body.wake()

    c.geom.setUserData(c.id)

    return c
    
def makeRupee(app, name, offset, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Rupee(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'GemRupee.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (5.5, ei.getSize())
    mass.setDensity(0.10, ei.getSize())
    c.body.setMass(mass)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)
     
    velocity = ogre.Vector3(random.random(), random.random(), random.random())
    velocity.normalise()
    c.body.setAngularVelocity(velocity)

    c.joint = OgreOde.BallJoint(app._world)
    
    c.joint.attach(c.body)
    c.joint.setAnchor(offset)

    c.motor = OgreOde.AngularMotorJoint(app._world)
    c.motor.setAnchor(offset)
    c.motor.attach(c.body)
    c.motor.setAxisCount(3)
    c.motor.setAxis(0, OgreOde.AngularMotorJoint.RelativeOrientation_GlobalFrame, ogre.Vector3().UNIT_Y)
    c.motor.setAxis(1, OgreOde.AngularMotorJoint.RelativeOrientation_GlobalFrame, ogre.Vector3().UNIT_X)
    c.motor.setAxis(2, OgreOde.AngularMotorJoint.RelativeOrientation_GlobalFrame, ogre.Vector3().UNIT_Z)

    c.motor.setMode(OgreOde.AngularMotorJoint.Mode_UserAngularMotor)
    c.motor.setAngle(0, 0)
    c.motor.setAngle(1, 0)
    c.motor.setAngle(2, 0)
    c.motor.setParameter(OgreOde.Joint.Parameter_MaximumForce, 5, 1)
    c.motor.setParameter(OgreOde.Joint.Parameter_MotorVelocity, 0, 1)
    c.motor.setParameter(OgreOde.Joint.Parameter_MaximumForce, 5, 2)
    c.motor.setParameter(OgreOde.Joint.Parameter_MotorVelocity, 0, 2)
    c.motor.setParameter(OgreOde.Joint.Parameter_MaximumForce, 5, 3)
    c.motor.setParameter(OgreOde.Joint.Parameter_MotorVelocity, 0, 3)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['bell-%d' % random.randrange(6)]

    c.geom.setUserData(c.id)

    return c

def makeLevelLock(app, offset):
    lock = MultiPartLock()
    def areaClear():
        scn = app.sceneManager
        root = scn.getRootSceneNode()
        overlay = ogre.OverlayManager.getSingleton().getByName('AreaClearOverlay')
        overlay.show()
        if ("StartArrow" not in particles):  
            c = Container("StartArrow")
            c.particleSystem = scn.createParticleSystem('arrow', 'Examples/njrGreenyNimbus')
            c.particleSystem.setKeepParticlesInLocalSpace(True)
        
            c.node = root.createChildSceneNode("StartArrow")
            c.node.setPosition(offset + ogre.Vector3(0,0,-50))
    
            c.node.attachObject(c.particleSystem)
            particles["StartArrow"] = c
        
    lock.unlockCallback = areaClear
    
    return lock

def makePlank(app, name, offset, angle=0, sound=None):
    scn = app.sceneManager
    rootNode = scn.getRootSceneNode()
    name = name + str(offset)

    c = Platform(name, materialName="Plank-")
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Plank.mesh")
    c.ent.setCastShadows(True)
    c.node = rootNode.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)
    c.startPosition = offset
    c.node.setPosition(offset)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    #print 'scale', str(c.node.getScale())
    #print '  mtx', str(ogre.Matrix4.getScale(c.node.getScale()))
    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(0.5,app._world, app._space)
    c.body.setDamping(2, 2)
    c.geom = c.body.getGeometry(0)
    c.geom.setUserData(c.id)

    c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    return c

def makeDonut(app, name, offset, angle=0):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Donut.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (20.0, ei.getSize())
    mass.setDensity(5.0, ei.getSize())
    c.body.setMass(mass)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)

    c.joint = OgreOde.BallJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAnchor(offset)

    c.geom.setUserData(c.id)

    return c

def makeBallBearing(app, name, offset, angle=0):
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

    ei = OgreOde.EntityInformer(c.ent, ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicSphere(10.0, app._world, app._space)

    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)

    return c

def makeBowlingPin(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    offset = offset + ogre.Vector3(0,5.01,0)
    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'BowlingPin.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.CapsuleMass(0.05, 2.0, ogre.Vector3().UNIT_Y, 10.0)
    mass.setDensity(0.02, 2.0, ogre.Vector3().UNIT_Y, 10.0)
    c.body.setMass(mass)
    c.body.setDamping(2,2)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)

    c.geom.setUserData(c.id)

    return c

def makeGear(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    offset = offset + ogre.Vector3(0,1.5,0) 

    c = Container(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Gear.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (0.5, ei.getSize())
    mass.setDensity(0.025, ei.getSize())
    c.body.setMass(mass)
    c.body.setDamping(2,2)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)
    
    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_Y)
    c.joint.setAnchor(offset)

    c.geom.setUserData(c.id)

    return c
    
    
def makeBell(app, name, offset, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    

    c = Fireable(name, materialName='Bell-')
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'Bell.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.body = OgreOde.Body(app._world, 'OgreOde::Body_' + c.node.getName())
    c.node.attachObject(c.body)
    mass = OgreOde.BoxMass (5.5, ei.getSize())
    mass.setDensity(0.10, ei.getSize())
    c.body.setMass(mass)
    
    c.geom.setBody(c.body)
    c.ent.setUserObject(c.geom)
    
    c.body.setPosition(offset)
     
    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_X)
    c.joint.setAnchor(ogre.Vector3(0, 6, 0) + offset)

    c.motor = OgreOde.AngularMotorJoint(app._world)
    c.motor.setAnchor(offset)
    c.motor.attach(c.body)
    c.motor.setAxisCount(1)
    c.motor.setAxis(0, OgreOde.AngularMotorJoint.RelativeOrientation_GlobalFrame, ogre.Vector3().UNIT_X)

    c.motor.setMode(OgreOde.AngularMotorJoint.Mode_UserAngularMotor)
    c.motor.setAngle(0, 0)
    c.motor.setParameter(OgreOde.Joint.Parameter_MaximumForce, 5, 1)
    c.motor.setParameter(OgreOde.Joint.Parameter_MotorVelocity, 0, 1)

    c.geom.setUserData(c.id)


    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['bell-%d' % random.randrange(2)]
        

    return c


def makeBridge(app, name, offset):

    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    

    start = makePlank(app, name+'start', offset + ogre.Vector3(0, 0, -5))
    #l = OgreOde.FixedJoint(app._world)
    #l.attach(start.body)

    start.anchor = OgreOde.HingeJoint(app._world)
    start.anchor.attach(start.body)
    start.anchor.setAxis(ogre.Vector3().UNIT_X)
    start.anchor.setAnchor(offset + ogre.Vector3(0, 0, -5.5))

    prev = start
    for z in range(-4, 5):
        plank = makePlank(app, name + str(z), offset + ogre.Vector3(0, -((5 - abs(z)) / 10.0), z))        
        plank.joint = OgreOde.HingeJoint(app._world)
        plank.joint.attach(prev.body, plank.body)
        plank.joint.setAxis(ogre.Vector3().UNIT_X)
        #print 'hinge:', str((plank.body.getPosition() + prev.body.getPosition()) / 2)
        plank.joint.setAnchor((plank.body.getPosition() + prev.body.getPosition()) / 2)
        prev = plank


    end = makePlank(app, name+'end', offset + ogre.Vector3(0, 0, 5))

    end.joint = OgreOde.HingeJoint(app._world)
    end.joint.attach(prev.body, end.body)
    end.joint.setAxis(ogre.Vector3().UNIT_X)
    end.joint.setAnchor((end.body.getPosition() + prev.body.getPosition()) / 2)

    end.anchor = OgreOde.HingeJoint(app._world)
    end.anchor.attach(end.body)
    end.anchor.setAxis(ogre.Vector3().UNIT_X)
    end.anchor.setAnchor(offset + ogre.Vector3(0, 0, 5.5))
