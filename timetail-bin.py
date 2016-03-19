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


def find_point(f, now, filepath):
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()
    time_to_find = now - args.time
    print time.ctime(time_to_find)
    year = time.strftime("%Y")
    fSize = os.path.getsize(filepath)
    begin = 0.0
    end = float(fSize)
#    print "begin = {}, end = {}".format(begin, end)
    while end - begin > 0.0001:
        point_to_seek = begin + (end - begin)/2
#        print "begin = {}, end = {}, point_to_seek = {}".format(begin, \
#                                                                end, \
#                                                                point_to_seek)
#        time.sleep(1)
#        print "{}".format(point_to_seek)

        f.seek(int(point_to_seek))
        line = f.readline()
        time_in_log = line[0:15]
        try:
            time_to_struct = time.strptime(time_in_log + " " +
                                             year,
                                             "%b %d %H:%M:%S %Y")
        except:
            line = f.readline()
            time_in_log = line[0:15]
            time_to_struct = time.strptime(time_in_log + " " +
                                             year,
                                             "%b %d %H:%M:%S %Y")
        time_to_unixtime = time.mktime(time_to_struct)
#        print "{}".format(time_to_find)
#        print "{}".format(time_to_unixtime)
        if time_to_unixtime >= time_to_find:
            end = point_to_seek
#            print "time_in_log = {}".format(time_in_log)
        else:
            begin = point_to_seek
    filePos = f.tell()
    return filePos



    """
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
    """

# @profile
def main():
    now = time.time()
    args = parseArgs()
    filepath = args.filepath


    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            time_begin_in_log = f.read(15)
            time_begin = time.strptime(time_begin_in_log + " " +
                                       time.strftime("%Y"),
                                       "%b %d %H:%M:%S %Y")
            time_begin_in_unixtime = time.mktime(time_begin)
            if (now - time_begin_in_unixtime > args.time):
                filePos = find_point(f,now,filepath)
                f.seek(filePos)
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    else:
                        line = str.strip(line)
#                        print "{}".format(line)
                        try:
                            print line
                        except IOError:
                                try:
                                        sys.stdout.close()
                                except IOError:
                                        pass
                                try:
                                        sys.stderr.close()
                                except IOError:
                                        pass

            else:
                f.seek(0)
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    else:
                        line = str.strip(line)
                        print line
#                        print "{}".format(line)
    else:
        print "{} is not exist".format(filepath)
        sys.exit(1)

if __name__ == "__main__":
    main()
