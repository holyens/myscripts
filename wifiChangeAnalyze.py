# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:04:00 2018
function: 分析RSS改变
@author: zxc17
"""
import re,mutils
import numpy as np,xlwt
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
print('start:')
# 全局参数
iswrite = False
srcfile = 'G:/libdata3/async1/mi5.txt'
print(srcfile)
# 读入WLAN数据
list = [[],[],[],[],[]]
(id,bssid,rssi,chan,timestamp,cols) = (0,1,2,3,4,5)
with open(srcfile,'r') as fpsrc:
    #if os.path.getsize(srcfile)<100*1024*1024:
    for line in fpsrc:        
        res = [f(s) for f,s in zip((int,str,int,int,int), line.split(' '))]
        for i in range(cols):
            list[i].append(res[i])
        #fpdes.write(','.join(resline)+'\n')
# 生成BSSID集合
bssids = {e:index for index,e in enumerate(sorted(set(list[bssid])))}        
print('#read:',len(list[id]),'rows, maxid:',list[0][-1],'AP number:',len(bssids))

# 以（采集次数，AP数）为（行，列）生成RSSI与CHANNEL矩阵
rssis = np.zeros((list[id][-1]+1, len(bssids)),np.int32)-100
chans = np.zeros((list[id][-1]+1, len(bssids)),np.int32)
times = np.zeros((list[id][-1]+1),np.int64)
for i in range(len(list[id])):
    idx = [list[id][i],bssids[ list[bssid][i] ]]
    rssis[idx[0]][idx[1]] = list[rssi][i]
    chans[idx[0]][idx[1]] = list[chan][i]
    times[idx[0]] = list[timestamp][i]
print('rssi size:',rssis.shape)    
# 将矩阵写入csv文件
if iswrite:
    mutils.write2csv(mutils.getOutFilename(srcfile,'rssi_','csv'), rssis.tolist())
    mutils.write2csv(mutils.getOutFilename(srcfile,'chan_','csv'), chans.tolist())
print('#write:',mutils.getOutFilename(srcfile,'rssi_','csv'))
print('#write:',mutils.getOutFilename(srcfile,'chan_','csv'))
# 分析RSSI发生变化的平均时间
lastidx = 0
tl = []
for i in range(1,rssis.shape[0]):
    if not (rssis[i]==rssis[lastidx]).all() :
        tl.append((i, i-lastidx, times[i]-times[lastidx]))
        lastidx = i
(ave_id, ave_time) = ( np.average(np.array(tl)[:,1]), np.average(np.array(tl)[:,2]) )
print('changed times:',len(tl),'ave_id:',ave_id,'ave_time:',ave_time)
if iswrite:
    mutils.write2csv(mutils.getOutFilename(srcfile,'change_','csv'), tl)
charr = np.array(tl)[:,1]
total_num = len(tl)
tm = set(charr.tolist())
stats = []
for em in tm:
    stats.append ((em, np.sum(charr == em)/total_num*100))
(x,y) = ([x for (x,y) in stats], [y for (x,y) in stats])
# plt.bar(x,y)
regf = re.compile(r'^.*/(\w+)/([^/]+)\.\w+$')
# plt.title('  '.join(regf.findall(srcfile)[0]))
# plt.xlabel('id nterval')

plt.hist(np.array(tl)[:,2])
plt.title('  '.join(regf.findall(srcfile)[0]))
plt.xlabel('time nterval (ms)')
#plt.ylabel('(%)')
plt.show()
#print(charr)
#print(stats)


# 分析同一AP是否会自动切换channel
chanschanged = []
chanslist = np.transpose(chans).tolist()
for i in range(len(chanslist)):
    tmp = set(chanslist[i])
    if 0 in tmp:
        tmp.remove(0)
    chanschanged.append(tmp)
    if len(tmp)>1:
        print(' AP:', i, tmp)

print('\ndone...')


