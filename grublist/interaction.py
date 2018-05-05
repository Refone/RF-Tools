#!/usr/bin/env python

import sys
import os

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
