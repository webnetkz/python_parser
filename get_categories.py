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
                            'parent_level_two': a_tag.find('span').text.strip(),
                            'parent_level_one': a_tag_2.find('span').text.strip()
                        }
                        categories.append(category)
    
    return categories
