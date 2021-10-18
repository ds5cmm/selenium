from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import numpy as np


url = f'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%89%B4%EC%8A%A4&oquery='
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
        EC.presence_of_element_located((By.CLASS_NAME, 'list_news'))
    )

    theater_list = []
    pageNum = 10
    count = 0

    for i in  range(1, pageNum):
        news_col_count = 4

        # 기사url
        url_link_list = []
        
        # 신문사url
        url_data_list = []
        url_data = driver.find_elements_by_css_selector(" .news_wrap .info_group > a")
        for k in url_data:
            if k.get_attribute('class') == 'info press':
                url_data_list.append(k.get_attribute('href'))
            if k.get_attribute('class') == 'info':
                url_link_list.append(k.get_attribute('href'))


        # 페이지별 배열 초기화
        news_total = len(url_data_list)
        news_list = [[''] * news_col_count for _ in range(news_total)]
        
        # 신문사url 초기화
        for r in range(news_total):
            news_list[r][0] = url_data_list[r]
        
        # 기사 타이틀
        title_row = 0
        title_data = driver.find_elements_by_css_selector(" .news_wrap .news_tit")        
        for k in title_data:
            news_list[title_row][1] = k.get_attribute('title')
            title_row += 1

        # 기사 url
        link_row = 0
        for k in url_link_list:
            news_list[link_row][2] = k
            link_row += 1
        
        # 요약기사
        content_row = 0
        content_data = driver.find_elements_by_css_selector(" .news_wrap .dsc_wrap .dsc_txt_wrap")           
        for k in content_data:
            news_list[content_row][3] = k.text
            content_row += 1
        
        # 이미지 저장
        #for j in img_data:
        #    count += 1
        #    j.screenshot(f'img/{count}.png')

        for k in news_list:
            theater_list.append(k)

        driver.find_element_by_xpath("//a[@class='btn_next']").click()
        time.sleep(3)
    
except TimeoutException:
    print ('해당 페이지에 정보가 존재하지 않습니다.')
finally:
    driver.quit()

print(len(theater_list))

    
theater_df = pd.DataFrame(theater_list, columns=['신문사url', '기사타이틀', '기사url', '요약기사'])
theater_df.index = theater_df.index + 1
theater_df.to_csv(f'./output_data/theater_news_df.csv', mode='w', encoding='utf-8-sig', header=True, index=True)

print('정보수집이 완료되었습니다. 시간:', time.time() - startTime)

    