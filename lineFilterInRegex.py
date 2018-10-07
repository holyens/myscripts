# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:04:00 2018
function: 根据正则表达式过滤日志型文件，并将结果保存到新文件中
@author: zxc17
"""
import re
srcfile = 'C:/Users/admin/Documents/Tencent Files/644026981/FileRecv/MobileFile/host_driver_logs_current.txt'
desfile = 'E:/xstt.csv'
regs = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{6}).+?\[(\d{2}:\d{2}:\d{2}\.\d{6})\].+?wmi_scan_event.+?scan_id (\d+), freq (\d+)')
#regd = re.compile(r'WiFi[ \t]*:[ \t]*([-_/\w]+)[ \t]*?')

fpdes = open(desfile,'w')
with open(srcfile,'r') as fpsrc:
    #if os.path.getsize(srcfile)<100*1024*1024:
    for line in fpsrc:
        resline = regs.findall(line) #默认一行最多出现一次匹配
        if(len(resline)>0):
            resline = resline[0]
            #print(','.join(resline))
            fpdes.write(','.join(resline)+'\n')
fpdes.close
print('done...')
