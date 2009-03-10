import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS
import math

from Container import *
from Catalog import *
import random

class Level(BaseLevel):
#    def __init__(self, levelId):
#        BaseLevel.__init__(self, levelId)
##
##
##    def __del__(self):
##        BaseLevel.__del__(self)
##


    def load(self, app):
        self.backgroundMusic = app.music['bg-5']

        makePlatform(app,'low',
                     self.offset + ogre.Vector3(-20,3,20))
        makePlatform(app,'medium',
                     self.offset + ogre.Vector3(-20,6,28))
        makePlatform(app,'high',
                     self.offset + ogre.Vector3(-20,9,36))

        #slippery
        for z in range(-38,-14,4):
            for x in range (-28,0,4):
                icy = makeIcyPlatform(app,'icy1',self.offset + ogre.Vector3(x,0,z))
                icy.restartable = True

        #bowling
        startRowX = -20
        startRowZ = -27
        for row in [0,1,2]:
            rowX = startRowX - (5*row)
            rowZ = startRowZ - (2.5*row)
            for pin in range(0,row+1):
                pinZ = rowZ + (5*pin)
                bp = makeBowlingPin(app,'pin'+str(row)+str(pin),
                               self.offset + ogre.Vector3(rowX,.5,pinZ))
                bp.body.sleep()

        crate = makeCrate(app,'Another Crate',self.offset + ogre.Vector3(-20,9,28))
        crate.sound = app.sounds['perc-4']

        makeBridge(app,'Bridge to Nowhere',
                   self.offset + ogre.Vector3(-20,4,10))

        makeIcyPlatform(app,'Icy',
                            self.offset + ogre.Vector3(-20,2,-4),sound='bell-3')
        makeTiltingPlatform(app,'Tilt',
                            self.offset + ogre.Vector3(-28,2,7),sound='bell-2')
        makeTiltingPlatform(app,'Tilt',
                            self.offset + ogre.Vector3(-13,2,7),sound='bell-2')

        doors = makeSwingingDoors(app,self.offset + ogre.Vector3(0,0,50))

        lock = makeLevelLock(app,self.offset)
        doors[0].lock(app._world,lock)
        doors[1].lock(app._world,lock)
        key1 = makeUnlockKey(app,self.offset + ogre.Vector3(-20,11,36),lock=lock)

        key2 = makeUnlockKey(app,self.offset + ogre.Vector3(-20,9,-4),lock=lock)
        key2.sound = app.sounds['key-0']

        for a in range (0,355,30):
            x = math.cos(math.radians(a)) * 7
            z = math.sin(math.radians(a)) * 7
            makeLeadCrate(app,'crate'+str(a),self.offset + ogre.Vector3(-20+x,0,-4+z))
            makeLeadCrate(app,'crate'+str(a),self.offset + ogre.Vector3(-20+x,2.5,-4+z))

        #snake
        snakeStartZ = 5
        startBall = makeBall(app,'startBall',self.offset + ogre.Vector3(0,5,snakeStartZ))
        prev = startBall
        for z in range (snakeStartZ+6.1,snakeStartZ+(6.1*6),6.1):
            ball = makeBall(app, 'ball'+str(z), self.offset + ogre.Vector3(0,5,z))
            ball.joint = OgreOde.BallJoint(app._world)
            ball.joint.attach(prev.body, ball.body)
            ball.joint.setAnchor((ball.body.getPosition() + prev.body.getPosition()) / 2)
            prev = ball

        #
        # Puzzle 1: Climb the platforms
        #
        # Make Platforms
        # Sounds to use: bell-3, 
        PlatformHeight = 3
        PlatformSpacing = 6
        PlatformOffset = self.offset + ogre.Vector3(35,1,-5)
        PlatformA = makePlatform(app, 'Platform A', PlatformOffset + ogre.Vector3(0,PlatformHeight,-2*PlatformSpacing),sound="key-2")
        PlatformB = makePlatform(app, 'Platform B', PlatformOffset + ogre.Vector3(0,2*PlatformHeight,-PlatformSpacing),sound="key-2")
        PlatformC = makePlatform(app, 'Platform C', PlatformOffset + ogre.Vector3(0,3*PlatformHeight,0),sound="key-2")
        PlatformD = makePlatform(app, 'Platform D', PlatformOffset + ogre.Vector3(0,4*PlatformHeight,PlatformSpacing),sound="key-2")
        PlatformE = makeIcyPlatform(app, 'Platform E', PlatformOffset + ogre.Vector3(0,5*PlatformHeight,2*PlatformSpacing),sound="key-1")
        PlatformKeyLoc = PlatformOffset + ogre.Vector3(0,4*PlatformHeight,3*PlatformSpacing)
        Level1Key1 = makeUnlockKey(app, PlatformKeyLoc, lock=lock, sound='bell-4')
        # Make Crates
        makeCrate(app, 'Crate A', PlatformOffset + ogre.Vector3(40-random.randrange(80),40-random.randrange(80),random.randrange(40)))
        makeMetalCrate(app, 'Metal Crate A', PlatformOffset + ogre.Vector3(0,0,-3*PlatformSpacing))
        makeLeadCrate(app, 'Lead Crate A', PlatformOffset + ogre.Vector3(0,2,-3*PlatformSpacing))
        makeAluminumCrate(app, 'Aluminum Crate A', PlatformOffset + ogre.Vector3(0,4,-3*PlatformSpacing))
        #
        # Puzzle 2: Make a "MyTiltRamp" (Wedge)
        #
        WedgeSep = -5
        WedgeOffset = self.offset + ogre.Vector3(15,0,0)
        Wedge1 = makeMyTiltRamp(app, "Wedge1", WedgeOffset + ogre.Vector3(-WedgeSep, 0, 0), 90)
        Wedge2 = makeMyTiltRamp(app, "Wedge2", WedgeOffset + ogre.Vector3( WedgeSep, 0, 0), 270)
        Wedge3 = makeMyTiltRamp(app, "Wedge3", WedgeOffset + ogre.Vector3( 0, 0,  WedgeSep), 180)
        Wedge4 = makeMyTiltRamp(app, "Wedge4", WedgeOffset + ogre.Vector3( 0, 0, -WedgeSep), 0)
        Ball = makeBall(app,"Ball",WedgeOffset + ogre.Vector3(0, 10, WedgeSep))
        WedgeKeyLoc = WedgeOffset + ogre.Vector3(0,2,0)
        WedgeKey    = makeUnlockKey(app, WedgeKeyLoc, lock=lock, sound='bell-4')
        # Loc_Ramp1 = RampOffset + ogre.Vector3(0,0,10)
        # Loc_Ramp2 = RampOffset + ogre.Vector3(0,0,-10)
        # Ramp1 = makeMyTiltRamp(app, "Ramp1", Loc_Ramp1, angle=0)
        # Ramp2 = makeMyTiltRamp(app, "Ramp2", Loc_Ramp2, angle=180)
        # Loc_Ramp = ogre.Vector3(0,0,3.0*PlatformSpacing)
        # Ramp = makeTiltRamp(app, "The Ramp", self.offset+Loc_Ramp, angle=90) #, material = 'platform0-', sound='runup')
          # makeStraightRamp
          # makeOnOffRamp
          # makeUpDownRamp
          # makeTiltRamp
          # makeCornerRamp        
        #
        # Puzzle 3: Climb the Ladder
        #
        LadderOffset = self.offset + ogre.Vector3(25,0,-25)
        Ladder = makeLadder(app,"Ladder",LadderOffset + ogre.Vector3(0,10,0))
        LadderKeyLoc = LadderOffset + ogre.Vector3(0,11.5,4)
        LadderKey = makeUnlockKey(app, LadderKeyLoc, lock=lock, sound='bell-4')
        #
        print 'Loaded ExpertLevel'


        def unload(self, app):
            pass



