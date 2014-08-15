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
                #thread.join()
            print self.status

cmd = "java -jar -Xms4096m -Xmx8192m Flowdroid.jar /home/wyang/workspace/CommandLine/samples/DroidKungFu3/4c9f885680124dbcb8d590704d0f8dff4602f909.apk /home/wyang/android-sdks/platforms --aliasflowins --TIMEOUT 1800"
print "begin"
outputfile = os.path.join(os.getcwd(),"output.log")
errfile = os.path.join(os.getcwd(),"erroutput.log")
command = Command(cmd)
command.run(timeout=2,outputfile = outputfile, errfile = errfile)