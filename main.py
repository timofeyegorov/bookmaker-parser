import requests
from bs4 import BeautifulSoup
from functions import get_match_result, get_text_info, get_coefs, get_personal_meetings
from functions import get_matches_history, get_current_results, check_len
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd
import csv
import sys


# sys.stdout = open('console_output.txt', 'a')

bookmaker_list = ['1хСтавка', ' 1хСтавка ', 'Winline', ' Winline ', 'Fonbet', ' Fonbet ']

driver = webdriver.Chrome(executable_path=r'C:\Users\User\PycharmProjects\bookmaker-parser\chromedriver.exe')
base_url = 'https://legalbet.ru'
url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
driver.get(url=url)

tabs_for_click = driver.find_elements_by_class_name('tabs__item')
tabs_for_click[-1].click()
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="archive-seasons"]/div/div[1]')))
# driver.execute_script("var ele = arguments[0];ele.addEventListener('click', function() {ele.setAttribute('automationTrack','true');});",element)
m_idx = 0
data = []
match_list = []
prev_season = 0
start_time = time.time()

columns = ['Хоязяева', 'Гости', 'Голы хозяев', 'Голы гостей', 'Дата матча',
           '1хСтавка', '1', 'Х', '2', 'ТМ 2.5', 'ТБ 2.5',
           'Winline', '1', 'Х', '2', 'ТМ 2.5', 'ТБ 2.5',
           'Fonbet', '1', 'Х', '2', 'ТМ 2.5', 'ТБ 2.5',
           'Турнир', 'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Турнир', 'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Турнир', 'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Турнир', 'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Турнир', 'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей',
           'Название команды', 'Позиция', 'Перспектива', 'Игры', 'Победы', 'Ничьи', 'Поражения', 'Забитые голы', 'Пропущенные голы',
           'очки +3 позиции', 'очки +2 позиции', 'очки +1 позиции', 'очки', 'очки -1 позиции', 'очки -2 позиции', 'очки -3 позиции',
           'Название команды', 'Позиция', 'Перспектива', 'Игры', 'Победы', 'Ничьи', 'Поражения', 'Забитые голы', 'Пропущенные голы',
           'очки +3 позиции', 'очки +2 позиции', 'очки +1 позиции', 'очки', 'очки -1 позиции', 'очки -2 позиции', 'очки -3 позиции',
           ]
with open('data.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=';')
    datawriter.writerow(columns)


for i in range(100):
    element.click()
    checking = driver.find_element_by_class_name('select-heading')
    curr_season = checking.get_attribute('innerHTML').replace('\n', '')
    if curr_season != prev_season:
        print(i, '. Парсится сезон ', curr_season, sep='')
        print('----------------//')
        WebDriverWait(driver, 20)
        response_season = driver.page_source

        # Ссылка на страницу со всеми матчами выбранной лиги
        # season_url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
        # response_season = requests.get(season_url)

        soup_season = BeautifulSoup(response_season, 'html.parser')
        soup_table = soup_season.find('div', 'tab-panel archive-tab active')
        soup_matches = soup_table.findAll('td', class_='match-td')

        print(len(soup_matches))

        for soup_match in soup_matches:
            m_idx += 1
            if m_idx > 356:
                match_url = base_url + soup_match.find('a', class_='link')['href']
                response_match = requests.get(match_url)
                soup = BeautifulSoup(response_match.text, 'html.parser')
                try:
                    team_1, team_2, match_date, match_result_list = get_match_result(soup)
                    # text_info_list = get_text_info(soup, team_1, team_2)
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
                    match_list = match_result_list +\
                                 coefs_list +\
                                 personal_meetings_list +\
                                 matches_history_list +\
                                 owner_result + guest_result
                    data.append(match_list)
                    # print(element.get_attribute("automationTrack"))
                    print(f'{m_idx}. Завершен парсинг матча {team_1} - {team_2} сезона {curr_season}, {match_date}')
                    if check_len(match_result_list, 5):
                        print('Список с результатами длинее 5 элементов (ожидается 5)')
                        print(match_result_list)
                    # if check_len(text_info_list, 7):
                    #     print('')
                    if check_len(coefs_list, 18):
                        print(f'Список coefs_list не совпадает - {len(coefs_list)} элементов (ожидается 18)')
                        print(coefs_list)
                    if check_len(personal_meetings_list, 30):
                        print(f'Список personal_meetings_list не совпадает - {len(personal_meetings_list)} элементов (ожидается 30)')
                        print(personal_meetings_list)
                    if check_len(matches_history_list, 70):
                        print(f'Список matches_history_list не совпадает - {len(matches_history_list)} элементов (ожидается 70)')
                        print(matches_history_list)
                    if check_len(owner_result, 16):
                        print(f'Список owner_result не совпадает - {len(owner_result)} элементов (ожидается 16)')
                        print(owner_result)
                    if check_len(guest_result, 16):
                        print(f'Список guest_result не совпадает - {len(guest_result)} элементов (ожидается 16)')
                        print(guest_result)
                    with open('logs.csv', 'a', newline='') as csvfile:
                        datawriter = csv.writer(csvfile, delimiter=';')
                        datawriter.writerow(match_list)

                except AttributeError:
                    print(f'{m_idx}. Парсинг матча прерван')
                    match_list = ['Нет данных/парсинг матча прерван']
                # print(match_list)
                with open('data.csv', 'a', newline='') as csvfile:
                    datawriter = csv.writer(csvfile, delimiter=';')
                    datawriter.writerow(match_list)

        print('Парсинг сезона', curr_season, 'завершен')
        prev_season = curr_season
        print('//---------------//')
print('Парсинг лиги завершен')
end_time = time.time() - start_time
print(end_time/60, 'минут')
driver.close()
driver.quit()
# sys.stdout.close()

df_data = pd.DataFrame(data)

df_data.to_csv('df_data')






# Парсим назвние сезона, название турнира

# Сезон
# Проведенные игры
# Игры до конца сезона
# очки до значимого места
# очки ближайших соперников
