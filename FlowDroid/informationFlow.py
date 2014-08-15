import os
import argparse
import sys
import subprocess
import datetime
import time

#parser = argparse.ArgumentParser(description='Generate SVG of callgraph and sub-callgraph for given APK')
#saveout = sys.stdout
currentdir = os.getcwd()
rootdir = "/home/wyang/workspace/CommandLine/APPLICATIONS"
#"/home/wyang/workspace/CommandLine/samples/" 
#"/home/wyang/workspace/CommandLine/samples/DroidKungFu1"
#"/home/wyang/workspace/CommandLine/samples/GoldDream"
#"/home/wyang/workspace/CommandLine/APPLICATIONS"
#os.path.join(currentdir, "APPLICATIONS")
for path, subdirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith(".apk"):
            
            filepath = os.path.join(path, name)
            print filepath
            saveout = sys.stdout
            p, filename = os.path.split(filepath)
            #print filename
            a, dir = os.path.split(p)
            #print dir
            filepath1 = os.path.join(currentdir, "INFORMATION_FLOW", dir, filename)
            #print filepath1
            if os.path.exists(filepath1):
                #if not (filepath1.endswith("c9305cc8e1d2908708a49e8d9b932c2fdb952106.apk")):
                continue;
            #else:
             #   os.makedirs(os.path.dirname(filepath1))
            platformPath = "/home/wyang/android-sdks/platforms"
            
            # print "decompiling"	
            # cmd1 = './apktool d ' + filepath + ' '+filepath1;
            # fp1 = os.popen(cmd1)
            # res1 = fp1.read()
            # print res1

            if not os.path.exists(filepath1):
                os.makedirs(filepath1)

            start = time.time()
            
            print "processing inforflow"
            cmd = 'java -jar -Xms8192m -Xmx16384m Flowdroid.jar ' + filepath + ' '+platformPath+' '+'--aliasflowins' +' --TIMEOUT 1800' #
            open(os.path.join(filepath1,"output1.log"), 'w').close()
            open(os.path.join(filepath1,"erroutput1.log"), 'w').close()
            child = subprocess.Popen(cmd, shell=True,stdout = file(os.path.join(filepath1,"output1.log"), 'w+'), stderr = file(os.path.join(filepath1,"erroutput1.log"), 'w+'))
            (output, errput) = child.communicate()
            print "Out:'%s'" % output
            print "Err:'%s'" % errput
            #sys.stdout = saveout
            end = time.time()
            elapsed = end - start
            with open("time1.txt", "a") as myfile:
                myfile.write(dir+ "_" + filename+": "+str(elapsed)+'\n')
            print 'finish '+ filename
            print 'finish infoflow of '+ filepath
