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
        print 'Loaded Level Lab1: ACME'
        
        self.backgroundMusic = app.music['bg-1']
        # self.app = app # keep copy of app

         # middle of platform is at 0, 0, 0 (self.offset)
        # dimensions of arena are around 45
        # doors are at Z +- 45, y is altitude
        makePlatform(app, 'Platform1', self.offset + ogre.Vector3(0, 1.5, -30))
        # makeIcePlatform(app, 'A Ice Platform', self.offset + ogre.Vector3(0, 1.5, -30), 45)
        makePlatform(app, 'Platform2', self.offset + ogre.Vector3(0, 3, -25), sound = 'tone-0')
        makePlatform(app, 'Platform3', self.offset + ogre.Vector3(0, 4.5, -20))
        makePlatform(app, 'Platform4', self.offset + ogre.Vector3(0, 6, -15), sound = 'tone-1')
        makePlatform(app, 'Platform5', self.offset + ogre.Vector3(0, 8, -10))
        makePlatform(app, 'Platform6', self.offset + ogre.Vector3(0, 10, 0), sound = 'tone-4')

        makeDomino(app, "d1", self.offset + ogre.Vector3(0,10.25,0), sound = 'perc-0')

        # BRIDGE WALKWAY
        makeBridge(app, 'A Bridge', self.offset + ogre.Vector3(2.01, 10, 11))
        makeBridge(app, 'A Bridge', self.offset + ogre.Vector3(2.01, 10, 22))
        makeBridge(app, 'A Bridge', self.offset + ogre.Vector3(2.01, 10, 33))

        makeBridge(app, 'A Bridge', self.offset + ogre.Vector3(-2.01, 10, 11))
        makeBridge(app, 'A Bridge', self.offset + ogre.Vector3(-2.01, 10, 22))
        makeBridge(app, 'A Bridge', self.offset + ogre.Vector3(-2.01, 10, 33))
		      
        # makeBlockingWall(app, self.offset + ogre.Vector3(0, 5, -10), 1)
		# makeInnerWall(app, 'wall', self.offset + ogre.Vector3(5, 5, 0))	
        # makePlatform(app, 'A Platform', self.offset + ogre.Vector3(42, 5, 0))
        
        for i in range(0,4):
         makeRupee(app, 'A Rupee', self.offset + ogre.Vector3(42-2*i, 5-i, 5 + i))
        #makeRupee(app, 'A Rupee', self.offset + ogre.Vector3(41, 3, 6))
        
        makeBall(app, 'A Ball', self.offset + ogre.Vector3(41, 3, 14))
        
        makeBarbell(app, 'A Ball', self.offset + ogre.Vector3(39, 3, 20))
                
        self.makePlanks(app, -3, 0)
        self.makePlanks(app, -10, 0)
        #self.makePlanks(app, -17, 0)
        
            # plank = makePlank(app, 'Plank' + str(i), self.offset + ogre.Vector3(40-i*3, random.randrange(3),
                    # random.randrange(6) - 10), angle=5)
            # plank.body.sleep()
        	
        makePlatform(app, 'Platform7', self.offset + ogre.Vector3(0, 12, 40), sound = 'tone-5')
        makePlatform(app, 'Platform8', self.offset + ogre.Vector3(-5, 14, 42))
        makePlatform(app, 'Platform9', self.offset + ogre.Vector3(-10, 16, 42), sound = 'tone-6')
        makePlatform(app, 'Platform10', self.offset + ogre.Vector3(-15, 18, 42))
        makePlatform(app, 'Platform11', self.offset + ogre.Vector3(-20, 20, 38), sound = 'tone-6')
        makePlatform(app, 'Platform12', self.offset + ogre.Vector3(-25, 22, 35))
        makePlatform(app, 'Platform13', self.offset + ogre.Vector3(-28, 24, 32), sound = 'tone-7')
        
        makeGear(app, 'Spinning Gear', self.offset + ogre.Vector3(-30, 4, 15)) # +15z
        makeGear(app, 'Spinning Gear', self.offset + ogre.Vector3(-30, 12, -15))
        #makeBowlingPin(app, 'Spinning Gear', self.offset + ogre.Vector3(-30, 0, 15))
        
        makeBell(app, 'Bell', self.offset + ogre.Vector3(-30, 2, -15), sound = 'bell-3')
               	
        makeDonut(app, 'A Donut', self.offset + ogre.Vector3(-14.6, 7.5, 8.1)) # -7
        makeUpDownRamp(app, 'An UpDown Ramp', self.offset + ogre.Vector3(-8.9, 0, 5.7), 295, sound='perc-1') 
        makeUpDownRamp(app, 'An UpDown Ramp', self.offset + ogre.Vector3(-12.5, 2, 7.4), 295, sound='perc-2')
        
        #makeIcePlatform(app, 'Platform13', self.offset + ogre.Vector3(0,0,-40), material='IceChunk-', sound='bell-0')
        self.makeIceyPlatform(app, 'Platform13', self.offset + ogre.Vector3(0,0,-40), material='Plank-', sound='bell-0')
        
        # tilt = makeTiltRamp(app, 'A Tilt Ramp', self.offset + ogre.Vector3(-11, 0, -7), 290, sound='perc-1') 
        # size = ogre.Vector3(3.9803, 5.99281, 5.99701)       
        # mass = OgreOde.BoxMass (.5, size) # mass = OgreOde.BoxMass (0.5, ei.getSize())
        # mass.setDensity(0.5, size)           # mass.setDensity(0.5, ei.getSize())
        # tilt.body.setMass(mass)       
        
        # makeUpDownRamp(app, 'UpDown Ramp', self.offset + ogre.Vector3(-20, 13, 42), 90)

        makeMetalCrate(app, 'A Crate', self.offset + ogre.Vector3(18, 1, 18)) #, sound = 'bell-0')
        makeCrate(app, 'A Crate', self.offset + ogre.Vector3(14, 0, 20)) #, sound = 'bell-1')
        makeCrate(app, 'A Crate', self.offset + ogre.Vector3(22, 0, 24)) #, sound = 'bell-2')
        makeMetalCrate(app, 'A Crate', self.offset + ogre.Vector3(24, 1, 28)) #, sound = 'bell-3')
        #makeLeadCrate(app, 'A Crate', self.offset + ogre.Vector3(24, 1, 28)) #, sound = 'bell-3')        
        
        (leftdoor,rightdoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0, 0, 50))
        lock = makeLevelLock(app, self.offset)
       
        leftdoor.lock(app._world, lock)
        rightdoor.lock(app._world, lock)
                
        # key1 = makeUnlockKey(app, self.offset + ogre.Vector3(10, 4, -10), sound='key-0', lock = lock)
        # key over gear #2
        self.key1 = makeUnlockKey(app, self.offset + ogre.Vector3(-30, 18, -15), sound='key-0', lock=lock)
        
        self.key2 = makeUnlockKey(app, self.offset + ogre.Vector3(-28, 28, 32), sound='key-2', lock=lock)
        self.key1.fireCallback = self.spin1
        self.key2.fireCallback = self.spin2
        
    def makePlanks(self, app, z, angle):
        prev = None
        for i in range(0, 12):
            y = random.randrange(3)
            if prev != None and abs(prev - y) < 1:
                y = y + 1
            prev = y
            plank = makePlank(app, 'Plank' + str(i), self.offset + ogre.Vector3(40-i*3, y,
                    random.randrange(6) + z), angle=angle)
            plank.body.sleep()
        
    def makeIceyPlatform(self, app, name, offset, material='platform0-', sound=None):
        scn = app.sceneManager
        root = scn.getRootSceneNode()
        name = name + str(offset)
        
        c = Platform(name = name, materialName = material)
        containers[c.id] = c
        c.ent = scn.createEntity(name, 'IceChunk.mesh')
        c.node = root.createChildSceneNode(name)
        c.node.setPosition(offset)
        c.node.setScale(4,0.75,2)
        c.node.attachObject(c.ent)

        c.ent.setCastShadows(True)

        ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
        c.geom = ei.createStaticTriangleMesh(app._world, app._space)

        c.ent.setUserObject(c.geom)
        
        # set the initial material
        c.setMaterial()
        
        c.friction = .001

        if sound:
            c.sound = app.sounds[sound]
        else:
            c.sound = app.sounds['tone-%d' % random.randrange(8)]

        c.geom.setUserData(c.id)

        return c
        
    def spin1(self):
        #print "spin faster..."
        #print type(self)
        #print type(self.key1)
        #selt.setMaterial()
        #velocity = ogre.Vector3(random.random(), random.random(), random.random())
        velocity = self.key1.body.getAngularVelocity()
        velocity = ogre.Vector3(25,25,25)
        #velocity.normalise()
        # todo: add motor .. see makeRupee 
        self.key1.body.setAngularVelocity(velocity)
        # self.backgroundMusic = self.app.music['bg-5']
        #self.key1.body.setAngularVelocity(ogre.Vector3().NEGATIVE_UNIT_Y);
        
    def spin2(self):
        velocity = self.key1.body.getAngularVelocity()
        velocity = ogre.Vector3(25,25,25)
        self.key2.body.setAngularVelocity(velocity)

    def unload(self, app):
        pass
