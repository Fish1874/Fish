#(https://github.com/dxxzst/free-proxy-list)

import requests
from bs4 import BeautifulSoup
import threading
from pymongo import MongoClient
from lxml import etree


#检查代理是否可用
def checkip(proxy):
    try:
        url = 'http://ip.tool.chinaz.com/'
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        res = requests.get(url,headers=headers,
                             proxies={'https': 'https://{}'.format(proxy),
                                      'http': 'http://{}'.format(proxy)},
                             timeout=30
                         )
        html = etree.HTML(res.text)
        ip_address = html.xpath('//dd[@class="fz24"]/text()')   #自己的ip地址

        if ip_address[0] == proxy[:-5]:
            return True
        elif ip_address[0] == proxy[:-6]:
            return True
        else:
            return False
    except:
        return False



def getgoodproxy(ip,ip_type):
    if checkip(ip):
        print('{}可用，类型为{}'.format(ip, ip_type))
        goodip.append(ip)
        handler.insert_one({'ip': ip})


if __name__ == '__main__':

    url = 'https://github.com/dxxzst/free-proxy-list'
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    table = soup.find_all('table')[1]
    ulist1 = []
    ulist2 = []
    for tr in table.find_all('tr')[1:]:
        a = tr.text.split('\n')
        if a[4] == 'high':
            if a[3] == 'http':
                ulist1.append('{}:{}'.format(a[1], a[2]))
            else:
                ulist2.append('{}:{}'.format(a[1], a[2]))

    goodip = []
    client = MongoClient('localhost')
    db = client.proxy
    handler = db.good_proxy
    handler.delete_many({})    #删除所有代理

    tasks = []              #线程池
    for ip1 in ulist1:

        task = threading.Thread(target=getgoodproxy, args=(ip1,'http',))    #function_name: 需要线程去执行的方法名
        tasks.append(task)                                 #args: 线程执行方法接收的参数，该属性是一个元组，如果只有一个参数也需要在末尾加逗号。
        task.start()



    for ip2 in ulist2:
        task = threading.Thread(target=getgoodproxy, args=(ip2,'https',))
        tasks.append(task)
        task.start()

    for _ in tasks:
        _.join()

    print('完成代理ip验证并储存到本地！')

'''
使用方法：
conn = MongoClient('localhost')
db = conn.proxy
mongo_proxy = db.good_proxy

proxy_data = mongo_proxy.find()
proxies = json_normalize([ip for ip in proxy_data])
proxy_list = list(proxies['ip'])
proxy = random.choice(proxy_list)

r = requests.get(url,headers=headers,
                proxies={'https':'https://{}'.format(proxy),
                         'http': 'http://{}'.format(proxy)}

'''


