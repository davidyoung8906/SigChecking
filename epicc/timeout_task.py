import subprocess, threading

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        print self.process.returncode

command = Command("java -jar -Xms2048m -Xmx4096m epicc-0.1.jar -apk /home/wyang/workspace/CommandLine/samples/Jifake/9440bb3da5e1ad862f357248b5da0c59dc7fc96b.apk -android-directory /home/wyang/workspace/CommandLine/epicc/RetargetDir/Jifake/9440bb3da5e1ad862f357248b5da0c59dc7fc96b.apk/retargeted/* -cp android.jar -icc-study /home/wyang/workspace/CommandLine/epicc/StudyDir")
command.run(timeout=3)
command.run(timeout=1)