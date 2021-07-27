import requests
from bs4 import BeautifulSoup
from functions import get_match_result, get_text_info, get_coefs

url = 'https://legalbet.ru/match-center/brighton-and-hove-albion-manchester-city-15-05-2021/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

team_1, team_2, match_result_list = get_match_result(soup)
# text_info_list = get_text_info(soup)
# get_coefs_list = get_coefs(soup)


'''
    Парсинг текстовой информации о матче
    :return стадион, судья, турнирные расклады, инфу о хозяевах, инфу о гостях, инфу для ставок
'''
# Получаем блок с текстовой инфой о предстоящем матче
add_info = soup.find('div', class_='content-body body post-body match-lead no-paddings without-margins')
# Выцепляем инфу о стадионе и судье
stadium = add_info.find('div', class_='match-stadium').get_text()
referee = add_info.find('div', class_='match-referee').get_text()

# Получаем блок в текстом формате после инфы о судье
info_temp = add_info.get_text().replace('\n', '')
info_temp = info_temp.split('О матче')[1]

# Получаем дополнительные текстовые разделители
add_info = str(add_info)
# first_team_split == название первой команды + первые несколько букв текста за ним (пример: «Брайтон»Подоп)
first_team_split = add_info.split(f'<h3>«{team_1}»</h3><p>')[1][:5]
# first_team_split == название второй команды + первые несколько букв текста за ним (пример: «Брайтон»Подоп)
second_team_split = add_info.split(f'<h3>«{team_2}»</h3><p>')[1][:5]

# print(first_team_split)
# about_match = info_temp.split('Турнирные расклады')[0]
# tournament_layouts = f'«{team_1}»' + info_temp.split('Турнирные расклады')[1].split(first_team_split)[0].replace(f'«{team_1}»', '')
# about_team_1 = first_team_split + \
#                info_temp.split(f'«{team_1}»' + first_team_split)[1].split(f'«{team_2}»' + second_team_split)[0]
# about_team_2 = second_team_split + info_temp.split(f'«{team_2}»' + second_team_split)[1].split('Информация для ставок')[0]
bet_info = info_temp.split('Турнирные расклады')[1].split('Информация для ставок')[1]

# add_info = soup.find('div', class_='content-body body post-body match-lead no-paddings without-margins')
# bet_info_2 = add_info
#

# print(add_info.split('<h3>Информация для ставок</h3>')[-1])
x1 = add_info.split('<h3>Информация для ставок</h3>')[-1]
x2 = BeautifulSoup(x1, 'html.parser')
print(x2.get_text())
# Корректировка, чтобы корректно разбелялись блоки в Информация для ставок

# Парсим результаты последных личных встреч


# Парсим результаты последных встреч в турнире


# Парсим положение в турнирной таблице на текущий момент

