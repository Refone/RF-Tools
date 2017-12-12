#!/usr/bin/env python
# encoding: utf-8

#import sys
import os
import re
import json
from collections import defaultdict

def tree():
    return defaultdict(tree)

entry = tree()      #   name
                    #   childnum
                    #   child[]
level = 0

def loadGrub():
    global entry
    global level

    try:
        f = open('/boot/grub/grub.cfg', 'r')
    except IOError:
        print "Open file \"/boot/grub/grub.cfg\" Failed."
        return

    entry['name']='root'
    entry['childnum'] = 0
    entry['type'] = 'root'
    for eachLine in f.readlines():
        r = re.findall(r'^\s*(menuentry|submenu)\s*\'([^\']*)\'', eachLine)
        if r:
            e = entry
            for i in range(0, level):
                childnum = e['childnum']
                e = e['child'][childnum]

            print e['name']
            print e['childnum']
            childnum = e['childnum']
            e['child'][childnum]['name'] = r[0][1]
            e['child'][childnum]['childnum'] = 0
            e['childnum'] += 1

            if r[0][0] == 'menuentry': 
                e['child'][childnum]['type'] = 'menuentry'
            elif r[0][0] == 'submenu':
                e['child'][childnum]['type'] = 'submenu'

        r = re.findall(r'{\s*$', eachLine)
        if r:
            level += 1

        r = re.findall(r'^\s*}', eachLine)
        if r:
            level -= 1
               
                #print "%s%s %s"%(r[0][0], r[0][1])
    
    print(json.dumps(entry))
    f.close()

def printGrub(e, level):
    #print(" "*(4*(level-1))+e['name'])
    print(e['name'])
    if e['type']=='submenu':
        for i in range(0, e['childnum']):
            printGrub(e['child'][i], level+1)

def showGrub():
    for i in range(0, entry['childnum']):
        printGrub(entry['child'][i], 0)
    
def main():
    loadGrub()
    showGrub()

if __name__ == '__main__':
    main()
