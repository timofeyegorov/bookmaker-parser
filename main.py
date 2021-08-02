import requests
from bs4 import BeautifulSoup
from functions import get_match_result, get_text_info, get_coefs, get_personal_meetings
from functions import get_matches_history, get_current_results
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd

bookmaker_list = ['1хСтавка', 'Winline', 'Fonbet']

driver = webdriver.Chrome(executable_path=r'C:\Users\admin\PycharmProjects\bookmaker-parser\chromedriver.exe')
base_url = 'https://legalbet.ru'
url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
driver.get(url=url)

tabs_for_click = driver.find_elements_by_class_name('tabs__item')
tabs_for_click[-1].click()
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="archive-seasons"]/div/div[1]')))
# driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack','true');});",element)
m_idx = 0
data = []
prev_season = 0
for i in range(100):
    element.click()
    checking = driver.find_element_by_class_name('select-heading')
    curr_season = checking.get_attribute('innerHTML').replace('\n', '')
    if curr_season != prev_season:
        print(i, '. Парсится сезон ', curr_season, sep='')
        print('   //---------------//')
        WebDriverWait(driver, 20)
        response_season = driver.page_source

        # Ссылка на страницу со всеми матчами выбранной лиги
        # season_url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
        # response_season = requests.get(season_url)

        soup_season = BeautifulSoup(response_season, 'html.parser')
        soup_table = soup_season.find('div', 'tab-panel archive-tab active')
        soup_matches = soup_table.findAll('td', class_='match-td')

        for soup_match in soup_matches:
            m_idx += 1
            match_url = base_url + soup_match.find('a', class_='link')['href']
            response_match = requests.get(match_url)
            soup = BeautifulSoup(response_match.text, 'html.parser')
            try:
                team_1, team_2, match_date, match_result_list = get_match_result(soup)
                text_info_list = get_text_info(soup, team_1, team_2)
                coefs_list = get_coefs(soup, bookmaker_list)
                personal_meetings_list = get_personal_meetings(soup)
                matches_history_list = get_matches_history(soup)
                owner_result, guest_result = get_current_results(soup, team_1, team_2)

                # Генерируем задержку до следующего запроса от 1 до 11 секунд
                value = random.random()  # Генерируем случайное число от 0 до 1
                time_sleep = 1 + value * 10  # Добавляем случайное число к единице
                # print(f'Задержка до следующего запроса: {round(time_sleep, 1)} сек')
                time.sleep(time_sleep)  # Откладываем исполнение кода на time_sleep секунд
                # print('--------------------------------')
                data.append(match_result_list +\
                            text_info_list +\
                            coefs_list +\
                            personal_meetings_list +\
                            matches_history_list +\
                            owner_result + guest_result)
                # print(element.get_attribute("automationTrack"))
                print(f'{m_idx}. Завершен парсинг матча {team_1} - {team_2} сезона {curr_season}, {match_date}')
            except AttributeError:
                print(f'Парсинг матча прерван')
        prev_season = curr_season
    print('Парсинг сезона', curr_season, 'завершен')
    print('//---------------//')
print('Парсинг лиги завершен')

driver.close()
driver.quit()


df_data = pd.DataFrame(data)

df_data.to_csv('df_data')






# Парсим назвние сезона, название турнира


# Проведенные игры
# Игры до конца сезона
# очки до значимого места
# очки ближайших соперников
