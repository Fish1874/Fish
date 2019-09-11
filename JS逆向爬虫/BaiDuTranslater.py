import requests
import js2py


#执行JS文件里的代码
context = js2py.EvalJs()




class BaiDuTranslater(object):


    def __init__(self,query):
        self.url = 'https://fanyi.baidu.com/extendtrans'
        self.query = query
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
            'Referer':'https://fanyi.baidu.com/',
            'Cookie':'BAIDUID=802F99DDDF5CBB9CB2C01EC34A6BA396:FG=1; BIDUPSID=802F99DDDF5CBB9CB2C01EC34A6BA396; PSTM=1558266513; MCITY=-218%3A; H_WISE_SIDS=133428_125703_133107_131439_131676_133889_128066_131887_126065_120198_131602_133017_132911_133045_131246_132439_130763_132378_131518_118892_118876_118843_118822_118790_131650_132840_132604_107318_133159_132590_132781_130122_133116_133352_133303_132889_129648_132251_127024_132558_132542_133837_133473_131906_128891_133847_132551_133695_133287_132554_129644_131423_132416_133414_132906_133013_110085_127969_123290_127319_128200_133729_133543; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDUSS=XZXRGVxZ1FmUmszNDhpME0yYlFzTXBEUE01R2hVaHZkTjB0aEMtUk15V0Y0cDVkSVFBQUFBJCQAAAAAAAAAAAEAAAAc0yGGyfHYr8rAvM0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIVVd12FVXddO; APPGUIDE_8_0_0=1; locale=zh; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1568114825,1568114858; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1568114804,1568114819,1568114825,1568114859; yjs_js_security_passport=eab8f4545eecef896257ad359ece19c0c42936b4_1568115278_js; __yjsv5_shitong=1.0_7_4d253e1275305d2c49a0b836c3feabc304f5_300_1568115417450_113.82.237.24_b72fc6b5; BDRCVFR[VXHUG3ZuJnT]=mk3SLVN4HKm; delPer=0; PSINO=6; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1568115996; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1568115996',

        }

    def make_sign(self):
        #js逆向获取sign的值
        #读取JS文件

        with open('jswenjian.js','r',encoding='utf-8') as f:
            #添加至上下文
            context.execute(f.read())

        #调用js中的函数生成sign
        sign = context.a(self.query)

        return sign

    def make_data(self,sign):
        data = {
            'query': self.query,
            'from': 'en',
            'to': 'zh',
            'token': '5ec7612af5e46e5f535d63b292ffa1dd',
            'sign': sign
        }
        return data

    def get_content(self,data):
        try:
            response = requests.post(url=self.url,headers=self.headers,data=data)
            print(response.json())
            #然后再返回json格式
            return response.json()
        except Exception as e:
            print('请求失败',e)




    def run(self):
        #获取sign的值
        sign = self.make_sign()
        #构建参数
        data = self.make_data(sign)
        #获取翻译内容
        content = self.get_content(data)
        print(content['data']['st_tag'])


if __name__ == '__main__':
    query = input('请输出英语：')
    aoo = BaiDuTranslater(query)
    aoo.run()
