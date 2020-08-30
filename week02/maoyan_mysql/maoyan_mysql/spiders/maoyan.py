# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from maoyan_mysql.items import MaoyanMysqlItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    # def start_requests(self):
    #     #自己的headers
    #     User_Agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    #     #发送请求
    #     cookie='__mta=188560663.1597890698273.1597890698273.1597890970124.2; uuid_n_v=v1; uuid=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; _csrf=95755be51375160d997f21019e57056e3f906d41ebb3255f831df72a64243871; _lxsdk_cuid=17409b51631c8-00610c57583e4f-31667305-100200-17409b51631c8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1597890698; mojo-uuid=80eca9132ab764022c411ac5b41b4e26; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%7D; mojo-session-id={"id":"af2c98d5c5e7fbcd914e040c05f3cea1","time":1597894930250}; _lxsdk=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1597897395; __mta=188560663.1597890698273.1597897246073.1597897396016.4; _lxsdk_s=17409e5ceb7-a2e-e9-9c%7C%7C38'

    #     headers={'user-agent':User_Agent,'cookie':cookie}
    #     url='https://maoyan.com/films?showType=3'
    #     yield scrapy.Request(url,callback=self.parse,headers=headers)

    def parse(self, response):
        links=Selector(response=response).xpath('//div[@class="movie-item film-channel"]/a/@href').extract()[:10]
        links=['https://maoyan.com'+i for i in links]
        items=[]
        for link in links:
            item=MaoyanMysqlItem()
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
