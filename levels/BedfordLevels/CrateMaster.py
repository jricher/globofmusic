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
        print 'Loaded Level Lab1'
        self.backgroundMusic = app.music['bg-3']
        makePlatform(app, "An awesome platform",
                     self.offset + ogre.Vector3(0,1,-40),
                     sound='tone-5')
        makeCrate(app, "My Crate",
                  self.offset + ogre.Vector3(0,0,0))
        (leftdoor, rightdoor) = makeSwingingDoors(app, 
                          self.offset + ogre.Vector3(0,0,50))
        
        myLock = makeLevelLock(app, self.offset)
        
        leftdoor.lock(app._world, myLock)
        rightdoor.lock(app._world, myLock)
        
        key = makeUnlockKey(app, 
                            self.offset + ogre.Vector3(0,2,-20),
                            lock = myLock)
                            
        metalCrate = makeLeadCrate(app, "A Metal Crate", 
                                    self.offset + ogre.Vector3(0,2,-30))
        
        makeIcyPlatform(app, "Icy Platform",
                        self.offset + ogre.Vector3(0,1,-30),
                        material='Icy-')
                        
        makeTiltRamp(app, "Tilting Ramp", self.offset + ogre.Vector3(0,0,-80), angle=45)
        
       
        
        
        
        
        
        


    def unload(self, app):
        pass

        


def makeLeadCrate(app, name, offset):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    offset = offset + ogre.Vector3(0,3,0)
    
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

    c.node.setScale(2, 6, 2)

    ei = OgreOde.EntityInformer (c.ent,ogre.Matrix4.getScale(c.node.getScale()))
    c.body = ei.createSingleDynamicBox(0.15, app._world, app._space)
    c.body.setDamping(2,2)
    c.body.sleep() # put the crates to sleep until we need them
    c.geom = c.body.getGeometry(0)

    c.geom.setUserData(c.id)
    
    c.friction = 50
    
    return c        
        

def makeIcyPlatform(app, name, offset, material= None, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, "IceChunk.mesh")
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    
    #c.ent.setCastShadows(True)
    
    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)
    
    c.ent.setUserObject(c.geom)
    
    c.setMaterial()
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
    
    c.geom.setUserData(c.id)
    
    c.fricton = 10
    
    return c
    
         
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        