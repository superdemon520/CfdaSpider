# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QtshuItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    pass

class MediItem(scrapy.Item):
	pizhunwenhao = scrapy.Field()
	mingchen = scrapy.Field()
	shengchandanwei = scrapy.Field()
	shengchandizhi = scrapy.Field()
	jixing = scrapy.Field()
	chufangyao = scrapy.Field()
	jibenyao = scrapy.Field()
	baoxiao = scrapy.Field()
	chengfen = scrapy.Field()
	chucang = scrapy.Field()
	tiaoma = scrapy.Field()
	shangbiao = scrapy.Field()
	jiage = scrapy.Field()
	guige = scrapy.Field()
	baozhuangguige = scrapy.Field()
	fuheguige = scrapy.Field()
	fenlei1 = scrapy.Field()
	fenlei2 = scrapy.Field()
	# guige = scrapy.Field()
	pass