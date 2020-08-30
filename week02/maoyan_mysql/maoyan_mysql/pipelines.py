# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import NotConfigured

class MaoyanMysqlPipeline:

    def __init__(self,info):
        self.info=info

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('DBINFO'):
            raise NotConfigured
        return cls(crawler.settings.get('DBINFO'))

    def open_conn(self,spider):
        self.conn=pymysql.connect(
            host = self.info['host'],
            port = self.info['port'],
            user = self.info['user'],
            password = self.info['password'],
            db = self.info['db']
        )
    
    def process_item(self, item, spider):
        name=item['name']
        style=item['style']
        film_time=item['film_time']
        try:
            with self.conn.cursor() as cur:
                sql='INSERT INTO"movies"("name","style","film_time") VALUES (%s,%s,%s)'
                cur.execute(sql,(name,style,film_time))
            self.conn.commit()
            self.conn.close()
        except:
            self.conn.rollback()
        finally:
            return item


        
