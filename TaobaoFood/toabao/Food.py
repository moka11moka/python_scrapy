import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from toabao.config import *
import pymongo

# 如果失败,是缺少ChromeDriver

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400,900)

#连接mongodb
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

#向搜索框输入美食,然后点击提交
def search():
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        return search()

#进行翻页操作
def next_page(page_num):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()#记得要有清除操作
        input.send_keys(page_num)
        submit.click()
        #判定页码是不是在反转的页面上
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_num)))
        get_food()
    except TimeoutException:
        return next_page(page_num)

#获取图片信息
def get_food():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    #得到图片对应标签下的信息
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
    print(product)
    save_to_mongo(product)

#保存mongodb

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到mongodb失败', result)


def main():
    try:
        total = search()
        #得到页面数
        total = int(re.compile('(\d+)').search(total).group(1))
        for page_num in range(2, total-2):
            next_page(page_num)
        print(total)
    finally:
        browser.close()


if __name__ == '__main__':
    main()


