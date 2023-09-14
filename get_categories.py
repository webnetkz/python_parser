import requests
from bs4 import BeautifulSoup
import json


url = "https://anepmetall.kz/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


ul = soup.find('ul', class_='list-unstyled scroll-ul border')


def get_category():
    categories = []
    for li in ul.find_all('li'):
        a_tag = li.find('a')
        category = {
            'name': a_tag.find('span').text.strip(),
            'url': a_tag['href'],
            'parent': 0
        }
        categories.append(category)
    
    return categories

print(get_category())
exit()




# 6. Далее в каждом элементе есть div со списком второго уровня
for category in categories:
    category_url = category['url']
    category_response = requests.get(category_url)
    category_soup = BeautifulSoup(category_response.text, 'html.parser')

    # 7. Извлекаем категории второго уровня
    sub_categories = []
    sub_ul = category_soup.find('ul', class_='your-sub-ul-class')  # Замените на класс вашего под-списка
    if sub_ul:
        for sub_li in sub_ul.find_all('li'):
            sub_a_tag = sub_li.find('a')
            sub_category = {
                'name': sub_a_tag.find('span').text.strip(),
                'url': sub_a_tag['href'],
                'parent': category['name']  # Обозначаем родительскую категорию
            }
            sub_categories.append(sub_category)

        # 8. В списке второго уровня также может быть список третьего уровня (повторите шаги по необходимости)

    category['sub_categories'] = sub_categories

# Создаем JSON-файл
with open('categories.json', 'w', encoding='utf-8') as json_file:
    json.dump(categories, json_file, ensure_ascii=False, indent=4)
