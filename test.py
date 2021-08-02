from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path=r'C:\Users\admin\PycharmProjects\bookmaker-parser\chromedriver.exe')
url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
driver.get(url=url)

x1 = driver.find_elements_by_class_name('tabs__item')
x1[-1].click()
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="archive-seasons"]/div/div[1]')))
# driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack','true');});",element)
prev_season = 0
for i in range(1):
    element.click()
    checking = driver.find_element_by_class_name('select-heading')
    curr_season = checking.get_attribute('innerHTML').replace('\n', '')
    if curr_season != prev_season:
        print(i, '. Парсится сезон ', curr_season)
        time.sleep(2)
        html = driver.page_source
        print(html)
        print(type(html))
        print('-----------------------')
        prev_season = curr_season
        # print(element.get_attribute("automationTrack"))
        soup_season = BeautifulSoup(html, 'html.parser')
        print(soup_season)
print('Парсинг лиги завершен')

driver.close()
driver.quit()

