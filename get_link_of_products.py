import requests
from bs4 import BeautifulSoup


def get_links_of_product(url, parent):
    links = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')   
    table = soup.find('table', class_='products-table')
    
    for a_tag in table.find_all('a'):
        link = a_tag.get('href')
        if link:
            product = {
                'link': link,
                'parent': parent
            }
            links.append(product)
    
    return links


print(get_links_of_product('https://anepmetall.kz/katalog/chernyj-metalloprokat/listovoj-prokat/list-perforirovannyj/', 'yes'))


exit()
