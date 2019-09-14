from requests import get
import os
from os.path import exists
from contextlib import closing
import json
from filetype import guess
#文件下载器

def Down_load(file_url, file_full_name, now_photo_count, all_photo_count):
    headers = {"User-Agent":"Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"}

    #开始下载图片
    with closing(get(file_url, headers=headers,stream=True)) as response:
        chunk_size = 1024 #单次请求最大值
        content_size = int(response.headers['content-length']) #文件总大小
        data_count = 0 #当前已传输的大小
        with open(file_full_name,'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data) #显示进度条效果
                done_block = int((data_count / content_size)*50)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r %s：[%s%s] %d%% %d/%d" % (file_full_name, done_block * '█', ' ' * (50 - 1 - done_block), now_jd, now_photo_count, all_photo_count), end=" ")

    #下载完图片后获取图片扩展名，并为其增加扩展名
    file_type = guess(file_full_name)  #这里用到filetype库 对文件进行解析，判断其类型，比如:png,gif,jpg....
    os.rename(file_full_name,file_full_name + '.' + file_type.extension)

#爬取不同类型图片
def crawler_photo(type_id, photo_count):
    #1最新2最热
    if(type_id == 1):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c68ffb9463b7fbfe72b0db0?page=1&per_page=' + str(photo_count)
    elif(type_id == 2):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c69251c9b1c011c41bb97be?page=1&per_page=' + str(photo_count)

    #获取图片列表数据
    headers = {"User-Agent":"Mozilla/5.0\
(Windows NT 6.1; WOW64) AppleWe\
bKit/537.36 (KHTML, like Gecko) \
Chrome/57.0.2987.98 Safari/537.\
36 LBBROWSER"}
    response = get(url,headers=headers)
    photo_data = json.loads(response.content)

    #已经下载的图片张数
    now_photo_count = 1

    #所有的图片张数
    all_photo_count = len(photo_data)

    #开始下载并保存
    for photo in photo_data:

        #创建一个文件夹
        if not exists('./' + str(type_id)):
            os.makedirs('./' + str(type_id))

        #准备下载的图片链接
        file_url = photo['urls']['raw']

        #准备下载的图片名称
        file_name_only = file_url.split('/')
        file_name_only = file_name_only[len(file_name_only) -1]

        #准备保存到本地的完整路径
        file_full_name = './' +str(type_id) + './' + file_name_only

        #开始下载图片
        Down_load(file_url, file_full_name, now_photo_count, all_photo_count)
        now_photo_count = now_photo_count + 1

if __name__ == '__main__':
    wall_paper_id = 1
    wall_paper_count = 10
    while (True):

        # 换行符
        print('\n\n')

        # 选择壁纸类型
        wall_paper_id = input("壁纸类型：1.最新壁纸 , 2.最热壁纸 \n请输入编号以便选择5K超清壁纸类型：")
        # 判断输入是否正确
        while (wall_paper_id != str(1) and wall_paper_id != str(2)):
            wall_paper_id = input("壁纸类型：1.最新壁纸 , 2.最热壁纸 \n请输入编号以便选择5K超清壁纸类型：")

        # 选择要下载的壁纸数量
        wall_paper_count = input("请输入要下载的5K超清壁纸的数量：")
        # 判断输入是否正确
        while (int(wall_paper_count) <= 0):
            wall_paper_count = input("请输入要下载的5K超清壁纸的数量：")

        # 开始爬取5K高清壁纸
        print("正在下载5K超清壁纸，请稍等……")
        crawler_photo(int(wall_paper_id), int(wall_paper_count))
        print('\n下载5K高清壁纸成功!')