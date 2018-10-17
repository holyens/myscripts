# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:04:00 2018
function: 分析RSS改变
@author: zxc17
"""
import re,mutils
import numpy as np
#import matplotlib.pyplot as plt

class WlanDataHelper:
    (id,bssid,rssi,chan,timestamp,cols) = (0,1,2,3,4,5)
    rssi_defval = -100
    channel_defval = 0

    def __init__(self, inDir='.', inFilename='',outDir='.',outFilePrefix='out'):
        self.inDir = inDir.rstrip('/')
        self.inFilename = inFilename
        self.outDir = outDir.rstrip('/')
        self.outFilePrefix = outFilePrefix

    def readFile(self):
        self.data = [[],[],[],[],[]]
        with open(self.inDir+'/'+self.inFilename,'r') as fpsrc:
        #if os.path.getsize(srcfile)<100*1024*1024:
            for line in fpsrc:     
                res = [f(s) for f,s in zip((int,str,int,int,int), line.split(' '))]
                for i in range(WlanDataHelper.cols):
                    self.data[i].append(res[i])
        return len(self.data[0])

    def getBssidSet(self):
        self.bssidset = {e:index for index,e in enumerate(sorted(set(self.data[WlanDataHelper.bssid])))}
        return len(self.bssidset)

    def getRCTArray(self):
        self.rssiArray = np.zeros((self.data[WlanDataHelper.id][-1]+1, len(self.bssidset)),np.int32)+WlanDataHelper.rssi_defval
        self.channelArray = np.zeros((self.data[WlanDataHelper.id][-1]+1, len(self.bssidset)),np.int32)+WlanDataHelper.channel_defval
        self.timeVector = np.zeros((self.data[WlanDataHelper.id][-1]+1),np.int64)
        for i in range(len(self.data[WlanDataHelper.id])):
            idx = [self.data[WlanDataHelper.id][i],self.bssidset[ self.data[WlanDataHelper.bssid][i] ]]
            self.rssiArray[idx[0]][idx[1]] = self.data[WlanDataHelper.rssi][i]
            self.channelArray[idx[0]][idx[1]] = self.data[WlanDataHelper.chan][i]
            self.timeVector[idx[0]] = self.data[WlanDataHelper.timestamp][i]
        return self.rssiArray.shape
    def getChangeData(self):
        lastidx = 0
        self.change_list = []
        for i in range(1,self.rssiArray.shape[0]):
            if not (self.rssiArray[i]==self.rssiArray[lastidx]).all() :
                self.change_list.append((i, i-lastidx, self.timeVector[i]-self.timeVector[lastidx]))
                lastidx = i
        # (ave_id, ave_time) = ( np.average(np.array(tl)[:,1]), np.average(np.array(tl)[:,2]) )
        return len(self.change_list)

    def analyzeRssiChangeOnId(self):        
        total_num = len(self.change_list)
        id_diff_vector = np.array(self.change_list)[:,1]
        id_diff_set = set(id_diff_vector.tolist())
        statis = []
        for em in id_diff_set:
            statis.append ((em, np.sum(id_diff_vector == em)/total_num*100))
        (id_diff, prop) = ([x for (x,y) in statis], [y for (x,y) in statis])
        # plt.bar(x,y)
        regf = re.compile(r'^.*/(\w+)/([^/]+)\.\w+$')
        # plt.title('  '.join(regf.findall(srcfile)[0]))
        # plt.xlabel('id nterval')
        # plt.ylabel('(%)')
        plt.show()

    def analyzeRssiChangeOnTime(self):
        plt.hist(np.array(self.change_list)[:,2])
        plt.title('  '.join(regf.findall(srcfile)[0]))
        plt.xlabel('time nterval (ms)')
        plt.ylabel('(%)')
        plt.show()

    def getMultChannelAP(self):
        multchannelAP = []
        channel_list = np.transpose(self.channelArray).tolist()
        for i in range(len(channel_list)):
            tmp = set(channel_list[i])
            if WlanDataHelper.channel_defval in tmp:
                tmp.remove(WlanDataHelper.channel_defval)
            multchannelAP.append((i, tmp))
        return len(multchannelAP)

    def analyzeRssiLoss(self):
        total_num = self.rssiArray.shape[0]
        self.lossVector = np.sum(self.rssiArray==WlanDataHelper.rssi_defval, axis=0)/total_num
        return np.mean(self.lossVector)

    def write2csv(self, tag, list):
        with open(self.outDir+'/'+self.outFilePrefix+tag+'.csv', 'w') as fpdst:
            for e in list:
                line =  ','.join(e)+'\n'
                fpdst.write(line)
        return True
    
    def writeLoss2csv(self):
        list=[]
        for i,bssid in enumerate(self.bssidset):
            list.append((bssid, str(self.lossVector[i])))
        # sort
        list.sort(key=lambda tpl: tpl[1], reverse=False)    
        return self.write2csv('loss', list)
    
