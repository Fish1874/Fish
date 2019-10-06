import requests
from pyquery import PyQuery as pq
import pymongo
import time


client = pymongo.MongoClient('localhost')
db = client['bokeyuan']
collection = db['boke']


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'referer': 'https://www.cnblogs.com/'

    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response
    except Exception as e:
        raise e

def parse_data(response):
    html = response.content.decode('utf-8')
    doc = pq(html)
    contents = doc('.post_item').items()  #获取文章信息的div节点

    data = []
    for content in contents:
        con = {
            'name': content.find('.post_item_foot .lightblue').text(),
            'title': content.find('.titlelnk').text(),
            'url': content.find('.titlelnk').attr('href'),
            'time': content.find('.post_item_foot').text().split()[2] + '' +
                    content.find('.post_item_foot').text().split()[3],
            'article_comment': content.find('.article_comment .gray').text(),
            'read_counts': content.find('.article_view .gray').text(),
        }
        data.append(con)
    return data

def save_data(data):
    try:
        if collection.insert(data):
            print('保存至mongodb成功')
            time.sleep(0.5)
    except Exception:
        print('保存至mongodb失败')

def main():
    for i in range(1,10):
        url = 'https://www.cnblogs.com/#p{}'.format(i)
        html = get_data(url)
        data = parse_data(html)
        save_data(data)
if __name__ == '__main__':
    main()