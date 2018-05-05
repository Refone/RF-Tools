#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import json
from colorprint import Bcolors
from collections import defaultdict
from interaction import *

bcolors = Bcolors()

class tags:
    SUBENTRY = "["+bcolors.FAIL+"+" +bcolors.ENDC+"] "
    ENTRY = "["+bcolors.OKGREEN+"●" +bcolors.ENDC+"] "

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
        print "LoadGrub Failed.\"/boot/grub/grub.cfg\" Not Found."
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
            if root['child'][i]['type'] == "submenu":
                print(" "*(4*l) + tags.SUBENTRY + \
                        bcolors.INVERSE + \
                        root['child'][i]['name'] + \
                        bcolors.ENDC)
                if l+1<len(p):
                    printEntry(root['child'][i], p, l+1)
            else:
                print(" "*(4*l) + tags.ENTRY + \
                        bcolors.INVERSE + \
                        root['child'][i]['name'] + \
                        bcolors.ENDC)
        else:
            if root['child'][i]['type'] == "submenu":
                print(" "*(4*l) + tags.SUBENTRY + \
                        root['child'][i]['name'])
            else:
                print(" "*(4*l) + tags.ENTRY + \
                        root['child'][i]['name'])

def getEntry(root, p):
    e = root
    for i in range(0, len(p)):
        idx = p[i]
        e = e['child'][idx]
    return e

def checkDefault():
    # Check "/etc/default/grub" GRUB_DEFAULT=saved
    # OK: return 1; NOOK: return 0.
    try:
        f = open('/etc/default/grub', 'r')
    except IOError:
        print "CheckDefault Failed.\"/etc/default/grub\" Not Found."
        return 0

    for eachLine in f.readlines():
        r = re.findall(r'^\s*GRUB_DEFAULT\s*=\s*[\'\"]?(\w+)[\'\"]?', eachLine)
        if r:
            if r[0]=='saved':
                return 1
            else:
                return 0

    return 0

def reboot():
    while True:
        answer = raw_input(bcolors.BOLD + \
                "Reboot now? [Y/n]" + \
                bcolors.ENDC )
        if answer=="y" or answer=="Y" or answer=="yes" or answer=="":
            os.system("sudo reboot")
            return
        elif answer=="n" or answer=="N" or answer=="no":
            return
        else:
            continue

def setEntry(path):
    # set entry succeed:    return 1
    # grub-reboot disable:  return 1
    # set entry failed:     retuen 0
    global entry
    
    print ""
    if not checkDefault():
        print bcolors.WARNING + \
                "Please change the following setting in " + bcolors.ENDC + \
                bcolors.BOLD + "/etc/default/grub:" + \
                bcolors.ENDC
        print ""
        print bcolors.BOLD + "GRUB_DEFAULT" + bcolors.ENDC +\
                " = " + \
                bcolors.OKGREEN + "saved" + bcolors.ENDC
        print ""
        print "And then " + \
                bcolors.BOLD + "sudo update-grub" + bcolors.ENDC
        return 1

    p_str = ""
    for i in range(0,len(path)-1):
        p_str += str(path[i])
        p_str += ">"
    p_str += str(path[len(path)-1])

    cmd = "sudo grub-reboot " + "\"" + p_str + "\""
    
    while True:
        answer = raw_input(bcolors.BOLD + \
                "Change the Selected Entry? [Y/n]" + \
                bcolors.ENDC )
        if answer=="y" or answer=="Y" or answer=="yes" or answer=="":
            print bcolors.OKGREEN + cmd + bcolors.ENDC
            os.system(cmd)
            reboot()
            print bcolors.OKGREEN + \
                    "Grub Entry has changed to:" + \
                    bcolors.ENDC
            print bcolors.BOLD + \
                    getEntry(entry, path)['name'] + \
                    bcolors.ENDC
            return 1
        elif answer=="n" or answer=="N" or answer=="no":
            return 0
        else:
            continue

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

        if k==1:                    # Up
            p = path.pop()
            p = max(0, p-1)
            path.append(p)
            continue
        if k==2:                    # Down
            p = path.pop()
            p = min(getEntry(entry, path)['childnum']-1, p+1)
            path.append(p)
            continue
        if k==3 or k==5:            # Right & Enter
            if getEntry(entry, path)['type']=='submenu':
                path.append(0)
                continue
            else:
                if setEntry(path)==0:
                    continue
                else:
                    break
        if k==4:                    # Left
            if len(path)>1:
                path.pop()
            continue
        if k==6:                    # q
            break

def main():
    loadGrub()
    menu()
    #showGrub()

if __name__ == '__main__':
    main()
