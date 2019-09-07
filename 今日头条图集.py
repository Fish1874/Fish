import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re


def get_page(offset):
    headers = {
        'cookie': 'tt_webid=6722242761368864270; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6722242761368864270; csrftoken=7cfc81422c770ea7aa39140c9fd61de0; UM_distinctid=16c69d65d42b13-0b1ace1877d3b4-c343162-1fa400-16c69d65d439ce; CNZZDATA1259612802=248233061-1565143756-https%253A%252F%252Fwww.toutiao.com%252F%7C1565143756; sso_uid_tt=2d945211ee1c688c4534d0a69ddeee91; toutiao_sso_user=ac94552c947523e9b67e255646805d14; login_flag=6bcba4a9eb46d9b1ca581e3c1dfef72d; sessionid=a9f1868fd1919be6946ed81fbf4a27c6; uid_tt=00772c94bed30ff93140e4c19b461236; sid_tt=a9f1868fd1919be6946ed81fbf4a27c6; sid_guard="a9f1868fd1919be6946ed81fbf4a27c6|1567493337|15552000|Sun\054 01-Mar-2020 06:48:57 GMT"; __tasessionId=2cyasqfh81567684037065; s_v_web_id=7601159053605d84d0e682af78cb480e',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    }
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '风景',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    # print(url)
    try:
        resp = requests.get(url, headers=headers)
        if 200  == resp.status_code:
            return resp.json()
    except requests.ConnectionError:
        return None

#提取所需的信息
def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            #防止找不到报错
            if item.get('title') is None:
                continue
            title = re.sub('[\t\|]', '', item.get('title'))
            if item.get('image_list') is None:
                continue
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub("list.*?pgc-image", "large/pgc-image", image.get('url'))  #把图片尺寸换大
                yield {
                    'image': origin_image,
                    'title': title
                }


def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(response.content).hexdigest(),        #hash算法md5， hexdigest把二进制转为十六进制
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print('正在下载 %s' % file_path)
            else:
                print('下载完成','-----'*20)
    except Exception as e:
        print(e)


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        save_image(item)


GROUP_START = 0
GROUP_END = 9
#使用多进程
if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    # for i in range(0,1):
    #     main(i)
