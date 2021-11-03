from aiohttp import ClientSession
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from numpy import short
import pandas as pd
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from seleniumwire import webdriver
import time

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

def get_grefs(city_pairs: dict) -> None:

    login = 'dnxfuf'
    password = '24lhnBJG9a'
    proxy_options = {
        'proxy': {
            'https': f'http://{login}:{password}@193.57.136.78:24531'
        },
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        "prefs": {"profile.default_content_setting_values.cookies": 2}
    }
    
    cities = [city for city in city_pairs.keys()]
    driver = webdriver.Chrome(executable_path='chromedriver_win32\\chromedriver.exe', seleniumwire_options=proxy_options)
    driver.maximize_window()

    for city in cities:
        hrefs = []
        try:
            i = 1
            driver.get(city_pairs[city])
            # driver.get('https://2gis.ru/volgograd/search/%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D1%8F?m=44.428131%2C48.653067%2F11')
            while True:
                
                try:  
                    i+=1
                    element = driver.find_element(by='class name', value='_1x4k6z7')
                    ActionChains(driver).move_to_element(element).perform()
                    time.sleep(3)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    for each in soup.find_all('div', class_='_1hf7139'):
                        url = each.find('div', class_='_1h3cgic').find('a').get('href')
                        hrefs.append(url)
                    page = driver.find_element(by='xpath', value = f"//span[text()='{i}']")
                    page.click()
                    time.sleep(2)              

                except NoSuchElementException:
                    with open(f'2gis\\row_hrefs\\{city}.txt', 'w', encoding='utf8') as file:
                        for href in hrefs:
                            file.write(href+'\n')
                    break
        except Exception as _ex:
            print(_ex)

def prepare_hrefs(city_dict):
    '''
    Создание полных ссылок, для дальнейшей работы
    '''

    cities = [city for city in city_dict.keys()]
    for city in cities:
        with open(f'2gis\\row_hrefs\\{city}.txt', encoding='utf8') as file:
            with open(f'2gis\\hrefs\\{city}.txt', 'w', encoding='utf8') as result:
                result_url = ['https://2gis.ru'+ url.strip().split('?')[0] for url in file.readlines()]
                # print(result_url)
                for url in result_url:
                    result.write(url+'\n')
        print(f'Ссылки по городу {city} были обработаны.')


async def gather_base_info(file_path:str):

    global short_data
    short_data = []
    tasks = []
    for file in os.listdir(file_path):
        city = file.split('.')[0]

        with open(os.path.join(file_path, file), encoding='utf8') as f:
            urls = [url.strip() for url in f.readlines()]     
            lenght = len(urls)
            
            for pos, url in enumerate(urls):                   
                task = asyncio.create_task(get_base_info(url, city, pos, lenght))
                tasks.append(task)
        # pd.DataFrame(short_data, columns=['City', 'Company', 'Phone', 'URL', 'Social new']).to_csv(f'2gis\\company_info\\{city}.csv', index=False)
        # await asyncio.sleep(20)
        # pd.DataFrame(short_data, columns=['City', 'Company', 'Phone', 'URL', 'Social new']).to_csv(f'2gis\\company_info\\CUMUL-{city}.csv', index=False)
    await asyncio.gather(*tasks)


async def get_base_info(url: str, city: str, pos, lenght):
    '''
    Функция запросов и создание соответствующейго csv под файл
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    # length = len(urls)
    # data = []
    async with ClientSession() as session:        
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        try:
            company_name = soup.find('span', class_='_oqoid').text
        except:
            company_name = 'Неизвестно'
        try:
            phone = soup.find('div', class_ = '_b0ke8').find('a', class_='_2lcm958').get('href')
        except AttributeError:
            phone = 'Неизвестно'
        try:
            url = soup.find('div', class_='_49kxlr').find('a', class_='_1rehek').text
        except AttributeError:
            url = 'Неизвестно'
        try:
            social_media = '\n'.join([url.get('href') for url in soup.find_all('a', class_='_1rehek')[:4]])
        except AttributeError:
            social_media = 'Неизвестно'
        short_data.append([city, company_name, phone, url, social_media])
        print(f'Обработано: {pos}/{lenght}')

def concat_pandas(file_path: str):

    files = os.listdir(file_path)[8:]
    df = pd.DataFrame()

    for file in files:
        df_city = pd.read_csv(os.path.join(file_path, file))
        df = pd.concat([df, df_city])
    df.drop_duplicates(inplace=True)
    df.to_csv('2gis\\ALL_DATA\\basic.csv', index=False)

def main():
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_base_info('2gis\\hrefs\\'))
    pd.DataFrame(short_data, columns=['City', 'Company', 'Phone', 'URL', 'Social new']).to_csv('2gis\\ALL_DATA\\BASE_SUMARY_2gis.csv', index=False)
    # concat_pandas('2gis\\company_info\\')
    # global data
    # data = []
    # get_grefs(town_pairs)
    # prepare_hrefs(town_pairs)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(gather_data()) # Передать словарь
    # pd.DataFrame(data, columns=['City', 'URL']).to_csv(os.path.join('ALL_goog.csv'), index=False)
    # pd.DataFrame(reviews_info, columns=['Company', 'City', 'Name', 'Date', 'Review']).to_csv(os.path.join('ALL.csv'), index=False)
    
if __name__ == '__main__':
    main()