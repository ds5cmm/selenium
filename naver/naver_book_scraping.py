from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import numpy as np


url = f'https://book.naver.com/search/search.nhn?query=%EB%8F%84%EC%84%9C'
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
        EC.presence_of_element_located((By.ID, 'searchBiblioList'))
    )

    theater_list = []
    pageNum = 3
    count = 0

    for i in  range(1, pageNum):
        news_col_count = 7

        # 기사url
        url_link_list = []
        
        # 도서명
        data_1_list = []
        data_1 = driver.find_elements_by_css_selector("#searchBiblioList > li")
        
        # 페이지별 배열 초기화
        news_total = len(data_1)
        news_list = [[''] * news_col_count for _ in range(news_total)]
        
        print("한페이지 조회건수: "+ str(news_total))
        # 도서명 초기화
        for r in range(1, news_total):
            f = driver.find_element_by_xpath("//*[@id='searchBiblioList']/li["+str(r)+"]/dl/dt/a")
            news_list[r][0] = f.text

        # 저자 등
        for r in range(1, news_total):
            f = driver.find_element_by_xpath("//*[@id='searchBiblioList']/li["+str(r)+"]/dl/dd[1]")
            book_writer = f.text.split('|')
            if len(book_writer) == 3:
                news_list[r][1] = f.text.split('|')[0] # 저자
                news_list[r][3] = f.text.split('|')[1] # 출판사
                #news_list[r][3] = f.text.split('|')[2] # 출판일
            else :
                news_list[r][1] = f.text.split('|')[0] # 저자
                news_list[r][2] = f.text.split('|')[1] # 번역
                news_list[r][3] = f.text.split('|')[2] # 출판사
                #news_list[r][4] = f.text.split('|')[3] # 출판일
        
        # 가격
        for r in range(1, news_total):
            f = driver.find_element_by_xpath("//*[@id='searchBiblioList']/li["+str(r)+"]/dl/dd[2]")
            if len(f.text.split('|')) == 3:
                book_writer = f.text.split('|')[2].split('→')
                if len(book_writer) == 2:
                    news_list[r][4] = book_writer[0] # 정가
                    news_list[r][5] = book_writer[1].split('원')[0] + '원' # 판매가격
                else :
                    news_list[r][4] = book_writer[0] # 정가

        # 소개
        for r in range(1, news_total):
            f = driver.find_element_by_xpath("//*[@id='searchBiblioList']/li["+str(r)+"]/dl/dd[3]")
            news_list[r][6] = f.text.replace("소개", "")

        for k in news_list:
            theater_list.append(k)

        driver.find_element_by_xpath("//a[@class='next']").click()
        time.sleep(3)
    
except TimeoutException:
    print ('해당 페이지에 정보가 존재하지 않습니다.')
finally:
    driver.quit()

print(len(theater_list))

    
theater_df = pd.DataFrame(theater_list, columns=['도서명', '저자', '번역', '출판사', '정가', '판매가격', '소개'])
theater_df.index = theater_df.index + 1
theater_df.to_csv(f'./output_data/theater_book_df.csv', mode='w', encoding='utf-8-sig', header=True, index=True)

print('정보수집이 완료되었습니다. 시간:', time.time() - startTime)
