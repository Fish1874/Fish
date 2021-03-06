# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class DoubanPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['douban']
        self.top250 = self.db['Top250']

    def process_item(self, item, spider):
        content = dict(item)
        self.top250.insert(content)
        return item

    def open_spider(self,spider):
        pass

    def close_spider(self,spider):
        self.client.close()