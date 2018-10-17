import WlanDataHelper as WDH,re,numpy as np
#import matplotlib.pyplot as plt

wdh = WDH.WlanDataHelper('G:/0927_三手机单点同步异步对比测试/async1','mi5.txt', \
                           'G:/0927_三手机单点同步异步对比测试/output', 'out_a_bn_' )
print('lines', wdh.readFile())
print('BSSID', wdh.getBssidSet())
print('RCT', wdh.getRCTArray())
print('Loss', wdh.analyzeRssiLoss())
print(wdh.lossVector,len(wdh.lossVector))
wdh.writeLoss2csv()
#print(wdh.bssidset)