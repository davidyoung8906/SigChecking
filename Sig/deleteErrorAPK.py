import os
import argparse
import sys
import subprocess
import datetime
import time

apkdir = "/home/wyang/workspace/CommandLine/SigChecking/BenignCheckingApps/FINANCE"
resultFile = "/home/wyang/workspace/CommandLine/SigChecking/FINANCE_result"

if os.path.isfile(resultFile):
    a=open(resultFile,'rb')
    lines = a.readlines()
    for line in lines:
        if(("ICC file" in  line) or ("No Flow information " in  line)):
             i = line.index(".apk")+4	
             fileName = line[:i]
             fullPath = os.path.join(apkdir,fileName)
             if os.path.isfile(fullPath):
                 os.remove(fullPath)
             

    		

