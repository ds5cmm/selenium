import requests 
import time

from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import pandas as pd
import numpy as np



url = f'https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=reserve'
chromeDriver = '/Users/jarvis/Documents/app/Python/chromedriver'

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome(chromeDriver, chrome_options=options)
driver.get(url)

print('정보수집을 시작합니다.')
startTime = time.time() 

try:
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'thumb'))
    )

    theater_list = []
    pageNum = 2
    count = 0

    for i in  range(1, pageNum):
        news_col_count = 11

        # 기사url
        url_link_list = []
        
        # 데이타 건수
        data_1_list = []
        data_1 = driver.find_elements_by_css_selector(".lst_detail_t1 > li")
        
        print("한페이지 조회건수: "+ str(len(data_1)))
        # 페이지별 배열 초기화
        news_total = len(data_1)
        news_list = [[''] * news_col_count for _ in range(news_total)]
        
        # 영화
        for r in range(1, news_total):
            c0 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dt/a')
            c0_link = c0.get_attribute('href') # 영화url
            # 소개
            c0_link_content = ''
            if c0_link:
                try:
                    res = requests.get(c0_link)
                    if res.status_code == 200:
                        link_data = BeautifulSoup(res.text.replace("<br>", ""), 'html.parser')
                        link_content = link_data.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
                        for content in link_content:
                            c = content.string
                            if c is not None:
                                c0_link_content += c.replace('\n', ' ').replace("\r", "")
                except Exception:
                    print("소개자료 존재하지 않습니다." + c0.text)
            
            news_list[r][10] = c0_link_content

            news_list[r][0] = c0.text
            try:
                c1 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dt/span')
                news_list[r][1] = c1.text                        
            except Exception:
                print ('등급이 존재하지 않습니다.' + c0.text)
            c3 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dd[1]/dl[1]/dd/div/a/span[2]')
            news_list[r][2] = c3.text
            c4 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dd[1]/dl[1]/dd/div/a/span[3]/em')
            news_list[r][3] = c4.text

            try:
                c5 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dd[1]/dl[2]/dd/div/span[1]')
                news_list[r][4] = c5.text                
            except Exception:
                print ('현 예매율이 존재하지 않습니다.' + c0.text)
            
            c6 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dd[2]/dl/dd[1]')
            c6_data = c6.text.split('|')
            if len(c6_data) == 3:
                news_list[r][5] = c6_data[0].replace("개요", "").strip()
                news_list[r][6] = c6_data[1].strip()
                news_list[r][7] = c6_data[2].replace("개봉", "").strip()
            

            c7 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dd[2]/dl/dd[2]/span/a')
            news_list[r][8] = c7.text

            try:
                c8 = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(r)+']/dl/dd[2]/dl/dd[3]/span')
                news_list[r][9] = c8.text                     
            except Exception:
                print ('출연이 존재하지 않습니다.' + c0.text)

        # 재배열
        for k in news_list:
            theater_list.append(k)
        
except TimeoutException:
    print ('해당 페이지에 정보가 존재하지 않습니다.')
finally:
    driver.quit()

print(len(theater_list))

    
theater_df = pd.DataFrame(theater_list, columns=['영화제목', '관람등급', '네티즌평점', '참여인원수', '현 예매율', '장르', '시간', '개봉일', '감독', '출연', '소개'])
theater_df.index = theater_df.index + 1
theater_df.to_csv(f'./output_data/theater_movie_df.csv', mode='w', encoding='utf-8-sig', header=True, index=True)

print('정보수집이 완료되었습니다. 시간:', time.time() - startTime)
