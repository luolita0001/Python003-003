"""
作业一：

安装并使用 requests、bs4 库，爬取猫眼电影（）的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
"""
#方法一
#导入模块
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

#目标地址
url='https://maoyan.com/films?showType=3'

#请求头
USER_AGENT_LIST=[
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

USER_AGENT = random.choice(USER_AGENT_LIST)
#发送请求
# cookie='__mta=188560663.1597890698273.1597890698273.1597890970124.2; uuid_n_v=v1; uuid=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; _csrf=95755be51375160d997f21019e57056e3f906d41ebb3255f831df72a64243871; _lxsdk_cuid=17409b51631c8-00610c57583e4f-31667305-100200-17409b51631c8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1597890698; mojo-uuid=80eca9132ab764022c411ac5b41b4e26; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217409e6120040c-01efdcd8470923-74246634-174410-17409e61202170%22%7D; mojo-session-id={"id":"af2c98d5c5e7fbcd914e040c05f3cea1","time":1597894930250}; _lxsdk=442E90F0E28D11EA96A68775497B19D833D99B85017042CAA1D8CF364581FD43; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1597897395; __mta=188560663.1597890698273.1597897246073.1597897396016.4; _lxsdk_s=17409e5ceb7-a2e-e9-9c%7C%7C38'

headers={'user-agent':USER_AGENT}
res=requests.get(url,headers=headers)
# print(res.status_code)
res=res.content.decode('utf-8')
res=res.replace('<!--', '').replace('-->', '')
# print(f'状态码为{res.status_code}')
soup=BeautifulSoup(res,'lxml')
#找规律
"""
1。内容都在class属性为movie-hover-info的div标签下
2。电影名称在div/div[@class=movie-hover-title]/span，class属性为name的文本中
3。电影类型在div/div[@class=movie-hover-title]/span,class属性为hover-tag的文本中
4。上映时间在div/div[@]/span,class属性为hover-tag的文本中
"""
film_name=[]
film_style=[]
film_time=[]
for div1 in soup.find_all('div',attrs={'class':'movie-hover-info'})[:10]:
    film_name.append(div1.find_all('div')[0].span.text)
    film_style.append(div1.find_all('div')[1].text.split()[1])
    film_time.append(div1.find_all('div')[3].text.split()[1])
    time.sleep(1)

d={'电影名称':film_name,'电影类型':film_style,'上映时间':film_time}
df=pd.DataFrame(d)
df.to_csv('./猫眼电影.csv',encoding='utf8')