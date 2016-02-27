#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mmap
import os
import time

offset = 8
numLine = 10
filename = "/tmp/syslog"
File = open(filename, "rb")
size = os.path.getsize(filename)
data = mmap.mmap(File.fileno(), size, access=1)

pos = size - offset
data.seek(pos)

newline = 0
newline_pos = 0
for i in xrange(pos, size):
    if data[i] == '\n':
        newline += 1
        if not newline_pos:
            newline_pos = i + 1
    i += 1

if newline < numLine:
    for i in xrange(pos, 0, -1):
        if data[i] == '\n':
            newline += 1
            newline_pos = i + 1
        if newline > numLine:
            break

data.seek(newline_pos)
line = data.readline().strip()
while line != '':
    print line
    line = data.readline().strip()

while True:
    newFsize = os.path.getsize(filename)
    if newFsize > size:
        data = mmap.mmap(File.fileno(), newFsize, access=1)
        data.seek(size)
        line = data.readline()
        while line != '':
            print line.strip()
            line = data.readline()
        size = newFsize
    else:
        time.sleep(1)
