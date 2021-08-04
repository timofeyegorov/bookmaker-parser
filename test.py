# import sys
#
# sys.stdout = open('test.txt', 'a')
# print('строка 1')
# print('строка 2')
# print('строка 3')
# sys.stdout.close()
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(executable_path=r'C:\Users\User\PycharmProjects\bookmaker-parser\chromedriver.exe')
base_url = 'https://legalbet.ru'
url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
driver.get(url=url)

tabs_for_click = driver.find_elements_by_class_name('tabs__item')
tabs_for_click[-1].click()
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="archive-seasons"]/div/div[1]')))

element.click()
checking = driver.find_element_by_class_name('block')
response_season = driver.page_source
soup_season = BeautifulSoup(response_season, 'html.parser')
soup_table = soup_season.find('div', 'block')

print(len(soup_table))
for el in soup_table:
    print(el)