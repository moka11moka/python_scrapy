# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from Scrapy_Project.items import DoubanItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    rules = [
        # r防止字符转义 follow=False表示不再继续找类似的url
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),
        callback='parse_item', follow=False)
     ]

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanItem()
        item['name'] = sel.xpath(".//*[@id='content']/h1/span[1]/text()").extract()
        item['year'] = sel.xpath(".//*[@id='content']/h1/span[2]/text()").extract()
        item['score'] = sel.xpath(".//*[@id='interest_sectl']/div[1]/div[2]/strong/text()").extract()
        item['director'] = sel.xpath(".//*[@id='info']/span[1]/span[2]/a/text()").extract()
        item['actors'] = sel.xpath(".//*[@id='info']/span[3]//a/text()").extract()
        item['classify'] = sel.xpath(".//span[@property='v:genre']/text()").extract()
        item['image_urls'] = sel.xpath(".//*[@id='mainpic']/a[@class='nbgnbg']/img/@src").extract()
        yield item
