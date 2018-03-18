import requests
from bs4 import BeautifulSoup

html = requests.get('https://www.baidu.com/')
#print(html.text)
soup = BeautifulSoup(html.content,'lxml')
print(soup)