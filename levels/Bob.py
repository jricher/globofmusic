import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *

class Level(BaseLevel):
    def __init__(self, levelId):
        BaseLevel.__init__(self, levelId)
##
##
##    def __del__(self):
##        BaseLevel.__del__(self)
##

    def load(self, app):
        print 'Loaded Level Bob'

        self.backgroundMusic = app.music['bg-3']

        crate = makeCrate(app, 'Bob Crate', self.offset + ogre.Vector3(0, 2, 0))
        crate.sound = app.sounds['bell-lo-0']

        platform = makeIcePlatform(app, 'Bob Platform', self.offset + ogre.Vector3(10, 1, 0))
        platform.sound = app.sounds['key-1']
        

    def unload(self, app):
        pass


def makeIcePlatform(app, name, offset, material = None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'IceChunk.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    # set the initial material
    c.setMaterial()

    c.geom.setUserData(c.id)

    c.friction = 10

    return c

    
