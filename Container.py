##
## Glob of Music
## Copyright 2007
##  Justin Richer
##  Nathan Rackliffe
##  Paul Laidler
##  Rob Whalen
##

import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

# A set of generic containers to hold OGRE, ODE, and OpenAL entities in one place

class Container(object):

    def __init__(self, name = None):
        self.body = None # ODE body
        self.geom = None # ODE geometry
        self.node = None # OGRE scene node
        self.ent = None  # OGRE entity
        self.joint = None # ODE Joint
        self.sound = None  # OpenAL sound
        self.sounds = [] # List of OpenAL sounds
        self.quant = None # MusicManager quantization
        self.rest = None # MusicManager post-sound rest
        self.name = name  # name to refer to this by
        self.anim = None # animation
        self.friction = 500
        self.bouncy = 0.1
        
        self.id = _mkId() # unique ID (useful for setUserData calls)

        #containers[self.id] = self

    def __del__(self):
        #For some reason, this destructor isn't sufficent.  There is a memory leak in here someplace
        if not Container:
            return
        self.destroy()
        if self.body:
            del self.body
        if self.node:
            del self.node
        if self.ent:
            del self.ent
        if self.joint:
            self.joint.detach()
            del self.joint
        if self.geom:
            self.geom.disable()
            del self.geom
        if self.sound:
            del self.sound
        if self.sounds:
            del self.sounds
        if self.quant:
            del self.quant
        if self.rest:
            del self.rest
        if self.id:
            del self.id
        if self.anim:
            del self.anim
        if self.friction:
            del self.friction
        if self.bouncy:
            del self.bouncy
        #print "Container deleted"
        
    def destroy(self):
        if self.ent and self.node:
            scn = self.node.getCreator()
            self.node.detachObject(self.ent)
            scn.destroyEntity(self.ent.getName())

            if self.body:
                pass

            if self.geom:
                self.geom.disable()

            if self.anim:
                as = scn.getAnimationState(self.anim.getName())
                as.setEnabled(False)
                #scn.destroyAnimationState(self.anim.getName())
                #scn.destroyAnimation(self.anim.getName())
                
                
            
            scn.destroySceneNode(self.node.getName())

            self.ent = None
            self.node = None
            self.body = None
            self.geom = None

    def collide(self, other, contact, normal, lm):
        # by default, everything's collidable

        #contact.setCoulombFriction(max(self.friction, other.friction))
        #contact.setBouncyness(max(self.bouncy, other.bouncy))

        if not other.collideWith(self, contact, -normal, lm):
            contact.setCoulombFriction(self.friction)
            contact.setBouncyness(self.bouncy)

        # make a noise if the player hits it
        if self.sound and isinstance(other, Player):
            lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id)

        return True

    def collideWith(self, other, contact, normal, lm):
        return False

def _mkId():
    '''
    Generator function for unique IDs
    '''
    
    _mkId.__maxID = _mkId.__maxID + 1
    return _mkId.__maxID

_mkId.__maxID = 0




class Player(Container):
    def __init__(self, name = None):
        Container.__init__(self, name)
        self.warpTo = None
        self.jumpVector = ogre.Vector3().ZERO
        self.jumpTime = 0.0
        self.powerups = []

    def __del__(self):
        if not Container:
            return
        if self.warpTo:
            del self.warpTo
        if self.jumpVector:
            del self.jumpVector
        if self.jumpTime:
            del self.jumpTime
        if self.powerups:
            del self.powerups
        Container.__del__(self)

    def collide(self, other, contact, normal, lm):
        # take care of jumping, that's it
        if normal != self.jumpVector:
            self.jumpVector = normal

        self.jumpTime = 0.050 # jump for just a bit

        return Container.collide(self, other, contact, normal, lm)
                    
    def collideWith(self, other, contact, normal, lm):
        # take care of jumping, that's it
        if normal != self.jumpVector:
            self.jumpVector = normal

        self.jumpTime = 0.050 # jump for just a bit

        return False
                    


class Powerup(Container):
    def __init__(self, powerupName, name = None):
        Container.__init__(self, name)

        self.powerupName = powerupName
        self.overlay = None
        
    def __del__(self):
        if self.powerupName:
            del self.powerupName
        if self.overlay:
            del self.overlay
        if not Container:
            return
        Container.__del__(self)

    def pickedUp(self, player):
        if self.powerupName not in player.powerups:
            player.powerups.append(self.powerupName)

        if self.overlay:
            self.overlay.show()

        #del containers[self.id]
            
            

