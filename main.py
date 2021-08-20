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

# Файлы для записи данных
EPL = 'data_epl.csv'
LaLiga = 'data_LaLiga.csv'
serieA = 'data_serieA.csv'
bundesliga = 'data_bundesliga.csv'
ligue1 = 'data_ligue1.csv'
rpl = 'rpl.csv'

# sys.stdout = open('console_output.txt', 'a')

bookmaker_list = ['1хСтавка', ' 1хСтавка ', 'Winline', ' Winline ', 'Fonbet', ' Fonbet ']

driver = webdriver.Chrome(executable_path=r'C:\Users\User\PycharmProjects\bookmaker-parser\chromedriver.exe')
base_url = 'https://legalbet.ru'
url = 'https://legalbet.ru/match-center/tournaments/russian-premer-liga/'
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

columns = ['Сезон', 'Тур',
           'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей', 'Дата матча',
           '1хСтавка', '1_а', 'Х_а', '2_а', 'ТМ 2.5_а', 'ТБ 2.5_а',
           'Winline', '1_б', 'Х_б', '2_б', 'ТМ 2.5_б', 'ТБ 2.5_б',
           'Fonbet', '1_в', 'Х_в', '2_в', 'ТМ 2.5_в', 'ТБ 2.5_в',
           'Турнир_1', 'Дата матча_1', 'Хозяева_1', 'Гости_1', 'Голы хозяев_1', 'Голы гостей_1',
           'Турнир_2', 'Дата матча_2', 'Хозяева_2', 'Гости_2', 'Голы хозяев_2', 'Голы гостей_2',
           'Турнир_3', 'Дата матча_3', 'Хозяева_3', 'Гости_3', 'Голы хозяев_3', 'Голы гостей_3',
           'Турнир_4', 'Дата матча_4', 'Хозяева_4', 'Гости_4', 'Голы хозяев_4', 'Голы гостей_4',
           'Турнир_5', 'Дата матча_5', 'Хозяева_5', 'Гости_5', 'Голы хозяев_5', 'Голы гостей_5',
           'Дата матча_6', 'Хозяева_6', 'Гости_6', 'Голы хозяев_6', 'Голы гостей_6',
           'Дата матча_7', 'Хозяева_7', 'Гости_7', 'Голы хозяев_7', 'Голы гостей_7',
           'Дата матча_8', 'Хозяева_8', 'Гости_8', 'Голы хозяев_8', 'Голы гостей_8',
           'Дата матча_9', 'Хозяева_9', 'Гости_9', 'Голы хозяев_9', 'Голы гостей_9',
           'Дата матча_10', 'Хозяева_10', 'Гости_10', 'Голы хозяев_10', 'Голы гостей_10',
           'Дата матча_11', 'Хозяева_11', 'Гости_11', 'Голы хозяев_11', 'Голы гостей_11',
           'Дата матча_12', 'Хозяева_12', 'Гости_12', 'Голы хозяев_12', 'Голы гостей_12',
           'Дата матча_13', 'Хозяева_13', 'Гости_13', 'Голы хозяев_13', 'Голы гостей_13',
           'Дата матча_14', 'Хозяева_14', 'Гости_14', 'Голы хозяев_14', 'Голы гостей_14',
           'Дата матча_15', 'Хозяева_15', 'Гости_15', 'Голы хозяев_15', 'Голы гостей_15',
           'Дата матча_16', 'Хозяева_16', 'Гости_16', 'Голы хозяев_16', 'Голы гостей_16',
           'Дата матча_17', 'Хозяева_17', 'Гости_17', 'Голы хозяев_17', 'Голы гостей_17',
           'Дата матча_18', 'Хозяева_18', 'Гости_18', 'Голы хозяев_18', 'Голы гостей_18',
           'Дата матча_19', 'Хозяева_19', 'Гости_19', 'Голы хозяев_19', 'Голы гостей_19',
           'Название команды_1', 'Позиция_1', 'Перспектива_1', 'Игры_1', 'Победы_1', 'Ничьи_1', 'Поражения_1', 'Забитые голы_1', 'Пропущенные голы_1',
           'очки +3 позиции_1', 'очки +2 позиции_1', 'очки +1 позиции_1', 'очки_1', 'очки -1 позиции_1', 'очки -2 позиции_1', 'очки -3 позиции_1',
           'Название команды_2', 'Позиция_2', 'Перспектива_2', 'Игры_2', 'Победы_2', 'Ничьи_2', 'Поражения_2', 'Забитые голы_2', 'Пропущенные голы_2',
           'очки +3 позиции_2', 'очки +2 позиции_2', 'очки +1 позиции_2', 'очки_2', 'очки -1 позиции_2', 'очки -2 позиции_2', 'очки -3 позиции_2'
           ]
with open(rpl, 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=';')
    datawriter.writerow(columns)

