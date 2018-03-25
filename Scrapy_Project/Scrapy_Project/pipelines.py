# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
    #通过图片的url返回一个Request对象
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item})  #meta生成一个request的浅拷贝

    def item_completed(self, results, item, info):
        image_url = [x['path'] for ok, x in results if ok]
        if not image_url:
            raise DropItem("Item contains no images")
        #item['image_path'] = image_path
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        name = item['name']
        filename = '{}.jpg'.format("".join(name))
        return filename