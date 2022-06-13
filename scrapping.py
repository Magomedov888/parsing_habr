import json
from random import choice
from pprint import pprint

from bs4 import BeautifulSoup
import requests


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},

]

url = 'https://freelance.habr.com/tasks?q=Python'

response = requests.get(url, headers=choice(headers))


jobs = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='task task_list')
    for article in articles:
        url = 'https://freelance.habr.com/' + article.a['href']
        title = article.find('div', class_='task__title').text.strip()
        price = article.find('div', class_='task__price').text.strip()
        responses = article.find('span', class_='params__responses')
        responses = responses.text.strip() if responses else '0 отликов'
        views = article.find('span', class_='params__views').text.strip()
        published_at = article.find(
            'span', class_='params__published-at').text.strip()
        tags = [tag.text for tag in article.find_all(
            'a', class_='tags__item_link')]
        jobs.append({'url': url, 'title': title, 'price': price, 'responses': responses,
                     'views': views, 'published_at': published_at, 'tags': tags})
with open('jobs.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(jobs, indent=4, ensure_ascii=False))