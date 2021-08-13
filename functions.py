import requests
from bs4 import BeautifulSoup

def get_match_result(soup):
    '''
        Функция получает результат матча
        :return возвращает названия команд и результат матча
        Длина возвращаемого списка match_result_list == 5
        ['Хоязяева', 'Гости', 'Голы хозяев', 'Голы гостей', 'Дата матча']
    '''
    # Получаем блок с результатми матча
    match_result = soup.find('div', class_='match-complete block block-section')
    if match_result != None:
        # Получаем название первой команды
        team_1 = match_result.findAll('span', class_='heading heading-3')[-1].get_text().replace('\n', '').split(' — ')[0]
        # Получаем название второй команды
        team_2 = match_result.findAll('span', class_='heading heading-3')[-1].get_text().replace('\n', '').split(' — ')[1]
        # Получаем количество голов первой команды
        team_1_goals = match_result.findAll('span', class_='heading heading-3')[0].get_text().replace('\n', '').replace(' ', '')[0]
        # Получаем количество голов второй команды
        team_2_goals = match_result.findAll('span', class_='heading heading-3')[0].get_text().replace('\n', '').replace(' ', '')[2]
        # Получаем дату матча
        match_date = match_result.find('span', class_='heading heading-4').get_text().replace('\n', '')
        # print(team_1, team_2, team_1_goals, team_2_goals, match_date)
        match_result_list = [team_1, team_2, team_1_goals, team_2_goals, match_date]
        return team_1, team_2, match_date, match_result_list
    else:
        match_result = soup.find('span', class_='tip time-before').get_text().replace('\n', '')
        return 0, 0, 0, match_result


