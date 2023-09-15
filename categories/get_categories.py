import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://anepmetall.ru/"

def create_categories_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT,
        url TEXT,
        parent TEXT
    )
    ''')
    connection.commit()

def insert_category(connection, name, url, parent):
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO categories (name, url, parent)
    VALUES (?, ?, ?)
    ''', (name, url, parent))
    connection.commit()

def get_category_level_zero(url):
    categories = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ul = soup.find('ul', class_='list-unstyled scroll-ul border')

    for li in ul.find_all('li', recursive=False):
        a_tag = li.find('a')
        category = {
            'name': a_tag.find('span').text.strip(),
            'url': a_tag['href'],
            'parent': 0
        }
        categories.append(category)

    return categories

def get_category_level_two(url):
    categories = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ul = soup.find('ul', class_='list-unstyled scroll-ul border')

    for li in ul.find_all('li'):
        a_tag = li.find('a')
        ul_tag = li.find('ul')

        if ul_tag:
            for li_2 in ul_tag.find_all('li'):
                a_tag_2 = li_2.find('a')
                category = {
                    'name': a_tag_2.find('span').text.strip(),
                    'url': a_tag_2['href'],
                    'parent': a_tag.find('span').text.strip()
                }
                categories.append(category)

    return categories

def get_category_level_three(url):
    categories = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ul = soup.find('ul', class_='list-unstyled scroll-ul border')

    for li in ul.find_all('li'):
        a_tag = li.find('a')
        ul_tag = li.find('ul')

        if ul_tag:
            for li_2 in ul_tag.find_all('li'):
                a_tag_2 = li_2.find('a')
                ul_tag_2 = li_2.find('ul')

                if ul_tag_2:
                    for li_3 in ul_tag_2.find_all('li'):
                        a_tag_3 = li_3.find('a')
                        category = {
                            'name': a_tag_3.find('span').text.strip(),
                            'url': a_tag_3['href'],
                            'parent': a_tag.find('span').text.strip()
                        }
                        categories.append(category)

    return categories

# Создаем или подключаемся к базе данных SQLite
conn = sqlite3.connect('categories.db')

# Создаем таблицу для хранения категорий
create_categories_table(conn)

# Получаем списки категорий для каждого уровня
level_zero_categories = get_category_level_zero(url)  # Получаем категории нулевого уровня
level_two_categories = get_category_level_two(url)
level_three_categories = get_category_level_three(url)

# Объединяем списки категорий в один общий список
all_categories = level_zero_categories + level_two_categories + level_three_categories

# Вставляем данные в таблицу
for category in all_categories:
    insert_category(conn, category['name'], category['url'], category['parent'])

# Закрываем соединение с базой данных
conn.close()
