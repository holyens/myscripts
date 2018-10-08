import re
def write2csv(filename, list):
    fp = open(filename, 'w')
    for tp in list:
        fp.write(','.join(map(str,tp))+'\n')
    fp.close
    return

def getOutFilename(inFilename, outPrefix, outExt='csv'):
    regf = re.compile(r'^(.*)(/)([^/]+\.)(\w+)$')
    s = regf.findall(inFilename)[0]
    return ''.join([s[0],s[1],outPrefix,s[2],outExt])
