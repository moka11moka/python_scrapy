from selenium import webdriver
import time
browser = webdriver.Chrome() #声明浏览器驱动对象
browser.get('https://www.zhihu.com/explore')
try:
    print(browser.page_source)
    input = browser.find_element_by_id('q')
    input.send_keys('iPhone')
    time.sleep(1)
    input.clear()
    input.send_keys('iPad')

    button = browser.find_element_by_class_name('btn-search')
    button.click()




finally:
    browser.close()