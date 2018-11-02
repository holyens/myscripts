# 豆瓣爬虫，评论
import io,sys
import requests,struct,socket,re,html,scrapy
whitespace = re.compile(r'(?:\n| |\r|:|<.*?>|&nbsp;)',re.S)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
def extractInfo(content=''):
    title=re.findall(r'<h1>.*?<span.*?>(.*?)</span>.*?</h1>',content,re.S)[0]
    info = re.findall(r'<div.*?id="info".*?>(.*?)</div>',content,re.S)[0]
    info_list = re.findall(r'<span class="pl".*?>(.*?):?</span>(.*?)(?:</span>)?<br/?>',info,re.S)
    info_dict={}
    for (key,val) in info_list:
        key = whitespace.sub('', key)
        val = whitespace.sub('', val)
        info_dict[key] = val
    return (title,info_dict)

def paserRating(content=''):
    title=re.findall(r'<h1>.*?<span.*?>(.*?)</span>.*?</h1>',content,re.S)[0]

    info = re.findall(r'<div.*?rel="v:rating">(.*?)</div>',content,re.S)[0]
    info_list = re.findall(r'<span class="pl".*?>(.*?):?</span>(.*?)(?:</span>)?<br/?>',info,re.S)
    info_dict={}
    for (key,val) in info_list:
        key = whitespace.sub('', key)
        val = whitespace.sub('', val)
        info_dict[key] = val
    return (title,info_dict)

s = requests.Session()
url = 'https://book.douban.com/subject/26425831/'
content = s.get(url).text
print(len(content))
with open('G:/BigData/data/test.txt','w') as fp:
    fp.writelines(content)
    pass
print(extractInfo(content))
