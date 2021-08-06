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

response_season = driver.page_source
soup = BeautifulSoup(response_season, 'html.parser')
soup_all_seasons = soup.find('div', class_='tab-panel archive-tab active')
# print(soup_table)
soup_season = soup_all_seasons.find('div', class_='tab-panel js-archive-season-tab-201 active')
tours = soup_season.findAll('div', class_='block-section')
print(len(tours))
for tour in tours:
    soup_tour = tour.find('div', class_='heading heading-3')
    print(soup_tour)
    if soup_tour != None:
        print(soup_tour.get_text())
        soup_matches = tour.findAll('td', class_='match-td')
        print(soup_matches)
    # tour_num = soup_season.find('div', class_='heading heading-3').get_text()
    # soup_matches = soup_season.findAll('td', class_='match-td')
# print(tour_num)
# print(len(soup_matches))
# print(soup_matches[0])

# print('---')
# soup_season = soup_all_seasons.find('div', class_='tab-panel js-archive-season-tab-131')
# tours = soup_season.findAll('div', class_='block-section')
# print(len(tours))
# for tour in tours:
#     print(type(tour))
#     # print(tour)
#     tour_num = tour.find('div', class_='heading heading-3').get_text()
#     print(tour_num)
#     soup_matches = tours.findAll('td', class_='match-td')
#     print(soup_matches)
# print(tour_num)
# print(len(soup_matches))
# print(soup_matches[0])
# for season in seasons:
#     tours = season.findAll('div', class_='block-section')
#     print(len(tours))
#     for tour in tours:
#         tour_num = tour.find('div', class_='heading heading-3').get_text()
#         print(tour_num)
#         soup_matches = tour_num.findAll('td', class_='match-td')
#         for soup_match in soup_matches:
#             match_url = base_url + soup_match.find('a', class_='link')['href']
#             print(match_url)

# print(len(tables))
# print(tables[0])

# soup_matches = tables.findAll('td', class_='match-td')
#
# print(type(tables))
#

# response_season = driver.find_element_by_id('archive')

# checking = driver.find_element_by_class_name('tab-panel archive-tab active')
# response_season = response_season.get_attribute('innerHTML')
# print(type(response_season))
# soup_season = BeautifulSoup(response_season, 'html.parser')
# soup_table = response_season.find('div', class_='tab-panel js-archive-season-tab-201')
# soup_matches = soup_table.findAll('td', class_='block-section')
#
# print(soup_matches[0])
# print(type(soup_table))
# print(len(soup_table))
# for el in soup_table:
#     print(el)

driver.close()
driver.quit()