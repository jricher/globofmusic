##
## Glob of Music
## Copyright 2007
##  Justin Richer
##  Nathan Rackliffe
##  Paul Laidler
##  Rob Whalen
##

#
# Level 0 of the Glob of Music game
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

def load(app):
    return Level0(app)

class Level0(OgreOde.CollisionListener, object):
    def __init__(self, app):
        OgreOde.CollisionListener.__init__(self)

        self.tempo = 90
        self._world = app._world
        self._world.setCollisionListener(self)
        self._space = app._space
        self.camera = app.camera
        self.player = app.player
        self._plane = app._plane
        self.rootNode = app.sceneManager.getRootSceneNode()
        
        self.dominoes = []
        self.mazeBits = []
        self.stairs = []
        self.dominoResetPlatform = None
        self.dominoOffset = 0
        self.lastKey = None

        self.doorSounds = []
        
        self.ramps = []

        self.cameraPositions = []
        self.playerStarts = []

        self.overlay = None
        self.overlayTimeout = None
        
        # this is uninitialized
        self.area = -1

        # list of animations to play
        self.animations = []
        
        self.particles = {}
        self.particleTimeout = None
        self.decayParticle = False

        self.initSounds(app)

        self.initGraphics(app)

        
    def __del__(self):
        if (self._world.getCollisionListener() == self): 
            self._world.setCollisionListener(None)
        del self.camera
        del self._world
        del self._space
        del self.mm
        del self.music
        del self.sounds
        del self.area
        del self.player
        del self._plane
        if self.particles: self.particleSystemCleanup()
        containers.clear()
        del self.dominoes [:]
        del self.stairs[:]
        del self.dominoResetPlatform
        del self.dominoOffset
        if self.lastKey: del self.lastKey
        del self.animations[:]
        if self.overlay:
            del self.overlay
        del self.doorSounds[:]
        del self.ramps[:]
        del self.mazeBits[:]
        del self.rootNode

        
    def initGraphics(self, app):

        scn = app.sceneManager

        scn.setAmbientLight (ogre.ColourValue(0.2, 0.2, 0.2))
        
        # give us a skybox
        scn.setSkyBox(True, 'RedSkyBox')
        
        # Set out our four sub-areas
        # each area is 100x100 units
        # add two rooms to either end

        # start room
            
        c = Arena('StartRoom', 0)
        containers[c.id] = c
        c.ent = scn.createEntity('StartRoom', 'ArenaEnd.mesh')
        c.node = self.rootNode.createChildSceneNode('StartRoom')
        c.node.setPosition(ogre.Vector3(0, 0, -75.01))
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(180), ogre.Vector3().UNIT_Y))
        c.node.attachObject(c.ent)
        c.ent.setCastShadows(False)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)

        c.geom.setUserData(c.id)


        # end room
        
        c = Arena('EndRoom', 5)
        containers[c.id] = c
        c.ent = scn.createEntity('EndRoom', 'ArenaEnd.mesh')
        c.node = self.rootNode.createChildSceneNode('EndRoom')
        c.node.setPosition(ogre.Vector3(0, 0, 375.01))
        c.node.attachObject(c.ent)
        c.ent.setCastShadows(False)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)

        c.geom.setUserData(c.id)

        
        # store up calculated positions while we're at it
        for i in range(0, 6):
            #self.cameraPositions.append(ogre.Vector3(10, 35, -60 + 100 * i)) # front view
            #self.cameraPositions.append(ogre.Vector3(-100, 35, 0 + 100 * i))  # side view
            #self.cameraPositions.append(ogre.Vector3(-55, 45, -100 + 100 * i))  # side view
            self.cameraPositions.append(ogre.Vector3(0, 0, -100 + 100 * i))  # Anchor point


            # JR: CHANGE THIS
            #self.cameraPositions.append(ogre.Vector3(10, 10, 70 + 100 * i)) # front view

            if i > 0 and i < 5:
                self.playerStarts.append(ogre.Vector3(0, 4, -145 + 100 * i))

                # set up the arena floors
                c = Arena('arena%d' % (i - 1), i)
                containers[c.id] = c
                c.ent = scn.createEntity('arena%d' % (i - 1), 'Arena.mesh')
                c.node = self.rootNode.createChildSceneNode('arena%d' % (i - 1))
                c.node.setPosition(ogre.Vector3(0, 0, -100 + i * 100))
                c.node.attachObject(c.ent)

                c.ent.setCastShadows(False)
                
                # set the floor color properly
                sub = c.ent.getSubEntity(0)
                sub.materialName = 'Floor%d' % (i - 1)
                
                # copied from SimpleScenes_TriMesh, there's probably a much more efficient way to do this
                ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
                c.geom = ei.createStaticTriangleMesh(self._world, self._space)
                c.ent.setUserObject(c.geom)
                
                c.geom.setUserData(c.id)
            elif i == 0:
                # first room
                self.playerStarts.append(ogre.Vector3(0, 4, -75 + 100 * i))
            elif i == 5:
                # final room
                self.playerStarts.append(ogre.Vector3(0, 4, -125 + 100 * i))

        #Starting room Arrow hint
        self.startingArrow(-95)
        
        #Starting Room platform
        key = MultiKey()
        c = Platform(materialName = 'platform0-')
        containers[c.id] = c
        c.ent = scn.createEntity('tilt_plat0', 'platform.mesh')
        c.node = self.rootNode.createChildSceneNode('tilt_platform0')
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)

        c.body = OgreOde.Body(self._world, 'OgreOde::Body_' + c.node.getName())
        c.node.attachObject(c.body)
        mass = OgreOde.BoxMass (20.0, ei.getSize())
        mass.setDensity(5.0, ei.getSize())
        c.body.setMass(mass)
        
        c.geom.setBody(c.body)
        c.ent.setUserObject(c.geom)
        
        c.body.setPosition(ogre.Vector3(0, 2, -85))

        c.joint = OgreOde.BallJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAnchor(ogre.Vector3(0, 2, -85))

        c.sound = self.sounds['key-1']
        #c.sound = random.choice(self.sounds.values())
        c.quant = 8

        # set the initial material
        c.setMaterial()

        c.geom.setUserData(c.id)

        c.key = key
        key.platforms.append(c)
        containers[c.id] = c
        
        ## Create a door hinged on the left hand side
        c = Door('left door')
        containers[c.id] = c
        c.ent = scn.createEntity("Left_Door","door.mesh")
        c.ent.setCastShadows(True)

        c.node = self.rootNode.createChildSceneNode(c.ent.getName())

        c.node.attachObject(c.ent)
        c.node.setPosition(4,2.5,-50)
        c.node.setScale(4,1,2)

        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(20.0,self._world, self._space)
        c.body.setDamping(0,20)
        c.geom = c.body.getGeometry(0)

        c.joint = OgreOde.HingeJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAxis(ogre.Vector3().UNIT_Y)
        c.joint.setAnchor(ogre.Vector3(7.5,2.5,-50))
        
        # create fixed joint to form a lock
        l = OgreOde.FixedJoint(self._world)
        l.attach(c.body)
        c.locks.append(l)
        c.locked = True
        
        c.sound = self.sounds[random.choice(self.doorSounds)]

        c.geom.setUserData(c.id)

        key.doors.append(c)
        
        ## Create a door hinged on the right hand side
        c = Door('right door')
        containers[c.id] = c
        c.ent = scn.createEntity("Right_Door","door.mesh")
        #c.ent.setNormaliseNormals(True)
        c.ent.setCastShadows(True)

        c.node = self.rootNode.createChildSceneNode(c.ent.getName())

        c.node.attachObject(c.ent)
        c.node.setPosition(-4.1,2.5,-50)
        c.node.setScale(4,1,2)
        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(20.0,self._world, self._space)
        c.body.setDamping(0,2)
        c.geom = c.body.getGeometry(0)

        c.joint = OgreOde.HingeJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAxis(ogre.Vector3().UNIT_Y)
        c.joint.setAnchor(ogre.Vector3(-7.6,2.5,-50))
        
        c.sound = self.sounds[random.choice(self.doorSounds)]
        
        # create fixed joint to form a lock
        l = OgreOde.FixedJoint(self._world)
        l.attach(c.body)
        c.locks.append(l)
        c.locked = True
        
        c.geom.setUserData(c.id)
    
        key.doors.append(c)
        
        
        
        self.loadArea0()
        #self.loadArea1()
        #self.loadArea2()
        #self.loadArea3()
        #print 'Containers:', containers


    def loadArea0(self):
        scn = self.rootNode.getCreator()
        offset = 0

        # create a key
        key = MultiKey('Area0')
        key.unlockCallback = self.areaClear

        ##Create a platform
        c = Platform(materialName = 'platform0-')
        containers[c.id] = c
        c.ent = scn.createEntity('plat0', 'platform.mesh')
        c.node = self.rootNode.createChildSceneNode('platform')
        c.node.setPosition(ogre.Vector3(0, 0.09, offset - 30))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        # set the floor color properly
        #sub = c.ent.getSubEntity(0)
        #sub.materialName = 'plat0'
            
        # copied from SimpleScenes_TriMesh, there's probably a much more efficient way to do this
        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['key-0']
        #c.sound = random.choice(self.sounds.values())
        c.quant = 8

        # set the initial material
        c.setMaterial()

        c.key = key
        key.platforms.append(c)

        ##Create dynamic platform    

        c = Platform(materialName = 'platform0-')
        containers[c.id] = c
        c.ent = scn.createEntity('tilt_plat', 'platform.mesh')
        c.node = self.rootNode.createChildSceneNode('tilt_platform')
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)

        c.body = OgreOde.Body(self._world, 'OgreOde::Body_' + c.node.getName())
        c.node.attachObject(c.body)
        mass = OgreOde.BoxMass (20.0, ei.getSize())
        mass.setDensity(5.0, ei.getSize())
        c.body.setMass(mass)
        
        c.geom.setBody(c.body)
        c.ent.setUserObject(c.geom)
        
        c.body.setPosition(ogre.Vector3(40, 2, offset))

        c.joint = OgreOde.BallJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAnchor(ogre.Vector3(40, 2, offset))

        c.sound = self.sounds['key-1']
        #c.sound = random.choice(self.sounds.values())
        c.quant = 8

        # set the initial material
        c.setMaterial()

        c.geom.setUserData(c.id)

        c.key = key
        key.platforms.append(c)
        
        ##end dynamic platform




        # [Jumping Platforms
        # [Platform 1
        c = Platform(materialName = 'plat1-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('plat1', 'plat1.mesh')
        c.node = self.rootNode.createChildSceneNode('plat1')
        c.node.setPosition(ogre.Vector3(0, 3, offset))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['tabla-0']

        c.setMaterial()
        # Platform 1]

        # [Platform 2
        c = Platform(materialName = 'plat1-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('plat2', 'plat1.mesh')
        c.node = self.rootNode.createChildSceneNode('plat2')
        c.node.setPosition(ogre.Vector3(-2, 6, offset + 4))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['tabla-1']

        c.setMaterial()
        # Platform 2]

        # [Platform 3
        c = Platform(materialName = 'plat1-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('plat3', 'plat2.mesh')
        c.node = self.rootNode.createChildSceneNode('plat3')
        c.node.setPosition(ogre.Vector3(-4, 9, offset + 8))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['tabla-2']

        c.setMaterial()
        # Platform 3]

        # [Platform 4
        c = Platform(materialName = 'plat1-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('plat4', 'plat2.mesh')
        c.node = self.rootNode.createChildSceneNode('plat4')
        c.node.setPosition(ogre.Vector3(-4, 12, offset + 12))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['tabla-3']

        c.setMaterial()
        # Platform 4]

        # [Platform 5
        c = Platform(materialName = 'plat1-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('plat5', 'plat3.mesh')
        c.node = self.rootNode.createChildSceneNode('plat5')
        c.node.setPosition(ogre.Vector3(-2, 15, offset + 16))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['tabla-4']

        c.setMaterial()
        # Platform 5]

        # [Key Platform
        c = Platform(materialName = 'platform0-')
        containers[c.id] = c
        c.ent = scn.createEntity('keyplat2', 'platform.mesh')
        c.node = self.rootNode.createChildSceneNode('keyplat2')
        c.node.setPosition(ogre.Vector3(0, 18, offset + 20))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['key-2']
        c.quant = 8

        c.setMaterial()
        
        c.key = key
        key.platforms.append(c)
        # Key Platform]
        # Jumping Platforms]


        # [Ramp
        # [Ramp 1
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_Start', 'RampStart.mesh')
        c.node = self.rootNode.createChildSceneNode('rampstart')
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(175), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(-27, 2.65, offset - 28.5))        
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-0']

        c.setMaterial()
        # Ramp 1]

        # [Ramp 2
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_2', 'ramp2.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp2')
        c.node.setScale(ogre.Vector3(1.0, 1.0, 0.96))
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(179.5), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(-41.0, 4.45, offset + 1.7))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-1']

        c.setMaterial()
        # Ramp 2]

        # [Ramp 3
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_3', 'ramp3.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp3')
        c.node.setScale(ogre.Vector3(1.0, 1.0, 1.1))
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(184.5), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(-32.4, 8.125, offset + 30.75))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-0']

        c.setMaterial()
        # Ramp 3]

        # [Ramp 4
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_4', 'ramp4.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp4')
        c.node.setScale(ogre.Vector3(0.93, 1.0, 1.0))
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(177.5), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(0, 9.65, offset + 42.507))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-1']

        c.setMaterial()
        # Ramp4]

        # [Ramp 5
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_5', 'ramp5.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp5')
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(177.5), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(32, 11.485, offset + 34.3))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-0']

        c.setMaterial()
        # Ramp5]

        # [Ramp 6
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_6', 'ramp6.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp6')
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(179.5), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(41, 12.55, offset + 0.4))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-1']

        c.setMaterial()
        # Ramp6]

        # [Ramp 7
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_7', 'ramp7.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp7')
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(179.4), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(32.3, 12.8, offset - 33))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-0']

        c.setMaterial()
        # Ramp7]

        # [Ramp 8
        c = Platform(materialName = 'LRamp-')
        containers[c.id] = c
        #self.ramps.append(c.id)
        c.ent = scn.createEntity('Ramp_8', 'ramp8.mesh')
        c.node = self.rootNode.createChildSceneNode('ramp8')
        c.node.setOrientation(ogre.Quaternion(ogre.Degree(179.8), ogre.Vector3().UNIT_Y))
        c.node.setPosition(ogre.Vector3(14.5, 14.1, offset - 36.9))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['neutron-1']

        c.setMaterial()
        # Ramp8]

        # [Key Platform
        c = Platform(materialName = 'platform0-')
        containers[c.id] = c
        c.ent = scn.createEntity('keyplat3', 'platform.mesh')
        c.node = self.rootNode.createChildSceneNode('keyplat3')
        c.node.setPosition(ogre.Vector3(14.5, 15, offset - 35.7))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['key-3']
        c.quant = 8

        c.setMaterial()
        
        c.key = key
        key.platforms.append(c)
        # Key Platform]
        # Ramp]
        
        
        #Need door here
         #Create the glass exit door
        c = Door('r Door')
        containers[c.id] = c
        c.ent = scn.createEntity("r_Door","door.mesh")
        #c.ent.setNormaliseNormals(True)
        c.ent.getSubEntity(0).materialName = "MusicDoor"
        c.ent.setCastShadows(True)

        c.node = self.rootNode.createChildSceneNode(c.ent.getName())

        c.node.attachObject(c.ent)
        c.node.setPosition(0,2.8,offset + 48)
        c.node.setScale(8,1,1)
        
        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(200.0,self._world, self._space)
        c.body.setDamping(200,200)
        c.geom = c.body.getGeometry(0)

        c.joint = OgreOde.HingeJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAxis(ogre.Vector3().UNIT_Y)
        c.joint.setAnchor(ogre.Vector3(0,0,offset + 48))
        
        c.sound = self.sounds[random.choice(self.doorSounds)]
        
        l = OgreOde.FixedJoint(self._world)
        l.attach(c.body)
        c.locks.append(l)
        c.locked = True
        
        c.geom.setUserData(c.id)
        
        key.doors.append(c)
        
        
        

    def loadArea1(self):
        offset = 100
        # The offset value tells you which sublevel to draw everything on
        #print self.cameraPositions
        #print self.cameraPositions[2]
        #self.cameraPositions[2] = ogre.Vector3(-35, 45, offset - 50)
        
        #I want my antigravity back :(
        #self.player.powerups.append("gravity") # too bad
        self.nrackliffe_Dominoes(offset)
        
    def loadArea2(self):
        scn = self.rootNode.getCreator()
        offset = 200
        
        key = MultiKey('Area2')
        key.unlockCallback = self.areaClear
        
        self.nextPlatformSound=0
        
        self.WobblyPlatforms = []
        
        def plRamp(self, x, y, z, roty):
            
            name = 'plramp_%f_%f_%f' % (x,y,z)
            c = Platform(name, materialName = 'thinmat3')
            self.WobblyPlatforms.append(c.id)
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'ramp.mesh')
            c.node = self.rootNode.createChildSceneNode(name)
            
            c.node.setPosition(ogre.Vector3(x, y, z+offset))
            c.node.rotate(ogre.Vector3(0,1,0), ogre.Degree(roty))
            
            #scale ever so slightly so that ramps can be put next to each other without collisions
            c.node.setScale(0.9999,0.9999,0.9999)
            
            c.node.attachObject(c.ent)

            c.ent.setCastShadows(True)

            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createStaticTriangleMesh(self._world, self._space)
            
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)
            if self.nextPlatformSound > 5:
                self.nextPlatformSound=0
            c.sound = self.sounds['tabla-%d' % self.nextPlatformSound]
            self.nextPlatformSound+=1

            
            c.setMaterial()
            
        def plDynamicPlatform(self, x, y, z, roty):
            name = 'plDynamicPlatform_%f_%f_%f' % (x,y,z)
            c = Platform(name, materialName = 'thinmat2')
            self.WobblyPlatforms.append(c.id)
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'thinplat.mesh')
            c.node = self.rootNode.createChildSceneNode(name)
            c.ent.setCastShadows(False)
            c.node.setPosition(ogre.Vector3(x, y, z+offset))

            quat = ogre.Quaternion(ogre.Degree(roty),ogre.Vector3().UNIT_Y)
            c.node.setOrientation(quat)
            
            #scale ever so slightly so that platforms can be put next to each other without collisions
            c.node.setScale(0.9999,0.9999,0.9999)

            c.node.attachObject(c.ent)
            c.startPosition = (x,y,z+offset)
            c.node.setPosition(c.startPosition)
            quat = ogre.Quaternion(ogre.Degree(roty),ogre.Vector3().UNIT_Y)
            c.node.setOrientation(quat)
            ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
            
            c.body = ei.createSingleDynamicBox(20.0,self._world, self._space)
            c.geom = c.body.getGeometry(0)
            c.joint = OgreOde.HingeJoint(self._world)
            c.joint.attach(c.body)
            c.joint.setAxis(quat.zAxis())
            c.joint.setAnchor(ogre.Vector3(x,y,z+offset))

            c.geom.setBody(c.body)
            c.ent.setUserObject(c.geom)
            
            c.geom.setUserData(c.id)
            
            c.sound = self.sounds['wurl-%d' % random.randint(0, 3)]
            
            c.setMaterial()


        def plStaticPlatform(self, x, y, z, roty):
            name = 'plStaticPlatform_%f_%f_%f' % (x,y,z)
            c = Platform(name, materialName = 'thinmat3')
            self.WobblyPlatforms.append(c.id)
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'thinplat.mesh')
            c.node = self.rootNode.createChildSceneNode(name)
            c.ent.setCastShadows(True)
            c.node.setPosition(ogre.Vector3(x, y, z+offset))

            quat = ogre.Quaternion(ogre.Degree(roty),ogre.Vector3().UNIT_Y)
            c.node.setOrientation(quat)
            #scale ever so slightly so that platforms can be put next to each other without collisions
            c.node.setScale(0.9999,0.9999,0.9999)

            c.node.attachObject(c.ent)
            c.startPosition = (x,y,z+offset)
            c.node.setPosition(c.startPosition)
            quat = ogre.Quaternion(ogre.Degree(roty),ogre.Vector3().UNIT_Y)
            c.node.setOrientation(quat)
            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createStaticTriangleMesh(self._world, self._space)
            
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)
            
            c.sound = self.sounds['bowen-%d' % random.randint(0, 3)]
            
            c.setMaterial()


        def plKeyPlatform(x, y, z, k):
            name = 'plkeyplat_%f_%f_%f' % (x,y,z)
            c = Platform(materialName = 'platform0-')
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'platform.mesh')
            c.node = self.rootNode.createChildSceneNode(name)
            c.node.setPosition(ogre.Vector3(x, y, z+offset))
            c.node.attachObject(c.ent)
            
            #make key platform a bit larger            
            c.node.setScale(1.55,1.55,1.55)
            
            c.ent.setCastShadows(True)
            
            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createStaticTriangleMesh(self._world, self._space)
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)

            c.sound = self.sounds['key-%d' % k]
            c.quant = 8

            c.setMaterial()

            c.key = key
            key.platforms.append(c)

        def makeWobblyPlatform(self, x, y, z, roty, seperation):
            plDynamicPlatform(self, x, y, z, roty)
            plStaticPlatform(self, x, y-seperation, z, roty)
        
        ##Setup area
        #North platforms 
        for i in range(15):
            plRamp(self, 30,0.5+i,-25+i, 0.0)
        
        for i in range(20):
            makeWobblyPlatform(self, 30, 15, -10+i, 0.0, 2.0)
            
        plKeyPlatform(30.5, 14.5, 15, 0)
        
        #East platforms
        for i in range(5):
            plRamp(self, 25-i,14-i, 15, 90)
            
        for i in range(15):
            makeWobblyPlatform(self, 20-i, 10, 15, 90, 2.0)
            
        for i in range(5):
            plRamp(self, 5-i,10+i, 15, 270)

        for i in range(5):
            plRamp(self, 0-i, 14-i, 15, 90)
        
        for i in range(15):
            makeWobblyPlatform(self, -5-i, 10, 15, 90, 2.0)
            
        plKeyPlatform(-25, 10, 15, 1)
        
        #South Platforms
        for i in range(10):
            makeWobblyPlatform(self, -25-i, 10, 9-i, 0, 2.0)
            
        for i in range(10):
            makeWobblyPlatform(self,  -35+i, 10 , -1-i, 0, 2.0)
            
        plKeyPlatform(-25, 10, -16, 2)
        
        #Center Platforms
        for i in range(10):
            plRamp(self, -20+i , 10+i,-16, 90)

        #make the ones at the end a little easier we wouldn't want the player to fall off now... would we?
        for i in range(20):
            makeWobblyPlatform(self,  -10+i, 19 , -16, 90, 1.5)
        
        #drop down a bit to the platform
        plKeyPlatform( 15, 17, -16, 3)
        
        #Create the glass exit door
        c = Door('p Door')
        containers[c.id] = c
        c.ent = scn.createEntity("p_Door","pdoor0.mesh")
        #c.ent.setNormaliseNormals(True)
        c.ent.setCastShadows(True)

        c.node = self.rootNode.createChildSceneNode(c.ent.getName())

        c.node.attachObject(c.ent)
        c.node.setPosition(0,2.8,47+offset)
        
        c.ent.getSubEntity(0).materialName = 'thinmat2'
        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(20.0,self._world, self._space)
        c.body.setDamping(0,20)
        c.geom = c.body.getGeometry(0)

        c.joint = OgreOde.HingeJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAxis(ogre.Vector3().UNIT_X)
        c.joint.setAnchor(ogre.Vector3(0,5,47+offset))
        
        c.sound = self.sounds[random.choice(self.doorSounds)]
        
        l = OgreOde.FixedJoint(self._world)
        l.attach(c.body)
        c.locks.append(l)
        c.locked = True
        
        c.geom.setUserData(c.id)
        
        key.doors.append(c)
        
    def loadArea3(self):
        scn = self.rootNode.getCreator()
        offset = 300

        tilesize = 6
        startx = tilesize * 5
        starty = 0.2
        startz = -(tilesize * 4)

        # load our powerup

        g = Powerup('gravity', 'GravityLift')
        containers[g.id] = g
        g.ent = scn.createEntity('GravityLift', 'GravityLift.mesh')
        g.node = self.rootNode.createChildSceneNode()

        g.node.attachObject(g.ent)
        g.node.setPosition(startx + (tilesize * -7),
                           3,
                           startz + (tilesize * 7) + offset)

        ei = OgreOde.EntityInformer(g.ent, ogre.Matrix4.getScale(self.player.node.getScale()))
        g.geom = ei.createSingleStaticBox(self._world, self._space)

        g.geom.setUserData(g.id)

        g.sound = self.sounds['bell-hi-0']

        g.overlay = ogre.OverlayManager.getSingleton().getByName('AntigravityOverlay')
        g.overlay.hide()

        # animation for the powerup
        g.anim = scn.createAnimation('GravityLiftRotate', 8)
        g.anim.interpolationMode = ogre.Animation.IM_SPLINE

        track = g.anim.createNodeTrack(0, g.node)

        key = track.createNodeKeyFrame(0)
        key.setTranslate(g.node.getPosition())
        key.setRotation(ogre.Quaternion(ogre.Degree(0), ogre.Vector3().UNIT_X))

        key = track.createNodeKeyFrame(2)
        key.setTranslate(g.node.getPosition())
        key.setRotation(ogre.Quaternion(ogre.Degree(180), ogre.Vector3().UNIT_X))

        key = track.createNodeKeyFrame(6)
        key.setTranslate(g.node.getPosition())
        key.setRotation(ogre.Quaternion(ogre.Degree(180), ogre.Vector3().UNIT_Z))

        key = track.createNodeKeyFrame(8)
        key.setTranslate(g.node.getPosition())
        key.setRotation(ogre.Quaternion(ogre.Degree(0), ogre.Vector3().UNIT_X))

        aState = scn.createAnimationState('GravityLiftRotate')
        aState.setEnabled(True)
        aState.setLoop(True)

        self.animations.append(aState)


        # create our exit key
        key = MultiKey('Area3')
        key.unlockCallback = self.areaClear
        self.lastKey = key

        ## functions for building the maze tiles

        # available sounds for each type of maze unit
        h0Sounds = ['tabla-%d' % i for i in range(0, 5)]
        v1Sounds = ['bowen-%d' % i for i in range(0, 3)]
        v2Sounds = ['wurl-%d' % i for i in range(0, 3)]
        holesounds = ['neutron-0', 'neutron-1']
        
        def mkHPlane(x, y, z, isKey, lastKey):
            '''
            Create a single piece in the XZ Plane
            '''
            
            name = 'mz_h_%d_%d_%d' % (x, y, z)

            floor = y
            
            #print 'adding maze unit', name
            
            # scale the values appropriately
            x = -x * tilesize + startx
            y = y * tilesize + starty
            z = z * tilesize + startz
            

            c = Platform(name, materialName = 'mazeGlass%d-' % floor)
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'HPlane.mesh')
            c.node = self.rootNode.createChildSceneNode()
            c.node.setPosition(ogre.Vector3(x, y, z + offset))
            c.node.attachObject(c.ent)
            c.ent.setCastShadows(False)
                    
            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createSingleStaticBox(self._world, self._space)
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)
                    
            if isKey:
                c.key = key
                key.platforms.append(c)
                c.materialName = 'mazeGlass-key-'
                c.sound = self.sounds['key-%d' % lastKey]
                c.quant = 8
                lastKey += 1
            else:
                c.sound = self.sounds[random.choice(h0Sounds)]
                
            # set the initial material
            c.setMaterial()

            self.mazeBits.append(c.id)

        def mkHole(x, y, z):
            '''
            Create a single piece in the XZ Plane with a hole in it
            '''
            
            name = 'mz_hole_%d_%d_%d' % (x, y, z)

            #print 'adding maze unit', name
            
            # scale the values appropriately
            x = -x * tilesize + startx
            y = y * tilesize + starty
            z = z * tilesize + startz
            

            c = Platform(name, materialName = 'mazeGlass-hole-')
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'Hole.mesh')
            c.node = self.rootNode.createChildSceneNode()
            c.node.setPosition(ogre.Vector3(x, y, z + offset))
            c.node.attachObject(c.ent)
            c.ent.setCastShadows(False)
                    
            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createStaticTriangleMesh(self._world, self._space)
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)
                    
            c.sound = self.sounds[random.choice(holesounds)]

            # set the initial material
            c.setMaterial()
            
            self.mazeBits.append(c.id)


        def mkVPlane(x, y, z, isKey, lastKey):
            '''
            Create a single piece in the XY Plane
            '''
            
            name = 'mz_v1_%d_%d_%d' % (x, y, z)

            floor = y

            # scale the values appropriately
            x = -x * tilesize + startx
            y = y * tilesize + starty + tilesize / 2
            z = z * tilesize + startz - tilesize / 2
            
            #print 'adding maze unit', name
            
            c = Platform(name, materialName = 'mazeGlass%d-' % floor)
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'VPlane.mesh')
            c.node = self.rootNode.createChildSceneNode()
            c.node.setPosition(ogre.Vector3(x, y, z + offset))
            c.node.attachObject(c.ent)
            c.ent.setCastShadows(False)
                    
            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createSingleStaticBox(self._world, self._space)
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)
                    
            if isKey:
                c.key = key
                key.platforms.append(c)
                c.materialName = 'mazeGlass-key-'
                c.sound = self.sounds['key-%d' % lastKey]
                c.quant = 8
            else:
                c.sound = self.sounds[random.choice(v1Sounds)]
                
            c.setMaterial()

            self.mazeBits.append(c.id)


        def mkVPlane2(x, y, z, isKey, lastKey):
            '''
            Create a single piece in the ZY Plane
            '''
            
            name = 'mz_v2_%d_%d_%d' % (x, y, z)

            floor = y
            
            x = -x * tilesize + startx - tilesize / 2
            y = y * tilesize + starty + tilesize / 2
            z = z * tilesize + startz
            
            #print 'adding maze unit', name
            
            c = Platform(name, materialName = 'mazeGlass%d-' % floor)
            containers[c.id] = c
            c.ent = scn.createEntity(name, 'VPlane2.mesh')
            c.node = self.rootNode.createChildSceneNode()
            c.node.setPosition(ogre.Vector3(x, y, z + offset))
            c.node.attachObject(c.ent)
            c.ent.setCastShadows(False)
                    
            ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
            c.geom = ei.createSingleStaticBox(self._world, self._space)
            c.ent.setUserObject(c.geom)
            c.geom.setUserData(c.id)
                    
                    
            if isKey:
                c.key = key
                key.platforms.append(c)
                c.materialName = 'mazeGlass-key-'
                c.sound = self.sounds['key-%d' % lastKey]
                c.quant = 8
            else:
                c.sound = self.sounds[random.choice(v2Sounds)]
                
            c.setMaterial()

            self.mazeBits.append(c.id)


        h0 = [
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 2, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 2, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 3, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 3, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 3, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 3, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 3, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 3, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 3, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 3, 3, 1, 1, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 3, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              ]
        v1 = [
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
               [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
               [1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
               [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
               [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
               [1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
               [1, 0, 0, 1, 0, 0, 1, 0, 0, 1]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
               [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
               [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
               [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 1, 1]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
               [0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
               [0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
               [0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
               [0, 1, 1, 1, 1, 1, 1, 2, 1, 0],
               [0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              ]
        v2 = [
              [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
               [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
               [1, 1, 1, 0, 0, 0, 1, 1, 1, 0]],
              [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
               [1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 2, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
               [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
               [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
               [0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
              ]
        


        lastKey = 0 # last key sound used
        
        for x in range(10):
            for y in range(6):
                for z in range(10):

                    if h0[y][x][z]:
                        if h0[y][x][z] == 3:
                            mkHole(x, y, z)
                        else:
                            mkHPlane(x, y, z, h0[y][x][z] > 1, lastKey)
                            if h0[y][x][z] > 1:
                                lastKey += 1
                    if v1[y][x][z]:
                        mkVPlane(x, y, z, v1[y][x][z] > 1, lastKey)
                        if v1[y][x][z] > 1:
                            lastKey += 1
                    if v2[y][x][z]:
                        mkVPlane2(x, y, z, v2[y][x][z] > 1, lastKey)
                        if v2[y][x][z] > 1:
                            lastKey += 1
                    

        # one door to top off the maze

        c = Door('MazeExitCap')
        containers[c.id] = c
        c.ent = scn.createEntity('MazeExitCap', 'MazeDoor.mesh')
        c.ent.setCastShadows(False)
        c.node = self.rootNode.createChildSceneNode(c.ent.getName())
        c.node.attachObject(c.ent)

        #sub = c.ent.getSubEntity(0)
        #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door

        # right in the middle
        x = -5 * tilesize + startx
        y = 6 * tilesize + starty + 0.5 # small offset so we don't hit a static collision thing
        z = 4 * tilesize + startz + offset
        c.node.setPosition(x, y, z)

        ei = OgreOde.EntityInformer(c.ent, ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(1.0,self._world, self._space)
        
        c.body.sleep() # put the door to sleep until we need it
        c.geom = c.body.getGeometry(0)

        c.sound = self.sounds[random.choice(self.doorSounds)]
        c.geom.setUserData(c.id)
            
        l = OgreOde.FixedJoint(self._world)
        l.attach(c.body)
        c.locks.append(l)
        c.locked = True
        
        key.doors.append(c)



        # make some doors for the exit

        def mkDoorCube(name, x, y, z):
            c = Door(name)
            containers[c.id] = c
            c.ent = scn.createEntity(name, "Cube.mesh")
            #c.ent.setNormaliseNormals(True)
            c.ent.setCastShadows(True)

            #sub = c.ent.getSubEntity(0)
            #sub.materialName = 'Ac3d/Door/Mat001_Tex00' # look like a door


            
            c.node = self.rootNode.createChildSceneNode(c.ent.getName())
            c.node.attachObject(c.ent)

            c.node.setPosition(x + 0.5, y + 0.5, z + offset)

            ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
            c.body = ei.createSingleDynamicBox(0.2,self._world, self._space)
            #c.body.setDamping(2,2)
            c.body.sleep() # put the doors to sleep until we need them
            c.geom = c.body.getGeometry(0)

            c.sound = self.sounds[random.choice(self.doorSounds)]
            c.geom.setUserData(c.id)
            
            l = OgreOde.FixedJoint(self._world)
            l.attach(c.body)
            c.locks.append(l)
            c.locked = True

            key.doors.append(c)

            return c
        

        for x in range(-8, 8):
            for y in range(0, 5):
                z = 49
         
                mkDoorCube('doorCube_%d_%d_%d' % (x, y, z), x, y, z)




    def initSounds(self, app):
        self.plsounds = {}
        self.sounds = {}
        self.music = {}

        sm = app.soundManager
        self.mm = app.musicManager

        self.mm.setTempo(self.tempo)
        
        # grab our background tracks
        self.music['bg-1'] = sm.createSound('bg-1', 'level-0-1.wav', True)
        self.music['bg-2'] = sm.createSound('bg-2', 'level-0-2.wav', True)
        self.music['bg-3'] = sm.createSound('bg-3', 'level-0-3.wav', True)
        self.music['bg-4'] = sm.createSound('bg-4', 'level-0-4.wav', True)

        # set all music tracks relative to the listener
        for m in self.music.values():
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
            self.sounds[f] = sm.createSound(f, f + '.wav', False)        

            
        # set all sounds relative to the listener
        for s in self.sounds.values():
            s.setRelativeToListener(True)


        self.doorSounds = ['bell-hi-0', 'bell-hi-1', 'bell-lo-0', 'bell-lo-1',
                 'bowen-0', 'bowen-1', 'bowen-2', 'bowen-3',
                 'neutron-0', 'neutron-1']
    
    def setArea(self, area):
        '''
        Set our current area
        '''

        if area == self.area:
            return

        if area < 0:
            return
        
        if area in [1,2,3,4]:
            try: self.particles["StartArrow"] #check to see if particles exist
            except KeyError: #if they don't
                #player has jumped a wall, CHEATER!
                self.player.warpTo = (self.playerStarts[area-1])
                return 'CHEATER'
            else: #if they do
                self.particles["StartArrow"].particleSystem.removeAllEmitters()
                self.decayParticle = True

        print 'Entering area %d' % area

        # set the appropriate background music
        if self.area in [0, 1, 5] and area not in [0, 1, 5]:
            self.mm.stopSound(self.music['bg-1'], 0)
        elif self.area == 2:
            self.clearDominoes()
            self.mm.stopSound(self.music['bg-2'], 0)
        elif self.area == 3:
            self.mm.stopSound(self.music['bg-3'], 0)
        elif self.area == 4:
            self.mm.stopSound(self.music['bg-4'], 0)

        if area in [0, 1, 5] and self.area not in [0, 1, 5]:
            self.mm.addQueuedSound(self.music['bg-1'], self.mm.totalBeats)
        elif area == 2:
            self.mm.addQueuedSound(self.music['bg-2'], self.mm.totalBeats)
        elif area == 3:
            self.mm.addQueuedSound(self.music['bg-3'], self.mm.totalBeats)
        elif area == 4:
            self.mm.addQueuedSound(self.music['bg-4'], self.mm.totalBeats)

        # warp the character if we're just starting
        if self.area == -1:
            self.player.warpTo = (self.playerStarts[area])

        self.area = area

        # move the camera
        if self.area == 0 :
            return # Don't animate the camera to start
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
        #key.setTranslate (self.cameraPositions[self.area] - self.camera.getPosition())
        key.setTranslate(node.getPosition() + ogre.Vector3().UNIT_Z*100)
        animationState = sceneManager.createAnimationState('CameraTrack')
        animationState.setEnabled(True)
        animationState.setLoop(False)

        self.animations.append(animationState)

        
    def triggerRandomSounds(self):

        numSounds = random.randint(3, 10)

        print 'Queing %d random sounds' % numSounds

        sounds = random.sample(self.sounds.values(), numSounds)

        for sound in sounds:
            self.mm.addQueuedSound(sound, random.choice([2, 4]), random.choice([8, 4, None, None, None]))

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
                    print 'Static collision error: %s <=> %s' % (containers[u1].name, containers[u2].name)
                return False


            u1 = g1.getUserData()
            u2 = g2.getUserData()

            #print u1, u2

            if u1 in containers and u2 in containers:
                #print containers[u1], containers[u1].name, 'collided with', containers[u2], containers[u2].name
                if containers[u1] is self.player:
                    return self.collideWithPlayer(containers[u2], contact, contact.getNormal())
                elif containers[u2] is self.player:
                    return self.collideWithPlayer(containers[u1], contact, -contact.getNormal())
                #by this point, we know it's not a player

                #Deal with domino collisions
                elif isinstance(containers[u1], Domino):
                    return self.collideWithDomino(containers[u1], containers[u2], contact, contact.getNormal())
                elif isinstance(containers[u2], Domino):
                    return self.collideWithDomino(containers[u2], containers[u1], contact, -contact.getNormal())
                    
                
                # see if something hit a platform that wasn't the player
                elif isinstance(containers[u1], Platform):
                    return self.collideWithPlatform(containers[u1], containers[u2], contact, contact.getNormal())
                elif isinstance(containers[u2], Platform):
                    return self.collideWithPlatform(containers[u2], containers[u1], contact, -contact.getNormal())
                
                #Deal with door collisions
                elif isinstance(containers[u1], Door):
                    return self.collideWithDoor(containers[u1], containers[u2], contact, contact.getNormal())
                elif isinstance(containers[u2], Door):
                    return self.collideWithDoor(containers[u2], containers[u1], contact, contact.getNormal())

                else:
                    print 'Strange container collision: %s <=> %s' % (containers[u1].name, containers[u2].name)
                    

        return True
    def collideWithDomino(self, me, other, contact, normal):
        if isinstance(other, Arena):
            #print "%s (Domino) really shouldn't run into %s" % (str(me.name), str(other.name))
            pass #It's ok if dominos hit the ground
        elif isinstance(other, Domino):
            if me.arm():
                if not self.mm.isFireKeyQueued(me.id):
                    self.mm.addQueuedSound(me.sound, me.quant, me.rest, me.id)
            if other.arm():
                if not self.mm.isFireKeyQueued(other.id):
                    self.mm.addQueuedSound(other.sound, other.quant, other.rest, other.id)
            contact.setCoulombFriction( 50 )
            contact.setBouncyness(0.2)
            return True
                
        elif type(other) == Container:
            pass # Also don't care a whole lot about generic Container (Read Stairs) collisions
        elif isinstance(other,Platform):
            if other.arm():
                if not self.mm.isFireKeyQueued(other.id):
                    self.mm.addQueuedSound(other.sound, other.quant, other.rest, other.id)
        else:
            print "%s (Domino) really shouldn't run into %s" % (str(me.name), str(other.name))
        ## Set the friction at the contact
        ## Infinity didn't get exposed :(
        contact.setCoulombFriction( 9999999999 )    ### OgreOde.Utility.Infinity)
        contact.setBouncyness(0.4)
    
        ## Yes, this collision is valid
        return True
    def collideWithDoor(self, me, other, contact, normal):

        # honestly, we don't much care what a door hits

        ## Set the friction at the contact
        
        contact.setCoulombFriction( 20 )    # Don't make the doors too sticky
        contact.setBouncyness(0.5)
    
        ## Yes, this collision is valid
        return True        
    def collideWithPlayer(self, other, contact, normal):

        # note that normal may be flipped on the way in
        if normal != self.player.jumpVector:
            self.player.jumpVector = normal

        self.player.jumpTime = 0.050 # jump for just a bit
                    
        if isinstance(other, Arena):
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
                    if other.arenaId == 5:
                        # last one
                        overlay = ogre.OverlayManager.getSingleton().getByName('CongratsOverlay')
                        overlay.show()
                        self.fireworks()
                    
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
        


 
    def nrackliffe_Dominoes(self, offset = 0):
        scn = self.rootNode.getCreator()
        # unlock key
        key = MultiKey()
        key.unlockCallback = self.areaClear
        
        self.dominoOffset = offset
        
        self.dominoStage1()
    #Key Platforms
        self.makePlatform("D_platform0", 5,offset+40,15,key, 0)
        self.makePlatform("D_platform1", -5,offset+40,15,key, 1)
        p = self.makePlatform("D_platform2", 14, offset, 10,key, 2)
        p.fireCallback = self.dominoStage2
        p = self.makePlatform("D_platform4", -14, offset, 10, key, 3)
        p.fireCallback = self.dominoStage3
        
    #Reset Platform
        ##Create a platform
        c = Platform("ResetDominoes", materialName = 'njrWoodPallet-',restartable=True)
        c.fireCallback = self.resetDominoes
            
        containers[c.id] = c
        c.ent = scn.createEntity("ResetDominoes", 'WoodPallet.mesh')
        c.node = self.rootNode.createChildSceneNode("ResetDominoes")
        c.node.setPosition(ogre.Vector3(20, 6,offset-45))
        quat = ogre.Quaternion(ogre.Degree(90),ogre.Vector3().UNIT_X)
        c.node.setOrientation(quat)
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(False)
        
        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['runup']
        c.setMaterial()
        
        self.dominoResetPlatform = c    
      
        #make Domino doors to the next sublevel
        floor = 2.1
        jointAnchor = 0.1
        door_offset = offset+50 #End of our area
        
        for i in [6,3,0,-3,-6]:
            name = "DominoDoor_%d" %i
            d = self.makeDominoDoor(name, i, door_offset, floor, jointAnchor)
            key.doors.append(d)
            
    def dominoStage1(self):
        offset = self.dominoOffset
        floor = 2.5
        for i in range(-27,0,3):
            for j in range(0,10,1):
                self.makeDomino("D_fan%d_%d" % (j,i), (j-5)*2.5, offset+i, floor+((i+27)/27.0)*j,0)

        # I'm too lazy to figure out blender, so let's use dominoes
        for i in range(0,10,1):
            d = self.makeStair("D_Stairs_%d" % i,(i-5)*2.5, offset, floor+i*.9-2)
            
    def dominoStage2(self):
        offset = self.dominoOffset
        
        
        #High road
        floor = 12
        for i in range(5, 35, 2):
            self.makeDomino("D_highroad_%d" % i, 14, offset+i, floor, 0)
            self.makeDomino("D_highroad2_%d" % i,-14, offset+i, floor,0)
        for i in range(-12,14,2):
            self.makeDomino("D_highroadcenter_%d" %i, i, offset+37,floor,90)
        self.makeDomino("D_highroad_leadin_00", -14, offset+35,floor,30)
        self.makeDomino("D_highroad_leadin_01", -13, offset+36,floor,60)
        self.makeDomino("D_highroad_leadin_03", 14, offset+35,floor,-30)
        self.makeDomino("D_highroad_leadin_04", 13, offset+36,floor,-60)
            
    def dominoStage3(self):
        offset = self.dominoOffset
        floor = 2.5
        self.clearDominoes()
        
        #NW corner
        for i in range(0,14,1):
            self.makeDomino("D_NWStair_%d" % i, i+28,offset+40-i, floor +10 - (i/(14.0))*10, -45)
            self.makeDomino("D_SWStair_%d" % -i, -(i+28),offset+40-i, floor +10 - (i/(14.0))*10, 45)
            
        #Lead in
        self.makeDomino("D_NWStair_013", 42,offset+25,floor,-30)
        self.makeDomino("D_NWStair_014", 43,offset+24,floor,-20)
        self.makeDomino("D_NWStair_015", 43.5,offset+23,floor,-10)
        
        #Leadout
        self.makeDomino("D_NWStair_T01", 26, offset + 40, floor+10, -60)
        self.makeDomino("D_NWStair_T02", 24, offset + 40, floor+11, -70)
        self.makeDomino("D_NWStair_T03", 22, offset + 40, floor+12, -80)
        
        #Lead in
        self.makeDomino("D_SWStair_013", -42,offset+25,floor,30)
        self.makeDomino("D_SWStair_014", -43,offset+24,floor,20)
        self.makeDomino("D_SWStair_015", -44,offset+22,floor,10)
        
        #Leadout
        self.makeDomino("D_SWStair_T01", -26, offset + 40, floor+10, 60)
        self.makeDomino("D_SWStair_T02", -24, offset + 40, floor+11, 70)
        self.makeDomino("D_SWStair_T03", -22, offset + 40, floor+12, 80)


        for i in range(-21,23,2):
            #North Line
            self.makeDomino("D_NorthLine_%d" % i, 44, offset+i, floor, 0)
            #South Line
            self.makeDomino("D_SouthLine_%d" % i, -44,offset+i, floor, 0)
                
        #Over the exit dominoes
        floor = 16
        for i in range(11,20,2):
            self.makeDomino("D_Nexit_%d" % i, i, offset+40, floor, 90)
            self.makeDomino("D_Sexit_%d" % i, -i, offset+40, floor, 90)
            
    # Subfunctions to create dominoes
    def makeDomino(self, name, x, offset, floor, angle):
        scn = self.rootNode.getCreator()
        jointAnchor = floor-2.0  #Any lower and the domino won't fall all the way flat
        c = Domino(name,angle, materialName = 'Domino-')
        self.dominoes.append(c.id)
        containers[c.id] = c
        c.ent = scn.createEntity(name, "Domino.mesh")
        #c.ent.setNormaliseNormals(True)
        c.ent.setCastShadows(True)
        c.node = self.rootNode.createChildSceneNode(c.ent.getName())
        c.node.attachObject(c.ent)
        c.startPosition = (x,floor,offset)
        c.node.setPosition(c.startPosition)
        quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
        c.node.setOrientation(quat)
        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(5.0,self._world, self._space)
        c.body.setDamping(2,2)
        c.geom = c.body.getGeometry(0)
        c.joint = OgreOde.HingeJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAxis(quat.xAxis())
        c.joint.setAnchor(ogre.Vector3(x,jointAnchor,offset))
    
        #c.sound = random.choice(self.sounds.values())

        c.sound = self.sounds['tabla-%d' % random.randint(0, 5)]
        
        #print c.sound.getFileName()
        c.geom.setUserData(c.id)

        c.setMaterial()
        
        return c

    def makeDominoDoor(self, name,x,offset,floor,jointAnchor,angle=0.0):
        scn = self.rootNode.getCreator()
        c = Door(name)
        containers[c.id] = c
        c.ent = scn.createEntity(name, "door.mesh")
        #c.ent.setNormaliseNormals(True)
        c.ent.setCastShadows(True)
        c.node = self.rootNode.createChildSceneNode(c.ent.getName())
        c.node.attachObject(c.ent)
        c.startPosition = (x,floor,offset)
        c.node.setPosition(c.startPosition)
        quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
        c.node.setOrientation(quat)
        c.angle = angle
        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.body = ei.createSingleDynamicBox(5.0,self._world, self._space)
        c.body.setDamping(2,2)
        c.geom = c.body.getGeometry(0)
        c.joint = OgreOde.HingeJoint(self._world)
        c.joint.attach(c.body)
        c.joint.setAxis(quat.xAxis())
        c.joint.setAnchor(ogre.Vector3(x,jointAnchor,offset+.1))
    
        c.sound = self.sounds[random.choice(self.doorSounds)]
        
        c.geom.setUserData(c.id)
        
        l = OgreOde.FixedJoint(self._world)
        l.attach(c.body)
        c.locks.append(l)
        c.locked = True

        return c
    def makeStair(self, name,x,offset,floor):
        scn = self.rootNode.getCreator()
        c = Container(name)
        containers[c.id] = c
        # Let's put them with the dominoes so they go away afterwards
        self.stairs.append(c.id)
        c.ent = scn.createEntity(name, "door.mesh")
        #c.ent.setNormaliseNormals(True)
        c.ent.setCastShadows(False)
        c.node = self.rootNode.createChildSceneNode(c.ent.getName())
        c.node.setScale(0.1,0.1,0.1)
        c.node.attachObject(c.ent)
        c.startPosition = (x,floor,offset)
        c.node.setPosition(c.startPosition)
        ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
        c.geom = ei.createSingleStaticBox(self._world, self._space)
        c.geom.setUserData(c.id)
        return c

    def makePlatform(self, name,x,offset,floor,key,snd):
        scn = self.rootNode.getCreator()
        ##Create a platform
        c = Platform(name,materialName = 'platform0-')
        containers[c.id] = c
        c.ent = scn.createEntity(name, 'platform.mesh')
        c.node = self.rootNode.createChildSceneNode(name)
        c.node.setPosition(ogre.Vector3(x, floor,offset))
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)
        
        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(self._world, self._space)
        c.ent.setUserObject(c.geom)
        c.geom.setUserData(c.id)

        c.sound = self.sounds['key-%d' % (snd)]
        c.quant = 8
        c.setMaterial()

        c.key = key
        key.platforms.append(c)
        
        return c
            
        
    def resetDominoes(self):
        if self.dominoes:
            
            for id in self.dominoes:
                domino = containers[id]
                
                domino.body.setAngularVelocity(ogre.Vector3().ZERO)
                domino.body.setLinearVelocity(ogre.Vector3().ZERO)
                domino.body.setPosition(domino.startPosition)
                domino.body.setOrientation(ogre.Quaternion(ogre.Degree(domino.angle), ogre.Vector3().UNIT_Y))
                domino.reset()
            self.dominoResetPlatform.reset()
            return True
        else:
            return False
    def clearDominoes(self):
        if self.dominoes:
            for id in self.dominoes:
                if containers[id].body:
                    containers[id].body.wake()
                del containers[id]
            del self.dominoes [:]
        if self.stairs:
            for id in self.stairs:
                del containers[id]
            del self.stairs[:]
    def clearWobblyPlatforms(self):
        if self.WobblyPlatforms:
            for id in self.WobblyPlatforms:
                if containers[id].body:
                    containers[id].body.wake()
                del containers[id]
            del self.WobblyPlatforms [:]
                
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
            self.clearDominoes()
            self.loadArea2()
            self.startingArrow(100-40)
        elif self.area == 3:
            self.clearWobblyPlatforms()
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

    def fireWholeMaze(self):
        for mz in self.mazeBits:
            c = containers[mz]
            if c.arm():
                if not self.mm.isFireKeyQueued(c.id):
                    self.mm.addQueuedSound(c.sound, c.quant, c.rest, c.id)

        del self.mazeBits[:]
