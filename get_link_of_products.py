import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Функция для создания таблицы в базе данных
def create_products_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        link TEXT,
        parent TEXT
    )
    ''')
    connection.commit()

# Функция для вставки данных в таблицу
def insert_product(connection, link, parent):
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO products (link, parent)
    VALUES (?, ?)
    ''', (link, parent))
    connection.commit()

# Функция для получения категорий последнего уровня из базы данных
def get_last_level_categories(connection):
    cursor = connection.cursor()
    cursor.execute('''
    SELECT name, url FROM categories WHERE id NOT IN (
        SELECT DISTINCT parent FROM categories WHERE parent IS NOT NULL
    )
    ORDER BY id DESC  -- Здесь добавлено ключевое слово DESC для сортировки по убыванию
    ''')
    last_level_categories = cursor.fetchall()
    return last_level_categories

# Функция для получения ссылок на продукты
def get_links_of_product(url, parent):
    links = []

    page = 1

    while True:
        response = requests.get(f'{url}?page={page}')
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='products-table')

        if not table:
            print(f'Finish category: {parent}, page: {page}')
            break

        for a_tag in table.find_all('a'):
            link = a_tag.get('href')
            if link:
                product = {
                    'link': link,
                    'parent': parent
                }
                links.append(product)

        print(f'Category: {parent}, Page: {page}')  # Вывод текущей категории и страницы в консоль

        page += 1  # Увеличиваем номер страницы

        # Добавляем задержку перед следующим запросом (чтобы не нагружать сервер)
        time.sleep(3)

    return links

# Подключаемся к базе данных categories.db
conn_categories = sqlite3.connect('./categories/categories.db')

# Создаем таблицу для продуктов в базе данных products_link.db
conn_products = sqlite3.connect('products_link.db')
create_products_table(conn_products)

# Получаем категории последнего уровня в обратном порядке
last_level_categories = get_last_level_categories(conn_categories)

# Обходим каждую категорию и получаем ссылки на продукты
for category_name, category_url in last_level_categories:
    category_name = category_name.strip()
    product_links = get_links_of_product(category_url, category_name)

    # Вставляем данные в таблицу products
    for product in product_links:
        insert_product(conn_products, product['link'], product['parent'])

# Закрываем соединение с обеими базами данных
conn_categories.close()
conn_products.close()
