import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}  # 'User-Agent'务必要加"，否则出错
res = requests.get('http://bj.xiaozhu.com', headers=headers)  # 网站为小猪短租网北京地区网址，get方法加入请求头
soup = BeautifulSoup(res.text, 'html.parser')  # 对返回的结果进行解析
prices = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > div:nth-child(1) > span > i')
                                        #d定位元素位置并通过selector方法提取.  li:nth-child(1)改为li
for price in prices:      #此时prices为列表，需循环遍历
    print(price.get_text())      #通过get_text()方法获取文字信息
#print(soup.prettify())
'''try:
    print(res)  # pycharm中返回结果为
except ConnectionError:     #出现错误会执行下面的操作
    print(res.text)'''
