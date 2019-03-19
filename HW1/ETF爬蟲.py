#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
import requests 
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from io import BytesIO
import datetime
from urllib import request,error


# In[2]:


def yahoo_download(url):
	url = "https://finance.yahoo.com/quote/" + url + "/history"
	head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	main_driver = webdriver.Chrome('/Users/lou_tun_chieh/Desktop/webdriver/chromedriver')  # 注意你們放CHROMEDRIVER的位置
	#告訴chromedriver 等下要找的element 如果沒有找到，要等10秒讓他們生完
	main_driver.implicitly_wait(10)
	main_driver.get(url)
	cookie_list = main_driver.get_cookies()
	cookies_dict = {}
	for cookie in cookie_list:
		cookies_dict['B'] = cookie['value']
	#print(cookies_dict)

	date_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
	date_btn_ele.click()
	main_driver.implicitly_wait(10)

	#點擊date button
	date_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/input[1]').clear()
	date_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/input[1]').send_keys("01/01/2016")
	#date_btn_ele.click()
	main_driver.implicitly_wait(10)

	##點擊done button
	done_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]')
	done_btn_ele.click()
	main_driver.implicitly_wait(10)

	#點擊apply button
	done_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
	done_btn_ele.click()
	main_driver.implicitly_wait(10)
	time.sleep(30)
	
	#得到歷史資料的csv檔
	export_btn_ele = main_driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
	csv_url = export_btn_ele.get_attribute('href')
	main_driver.quit()
	return csv_url, cookies_dict


# In[3]:


def write_down_csv(etf_name):
	
	tmp_url, tmp_cookie  = yahoo_download(etf_name)
	download = requests.get(tmp_url, cookies=tmp_cookie)
	df = pd.read_csv(BytesIO(download.content))
	#將該變數轉成pandas的dataframe格式
	df = pd.DataFrame(df)
	df = df.rename(columns={'Adj Close': etf_name})
	"""
	filename = etf_name + ".csv"
	with open (filename, 'wb') as handle:
		for block in download.iter_content(1024):
			handle.write(block)
	"""
	return df


# In[4]:


head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
#必須帶有瀏覽器等資訊
etf_list_1 = "Municipal Bond ETF List (29).csv"
etf_list_2 = "Target Maturity Date Corporate Bond ETF List (24).csv"

df_1 = pd.read_csv(etf_list_1)
df_2 = pd.read_csv(etf_list_2)
df = pd.concat([df_1, df_2])

df = df[df["Inception"] < "2016"]
df = df.reset_index(drop=True)

tmp_df =  write_down_csv(df["Symbol"][0])
#Date = tmp_df["Date"]
result =  pd.concat([tmp_df["Date"], tmp_df[df["Symbol"][0]]], axis=1)
for i in range(1, len(df["Symbol"])):
    
	tmp_df =  write_down_csv(df["Symbol"][i])
	#print(tmp_df[df["Symbol"][i]])
	result =  pd.concat([result, tmp_df[df["Symbol"][i]]], axis=1)
	#print(result)
result

