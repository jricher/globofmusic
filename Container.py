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
import random


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
        if self.sound and isinstance(other, Player) and not lm.mm.isSoundQueued(self.sound):
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
                self.key.sourceFired(self)
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
            if self.sound and not lm.mm.isFireKeyQueued(self.id):
                lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id)
        return Container.collide(self, other, contact, normal, lm)
        
    def collideWith(self, other, contact, normal, lm):
        if isinstance(other, Player) and self.arm():
            if self.sound and not lm.mm.isFireKeyQueued(self.id):
                lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id)
        return False
        
class Platform(Fireable):
    def __init__(self, name = None, materialName = None, restartable = False, key = None):
        Fireable.__init__(self, name, materialName, restartable, key)
    def __del__(self):
        if not Fireable:
            return
        Fireable.__del__(self)

class Key(Fireable):
    def __init__(self, name = None):
        Fireable.__init__(self, name)
    def __del__(self):
        if not Fireable:
            return
        Fireable.__del__(self)

    def setMaterial(self):
        if self.ent:
            n = self.ent.getNumSubEntities()
            for i in range(n):
                sub = self.ent.getSubEntity(i)
                sub.materialName = self.materialName + self.state

               
class MultiPartLock(object):
    def __init__(self, name = None):
        self.name = name
        self.doors = []
        self.sources = []
        self.unlockCallback = None

    def __del__(self):
        del self.name
        del self.doors[:]
        del self.sources[:]
        del self.unlockCallback
        
    def sourceFired(self, source):
        '''
        Call when a platform has fired, will unlock all doors if all platforms have fired
        '''
        unlock = source.isFired()
        for p in self.sources:
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
        self.wide = False
        
    def __del__(self):
        del self.levelId
        del self.cameraAnchor
        del self.playerStart
        del self.backgroundMusic
        del self.arena
        del self.offset
        del self.startLevelCallback
        del self.wide

class Rupee(Powerup):
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
        
    def collide(self, other, contact, normal, lm):
        return Container.collide(self, other, contact, normal, lm)