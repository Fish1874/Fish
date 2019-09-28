# -*- coding: utf-8 -*-
import scrapy


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['gz.lianjia.com']
    start_urls = ['http://gz.lianjia.com/zufang/pg{}'.format(i) for i in range(1,2)]

    def parse(self, response):
        urls = response.xpath('//div[@class="content__list--item"]/a/@href').extract()
        for url in urls:
            url = 'http://gz.lianjia.com' + url
            yield scrapy.Request(url,callback=self.parse_info)

    def parse_info(self,response):
        total_price = response.xpath('//div[@class="wrapper"]//p[@class="content__title"]/text()').extract_first()
        moneys = response.xpath('//div[@class="wrapper"]//p[@class="content__aside--title"]/span/text()').extract_first()
        facilitie = response.xpath('//ul[@class="content__article__info2"]//text()').getall()
        image = response.xpath('//ul[@class="content__article__slide__wrapper"]//img/@src').getall()
        money = moneys + '元/月'
        facilities = [x.strip() for x in facilitie if x.strip()!='']
        yield {
            '标题':total_price,
            '价钱':money,
            '设施':facilities,
            '图片':image
        }