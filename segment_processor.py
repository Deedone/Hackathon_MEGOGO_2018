import sub_generator.api as api
import subprocess
from threading import Thread
import m3u8 as mstream
import urllib.request
import time
import atexit

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
        self.index = 300
        self.data = {}
        self.preload = 3
        self.isstop = False

        self.stream = mstream.load(path)
        if self.stream.is_variant:
            self.fixvariant()
        self.t = Thread(target=self.manage)
        self.t.start()
        print("Time to return")
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
            lastindex = 300
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
                self.data[to_load] = data
            time.sleep(0.5)

    def next(self):
        self.index = self.index+1
        return self.data[self.index]

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

    return {'subs':subs}#,'video_path':mp4}
    

o = SegmentManager("./index.m3u8") 
