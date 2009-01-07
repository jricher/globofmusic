#!/usr/bin/python

##
## Glob of Music
## Copyright 2007
##  Justin Richer
##  Nathan Rackliffe
##  Paul Laidler
##  Rob Whalen
##


#
# Main executable file for A Glob of Music
#

import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS
import SampleFramework as sf
import os
import math
from MusicManager import MusicManager
from Container import *

from threading import Thread
import time

# don't think we need this one, seriously
# import PythonOgreConfig

WINDOWS = (os.name == 'nt')
JOYDEBUG = False  #set to True to see the raw joystick values
WIIMOTE = False
SWEET_LIGHTS = False  #this really slows things down, so use with caution
#Xbox mapping (requires xboxmapping.xgi)
BUTTON_MAP = { 0:"A", 1:"B", 2:"X", 3:"Y", 4:"Black", 5:"White", 6:"Start", 7:"Back" , 8:"LeftStick", 9:"RightStick", 10:"Left", 11:"Right", 23:"D_Down", 22:"D_Right", 21:"D_Left", 20:"D_Up"}

PHYSICAL_WIIMOTE_BUTTON_MAP = { 0:"A", 1:"B", 2:"C", 3:"Z", 4:"Minus", 5:"Plus", 6:"Home", 7:"1", 8:"2", 9:"D_Up", 10:"D_Down", 11:"D_Left", 12:"D_Right"}
#Modify this one to change the key bindings to what you want.
WIIMOTE_BUTTON_MAP = { 0:"A", 1:"A", 2:"X", 3:"Y", 4:"White", 5:"Black", 6:"Start", 7:"1", 8:"2", 9:"D_Up", 10:"D_Down", 11:"D_Left", 12:"D_Right"}
#I'm guessing on these linux mappings
LINUX_BUTTON_MAP = { 5:"A", 4:"B", 3:"X", 2:"Y", 1:"Black", 0:"White", 6:"Start", 7:"Back", 8:"Left", 9:"Right" }


##
## A few magical constants from the demos
##

STEP_RATE=0.01
ANY_QUERY_MASK                  = 1<<0

# Custom parameter bindings
CUSTOM_SHININESS = 1
CUSTOM_DIFFUSE = 2
CUSTOM_SPECULAR = 3


##

