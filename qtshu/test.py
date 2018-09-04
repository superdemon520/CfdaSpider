#encoding:utf-8
import re
import json
import difflib
import hashlib
import requests 
import Levenshtein
from lxml import etree
from selenium import webdriver
from twisted.internet import defer
from scrapy.http import HtmlResponse
from daxiangproxies import DaxiangProxies
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware 
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Page

class test(object):

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Language':'zh-cn',
        'Accept-Encoding':'br, gzip, deflate'

    }

    if __name__ == '__main__':

        url = 'http://ypk.39.net/889443/'
        res = requests.get(url,headers=headers)
        selector = etree.HTML(res.text)
        print(res.text)
        print(selector.xpath('//div[@class="ps"]/p[1]/a/text()'))
        print(selector.xpath('//div[@class="ps"]/p[1]/text()'))

        # # selector = etree.HTML(res.body)
        # data = selector.xpath('//div[@class="ps"]')[0]
        # chenfens = data.xpath('string(.)').replace('\n','').split('\r')
        # # print(chenfen)
        # for chenfen in chenfens:
        #     print('********************')
        #     print(chenfen)
        #     if len(chenfen.strip()) > 10:
        #         print(chenfen)
        #         break

        # url = 'https://www.meishij.net/chufang/diy/'
        # res = requests.get(url,headers=headers)
        # print(res.text)
        






# def scraper(url):
# 	res = requests.get(url,headers=headers)
# 	print(res.text)
  
# if __name__ == '__main__':  
#     scraper(url)
  


#####################名字类比测试###################
# stra1='去痛片'
# stra2='去痛片(索密痛/华南牌)'

# strb1='吸入用硫酸沙丁胺醇溶液'
# strb2='二甲双胍格列吡嗪片(Ⅱ)'



# print(difflib.SequenceMatcher(None,stra1,stra2).ratio())

# print(Levenshtein.ratio(stra1,stra2))

