from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
driver = webdriver.Chrome('/Users/jarvis/Documents/app/Python/chromedriver')
url = 'https://google.com'
driver.get(url)
#driver.maximize_window()
action = ActionChains(driver)

# 로그인 화면 이동
driver.find_element_by_css_selector('#gb > div > div.gb_Se > a').click()

# 아이디 입력
action.send_keys('ds5cmm@gmail.com').perform()

# 다음 클릭
driver.find_element_by_css_selector('#identifierNext > div > button').click()


driver.close()
