# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class MaoyanPipeline:
    def process_item(self, item, spider):
        name=item['name']
        style=item['style']
        film_time=item['film_time']
        d={'电影名称':name,'电影类型':style,'上映时间':film_time}
        df=pd.DataFrame(d,index=[0])
        df.to_csv('./maoyan.csv',mode='a+',encoding='utf8',index=False,header=False)
        return item
