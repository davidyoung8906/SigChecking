import subprocess, threading
import shlex
import os
import traceback
import epicc_parser
import json

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

    def run(self, timeout):
        def target():
            print 'Thread started'
            try:
                print self.cmd
                retargetPath = "/home/wyang/workspace/CommandLine/epicc/RetargetDir/Jifake/9440bb3da5e1ad862f357248b5da0c59dc7fc96b.apk/"
                outputfile = os.path.join(retargetPath,"output.log")
                errfile = os.path.join(retargetPath,"erroutput.log")
                open(outputfile, 'w').close()
                open(errfile, 'w').close()
            
                self.process = subprocess.Popen(self.cmd, shell=True, stdout = file(outputfile, 'w+'), stderr = file(errfile, 'w+')) #
                (self.output, self.error) = self.process.communicate() #
                self.status = self.process.returncode
                print self.output #"Out:'%s'" % 
                print self.error #"Err:'%s'" % 
                print 'Thread finished'
            
                if(os.stat(errfile)[6] == 0):
                    a=open(outputfile,'rb')
                    lines = a.readlines()
                    last = lines[-1]
                    print last
                    if "The following ICC values were found:" not in last:
                        jsonfile = os.path.join(retargetPath,"intent.json")
                        ret = epicc_parser.parse_epicc(outputfile)
                        ret_json = json.dumps(ret, sort_keys=True, indent=4, separators=(',', ': '))
                        jsonfo = open(jsonfile,"wb")
                        jsonfo.write(ret_json)
            except:
                self.error = traceback.format_exc()
                self.status = -1      
                print self.error  

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        print self.status, self.output, self.error

cmd = "java -jar -Xms2048m -Xmx4096m epicc-0.1.jar -apk /home/wyang/workspace/CommandLine/samples/Jifake/9440bb3da5e1ad862f357248b5da0c59dc7fc96b.apk -android-directory /home/wyang/workspace/CommandLine/epicc/RetargetDir/Jifake/9440bb3da5e1ad862f357248b5da0c59dc7fc96b.apk/retargeted/* -cp android.jar -icc-study /home/wyang/workspace/CommandLine/epicc/StudyDir"

command = Command(cmd)
#command.run(timeout=0.1)
command.run(timeout=10000)