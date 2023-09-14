import requests
from bs4 import BeautifulSoup
import json


url = "https://anepmetall.kz/"


def get_category_level_one(url):
    categories = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ul = soup.find('ul', class_='list-unstyled scroll-ul border')

    for li in ul.find_all('li'):
        a_tag = li.find('a')
        category = {
            'name': a_tag.find('span').text.strip(),
            'url': a_tag['href'],
            'parent': 1
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
                            'parent_level_two': a_tag.find('span').text.strip(),
                            'parent_level_one': a_tag_2.find('span').text.strip()
                        }
                        categories.append(category)
    
    return categories


# Получаем списки категорий для каждого уровня
level_one_categories = get_category_level_one(url)
level_two_categories = get_category_level_two(url)
level_three_categories = get_category_level_three(url)

# Объединяем списки категорий в один общий список
all_categories = level_one_categories + level_two_categories + level_three_categories

# Сериализуем данные в JSON
json_data = json.dumps(all_categories, ensure_ascii=False, indent=4)

# Сохраняем JSON в файл или выводим на экран
with open("categories.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)

# Если нужно вывести JSON на экран
print(json_data)




