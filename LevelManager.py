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
from Catalog import *

from threading import Thread
import time

import random

class LevelManager(OgreOde.CollisionListener, object):
    def __init__(self, app, levels, names):
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

        self.initGraphics(app, levels, names)

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
        if self.particles: 
            for name in particles.keys():
                self.particleSystemCleanup(name)
        containers.clear()
        particles.clear()
        del self.animations[:]
        if self.overlay:
            del self.overlay
        del self.rootNode

        
    def initGraphics(self, app, levels, names):

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
                level.name = names[i - 1]
                level.cameraAnchor = ogre.Vector3(0, 0, startz + 100 * i)
                level.playerStart = ogre.Vector3(0, 4, startz - 45 + 100 * i)

                #self.makeCrate("crate " + str(i), self.rootNode, ogre.Vector3(0, 2, startz + 100 * i), scn)
                #self.makeArena(self.rootNode, ogre.Vector3(0, 0, startz + 100 * i), scn, i)
                offset = ogre.Vector3(0, 0, startz + 100 * i)
                level.offset = offset
                level.arena = makeArena(app, offset, i, level.wide)
                self.levels.append(level)

                #todo: dynamic loading
                level.load(app)
                
            elif i == 0:
                # first room
                level = BaseLevel(i)
                level.name = 'Start'
                level.cameraAnchor = ogre.Vector3(0, 0, startz + 100 * i)
                level.playerStart = ogre.Vector3(0, 4, startz + 25 + 100 * i)
                level.arena = makeStartRoom(app, ogre.Vector3(0, 0, startz + 25 + 100 * i), i)
               
                #level.startLevelCallback = self.snow
                self.levels.append(level)
            elif i == n + 1:
                # final room
                level = BaseLevel(i)
                level.name = 'Finish'
                level.cameraAnchor = ogre.Vector3(0, 0, startz + 100 * i)
                level.playerStart = ogre.Vector3(0, 4, startz - 125 + 100 * i)
                level.arena = makeEndRoom(app, ogre.Vector3(0, 0, startz - 25 + 100 * i), i)
                level.startLevelCallback = self.fireworks
                    
                self.levels.append(level)

    def initSounds(self, app):
        sm = app.soundManager
        self.mm = app.musicManager

        self.mm.setTempo(self.tempo)
        
        # grab our background tracks
##        app.music['bg-1'] = sm.createSound('bg-1', 'zile.wav', True)
##        app.music['bg-2'] = sm.createSound('bg-2', 'pyke.wav', True)
##        app.music['bg-3'] = sm.createSound('bg-3', 'stye.wav', True)
##        app.music['bg-4'] = sm.createSound('bg-4', 'zile.wav', True)
##        app.music['bg-5'] = sm.createSound('bg-5', 'pyke.wav', True)
##        app.music['bg-6'] = sm.createSound('bg-6', 'stye.wav', True)
##


        app.music['bg-1'] = sm.createSound('bg-1', 'level-0-1.wav', True)
        app.music['bg-2'] = sm.createSound('bg-2', 'level-0-2.wav', True)
        app.music['bg-3'] = sm.createSound('bg-3', 'level-0-3.wav', True)
        app.music['bg-4'] = sm.createSound('bg-4', 'level-0-4.wav', True)
        app.music['bg-5'] = sm.createSound('bg-5', 'level-0-5.wav', True)
        app.music['bg-6'] = sm.createSound('bg-6', 'level-0-6.wav', True)

        self.defaultBackgroundMusic = app.music['bg-1']

        # set all music tracks relative to the listener
        for m in app.music.values():
            m.setRelativeToListener(True)
            #m.setGain(0.25)

        # grab all of our sound effects
