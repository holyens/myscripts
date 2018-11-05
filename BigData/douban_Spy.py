# 豆瓣爬虫，评论
import io,sys
import requests,struct,socket,re,html
from bs4 import BeautifulSoup
# Setup
whitespace = re.compile(r'(?:\n| |\r|:|<.*?>|&nbsp;)',re.S)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
# Get html
s = requests.Session()
id = '2868943'
url = 'https://www.douban.com/people/%s/' % id
#html = s.get(url).text
html = '''<div class=" " id="book">
    
    
    <h2>
        冷眼探花郎的书
            &nbsp;·&nbsp;·&nbsp;·&nbsp;·&nbsp;·&nbsp;·
            <span class="pl">&nbsp;(
                
                <a href="https://book.douban.com/people/langyiqun/do" target="_blank">9本在读</a>&nbsp;·&nbsp;<a href="https://book.douban.com/people/langyiqun/wish" target="_blank">30本想读</a>&nbsp;·&nbsp;<a href="https://book.douban.com/people/langyiqun/collect" target="_blank">493本读过</a>
                ) </span>
    </h2>


    
    
            <div class="obssin">
                <div class="substatus">在读</div>
                <ul><li class="aob"><a href="https://book.douban.com/subject/26949777/" title="曾国藩" target="_blank"><img src="https://img3.doubanio.com/view/subject/l/public/s29265736.jpg" class="climg" alt="曾国藩"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/26984949/" title="地下铁道

The Underground Railroad" target="_blank"><img src="https://img1.doubanio.com/view/subject/l/public/s29385647.jpg" class="climg" alt="地下铁道"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/25904820/" title="中国的内战

Civil War in China:The Political Struggle 1945-1949" target="_blank"><img src="https://img3.doubanio.com/view/subject/l/public/s27470110.jpg" class="climg" alt="中国的内战"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/6861234/" title="伤寒论辑义" target="_blank"><img src="https://img3.doubanio.com/view/subject/l/public/s6981925.jpg" class="climg" alt="伤寒论辑义"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/3927613/" title="金匮要略集注" target="_blank"><img src="https://img1.doubanio.com/view/subject/l/public/s4668729.jpg" class="climg" alt="金匮要略集注"></a></li>
            </ul>
            <div class="clear"></div></div>
        
    
            <div class="obssin">
                <div class="substatus">想读</div>
                <ul><li class="aob"><a href="https://book.douban.com/subject/1948429/" title="诗人

The Poet" target="_blank"><img src="https://img1.doubanio.com/view/subject/l/public/s1964928.jpg" class="climg" alt="诗人"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/30277466/" title="南宋行暮" target="_blank"><img src="https://img3.doubanio.com/view/subject/l/public/s29854676.jpg" class="climg" alt="南宋行暮"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/30207663/" title="茶的真实历史

The True History of Tea" target="_blank"><img src="https://img1.doubanio.com/view/subject/l/public/s29753408.jpg" class="climg" alt="茶的真实历史"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/1126213/" title="道教史发微" target="_blank"><img src="https://img3.doubanio.com/view/subject/l/public/s1098952.jpg" class="climg" alt="道教史发微"></a></li>
            <li class="aob"><a href="https://book.douban.com/subject/26864984/" title="金色梦乡

ゴールデンスランバー" target="_blank"><img src="https://img3.doubanio.com/view/subject/l/public/s29860726.jpg" class="climg" alt="金色梦乡"></a></li>
            </ul>
            <div class="clear"></div></div>
        
    
    


    </div>
'''
print(len(html))
# print(html)
with open('G:/BigData/data/test.txt','w') as fp:
    #fp.writelines(content)
    pass
# DOM
soup=BeautifulSoup(html,'lxml')

dic = {
    #'id': id,
    #'nick': list(soup.h1.children)[0].strip(),
    #'signature': soup.h1.div.string.strip(),
    'book-do': soup.find_all(name='div',attrs={'id':'book'})[0].h2.span.a
    
}

print(dic)
