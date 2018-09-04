# -*- coding: utf-8 -*-
import re
import json
import time
import scrapy
import string
import difflib
import datetime
from ..items import *
from lxml import etree
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

'''
类说明
起始页从cfda药品栏目列表页开始
1.首先根据设置的页数循环获取列表中药品名称
2.通过名称查询此药的列表页
3.根据列表页中的链接地址循环获取到cfda药品详情页爬取需要的信息
4.循环中根据爬取到的批准文号去39网站获取对应药品列表，如无列表则跳过39网进入315爬取，有则获取链接进入详情页爬取
5.39网详情页爬取数据后根据批准文号去315上查询此药品信息
6.通过批准文号查询315爬取可能会有多条数据，一般是包装规格不同（1对多）和类似名称（类比处理）
7.根据上一步获取的详情链接进入详情页爬取更多信息
8.对于仍然没有爬取到的数据进行补全
'''
class CfdaCrawl(scrapy.Spider):
    name = 'cfdacrawl'
    start_urls = ['http://app2.sfda.gov.cn/datasearchp/gzcxSearch.do?page={}&optionType=V1&formRender=cx'.format(str(i)) for i in range(500,501)]

    def __init__(self):
        self.settings = get_project_settings()
        self.catetorys = self.settings.get('CATEGORY_MATCH')

    def parse(self, response):
        selector = etree.HTML(response.body)
        # 获取名称
        names = selector.xpath('//tr[@name]/td[1]/text()')
        # 过滤关键字
        filters = self.settings.get('FILTER_WORDS')
        for name in names:
            for filter1 in filters:
                if name.find(filter1)>-1:
                    names.remove(name)

        # 循环调用下一步抓取CFDA详情
        for name in names:
            url = 'http://app2.sfda.gov.cn/datasearchp/all.do?tableName=TABLE25&formRender=cx&searchcx=&name={}'.format(name)
            request = Request(url=url, callback=self.parse_cfdadatelist)
            request.meta['preurl'] = url
            yield request

            url = 'http://app2.sfda.gov.cn/datasearchp/all.do?tableName=TABLE36&formRender=cx&searchcx=&name={}'.format(name)
            request = Request(url=url, callback=self.parse_cfdadatelist)
            request.meta['preurl'] = url
            yield request

    # 查询对应药名的列表页
    def parse_cfdadatelist(self, response):
        selector = etree.HTML(response.body)
        # 获取页面跳转信息及页数
        page = selector.xpath('//tbody/tr/td/table[2]/tbody/tr/td/text()')[0]
        page = re.findall(r"/共(.+?)页",page)[0]
        urls = [response.meta['preurl'] + "&page={}".format(str(i)) for i in range(1,int(page)+1)]
        for url in urls:
            request = Request(url=url,callback=self.parse_cfdainnerlist)
            request.meta['preurl'] = url
            yield request

    # 循环药品列表
    def parse_cfdainnerlist(self, response):
        selector = etree.HTML(response.body)
        detailurls = selector.xpath('//td[2]/a[@target]/@href')
        for url in detailurls:
            url = "http://app2.sfda.gov.cn" + url
            # print('[parse_cfdainnerlist]url:' + response.meta['preurl'])
            request = Request(url=url,callback=self.parse_cfdadetail)
            request.meta['preurl'] = url
            yield request

    # 根据url获取详细信息
    def parse_cfdadetail(self, response):
        item = MediItem()
        item['tiaoma'] = ''
        item['mingchen'] = ''
        item['shangbiao'] = ''
        item['pizhunwenhao'] = ''
        item['jixing'] = ''
        item['guige'] = ''
        item['baozhuangguige'] = ''
        item['chengfen'] = ''
        item['shengchandanwei'] = ''
        item['shengchandizhi'] = ''
        item['chufangyao'] = ''
        item['jibenyao'] = ''
        item['baoxiao'] = ''
        item['chucang'] = ''
        item['jiage'] = ''
        item['fenlei1'] = ''
        item['fenlei2'] = ''

        selector = etree.HTML(response.body)
        item['pizhunwenhao'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[1]/td[1]/text()')[0]
        if response.url.find('tableId=36')>-1:
            item['shengchandanwei'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td[2]/text()')[0]
            item['mingchen'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[6]/td[1]/text()')[0]
            item['jixing'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[8]/td[1]/text()')[0]
            item['guige'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[8]/td[2]/text()')[0]
        if response.url.find('tableId=25')>-1:
            item['shengchandanwei'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[4]/td[1]/text()')[0]
            item['mingchen'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[1]/td[2]/text()')[0]
            item['jixing'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td[1]/text()')[0]
            item['guige'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td[2]/text()')[0]
        item['shengchandizhi'] = selector.xpath('/html/body/center/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[4]/td[2]/text()')[0]
        item['shangbiao'] = item['mingchen']
        
        url = 'http://ypk.39.net/search/all?k={}'.format(item['pizhunwenhao'])

        # 根据名称查找分类并赋值
        for catetory in self.catetorys:
            if item['mingchen'].find(catetory['word'])>-1:
                item['fenlei1'] = str(catetory['fenlei1'])
                item['fenlei2'] = str(catetory['fenlei2'])
                break

        request = Request(url=url,callback=self.parse_39)
        request.meta['item'] = item
        yield request
        
    # 获取39药品网信息
    def parse_39(self, response):
        item = response.meta['item']
        selector = etree.HTML(response.body)
        params = selector.xpath('/html/body/div[8]/div[2]/ul/li[1]/div[1]/strong/i/span/text()')
        for param in params:
            if param.find("甲类非处方药")>-1:
                item['chufangyao'] = '甲类非处方药'
            elif param.find("乙类非处方药")>-1:
                item['chufangyao'] = '乙类非处方药'
            elif param.find("国家基本药物")>-1:
                item['jibenyao'] = '基本药'
            elif param.find('医保药品甲类')>-1:
                item['baoxiao'] = '医保药品甲类'
            elif param.find('医保药品乙类')>-1:
                item['baoxiao'] = '医保药品乙类'
        if len(selector.xpath('/html/body/div[8]/div[2]/ul/li/div[1]/strong/a/@href'))>0:
            url = 'http://ypk.39.net'+ selector.xpath('/html/body/div[8]/div[2]/ul/li/div[1]/strong/a/@href')[0]
            request = Request(url=url,callback=self.parse_39detail)
            request.meta['item'] = item
            yield request
        else:
            url = 'https://www.315jiage.cn/search.aspx?where=certification&keyword={}#certification'.format(str(item['pizhunwenhao']))
            request = Request(url=url,callback=self.parse_315)
            request.meta['item'] = item
            yield request

    def parse_39detail(self, response):
        item = response.meta['item']
        selector = etree.HTML(response.body)
        # 判断是否有储藏方式
        if len(selector.xpath('/html/body/div[12]/div[2]/div[1]/div[1]/ul[2]/li[3]/text()'))>0:
            item['chucang'] = selector.xpath('/html/body/div[12]/div[2]/div[1]/div[1]/ul[2]/li[3]/text()')[0].strip()
        if len(selector.xpath('//div[@class="ps"]/p[1]/text()'))>0:
            data = selector.xpath('//div[@class="ps"]')[0]
            chengfens = data.xpath('string(.)').replace('\n','').split('\r')
            for chengfen in chengfens:
                if len(chengfen.strip()) > 10:
                    words = re.findall(u'成\xa0\xa0分(.+?)适应症',chengfen.replace(' ',''))
                    if len(words)<1:
                        words = re.findall(u'成\xa0\xa0分(.+?)功能主治',chengfen.replace(' ',''))
                    if len(words)>0:
                        item['chengfen'] = words[0]
        if len(selector.xpath('/html/body/div[12]/div[1]/div[1]/h1/a/text()'))>0:
            shangbiao = selector.xpath('/html/body/div[12]/div[1]/div[1]/h1/a/text()')[0]
            if shangbiao.find('(')>0:
                point = shangbiao.find('(')
                item['shangbiao'] = shangbiao[0:point]
            else:
                item['shangbiao'] = shangbiao

        url = 'https://www.315jiage.cn/search.aspx?where=certification&keyword={}#certification'.format(str(item['pizhunwenhao']))
        request = Request(url=url,callback=self.parse_315)
        request.meta['item'] = item
        yield request


    def parse_315(self, response):
        item = response.meta['item']
        selector = etree.HTML(response.body)
        urls = selector.xpath('//div[@class="title"]/a/@href')
        names = selector.xpath('/html/body/div[2]/table/tbody/tr/td[1]/div[1]/div[2]/div/div/div/div/a/text()')
        guiges = selector.xpath('/html/body/div[2]/table/tbody/tr/td[1]/div[1]/div[2]/div/div/div/div/text()[1]')
        # 判断有更多详细信息抓取
        if len(urls)>0:
            for name,url,guige in zip(names,urls,guiges):
                # 相似度判断名字是否为同一种药，相似度大于0.3就继续抓取详情
                if difflib.SequenceMatcher(None,item['mingchen'],name).ratio() > 0.3:
                    guige = guige.replace('规格：','').split(' ')
                    if len(urls)>0 and len(guige)>0:
                        item['guige'] = guige[0]
                    url = 'https://www.315jiage.cn/' + url
                    request = Request(url=url,callback=self.parse_315detail)
                    request.meta['item'] = item
                    yield request
        else:
        	yield item

    def parse_315detail(self, response):
        item = response.meta['item']
        selector = etree.HTML(response.body)
        contents = selector.xpath('//*[@id="tab1"]/ul/li/text()')
        # 遍历获取结构会变化的商品信息内容
        for content in contents:
            if content.find("【规格】")>-1:
                if item['guige']!='':
                    item['baozhuangguige'] = content.replace("【规格】","")
                if item['guige'].strip()=='' and item['guige'].find('*')>-1 :
                    point = item['guige'].index('*')
                    item['baozhuangguige'] = item['guige'][point+1:]
                    item['guige'] = item['guige'][0:point]
            elif item['chengfen'].strip()=='' and content.find("【主要成份】")>-1:
                item['chengfen'] = content.replace("【主要成份】","")
            elif content.find("【贮藏】")>-1:
                chucang = content.replace("【贮藏】","")
                item['chucang'] = chucang.replace("。","")
            elif content.find("【条形码】")>-1:
                item['tiaoma'] = content.replace("【条形码】","")
            if len(selector.xpath('//*[@id="tab1"]/ul/li[2]/h2/text()')) > 0:
                item['shangbiao'] = selector.xpath('//*[@id="tab1"]/ul/li[2]/h2/text()')[0]
            jiage = selector.xpath('//*[@id="content"]/p[1]/text()')[0]
            item['jiage'] = re.findall('零售价格：(.+?)元',jiage)[0]
            item['baozhuangguige'] = selector.xpath('//*[@id="content"]/p[3]/u[1]/text()')[0]

        yield item
        

        




