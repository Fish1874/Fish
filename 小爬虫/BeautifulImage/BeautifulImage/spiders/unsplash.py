# -*- coding: utf-8 -*-
import scrapy
from BeautifulImage.items import BeautifulimageItem
import json


class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['http://unsplash.com/napi/photos?page={}&per_page=12'.format(i) for i in range(5000)]

    def parse(self, response):
        play_url = json.loads(response.text)
        for download_url in play_url:
            image_url = download_url['links']['download']
            yield scrapy.Request(image_url,callback=self.parse_url)

    def parse_url(self,response):
        pic = BeautifulimageItem()
        image = response.body    #获得bytes类型
        pic['image'] = image
        yield pic