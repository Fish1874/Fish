#识别验证码缺口
#模拟拖动滑块

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image       #PIL强大的python图像管理库
from io import BytesIO


class Bilibili_Login():

    def __init__(self,username,password):
        self.url = "https://passport.bilibili.com/login"
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,10)
        self.username = username
        self.password = password

    def __del__(self):
        self.browser.close()

    #获取验证码图片位置
    def get_position(self, flag):
        img = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'canvas.geetest_canvas_slice')))
        time.sleep(2)
        if flag:
            #执行js获取不带缺口的原图
            js1 = 'document.getElementsByClassName("geetest_canvas_fullbg")[0].setAttribute("style","")'
            self.browser.execute_script(js1) #调用js方法，执行javescrpit脚本
        else:
            #执行js，把缺口复原
            js2 = 'document.getElementsByClassName("geetest_canvas_fullbg")[0].setAttribute("style", "opacity: 1; display: none;")'
            self.browser.execute_script(js2)
        location = img.location                   #返回的是字典
        print('图片坐标为:{}'.format(location))
        size = img.size                           #返回的是字典
        print('图片大小为：{}'.format(size))
        bottom, top, left, right = location["y"], location["y"]+size["height"], location["x"], location["x"]+size['width']
        return (bottom, top, left, right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()    #截图

        return Image.open(BytesIO(screenshot))  #BytesIO在内存中读取二进制文件，Image.open()打开图片


    def is_pixel_equal(self, image1, image2, x, y):
        '''
        像素值比较，若三个通道均出现超过阈值的变化，返回True
        '''
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        #abs()返回数字绝对值
        if abs(pixel1[0] - pixel2[0]) < THRESHOLD and abs(pixel1[1] - pixel2[1]) < THRESHOLD and abs(pixel1[2] - pixel2[2]) < THRESHOLD:
            return True
        else:
            return False


    #输出账号和密码
    def enter(self):
        self.browser.get(self.url)
        username = self.wait.until(EC.element_to_be_clickable((By.ID,'login-username')))
        password = self.wait.until(EC.element_to_be_clickable((By.ID,'login-passwd')))
        login = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-login')))
        username.send_keys(self.username)
        time.sleep(0.5)
        password.send_keys(self.password)
        time.sleep(0.5)
        login.click()

    #获取验证码图片
    def get_geetest_image(self, name, flag):
        bottom, top, left, right = self.get_position(flag)
        print('验证码位置:', bottom, top, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, bottom, right, top))
        captcha.save(name)
        return captcha

    def get_gap(self,image1,image2):
        '''
        获取缺口位置，通过比较像素值
        '''
        for i in range(LEFT, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    return i
        return LEFT

    def get_track(self, distance):

        """
        获取滑块移动轨迹的列表,distance是缺口的左侧横坐标值
        """
        track = []
        current = 0
        mid = distance * 0.8
        t = 0.5
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            current += move
            track.append(round(move))
        return track

    def get_slider(self):
        #获取滑块
        geetest = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return geetest


    #操作滑块至缺口处
    def move_to_gap(self, button, track):

        ActionChains(self.browser).click_and_hold(button).perform()
        for i in track:
            ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()
            time.sleep(0.1)
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()


    def get_cookies(self):
        cookies = ''
        cookies_list = self.browser.get_cookies()
        for i in cookies_list:
            cookies += i['name'] + '' + i['value'] + ';'
        with open('cookies.txt', 'w', encoding='utf-8') as f:
            f.write(cookies)


    def run(self):
        self.enter()
        image1 = self.get_geetest_image('captcha1.png', True)        #获取不带缺口图片
        image2 = self.get_geetest_image('captcha2.png', False)       #获取带缺口图片
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        track = self.get_track(gap-BORDER)
        print('滑块轨迹序列', track)
        slider = self.get_slider()                                  #获取滑块
        self.move_to_gap(slider, track)                              #操作滑块
        time.sleep(1)

        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'head-logo')))  #定位到Bilibili图标，表示登陆成功
            print('登陆成功，开始保存cookies!')

        except:
            print('登陆失败，自动重试...')
            self.run()


if __name__ == '__main__':
    THRESHOLD = 60
    LEFT = 60
    BORDER = 6
    username = input('账号：')
    password = input('密码:')
    bili = Bilibili_Login(username, password)
    bili.run()


















