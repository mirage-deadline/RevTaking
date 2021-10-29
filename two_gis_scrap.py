from aiohttp import ClientSession
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium.webdriver.common.action_chains import ActionChains

from seleniumwire import webdriver


town_pairs = {
    'VOLGOGRAD': 'https://2gis.ru/volgograd/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D1%8F?m=44.428131%2C48.653067%2F11',
    'VORONEZH': 'https://2gis.ru/voronezh/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=39.200594%2C51.66073%2F11',
    'KRASNODAR': 'https://2gis.ru/krasnodar/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=38.971526%2C45.024359%2F11',
    'EKATERINBURG': 'https://2gis.ru/ekaterinburg/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=60.61642%2C56.839656%2F11',
    'CHELYABINSK': 'https://2gis.ru/chelyabinsk/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=61.402709%2C55.157389%2F11',
    'NIZNIYNOVG': 'https://2gis.ru/n_novgorod/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=43.928022%2C56.301157%2F11',
    'SAMARA': 'https://2gis.ru/samara/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=50.180997%2C53.20698%2F12',
    'KAZAN': 'https://2gis.ru/kazan/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=49.130025%2C55.798875%2F11',
    'UFA': 'https://2gis.ru/ufa/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=56.023289%2C54.773241%2F11',
    'SARATOV': 'https://2gis.ru/saratov/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=46.034329%2C51.533296%2F11',
    'YOSHKAR-OLA': 'https://2gis.ru/yoshkarola/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=47.887645%2C56.637319%2F11',
    'RND': 'https://2gis.ru/rostov/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=39.691771%2C47.222099%2F11',
    'MSC': 'https://2gis.ru/moscow/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=37.62017%2C55.753466%2F11',
    'SPB': 'https://2gis.ru/spb/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5?m=30.321941%2C59.928527%2F11', 
}

async def gather_data(city_pairs: dict):
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    tasks = []
    for city in city_pairs.keys():
        url = city_pairs[city]
        async with ClientSession() as session:
            response = await session.get(url=url, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            pages = int(soup.find('span', class_ = '_18lf326a').text)
            task = parse_first_data(session, url, pages, city)
            tasks.append(task)
    asyncio.gather(*tasks)

async def parse_first_data(session, url:str, max_pages: int, city: str):
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    global data
    data = []
    for page in range(1, max_pages+1):
        async with session.get(url=url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            for each in soup.find_all('div', class_='_1hf7139'):
                url = each.find('a').get('href')
                data.append([city, url])


def get_grefs(city_pairs: dict) -> None:

    login = 'dnxfuf'
    password = '24lhnBJG9a'
    proxy_options = {
        'proxy': {
            'https': f'http://{login}:{password}@193.57.136.78:24531'
        },
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    
    cities = [city for city in city_pairs.keys()]
    driver = webdriver.Chrome(executable_path='chromedriver_win32\\chromedriver.exe', seleniumwire_options=proxy_options)
    driver.maximize_window()

    for city in cities:
        hrefs = []
        try:
            i = 1
            driver.get(city_pairs[city])
            while True:
                i+=1
                element = driver.find_element(by='class name', value='_1x4k6z7')
                ActionChains(driver).move_to_element(element).perform()
                soup = BeautifulSoup(driver.page_source, 'lxml')
                base_http = 'https://2gis.ru/rostov'
                hrefs.append([base_http + url.find('a')['href'] for url in soup.find_all('div', class_='_1h3cgic')])
                pass
        except Exception as _ex:
            print(_ex)


def main():
    get_grefs()
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(gather_data()) # Передать словарь
    # pd.DataFrame(data, columns=['City', 'URL']).to_csv(os.path.join('ALL_goog.csv'), index=False)
    # pd.DataFrame(reviews_info, columns=['Company', 'City', 'Name', 'Date', 'Review']).to_csv(os.path.join('ALL.csv'), index=False)
    