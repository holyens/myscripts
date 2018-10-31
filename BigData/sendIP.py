# 豆瓣爬虫，评论
import io,sys
import requests,struct,socket,re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
def extractInfo(content=''):
    title=re.findall(r'<h1>.*?<span.*?>(.*?)</span>.*?</h1>',content,re.S)[0]
    return (title)

s = requests.Session()
url = 'https://book.douban.com/subject/26853356/'
res = s.get(url)
html = res.content.decode("UTF-8")
print(len(html))
with open('G:/BigData/data/test.txt','w') as fp:
    #fp.writelines(str(html))
    pass
print(extractInfo(html)[0])



def post_ip():
    ips = get_ips()
    param = {'token': 'qaz', 'ips': ips}
    url = 'https://api.iotfan.net/other/recip.php'
    res = s.post(url, data=param)
    return res.content

#def main():
#    print(post_ip())

#if __name__ == "__main__":
#    main()
