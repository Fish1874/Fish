# -*- coding: utf-8 -*-
import scrapy

class CnweatherSpider(scrapy.Spider):
    name = 'cnweather'
    allowed_domains = ['tianqi.com']
    start_urls = ['https://lishi.tianqi.com/']

    def parse(self, response):
        city_url = []
        city_name = []
        for alpha in [chr(i) for i in range(65,91)]:  #随机生成数，65-91对应字母A-Z
            city_url.extend(response.xpath('//ul[@id="city_{}"]/li/a/@href'.format(alpha)).getall()[1:])
            city_name.extend(response.xpath('//ul[@id="city_{}"]/li/a/text()'.format(alpha)).getall()[1:])
        for i in range(len(city_url)):
            yield scrapy.Request(city_url[i],callback=self.parse_info1,meta={'city':city_name[i]})

    def parse_info1(self,response):
        detail_href = response.xpath('//div[@class="tqtongji1"]/ul/li/a/@href').getall()[:-20]
        # print(detail_href)
        for href in detail_href:
            yield scrapy.Request(href,callback=self.parse_info2,meta=response.meta)

    def parse_info2(self,response):
        date = response.xpath('//div[@class="tqtongji2"]/ul/li[1]/a/text()').getall()
        high_temp = response.xpath('//div[@class="tqtongji2"]/ul/li[2]/text()').getall()[1:]
        low_temp = response.xpath('//div[@class="tqtongji2"]/ul/li[3]/text()').getall()[1:]
        weather = response.xpath('//div[@class="tqtongji2"]/ul/li[4]/text()').extract()[1:]
        for i in range(len(date)):
            yield {
                '城市': response.meta['city'],
                '日期': date[i],
                '最高气温': high_temp[i],
                '最低气温': low_temp[i],
                '天气': weather[i]
            }