##        files = {'key-0' : 'zinn.wav',
##                 'key-1' : 'tax2.wav',
##                 'key-2' : 'rocket.wav',
##                 'key-3' : 'imperial.wav',
##                 'tone-0' : 'good2.wav',
##                 'tone-1' : 'good3.wav',
##                 'tone-2' : 'advert.wav',
##                 'tone-3' : 'asian.wav',
##                 'tone-4' : 'asian2.wav',
##                 'tone-5' : 'bad.wav',
##                 'tone-6' : 'baddeal.wav',
##                 'tone-7' : 'bank2.wav',
##                 'perc-0' : 'bank.wav',
##                 'perc-1' : 'crew.wav',
##                 'perc-2' : 'engine.wav',
##                 'perc-3' : 'fuel.wav',
##                 'perc-4' : 'help.wav',
##                 'perc-5' : 'insure.wav',
##                 'bell-0' : 'lavamind.wav',
##                 'bell-1' : 'loan.wav',
##                 'bell-2' : 'loro.wav',
##                 'bell-3' : 'mech.wav',
##                 'bell-4' : 'zinn.wav',
##                 'bell-5' : 'tax.wav'
##                 }
        # grab all of our sound effects
        files = {'key-0' : 'key-0.wav',
                 'key-1' : 'key-1.wav',
                 'key-2' : 'key-2.wav',
                 'key-3' : 'key-3.wav',
                 'tone-0' : 'wurl-0.wav',
                 'tone-1' : 'wurl-1.wav',
                 'tone-2' : 'wurl-2.wav',
                 'tone-3' : 'wurl-3.wav',
                 'tone-4' : 'bowen-0.wav',
                 'tone-5' : 'bowen-1.wav',
                 'tone-6' : 'bowen-2.wav',
                 'tone-7' : 'bowen-3.wav',
                 'perc-0' : 'tabla-0.wav',
                 'perc-1' : 'tabla-1.wav',
                 'perc-2' : 'tabla-2.wav',
                 'perc-3' : 'tabla-3.wav',
                 'perc-4' : 'tabla-4.wav',
                 'perc-5' : 'tabla-5.wav',
                 'bell-0' : 'bell-hi-0.wav',
                 'bell-1' : 'bell-hi-1.wav',
                 'bell-2' : 'bell-lo-0.wav',
                 'bell-3' : 'bell-lo-1.wav',
                 'bell-4' : 'neutron-0.wav',
                 'bell-5' : 'neutron-1.wav'
                 }

        for f in sorted(files):
            print 'Loading sound %s from file %s' % (f, files[f])
            app.sounds[f] = sm.createSound(f, files[f], False)        

            
        # set all sounds relative to the listener
        for s in app.sounds.values():
            s.setRelativeToListener(True)


    def setCurrentLevel(self, level):
        '''
        Set our current level
        '''
        print particles
        if level == self.currentLevel:
            print 'Error: entering current level'
            return

        if level < 0:
            print 'Error: negative level', level
            return
        if level >= len(self.levels):
            print 'Error: level id too big', level
            return
             
        # warp the character if we're just starting
        if self.currentLevel == -1:
            self.player.warpTo = (self.levels[level].playerStart)
        
        print 'Entering level %s (%d)' % (self.levels[level].name, level)
        ogre.OverlayManager.getSingleton().getOverlayElement("CurrentLevel/Level").setCaption(self.levels[level].name)
        ogre.OverlayManager.getSingleton().getByName("AreaClearOverlay").hide()
        if ("StartArrow" in particles):
            self.decayParticle = True
            self.particles["StartArrow"] = particles["StartArrow"]
            self.particleTimeout = 4
            del particles["StartArrow"]

        # set the appropriate background music
        if self.currentLevel > 0 and self.levels[self.currentLevel].backgroundMusic:
            self.mm.stopSound(self.levels[self.currentLevel].backgroundMusic, 0)
        else:
            self.mm.stopSound(self.defaultBackgroundMusic, 0)
        oldlevel = self.currentLevel
        self.currentLevel = level

        if self.levels[self.currentLevel].backgroundMusic:
            self.mm.addQueuedSound(self.levels[self.currentLevel].backgroundMusic, self.mm.totalBeats)
        else:
            self.mm.addQueuedSound(self.defaultBackgroundMusic, self.mm.totalBeats)
        
        #trigger any animation
        if (self.levels[oldlevel].stopLevelCallback):
                self.levels[oldlevel].stopLevelCallback(self.levels[oldlevel])
        if (self.levels[self.currentLevel].startLevelCallback):
                self.levels[self.currentLevel].startLevelCallback(self.levels[self.currentLevel])
        
        # move the camera
        if oldlevel != -1: # Don't animate the camera to start
            
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
            #Move from the current anchor to the next one
            key.setTranslate(node.getPosition() + (self.levels[self.currentLevel].cameraAnchor-self.levels[oldlevel].cameraAnchor))
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

                return col1

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
                self.particleSystemCleanup("StartArrow")
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
 
    def fireworks(self, level):
        if (not self.particles.has_key("Fireworks")):
            scn = self.rootNode.getCreator()
            c = Container("Fireworks")
            c.particleSystem = scn.createParticleSystem('fireworks', 'Examples/njrFireworks')
            c.particleSystem.setKeepParticlesInLocalSpace(True)
        
            c.node = self.rootNode.createChildSceneNode("Fireworks")
            #c.node.setPosition(0, 0, 375)
            c.node.setPosition(level.cameraAnchor - ogre.Vector3(0,0,25))
        
            c.node.attachObject(c.particleSystem)
        
            self.particles["Fireworks"] = c
            
            #overlay = ogre.OverlayManager.getSingleton().getByName('CongratsOverlay')
            #overlay.show()
            
    def snow(self, level):
        if (not self.particles.has_key("Snow")):
            scn = self.rootNode.getCreator()
            c = Container("Snow")
            c.particleSystem = scn.createParticleSystem('snow', 'Snow')
            c.particleSystem.setKeepParticlesInLocalSpace(True)
            
            c.node = self.rootNode.createChildSceneNode("Snow")
            #c.node = self.player.node.createChildSceneNode("Snow")  #for extra kicks, attach to the player
            #c.node.setPosition(0, 0, 375)
            print "Snow: ", level.cameraAnchor.x, level.cameraAnchor.y, level.cameraAnchor.z
            c.node.setPosition(level.cameraAnchor + ogre.Vector3(0,0,25))
            
            c.node.attachObject(c.particleSystem)
            
            self.particles["Snow"] = c
            
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
        
    def particleSystemCleanup(self, name):
        #self.particles["StartArrow"].particleSystem.removeAllEmitters()
        if (name in self.particles):
            scn = self.rootNode.getCreator()
            c = self.particles[name]
            scn.destroyParticleSystem(c.particleSystem)
            del c.particleSystem
            scn.destroySceneNode(c.node.getName())
            del self.particles[name]
        

    def resetPlayer(self):
        self.player.warpTo = self.levels[self.currentLevel].playerStart

