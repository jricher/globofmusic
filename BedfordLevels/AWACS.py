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
            
        platform = makePlatform(app, 'Lab1 Platfrom', self.offset + ogre.Vector3(0,1,-20))
        crate = makeCrate(app, 'Lab1 Crate', self.offset + ogre.Vector3(0, 2, 0))
        crate.sound = app.sounds['bell-0']
    
        MetalCrate = makeMetalCrate(app, 'Lab1 Metal CRATE', self.offset + ogre.Vector3(0, 2, 0))



    def unload(self, app):
        pass



    


def makeIcePlatform(app, name, offset, angle=0, material = "Icy-", sound = None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'IceChunk.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    c.friction = 10

    return c
