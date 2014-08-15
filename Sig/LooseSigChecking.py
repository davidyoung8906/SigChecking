import os
import argparse
import sys
import subprocess
import datetime
import time

#parser = argparse.ArgumentParser(description='Generate SVG of callgraph and sub-callgraph for given APK')
#saveout = sys.stdout
currentdir = os.getcwd()
rootdir = "/home/wyang/workspace/CommandLine/samples/GoldDream"
#"/home/wyang/workspace/CommandLine/APPLICATIONS"

manifestdir = "/home/wyang/workspace/CommandLine/decompile_samples"
ICCdir = "/home/wyang/workspace/CommandLine/epicc/RetargetDir"
flowdir = "/home/wyang/workspace/CommandLine/FlowDroid/INFORMATION_FLOW"

for path, subdirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith(".apk"):

            start = time.time()
            appName = name[:-4]
            filepath = os.path.join(path, name)
            print filepath
            saveout = sys.stdout
            p, filename = os.path.split(filepath)
            #print filename
            a, dir = os.path.split(p)
            #print dir
            resultpath = os.path.join(currentdir, "Result", dir, filename)
            if not os.path.exists(resultpath):
                os.makedirs(resultpath)
            resultfile = os.path.join(resultpath, "result.log")
            manifestfile = os.path.join(manifestdir, dir, filename, "AndroidManifest.xml")
            ICCfile = os.path.join(ICCdir, dir, filename, "intent.json")
            flowfile = os.path.join(flowdir, dir, filename, "erroutput.log")
            #print filepath1
            if os.path.exists(resultfile):
                continue;
            #else:
             #   os.makedirs(os.path.dirname(filepath1))
            platformPath = "/home/wyang/android-sdks/platforms"
            
            print "processing result"
            cmd = 'java -jar LooseSigChecker.jar -manifest ' + manifestfile + ' -ICC '+ICCfile+' -flow '+ flowfile + " -result "+resultfile
            print cmd
            open(os.path.join(currentdir,"output.log"), 'a').close()
            open(os.path.join(currentdir,"erroutput.log"), 'a').close()
            child = subprocess.Popen(cmd, shell=True,stdout = file(os.path.join(currentdir,"output.log"), 'a'), stderr = file(os.path.join(currentdir,"erroutput.log"), 'a'))
            (output, errput) = child.communicate()
            print "Out:'%s'" % output
            print "Err:'%s'" % errput
            #sys.stdout = saveout
            end = time.time()
            elapsed = end - start
            with open("time.txt", "a") as myfile:
                if(os.stat(resultfile)[6] != 0):
                    a=open(resultfile,'rb')
                    lines = a.readlines()
                    last = lines[0]
                    print last
                    if "Not Matching" not in last:
                        myfile.write(filename+": "+str(elapsed)+' Matched! \n')
                        #jsonfo.write(ret)
                    else:
                        myfile.write(filename+": "+str(elapsed)+' Not Matched! \n')
                else:
                    myfile.write(filename+": "+str(elapsed)+' Error! \n')
            print 'finish result of '+ filepath
