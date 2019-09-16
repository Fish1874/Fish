# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250?']

    def parse(self, response):
        for item in response.css('.item'):
            movie = DoubanItem()
            movie['title'] = item.css('.hd span.title::text').extract_first()
            movie['staring'] = item.css('.bd p::text').extract_first()
            movie['star'] = item.css('.star span.rating_num::text').extract_first()
            movie['quote'] = item.css('.quote span.inq::text').extract_first()
            movie['url'] = item.css('.pic a::attr("href")').extract_first()
            movie['image_url'] = item.css('.pic img::attr("src")').extract_first()

            yield movie

        #下一页
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = response.urljoin(next_url)
            yield scrapy.Request(url=url,callback=self.parse)