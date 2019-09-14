import requests
from lxml import etree
import json
import pymongo

class TiebaSpider:
    def __init__(self):
        self.url_temp = 'https://www.qiushibaike.com/imgrank/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
        	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0\
        	.2743.116 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8'}

    def get_url_list(self):
        url_list = [self.url_temp.format(i) for i in range(1,3)]
        return url_list

    def parse_list(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode()
    def get_content_list(self,html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath('//div[@id="content-left"]/div')
        content_list = []
        for div in div_list:
            item = {}
            item['content'] = div.xpath('.//div[@class="content"]/span/text()')[0].strip()
            item['jpg'] = div.xpath('.//div[@class="thumb"]//img/@src')
            content_list.append(item)
        return content_list
    def save_list(self,content_list):
        with open('图片.txt','a',encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content,ensure_ascii=False))
                f.write('\n')
        print("保存成功")


    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            html_str = self.parse_list(url)
            content_list = self.get_content_list(html_str)
            self.save_list(content_list)
if __name__ == '__main__':
    tieba = TiebaSpider()
    tieba.run()
