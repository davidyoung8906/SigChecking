import os
import argparse
import sys
import subprocess
import datetime
import time

#parser = argparse.ArgumentParser(description='Generate SVG of callgraph and sub-callgraph for given APK')
#saveout = sys.stdout
currentdir = os.getcwd()
appType = sys.argv[1]
#rootdir = "/home/wyang/workspace/CommandLine/samples/"+appType
#rootdir = "/home/wyang/workspace/CommandLine/APPLICATIONS"
rootdir = "/home/wyang/workspace/CommandLine/SigChecking/BenignCheckingApps"
print rootdir
sigfile = "/home/wyang/workspace/AppoCheck1/ResultParser/Test/"+appType+".xml"
apkdir = "/home/wyang/workspace/CommandLine/SigChecking/BenignCheckingApps/"
#"/home/wyang/workspace/CommandLine/APPLICATIONS"

#manifestdir = "/home/wyang/workspace/CommandLine/decompile_samples"
manifestdir = "/home/wyang/workspace/CommandLine/decompile_APPLICATIONS"
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
            resultpath = os.path.join(currentdir, "Benign_Result", dir, filename)
            if not os.path.exists(resultpath):
                os.makedirs(resultpath)
            resultfile = os.path.join(resultpath, "result.log")
            #
            manifestfile = os.path.join(manifestdir, dir, filename, "AndroidManifest.xml")
            ICCfile = os.path.join(ICCdir, dir, filename, "intent.json")
            flowfile = os.path.join(flowdir, dir, filename, "erroutput.log") #"erroutput1.log"
            if(os.path.isfile(os.path.join(flowdir, dir, filename, "erroutput1.log"))):
                os.rename(os.path.join(flowdir, dir, filename, "erroutput1.log"), flowfile)
                os.rename(os.path.join(flowdir, dir, filename, "output1.log"), os.path.join(flowdir, dir, filename, "output.log"))
            apkfile = os.path.join(rootdir, dir, filename)
            #print filepath1

            if os.path.exists(resultfile):
                continue;

            #else:
             #   os.makedirs(os.path.dirname(filepath1))
            platformPath = "/home/wyang/android-sdks/platforms"
            
            print "processing result"
            cmd = 'java -jar -Xms2048m -Xmx4096m ResultParser.jar -manifest ' + manifestfile + ' -ICC '+ICCfile+' -flow '+ flowfile + " -result "+resultfile+" -apk "+apkfile + " -sdk "+platformPath+ " -sig "+ sigfile
            print cmd
            open(os.path.join(resultpath,"output.log"), 'w').close()
            open(os.path.join(resultpath,"erroutput.log"), 'w').close()
            child = subprocess.Popen(cmd, shell=True,stdout = file(os.path.join(resultpath,"output.log"), 'a'), stderr = file(os.path.join(resultpath,"erroutput.log"), 'a'))
            (output, errput) = child.communicate()
            print "Out:'%s'" % output
            print "Err:'%s'" % errput
            #sys.stdout = saveout
            end = time.time()
            elapsed = end - start
            #open(resultfile, 'w+').close()
            with open("time_Benign.txt", "a") as myfile:
                if(os.stat(resultfile)[6] != 0):
                    a=open(resultfile,'rb')
                    lines = a.readlines()
                    last = lines[0]
                    print last
                    # if "not matching" in last:
                    #     myfile.write(filename+": "+str(elapsed)+' Not Matched! \n')
                    #     #jsonfo.write(ret)
                    # elif "No Flow information" in last:
                    #     myfile.write(filename+": "+str(elapsed)+' No FlowInformation! \n')
                    # elif "Matching golddream malware" in last:
                    #     myfile.write(filename+": "+str(elapsed)+' Matched! \n')
                    myfile.write(filename+": "+str(elapsed)+"   "+last+'  \n')
                    if(("ICC file" in  last) or ("No Flow information " in  last)):
                        fullPath = os.path.join(apkdir,dir,filename)
                        if os.path.isfile(fullPath):
                            os.remove(fullPath)
                else:
                    myfile.write(filename+": "+str(elapsed)+' Error! \n')
            print 'finish result of '+ filepath