class Fireable(Container):
    def __init__(self, name = None, materialName = None, restartable = False, key = None):
        Container.__init__(self, name)
        self.state = 'waiting'
        self.materialName = materialName
        self.restartable = restartable
        self.setMaterial()
        self.key = key
        self.fireCallback = None
        
    def __del__(self):
        if not Container:
            return
        Container.__del__(self)
        del self.state
        del self.materialName
        del self.restartable
        del self.key
        if self.fireCallback:
            del self.fireCallback

    def isArmed(self):
        return self.state == 'armed'

    def isFired(self):
        return self.state == 'fired' 
        
    def isDone(self):
        return self.state == 'done'

    def arm(self):
        '''
        Arm this platform. Returns True if successfully armed.
        '''
        if self.state == 'waiting' or ((self.state == 'fired' or self.state == 'done') and self.restartable):
            self.state = 'armed'
            self.setMaterial()
            return True
        else:
            return False

    def fire(self):
        '''
        Fire this platform. Return True if successfully fired. Note that platforms must be armed first.
        '''
        if self.state == 'armed':
            self.state = 'fired'
            self.setMaterial()

            if self.key:
                # tell our key that we've fired
                self.key.platformFired(self)
            if self.fireCallback:
                self.fireCallback()
            
            return True
        else:
            return False
        
    def done(self):
        self.state = "done"
        self.setMaterial()
        
    def reset(self):
        self.state = "waiting"
        self.setMaterial()

    def setMaterial(self):
        '''
        Set a material on the first sub-entity if we have the right parts
        '''
        if self.ent and self.materialName:
            sub = self.ent.getSubEntity(0)
            sub.materialName = self.materialName + self.state


    def collide(self, other, contact, normal, lm):
        if isinstance(other, Player) and self.arm():
            if not lm.mm.isFireKeyQueued(self.id):
                lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id)
        return Container.collide(self, other, contact, normal, lm)
        
    def collideWith(self, other, contact, normal, lm):
        if isinstance(other, Player) and self.arm():
            if not lm.mm.isFireKeyQueued(self.id):
                lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id)
        return False
        
class Platform(Fireable):
    def __init__(self, name = None, materialName = None, restartable = False, key = None):
        Fireable.__init__(self, name, materialName, restartable, key)
    def __del__(self):
        if not Fireable:
            return
        Fireable.__del__(self)

                
class MultiKey(object):
    def __init__(self, name = None):
        self.name = name
        self.doors = []
        self.platforms = []
        self.unlockCallback = None

    def __del__(self):
        del self.name
        del self.doors[:]
        del self.platforms[:]
        del self.unlockCallback
        
    def platformFired(self, source):
        '''
        Call when a platform has fired, will unlock all doors if all platforms have fired
        '''
        unlock = source.isFired()
        for p in self.platforms:
            # will turn true as long as all platforms have fired
            #print '%s fired? %s' % (str(p.name), str(p.isFired()))
            unlock = (unlock and p.isFired()) or (unlock and p.isDone())

        if unlock:
            for d in self.doors:
                print 'Unlocking door', d.name
                d.unlock()
            if self.unlockCallback:
                self.unlockCallback()
 
class ArenaFloor(Container):
    def __init__(self, name, arenaId):
        Container.__init__(self, name)
        self.hit = False
        self.arenaId = arenaId

    def __del__(self):
        if not Container:
            return
        Container.__del__(self)
        del self.hit
        del self.arenaId

    def collide(self, other, contact, normal, lm):
        if isinstance(other, Player):
            # floors are pretty sticky
            contact.setCoulombFriction( 9999999999 )    ### OgreOde.Utility.Infinity)
            contact.setBouncyness(0.4)

            if lm.currentLevel is not self.arenaId :
                lm.setCurrentLevel(self.arenaId)
    
            ## Yes, this collision is valid
            return True
        else:
            return Container.collide(self, other, contact, normal, lm)
        
    def collideWith(self, other, contact, normal, lm):
        if isinstance(other, Player):
            # floors are pretty sticky
            contact.setCoulombFriction( 9999999999 )    ### OgreOde.Utility.Infinity)
            contact.setBouncyness(0.4)

            if lm.currentLevel is not self.arenaId :
                lm.setCurrentLevel(self.arenaId)
    
            ## Yes, we changed things
            return True
        else:
            return False
        

class ArenaWalls(Container):
    def __init__(self, name, arenaId):
        Container.__init__(self, name)
        self.arenaId = arenaId
        self.friction = 100
        self.bouncy = 0.7

    def __del__(self):
        if not Container:
            return
        Container.__del__(self)
        del self.arenaId

    def collide(self, other, contact, normal, lm):
        contact.setCoulombFriction(self.friction)    # walls are pretty slick
        contact.setBouncyness(self.bouncy)
        return True

    def collideWith(self, other, contact, normal, lm):
        contact.setCoulombFriction(self.friction)    # walls are pretty slick
        contact.setBouncyness(self.bouncy)
        return True

class Arena(object):
    def __init__(self, floor, walls, arenaId):
        self.floor = floor
        self.walls = walls
        self.arenaId = arenaId

    def __del__(self):
        del self.floor
        del self.walls
        del self.arenaId
    
class GroundPlane(Container):
    def __init__(self, name):
        Container.__init__(self, name)

    def __del__(self):
        if not Container:
            return
        Container.__del__(self)

    def collide(self, other, contact, normal, lm):
        if isinstance(other, Player):
            lm.resetPlayer()
        return True

    def collideWith(self, other, contact, normal, lm):
        if isinstance(other, Player):
            lm.resetPlayer()
        return False
    
