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

        #platform = makeIcePlatform(app, 'Bob Platform', self.offset + ogre.Vector3(10, 1, 0))
        #platform.sound = app.sounds['key-1']

        makeOnOffRamp(app, 'onoff', self.offset + ogre.Vector3(10, 0, -20))
        makeStraightRamp(app, 's1', self.offset + ogre.Vector3(10, 0, -17))
        makeStraightRamp(app, 's2', self.offset + ogre.Vector3(10, 0, -15))
        makeUpDownRamp(app, 'updown0', self.offset + ogre.Vector3(10, 0, -12))
        makeUpDownRamp(app, 'updown1', self.offset + ogre.Vector3(10, 2, -8))
        makeUpDownRamp(app, 'updown2', self.offset + ogre.Vector3(10, 4, -4))
        makeUpDownRamp(app, 'updown3', self.offset + ogre.Vector3(10, 6, 0))
        makeCornerRamp(app, 'corner', self.offset + ogre.Vector3(10, 8, 4))
        

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

    
def makeCornerRamp(app, name, offset, material = 'platform0-'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'CornerRamp.mesh')
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

    return c

    
def makeStraightRamp(app, name, offset, material = 'platform0-'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'StraightRamp.mesh')
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

    return c

    
def makeUpDownRamp(app, name, offset, material = 'platform0-'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'UpDownRamp.mesh')
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

    return c

    
def makeOnOffRamp(app, name, offset, material = 'platform0-'):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    
    c = Platform(name = name, materialName = material)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'OnOffRamp.mesh')
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

    return c

    
