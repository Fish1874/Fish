import requests
from lxml import etree
import json

#基础域名
BASE_DOMAIN = 'https://www.dytt8.net'

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0\
	.2743.116 Safari/537.36',
	'Accept-Language': 'zh-CN,zh;q=0.8'}

#获取每个电影详情页的URL
def get_parse(url):
    response = requests.get(url,headers=HEADERS).text
    html = etree.HTML(response)
    detailed_url = html.xpath('//table[@class="tbspan"]//a//@href')
    detailed_urls = [BASE_DOMAIN + url for url in detailed_url]
    # detailed_urls = map(lambda url:BASE_DOMAIN + url, detailed_url)
    return detailed_urls

#提取详情页的内容
def get_content(detailed_urls):
    movie = {}
    response = requests.get(detailed_urls,headers=HEADERS)
    #这里乱码了，需要自己换成gbk
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    zoom = html.xpath('//div[@id="Zoom"]')[0]
    img = zoom.xpath('.//img/@src')[0]
    movie['img'] = img
    #获取所有的文本内容
    infos = zoom.xpath('.//text()')

    #定义一个规则
    def parse_info(info,rule):
        return info.replace(rule,'').strip()

    for index,info in enumerate(infos):
        if info.startswith('◎译　　名'):
            info = parse_info(info,'◎译　　名')
            movie['name'] = info
        if info.startswith('◎年　　代'):
            info = parse_info(info,'◎年　　代')
            movie['years'] = info
        if info.startswith('◎产　　地'):
            info = parse_info(info,'◎产　　地')
            movie['place'] = info
        if info.startswith('◎语　　言'):
            info = parse_info(info,'◎语　　言')
            movie['language'] = info
        if info.startswith('◎主　　演'):
            info = parse_info(info,'◎主　　演')
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith('◎'):
                    break
                actors.append(actor)
            movie['actor'] = actors
    #种子下载地址
    download_url = html.xpath('//td[@bgcolor="#fdfddf"]/a/@href')[0]
    movie['download_url'] = download_url
    return movie


def write_to_file(content):
    with open('电影天堂.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_'+ str(offset) + '.html'
    detailed_urls = get_parse(url)
    for detailed_url in detailed_urls:
        content = get_content(detailed_url)
        print(content)
        write_to_file(content)

if __name__ == '__main__':
    for i in range(1,8):
        main(i)
