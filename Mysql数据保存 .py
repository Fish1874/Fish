import pymysql
import requests
from urllib.parse import urlencode
import json

def baipin_api(pn):
    base_url="https://sp0.baidu.com/yrwHcyah_cgCo2Kml5_Y_D3/api/newasync?"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    params = {
        'pn': pn,
        'query': 'python爬虫',
        'city': '广州'
    }
    url = base_url + urlencode(params)
    html = requests.get(url, headers=headers).text
    html = json.loads(html)
    return html

def insert_into_db(conn,jobs):
    conn.ping(reconnect=True)  #如果断开就重连
    cursor = conn.cursor()
    #cur.execute('truncate zhaoping') #清空现在所有的数据
    jobs = jobs['data']['data']['disp_data']

    for job in jobs:
        title = job['title']
        content = job['description']
        source = job['source']
        time = job['lastmod']
        # print(title,content,source,time)
        sql_p = 'insert into zhaoping(title,content,source,time) values(%s,%s,%s,%s)'

        cursor.execute(sql_p,(title,content,source,time))
        print('保存成功')
    conn.commit()
    cursor.close()
    conn.close()


def get_db():
    conn = pymysql.connect(host='localhost',
                         user='root',
                         password='1874',
                         db='test',
                         port=3306,
                         charset='utf8')
    cursor = conn.cursor()
    cursor.execute('drop table if exists zhaoping')

    sql = '''create table zhaoping(
            id int not null auto_increment primary key,
            title text not null,
            content longtext not null,
            source longtext null,
            time date null
            )default charset 'utf8';
    '''

    cursor.execute(sql)

    return conn

if __name__ == '__main__':
    conn = get_db()
    for i in range(1,20):
        job = baipin_api(i)
        insert_into_db(conn,job)
