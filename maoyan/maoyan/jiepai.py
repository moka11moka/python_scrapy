#requests得到索引页
import re
from hashlib import md5
from urllib.parse import urlencode
import os
import requests
from requests.exceptions import RequestException
import json
import pymongo
from bs4 import BeautifulSoup
from maoyan.config_mongo import *

#声明一个mongodb对象
client = pymongo.MongoClient(MONGO_URL)
#声明一个数据库
db = client[MONGO_DB]


def get_index_page(offset,keyword):
    #url后面的参数
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,
        'from':'gallery'
    }
    # urllib库提供的编码方法,可以将字典形式转化为url后面的参数
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  #得到json
        return None
    except RequestException:
        print('请求索引页出错')
        return None

#对得到的json进行解析
def parse_page_index(html):
    data = json.loads(html) #生成一个json对象
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

#根据索引页得到详细页
def get_page_detail(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text  #得到json
        return None
    except RequestException:
        print('请求详细页出错',url)
        return None

#解析详细页面
def parse_page_detail(html):
    soup = BeautifulSoup(html,'lxml') #定义BeautifulSoup将title解析出来,lxml是一种解析方式
    title = soup.select('title')[0].get_text() #提出名称
    print(title)
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
    result_tmp = re.search(images_pattern,html)
    if result_tmp:
        result = re.sub(r'\\', '', result_tmp.group(1)) #要求比较正规的字典格式,group(1)定义第一个括号的内容
        data = json.loads(result) #正则表达式第一个括号的内容
        print(data)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images] #遍历sub_images
            for image in images:
                download_image(image)
            return {
                'title':title,
                'images':images
            }            #返回形式,存在mongodb中

#声明存储在mongodb的方法
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功....',result)
        return True
    return False

#download对应图片
def download_image(url):
    print('正在下载',url)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            save_image(response.content) #content返回二进制内容,存储图片
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

#存储图片
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg') #保存当前路径,防止重复,
    print(os.getcwd()) #当前路径
    if not os.path.exists(file_path):#如果图片不存在
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()


def main():
    html = get_index_page(20,'街拍')
    #print(html)
    html = get_page_detail('https://www.toutiao.com/a6503682001730535950/')
    if html:
        result = parse_page_detail(html)
        save_to_mongo(result)
if __name__== '__main__':
    main()



