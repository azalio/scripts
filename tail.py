#!/usr/bin/env python

import os
import time

linesNum = 10
filename = '/tmp/syslog'
readBytes = 1024

f = open(filename, 'r')

fSize = os.path.getsize(filename)

f.seek(fSize - readBytes)
lines = f.readlines()

while len(lines) <= linesNum:
    readBytes = readBytes*2
    f.seek(fSize - readBytes)
    lines = f.readlines()

indexFrom = len(lines) - linesNum
for x in xrange(indexFrom,len(lines)):
    print lines[x].strip()

while True:
    newFsize = os.path.getsize(filename)
    if newFsize > fSize:
        line = f.readline()
        while line != '':
            print line.strip()
            line = f.readline()
        fSize = newFsize
    else:
        time.sleep(1)

