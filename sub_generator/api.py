import speech_recognition as sr
import subprocess
import os
import hashlib
import json
import wave



if "cache.json" not in os.listdir():
    with open("cache.json","w") as i:
        i.write("{}")



def write_cache(key, value):
    data = 0
    with open("cache.json","r") as i:
        buf = i.read()
        data = json.loads(buf)
    data[key] = value
    with open("cache.json","w") as o:
        o.write(json.dumps(data))



def get_cache(key):
    buf = 0
    with open("cache.json","r") as i:
        buf = i.read()
    data = json.loads(buf)
    if key in data.keys():
        return data[key]
    else:
        return 0

def get_hash(filename):
    hasher = hashlib.md5()
    with open(filename,"rb") as i:
        buf = i.read()
        hasher.update(buf)
        print("Hashed %s - %s" % (filename, hasher.hexdigest()))
        
        return hasher.hexdigest()
    raise Exception("Hashing error")

def get_subs(segment): # segment is the name of .ts file (without .ts)
    r = sr.Recognizer()

    infile = "ts/"+segment + ".ts"
    outfile = "wavs/"+segment + ".wav"



    hs = get_hash(infile)
    cache = get_cache(hs)
    if cache != 0:
        print("Found in cache")
        return cache



    subprocess.run(["ffmpeg", "-i", infile, outfile,"-y","-loglevel", "panic","-hide_banner","-nostats"])


    segmentAudio = sr.AudioFile(outfile)
    dur = 0;
    with segmentAudio as source:
        print(source.DURATION)
        dur = source.DURATION
        audio = r.record(source)
    sub = None
    try:
        sub = r.recognize_google(audio, language="ru_RU")
    except sr.UnknownValueError:
        pass
    write_cache(hs,{'sub':sub,'dur':dur})
    os.remove(outfile)
    return {'sub':sub,'dur':dur}

