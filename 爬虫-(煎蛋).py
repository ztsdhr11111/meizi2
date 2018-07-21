#导包
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import re
import os
import requests

#声明浏览器对象
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

#模拟浏览器访问网页
def index_page(page):
    print('正在爬取第',page,'页')
    try:
        url = 'http://jandan.net/ooxx/page-' + str(page)
        browser.get(url)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#wrapper #content .comments div.cp-pagenavi > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wrapper #content .commentlist .row')))
        get_image()
    except TimeoutException:
        index_page(page)

#获取图片地址
def get_image():
    html = browser.page_source
    doc = pq(html)
    div = doc('#wrapper #content .commentlist .row .text')
    urls = re.findall('[a-zA-Z]+://[^\s]*jpg|[A-Za-z]+://[^\s]*gif', str(div))
    for url in urls:
        save_image(url)

#保存图片
def save_image(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        file_path = url.split('/')[-1]
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(r.content)
                print('保存成功')
        else:
            print('文件已经有了，还想要更多自己再去找找吧')

    except requests.ConnectionError:
        print('你的梦想破灭了')
            
    
        
def main():
    for i in range(1, 100):
        index_page(i)

        

        

