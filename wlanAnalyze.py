import WlanDataHelper as WDH,re,numpy as np
#import matplotlib.pyplot as plt
phones=['hm', 'mi5', 'vivo']
ns=['2','3']
for si in phones: 
    for sj in ns:
        inFile = 'G:/1017_beacon间隔测试/%s/W%s.txt' %(si, sj)
        outFilePrefix = 'G:/1017_beacon间隔测试/output/out_%s_%s_' %(si, sj)
        print(inFile)
        wdh = WDH.WlanDataHelper(inFile, outFilePrefix)
        print('lines', wdh.readFile())
        wdh.getBssidSet()
        wdh.getRCTArray()
        wdh.analyzeRssiLoss()
        print(len(wdh.lossVector))
        wdh.writeLoss2csv()

#print(wdh.bssidset)