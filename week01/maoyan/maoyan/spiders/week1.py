# -*- coding: utf-8 -*-
"""
首先需要从首页获取电影的跳转链接，再在各个电影详情页获取电影名称，类型，上映时间
"""
import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class Week1Spider(scrapy.Spider):
    name = 'week1'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        url='https://maoyan.com/films?showType=3'
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        links=Selector(response=response).xpath('//div[@class="movie-item film-channel"]/a/@href').extract()[:10]
        links=['https://maoyan.com'+i for i in links]
        items=[]
        for link in links:
            item=MaoyanItem()
            item['link']=link
            items.append(item)
            yield scrapy.Request(link,meta={'item':item},callback=self.parse2,dont_filter=False)

    def parse2(self,response):
        item=response.meta['item']
        content=Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        name=content.xpath('./h1/text()')
        style=content.xpath('./ul/li[1]/a/text()')
        film_time = content.xpath('./ul/li[3]/text()')
        item['name']=name.extract_first()
        item['style']='_'.join([i.strip() for i in style.extract()])
        item['film_time']=film_time.extract_first()
        # print(name.extract_first())
        # print(style.extract())
        # print(film_time.extract_first())
        # print('---------------------')
        yield item

