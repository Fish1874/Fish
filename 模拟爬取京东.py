import pymongo
from pyquery import PyQuery as pq
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


MONGO_URL = 'localhost'
MONGO_DB = 'JD'
MONGO_TABLE = 'JD'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

options = Options()
options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=options)
browser.maximize_window()
wait = WebDriverWait(browser,3)#设置等待时间
def search():
    try:
        browser.get('https://www.jd.com')
        input = wait.until(EC.presence_of_element_located((By.ID,'key')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search"]/div/div[2]/button')))
        input.send_keys('算法')
        submit.click()
        total = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="J_bottomPage"]/span[2]/em[1]')))
        get_products()
        return total[0].text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_bottomPage"]/span[2]/input')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_bottomPage"]/span[2]/a')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList > ul .gl-item')))
    html = browser.page_source #获取网页源代码
    doc = pq(html)
    items = doc('#J_goodsList > ul .gl-item').items() #获取一个生成器
    for item in items:
        product = {
            'image': item.find('.p-img .img').attr('src'),
            'price': item.find('.p-price').text(),
            'deak': item.find('.p-commit').text(),
            'title': item.find('.p-name').text(),
            'shop': item.find('.p-shopnum').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongodb成功',result)
    except Exception:
        print('存储失败',result)
def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        print(total)
        for i in range(5,total + 1):
            next_page(i)
            print('--' * 50)
    except Exception:
        browser.close()


if __name__ == '__main__':
    main()
