import requests
import re
import random
import queue
import threading
import csv
import json
import pymongo
from pandas.io.json import json_normalize

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]


def get_proxy():
    conn = pymongo.MongoClient('localhost')
    db = conn.proxy
    mongo_proxy = db.good_proxy
    proxy_data = mongo_proxy.find()
    allproxy = []
    for ip in proxy_data:
        pro = {'https': 'https://{}'.format(ip['ip'])}
        allproxy.append(pro)
    proxy = random.choice(allproxy)
    return proxy

# def get_proxy():
#     r = requests.get('http://47.100.21.174:8899/api/v1/proxies?page=1').json()
#     proxy = random.choice(r['proxies'])
#     proxy = {'https':'https://{}:{}'.format(proxy['ip'],proxy['port'])}
#     return proxy




#获取所有基金代码
def get_fund_code():
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Referer': 'http://fund.eastmoney.com/110023.html'
    }
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    r = requests.get(url,headers=headers,timeout=5)

    fund_code = r.content.decode()
    fund_code = fund_code.replace("﻿var r = [","").replace("];","")

    #正则批量提取
    fund_code = re.findall(r'[\[](.*?)[\]]',fund_code)

    #对每行数据进行处理,并存到fund_code_list列表中
    fund_code_list = []
    for sub_data in fund_code:
        data = sub_data.replace('\"','').replace("'","")
        data_list = data.split(",")
        fund_code_list.append(data_list)

    return fund_code_list

# 获取基金数据
def get_fund_data():

    # 当队列不为空时
    while (not fund_code_queue.empty()):

        # 从队列读取一个基金代码
        # 读取是阻塞操作
        fund_code = fund_code_queue.get()

        # 获取一个代理，格式为ip:端口
        proxy = get_proxy()

        # 获取一个随机user_agent和Referer
        headers = {'User-Agent': random.choice(user_agent_list),
                  'Referer': 'http://fund.eastmoney.com/110023.html'
        }

        # 使用try、except来捕获异常
        # 如果不捕获异常，程序可能崩溃
        try:
            # 使用代理访问
            req = requests.get("http://fundgz.1234567.com.cn/js/" + str(fund_code) + ".js", proxies=proxy,timeout=3, headers=headers)

            # 没有报异常，说明访问成功
            # 获得返回数据
            data = (req.content.decode()).replace("jsonpgz(","").replace(");","").replace("'","\"")
            data_dict = json.loads(data)
            print(data_dict)

            # 申请获取锁，此过程为阻塞等待状态，直到获取锁完毕
            mutex_lock.acquire()

            # 追加数据写入csv文件，若文件不存在则自动创建
            with open('./fund_data.csv', 'a+', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                data_list = [x for x in data_dict.values()]
                csv_writer.writerow(data_list)

            # 释放锁
            mutex_lock.release()

        except Exception:
            # 访问失败了，所以要把我们刚才取出的数据再放回去队列中
            fund_code_queue.put(fund_code)
            print("访问失败，重新执行")


if __name__ == '__main__':

    # 获取所有基金代码
    fund_code_list = get_fund_code()

    # 将所有基金代码放入先进先出FIFO队列中
    # 队列的写入和读取都是阻塞的，故在多线程情况下不会乱
    # 在不使用框架的前提下，引入多线程，提高爬取效率
    # 创建一个队列
    fund_code_queue = queue.Queue(len(fund_code_list))
    # 写入基金代码数据到队列
    for i in range(len(fund_code_list)):
        #fund_code_list[i]也是list类型，其中该list中的第0个元素存放基金代码
        fund_code_queue.put(fund_code_list[i][0])



    # 创建一个线程锁，防止多线程写入文件时发生错乱
    mutex_lock = threading.Lock()
    # 线程数为50，在一定范围内，线程数越多，速度越快
    for i in range(50):
        t = threading.Thread(target=get_fund_data,name='LoopThread'+str(i))
        t.start()

    for i in fund_code_list:
        i.join()