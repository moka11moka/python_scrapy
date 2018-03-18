#coding:utf8
import codecs

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from bs4 import BeautifulSoup
import pymongo
from qunar.config import *
import os

driver = webdriver.Chrome()
driver.get('https://www.qunar.com/')
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
wait = WebDriverWait(driver, 10)

def search(toCity,fromDate,toDate):
    try:
        hotel_link = driver.find_element_by_link_text('酒店')
        hotel_link.click()
        driver.implicitly_wait(2)
        ele_tocity = driver.find_element_by_id('toCity')
        ele_fromdate = driver.find_element_by_name('fromDate')
        ele_todate = driver.find_element_by_name('toDate')
        ele_submit = driver.find_element_by_class_name('search-btn')
        ele_tocity.clear()
        ele_tocity.send_keys(toCity)
        ele_fromdate.clear()
        ele_fromdate.send_keys(fromDate)
        ele_todate.clear()
        ele_todate.send_keys(toDate)
        time.sleep(4)
        ele_submit.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        infos = soup.find_all(class_='item_hotel_info')
        for i in range(2, 10):
            submit = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,'#searchHotelPanel > div.b_tool.clr_after > div.pager.js_pager > div > ul > li.item.next > a > span:nth-child(1)')))
            submit.click()
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            info = soup.find_all(class_='item_hotel_info')
            #print(info)
            infos.append(info)
        print(infos)
        print(type(infos))
        return infos
    except TimeoutException:
        return search()

#解析html
def analyse_html():
    html= search('上海', '2018-03-06', '2018-03-07')
    name_list = []
    price_list = []
    address_list = []
    for h1 in html:
        soup = BeautifulSoup(str(h1), 'lxml')
        hotel_html = soup.find_all(class_='hotel_item')
        hotel_price = soup.find_all(class_='js_list_price')
        hotel_address = soup.find_all(class_='area_contair')
        for name1 in hotel_html:
            name = name1.a.text
            name_list.append(name)

        for price1 in hotel_price:
            price = price1.cite.text + price1.b.text
            price = re.sub('，', '', price)
            price_list.append(price)

        for address1 in hotel_address:
            address = address1.em.text
            address = re.sub('，', '', address)
            address_list.append(address)

    hotel = zip(name_list, address_list, price_list)
    file_path = os.getcwd()+'\hotel.txt'
    f = open(file_path, 'w+', encoding='utf-8')
    for name,address,price in hotel:
        result = {
            'name':name,
            'address':address,
            'price':price
        }
        for key, value in result.items():
            print(key, value)
            f.write(str(key) + ':' + str(value) + "\n")
        saveToMongo(result)
    f.close()



    #print(result)
global index
index = 1
def next_page(page_num):
    analyse_html()
    try:
        for i in range(1, page_num):
            index = index + 1
            submit = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,'#searchHotelPanel > div.b_tool.clr_after > div.pager.js_pager > div > ul > li.item.next > a > span:nth-child(1)')))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            submit.click()
            analyse_html()
            time.sleep(2)
    except Exception:
        return next_page(page_num)

#存储到mongodb
def saveToMongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
           print('插入mongodb成功')
    except Exception:
        print('插入mongodb失败')


def main():
    analyse_html()


if __name__ == '__main__':
    main()