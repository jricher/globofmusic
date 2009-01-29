##
## Glob of Music
## Copyright 2007
##  Justin Richer
##  Nathan Rackliffe
##  Paul Laidler
##  Rob Whalen
##


#
# Music manager plays sounds on beat
#

class MusicManager():
    def __init__(self, tempo = 90):
        self.queue = []       # queue of sounds to play, in order; contains None for rests
        self.loop = []        # list of sounds to play during a loop
        self.stops = []       # list of sounds to be stopped
        self.fading = []      # list of sounds that are currently fading out
        self.fireKeys = []    # list of ids for sounds that got fired from the queue (to be read and cleared externally)
        self.playing  = []    # list of ids for sounds that are currently playing, fired from the queue 
        self.finishKeys = []  # list of ids for sounds that ended after being fired from the queue (Also to be read and cleared externally)
        self.silentCount = {} # dictionary of id->count for sounds that should not be re-queued
        self.setTempo(tempo)

    def __del__(self):
        del self.queue
        del self.loop
        del self.stops
        del self.fading
        del self.fireKeys
        del self.silentCount[:]

    def setTempo(self, tempo,
                 bars = 4,            # number of consecutive bars (for loop processing)
                 barSize = 4,         # number of major beats per bar (4/4 time == 4 beats per measure)
                 beatSize = 4,        # number of minor beats per major beat (1/4 of a 1/4 note == 1/16 note quantization)
                 ):

        self.clearQueue()
        
        self.tempo = float(tempo)     # number of (major) beats per minute

        self.bars = bars
        self.barSize = barSize     
        self.beatSize = beatSize

        self.totalBeats = int(self.beatSize * self.barSize * self.bars) # number of minor beats total
        
        self.timePerBeat = 60.0 / float(self.beatSize) / self.tempo # number of seconds for each beat

        # start us off at -1 because we somehow miss beat 0 otherwise
        self.currentBeat = -1

        # buffer of sounds to play per beat
        self.loop = [[] for x in range(self.totalBeats)]
        self.stops = [[] for x in range(self.totalBeats)]

        self.timer = 0.0

        print 'Total resolution:', str(self.totalBeats)
        print 'MS per beat:', str(self.timePerBeat * 1000)

    def advance(self, time):
        #print time
        self.timer += time
        newBeat = False
        while self.timer >= self.timePerBeat:
            if newBeat:
                # we already had a new beat this cycle, so we must be skipping it
                print 'skipping beat', self.currentBeat
            self.timer -= self.timePerBeat
            self.currentBeat = int((self.currentBeat + 1) % self.totalBeats)
            newBeat = True

        # fades out any sounds that need to be stopped
        for sound in self.fading:
            if sound.isPlaying():
                if sound.getGain() > (time / 2):
                    # TODO: this fades after 2 seconds, should be X beats instead...
                    sound.setGain(sound.getGain() - (time / 2))
                    #print 'fading %s to %f' % (sound.getFileName(), sound.getGain())
                else:
                    print 'stopping %s' % sound.getFileName()
                    sound.stop()
                    sound.setGain(1.0)
            else:
                self.fading.remove(sound)

        if newBeat:
            #print '+++', self.currentBeat
            #print 'overage (ms)', str(self.timer * 1000)
            
            # play sounds for the current beat
            if self.loop[self.currentBeat]:
                for sound in self.loop[self.currentBeat]:
                    if sound.isPlaying():
                        #print 'restart', sound.getFileName()
                        sound.stop() # restart if needed
                    print 'loop', sound.getFileName()
                    sound.play()

            # set up any 'stopping' sounds to be gradually faded out
            if self.stops[self.currentBeat]:
                for sound in self.stops[self.currentBeat]:
                    if sound.isPlaying():
                        self.stops[self.currentBeat].remove(sound)
                        self.fading.append(sound)
            
            #Check to see if any of the sounds started from the quantization queue have finished (if they had id's associated with them)
            if self.playing:
                # Python speed optimization using list comprehension

                pl = [p for p in self.playing if p[0].isPlaying()]

                for p in pl:
                    self.playing.remove(p)
                    self.finishKeys.append(p[1])
                
                #for s in self.playing:
                #    (sound, key) = s
                #    if sound.isPlaying():
                #        pass
                #    else:
                #        self.playing.remove(s)
                #        self.finishKeys.append(key)
                
            # play any sounds waiting on the quantization queue
            if self.queue:
                #print self.queue
                s = self.queue.pop(0)
                # s may be:
                #   None           meaning a rest
                #   Sound          meaning a sound to play
                #   (Sound, int)   meaning a sound and a container id
                if s:

                    if type(s) is tuple:
                        (s, key) = s
                        self.fireKeys.append(key)
                        self.playing.append((s,key))
                    
                    if s.isPlaying():
                        #print 'restarting', s.getFileName()
                        s.stop()
                    #print 'queue', s.getFileName()
                    s.play()
                #else:
                    #print 'queue', 'rest'

            if self.silentCount:
                unsilence = []
                for id in self.silentCount:
                    self.silentCount[id] -= 1
                    if self.silentCount[id] <= 0:
                        unsilence.append(id)
                for u in unsilence:
                    del self.silentCount[u]
                #print self.silentCount
                    
                    

        
    def addLoopedSound(self, sound, beat):
        '''
        Add a new sound to be played indefinitely on a particular beat
        '''
        beat = beat % self.totalBeats
        if sound not in self.loop[beat]:
            self.loop[beat].append(sound)
            # remove this sound from the stops on that beat
            if sound in self.stops[beat]:
                self.stops[beat].remove(sound)

    def stopSound(self, sound, beat):
        '''
        Stop a sound on the given beat
        '''
        beat = beat % self.totalBeats
        if sound not in self.stops[beat]:
            self.stops[beat].append(sound)

            # remove it from the loop on that beat
            if sound in self.loop[beat]:
                self.loop[beat].remove(sound)

        # clean the sound out of the queue if it's there
        while sound in self.queue:
            self.queue[self.queue.index(sound)] = None


        if self.queue and not bool([s for s in self.queue if s]):
            # we have a queue, but it's full of None so clear it out
            self.clearQueue()
            
        

    def removeLoopedSound(self, sound, beat):
        '''
        Remove a sound from playing on a particular beat
        '''
        beat = beat % self.totalBeats
        if sound in self.loop[beat]:
            self.loop[beat].remove(sound)

    def addQueuedSound(self, sound, quantize=None, space=None, id=None, silence=False):
        '''
        Adds the given sound, optionally quantized to the given resolution
        and given 'space' number of beats before the next trigger is allowed.
        Defaults to quantizing to the full resolution of this manager with no
        intervening space.
        '''
        #print 'appending %s to queue' % sound.getFileName()

        # add to the silent count if need be
        if id and silence:
            if id in self.silentCount:
                return # shortcut out if needed
            self.silentCount[id] = self.totalBeats / 2
            
        #if not self.queue and quantize == self.totalBeats:
            # we don't have anything queued, and we're asked to quantize on the start beat
            # might as well start-a-fresh!
        #    self.currentBeat = 0        
        #el maybe not
        if quantize and quantize <= self.totalBeats:
            # otherwise, if we've been asked to quantize to a beat resoltuion, skip minor beats until we hit it
            
            # check for the next available beat. start at our current beat, go to the end of the queue, and add one.
            # this offset by one is to account for the fact that the queue won't get checked until the *next* beat
            b = self.currentBeat + len(self.queue) + 1
            
            #print ' b', b
            #print ' quantize', quantize
            while b % quantize:
                #print ' b % quantize', b % quantize
                #print ' skipping %d for quantization...' % b
                self.queue.append(None)
                b += 1

        # put the given sound onto the play queue
        if id:
            self.queue.append((sound, id))
        else:
            self.queue.append(sound)

        # put in some rests after our sound plays
        if space:
            # knock off one for the sound itself
            space = space - 1;

            # now tick off the rest
            while space > 0:
                self.queue.append(None)
                space = space - 1

        # clean out any stops on this sound
        for stop in self.stops:
            if sound in stop:
                stop.remove(sound)

    def isSoundQueued(self, sound):
        return (sound in (q[0] for q in self.queue if type(q) is tuple)) or (sound in self.queue)

    def isFireKeyQueued(self, key):
        return key in (q[1] for q in self.queue if type(q) is tuple)                

    def isSilent(self, id):
        return id in self.silentCount

    def clearQueue(self):
        '''
        Removes all pending sounds from the queue
        '''
        del self.queue[:]

    def clearLoop(self):
        '''
        Removes all looped sounds
        '''
        for l in self.loop:
            del l[:]

