import asyncio
import json
from asyncio.locks import Condition
import pandas as pd
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import StringIO
import time
from tqdm import tqdm

async def gather_data(file_path):

    tasks = []
    for file in os.listdir(file_path):
        city = file.split('.')[0]
        print(city)
        with open(os.path.join(file_path, file), encoding='utf8') as f:
            urls = [url.strip() for url in f.readlines()]
            # print(urls)
            for pos, url in enumerate(urls):
                # print(url)
                task = asyncio.create_task(get_base_data(url, city, pos, len(urls)))
                tasks.append(task)
        # print(f'Обработано {counter+1}/{TOTAL_FILES} файл(а/ов)')
        await asyncio.sleep(30)
    asyncio.gather(*tasks)


async def get_base_data(url, city, pos, lenght):

    headers = {
       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebt/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36' 
    }
    # proxy = {'http':'103.95.40.211:3128'}
    async with ClientSession() as session:
        try:
            response = await session.get(url=url, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
        except Exception as _ex:
            print(_ex)
        try:
            company_id = url.split('firm/')[1]
        except:
            company_id = url.split('geo/')[1]
        try:
            company_name = soup.find('span', class_='_oqoid').text
        except:
            company_name = 'Неизвестно'
        try:
            phone = soup.find('div', class_ = '_b0ke8').find('a', class_='_2lcm958').get('href')
        except AttributeError:
            phone = 'Неизвестно'
        try:
            url = soup.find_all('a', {'target': '_blank', 'class':'_1rehek'})[1]
            if '.ru' not in url:
                url = 'Неизветно'
        except AttributeError:
            url = 'Неизвестно'
        try:
            social_media = '\n'.join([url.get('href') for url in soup.find_all('a', class_='_1rehek')[:4]])
        except AttributeError:
            social_media = 'Неизвестно'
        short_data.append([city, company_name, company_id, phone, url, social_media])
        print(f'Обработано: {pos}/{lenght}')

def format_hrefs(file_path):
    '''
    Делаем URLSы для публичной апишки, через которую будут запросы
    '''
    
    for file in os.listdir(file_path):
        urls = []
        with open(os.path.join(file_path, file), encoding='utf8') as f:
            # Забираем id компании            
            for url in f.readlines():
                try:
                    urls.append(url.strip().split('firm/')[1])
                except IndexError:
                    continue               
        
        with open(f'2gis\\review_hrefs\\{file}', 'w', encoding='utf8') as f_result:
            for url in urls:
                # link = URL_PART_1 + url + URL_PART_2 + datetime.today().strftime('%Y-%m-%d') + URL_PART_3 + '\n'     
                f_result.write(url+"\n")

        print(f'Ссылки по городу {file[:-4]} были подготовлены')


async def gather_review(file_path: str):
    
    # global full_data
    # full_data = {}
    tasks = []
    for file in os.listdir(file_path):
        city = file.split('.')[0]
        pd.DataFrame().to_csv(f'2gis\\company_info\\{city}.csv')
        # print(city)
        with open(os.path.join(file_path, file), encoding='utf8') as f:
            urls = [url.strip() for url in f.readlines()]
            # print(urls)
            for pos, url_id in enumerate(urls):
                # print(url)
                task = asyncio.create_task(parse_review(url_id, city, pos, len(urls)))
                tasks.append(task)
        # print(f'Обработано {counter+1}/{TOTAL_FILES} файл(а/ов)')
        await asyncio.sleep(30)
    asyncio.gather(*tasks)


async def parse_review(url_id, city, pos, length):

    URL_PART_1 = 'https://api.reviews.2gis.com/2.0/branches/'
    URL_PART_2 = '/reviews?fields=meta.providers%2Cmeta.branch_rating%2Cmeta.branch_reviews_count%2Cmeta.total_count%2Creviews.hiding_reason%2Creviews.is_verified&is_advertiser=false&key=37c04fe6-a560-4549-b459-02309cf643ad&limit=50&locale=ru_RU&offset_date='
    URL_PART_3 = 'T12%3A27%3A50.824879%2B07%3A00&rated=true&sort_by=date_edited'
    headers = {
       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebt/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36' 
    }
    async with ClientSession() as session:
        # df = pd.read_csv(f'2gis\\company_info\\{city}.csv')
        date = str(datetime.now().date() + timedelta(days=1))
        while True:
            url = URL_PART_1 + url_id + URL_PART_2 + date + URL_PART_3
            # print(url)
            response = await session.get(url=url, headers=headers)
            base_js = await response.json()
            # js = json.dumps(await base_js['reviews'])
            try:
                date = base_js['reviews'][-1]['date_created'][:10]
            except IndexError:
                break
            if len(base_js['reviews']):
                # pd.concat([df, pd.read_json(StringIO(js))]).to_csv(f'2gis\\company_info\\{city}.csv')
                # print(type(base_js))
                with open(f'2gis\\json\\{city}\\{time.time()}.json', 'w', encoding='utf8') as file:
                    json.dump(base_js['reviews'], file)

        print(f'Обработано: {pos+1}/{length}')


def create_frame():

    cities = ['CHELYABINSK', 'EKATERINBURG', 'KAZAN', 'KRASNODAR', 'MSC_part1', 'MSC_part2', 'NIZNIYNOVG', 'RND', 'SAMARA', 'SARATOV', 'SPB', 'UFA', 'VOLGOGRAD', 'VORONEZH', 'YOSHKAR-OLA']
    
    for city in cities:
        df = pd.DataFrame()
        for file in tqdm(os.listdir(f'2gis\\json\\{city}')):
            # data = json.load(open(f'2gis\\json\\{city}\\{file}'))
            new = pd.read_json(f'2gis\\json\\{city}\\{file}')         
            # new = pd.read_json(f'2gis\\json\\{city}\\{file}')
            df = pd.concat([df, new])
        df.to_csv(f'2gis\\company_info\\{city}.csv', index=False)
    print('Обработка отзывов завершена')

def main():
    global short_data
    short_data = []
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(gather_review('2gis\\review_hrefs'))
    # create_frame()
    asyncio.run(gather_data('2gis\\hrefs\\'))
    pd.DataFrame(short_data, columns=['City', 'Company', 'Company_id', 'Phone', 'URL', 'Social new']).to_csv('2gis\\ALL_DATA\\BASE_INFO.csv', index=False)
    # format_hrefs('2gis\\hrefs\\')
    


if __name__ == '__main__':
    main()