#####################名字匹配分类测试###################
# maths=[
# {'fenlei1':'降压药','fenlei2':'CCB','word':'硝苯地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'氨氯地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'乐卡地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'尼莫地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'尼卡地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'尼群地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'尼索地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'非洛地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'贝尼地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'拉西地平'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'地尔硫卓'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'维拉帕米'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'氟桂利嗪'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'桂利嗪'},
# {'fenlei1':'降压药','fenlei2':'CCB','word':'利多氟嗪'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'氯沙坦'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'缬沙坦'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'厄贝沙坦'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'坎地沙坦'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'他索沙坦'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'依普罗沙坦'},
# {'fenlei1':'降压药','fenlei2':'ARB','word':'替米沙坦'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'卡托普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'依那普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'雷米普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'培哚普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'贝那普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'福辛普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'阿拉普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'莫维普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'西拉普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'喹那普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'螺普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'咪达普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'地拉普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'赖诺普利'},
# {'fenlei1':'降压药','fenlei2':'ACEI','word':'群多普利'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'阿替洛尔'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'美托洛尔'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'索他洛尔'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'普萘洛尔'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'比索洛尔'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'卡维地洛'},
# {'fenlei1':'降心率药','fenlei2':'β受体阻滞剂','word':'奈必洛尔'},
# {'fenlei1':'降糖药','fenlei2':'磺脲类','word':'格列吡嗪'},
# {'fenlei1':'降糖药','fenlei2':'磺脲类','word':'格列齐特'},
# {'fenlei1':'降糖药','fenlei2':'磺脲类','word':'格列本脲'},
# {'fenlei1':'降糖药','fenlei2':'磺脲类','word':'格列波脲'},
# {'fenlei1':'降糖药','fenlei2':'磺脲类','word':'格列美脲'},
# {'fenlei1':'降糖药','fenlei2':'磺脲类','word':'格列喹酮'},
# {'fenlei1':'降糖药','fenlei2':'非磺脲类苯茴酸类衍生物','word':'瑞格列奈'},
# {'fenlei1':'降糖药','fenlei2':'非磺脲类苯茴酸类衍生物','word':'那格列奈'},
# {'fenlei1':'降糖药','fenlei2':'双胍类','word':'二甲双胍'},
# {'fenlei1':'降糖药','fenlei2':'α-葡萄糖苷酶抑制剂','word':'糖-100'},
# {'fenlei1':'降糖药','fenlei2':'α-葡萄糖苷酶抑制剂','word':'阿卡波糖'},
# {'fenlei1':'降糖药','fenlei2':'α-葡萄糖苷酶抑制剂','word':'伏格列波糖'},
# {'fenlei1':'降糖药','fenlei2':'胰岛素增敏剂','word':'罗格列酮'},
# {'fenlei1':'降糖药','fenlei2':'胰岛素增敏剂','word':'吡格列酮'},
# {'fenlei1':'降糖药','fenlei2':'二肽基肽酶-4抑制剂','word':'西格列汀'},
# {'fenlei1':'降糖药','fenlei2':'二肽基肽酶-4抑制剂','word':'沙格列汀'},
# {'fenlei1':'降糖药','fenlei2':'二肽基肽酶-4抑制剂','word':'维格列汀'},
# {'fenlei1':'降糖药','fenlei2':'GLP-1受体激动剂','word':'艾塞那肽'},
# {'fenlei1':'降糖药','fenlei2':'GLP-1受体激动剂','word':'利拉鲁肽'},
# {'fenlei1':'降糖药','fenlei2':'胰岛素类','word':'胰岛素'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'洛伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'辛伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'普伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'氟伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'阿托伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'瑞舒伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'美伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'西立伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'罗伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'他汀类','word':'匹伐他汀'},
# {'fenlei1':'降脂药','fenlei2':'贝特类','word':'非诺贝特'},
# {'fenlei1':'降脂药','fenlei2':'贝特类','word':'苯扎贝特'},
# {'fenlei1':'降脂药','fenlei2':'贝特类','word':'吉非贝齐'},
# {'fenlei1':'降脂药','fenlei2':'贝特类','word':'氯贝特'},
# {'fenlei1':'降脂药','fenlei2':'贝特类','word':'利贝特'},
# {'fenlei1':'降脂药','fenlei2':'胆固醇吸收抑制剂','word':'依折麦布'},
# {'fenlei1':'降脂药','fenlei2':'胆固醇吸收抑制剂','word':'普罗布考'},
# {'fenlei1':'抗凝药','fenlei2':'抗血小板药','word':'阿司匹林'},
# {'fenlei1':'抗凝药','fenlei2':'抗血小板药','word':'双嘧达莫'},
# {'fenlei1':'抗凝药','fenlei2':'抗血小板药','word':'氯吡格雷'},
# {'fenlei1':'抗凝药','fenlei2':'抗血小板药','word':'替格瑞洛'},
# {'fenlei1':'抗凝药','fenlei2':'新型口服抗凝药','word':'阿哌沙班'},
# {'fenlei1':'抗凝药','fenlei2':'新型口服抗凝药','word':'利伐沙班'},
# {'fenlei1':'抗凝药','fenlei2':'新型口服抗凝药','word':'依度沙班'},
# {'fenlei1':'抗凝药','fenlei2':'新型口服抗凝药','word':'达比加群'},
# {'fenlei1':'利尿剂','fenlei2':'噻嗪类','word':'氯噻嗪'},
# {'fenlei1':'利尿剂','fenlei2':'噻嗪类','word':'氯噻酮'},
# {'fenlei1':'利尿剂','fenlei2':'噻嗪类','word':'氢氯噻嗪'},
# {'fenlei1':'利尿剂','fenlei2':'噻嗪类','word':'环戊噻嗪'},
# {'fenlei1':'利尿剂','fenlei2':'噻嗪类','word':'苄氟噻嗪'},
# {'fenlei1':'利尿剂','fenlei2':'噻嗪类','word':'美托拉宗'},
# {'fenlei1':'利尿剂','fenlei2':'髓袢利尿剂','word':'呋塞米'},
# {'fenlei1':'利尿剂','fenlei2':'髓袢利尿剂','word':'依他尼酸'},
# {'fenlei1':'利尿剂','fenlei2':'髓袢利尿剂','word':'布美他尼'},
# {'fenlei1':'利尿剂','fenlei2':'髓袢利尿剂','word':'吡咯他尼'},
# {'fenlei1':'利尿剂','fenlei2':'髓袢利尿剂','word':'托拉塞米'},
# {'fenlei1':'利尿剂','fenlei2':'保钾利尿剂','word':'螺内酯'},
# {'fenlei1':'降尿酸药','fenlei2':'抑制尿酸生成类药','word':'别嘌醇'},
# {'fenlei1':'降尿酸药','fenlei2':'促进尿酸排出药','word':'丙磺舒'},
# {'fenlei1':'降尿酸药','fenlei2':'促进尿酸排出药','word':'苯溴马隆'},
# {'fenlei1':'降尿酸药','fenlei2':'其他类','word':'非布司他'},
# {'fenlei1':'质子泵抑制剂','fenlei2':'','word':'奥美拉唑'},
# {'fenlei1':'质子泵抑制剂','fenlei2':'','word':'兰索拉唑'},
# {'fenlei1':'质子泵抑制剂','fenlei2':'','word':'泮托拉唑'},
# {'fenlei1':'质子泵抑制剂','fenlei2':'','word':'雷贝拉唑'},
# {'fenlei1':'质子泵抑制剂','fenlei2':'','word':'莱米诺拉唑'},
# {'fenlei1':'质子泵抑制剂','fenlei2':'','word':'埃索美拉唑'},
# {'fenlei1':'抗心绞痛类','fenlei2':'','word':'硝酸异山梨酯'},
# {'fenlei1':'抗心绞痛类','fenlei2':'','word':'单硝酸异山梨醇脂'},
# {'fenlei1':'抗心绞痛类','fenlei2':'','word':'曲美他嗪'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'枸橼酸铋钾'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'胶体次枸酸铋'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'雷尼替丁'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'铝碳酸铋'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'胶体果胶铋'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'西咪替丁'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'法莫替丁'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'铋剂','word':'拉呋替丁'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'前列腺素及其衍生物','word':'米索前列醇'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'其他','word':'硫糖铝'},
# {'fenlei1':'胃粘膜保护剂','fenlei2':'其他','word':'吉法酯'}
# ]

# mingchen = '西咪替丁哈哈哈'

# for math in maths:
# 	if mingchen.find(math['word'])>-1:
# 		print(math['fenlei1'])
# 		print(math['fenlei2'])
# 		print(math['word'])
# 		break

