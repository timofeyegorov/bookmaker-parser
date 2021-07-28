import requests
from bs4 import BeautifulSoup
from functions import get_match_result, get_text_info, get_coefs, get_personal_meetings
from functions import match_history, get_matches_history, get_current_results
import time
import random

season_classes =\
    ['tab-panel js-archive-season-tab-201 active',
     'tab-panel js-archive-season-tab-131',
     'tab-panel js-archive-season-tab-126',
     'tab-panel js-archive-season-tab-116',
     'tab-panel js-archive-season-tab-106',
     'tab-panel js-archive-season-tab-76',
     'tab-panel js-archive-season-tab-2']

# Ссылка на страницу со всеми матчами выбранного сезона
season_url = 'https://legalbet.ru/match-center/tournaments/england-premer-liga/'
response_season = requests.get(season_url)
soup_season = BeautifulSoup(response_season.text, 'html.parser')
print(soup_season.findAll('div', class_='block-section'))

# for season_class in season_classes[:1]:
#     print(season_class)
#     rounds = soup_season.find('div', class_=season_class)
#     print(rounds)
#     for round in rounds[:1]:
#         print(round)
#         matches = round.findAll('td', class_='match-td')
#         for match in matches[:2]:
#             match_url = match.find('a', class_='link')
#             print(match_url)

# bookmaker_list = ['1хСтавка', 'Winline', 'Fonbet']
# url = 'https://legalbet.ru/match-center/brighton-and-hove-albion-manchester-city-15-05-2021/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# team_1, team_2, match_result_list = get_match_result(soup)
# text_info_list = get_text_info(soup, team_1, team_2)
# coefs_list = get_coefs(soup, bookmaker_list)
# personal_meetings_list = get_personal_meetings(soup)
# matches_history_list = get_matches_history(soup)
# owner_result, guest_result = get_current_results(soup, team_1, team_2)

# Генерируем задержку до следующего запроса от 1 до 11 секунд
value = random.random()  # Генерируем случайное число от 0 до 1
time_sleep = 1 + value * 10  # Добавляем случайное число к единице
print(f'Задержка до следующего запроса: {round(time_sleep, 1)} сек')
time.sleep(time_sleep)  # Откладываем исполнение кода на time_sleep секунд
print('--------------------------------')


# Парсим назвние сезона, название турнира


# Проведенные игры
# Игры до конца сезона
# очки до значимого места
# очки ближайших соперников
