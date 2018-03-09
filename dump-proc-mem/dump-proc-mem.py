#! /usr/bin/env python
import re

def dump_page(chunk):
    for i in range(0, 16):
        line = ""
        for j in range(0, 16):
            line += "%x " % chunk[16*16*i + 16*j]
        print line

def main():
    pid = sys.argv[1]
    maps_filename = "/proc/" + pid + "/maps"
    mem_filename = "/proc/" + pid + "/mem"
    print maps_filename
    print mem_filename
    maps_file = open(maps_filename, 'r')
    mem_file = open(mem_filename, 'r', 0)
    
    for line in maps_file.readlines():  # for each mapped region
        print line
        m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
        if m.group(3) == 'r':  # if this is a readable region
            start = int(m.group(1), 16)
            end = int(m.group(2), 16)
            page_index = 0;
            while end >= start + 16*16*16:
                print("page[%d]"%page_index)
                mem_file.seek(start)  # seek to region start
                chunk = mem_file.read(16*16*16)  # read region contents
                dump_page(chunk)
                start += 16*16*16
                page_index += 1
                print "\n" 
    
    maps_file.close()
    mem_file.close()

if __name__ == '__main__':
    main()
