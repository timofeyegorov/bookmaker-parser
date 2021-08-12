import requests
from bs4 import BeautifulSoup

match_url = 'https://legalbet.ru/match-center/atalanta-sampdoriya-04-03-2018/'
response_match = requests.get(match_url)
soup = BeautifulSoup(response_match.text, 'html.parser')

match_result = soup.find('div', class_='match-complete block block-section')

print(match_result)

match_result = soup.find('span', class_='tip time-before').get_text().replace('\n', '')

print(match_result)