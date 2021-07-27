import requests
from bs4 import BeautifulSoup

def get_match_result(soup):
    match_result = soup.find('div', class_='match-complete block block-section')
    team_1 = match_result.findAll('span', class_='heading heading-3')[-1].get_text().replace('\n', '').split(' — ')[0]
    team_2 = match_result.findAll('span', class_='heading heading-3')[-1].get_text().replace('\n', '').split(' — ')[1]
    team_1_goals = match_result.findAll('span', class_='heading heading-3')[0].get_text().replace('\n', '')[0]
    team_2_goals = match_result.findAll('span', class_='heading heading-3')[0].get_text().replace('\n', '')[2]
    match_date = match_result.find('span', class_='heading heading-4').get_text().replace('\n', '')
    # print(team_1, team_2, team_1_goals, team_2_goals, match_date)
    match_result_list = [team_1, team_2, team_1_goals, team_2_goals, match_date]

    return team_1, team_2, match_result_list

def get_text_info(soup):
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

    about_match = info_temp.split('Турнирные расклады')[0]
    tournament_layouts = f'«{team_1}»' + info_temp.split('Турнирные расклады')[1].split(first_team_split)[0].replace(f'«{team_1}»', '')
    about_team_1 = first_team_split + info_temp.split(f'«{team_1}»' + first_team_split)[1].split(f'«{team_2}»' + second_team_split)[0]
    about_team_2 = second_team_split + info_temp.split(f'«{team_2}»' + second_team_split)[1].split('Информация для ставок')[0]

    bet_info_soup = add_info.split('<h3>Информация для ставок</h3>')[-1]
    bet_info = BeautifulSoup(bet_info_soup, 'html.parser')
    bet_info = bet_info.get_text().replace('\n', '')

    text_info_list = [about_match, tournament_layouts, about_team_1, about_team_2, bet_info]

    print(about_match)
    print()
    print(tournament_layouts)
    print()
    print(about_team_1)
    print()
    print(about_team_2)
    print()
    print(bet_info)
    return text_info_list

def get_coefs(soup):
    get_coefs_list = []
    bookmaker_list = ['1хСтавка', 'Winline', 'Fonbet']
    coefs_table = soup.find('table', class_='match-odds-table')
    rows = coefs_table.findAll("tr", class_="inactive")
    for row in rows:
        cell = row.find('div', class_='title')
        bookmaker_name = cell.get_text().replace('\n', '')
        if bookmaker_name in bookmaker_list:
            # print(bookmaker_name)
            get_coefs_list.append(bookmaker_name)
            coefs = row.findAll('div', class_=['odd match-rates-marker', 'odd match-rates-marker best-odd'])
            for coef in coefs:
                # print(coef.get_text().replace('\n', ''))
                get_coefs_list.append(coef.get_text().replace('\n', '. '))
    return get_coefs_list

if __name__ == '__main__':
    url = 'https://legalbet.ru/match-center/brighton-and-hove-albion-manchester-city-15-05-2021/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    team_1, team_2, match_result_list = get_match_result(soup)
    text_info_list = get_text_info(soup)
    get_coefs_list = get_coefs(soup)

    # print(match_result_list)
    # print(text_info_list)
    # print(get_coefs_list)