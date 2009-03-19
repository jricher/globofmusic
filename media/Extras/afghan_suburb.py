import ogre.renderer.OGRE as ogre
import ogre.physics.OgreOde as OgreOde
import ogre.sound.OgreAL as OgreAL
import ogre.io.OIS as OIS

from Container import *
from Catalog import *



class Level(BaseLevel):

    def __init__(self, levelId):
        BaseLevel.__init__(self, levelId)
        self.wide = True
        # Add non-standard sound

    def createCrate(self, app, x, z):
        cratesize = 2.4
        c = makeMetalCrate(app, 'crate', self.offset + ogre.Vector3(x*cratesize,0,z*cratesize-37))
        size = c.geom.getSize()
        mass = OgreOde.BoxMass (10.5, size)
        mass.setDensity(0.10, size)
        c.body.setMass(mass)
        c.friction = 100

    def load(self, app):
        print 'Loading afghan_suburb'
        sm = app.soundManager
        newmusic = sm.createSound('bg-9','afghan_lvl_music.wav',True)
        newmusic.setRelativeToListener(True)
        app.music['bg-9'] = newmusic
        self.backgroundMusic = app.music['bg-9']
        sound = sm.createSound('afghan-bump','bad.wav',False);
        sound.setRelativeToListener(True)
        app.sounds['afghan-bump'] = sound
        sound = sm.createSound('afghan-bumpkey','afghan_bumpkey.wav',False);
        sound.setRelativeToListener(True)
        app.sounds['afghan-bumpkey'] = sound
        sound = sm.createSound('afghan-findkey','afghan-anthem.wav',False);
        sound.setRelativeToListener(True)
        app.sounds['afghan-findkey'] = sound
        sound = sm.createSound('afghan-elder','afghan_advice.wav',False);
        sound.setRelativeToListener(True)
        app.sounds['afghan-elder'] = sound
        
        
        random.seed()

        #Make crates near entrance to slow person down
        # (to allow for the music to catch up)
        num = 10
        for z in range(0,2):
            for i in range(1,num):
                self.createCrate(app,i-1,z)
                self.createCrate(app,-i,z)
                pass
                
        # City extents
        spacing = 20
        xmin = -5
        xmax = 6
        zmin = -1
        zmax = 2
        noBldgProb = 0.1
        noTreeProb = 0.8
        treeYOffset = 3.7

        # Tree uses a box for its collision, and so it needs the object's
        # pivot point to be at its center - not its base.
        for x in range(xmin,xmax+1):
            for z in range (zmin,zmax+1):
                if random.random() > noTreeProb:
                    angle = random.randrange(0,360)
                    makeTree(app,'tree',self.offset+ogre.Vector3(x*spacing-10,treeYOffset,z*spacing-10),angle)
        
        keyXIndex = random.randrange(xmin,xmax)
        keyZIndex = random.randrange(zmin,zmax)
        keyX = spacing*keyXIndex
        keyZ = spacing*keyZIndex
        madeElder = False
        # Comment this out in final level version
        print "key location: " + str(keyXIndex) + "," + str(keyZIndex)
        
        for x in range(xmin,xmax):
            for z in range (zmin,zmax):
                angle = random.randrange(0,4)*90
                xoffset = random.random()*2 - 1
                zoffset = random.random()*2 - 1
                if (x != keyXIndex or z != keyZIndex):
                    if random.random() > noBldgProb:
                        makeBuilding(app, 'bldg', self.offset + ogre.Vector3(x*spacing+xoffset,0,z*spacing+zoffset),angle,sound='afghan-bump')
                    elif not madeElder:
                        madeElder = True
                        # Make the elder who has the clue
                        makeElder(app, 'elder', self.offset + ogre.Vector3(x*spacing,4.7,z*spacing),angle,'afghan-elder')
                else: # This is where the key is
                    makeBuilding(app, 'bldg', self.offset + ogre.Vector3(x*spacing+xoffset,0,z*spacing+zoffset),angle,sound='afghan-bumpkey')

        # Locks
        lock = makeLevelLock(app, self.offset)
        c = makeUnlockKey(app, self.offset + ogre.Vector3(keyX, 2, keyZ), sound='afghan-findkey')
        c.quant = 0
        c.key = lock
        lock.sources.append(c)
        
        (leftDoor, rightDoor) = makeSwingingDoors(app, self.offset + ogre.Vector3(0, 0, 50))
        leftDoor.lock(app._world, lock)
        rightDoor.lock(app._world, lock)


        
    def unload(self, app):
        pass

# New Container classes

class Building(Fireable):
    def __init__(self, name = None, materialName = None, restartable = False, key = None):
        Fireable.__init__(self, name, materialName, restartable, key)

    def collideWith(self, other, contact, normal, lm):
        # Relax condition about being armed - just play sound again
        if (isinstance(other, Player) or isinstance(other, Fireable)):
            if self.sound and not lm.mm.isFireKeyQueued(self.id):
                lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id, True)
        return False

class RepeatingSound(Container):
    def __init__(self, name = None):
        Container.__init__(self,name)

    def collideWith(self, other, contact, normal, lm):
        if isinstance(other, Player):
            if self.sound and not lm.mm.isFireKeyQueued(self.id):
                lm.mm.addQueuedSound(self.sound, self.quant, self.rest, self.id, True)
        return False

# New make functions

def makeBuilding(app, name, offset, angle = 0, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    #c = Container(name = name)
    #c = Platform(name = name, materialName = 'afghanbldgmat1-')
    c = Building(name = name, materialName = 'afghanbldgmat1-')
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'afghan_building.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.setScale(random.random()*0.4+0.8,random.random()*0.4+0.8,random.random()*0.4+0.8)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createStaticTriangleMesh(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    # set the initial material
    #c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    # Make this happen as soon as possible
    c.quant = 0

    c.geom.setUserData(c.id)

    return c

def makeTree(app, name, offset, angle = 0, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    c = Container(name = name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'afghan_tree.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    c.node.setScale(random.random()*0.4+0.8,1,random.random()*0.4+0.8)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createSingleStaticBox(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    # set the initial material
    #c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]
                             

    c.geom.setUserData(c.id)

    return c

def makeElder(app, name, offset, angle = 0, sound=None):
    scn = app.sceneManager
    root = scn.getRootSceneNode()
    name = name + str(offset)
    
    #c = Container(name = name)
    c = RepeatingSound(name = name)
    containers[c.id] = c
    c.ent = scn.createEntity(name, 'afghan_elder.mesh')
    c.node = root.createChildSceneNode(name)
    c.node.setPosition(offset)
    quat = ogre.Quaternion(ogre.Degree(angle),ogre.Vector3().UNIT_Y)
    c.node.setOrientation(quat)
    c.node.attachObject(c.ent)

    c.ent.setCastShadows(True)

    ei = OgreOde.EntityInformer(c.ent, c.node._getFullTransform())
    c.geom = ei.createSingleStaticBox(app._world, app._space)

    c.ent.setUserObject(c.geom)
    
    # set the initial material
    #c.setMaterial()

    if sound:
        c.sound = app.sounds[sound]
    else:
        c.sound = app.sounds['tone-%d' % random.randrange(8)]

    # Make this happen as soon as possible
    c.quant = 0

    c.geom.setUserData(c.id)

    return c
