import sub_generator.api as api
import subprocess
from threading import Thread

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


def ts_to_mp4(filename):

    infile = filename + ".ts"
    outfile = filename + ".mp4"


    subprocess.run(["ffmpeg", "-i", infile, outfile,"-y","-loglevel", "panic","-hide_banner","-nostats"])

    return outfile


def process(filename):
    if ".ts" in filename:
        filename = filename[:-3]

    t1 = ThreadWithReturnValue(target = api.get_subs, args=(filename,))
    t2 = ThreadWithReturnValue(target = ts_to_mp4, args=(filename,))
    t1.start()
    t2.start()
    subs =  t1.join()
    mp4 = t2.join()

    return {'subs':subs,'video_path':mp4}
    

print(process("./sub_generator/segment356.ts"))
