import re


import requests

#  得到猫眼的源码
def film_page(url):
    response = requests.get(url).text
    if response:
        return response
    else:
        return None


#  正则表达式解析网页
def analyse_code(html):
    #pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?data-src="(.*?)".*?<a.*?>(.*?)</a>.*?'
                         #+'<p.*?>主演：(.*?).*?上映时间：(.*?)</p>.*?"integer">(.*?).*?"fraction">(.*?)</i></p>.*?</dd>',re.S)

    pattern = re.compile('title="(.*?)"',re.S)
    text = re.findall(pattern,html)
    return text





if __name__ == "__main__":
    web_page = film_page('http://maoyan.com/board/4')
    #print(analyse_code(web_page))
    print(web_page)
    #print(analyse_code(web_page))