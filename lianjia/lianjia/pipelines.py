# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class LianjiaPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['lianjia']
        self.zufang = self.db['zufang']


    def process_item(self, item, spider):
        self.zufang.insert_one(item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self,spider):
        self.client.close()