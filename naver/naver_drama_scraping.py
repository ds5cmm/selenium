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



url = f'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EB%B0%A9%EC%98%81%EC%A2%85%EB%A3%8C%ED%95%9C%EA%B5%AD%EB%93%9C%EB%9D%BC%EB%A7%88'
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
        EC.presence_of_element_located((By.CLASS_NAME, 'list_info._list_item'))
    )
    theater_list = []
    pageNum = 8
    count = 0

    for i in  range(1, pageNum):
        news_col_count = 7

        # 데이타 건수
        data_1_list = []

        view_row = 0
        view_cnt = 0

        view_datas = driver.find_elements_by_xpath('//*[@id="mflick"]/div/div[1]/ul')
        for v in view_datas:
            if v.get_attribute("style") != "display: none;":
                view_row = view_cnt
            view_cnt += 1
                
        data_1 = driver.find_elements_by_css_selector('#mflick > div > div.box_card_image_list._list > ul:nth-child('+str(view_row)+') > li')
                
        print("한페이지 조회건수: "+ str(len(data_1)))
        # 페이지별 배열 초기화
        news_total = len(data_1)
        news_list = [[''] * news_col_count for _ in range(news_total)]
        
        # 드라마
        for r in range(1, news_total):

            c0 = driver.find_element_by_xpath('//*[@id="mflick"]/div/div[1]/ul['+str(view_row)+']/li['+str(r)+']/strong/a')            
            c0_link = c0.get_attribute('href') # 드라마url
            
            # 소개
            c0_link_html = ''
            c0_link_content = ''
            if c0_link:
                try:
                    HEADERS = ({'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                            'Accept-Language': 'en-US, en;q=0.5'})
                            
                    res = requests.get(c0_link, headers=HEADERS)
                    if res.status_code == 200:
                        c0_link_html = res.text.replace("<br>", "")
                        link_data = BeautifulSoup(c0_link_html, 'html.parser')
                        
                        link_content = link_data.select_one(' div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > div.text_expand._ellipsis._img_ellipsis > span')
                        
                        for content in link_content:
                            c = content.string
                            if c is not None:
                                c0_link_content += c.replace('\n', ' ').replace("\r", "")
                   

                        try:
                            link_content_0 = link_data.select_one('div.cm_top_wrap._sticky._custom_select > div.title_area._title_area > h2 > a > strong')                            
                            news_list[r][0] = link_content_0.string
                        except Exception:
                            print("작품명 존재하지 않습니다." + c0.text)

                        try:
                            link_content_1 = link_data.select_one('div.cm_top_wrap._sticky._custom_select > div.title_area._title_area > div.sub_title > span:nth-child(3)')                            
                            news_list[r][1] = link_content_1.string
                        except Exception:
                            print("등급 존재하지 않습니다." + c0.text)

                        try:
                            link_content_2 = link_data.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > dl > div:nth-child(1) > dd > a')
                            news_list[r][2] = link_content_2.get_text()
                        except Exception:
                            print("방송사 존재하지 않습니다." + c0.text)
                        
                        try:
                            link_content_3 = link_data.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > dl > div:nth-child(1) > dd > span')
                            news_list[r][3] = link_content_3.get_text()
                        except Exception:
                            print("방영시작일 존재하지 않습니다." + c0.text)
                        
                        try:                            
                            link_content_4 = link_data.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > dl > div:nth-child(1) > dd > span')
                            news_list[r][4] = link_content_4.get_text()
                        except Exception:
                            print("방영종료일 존재하지 않습니다." + c0.text)
                        
                        try:                            
                            link_content_5 = link_data.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > dl > div:nth-child(1) > dd > span:nth-child(3)')
                            news_list[r][5] = link_content_5.get_text()
                        except Exception:
                            print("방영일 및 방영시간 존재하지 않습니다." + c0.text)
                                
                
                except Exception:
                    print("소개자료 존재하지 않습니다." + c0.text)
                
                news_list[r][6] = c0_link_content
                

        # 재배열
        for k in news_list:
            if k[0] is not None:
                theater_list.append(k)
        
        driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[2]/div/div/div[3]/div/a[2]').click()
        time.sleep(5)
    
except TimeoutException:
    print ('해당 페이지에 정보가 존재하지 않습니다.')
finally:
    driver.quit()

print(len(theater_list))


theater_df = pd.DataFrame(theater_list, columns=['작품명', '관람등급', '방송사', '방영시작일', '방영종료일', '방영일/시간', '소개'])
theater_df.index = theater_df.index + 1
theater_df.to_csv(f'./output_data/theater_drama_df.csv', mode='w', encoding='utf-8-sig', header=True, index=True)

print('정보수집이 완료되었습니다. 시간:', time.time() - startTime)
