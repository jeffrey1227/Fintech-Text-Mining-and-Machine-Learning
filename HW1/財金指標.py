#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from io import BytesIO
import datetime


# In[2]:


#欲下載的網站
url = "https://www.mql5.com/en/economic-calendar/united-states/ism-non-manufacturing-pmi"
head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
main_driver = webdriver.Chrome('/Users/lou_tun_chieh/Desktop/webdriver/chromedriver')  # 注意放CHROMEDRIVER的位置
#告訴chromedriver 等下要找的element 如果沒有找到，要等20秒讓他們生完
main_driver.implicitly_wait(20)
main_driver.get(url)
#點取History button
history_btn_ele = main_driver.find_element_by_xpath('//*[@id="calendar-tabs"]/li[3]')
history_btn_ele.click()
main_driver.implicitly_wait(20)
#得到歷史資料的csv檔
export_btn_ele = main_driver.find_element_by_xpath('//*[@id="eventHistoryContent"]/div[2]/a')
csv_url = export_btn_ele.get_attribute('href')
csv_url


# In[3]:


download = requests.get(csv_url, headers=head)
df = pd.read_csv(BytesIO(download.content))
#將該變數轉成pandas的dataframe格式
df = pd.DataFrame(df)
df.head()


# In[4]:


date = []
value = []
#進行資料的整理，切割資料、篩選不要的資料（日期小於2015-12）
for i in range((df.shape[0]-1), -1, -1):
	data_list = (df.iloc[i, 0]).split("\t", 3)
	date.append(data_list[0])
	value.append(data_list[1])

#新創一個dataframe，並放入整理好的資料
table = {"Date": date,  
        "Value": value
        }
table = pd.DataFrame(table)
table['Date'] = table[table['Date'] < datetime.datetime.now().date().strftime("%Y.%m.%d")]
table['Date'] = pd.to_datetime(table['Date'], format="%Y-%m-%d")
table.head(20)

