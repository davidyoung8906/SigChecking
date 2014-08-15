import os
import argparse
import sys
import subprocess
import datetime
import time
import epicc_parser
import json
import threading
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
            self.process.kill()
            thread.join()
        print self.status, self.output, self.error
        
#parser = argparse.ArgumentParser(description='Generate SVG of callgraph and sub-callgraph for given APK')
#saveout = sys.stdout
currentdir = os.getcwd()
rootdir = "/home/wyang/workspace/CommandLine/APPLICATIONS"
#"/home/wyang/workspace/CommandLine/samples/DroidKungFu1"
#"/home/wyang/workspace/CommandLine/samples/"
#"/home/wyang/workspace/CommandLine/samples/GoldDream"
# "/home/wyang/workspace/CommandLine/APPLICATIONS"
retargetDir = os.path.join(currentdir, "RetargetDir")
studyDir = os.path.join(currentdir, "StudyDir")
for path, subdirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith(".apk"):

            apkpath = os.path.join(path, name)
            appName = name[:-4]
            #retargetPath = os.path.join(retargetDir, appName)
            # print filepath
            saveout = sys.stdout
            p, filename = os.path.split(apkpath)
            # #print filename
            a, dir = os.path.split(p)
            # #print dir
            retargetPath = os.path.join(currentdir, "RetargetDir", dir, filename)
            # #print filepath1
            if os.path.exists(retargetPath):
                continue;
            # #else:
            #  #   os.makedirs(os.path.dirname(filepath1))
            # platformPath = "/home/wyang/android-sdks/platforms"
            
            print "retargeting"	
            cmd1 = "./dare -e -p -d "+retargetPath+" "+apkpath 
            print cmd1
            fp1 = os.popen(cmd1)
            res1 = fp1.read()
            print res1

            start = time.time()
            
            print "processing icc"
            cmd = 'exec java -jar -Xms4096m -Xmx8192m epicc-0.1.jar -apk ' + apkpath + ' -android-directory '+retargetPath+'/retargeted/* -cp android.jar -icc-study '+studyDir
            print cmd
            outputfile = os.path.join(retargetPath,"output.log")
            errfile = os.path.join(retargetPath,"erroutput.log")
            command = Command(cmd)
            command.run(timeout=300,outputfile = outputfile, errfile = errfile)
            # open(outputfile, 'w').close()
            # open(errfile, 'w').close()
            # child = subprocess.Popen(cmd, shell=True,stdout = file(os.path.join(retargetPath,"output.log"), 'w+'), stderr = file(os.path.join(retargetPath,"erroutput.log"), 'w+'))
            # (output, errput) = child.communicate()
            # print "Out:'%s'" % output
            # print "Err:'%s'" % errput
            # #sys.stdout = saveout
            end = time.time()
            elapsed = end - start
            with open("time.txt", "a") as myfile:
                #if(os.stat(errfile)[6] == 0):
                if os.path.isfile(outputfile):
                    a=open(outputfile,'rb')
                    lines = a.readlines()
                    flag = False
                    if (command.status == 0):
                        for line in lines:
                            if "The following ICC values were found:" in line:
                                flag = True
                        if flag == False:
                            myfile.write(dir+"_"+appName+": "+str(elapsed)+' Error! \n')
                        else:
                            last = lines[-1]
                            print last
                            if "The following ICC values were found:" not in last:
                                myfile.write(dir+"_"+appName+": "+str(elapsed)+' Have ICC! \n')
                                jsonfile = os.path.join(retargetPath,"intent.json")
                                ret = epicc_parser.parse_epicc(outputfile)
                                ret_json = json.dumps(ret, sort_keys=True, indent=4, separators=(',', ': '))
                                jsonfo = open(jsonfile,"wb")
                                jsonfo.write(ret_json)
                                #jsonfo.write(ret)
                            else:
                                myfile.write(dir+"_"+appName+": "+str(elapsed)+' No ICC! \n')
                    else: 
                        myfile.write(dir+ "_" + appName+": "+str(elapsed)+ ' timeout!!'+ '\n')
                else:
                    myfile.write(dir+ "_" + appName+": "+str(elapsed)+ ' no outputfile!!'+'\n')
                
        print 'finish ICC of '+ appName


