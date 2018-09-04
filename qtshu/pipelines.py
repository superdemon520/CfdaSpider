# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QtshuPipeline(object):
    def process_item(self, item, spider):
        with open("shenmu.txt",'a') as fp:
            fp.write(item['title'] + '\n')
            fp.write(item['content'] + '\n')

class CfdaPipeline(object):
    def process_item(self, item, spider):
        with open("medicine.txt",'a') as fp:
            fp.write(
            	item['tiaoma'] + '^' +
                item['mingchen'] + '^' +
                item['shangbiao'] + '^' +
                item['pizhunwenhao'] + '^' +
                item['jixing'] + '^' +
                item['guige'] + '^' +
                '^^' +
                item['baozhuangguige'] + '^' +
                item['chengfen'] + '^' +
                item['shengchandanwei'] + '^' +
                item['shengchandizhi'] + '^' +
                item['chufangyao'] + '^' +
                '^' +
                item['jibenyao'] + '^' +
                item['baoxiao'] + '^' +
                item['chucang'] + '^' +
                item['jiage'] + '^' +
                item['fenlei1'] + '^' +
                item['fenlei2'] + '\n')
