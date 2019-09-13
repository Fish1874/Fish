import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading
import time

class Procuder(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)
            # time.sleep(0.5)

    #当作是对象方法
    def parse_page(self,url):
        headers = {"User-Agent": "Mozilla/5.0\
        (Windows NT 6.1; WOW64) AppleWe\
        bKit/537.36 (KHTML, like Gecko) \
        Chrome/57.0.2987.98 Safari/537.\
        36 LBBROWSER",
                   'Referer': 'http://www.doutula.com/article/list/?page=1',}
        response = requests.get(url,headers=headers).text
        html = etree.HTML(response)
        imgs = html.xpath('//div[@class="col-sm-9 center-wrap"]//img[@class!="gif"]')
        for img in imgs:
            img_url = img.get('data-original')      #图片地址
            alt = img.get('alt')                    #图片名字
            alt = re.sub(r'[\?？ \.。！*\!:：]','',alt)
            suffix = os.path.splitext(img_url)[1]   #分割后缀名
            filename = alt + suffix
            self.img_queue.put((img_url,filename))


class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get()
            request.urlretrieve(img_url, 'D:/TEST/' + filename)
            print(filename+'下载完成！')
            # time.sleep(0.5)
def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1,101):
        url = 'http://www.doutula.com/article/list/?page={}'.format(x)
        page_queue.put(url)
    for x in range(5):
        t = Procuder(page_queue,img_queue)
        t.start()
    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()
