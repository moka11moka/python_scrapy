import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)


#得到百度首页并且按视频按钮
def search():
    try:
        browser.get('https://www.baidu.com')
        vedio_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#u_sp > a:nth-child(4)')))
        vedio_link.click()
        print('按视频按钮完成.....')
    except TimeoutException:
        return search()

def main():
    search()

if __name__ == '__main__':
    main()