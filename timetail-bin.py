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
#    print time.ctime(time_to_find)
    year = time.strftime("%Y")
    fSize = os.path.getsize(filepath)
    begin = 0.0
    end = float(fSize)
    while end - begin > 1:
        point_to_seek = begin + (end - begin)/2
        f.seek(int(point_to_seek))
        line = f.readline()
        time_in_log = line[0:15]
        try:
            filePos = f.tell()
            time_to_struct = time.strptime(time_in_log + " " +
                                           year,
                                           "%b %d %H:%M:%S %Y")
        except:
            try:
                seek = find_new_line_pos(f, f.tell())
                f.seek(seek)
                filePos = f.tell()
                line = f.readline()
                time_in_log = line[0:15]
                time_to_struct = time.strptime(time_in_log + " " +
                                               year,
                                               "%b %d %H:%M:%S %Y")
            except:
                return None
        time_to_unixtime = time.mktime(time_to_struct)
        if time_to_unixtime > time_to_find:
            end = point_to_seek
        elif time_to_unixtime == time_to_find:
            newfilePos = check_file_for_date(f, filePos, time_to_find)
            return newfilePos
        else:
            begin = point_to_seek
    return filePos


def find_new_line_pos(f, offset):
    char = ''
    while char != '\n':
        offset = offset - 1
        f.seek(offset)
        char = f.read(1)
    return offset+1


def check_file_for_date(f, offset, time_to_find):
    offset = find_new_line_pos(f, offset-1)
    f.seek(offset)
    line = f.readline()
    newDate = line[0:15]
    year = time.strftime("%Y")
    time_to_struct = time.strptime(newDate + " " +
                                   year,
                                   "%b %d %H:%M:%S %Y")
    time_to_unixtime = time.mktime(time_to_struct)
    if time_to_unixtime == time_to_find:
        return check_file_for_date(f, offset, time_to_unixtime)
    else:
        filePos = f.tell()
        return filePos


def main():
    now = int(time.time())
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
                filePos = find_point(f, now, filepath)
                if not filePos:
                    print "no lines"
                    sys.exit(1)
                f.seek(filePos)
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    else:
                        line = str.strip(line)
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
    else:
        print "{} is not exist".format(filepath)
        sys.exit(1)

if __name__ == "__main__":
    main()
