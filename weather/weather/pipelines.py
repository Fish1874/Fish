# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class WeatherPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['weather']
        self.weather = self.db['cnweather']

    def process_item(self, item, spider):
        self.weather.insert(item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()