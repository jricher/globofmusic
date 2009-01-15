##
## Glob of Music
##

#
# Level Manager
#

import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS
import SampleFramework as sf

from MusicManager import MusicManager
from Container import *

from threading import Thread
import time

import random

class LevelManager(OgreOde.CollisionListener, object):
    def __init__(self, app, levels):
        OgreOde.CollisionListener.__init__(self)

        self.tempo = 90
        self._world = app._world
        self._world.setCollisionListener(self)
        self._space = app._space
        self.camera = app.camera
        self.player = app.player
        self._plane = app._plane
        self.rootNode = app.sceneManager.getRootSceneNode()
        
        self.doorSounds = []
        
        self.overlay = None
        self.overlayTimeout = None
        
        # this is uninitialized
        self.currentLevel = -1
        self.levels = []


        # list of animations to play
        self.animations = []
        
        self.particles = {}
        self.particleTimeout = None
        self.decayParticle = False

        self.initSounds(app)

        self.initGraphics(app, levels)

        self.setCurrentLevel(0)

        
    def __del__(self):
        if (self._world.getCollisionListener() == self): 
            self._world.setCollisionListener(None)
        del self.camera
        del self._world
        del self._space
        del self.mm
        del self.currentLevel
        del self.levels[:]
        del self.player
        del self._plane
        if self.particles: self.particleSystemCleanup()
        containers.clear()
        del self.animations[:]
        if self.overlay:
            del self.overlay
        del self.rootNode

        
    def initGraphics(self, app, levels):

        scn = app.sceneManager

        scn.setAmbientLight (ogre.ColourValue(0.2, 0.2, 0.25))
        
        # give us a skybox
        scn.setSkyBox(True, 'RedSkyBox')
        
        # Set out our four sub-areas
        # each area is 100x100 units
        # add two rooms to either end

        
        # store up calculated positions while we're at it
        n = len(levels)
        startz = -100 * (n / 2)
        for i in range(0, n + 2):

            if i > 0 and i < n + 1:
                level = levels[i - 1].Level(i)
                level.cameraPosition = ogre.Vector3(0, 0, startz + 100 * i)
                level.playerStart = ogre.Vector3(0, 4, startz - 45 + 100 * i)

                #self.makeCrate("crate " + str(i), self.rootNode, ogre.Vector3(0, 2, startz + 100 * i), scn)
                #self.makeArena(self.rootNode, ogre.Vector3(0, 0, startz + 100 * i), scn, i)
                offset = ogre.Vector3(0, 0, startz + 100 * i)
                level.offset = offset
                level.arena = makeArena(app, offset, i)
                self.levels.append(level)

                #todo: dynamic loading
                level.load(app)
                
            elif i == 0:
                # first room
                level = BaseLevel(i)
                level.cameraPosition = ogre.Vector3(0, 0, startz + 100 * i)
                level.playerStart = ogre.Vector3(0, 4, startz + 25 + 100 * i)
                level.arena = makeStartRoom(app, ogre.Vector3(0, 0, startz + 25 + 100 * i), i)
                self.levels.append(level)
            elif i == n + 1:
                # final room
                level = BaseLevel(i)
                level.cameraPosition = ogre.Vector3(0, 0, startz + 100 * i)
                level.playerStart = ogre.Vector3(0, 4, startz - 125 + 100 * i)
                level.arena = makeEndRoom(app, ogre.Vector3(0, 0, startz - 25 + 100 * i), i)
                self.levels.append(level)

        #(leftDoor, rightDoor) = makeSwingingDoors(app, ogre.Vector3(0, 0, 25))


    def initSounds(self, app):
        sm = app.soundManager
        self.mm = app.musicManager

        self.mm.setTempo(self.tempo)
        
        # grab our background tracks
        app.music['bg-1'] = sm.createSound('bg-1', 'level-0-1.wav', True)
        app.music['bg-2'] = sm.createSound('bg-2', 'level-0-2.wav', True)
        app.music['bg-3'] = sm.createSound('bg-3', 'level-0-3.wav', True)
        app.music['bg-4'] = sm.createSound('bg-4', 'level-0-4.wav', True)

        self.defaultBackgroundMusic = app.music['bg-1']

        # set all music tracks relative to the listener
        for m in app.music.values():
            m.setRelativeToListener(True)
            #m.setGain(0.25)

        # grab all of our sound effects
        files = ['bell-hi-0', 'bell-hi-1', 'bell-lo-0', 'bell-lo-1',
                 'bowen-0', 'bowen-1', 'bowen-2', 'bowen-3',
                 'key-0', 'key-1', 'key-2', 'key-3',
                 'neutron-0', 'neutron-1',
                 'tabla-0', 'tabla-1', 'tabla-2', 'tabla-3', 'tabla-4', 'tabla-5',
                 'wurl-0', 'wurl-1', 'wurl-2', 'wurl-3',
                 'runup']

        for f in files:
            print 'Loading sound %s' % (f + '.wav')
            app.sounds[f] = sm.createSound(f, f + '.wav', False)        

            
        # set all sounds relative to the listener
        for s in app.sounds.values():
            s.setRelativeToListener(True)


    def setCurrentLevel(self, level):
        '''
        Set our current level
        '''

        if level == self.currentLevel:
            print 'Error: entering current level'
            return

        if level < 0:
            print 'Error: negative level', level
            return
        if level >= len(self.levels):
            print 'Error: level id too big', level
            return
        
        if level <= self.currentLevel:
            print 'Error: level going backwards'
            return
        
        # warp the character if we're just starting
        if self.currentLevel == -1:
            self.player.warpTo = (self.levels[level].playerStart)
        
        print 'Entering level %d' % level

        # set the appropriate background music
        if self.currentLevel > 0 and self.levels[self.currentLevel].backgroundMusic:
            self.mm.stopSound(self.levels[self.currentLevel].backgroundMusic, 0)
        else:
            self.mm.stopSound(self.defaultBackgroundMusic, 0)

        self.currentLevel = level

        if self.levels[self.currentLevel].backgroundMusic:
            self.mm.addQueuedSound(self.levels[self.currentLevel].backgroundMusic, self.mm.totalBeats)
        else:
            self.mm.addQueuedSound(self.defaultBackgroundMusic, self.mm.totalBeats)
        

        
        # move the camera
        if self.currentLevel != 0: # Don't animate the camera to start
            
            #self.camera.setPosition(self.cameraPositions[self.area])
            
            node = self.camera.getParentSceneNode()

            sceneManager = node.getCreator()

            # animation code adapted from Demo_CameraTracking.py

            if sceneManager.hasAnimation('CameraTrack'):
                print 'destroying old CameraTrack'

                as = sceneManager.getAnimationState('CameraTrack')
                as.setEnabled(False)
                self.animations.remove(as)
                
                sceneManager.destroyAnimationState('CameraTrack')
                sceneManager.destroyAnimation('CameraTrack')
                
            
            animation = sceneManager.createAnimation('CameraTrack', 2)
            animation.interpolationMode = ogre.Animation.IM_SPLINE
            
            animationTrack = animation.createNodeTrack(0, node)
            
            key = animationTrack.createNodeKeyFrame(0)
            key.setTranslate(node.getPosition())
            
            key = animationTrack.createNodeKeyFrame(2)
            #key.setTranslate (self.levels[self.currentLevel].cameraPosition - self.camera.getPosition())
            key.setTranslate(node.getPosition() + ogre.Vector3().UNIT_Z*100)
            animationState = sceneManager.createAnimationState('CameraTrack')
            animationState.setEnabled(True)
            animationState.setLoop(False)

            self.animations.append(animationState)

        
    # 
    # Called by OgreOde whenever a collision occurs, so 
    # that we can modify the contact parameters
    # 
    def collision(self, contact) :

        ## Check for collisions between things that are connected and ignore them
        g1 = contact.getFirstGeometry()
        g2 = contact.getSecondGeometry()

        #print 'Collision!', contact, g1, g2
        #print dir(g2)
    
        if (g1 and g2):
            b1 = g1.getBody()
            b2 = g2.getBody()
            if (b1 and b2 and OgreOde.Joint.areConnected(b1, b2)):
                #print 'connected by joint!'
                return False
            elif not (b1 or b2):
                # no bodies, two static meshes don't "collide"
                u1 = g1.getUserData()
                u2 = g2.getUserData()

                if u1 in containers and u2 in containers:
                    # print out an error message since this shouldn't happen
                    print 'Static collision error: %s <=> %s' % (containers[u1].name, containers[u2].name)
                return False


            u1 = g1.getUserData()
            u2 = g2.getUserData()

            #print u1, u2

            if u1 in containers and u2 in containers:

                c1 = containers[u1]
                c2 = containers[u2]
                
                # we've got two Container objects, now we can collide them with each other (maybe)
                #print 'Colliding ' + c1.name + ' against ' + c2.name
                col1 = c1.collide(c2, contact, contact.getNormal(), self)
                col2 = c2.collide(c1, contact, -contact.getNormal(), self)

                if col1 or col2:
                    # if either of the collisions is true, we're OK
                    return True
                else:
                    return False
                

    def collideWithDoor(self, me, other, contact, normal):

        # honestly, we don't much care what a door hits

        ## Set the friction at the contact
        
        contact.setCoulombFriction( 20 )    # Don't make the doors too sticky
        contact.setBouncyness(0.5)
    
        ## Yes, this collision is valid
        return True        

    def collideWithPlayer(self, other, contact, normal):

        # note that normal may be flipped on the way in
        if isinstance(other, ArenaFloor):
            #print 'got a player and an arena'
            if not other.hit:
                #print 'not hit yet'
                rc = self.setArea(other.arenaId)
                if not rc == 'CHEATER':
                    other.hit = True
                    if self.overlay:
                        # hide our last overlay
                        self.overlay.hide()
                        self.overlay = None
                        self.overlayTimeout = None
                    #if other.arenaId == 5:
                        # last one
                    #    overlay = ogre.OverlayManager.getSingleton().getByName('CongratsOverlay')
                    #    overlay.show()
                    #    self.fireworks()
        elif isinstance(other, ArenaWalls):
            ## Set the friction at the contact
            contact.setCoulombFriction( 10 )    # walls are pretty slick
            contact.setBouncyness(0.4)
            return True
        elif other is self._plane:
            #print 'Ze Plane!'
            #print self.playerStarts[self.area]
            self.player.warpTo = (self.playerStarts[self.area])

        elif isinstance(other, Platform):
            #print 'Platform'
            # for now, only platforms can be armed and fired
            if other.arm():
                # if we successfully armed this platform, then queue the associated sound
                if not self.mm.isFireKeyQueued(other.id):
                    self.mm.addQueuedSound(other.sound, other.quant, other.rest, other.id)

        elif isinstance(other, Door):
            if other.locked:
                print 'Locked door!'
                if self.overlay:
                    self.overlay.hide()
                self.overlay = ogre.OverlayManager.getSingleton().getByName('DoorLockedOverlay')
                self.overlay.show()
                self.overlayTimeout = 1
                
            if other.sound:
                if not self.mm.isSoundQueued(other.sound):
                    self.mm.addQueuedSound(other.sound, other.quant, other.rest)
            contact.setCoulombFriction( 100 ) # doors should be slippery so we don't get stuck
            contact.setBouncyness(0.1)
            return True
        elif isinstance(other, Powerup):
            #if other.powerupName not in self.player.powerups:
            other.pickedUp(self.player)
            other.destroy()
            print 'Collected %s from %s', (other.powerupName, other.name)
            if other.sound:
                if not self.mm.isSoundQueued(other.sound):
                    self.mm.addQueuedSound(other.sound, other.quant, other.rest)
            return False # roll right through
        else:
            print "What a strange container?!", other.name
                       
    
        ## Set the friction at the contact
        ## Infinity didn't get exposed :(
        contact.setCoulombFriction( 9999999999 )    ### OgreOde.Utility.Infinity)
        contact.setBouncyness(0.4)
    
        ## Yes, this collision is valid
        return True
    def collideWithPlatform(self, me, other, contact, normal):
        # note that by now we should be able to tell that 'other' is not a player
        
        if isinstance(other, Domino):
            #If a domino hits a platform, arm the platform
            if me.arm():
                # if we successfully armed this platform, then queue the associated sound
                if not self.mm.isFireKeyQueued(me.id):
                    self.mm.addQueuedSound(me.sound, me.quant, me.rest, me.id)
        elif isinstance(other, Arena):
            # it's harmless to bounce an arena off of this, nothing special
            pass
        elif isinstance(other, Door):
            # doors are likewise harmless, and this actually happens in area 3
            pass
        elif isinstance(other, Platform):
            
            if me.arm():
                if not self.mm.isFireKeyQueued(me.id):
                    self.mm.addQueuedSound(me.sound, me.quant, me.rest, me.id)
        else:
            print "%s really shouldn't run into %s" % (str(other.name), str(me.name))
            
        ## Set the friction at the contact
        ## Infinity didn't get exposed :(
        contact.setCoulombFriction( 9999999999 )    ### OgreOde.Utility.Infinity)
        contact.setBouncyness(0.4)
    
        ## Yes, this collision is valid
        return True


    def animate(self, frameEvent):
        t = frameEvent.timeSinceLastFrame

        # animate overlays
        #print self.overlay, self.overlayTimeout
        if self.overlay and self.overlayTimeout != None:
            self.overlayTimeout -= t
            if self.overlayTimeout < 0:
                self.overlayTimeout = None
                self.overlay.hide()
                self.overlay = None
                
        if self.decayParticle and "StartArrow" in self.particles:
            self.particleTimeout -= t
            if self.particleTimeout < 0:
                self.particleTimeout = None
                self.particleSystemCleanup()
                self.decayParticle = False

        # step through all animations and check for dead ones
        dead = []
        for a in self.animations:
            if a.getEnabled() and not a.hasEnded():
                a.addTime(t)
                #print self.camera.getParentSceneNode().getPosition()
            else:
                # python really needs an iterator.remove function...
                dead.append(a)

        for d in dead:
            print 'removing dead animation', d
            name =  d.getAnimationName()
            print '  %s' % name

            d.setEnabled(False)
            
            # this is a hack to get at the sceneManager
            node = self.camera.getParentSceneNode()
            scn = node.getCreator()

            if scn.hasAnimation(name):
                scn.destroyAnimation(name)
                scn.destroyAnimationState(name)
            print self.animations
            self.animations.remove(d)

        del dead
        


 

    def areaClear(self):
        print 'Area clear!'
        if self.overlay:
            self.overlay.hide()
        if self.overlayTimeout != None:
            self.overlayTimeout = None
        
        self.overlay = ogre.OverlayManager.getSingleton().getByName('AreaClearOverlay')
        self.overlay.show()
        
        if self.area == 1:
            self.loadArea1()
            if self.ramps:
                for id in self.ramps:
                    if containers[id].body:
                        containers[id].body.wake()
                    del containers[id]
                del self.ramps[:]
            self.startingArrow(-40)
        elif self.area == 2:
            self.loadArea2()
            self.startingArrow(100-40)
        elif self.area == 3:
            self.loadArea3()
            self.startingArrow(200-40)
        elif self.area == 4: 
            self.startingArrow(300-40)
            #self.fireWholeMaze()

            
        # TODO: animate fading ramp

    def fireworks(self):
        scn = self.rootNode.getCreator()
        c = Container("Fireworks")
        c.particleSystem = scn.createParticleSystem('fireworks', 'Examples/njrFireworks')
        c.particleSystem.setKeepParticlesInLocalSpace(True)
        
        c.node = self.rootNode.createChildSceneNode("Fireworks")
        c.node.setPosition(0, 0, 375)
        
        c.node.attachObject(c.particleSystem)
        
        self.particles["Fireworks"] = c
        
    def startingArrow(self, offset):
        scn = self.rootNode.getCreator()
        
        #if ("StartArrow" in self.particles):
        #    scn.destroyParticleSystem(self.particles["StartArrow"].particleSystem)
        #    del self.particles["StartArrow"].particleSystem
        #    scn.destroySceneNode("StartArrow")
        #    self.particles.clear()
            
        c = Container("StartArrow")
        c.particleSystem = scn.createParticleSystem('arrow', 'Examples/njrGreenyNimbus')
        c.particleSystem.setKeepParticlesInLocalSpace(True)
        
        c.node = self.rootNode.createChildSceneNode("StartArrow")
        c.node.setPosition(0, 5, offset)
    
        c.node.attachObject(c.particleSystem)
        self.particles["StartArrow"] = c
        self.particleTimeout = 4
        
    def particleSystemCleanup(self):
        #self.particles["StartArrow"].particleSystem.removeAllEmitters()
        scn = self.rootNode.getCreator()
        c = self.particles["StartArrow"]
        scn.destroyParticleSystem(c.particleSystem)
        del c.particleSystem
        scn.destroySceneNode(c.node.getName())
        self.particles.clear()

    def resetPlayer(self):
        self.player.warpTo = self.levels[self.currentLevel].playerStart

