#!/usr/bin/env python

import sys
import os


def print_memory_from_to_addr(pid, start, stop):
    """
    Run as root, print content memory from start to end given address.
    For example:
        pmap -x `pgrep pdns_recursor`
        sudo ./dump_mem_addr.py [pid] [start] [stop]
        strings /tmp/mem_dump.*
    """
    with open("/proc/%d/mem" % pid, "rb", 0) as mem_file:
        mem_file.seek(start)
        chunk = mem_file.read(stop - start)
        with open("/tmp/mem_dump.%d" % os.getpid(), 'w') as save_to_file:
            save_to_file.write(chunk)
            save_to_file.close()

if __name__ == '__main__':  # Execute this code when run from the commandline.
    pid = int(sys.argv[1])
    start = int(sys.argv[2], 16)
    stop = int(sys.argv[3], 16)
    print_memory_from_to_addr(pid, start, stop)