class Door(Container):
    def __init__(self, name):
        Container.__init__(self, name)
        self.locks = []
        self.locked = False

    def __del__(self):
        if not Container:
            return
        Container.__del__(self)
        del self.locks
        del self.locked

    def lock(self, _world):
        # create fixed joint to form a lock
        l = OgreOde.FixedJoint(_world)
        l.attach(self.body)
        self.locks.append(l)
        self.locked = True
        
    def unlock(self):
        '''
        once unlocked, cant be re-locked
        '''
        del self.locks[:]
        self.locked = False

class Domino(Platform):
    def __init__(self, name, angle=0.0, materialName = None):
        self.angle = angle
        self.startPosition = None
        Platform.__init__(self, name, materialName, False)
        #newMaterial = "Domino%d-" % (int(name[-1]) % 6)
        newMaterial = "Domino%d-" % (self.id % 8)
        #print newMaterial 
        self.materialName = newMaterial
        self.setMaterial() 
    
    def __del__(self):
        #print "domino.__del__"
        del self.angle
        del self.startPosition 
        if not Platform:
            return
        Platform.__del__(self)

    def fire(self):
        if Platform.fire(self):
            pass
            #if self.geom:
            #    self.geom.disable()
            
    

# lookup table for containers
containers = {}



class BaseLevel(object):
    def __init__(self, levelId):
        self.levelId = levelId
        self.cameraAnchor = None
        self.playerStart = None
        self.backgroundMusic = None
        self.arena = None
        self.offset = None
        self.startLevelCallback = None
        
    def __del__(self):
        del self.levelId
        del self.cameraAnchor
        del self.playerStart
        del self.backgroundMusic
        del self.arena
        del self.offset
        del self.startLevelCallback

# creation functions
def makeArena(app, offset, i):

    scn = app.sceneManager
    root = scn.getRootSceneNode()

    print 'Making arena: ' + str(i) + ' @ ' + str(offset)
    
    # set up the arena floors
    floor = ArenaFloor('ArenaFloor%d' % i, i)
    containers[floor.id] = floor
    floor.ent = scn.createEntity('ArenaFloor%d' % i, 'ArenaFloor.mesh')
    floor.node = root.createChildSceneNode('ArenaFloor%d' % i)
    floor.node.setPosition(ogre.Vector3() + offset)
    floor.node.attachObject(floor.ent)

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
    wall.ent = scn.createEntity('ArenaWall%d' % i, 'ArenaWalls.mesh')
    wall.node = root.createChildSceneNode('ArenaWall%d' % i)
    wall.node.setPosition(ogre.Vector3() + offset)
    wall.node.attachObject(wall.ent)

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

def makeCrate(app, name, position):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Fireable(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Cube.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)
    #c.ent.setScale(4, 4, 4)

    #sub = c.ent.getSubEntity(0)
    #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)

    c.node.setPosition(position)

    c.node.setScale(2, 2.5, 2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(0.5, app._world, app._space)
    #c.body.setDamping(2,2)
    #c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    
    return c

def makeSleepyCrate(app, name, position):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Fireable(name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "Cube.mesh")
    #c.ent.setNormaliseNormals(True)
    c.ent.setCastShadows(True)
    #c.ent.setScale(4, 4, 4)

    #sub = c.ent.getSubEntity(0)
    #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door

    c.node = root.createChildSceneNode(c.ent.getName())
    c.node.attachObject(c.ent)

    c.node.setPosition(position)

    c.node.setScale(2, 2.5, 2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(50.5, app._world, app._space)
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
    key = MultiKey()
    c = makeTiltingPlatform(app, 'StatringRoom Platform0', offset + ogre.Vector3(0, 2, -10))

    c.sound = app.sounds['key-0']
    c.quant = 8
    
    c.key = key
    key.platforms.append(c)

    (leftDoor, rightDoor) = makeSwingingDoors(app, offset)
    #leftDoor.lock(self._world)
    rightDoor.lock(app._world)
    #key.doors.append(leftDoor)
    key.doors.append(rightDoor)

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
    

def makePlatform(app, name, offset, material='platform0-'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
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

    c.geom.setUserData(c.id)

    return c

def makeTiltingPlatform(app, name, offset, material='platform0-'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
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
    c.node.setPosition(ogre.Vector3(4,2.5,24.5) + offset)
    c.node.setScale(4,1,2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(20.0, app._world, app._space)
    c.body.setDamping(0,20)
    c.geom = c.body.getGeometry(0)

    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_Y)
    c.joint.setAnchor(ogre.Vector3(7.5,2.5,24.5) + offset)
    
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
    c.node.setPosition(ogre.Vector3(-4.1,2.5,24.5) + offset)
    c.node.setScale(4,1,2)
    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(20.0, app._world, app._space)
    c.body.setDamping(0,2)
    c.geom = c.body.getGeometry(0)

    c.joint = OgreOde.HingeJoint(app._world)
    c.joint.attach(c.body)
    c.joint.setAxis(ogre.Vector3().UNIT_Y)
    c.joint.setAnchor(ogre.Vector3(-7.6,2.5,24.5) + offset)
    
    c.geom.setUserData(c.id)
    
    doors.append(c)


    return doors


