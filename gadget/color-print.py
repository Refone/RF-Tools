#!/usr/bin/env python
#coding:utf-8
# Filename: systemstatus.py

import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    INVERSE = '\033[7m'
    UNDERLINE = '\033[4m'

def main():
    print bcolors.INVERSE + "Warning: No active frommets remain. Continue?"+bcolors.ENDC
    print "["+bcolors.OKGREEN+"+" +bcolors.ENDC+"]" + "ENTRY" 
    print "["+bcolors.FAIL+"●" +bcolors.ENDC+"]" + "ENTRY" 
    
if __name__ == "__main__":
    main()

"""
格式：\033[显示方式;前景色;背景色m
 
 说明：
 前景色            背景色           颜色
 ---------------------------------------
 30                40              黑色
 31                41              红色
 32                42              绿色
 33                43              黃色
 34                44              蓝色
 35                45              紫红色
 36                46              青蓝色
 37                47              白色
 显示方式           意义
 -------------------------
 0                终端默认设置
 1                高亮显示
 4                使用下划线
 5                闪烁
 7                反白显示
 8                不可见
  
  例子：
  \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
  \033[0m          <!--采用终端默认设置，即取消颜色设置-->
  """
