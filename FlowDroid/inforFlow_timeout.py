import os
import argparse
import sys
import datetime
import time
import subprocess, threading
import shlex
import traceback


class Command(object):

    cmd = None
    process = None
    status = None
    output, error = '', ''

    def __init__(self, cmd):
        # if isinstance(cmd, basestring):
        #     cmd = shlex.split(cmd)
        self.cmd = cmd
        #self.process = None

    def run(self, timeout, outputfile, errfile):
        def target():
            print 'Thread started'
            try:
                print self.cmd
                open(outputfile, 'w').close()
                open(errfile, 'w').close()
                self.process = subprocess.Popen(self.cmd, shell=True, stdout = file(outputfile, 'w+'), stderr = file(errfile, 'w+')) #
                (self.output, self.error) = self.process.communicate() #
                self.status = self.process.returncode
                print self.output #"Out:'%s'" % 
                print self.error #"Err:'%s'" % 
                print 'Thread finished'
            except:
                self.error = traceback.format_exc()
                self.status = -1      
                print self.error  

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.kill() #terminate
            thread.join()
        print self.status

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
            cmd = 'exec java -jar -Xms4096m -Xmx8192m Flowdroid.jar ' + filepath + ' '+platformPath+' '+'--aliasflowins' +' --TIMEOUT 1800' #
            outputfile = os.path.join(filepath1,"output1.log")
            errfile = os.path.join(filepath1,"erroutput1.log")
            # child = subprocess.Popen(cmd, shell=True,stdout = file(os.path.join(filepath1,"output1.log"), 'w+'), stderr = file(os.path.join(filepath1,"erroutput1.log"), 'w+'))
            # (output, errput) = child.communicate()
            # print "Out:'%s'" % output
            # print "Err:'%s'" % errput
            # #sys.stdout = saveout
            command = Command(cmd)
            command.run(timeout=2000,outputfile = outputfile, errfile = errfile)
            end = time.time()
            elapsed = end - start
            with open("time2.txt", "a") as myfile:
                if(command.status == 0):
                    myfile.write(dir+ "_" + filename+": "+str(elapsed)+'\n')
                else:
                    myfile.write(dir+ "_" + filename+": "+str(elapsed)+ 'timeout!!'+ '\n')
            print 'finish '+ filename
            print 'finish infoflow of '+ filepath
