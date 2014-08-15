import os
import sys

rootdir = "/home/wyang/workspace/CommandLine/samples/"
timeFile = "/home/wyang/workspace/CommandLine/epicc/time.txt"
with open("time_reWrite.txt", "a") as myfile:
    a=open(timeFile,'rb')
    lines = a.readlines()
    for line in lines:
        subLine = line[:line.index(": ")]
        #print subLine
        for path, subdirs, files in os.walk(rootdir):
            for name in files:
                if subLine in name:
                    apkpath = os.path.join(path, name)
                    p, filename = os.path.split(apkpath)
                    a, dir = os.path.split(p)
                    print dir+"_"+line
                    myfile.write(dir+"_"+line)
                    print line
                #     myfile.write(dir+"_"+line)
                #     print  dir+"_"+line
                # else:
                #     print line+'\n'
                    #myfile.write(line+'\n')
                    