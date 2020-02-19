from bs4 import BeautifulSoup
import requests
import time  # 导入相应的库文件
from  lxml import etree
import re
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='python', db='mydb', port=3306, charset='utf8')
cursor = conn.cursor()  #连接数据库及光标


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
}  # 'User-Agent'务必要加' '，否则出错


# 在北京家电脑的浏览器headers是   Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
# (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36
# 原有备份  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
# (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

def judgment_sex(class_name):  # 定义判断用户性别的函数
    if class_name == ['member_icol']:
        return '女'
    else:
        return '男'


def get_links(url):  # 定义获取详细页 URL 的函数
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#page_list > ul > li > a')  # links为URL列表
    for link in links:
        href = link.get("href")
        get_info(href)  # 循环出的URL，依次调用get_info()函数
        print(href)


def get_info(url):  # 定义获取网页信息的函数
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('div.pho_info > h4')
    addresses = soup.select('div.con_l > div.pho_info > p > span')
    prices = soup.select('#scrollPrice > div.fl > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')



    for title, address, price, img, name, sex in zip(titles, addresses, prices, imgs, names, sexs):
        data = {
            'title': title.get_text().strip(),
            'address': address.get_text().strip(),
            'price': price.get_text(),
            'img': img.get("src"),
            'name': name.get_text(),
            'sex': judgment_sex(sex.get("class"))
        }
        print(data)  # 获取信息并通过字典的信息打印
        cursor.execute(
            "insert into xiaozhuzufang (title,address,price,img,name,sex) values(%s,%s,%s,%s,%s,%s)",
            (str(title), str(address), str(price), str(img), str(name), str(sex))
        )  # 获取信息插入数据库


if __name__ == '__main__':
    urls = ['https://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in
            range(1,14)]  # 构造多页URL
    for single_url in urls:
        get_links(single_url)  # 循环调用 get_links()函数
        time.sleep(2)  # 睡眠2秒
    conn.commit()

