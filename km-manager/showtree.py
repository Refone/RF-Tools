#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import json
import commands
from collections import defaultdict

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Module:
    # name:     name of the module
    # used:     be used by how many modules
    # childnum: nameable child modules amount
    # child:    a dictionary contain the child modules
    def __init__(self, name, used):
        self.name = name
        self.used = used
        self.childnum = 0
        self.child = []
    
    def addChildModule(self, m):
        self.child.append(m)
    
def loadModuleTree(module_name):
    cmd = "sudo lsmod | grep " + module_name
    output = commands.getoutput(cmd)
    
    module_match = 0
    for eachline in output.splitlines():
        r = eachline.split()
        name = r[0]
        used = r[2]

        if name != module_name:
            continue

        # find the module by module name
        module_match = 1

        if len(r) < 4:
            # no more child modules
            return Module(name, used)
        
        childstr = r[3]
        m = Module(name, used)
        childs = childstr.split(',')
        for childname in childs:
            childmodule = loadModuleTree(childname)
            
            if childmodule is None:
                print("Module [" + module_name + "]\'s child module [" + \
                        m + "] load failed")
                return
            
            m.addChildModule(childmodule)

        return m

    if module_match == 0:
        # no matched kernel module found
        print("Module [" + module_name + "] not found")
        return

    return

level_max = [0,0,0,0,0,0,0,0,0,0]
level_cur = [0,0,0,0,0,0,0,0,0,0]
def printModuleTree(module, level):
    if level!=0:
        if level_cur[level] == level_max[level] - 1:
            head = "└─ "
        else:
            head = "├─ "

    if level==1:
        print head,
    if level>1:
        for i in range(1,level):
            #print i,
            #print "-",
            #print level_cur[i],
            #print "-",
            #print level_max[i],
            if level_cur[i] < level_max[i]:
                print "│  ",
            else:
                print "   ",
        print head,

    if module.used == 0:
        level_cur[level] += 1
        print(module.name + " [" + bcolors.OKGREEN + "0/0" + bcolors.ENDC + "]")
        return

    childnum = len(module.child)
    if int(module.used) == int(childnum):
        level_cur[level] += 1
        print(module.name + " [" + bcolors.OKGREEN + \
                str(childnum) + "/" + str(module.used) + \
                bcolors.ENDC + "]")
        level_max[level+1] = len(module.child)
        level_cur[level+1] = 0
        for c in module.child:
            printModuleTree(c, level+1)
    else:
        level_cur[level] += 1
        print(module.name + " [" + bcolors.FAIL + \
                str(childnum) + "/" + str(module.used) + \
                bcolors.ENDC + "]")
        level_max[level+1] = len(module.child)
        level_cur[level+1] = 0
        for c in module.child:
            printModuleTree(c, level+1)

def main():
    m = loadModuleTree(sys.argv[1])
    printModuleTree(m,0)

if __name__ == '__main__':
    main()
