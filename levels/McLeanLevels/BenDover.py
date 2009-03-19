import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):

    def load(self, app):
        print 'Loaded Blank Level'

        self.backgroundMusic = app.music['bg-4']

        #makePlatform(app,"plat1", self.offset + ogre.Vector3(0,2,-30), material = "IcePlatform-")
        #makePlatform(app,"plat2", self.offset + ogre.Vector3(-4,4,-25), material = "IcePlatform-")
        #makePlatform(app,"plat3", self.offset + ogre.Vector3(4,4,-25), material = "IcePlatform-")
        #makePlatform(app,"plat4", self.offset + ogre.Vector3(8,6,-20), material = "IcePlatform-")
        #makePlatform(app,"plat5", self.offset + ogre.Vector3(-8,6,-20), material = "IcePlatform-")
        #makePlatform(app,"plat6", self.offset + ogre.Vector3(14,6,-20), material = "IcePlatform-")
        #makePlatform(app,"plat7", self.offset + ogre.Vector3(-14,6,-20), material = "IcePlatform-")
        #makePlatform(app,"plat8", self.offset + ogre.Vector3(18,4,-15), material = "IcePlatform-")
        #makePlatform(app,"plat9", self.offset + ogre.Vector3(-18,4,-15), material = "IcePlatform-")     
        #makePlatform(app,"plat10", self.offset + ogre.Vector3(-4,4,-15))
        #makePlatform(app,"plat11", self.offset + ogre.Vector3(4,4,-15))
        #makePlatform(app,"plat20", self.offset + ogre.Vector3(0,2,-10))
        #makeCrate(app,"crat1", self.offset + ogre.Vector3(0,20,-10))
        makeBridge(app, "Bridge1", self.offset + ogre.Vector3(34,6,-9))
        makeBridge(app, "Bridge2", self.offset + ogre.Vector3(34,6,6))
        makeBridge(app, "Bridge3", self.offset + ogre.Vector3(34,6,21))
        
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,-27),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,-20),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,-13),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,-6),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,1),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,8),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,15),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,22),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,0,29),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,-27),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,-20),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,-13),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,-6),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,1),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,8),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,15),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,22),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(31,16,29),angle=90)


        doors1 = makeSwingingDoors(app, self.offset + ogre.Vector3(0,0,50))
        leftDoor1 = doors1[0]
        rightDoor1 = doors1[1]

        lock1 = makeLevelLock(app,self.offset)

        key1 = makeUnlockKey(app,self.offset + ogre.Vector3(34,9,30))
        key1.key = lock1
        lock1.sources.append(key1)
        leftDoor1.lock(app._world,lock1)
        rightDoor1.lock(app._world,lock1)



        makeInnerWall(app, "wall1", self.offset + ogre.Vector3(-5,0,-45), 0)
        makeInnerWall(app, "wall2", self.offset + ogre.Vector3(5,0,-45), 0)
        makeInnerWall(app, "wall3", self.offset + ogre.Vector3(3,0,-41), 90)
        makeInnerWall(app, "wall4", self.offset + ogre.Vector3(3,0,-34), 90)
        makeInnerWall(app, "wall5", self.offset + ogre.Vector3(-1,0,-31), 0)
        makeInnerWall(app, "wall6", self.offset + ogre.Vector3(-8,0,-31), 0)
        makeInnerWall(app, "wall7", self.offset + ogre.Vector3(-11,0,-35), 90)
        makeInnerWall(app, "wall7", self.offset + ogre.Vector3(-11,16,-35), 90)
        makeInnerWall(app, "wall8", self.offset + ogre.Vector3(-11,0,-42), 90)
        makeInnerWall(app, "wall9", self.offset + ogre.Vector3(-11,16,-42), 90)
        makeInnerWall(app, "wall11", self.offset + ogre.Vector3(7,0,-31), 0)
        makeInnerWall(app, "wall10", self.offset + ogre.Vector3(14,0,-31), 0)
        makeInnerWall(app, "wall10", self.offset + ogre.Vector3(21,0,-31), 0)
        makeInnerWall(app, "wall10", self.offset + ogre.Vector3(28,0,-31), 0)
        
       
        
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(0,0,-38),angle=0)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(0,2,-34),angle=0)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(-4,2,-34),angle=270)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(-8,4,-34),angle=270)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(-8,4,-38),angle=180)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(-8,6,-42),angle=-180)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(-4,6,-42),angle=90)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(0,8,-42),angle=-270)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(0,8,-38),angle=0)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(0,10,-34),angle=0)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(-4,10,-34),angle=270)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(-8,12,-34),angle=270)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(-8,12,-38),angle=180)
        makeCornerRamp(app, "ramp", self.offset + ogre.Vector3(-8,14,-42),angle=-180)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(-4,14,-42),angle=90)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(0,14,-42),angle=270)

        makeTiltRamp(app, "tilt", self.offset + ogre.Vector3(7,8,-41), angle=-90)
        makeTiltRamp(app, "tilt", self.offset + ogre.Vector3(7,8,-35), angle=-90)
        makeTiltRamp(app, "tilt", self.offset + ogre.Vector3(13,2,-41), angle=-90)
        makeTiltRamp(app, "tilt", self.offset + ogre.Vector3(13,2,-35), angle=-90)

        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(18,1,-43))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(18,1,-39))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(18,1,-35))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(23,1,-43))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(23,1,-39))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(23,1,-35))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(27,1,-39))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(27,1,-35))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(31,1,-35))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-31))
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(34,1,-27),angle=0)
        makeUpDownRamp(app, "ramp", self.offset + ogre.Vector3(34,3,-23),angle=0)
        makeStraightRamp(app, "ramp", self.offset + ogre.Vector3(34,5,-20),angle=0)
        makeStraightRamp(app, "ramp", self.offset + ogre.Vector3(34,5,-18),angle=0)
        makeStraightRamp(app, "ramp", self.offset + ogre.Vector3(34,5,-16),angle=0)


        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-25))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-21))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-17))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-13))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-9))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-5))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,-1))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,3))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,7))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,11))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,15))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,19))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,23))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,27))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(34,1,31))

        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-25))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-21))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-17))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-13))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-9))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-5))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,-1))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,3))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,7))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,11))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,15))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,19))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,23))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(38,1,27))

        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,-21))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,-17))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,-13))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,-9))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,-5))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,-1))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,3))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,7))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,11))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,15))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,19))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(42,1,23))

        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,-15),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,-8),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,-1),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,6),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,13),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,20),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,27),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,34),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,0,41),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,-15),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,-8),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,-1),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,6),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,13),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,20),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,27),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,34),angle=90)
        makeInnerWall(app, "wall", self.offset + ogre.Vector3(5,16,41),angle=90)        

 #       x = -41
 #       y = 0
 #       max_x = 10
 #       max_y = 10
 

#        while x < max_x
#            while y < max_y
#                    makeBowlingPin(app, "pin", self.offset + ogre.Vector3(5,0,41))
            
    def unload(self, app):
        pass


def makeIcePlatform(app, name, offset, material = "IcePlatform-", sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)

    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "IceChunk.mesh")
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

    c.friction = 1
    
    return c
    
    
    
