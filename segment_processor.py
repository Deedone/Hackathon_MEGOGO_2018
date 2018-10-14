import sub_generator.api as api
import subprocess
from threading import Thread
import m3u8 as mstream
import urllib.request
import time
import atexit
import math
import wave
import re

class ThreadWithReturnValue(Thread):#StackOverflow rulez
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


class SegmentManager:

    def __init__(self, path):
        self.index = -1
        self.data = {}
        self.preload = 10
        self.isstop = False
        self.time = 0

        self.stream = mstream.load(path)
        if self.stream.is_variant:
            self.fixvariant()
        self.t = Thread(target=self.manage)
        self.t.start()
        print("Time to return")
        while len(self.data.keys()) < 1:
            time.sleep(0.1)

        return


    def fixvariant(self):
        self.uri = self.stream.playlists[0].uri
        print("got uri %s" % (self.uri))
        self.stream = mstream.load(self.uri) 
        self.uri = self.uri[:self.uri.rfind("/")+1]
        print("new uri %s" % (self.uri))

    def stop(self):
        self.isstop = True
        self.t.join()

    def manage(self):
        while not self.isstop:
            lastindex = -1
            try:
                lastindex = max(self.data.keys())
            except ValueError:
                pass

            if lastindex < self.index + self.preload:
                to_load = lastindex+1
                seg = self.stream.segments[to_load].uri
                uri = self.uri + seg
                urllib.request.urlretrieve(uri,"ts/"+seg)
                data = process(seg)
                print(data)
                self.data[to_load] = {'subs':data['sub'],'timestamp':self.time,'dur':data['dur']}
                self.time += data['dur']
                if to_load % 2 == 1:
                    self.adjust_subs(to_load - 1)
            time.sleep(0.2)

    def adjust_subs(self,start):
        print("Starting sub adjustment+++===---")

        with wave.open("./wavs/combined.wav","wb") as out:
            for i in range(2):
                print(self.data[start + i]['subs'], end=" ")
                with wave.open("./wavs/segment"+str(start + i + 1) +".wav","rb") as inp:
                    if i == 0:
                        out.setparams(inp.getparams())
                    out.writeframes(inp.readframes(inp.getnframes()))

                    
        combtext = api.get_subs("","./wavs/combined.wav")
        print("Combined - "+str(combtext))
        #######################################################
        count_all  = 0
        count_sub1 = 0
        count_sub2 = 0

        for ch in str(combtext['sub']):
            if ch == ' ':
                count_all += 1
        print(count_all)
        for ch in str(self.data[start + 0]['subs']):
            if ch == ' ':
                
                count_sub1 += 1

        print(count_sub1)
        num = 0
        for i in range(count_sub1):
          print(combtext['sub'].find(' ', num))
          num = combtext['sub'].find(' ', num)
          num +=1

        print(num)
        
        string_sub1 =  combtext['sub'][0  :num]
        string_sub2 =  combtext['sub'][num: ]
        self.data[start + 0]['subs'] = string_sub1
        self.data[start + 1]['subs'] = string_sub2
        print('Super Combiner 11111 : ' + string_sub1 + '\n' + string_sub2)
        print('Super Combiner 22222 :' + self.data[start + 0]['subs'] + '\n' + self.data[start + 1]['subs'] )


    def next(self):
        self.index = self.index+1
        lastindex = max(self.data.keys())
        print('___________________Return____' + str(self.data[self.index])) 
        if self.data[self.index]['subs'] == None:
            self.data[self.index]['subs'] = ""
            return self.data[self.index]
        else :
            return self.data[self.index]
        # if there are no subtitles - returns empty string as subtitle
            

    def closestSubtitles(self, timestapm): # returns timestamp(number in secs) of closest data['timestamp']
        minDelta = prevMinDelta = 9999
        closestTimestamp = 0
        for dictLol in self.data[::-1]:
            prevMinDelta = minDelta
            minDelta = math.abs(timestamp - self.data[dictLol]['timestamp'])
            if prevMinDelta < minDelta:
                self.index = dictLol + 1
                return closestTimestamp

            closestTimestamp = self.data[dictLol]['timestamp']


    def jump_to():
        pass

def ts_to_mp4(filename):

    infile = "ts/"+filename + ".ts"
    outfile = "videos/"+filename + ".mp4"


    subprocess.run(["ffmpeg", "-i", infile, outfile,"-y","-loglevel", "panic","-hide_banner","-nostats"])

    return outfile


def process(filename):
    if ".ts" in filename:
        filename = filename[:-3]

    t1 = ThreadWithReturnValue(target = api.get_subs, args=(filename,))
    #t2 = ThreadWithReturnValue(target = ts_to_mp4, args=(filename,))
    t1.start()
    #t2.start()
    subs =  t1.join()
    #mp4 = t2.join()

    return subs
    