class GomFrameListener(sf.FrameListener, OgreOde.StepListener, object):
    def __init__(self, app, renderWindow, camera):
        sf.FrameListener.__init__(self, renderWindow, camera)
        OgreOde.StepListener.__init__(self)
        
        # copy references to the pieces we care about
        self.level = app.level
        self.player = app.player
        self.scn = app.sceneManager
        self.musicManager = app.musicManager
        self.overlay = app.overlay
        self.overlayCountdown = 8

        self.lights = app.lights
        
        app._stepper.setStepListener(self)
        
        self._world = app._world

        self.xAxis = 0
        self.yAxis = 0
        self.zAxis = 0
        self.xcAxis = 0
        self.ycAxis = 0
        self.zcAxis = 0
        self.fov = 5

        self.buttons = set()
        
        self.altitude = 50
        self.azimuth = 200

    def __del__(self):
        del self.level
        del self.player
        del self._world
        del self.scn
        del self.musicManager
        del self.overlay
        del self.altitude
        del self.azimuth
        del self.lights[:]
        sf.FrameListener.__del__(self)
        print 'FrameListener unloaded'
    
    def frameStarted(self, frameEvent):
        if self.overlay:
            if self.overlayCountdown > 0:
                self.overlayCountdown -= frameEvent.timeSinceLastFrame
                if self.overlayCountdown < 5:
                    self.overlay.hide()
                    self.overlay = None
                    #self.overlay = ogre.OverlayManager.getSingleton().getByName('NameCardOverlay')
                    #self.overlay.show()
            else:
                self.overlay.hide()
                self.overlay = None
            
        # Calculate the camera position
        if (self.scn.hasAnimation("CameraTrack")):
            # Don't allow changing the camera during animations
            self.xcAxis = self.ycAxis = self.zcAxis = 0.0
            
        if (self.xcAxis or self.ycAxis or self.zcAxis):
            self.azimuth = self.azimuth - self.xcAxis
            self.altitude = self.altitude - self.ycAxis
            # set zoom
            self.fov = self.fov - self.zcAxis/10.0
            if self.altitude > 85: self.altitude = 85
            if self.altitude < 20: self.altitude = 20
            if self.azimuth > 360: self.azimuth = self.azimuth - 360
            if self.azimuth < 0: self.azimuth = self.azimuth + 360
            if self.fov < 2: self.fov = 2
            if self.fov > 60: self.fov = 60
            self.camera.setFOVy(ogre.Radian(ogre.Degree(self.fov)))
        
            p_0 = self.level.cameraPositions[self.level.area]
            #p_0 = ogre.Vector3.ZERO
            
            radius = 300.0
            p_1 = ogre.Vector3(p_0.x + radius* math.cos(math.radians(self.azimuth)) * math.sin(math.radians(self.altitude)),
                               p_0.y + radius * math.cos(math.radians(self.altitude)),
                               p_0.z + radius* math.sin(math.radians(self.azimuth)) * math.sin(math.radians(self.altitude)))
        
            #print p_0
            #print p_1
            #print "self.azimuth [%d]" % self.azimuth
            #print "self.altitude [%d]" % self.altitude
            
            #self.camera.moveRelative(ogre.Vector3(self.xcAxis, -self.ycAxis,0.0))
            node = self.camera.getParentSceneNode()
            node.setPosition(p_1)
            

        ## animate the lights
        if SWEET_LIGHTS:
            ## yeah, this is a weird hack with way too many constants...
            b = self.musicManager.currentBeat % 16
    
            lightPositions = [ogre.Vector3(50,50,50), ogre.Vector3(50,50,-50), ogre.Vector3(-50,50,-50), ogre.Vector3(-50,50,50)]
            lightColors = [ogre.ColourValue(1.0, 0.0, 0.0), ogre.ColourValue(0,0,1), ogre.ColourValue(1,1,0),ogre.ColourValue(1.0,0,1.0)]
            for i in range(len(self.lights)):
                l = self.lights[i]
                color = l.getDiffuseColour()
                color.r *= 0.95
                color.g *= 0.95
                color.b *= 0.95
                l.setDiffuseColour(color)
                l.setSpecularColour(color)
                p = self.level.cameraPositions[self.level.area] + lightPositions[i]
                p2 = ogre.Vector3(p.x, p.y, p.z)
                l.setPosition(p2)
                l.setDirection(self.player.node.getPosition()- p2)
            
            #Boost the beat light
            l = self.lights[b/4]
            l.setDiffuseColour(lightColors[b/4])
            l.setSpecularColour(lightColors[b/4])
        
        result = sf.FrameListener.frameStarted(self,frameEvent)
        
        while self.musicManager.fireKeys:
            key = self.musicManager.fireKeys.pop(0)
            if key in containers:
                c = containers[key]
                if isinstance(c, Platform):
                    if len(c.sounds) < 1:
                        c.fire()
                    else:
                        #Now we can play more than one sound from a platform
                        c.sound = c.sounds.pop(0)
                        self.musicManager.addQueuedSound(c.sound, c.quant, c.rest, c.id)

        while self.musicManager.finishKeys:
            key = self.musicManager.finishKeys.pop(0)
            if key in containers:
                c = containers[key]
                if isinstance(c, Platform):
                    c.done()
                    
        self.level.animate(frameEvent)

        return result

    def frameEnded(self, frameEvent):
        result = sf.FrameListener.frameEnded(self,frameEvent)

        # give some time for the audio processing thread
        time.sleep(0.001)
        
        return result
     

        
    def windowClosed(self, rw):
        # need to override this so that the system gets properly cleaned up
        if( rw == self.renderWindow ):
            if( self.InputManager ):
                print 'Window closing'
                self.InputManager.destroyInputObjectKeyboard( self.Keyboard )
                # destroying the mouse is broken somehow
                #self.InputManager.destroyInputObjectMouse( self.Mouse )
                if self.Joy:
                    self.InputManager.destroyInputObjectJoyStick( self.Joy )
                OIS.InputManager.destroyInputSystem(self.InputManager)
                self.InputManager = None
                print 'Window closed'

    def _processUnbufferedKeyInput(self, frameEvent):

        #sf.FrameListener._processUnbufferedKeyInput(self, frameEvent)

        # force area selection
        # These don't make any sense any more
        #if self.Keyboard.isKeyDown(OIS.KC_1):
        #    self.level.setArea(1)
        #elif self.Keyboard.isKeyDown(OIS.KC_2):
        #    self.level.setArea(2)
        #elif self.Keyboard.isKeyDown(OIS.KC_3):
        #    self.level.setArea(3)
        #elif self.Keyboard.isKeyDown(OIS.KC_4):
        #    self.level.setArea(4)

        #if self._isToggleKeyDown(OIS.KC_E):
        #    self.level.triggerRandomSounds()

        # quit command
        if self.Keyboard.isKeyDown(OIS.KC_ESCAPE) or self.Keyboard.isKeyDown(OIS.KC_Q):
            print 'Quitting'
            return False

        self.xAxis = self.yAxis = 0
        self.zAxis = self.zcAxis = 0
        self.xcAxis = self.ycAxis = 0

        self.buttons.clear()
        
        #print self.level.camera.getRealPosition()
        
        # Joystick processing
        #print self.InputManager.numJoySticks()
        if (self.Joy) :
            joyState = self.Joy.getJoyStickState()
            if (JOYDEBUG) :
                print 'joyState.buttons', joyState.buttons
                print 'self.Joy.buttons', self.Joy.buttons()
                for button in range(self.Joy.buttons()) :
                    if joyState.buttonDown(button):
                        print 'Button %d down' % button
                for axis in range(self.Joy.axes()):
                    print 'Axis %d: ' % axis,
                    print joyState.mAxes[axis].abs
            #Xbox bindings
            

            # check the axes
            if (WINDOWS):
                if (WIIMOTE):
                    self.xAxis = joyState.mAxes[3].abs / 32768.0
                    self.yAxis = joyState.mAxes[4].abs / 32768.0
                    #self.xcAxis = -joyState.mAxes[0].abs / (32768.0*4)
                    #self.ycAxis = joyState.mAxes[2].abs / (32768.0*4)
                    #self.zcAxis = joyState.mAxes[1].abs / 32768.0
                    # We need a larger dead zone for the nunchuck
                    if (self.xAxis > -0.2 and self.xAxis < 0.2): self.xAxis = 0
                    if (self.yAxis > -0.2 and self.yAxis < 0.2): self.yAxis = 0
                    if (self.zAxis > -0.2 and self.zAxis < 0.2): self.zAxis = 0
                    
                    #Large dead zone for the Accelerometers too
                    if (self.xcAxis > -0.2 and self.xcAxis < 0.2): self.xcAxis = 0
                    if (self.ycAxis > -0.2 and self.ycAxis < 0.2): self.ycAxis = 0
                    
                    for button in range(self.Joy.buttons()) :
                        if joyState.buttonDown(button):
                            self.buttons.add(WIIMOTE_BUTTON_MAP[button])

                    
                else: #Xbox Controller
                    self.xAxis = joyState.mAxes[3].abs / 32768.0
                    self.yAxis = joyState.mAxes[2].abs / 32768.0
                    self.xcAxis = joyState.mAxes[1].abs / 32768.0
                    self.ycAxis = -joyState.mAxes[0].abs / 32768.0
                    if (self.xAxis > -0.1 and self.xAxis < 0.1): self.xAxis = 0
                    if (self.yAxis > -0.1 and self.yAxis < 0.1): self.yAxis = 0
                    if (self.zAxis > -0.1 and self.zAxis < 0.1): self.zAxis = 0
                    if (self.xcAxis > -0.1 and self.xcAxis < 0.1): self.xcAxis = 0
                    if (self.ycAxis > -0.1 and self.ycAxis < 0.1): self.ycAxis = 0
                    for button in range(self.Joy.buttons()) :
                        if joyState.buttonDown(button):
                            self.buttons.add(BUTTON_MAP[button])
                            
            else : #Linux mappings
                self.xAxis = joyState.mAxes[0].abs / 32768.0
                self.yAxis = joyState.mAxes[1].abs / 32768.0
                self.zAxis = joyState.mAxes[2].abs / 32768.0
                self.xcAxis = joyState.mAxes[3].abs / 32768.0
                self.ycAxis = joyState.mAxes[4].abs / 32768.0
                self.zcAxis = joyState.mAxes[5].abs / 32768.0
                if (self.xAxis > -0.2 and self.xAxis < 0.2): self.xAxis = 0
                if (self.yAxis > -0.2 and self.yAxis < 0.2): self.yAxis = 0
                if (self.zAxis > -0.2 and self.zAxis < 0.2): self.zAxis = 0
                if (self.xcAxis > -0.2 and self.xcAxis < 0.2): self.xcAxis = 0
                if (self.ycAxis > -0.2 and self.ycAxis < 0.2): self.ycAxis = 0
                for button in range(self.Joy.buttons()) :
                    if joyState.buttonDown(button):
                        self.buttons.add(LINUX_BUTTON_MAP[button])
        
        if (JOYDEBUG): print self.buttons

        #End Joystick processing


        # keyboard movement shortcuts
        if self.Keyboard.isKeyDown(OIS.KC_W) : self.yAxis = -1
        if self.Keyboard.isKeyDown(OIS.KC_A) : self.xAxis = -1
        if self.Keyboard.isKeyDown(OIS.KC_S) : self.yAxis = 1
        if self.Keyboard.isKeyDown(OIS.KC_D) : self.xAxis = 1
        
        #keyboard camera controls
        
        if self.Keyboard.isKeyDown(OIS.KC_I) :  self.buttons.add("D_Up")
        if self.Keyboard.isKeyDown(OIS.KC_J) :  self.buttons.add("D_Left")
        if self.Keyboard.isKeyDown(OIS.KC_K) :  self.buttons.add("D_Down")
        if self.Keyboard.isKeyDown(OIS.KC_L) :  self.buttons.add("D_Right")
        if self.Keyboard.isKeyDown(OIS.KC_MINUS) : self.zcAxis = -1
        if self.Keyboard.isKeyDown(OIS.KC_EQUALS): self.zcAxis = 1
        
        
        if self.Keyboard.isKeyDown(OIS.KC_SPACE) : self.buttons.add("A") # button 5 == 'A' on Xbox
        if self.Keyboard.isKeyDown(OIS.KC_V) : self.buttons.add("X")
        if self.Keyboard.isKeyDown(OIS.KC_C) : self.buttons.add("Y")
        
        if self.Keyboard.isKeyDown(OIS.KC_R) : self.buttons.add("Back")
        
        if self.Keyboard.isKeyDown(OIS.KC_N) : self.player.powerups.append("gravity")  #For cheaters
        if self.Keyboard.isKeyDown(OIS.KC_M) : 
            if self.level.lastKey:
                for d in self.level.lastKey.doors:
                    d.unlock()
        
        return True
        
    def preStep(self, time):
        self.addForcesAndTorques(time)
        
        return True
        
    def addForcesAndTorques(self, time):

        # the player should always be awake, i think...
        self.player.body.wake()
            
        if self.player.jumpTime > time:
            self.player.jumpTime -= time
        else:
            self.player.jumpTime = 0

        #print self.player.jumpTime
        
        # shortcut out if we have a point to warp to
        if self.player.warpTo:
            self.player.body.setPosition(self.player.warpTo)
            self.player.body.setAngularVelocity(ogre.Vector3().ZERO)
            self.player.body.setLinearVelocity(ogre.Vector3().ZERO)
            
            self.player.warpTo = None
            return
        
        #print curAngVelocity
        #print self.player.body.getPosition()
        #print self.player.body.isEnabled()
        
        #slow down if the user isn't moving the joystick
        #self.playerBody.setAngularVelocity(ogre.Vector3(curAngVelocity[0], curAngVelocity[1], curAngVelocity[2]))
        curAngVelocity = self.player.body.getAngularVelocity()
        curLinear = self.player.body.getLinearVelocity()

        if not (self.xAxis or self.yAxis or self.zAxis):
            if curAngVelocity.squaredLength() > 0.05:
                self.player.body.setAngularVelocity(curAngVelocity * 0.75)
            else:
                self.player.body.setAngularVelocity(ogre.Vector3().ZERO)
            #if curLinear.squaredLength() > 0.05:
            #    self.player.body.setLinearVelocity(curLinear * 0.75)
            #else:
            #    self.player.body.setLinearVelocity(ogre.Vector3.ZERO)
                
        else:

            # slow down a little even if we're pushing the joystick
            # this makes turns a bit snappier
            self.player.body.setAngularVelocity(curAngVelocity * 0.95)
            #self.player.body.setLinearVelocity(curLinear * 0.95)
            
            #print self.playerBody.getTorque()
            #print self.xAxis, ",", self.yAxis
        
                
            #map controller axis to camera relative controls
            ##i'm probably overdoing the normalization a little bit here, just making sure we get the right values

            #controllerDirection = ogre.Vector3(self.xAxis, 0, self.yAxis);
            #controllerDirection.normalise();
                
            forward = ogre.Vector3(self.camera.getDirection().x, 0, self.camera.getDirection().z); 
            #forward.normalise();
            
            right = ogre.Vector3(self.camera.getRight().x, 0, self.camera.getRight().z); 
            #right.normalise();
            
            up = ogre.Vector3(self.camera.getUp().x, 0, self.camera.getUp().z); 
            #up.normalise();
            
            forward=(forward+up)*self.xAxis;
            right=right*self.yAxis;
            
            #forward.normalise();
            #right.normalise();
            
            direction = forward+right;
            direction.normalise();
            
            #self.player.body.addTorque(forward);
            #Add torque from the joystick input
            #print "direction"
            #print direction;

            # cut off the accelleration if we're going fast enough
            # TODO: this should really be a scale function
            #print (curAngVelocity + direction).squaredLength()
            if (curAngVelocity + direction).squaredLength() < (50 * 50):
                self.player.body.addTorque(650*direction)
                
            #Slight Air control (added even when on the ground, but insignificant in comparison to the movement the torque generates)

            ldir = ogre.Vector3(-direction.z, 0, direction.x)
            #print 'jump + ldir:', (ldir + self.player.jumpVector).squaredLength()
            #if self.player.jumpVector and self.player.jumpTime > 0 and (ldir + self.player.jumpVector).squaredLength() < 1: # keep from holding onto the wall
            #print (ldir.x + self.player.jumpVector.x)
            #print (ldir.z + self.player.jumpVector.z)
            if self.player.jumpVector and self.player.jumpTime > 0 and math.fabs((ldir.x + self.player.jumpVector.x) < 0.5 or math.fabs(ldir.z + self.player.jumpVector.z) < 0.5):
                #ldir = ldir + (self.player.jumpVector)
                #print ldir.squaredLength()
                #pass
                #print '*' * 10, 'wall-holding cut'
                ldir = (ldir + self.player.jumpVector) / 2
                #ldir.y = -(ldir.y + 5)
                if math.fabs(ldir.y) < 0.10:
                    ldir.y = -5
                
            #print 'cur + ldir:', (curLinear + ldir).squaredLength()
            if (curLinear + ldir).squaredLength() < (25 * 25):
                    
                #curLinear = self.player.body.getLinearVelocity()
                #keep the current velocity, and add a little influence from the controller 
                #self.player.body.setLinearVelocity(curLinear + (ldir/4))
                self.player.body.addForce(ldir * 300)
                
        if self.buttons:

            if "A" in self.buttons and self.player.jumpVector and self.player.jumpTime > 0.0:
                #jv = self.player.jumpVector * 2 + ogre.Vector3.UNIT_Y * 10 * self.player.jumpVector.y
                #jv = ogre.Vector3(self.player.jumpVector.x, self.player.jumpVector.y * 100, self.player.jumpVector.z)
                jv = ogre.Vector3(self.player.jumpVector.x, (self.player.jumpVector.y + 1) * 100, self.player.jumpVector.z)

                jv.normalise()
            
                # Jump
                # project the current linear velocity along our jump vector
                proj = curLinear.dotProduct(jv) * jv

                #print proj.squaredLength()

            
                if (proj + jv).squaredLength() < (22 * 22):
                    #self.player.body.addForce((self.player.jumpVector + (ogre.Vector3.UNIT_Y * 0.25)) * 15000) # jumping has to be pretty powerful
                    self.player.body.setLinearVelocity(curLinear + jv * 10)
                    
            else:
                # cut out the jumping if we let go
                self.player.jumpTime = 0.0
            
            # Anti-gravity power
            # TODO: this needs some serious tweaking
            if 'gravity' in self.player.powerups and "X" in self.buttons and curLinear.y < 20:
                if self.player.body.getPosition().y < 45.0:
                    antigravity = self._world.getGravity() * -(20 - curLinear.y)
                    #print antigravity
                    self.player.body.addForce(antigravity)
                elif self.player.body.getPosition().y < 40.0:
                    antigravity = self._world.getGravity() * (40.0 - self.player.body.getPosition().y)
                    #print antigravity
                    self.player.body.addForce(antigravity)
                    
            # super-gravity power
            if 'gravity' in self.player.powerups and  "Y" in self.buttons and curLinear.y < 25:
                jupitergravity = self._world.getGravity()*10.0
                #print jupitergravity
                self.player.body.addForce(jupitergravity)
            
            # Camera Movement
            if "D_Up" in self.buttons: self.ycAxis = 1.0
            if "D_Down" in self.buttons: self.ycAxis = -1.0
            if "D_Left" in self.buttons: self.xcAxis = -1.0
            if "D_Right" in self.buttons: self.xcAxis = 1.0
            #self.camera.moveRelative(translate)
            
            #Domino Reset
            # NOTE: this is very Level0 specific, for debug purposes only
            if "Back" in self.buttons: self.level.resetDominoes()
            
            if "Start" in self.buttons:
                self.player.warpTo = self.level.playerStarts[self.level.area]
            if "Black" in self.buttons: self.zcAxis = 1
            if "White" in self.buttons: self.zcAxis = -1
            
        else:
            # special cleanup
            #self.player.jumpTime = 0.0
            pass
            
