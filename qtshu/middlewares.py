# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import redis
import random
import logging
# import settings
from scrapy.utils.project import get_project_settings
from scrapy import signals
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

# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options

class SeleniumMiddleware(object):
    def __init__(self):
        self.settings = get_project_settings()
        pool = redis.ConnectionPool(host=self.settings.get('REDIS_HOST'), port=self.settings.get('REDIS_PORT'), db=self.settings.get('REDIS_DB'))
        self.r = redis.StrictRedis(connection_pool=pool)
        self.max_retry_times = self.settings.get('RETRY_TIMES')
        '''
        引入自动化测试框架Selenium模拟真实用户操作，考虑加入headless提高速度
        '''
        chrome_options = Options()
        profile = {"plugins.plugins_disabled": ['Chrome PDF Viewer'],
             "plugins.plugins_disabled": ['Adobe Flash Player'],
             "profile.managed_default_content_settings.images":2}
        chrome_options.add_experimental_option("prefs", profile)
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_options.add_experimental_option("prefs", profile)
        # 设置无界面浏览器,需要对应无界面浏览器驱动配合
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
  
        # 向Options实例中添加禁用扩展插件的设置参数项
        chrome_options.add_argument("--disable-extensions")
        # # 添加屏蔽--ignore-certificate-errors提示信息的设置参数项
        chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        # # 添加浏览器最大化的设置参数项，启动同时最大化窗口
        chrome_options.add_argument('--start-maximized')
        self.browser = webdriver.Chrome(executable_path=self.settings.get('CHROME_PATH'),chrome_options=chrome_options)

        # options = Options()
        # options.add_argument('-headless')
        # self.browser = Firefox(executable_path='geckodriver', firefox_options=options)



    '''
    DownloadMiddle的请求方法中，不同的请求地址做不同的请求，比如某些请求地址使用selenium模拟请求，而某些地址
    '''
    def process_request(self, request, spider):
        # 判断缓存中代理池容量，小于设定的代理则数提取一批代理
        if self.r.dbsize() < self.settings.get('PROXY_NUMS'):
            DaxiangProxies.sync()
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        # print("this is request ip:"+proxy)
        print('[proxy]'+proxy+'  [scrapy_spider_url]:'+request.url)
        request.meta["proxy"] = proxy
        try:
            self.browser.get(request.url)  # 获取网页链接内容
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)  # 返回HTML数据
        except TimeoutException:
            return HtmlResponse(url=request.url, request=request, encoding='utf-8', status=500)
        finally:
            pass



    def get_random_proxy(self):
        '''随机从Redis中读取proxy'''
        proxy = self.r.randomkey().decode()
        return proxy

class MyProxyMiddleware(object):
    def __init__(self,ip=''):
        self.ip=ip
        pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.r = redis.StrictRedis(connection_pool=pool)
        self.max_retry_times = settings.RETRY_TIMES

    def process_request(self,request, spider):
        # 判断缓存中代理池容量，小于设定的代理则数提取一批代理
        if self.r.dbsize() < settings.PROXY_NUMS:
            DaxiangProxies.sync()
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        print("this is request ip:"+proxy)
        try:
            request.meta["proxy"] = proxy
        except Exception as e:
            print(e)
        return None

    def get_random_proxy(self):
        '''随机从Redis中读取proxy'''
        proxy = self.r.randomkey().decode()
        return proxy

class MyRetryMiddleware(RetryMiddleware):

    logger = logging.getLogger(__name__)

    # EXCEPTIONS_TO_CHANGE = (defer.TimeoutError, TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone)

    def delete_proxy(self,proxy):
        # 删除Redis中对应数据
        self.r.delete(proxy)
        # 判断缓存中代理池容量，小于设定的代理则数提取一批代理
        if self.r.dbsize() < settings.PROXY_NUMS:
            DaxiangProxies.sync()

    def get_random_proxy(self):
        print(settings.get('REDIS_HOST'))
        '''随机从Redis中读取proxy'''
        proxy = self.r.randomkey().decode()
        return proxy

    def __init__(self,settings):
        self.ip=''
        pool = redis.ConnectionPool(host=settings['REDIS_HOST'], port=settings.getint('REDIS_PORT'), db=settings['REDIS_DB'])
        self.r = redis.StrictRedis(connection_pool=pool)
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.r.delete(request.meta.get('proxy', False))
            # 重新获取代理
            # proxy = self.r.randomkey().decode()
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        print('[RetryMiddleWare] Retry Url: '+request.url)
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            return self._retry(request, exception, spider)
