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

#ICC 
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

currentdir = os.getcwd()
apkpath = raw_input("Please enter your the path of your apk file: ")
print "you entered", apkpath
