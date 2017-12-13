#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import json
from collections import defaultdict

def tree():
    return defaultdict(tree)

entry = tree()      #   name
                    #   childnum
                    #   child[]

def loadGrub():
    global entry
    level = 0

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
                e = e['child'][childnum-1]

            if e['childnum']=={}:
                e['childnum'] = 0

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
    
    #print(json.dumps(entry))
    f.close()

def printGrub(e, level):
    print(" "*(4*level)+e['name'])
    if e['type']=='submenu':
        for i in range(0, e['childnum']):
            printGrub(e['child'][i], level+1)

def showGrub():
    for i in range(0, entry['childnum']):
        printGrub(entry['child'][i], 0)

def printEntry(root, p, l):
    for i in range(0, root['childnum']):
        if i == p[l]:
            print(" "*(4*l-1)+"+"+root['child'][i]['name'])
            if root['child'][i]['type'] == "submenu" and l+1<len(p):
                printEntry(root['child'][i], p, l+1)
        else:
            print(" "*(4*l)+root['child'][i]['name'])

def getEntry(root, p):
    e = root
    for i in range(0, len(p)):
        idx = p[i]
        e = e['child'][idx]
    return e

def setEntry(path):
    return

" ====================  Implement Python getch()  =========================="
"""Gets a single character from standard input.  Does not echo to the screen."""

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchUnix()
            except ImportError:
                self.impl = _GetchMacCarbon()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys, termios 
        # import termios now or else you'll get the Unix version on the Mac

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

" ====================  Implement Python getch()  =========================="

" ====================  Get Keyboard Input ================="
" Up:       1       |   Enter:      5   "
" Down:     2       |   q:          6   "
" Right:    3       |   y:          7   "
" Left:     4       |   n:          8   "
" any key else:                     0   "
def getKeyInput():
    c = getch()
    if ord(c)==27:
        c = getch()
        if ord(c) != 91:
            return 0
        c = getch()
        if ord(c) == 65:    # Up
            return 1
        if ord(c) == 66:    # Down
            return 2
        if ord(c) == 67:    # Right
            return 3
        if ord(c) == 68:    # Left
            return 4
        return 0
    if ord(c)==13:          # Enter
        return 5
    if c=='q':              # q
        return 6
    if c=='y':              # y
        return 7
    if c=='n':              # n
        return 8
    return 0

def menu():
    global entry
    path = []
    path.append(0)
    k = 0
    while True:
        os.system("clear")
        printEntry(entry, path, 0)
        k=0
        while k==0:
            k = getKeyInput()

        if k==1:            # Up
            p = path.pop()
            p = max(0, p-1)
            path.append(p)
            continue
        if k==2:            # Down
            p = path.pop()
            p = min(getEntry(entry, path)['childnum']-1, p+1)
            path.append(p)
            continue
        if k==3:            # Right
            if getEntry(entry, path)['type']=='submenu':
                path.append(0)
                continue
            else:
                setEntry(path)
                break
        if k==4:            # Left
            if getEntry(entry, path)['type']=='submenu':
                path.pop()
            continue
        if k==6:
            break

def main():
    loadGrub()
    menu()
    #showGrub()

if __name__ == '__main__':
    main()