class GomApplication(sf.Application, object):
    def __init__(self):
        'Init render application'
        self.level = None
        self.player = None
        self.lights = []
        
        sf.Application.__init__(self)

    def __del__(self):
        # sound
        print 'sound--'
        self.soundManager.pauseAllSounds()
        self.soundManager.destroyAllSounds()
        del self.soundManager

        # game
        print 'game--'
        del self.level
        del self.player
        del self._plane
        del self.overlay
        del self.lights[:]

        # ODE
        print 'ode--'
        del self._stepper
        del self._space
        del self._world
        
        
        # music
        print 'music--'
        del self.musicManager
        del self._musicThread

        print 'pre-del'
        sf.Application.__del__(self)
        print 'Application Unloaded'

    def _createCamera(self):
        """Creates the camera."""        
        self.camera = self.sceneManager.createCamera('PlayerCam')

        node = self.sceneManager.getRootSceneNode().createChildSceneNode('PlayerCamNode')
        #This puts the camera at azimuth 200, altitude 50
        node.setPosition(-215.954, 192.836, -178.601)
        node.attachObject(self.camera)
        
        # zoom a little bit
        self.camera.setNearClipDistance(0.5)
        #print self.camera.getFOVy().valueDegrees()
        self.camera.setFOVy(ogre.Radian(ogre.Degree(5)))

    def _createScene(self):
        "Override sf create scene"
        global STEP_RATE, ANY_QUERY_MASK, STATIC_GEOMETRY_QUERY_MASK
        sceneManager = self.sceneManager

        # JR: HACK to turn off shadows on my laptop to make things run faster
        if WINDOWS:
            if SWEET_LIGHTS: sceneManager.setShadowTechnique(ogre.SHADOWTYPE_STENCIL_ADDITIVE)
            else: sceneManager.setShadowTechnique(ogre.SHADOWTYPE_STENCIL_MODULATIVE)
            #sceneManager.setShadowTechnique(ogre.SHADOWTYPE_TEXTURE_ADDITIVE)
            #sceneManager.setShadowTechnique(ogre.SHADOWTYPE_TEXTURE_MODULATIVE)
            

            #sceneManager.setShadowTextureSize(1024)
            sceneManager.setShadowFarDistance(500)
        
        ogre.MovableObject.setDefaultQueryFlags (ANY_QUERY_MASK)

        # create the sound system and managers
        self.soundManager = OgreAL.SoundManager()
        print 'Max Sources', self.soundManager.maxSources()
        self.musicManager = MusicManager()


        rootNode = sceneManager.getRootSceneNode()
        # start up ODE
        self.initializeOde()

        # Create the player object
        self.player = Player('Player')
        containers[self.player.id] = self.player
        self.player.ent = sceneManager.createEntity('Player', 'Glob.mesh')

        # playing with transparent material settings
        #sub = playerEnt.getSubEntity(0)
        #sub.materialName = 'Material.003'

        self.player.node = rootNode.createChildSceneNode('Player')
        self.player.node.attachObject(self.player.ent)

        self.player.node.setPosition(ogre.Vector3(0, 5, 0))

        # the OgreOde EntityInformer lets us connect ODE physics to OGRE geometry (i think)
        #
        ei = OgreOde.EntityInformer(self.player.ent, ogre.Matrix4.getScale(self.player.node.getScale()))
        self.player.body = ei.createSingleDynamicSphere(5.0, self._world, self._space)

        self.player.geom = self.player.body.getGeometry(0) # this is a guess??

        self.player.geom.setUserData(self.player.id)

        # create an invisible bottom floor 10 units down, completely flat
        self._plane = Container('Infinite Plane')
        containers[self._plane.id] = self._plane
        self._plane.geom = OgreOde.InfinitePlaneGeometry(ogre.Plane(ogre.Vector3(0, 1, 0), -10), self._world, self._space)
        self._plane.geom.setUserData(self._plane.id)

        # TODO: visualize the sucker?

        self.createLights()

        ###
        ### LOAD LEVELS
        ###

        import Level0

        import modulefinder
        import levels
        m = modulefinder.ModuleFinder()
        l = m.find_all_submodules(levels)
        ll = []
        for x in l:
            exec 'import ' + 'levels.' + x
            exec 'print x, dir(levels.' + x + ')'
            exec 'll.append(levels.' + x + ')'

        for x in ll:
            print x, type(x)
            print x.Level()

        self.level = Level0.load(self, l)

        self.level.setArea(0)

        ###
        ### 
        ### 

        # start music thread
        self._musicThread = MusicThread(self.musicManager)
        self._musicThread.setDaemon(True)
        self._musicThread.start()


        ## Position and orient the camera
        # TODO: this should depend on the player and be more dynamic
        #self.camera.setPosition(-50,25,0)
        #self.camera.lookAt(0,0,0)
        self.camera.setAutoTracking(True, self.player.node)

        # load up our titlecard
        self.overlay = None
        #self.overlay = ogre.OverlayManager.getSingleton().getByName('TitleCardOverlay')
        #self.overlay.show()


    def createLights(self):
        # Create the sun
        l = self.sceneManager.createLight('MainLight')

        #print '  >>', dir(l.getAnimableValueNames())
        #
        #for a in l.getAnimableValueNames():
        #    print "  **", a
        
        l.setType (ogre.Light.LT_POINT)
        #dirn = ogre.Vector3(0.5, -1, 0.5)
        #dirn.normalise()
        #l.setDirection(dirn)
        pos = ogre.Vector3(300, 900, -300)
        l.setPosition(pos)
        l.setDiffuseColour(ogre.ColourValue(0.8, 0.8, 0.8))
        l.setSpecularColour(ogre.ColourValue(1.0, 1.0, 1.0))
        
        #create a secondary dimmer light
        l = self.sceneManager.createLight('SecondLight')

        #print '  >>', dir(l.getAnimableValueNames())
        #
        #for a in l.getAnimableValueNames():
        #    print "  **", a
        
        l.setType (ogre.Light.LT_POINT)
        #dirn = ogre.Vector3(0.5, -1, 0.5)
        #dirn.normalise()
        #l.setDirection(dirn)
        pos = ogre.Vector3(300, 200, 300)
        l.setPosition(pos)
        l.setDiffuseColour(ogre.ColourValue(0.4, 0.4, 0.4))
        l.setSpecularColour(ogre.ColourValue(0.2, 0.2, 0.2))
        # effectively turn off shadows for this one
        l.setShadowFarDistance(0.01)

        if SWEET_LIGHTS:
            # Create pulsing lights
            dirn = ogre.Vector3(0.5, -0.75, 0.5)
            
            for i in range(4):
    
                dirn = ogre.Quaternion(ogre.Degree(120), ogre.Vector3().UNIT_Y) * dirn
                dirn.normalise()
                l = self.sceneManager.createLight('SpotLight%d' % i)
                l.setType (ogre.Light.LT_SPOTLIGHT)
                l.setDirection(dirn)
                l.setDiffuseColour(ogre.ColourValue(0.5, 0.5, 0.5))
                l.setSpecularColour(ogre.ColourValue(0.5, 0.5, 0.5))
                l.setSpotlightOuterAngle(ogre.Degree(10))
                self.lights.append(l)
        


    def initializeOde(self):
        # Copied and modified shamelessly from Demo_Scenes.py
        
        ## Create the ODE world
        self._world = OgreOde.World(self.sceneManager)
        #self._world.setGravity( (0,-9.80665,0) )
        self._world.setGravity( (0,-98.0665,0) ) # heavy gravity feels better somehow
        #self._world.setGravity( (0,-150.0,0) ) # heavy gravity feels better somehow
        self._world.setCFM(0.0000010 )  # 10e-5)
        self._world.setERP(0.8)
        self._world.setAutoSleep(True)
        self._world.setAutoSleepAverageSamplesCount(10)
        self._world.setContactCorrectionVelocity(1.0)
        self._space = self._world.getDefaultSpace()

        ## TODO: figure out what these constants mean
        ## Create something that will step the physics world
        _stepper_mode_choice = 2
        _stepper_choice = 3
        time_scale = 1.0  ## TODO: this is what slows everything down!!!!
        max_frame_time = 1.0 / 4.0
        frame_rate = 1.0 / 60.0

        if _stepper_mode_choice ==0:    stepModeType = OgreOde.StepHandler.BasicStep
        elif _stepper_mode_choice ==1:  stepModeType = OgreOde.StepHandler.FastStep
        elif _stepper_mode_choice ==2:  stepModeType = OgreOde.StepHandler.QuickStep
        else: stepModeType = OgreOde.StepHandler.QuickStep

        if _stepper_choice == 0:
            self._stepper = OgreOde.StepHandler(self._world, StepHandler.QuickStep, 
                STEP_RATE, max_frame_time,  time_scale)
        elif _stepper_choice == 1:
           self._stepper =  OgreOde.ExactVariableStepHandler(self._world, 
                stepModeType, 
                STEP_RATE,
                max_frame_time,
                time_scale)
        
        elif _stepper_choice == 2:
            self._stepper = OgreOde.ForwardFixedStepHandler(self._world, 
                stepModeType, 
                STEP_RATE,
                max_frame_time,
                time_scale)
        else:
            self._stepper = OgreOde.ForwardFixedInterpolatedStepHandler (self._world, 
                stepModeType, 
                STEP_RATE,
                frame_rate,
                max_frame_time,
                time_scale)
 
        
        self._stepper.setAutomatic(OgreOde.StepHandler.AutoMode_PostFrame, self.root)

    def _createFrameListener(self):
        # "create FrameListener"
        self.frameListener = GomFrameListener(self, self.renderWindow, self.camera)
        self.frameListener.showDebugOverlay(False)

        self.root.addFrameListener(self.frameListener)

    def _isPsycoEnabled(self):
        # return False
        return True

    def _configure(self):
        """This shows the config dialog and creates the renderWindow."""
        carryOn = self.root.showConfigDialog()
        if carryOn:
            self.renderWindow = self.root.initialise(True, "Glob of Music")
        return carryOn


class MusicThread(Thread, object):
    def __init__(self, mm):
        Thread.__init__(self)
        self.mm = mm
        
    def run(self):

        t = None
        d = None
        try:
            while True:
                if t:
                    s = time.time()
                    d = s - t
                    t = s
                else:
                    t = time.time()
                    d = 0
                    
                self.mm.advance(d)

                time.sleep(0.0001)
        except Exception, e:
            print 'Exception in music thread', e

        self.mm.clearQueue()
        self.mm.clearLoop()
        return False

        

if __name__ == '__main__':

    # try to use the fast code here
    #try:
    #    import psyco
    #    psyco.log()
    #    psyco.profile()
    #    psyco.full()
    #except ImportError:
    #    pass

    try:
        application = GomApplication()
        
        application.go()

        #import cProfile
        #cProfile.run('application.go()', 'profile.out')
        
    except ogre.OgreException, e:
        print e


