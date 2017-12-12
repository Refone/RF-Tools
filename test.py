#!/usr/bin/env python
#coding:utf-8
# Filename: systemstatus.py

import os


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
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
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

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

def main():
    item = "input"
    while True:
        item = getch()
        if item=='a':# or item == '\x1b':
            break
        elif ord(item) == 27:
           item = getch()
           item = getch()
           if ord(item) == 65:
               print "up"
           if ord(item) == 66:
               print "down"
           if ord(item) == 68:
               print "left"
           if ord(item) == 67:
               print "right"
            #if item == ''
        #else:
        #    print ord(item)
        #elif item=='\x1b[A':
        #    print "up"
        #elif item=='\x1b[B':
        #    print "down"
        #elif item=='\x1b[C':
        #    print "right"
        #elif item=='\x1b[D':
        #    print "left"
        else:
            print "not an arrow key!"

if __name__ == "__main__":
    main()
