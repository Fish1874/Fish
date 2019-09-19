import requests
from fontTools.ttLib import TTFont


# 学习来源（https://blog.csdn.net/xing851483876/article/details/82928607）
#编码，字体形状都有变化


url = 'https://maoyan.com/board/1'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
response = requests.get(url,headers).text

font_1 = TTFont('./a.woff')  #打开本地文件a.woff
font_1.saveXML('font_1.xml')     #将ttf文件转化成xml并保存到本地，方便我们查看里面的数据结构
name_list1 = font_1.getGlyphNames()[1:-1]  # 获取所有字符的对象，去除第一个和最后一个
print(name_list1)

font_dict = {
    'uniED83': '0', 'uniEAE0': '1', 'uniEA7F': '2', 'uniE0B1': '3', 'uniE82D': '4',
    'uniE072': '5', 'uniF107': '6', 'uniE701': '7', 'uniE3F6': '8', 'uniE7EC': '9'

}

font_2 = TTFont('./b.woff')  #打开第二个文件,  后面用于比较
font_2.saveXML('font_2.xml')
name_list2 = font_2.getGlyphNames()[1:-1]#获取所有字符的对象，去除第一个和最后一个
print(name_list2)

# 保存每个字符的坐标信息，分别存入corrinate_list1和coordinate_list2
coordinate_list1 = []
for i in name_list1:
    # 获取字体对象的横纵坐标信息
    coordinate = font_1['glyf'][i].coordinates
    coordinate_list1.append(list(coordinate))

coordinate_list2 = []
for i in name_list2:
    # 获取字体对象的横纵坐标信息
    coordinate = font_2['glyf'][i].coordinates
    coordinate_list2.append(list(coordinate))

# 构造新的映射
def compare(c1,c2):
    '''
    输入：某俩个对象字体的坐标列表
    输出:bool类型，True则可视为同一个字
    '''

    for i in range(5):
        if abs(c1[i][0]-c2[i][0]) < 70 and abs(c1[i][1]-c2[i][1]) < 70:
            pass
        else:
            return False
    return True

index2 = -1
new_dict = {}
for name2 in coordinate_list2:
    index2 += 1
    index1 = -1
    # print(name2)
    for name1 in coordinate_list1:
        index1 += 1
        # print(name1)
        if compare(name1,name2):
            new_dict[name_list2[index2]] = font_dict[name_list1[index1]]

print((new_dict))