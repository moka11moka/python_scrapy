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
driver.get('https://hotel.qunar.com/city/shanghai_city/#fromDate=2018-03-06&cityurl=shanghai_city&from=qunarHotel&toDate=2018-03-07')
wait = WebDriverWait(driver, 10)
for i in range(1, 20):
    submit = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '#searchHotelPanel > div.b_tool.clr_after > div.pager.js_pager > div > ul > li.item.next > a > span:nth-child(1)')))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit.click()
    print(submit)
    time.sleep(1)