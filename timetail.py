#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import time
import sys


def parseArgs():
    parser = argparse.ArgumentParser(description="Output some part of file \
                                     for given time intervals")
    parser.add_argument("filepath", type=str, help="Path to file.")
    parser.add_argument("--time", type=int, help="time in second from end of \
                        the file", default=600)
    parser.add_argument("--begin", type=str, help="Start time.")
    parser.add_argument("--end", type=str, help="End time.")
    global args
    args = parser.parse_args()
    return args


def find_point(f,now):
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()
    time_to_find = now - args.time
    year = time.strftime("%Y")
    f.seek(0)
    while True:
        filePos = f.tell()
        line = f.readline()
        time_in_log = line[0:15]
        if time_in_log == "":
            break
        else:
            time_to_struct = time.strptime(time_in_log + " " +
                                             year,
                                             "%b %d %H:%M:%S %Y")
            time_to_unixtime = time.mktime(time_to_struct)
            if time_to_unixtime >= time_to_find:
                return filePos

# @profile
def main():
    now = time.time()
    args = parseArgs()
    filepath = args.filepath


    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            time_begin_in_log = f.read(15)
            time_begin = time.strptime(time_begin_in_log + " " +
                                       time.strftime("%Y"),
                                       "%b %d %H:%M:%S %Y")
            time_begin_in_unixtime = time.mktime(time_begin)
            if (now - time_begin_in_unixtime > args.time):
                filePos = find_point(f,now)
                f.seek(filePos)
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    else:
                        line = str.strip(line)
                        print "{}".format(line)

            else:
                f.seek(0)
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    else:
                        line = str.strip(line)
                        print "{}".format(line)
    else:
        print "{} is not exist".format(filepath)
        sys.exit(1)

if __name__ == "__main__":
    main()
