#目标：通过webdriver来模拟登陆石墨文档

import requests
from selenium import webdriver
import time
try:
    browser=webdriver.Chrome()
    browser.get('https://shimo.im')
    time.sleep(0.3)
    btm1=browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    btm1.click()
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys('895590667@qq.com')
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys('895590667925')
    btm2=browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
    time.sleep(0.3)
    btm2.click()
    cookies=browser.get_cookies()
    print(cookies)

except Exception as e:
    print(e)
finally:
    browser.close()