from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '''<li><a href=http://www.cnblogs.com/v-July-v/>结构算法July</a></li>
              <li><a href=https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-software-engineering>NUS 科技硕士官网</a></li>
              <li><a href=http://quotes.toscrape.com/>官网scrapy测试网站</a></li>
              <li><a href=http://scrapy-chs.readthedocs.io/zh_CN/latest/>spider爬虫文档</a></li>
              <li><a href=https://www.cnblogs.com/sjjsxl/p/6285629.html>HMM前向后向算法</a></li>
              <li><a href=http://tushare.org>TuShare财经数据接口</a></li>
              <li><a href=http://blog.csdn.net/ruthywei/article/details/79070212>git命令的使用</a></li>
            '''

if __name__ == '__main__':
    app.run()