# -*- coding: utf-8 -*-
import scrapy
from ..items import *
from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


class QtcrawlSpider(scrapy.Spider):
    name = 'qtcrawl'
    allowed_domains = ['www.qtshu.com']
    start_urls = ['https://www.qtshu.com/shenmu/1280338.html']

    def parse(self, response):
        item = QtshuItem()
        item['title'] = response.xpath('//*[@id="htmltimu"]/text()')[0].extract()
        contents = response.xpath('//*[@id="htmlContent"]/p/text()').extract()
        # print('\n'.join(contents))
        item['content'] = "\n".join(contents)
        yield item

        next_page = response.xpath('//*[@id="htmlxiazhang"]/@href')[0].extract()
        yield Request(next_page, callback=self.parse)