seasons_tabs = ['tab-panel js-archive-season-tab-201',
                'tab-panel js-archive-season-tab-131',
                'tab-panel js-archive-season-tab-126',
                'tab-panel js-archive-season-tab-116',
                'tab-panel js-archive-season-tab-106',
                'tab-panel js-archive-season-tab-76',
                'tab-panel js-archive-season-tab-2'
                ]
num_seasons = len(seasons_tabs)

for i in range(num_seasons):
    element.click()

    checking = driver.find_element_by_class_name('select-heading')
    curr_season = checking.get_attribute('innerHTML').replace('\n', '')
    if curr_season != prev_season:
        season_m = 0
        print(f'Парсится сезон {curr_season}', sep='')
        print('-'*len(f'Парсится сезон {curr_season}'))

        print(f'Парсится сезон {curr_season}', sep='', file = open('console_output.txt', 'a'))
        print('-'*len(f'Парсится сезон {curr_season}'), file = open('console_output.txt', 'a'))

        WebDriverWait(driver, 20)

        response_season = driver.page_source

        soup = BeautifulSoup(response_season, 'html.parser')
        soup_all_seasons = soup.find('div', class_='tab-panel archive-tab active')
        soup_season = soup_all_seasons.find('div', class_=seasons_tabs[i] + ' active')
        # tour_num = soup_season.find('div', class_='heading heading-3').get_text()
        # soup_matches = soup_season.findAll('td', class_='match-td')


        soup_tours = soup_season.findAll('div', class_='block-section')

        for tour in soup_tours:
            soup_tour = tour.find('div', class_='heading heading-3')
            if soup_tour != None:
                # print(tour)
                # print('---')
                tour_num = soup_tour.get_text().replace('\n', '')
                if tour_num == 'Переходные матчи':
                    print(f'Парсинг матча прерван, причина: {tour_num}')
                    print(f'Парсинг матча прерван, причина: {tour_num}', \
                          file=open('console_output.txt', 'a'))
                    continue
                # print(tour_num)
                # print('---')
                soup_matches = tour.findAll(['td', 'th'], class_=['match-td', 'match-th'])
                # print(soup_matches)
                # print('---')
                soup_coefs = tour.findAll('tr')
                # print(soup_coefs)
                # print('---')
                # print(len(soup_coefs))
                # print('---')
                # print(soup_matches[0])
                # print('---')
                # print(soup_matches[1])
                # print('---')
                # print(soup_coefs[1].findAll('td', class_='odd-td'))
                soup_coefs_add = len(tour.findAll('tr', class_='league-row'))
                # print(m_idx, season_m, len(soup_matches)==len(soup_coefs))

                for idx, soup_match in enumerate(soup_matches):
                    if soup_match.find('a', class_='link') != None:
                        m_idx += 1
                        season_m += 1
                        add_info = ''
                        if (season_m > 0)&(m_idx>249):
                            match_url = base_url + soup_match.find('a', class_='link')['href']
                            response_match = requests.get(match_url)
                            soup = BeautifulSoup(response_match.text, 'html.parser')
                            # try:
                            team_1, team_2, match_date, match_result_list = get_match_result(soup)
                            if team_1 == 0:
                                print(f'Парсинг матча прерван, причина: {match_result_list}')
                                print(f'Парсинг матча прерван, причина: {match_result_list}',
                                        file = open('console_output.txt', 'a'))
                            else:
                                # text_info_list = get_text_info(soup, team_1, team_2)
                                try:
                                    coefs_list = get_coefs(soup, bookmaker_list)
                                except AttributeError:
                                    # print(soup_coefs)
                                    coefs_list = ['Неизвестно']
                                    coefs_list.append(soup_coefs[idx].findAll('td', class_='odd-td')[0].get_text())
                                    coefs_list.append(soup_coefs[idx].findAll('td', class_='odd-td')[1].get_text())
                                    coefs_list.append(soup_coefs[idx].findAll('td', class_='odd-td')[2].get_text())
                                    coefs_list.append(soup_coefs[idx].findAll('td', class_='odd-td')[3].get_text())
                                    coefs_list.append(soup_coefs[idx].findAll('td', class_='odd-td')[4].get_text())
                                    add_info = ['ПРОВЕРИТЬ КОЭФФИЦИЕНТЫ: '] + coefs_list
                                    if check_len(coefs_list, 18):
                                        coefs_list.extend([0 for i in range(18 - len(coefs_list))])
                                if coefs_list != -1:
                                    personal_meetings_list = get_personal_meetings(soup)
                                    matches_history_list = get_matches_history(soup)
                                    owner_result, guest_result = get_current_results(soup, team_1, team_2)


                                    # Генерируем задержку до следующего запроса от 1 до 11 секунд
                                    value = random.random()  # Генерируем случайное число от 0 до 1
                                    time_sleep = 1 + value * 10  # Добавляем случайное число к единице
                                    # print(f'Задержка до следующего запроса: {round(time_sleep, 1)} сек')
                                    time.sleep(time_sleep)  # Откладываем исполнение кода на time_sleep секунд
                                    # print('--------------------------------')
                                    match_list = [curr_season, tour_num] +\
                                                 match_result_list +\
                                                 coefs_list +\
                                                 personal_meetings_list +\
                                                 matches_history_list +\
                                                 owner_result + guest_result
                                    data.append(match_list)
                                    # print(element.get_attribute("automationTrack"))
                                    print(f'(ИТОГО: {m_idx} игр) Завершен парсинг матча (№{season_m}) {team_1} - {team_2} сезона {curr_season}, {match_date}. {add_info}')
                                    print(f'(ИТОГО: {m_idx} игр) Завершен парсинг матча (№{season_m}) {team_1} - {team_2} сезона {curr_season}, {match_date}. {add_info}', \
                                            file = open('console_output.txt', 'a'))
                                    if check_len(match_result_list, 5):
                                        print('Список с результатами длинее 5 элементов (ожидается 5)')
                                        print(match_result_list)
                                        print('Список с результатами длинее 5 элементов (ожидается 5)', file = open('console_output.txt', 'a'))
                                        print(match_result_list, file = open('console_output.txt', 'a'))
                                    # if check_len(text_info_list, 7):
                                    #     print('')
                                    if check_len(coefs_list, 18):
                                        print(f'Список coefs_list не совпадает - {len(coefs_list)} элементов (ожидается 18)')
                                        print(coefs_list)
                                        print(f'Список coefs_list не совпадает - {len(coefs_list)} элементов (ожидается 18)', file = open('console_output.txt', 'a'))
                                        print(coefs_list, file = open('console_output.txt', 'a'))
                                    if check_len(personal_meetings_list, 30):
                                        print(f'Список personal_meetings_list не совпадает - {len(personal_meetings_list)} элементов (ожидается 30)')
                                        print(personal_meetings_list)
                                        print(f'Список personal_meetings_list не совпадает - {len(personal_meetings_list)} элементов (ожидается 30)', file = open('console_output.txt', 'a'))
                                        print(personal_meetings_list, file = open('console_output.txt', 'a'))
                                    if check_len(matches_history_list, 70):
                                        print(f'Список matches_history_list не совпадает - {len(matches_history_list)} элементов (ожидается 70)')
                                        print(matches_history_list)
                                        print(f'Список matches_history_list не совпадает - {len(matches_history_list)} элементов (ожидается 70)', file = open('console_output.txt', 'a'))
                                        print(matches_history_list, file = open('console_output.txt', 'a'))
                                    if check_len(owner_result, 16):
                                        print(f'Список owner_result не совпадает - {len(owner_result)} элементов (ожидается 16)')
                                        print(owner_result)
                                        print(f'Список owner_result не совпадает - {len(owner_result)} элементов (ожидается 16)', file = open('console_output.txt', 'a'))
                                        print(owner_result, file = open('console_output.txt', 'a'))
                                    if check_len(guest_result, 16):
                                        print(f'Список guest_result не совпадает - {len(guest_result)} элементов (ожидается 16)')
                                        print(guest_result)
                                        print(f'Список guest_result не совпадает - {len(guest_result)} элементов (ожидается 16)', file = open('console_output.txt', 'a'))
                                        print(guest_result, file = open('console_output.txt', 'a'))
                                    with open(rpl, 'a', newline='') as csvfile:
                                        datawriter = csv.writer(csvfile, delimiter=';')
                                        datawriter.writerow(match_list)
                                else:
                                    print(f'Парсинг матча прерван, причина: Тех поражение')
                                    print(f'Парсинг матча прерван, причина: Тех поражение',
                                          file=open('console_output.txt', 'a'))

        print(f'Парсинг сезона', curr_season, 'завершен')
        prev_season = curr_season
        print('-'*len(f'Парсится сезон {curr_season}'))
        print(f'Парсинг сезона', curr_season, 'завершен', file = open('console_output.txt', 'a'))
        print('-'*len(f'Парсится сезон {curr_season}'), file = open('console_output.txt', 'a'))
print()
print('Парсинг лиги завершен')
print(file = open('console_output.txt', 'a'))
print('Парсинг лиги завершен', file = open('console_output.txt', 'a'))
end_time = time.time() - start_time
print('Затраченное время: ', int(round(end_time / 60, 0)), 'минут', int(round(end_time//60*60, 0)), 'секунд')
print('Затраченное время: ', int(round(end_time / 60, 0)), 'минут', int(round(end_time // 2 * 60 / 100, 0)),
              'секунд', file = open('console_output.txt', 'a'))
driver.close()
driver.quit()
# sys.stdout.close()
