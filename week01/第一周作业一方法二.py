"""
第一周作业方法二
目标：获取每部电影的跳转链接，再对链接重新发起请求里获取电影的名称，类型和上映时间
"""
#导入模块
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#目标地址
url='https://maoyan.com/films?showType=3'

#自己的headers
User_Agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
#发送请求
cookie='__mta=188560663.1597890698273.1597890698273.1597890970124.2; uuid_n_v=v1; uuid=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; _csrf=95755be51375160d997f21019e57056e3f906d41ebb3255f831df72a64243871; _lxsdk_cuid=17409b51631c8-00610c57583e4f-31667305-100200-17409b51631c8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1597890698; mojo-uuid=80eca9132ab764022c411ac5b41b4e26; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%7D; mojo-session-id={"id":"af2c98d5c5e7fbcd914e040c05f3cea1","time":1597894930250}; _lxsdk=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1597897395; __mta=188560663.1597890698273.1597897246073.1597897396016.4; _lxsdk_s=17409e5ceb7-a2e-e9-9c%7C%7C38'

headers={'user-agent':User_Agent,'cookie':cookie}
res=requests.get(url,headers=headers)
# print(res.status_code)
res=res.content.decode('utf-8')
res=res.replace('<!--', '').replace('-->', '')
# print(f'状态码为{res.status_code}')
soup=BeautifulSoup(res,'lxml')

#获取电影链接
links=[]
for div in soup.find_all('div',attrs={'class':'movie-item film-channel'})[:10]:
    links.append(div.a['href'])
links=['https://maoyan.com'+i for i in links]
# print(links)

#定义一个接受链接，获取电影名称，类型，上映时间的函数
def get_a_url(my_url):
    #传入新的cookie
    cookie = '__mta=188560663.1597890698273.1597890970124.1597911788515.3; uuid_n_v=v1; uuid=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; _csrf=95755be51375160d997f21019e57056e3f906d41ebb3255f831df72a64243871; _lxsdk_cuid=17409b51631c8-00610c57583e4f-31667305-100200-17409b51631c8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1597890698; mojo-uuid=80eca9132ab764022c411ac5b41b4e26; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%7D; _lxsdk=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; __mta=188560663.1597890698273.1597890970124.1597904134980.3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1597911788; _lxsdk_s=1740b1fe2ca-616-358-b9f%7C%7C1'
    headers = {'user-agent': User_Agent, 'cookie': cookie}

    res = requests.get(my_url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    film_name.append(soup.find('div', attrs={'class': 'movie-brief-container'}).h1.text)
    # print(f'电影名称{film_name}')
    li = soup.find_all('li', attrs={'class': 'ellipsis'})
    film_style.append(li[0].text.replace('\n', ''))
    # print(f'电影类型{film_style}')
    film_time.append(li[2].text)
    # print(f'上映时间{film_time}')


film_name=[]
film_style=[]
film_time=[]
for my_url in links:
    get_a_url(my_url)
d={'电影名称':film_name,'电影类型':film_style,'上映时间':film_time}
df=pd.DataFrame(d)
df.to_csv('./猫眼电影.csv',encoding='utf8',index=False,header=False)