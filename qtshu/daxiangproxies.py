# *-* coding:utf-8 *-*
import lxml
import json
import time
import redis
import random
import requests
import settings
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
 
class DaxiangProxies(object):
 
 
    """docstring for Proxies"""
    def __init__(self, page=5):
        self.proxies = []
        self.verify_pro = []
        self.headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies()

        # self.get_proxies_nn()
 
    def get_proxies(self):
        print('***************批量提取代理******************')
        url = 'http://tpv.daxiangdaili.com/ip/?tid=&num=30&delay=3&filter=on'
        html = requests.get(url, headers=self.headers).content
        ip_str = str(html).replace('b','')
        ip_str = ip_str.replace("'","")
        print(ip_str)
        ips = ip_str.split("\\r\\n")
        print(ips)
        for ip in ips:
            self.proxies.append("http://"+ip)

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print ('verify proxy........')
        works = []
        for _ in range(10):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue,new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print ('verify_proxies done!')
 
 
    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0:break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    # print ('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                print ('fail %s' % proxy)

    def sync():
        pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        r = redis.StrictRedis(connection_pool=pool)
        a = DaxiangProxies()
        # a.verify_proxies()
        proxie = a.proxies 
        with open('proxies.txt', 'a') as f:
            for proxy in proxie:
                f.write(proxy+'\n')
                if r.get(proxy)==None:
                    r.set(proxy,proxy)
 
 
if __name__ == '__main__':
    pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    r = redis.StrictRedis(connection_pool=pool)
    a = DaxiangProxies()
    # a.verify_proxies()
    proxie = a.proxies 
    with open('proxies.txt', 'a') as f:
       for proxy in proxie:
            f.write(proxy+'\n')
            if r.get(proxy)==None:
                r.set(proxy,proxy)
