import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *

class Level(BaseLevel):
    def __init__(self, levelId):
        BaseLevel.__init__(self, levelId)

    def load(self, app):
        print 'Loaded Domino Rally Level'
        self.backgroundMusic = app.music['bg-4']
        makeGear(app, "A Gear", self.offset + ogre.Vector3(-10,0,0))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(-4,3,-30))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(0,3,-30))
        makeIcePlatform(app, "Icy2", self.offset + ogre.Vector3(4,3,-30))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(-4,3,-34))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(0,3,-34))
        makeIcePlatform(app, "Icy2", self.offset + ogre.Vector3(4,3,-34))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(-4,3,-38))
        makeIcePlatform(app, "Icy", self.offset + ogre.Vector3(0,3,-38))
        makeIcePlatform(app, "Icy2", self.offset + ogre.Vector3(4,3,-38))
        for i in range(-13, -47, -7):
            makeInnerWall(app, "RightWall", self.offset + ogre.Vector3(i,0,-16.5))
            makeInnerWall(app, "LeftWall", self.offset + ogre.Vector3(i,0,16.5))
        
        
        makeInnerWall(app, "OverGear", self.offset + ogre.Vector3(-9,4,0), angle=90)
        makeInnerWall(app, "OverGear", self.offset + ogre.Vector3(-10,4,6.05), angle=90)
        makeInnerWall(app, "OverGear", self.offset + ogre.Vector3(-10,4,12.1), angle=90)
        makeInnerWall(app, "OverGear", self.offset + ogre.Vector3(-10,4,-6.05), angle=90)
        makeInnerWall(app, "OverGear", self.offset + ogre.Vector3(-10,4,-12.1), angle=90)
        
        
        lock = makeLevelLock(app, self.offset)

        c = makeUnlockKey(app, self.offset + ogre.Vector3(-40, 2, 0), sound='key-1')
        c.quant = 8
        c.key = lock
        lock.sources.append(c)
        
        c = makeUnlockKey(app, self.offset + ogre.Vector3(8, 15, 40), sound='key-1')
        c.quant = 8
        c.key = lock
        lock.sources.append(c)
    
        (leftDoor, rightDoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0, 0, 50))
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)
        
        
                
        #NW corner
        for i in range(0,14,1):
            makeDomino(app, "D_NWStair", self.offset + ogre.Vector3(i+28,10 - (i/(14.0))*10,40-i), angle = -45)
            
        #Lead in
        makeDomino(app, "D_NWStair_013", self.offset + ogre.Vector3(42,0.2,25), angle=-30)
        makeDomino(app, "D_NWStair_014", self.offset + ogre.Vector3(43,0.2,24), angle=-20)
        makeDomino(app, "D_NWStair_015", self.offset + ogre.Vector3(43.5, 0.2, 23), angle=-10)
        
        #Leadout
        makeDomino(app, "D_NWStair_T01", self.offset + ogre.Vector3(26, 10.5, 40), angle=-60)
        makeDomino(app, "D_NWStair_T02", self.offset + ogre.Vector3(24, 11.5, 40), angle=-70)
        makeDomino(app, "D_NWStair_T03", self.offset + ogre.Vector3(22, 12.5, 40), angle=-80)
        
#        #Lead in
#        makeDomino(app, "D_SWStair_013", self.offset + ogre.Vector3(-42,0,25), angle=30)
#        makeDomino(app, "D_SWStair_014", self.offset + ogre.Vector3(-43,0,24), angle=20)
#        makeDomino(app, "D_SWStair_015", self.offset + ogre.Vector3(-44,0,22), angle=10)
#        
#        #Leadout
#        makeDomino(app,"D_SWStair_T01", self.offset + ogre.Vector3(-26, 10, 40), angle=60)
#        makeDomino(app,"D_SWStair_T02", self.offset + ogre.Vector3(-24, 11, 40), angle=70)
#        makeDomino(app,"D_SWStair_T03", self.offset + ogre.Vector3(-22, 12, 40), angle=80)


        for i in range(-21,23,2):
            #North Line
            makeDomino(app, "D_NorthLine", self.offset + ogre.Vector3(44, 0.2, i))
           
                
        #Over the exit dominoes
        floor = 16
        for i in range(11,20,2):
            makeDomino(app, "D_Nexit", self.offset + ogre.Vector3(i, 14, 40), angle = 90)
       
        def sparks(level):
            if ("sparks" not in particles):
                scn = app.sceneManager
                root = scn.getRootSceneNode()
                c = Container("sparks")
                c.particleSystem = scn.createParticleSystem('Sparks', 'sparks')
                c.particleSystem.setKeepParticlesInLocalSpace(True)
                
                c.node = root.createChildSceneNode("sparks")
                #c.node = self.player.node.createChildSceneNode("Snow")  #for extra kicks, attach to the player
                #c.node.setPosition(0, 0, 375)
                print "Sparks: ", level.cameraAnchor.x, level.cameraAnchor.y, level.cameraAnchor.z
                c.node.setPosition(level.cameraAnchor + ogre.Vector3(0,0,0))
                
                c.node.attachObject(c.particleSystem)
                
                particles["sparks"] = c
        self.startLevelCallback = sparks 
        
        def stopSparks(level):
            if ("sparks" in particles):
                scn = app.sceneManager
                root = scn.getRootSceneNode()
                c = particles["sparks"]
                scn.destroyParticleSystem(c.particleSystem)
                del c.particleSystem
                scn.destroySceneNode(c.node.getName())
                del particles["sparks"]
        self.stopLevelCallback = stopSparks
        
        
        
        

    def unload(self, app):
        pass
        
    
def makeIcePlatform(app, name, offset, material="IcePlatform-", sound=None):
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
    c.friction = 10
    return c
    

