def makeLeadCrate(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    offset = offset + ogre.Vector3(0,1.25,0)

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
    c.body = ei.createSingleDynamicBox(50.0, app._world, app._space)
    c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.friction = 500

    c.geom.setUserData(c.id)

    return c


def makeIcyPlatform(app, name, offset, material='DiscoIcy-', sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    c = Platform(name=name, materialName=material)
    containers[c.id] = c
    c.ent = scn.createEntity(name,'IceChunk.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform  ())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    # set the initial material
    c.setMaterial()

    # Change the friction
    c.friction = 10

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
                             

    c.geom.setUserData(c.id)

    return c

def makeLadder(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    start = makePlank(app, name+'start', offset + ogre.Vector3(0, 0, -5))
    #l = OgreOde.FixedJoint(app._world)
    #l.attach(start.body)

    #TD start.anchor = OgreOde.HingeJoint(app._world)
    #TD start.anchor.attach(start.body)
    #TD start.anchor.setAxis(ogre.Vector3().UNIT_X)
    #TD start.anchor.setAnchor(offset + ogre.Vector3(0, 0, -5.5))

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

def makeMyTiltRamp(app, name, offset, angle=0, sound=None):
    ramp = makeTiltRamp(app, name, offset, angle, sound)
    # del ramp.joint
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    ramp.body.setOrientation(quat)
    return ramp

def makeAluminumCrate(app, name, offset):
    crate = makeMetalCrate(app, name, offset)
    newmass = OgreOde.BoxMass (1.0, crate.geom.getSize()) 
    newmass.setDensity(0.5, crate.geom.getSize())
    crate.body.setMass(newmass)
    return crate
