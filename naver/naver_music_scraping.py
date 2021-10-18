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



url = f'https://www.melon.com/chart/month/index.htm?classCd=DM0000'
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
        EC.presence_of_element_located((By.CLASS_NAME, 'lst50'))
    )

    theater_list = []
    pageNum = 2
    count = 0

    for i in  range(1, pageNum):
        news_col_count = 9
        
        # 데이타 건수
        data_1_list = []
        #lst50
        data_1 = driver.find_elements_by_css_selector("#frm > div > table > tbody > tr")
        
        print("한페이지 조회건수: "+ str(len(data_1)))
        # 페이지별 배열 초기화
        news_total = len(data_1)
        news_list = [[''] * news_col_count for _ in range(news_total)]
        
        # 음악
        for r in range(1, news_total):
            
            c0 = driver.find_element_by_xpath('//*[@id="frm"]/div/table/tbody/tr['+str(r)+']/td[6]/div/div/div[1]/span/a')
            
            # 곡명
            news_list[r][0] = c0.text

            # 가수
            c1 = driver.find_element_by_xpath('//*[@id="frm"]/div/table/tbody/tr['+str(r)+']/td[6]/div/div/div[2]/a')
            news_list[r][1] = c1.text

            # 앨범명 
            c2 = driver.find_element_by_xpath('//*[@id="frm"]/div/table/tbody/tr['+str(r)+']/td[7]/div/div/div/a')
            news_list[r][2] = c2.text
            
            c2_link = "http://www.melon.com/album/detail.htm?albumId=" + c2.get_attribute('href').replace("javascript:melon.link.goAlbumDetail('", "").replace("');", "") # 앨범url
            c2_link_header = {'User-Agent': 'Mozilla/5.0'}
            print(c2_link)

            # 소개            
            if c2_link:
                try:
                    res = requests.get(c2_link, headers=c2_link_header)
                    if res.status_code == 200:
                        link_data = BeautifulSoup(res.text.replace("<br>", ""), 'html.parser')
                        link_content_0 = link_data.select_one('#conts > div.section_info > div > div.entry > div.info > span')                        
                        news_list[r][3] = link_content_0.get_text()

                        link_content_1 = link_data.select_one('#conts > div.section_info > div > div.entry > div.meta > dl > dd:nth-child(2)')
                        news_list[r][4] = link_content_1.get_text()

                        link_content_2 = link_data.select_one('#conts > div.section_info > div > div.entry > div.meta > dl > dd:nth-child(4)')
                        news_list[r][5] = link_content_2.get_text()

                        link_content_3 = link_data.select_one('#conts > div.section_info > div > div.entry > div.meta > dl > dd:nth-child(6)')
                        news_list[r][6] = link_content_3.get_text()

                        link_content_4 = link_data.select_one('#conts > div.section_info > div > div.entry > div.meta > dl > dd:nth-child(8)')
                        news_list[r][7] = link_content_4.get_text()

                        c2_link_content = ""
                        link_content_5 = link_data.select_one('#d_video_summary > div')
                        for content in link_content_5:
                            c = content.string
                            if c is not None:
                                c2_link_content += c.replace('\n', ' ').replace("\r", "")                        
                        news_list[r][8] = c2_link_content

                except Exception:
                    print("소개자료 존재하지 않습니다." + c0.text)
            



        # 재배열
        for k in news_list:
            theater_list.append(k)
        
except TimeoutException:
    print ('해당 페이지에 정보가 존재하지 않습니다.')
finally:
    driver.quit()

print(len(theater_list))

    
theater_df = pd.DataFrame(theater_list, columns=['곡명', '가수', '앨범명', '앨범구분', '발매일', '장르', '발매사', '기획사', '소개'])
theater_df.index = theater_df.index + 1
theater_df.to_csv(f'./output_data/theater_music_df.csv', mode='w', encoding='utf-8-sig', header=True, index=True)

print('정보수집이 완료되었습니다. 시간:', time.time() - startTime)