def get_text_info(soup, team_1, team_2):
    '''
        Парсинг текстовой информации о матче
        :return стадион, судья, турнирные расклады, инфу о хозяевах, инфу о гостях, инфу для ставок
        Длина возвращаемого списка text_info_list == 7
        ['Стадион', 'Судья', 'О матче', 'Турнирные расклады', 'О хозяевах', 'О гостях', 'Информация для ставок']
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
    print(add_info)
    try:
        # first_team_split == название первой команды + первые несколько букв текста за ним (пример: «Брайтон»Подоп)
        first_team_split = add_info.split(f'<h3>«{team_1}»</h3><p>')[1][:5]
    except IndexError:
        first_team_split = add_info.split(f'<h3>«{team_1}  »</h3><p>')[1][:5]
    # first_team_split == название второй команды + первые несколько букв текста за ним (пример: «Брайтон»Подоп)
    second_team_split = add_info.split(f'<h3>«{team_2}»</h3><p>')[1][:5]

    about_match = info_temp.split('Турнирные расклады')[0]
    try:
        tournament_layouts = f'«{team_1}»' + info_temp.split('Турнирные расклады')[1].split(first_team_split)[0].replace(f'«{team_1}»', '')
    except IndexError:
        tournament_layouts = 'Нет информации'
    about_team_1 = first_team_split + info_temp.split(f'«{team_1}»' + first_team_split)[1].split(f'«{team_2}»' + second_team_split)[0]
    about_team_2 = second_team_split + info_temp.split(f'«{team_2}»' + second_team_split)[1].split('Информация для ставок')[0]

    bet_info_soup = add_info.split('<h3>Информация для ставок</h3>')[-1]
    bet_info = BeautifulSoup(bet_info_soup, 'html.parser')
    bet_info = bet_info.get_text().replace('\n\n\n\n', '').replace(' \n', ' ').replace('\n', ' ')

    text_info_list = [stadium, referee, about_match, tournament_layouts, about_team_1, about_team_2, bet_info]
    return text_info_list

def get_coefs(soup, bookmaker_list):
    '''
        Функция парсит все данные по коэффициентам выбранных букмекеров
        :return список коэффициентов
        Длина возвращаемого списка get_coefs_list == 18
        ['1хСтавка', '1', 'Х', '2', 'ТМ 2.5', 'ТБ 2.5',
        'Winline', '1', 'Х', '2', 'ТМ 2.5', 'ТБ 2.5',
        'Fonbet', '1', 'Х', '2', 'ТМ 2.5', 'ТБ 2.5']
    '''
    get_coefs_list = []
    coefs_table = soup.find('table', class_='match-odds-table')
    rows = coefs_table.findAll("tr", class_="inactive")
    for row in rows:
        cell = row.find('div', class_='title')
        bookmaker_name = cell.get_text().replace('\n', '').replace(' ', '')
        # print(cell)
        # print()
        # print(bookmaker_name)
        # print('--------------------')
        if bookmaker_name in bookmaker_list:
            # print(bookmaker_name)
            get_coefs_list.append(bookmaker_name)
            coefs = row.findAll('div', class_=['odd match-rates-marker', 'odd match-rates-marker best-odd', 'empty',
                                               'odd match-rates-marker up trend-up', 'odd match-rates-marker down trend-down',
                                               'odd match-rates-marker best-odd up trend-up'])
            for coef in coefs:
                # print(coef.get_text().replace('\n', ''))
                get_coefs_list.append(coef.get_text().replace('\n', ''))
    if check_len(get_coefs_list, 18):
        get_coefs_list.extend([0 for i in range(18 - len(get_coefs_list))])
    return get_coefs_list

def get_personal_meetings(soup):
    '''
        Функция парсит результаты последних встреч между командами
        :return список с результатами последних встреч
        Длина возвращаемого списка personal_meetings_list == 30 (Берем последние 5 встреч между командами)
        ['Турнир', 'Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей' ... х 5
    '''
    personal_meetings_block = soup.find('div',
                                        class_='matches-history_football matches-history block-section teams-meets-block')
    personal_meetings_list = []
    try:
        meetings_info = personal_meetings_block.findAll('div', class_=['category', 'match-score'])
        for idx, info in enumerate(meetings_info):
            if info['class'] == ['category']:
                personal_meetings_list.append(info.get_text())
            elif info['class'] == ['match-score']:
                match_date = info.find('div', class_='grey-text').get_text()
                owner = info.find('div', class_='top-side').find('div',
                                                                 class_=['left-side', 'green-text left-side']).get_text()
                guest = info.find('div', class_='top-side').find('div',
                                                                 class_=['right-side', 'green-text right-side']).get_text()
                try:
                    owner_goals = info.findAll('div', class_='number')[0].get_text()
                    guest_goals = info.findAll('div', class_='number')[1].get_text()
                    if meetings_info[idx - 1]['class'] == ['category']:
                        personal_meetings_list.extend([match_date, owner, guest, owner_goals, guest_goals])
                    elif meetings_info[idx - 1]['class'] == ['match-score']:
                        personal_meetings_list.append(meetings_info[idx - 2].get_text())
                        personal_meetings_list.extend([match_date, owner, guest, owner_goals, guest_goals])
                except IndexError:
                    if meetings_info[idx - 1]['class'] == ['category']:
                        personal_meetings_list.pop(-1)


        if len(personal_meetings_list) < 30:
            personal_meetings_list.extend([0 for i in range(30 - len(personal_meetings_list))])

    # Если истории нет
    except AttributeError:
        personal_meetings_list.extend([0 for i in range(30 - len(personal_meetings_list))])

    return personal_meetings_list[:30]

def match_history(match):
    '''
        Функция парсит все данные по матчу из истории
        : return спсиок с результатми матча
        Длина возвращаемого списка match_history == 5
        ['Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей']
    '''
    match_date = match.find('div', class_='grey-text').get_text()
    owner = match.find('div', class_='top-side').find('div',
                                                      class_=['left-side', 'left-side bold']).get_text().replace(' ',
                                                                                                                '')
    guest = match.find('div', class_='top-side').find('div', class_=['right-side', 'right-side bold']).get_text()
    owner_goals = match.findAll('div', class_='number')[0].get_text()
    guest_goals = match.findAll('div', class_='number')[1].get_text()
    match_history = [match_date, owner, guest, owner_goals, guest_goals]
    return match_history

def get_matches_history(soup):
    '''
        Функция получения истории результатов последних матчей
        :return список с результатми последних матчей в турнире, снчала хозяев, потом гостей
        Длина возвращаемого списка matches_history_list == 70, берем по 7 последних матчей
        ['Дата матча', 'Хозяева', 'Гости', 'Голы хозяев', 'Голы гостей' ... x 14
    '''
    matches_history_list = []  # Список для хранения всех результатов

    # Парсим блок с результатами
    matches_history = soup.findAll('div', class_='matches-history-block block')

    # Получаем блок с реузльтатми хозяев (если история есть)
    try:
        matches_history_owner = matches_history[0].findAll('div', class_='match-score')

        # Проходим по каждому матчу хозяев, аппендим данные в список (берем последние 5 матчей)
        for num, match in enumerate(matches_history_owner):
            if num < 7:
                curr_match = match_history(match)
                matches_history_list.extend(curr_match)
        if check_len(matches_history_list, 35):
            matches_history_list.extend([0 for i in range(35 - len(matches_history_list))])
    # Если истории нет
    except IndexError:
        matches_history_list.extend([0 for i in range(35 - len(matches_history_list))])

    # Получаем блок с реузльтатми гостей (если история есть)
    try:
        matches_history_guest = matches_history[1].findAll('div', class_='match-score')

        # Проходим по каждому матчу гостей, аппендим данные в список (берем последние 5 матчей)
        for num, match in enumerate(matches_history_guest):
            if num < 7:
                curr_match = match_history(match)
                matches_history_list.extend(curr_match)
        if check_len(matches_history_list, 70):
            matches_history_list.extend([0 for i in range(70 - len(matches_history_list))])
    # Если истории нет
    except IndexError:
        matches_history_list.extend([0 for i in range(70 - len(matches_history_list))])

    return matches_history_list

def get_current_results(soup, team_1, team_2):
    '''
        Функция получения текущего положения команды в турнирной таблице
        :return список с данными по текущим результатам, например, позиция, забитые голы, очки и т.д.
        Длина возвращаемого списка owner_result == 10 + 6
        Длина возвращаемого списка guest_result == 10 + 6
        ['Название команды', 'Позиция', 'Перспектива', 'Победы', 'Ничьи', 'Поражения', 'Забитые голы', 'Пропущенные голы',
        'очки +3 позиции', 'очки +2 позиции', 'очки +1 позиции', 'очки', 'очки -1 позиции', 'очки -2 позиции', 'очки -3 позиции']
    '''
    # Парсим положение в турнирной таблице на текущий момент
    # Получаем таблицу с результатми всех команд
    owner_result = []
    guest_result = []

    tournament_table = soup.find('table', class_='tournament-table tournament-table_match with-uniforms')
    teams = tournament_table.findAll('tr', class_=['current', '', 'promotion', 'relegation'])
    all_points = []
    for idx, team in enumerate(teams):
        team_name = team.find('div', class_='team-caption').get_text()
        all_points.append(team.findAll('td')[6].get_text())
        if (team_name[:-1] in team_1):
            team_name = team_1
            position = idx + 1
            perspectives = team.find('div', class_='qualification-status')['title']
            plays = team.findAll('td')[1].get_text()
            wins = team.findAll('td')[2].get_text()
            draws = team.findAll('td')[3].get_text()
            defeats = team.findAll('td')[4].get_text()
            goals_scored = team.findAll('td')[5].get_text().split(':')[0]
            goals_missed = team.findAll('td')[5].get_text().split(':')[1]
            points = team.findAll('td')[6].get_text()

            owner_result.extend([team_name, position, perspectives, plays, wins, draws, defeats, goals_scored, goals_missed])

            for i in reversed(range(1, 4)):
                try:
                    if teams[idx - i].findAll('td')[6].get_text() >= points:
                        owner_result.append(teams[idx - i].findAll('td')[6].get_text())
                    else:
                        owner_result.append('0')
                except IndexError:
                    owner_result.append('0')
            owner_result.append(points)
            for i in range(1, 4):
                try:
                    if teams[idx + i].findAll('td')[6].get_text() <= points:
                        owner_result.append(teams[idx + i].findAll('td')[6].get_text())
                    else:
                        owner_result.append(0)
                except IndexError:
                    owner_result.append('0')
        elif (team_name[:-1] in team_2):
            team_name = team_2
            position = idx + 1
            perspectives = team.find('div', class_='qualification-status')['title']
            plays = team.findAll('td')[1].get_text()
            wins = team.findAll('td')[2].get_text()
            draws = team.findAll('td')[3].get_text()
            defeats = team.findAll('td')[4].get_text()
            goals_scored = team.findAll('td')[5].get_text().split(':')[0]
            goals_missed = team.findAll('td')[5].get_text().split(':')[1]
            points = team.findAll('td')[6].get_text()

            guest_result.extend(
                [team_name, position, perspectives, plays, wins, draws, defeats, goals_scored, goals_missed])

            for i in reversed(range(1, 4)):
                try:
                    if teams[idx - i].findAll('td')[6].get_text() >= points:
                        guest_result.append(teams[idx - i].findAll('td')[6].get_text())
                    else:
                        guest_result.append('0')
                except IndexError:
                    owner_result.append('0')
            guest_result.append(points)
            for i in range(1, 4):
                try:
                    if teams[idx + i].findAll('td')[6].get_text() <= points:
                        guest_result.append(teams[idx + i].findAll('td')[6].get_text())
                    else:
                        guest_result.append(0)
                except IndexError:
                    guest_result.append('0')
    return owner_result, guest_result

def check_len(list_to_check, length):
    if len(list_to_check) != length:
        return True

if __name__ == '__main__':
    match_url = 'https://legalbet.ru/match-center/atalanta-sampdoriya-04-03-2018/'
    response_match = requests.get(match_url)
    soup = BeautifulSoup(response_match.text, 'html.parser')
    team_1, team_2, match_date, match_result_list = get_match_result(soup)