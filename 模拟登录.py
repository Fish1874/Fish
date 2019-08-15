from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#定义一个淘宝类
class taobao_infos:
    #对象初始化
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs",{'profile.managed_default_content_settings.images':2})
        # options.add_experimental_option('excludeSwitches',['enable-automation'])# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium


        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser,10)



    #登录淘宝
    def login(self):
        #打开网页
        self.browser.get(self.url)

        #等待 密码登录选项 出现
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        #等待微博选项出现
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.weibo-login')))
        password_login.click()

        #等待微博帐号出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        #等待微博密码出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        #等待登录按钮 出现
        submit =self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.login_box > .btn_tip > a > span')))
        submit.click()

        #直到获取淘宝会员名称才确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick')))
        print(taobao_name.text)

if __name__ == '__main__':
    chromedriver_path = 'C:/Users/24339/Scripts/chromedriver.exe'
    weibo_username = '......'
    weibo_password = '......'

    a = taobao_infos()
    a.login() #登录
