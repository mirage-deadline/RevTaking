from bs4 import BeautifulSoup
import lxml
import os
import pandas as pd
import pyautogui
import requests
from fake_useragent import UserAgent
# from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import time
from fake_head import headers
import random
import sys

STATUS = str

city_comp1 = {
    'EKT': 'https://yandex.ru/maps/54/yekaterinburg/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=60.868184%2C56.843386&sctx=ZAAAAAgBEAAaKAoSCZjArbt5TE5AERlYx%2FFDa0xAEhIJZAJ%2BjSTB5T8Ry%2FRLxFvn2D8iBgABAgMEBSgKOABAmldIAWoCcnWdAc3MTD2gAQCoAQC9AR%2BF2J7CAYEBj%2FbovgaxsPCsrgOOqcTTBMXYhPYEmb7F2wSDv8eABOWs6vgD45Hy4gPXruuVBN2W5%2FgDxMHm%2FJ4GxuP3xocEiY3DlATkvrqllgTAiYG9BM7wzOkFr7qXjwez8pr8BI%2BY9d8D7LLdpwT4k5rfBaPCqp8Eq9WvmASP6am3BJWHk%2FkF6gEA8gEA%2BAEAggIn0J7RhdGA0LDQvdC90L7QtSDQv9GA0LXQtNC%2F0YDQuNGP0YLQuNC1igIJMTg0MTA1Mzc0&sll=60.868184%2C56.843386&sspn=1.301065%2C0.421560&z=10.6',
    'VOLG': 'https://yandex.ru/maps/38/volgograd/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=44.398123%2C48.648664&sll=44.398123%2C48.648664&sspn=1.230883%2C0.482207&z=10.68',
    'VORON': 'https://yandex.ru/maps/193/voronezh/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=39.152834%2C51.685788&sll=39.335964%2C51.694278&sspn=1.140521%2C0.419056&z=12.79',
    'KRASN': 'https://yandex.ru/maps/35/krasnodar/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=39.005474%2C45.044552&sll=38.985679%2C45.066115&sspn=0.417455%2C0.174906&z=13.24',
    'CHELB': 'https://yandex.ru/maps/56/chelyabinsk/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=61.371666%2C55.199665&sll=61.391702%2C55.153365&sspn=0.992881%2C0.336149&z=11.99',
    'NIZNIYNOV': 'https://yandex.ru/maps/47/nizhny-novgorod/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=43.833528%2C56.304645&sll=43.833528%2C56.304645&sspn=0.726832%2C0.238894&z=11.44',
    'SAMARA': 'https://yandex.ru/maps/?display-text=%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5&ll=50.067935%2C53.271916&mode=search&sll=50.061318%2C53.322106&sspn=1.301065%2C0.460575&text=%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5&z=10.6',
    'KAZAN': 'https://yandex.ru/maps/43/kazan/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=49.142959%2C55.810093&sll=49.099982%2C55.767306&sspn=0.986023%2C0.328648&z=12',
    'UFA': 'https://yandex.ru/maps/172/ufa/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=56.027152%2C54.760969&sll=56.037733%2C54.730300&sspn=1.337643%2C0.457684&z=11.56',
    'SARAT': 'https://yandex.ru/maps/194/saratov/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=46.054002%2C51.526239&sll=46.007375%2C51.540864&sspn=0.806470%2C0.297326&z=12.29',
    'YOSH-OLA': 'https://yandex.ru/maps/41/yoshkar-ola/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=47.900161%2C56.629587&sll=47.900161%2C56.629587&sspn=0.234831%2C0.076523&z=13.07',
    'RND': 'https://yandex.ru/maps/39/rostov-na-donu/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=39.653644%2C47.250075&sll=39.653644%2C47.250075&sspn=0.479530%2C0.193044&z=12.04',
    'MSC_SOUTH': 'https://yandex.ru/maps/213/moscow/search/%D0%AE%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.691003%2C55.635770&sctx=ZAAAAAgCEAAaKAoSCYOJP4o610JAEa%2BWnl380ktAEhIJbpayFwit4D8Rqu3%2B5rnNxD8iBgABAgMEBSgKOABAiJ8BSAFqAnJ1nQHNzEw9oAEAqAEAvQHRarSpwgGGAZvEvP8Gu4CpwQSOv7nkBO6AmPATyPeUvtQC08D%2Bi%2BQDkaCwrqMEvpj83AO6sOyanAWyzr29iAL0n8SRrAWgqsqEBObm89CMB7bJroYFl5nQjgWXyozfA4%2Bo5IAE4PLA3AT1h%2FrLqgaCo7qYBe%2FU9OIGoYamiQW%2BoaCBywLana2OBZKs1oUF6gEA8gEA%2BAEAggJe0K7QttC90YvQuSDQsNC00LzQuNC90LjRgdGC0YDQsNGC0LjQstC90YvQuSDQvtC60YDRg9CzINCe0YXRgNCw0L3QvdC%2B0LUg0L%2FRgNC10LTQv9GA0LjRj9GC0LjQtYoCCTE4NDEwNTM3NA%3D%3D&sll=37.691003%2C55.635770&sspn=0.521122%2C0.162581&z=11.92',
    'MSC_SOUTHWESTER': 'https://yandex.ru/maps/213/moscow/search/%D1%8E%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.550650%2C55.622827&sll=37.550650%2C55.622827&sspn=0.711874%2C0.222165&z=11.47',
    'MSC_WEST': 'https://yandex.ru/maps/213/moscow/search/%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D1%8F/?ll=37.231274%2C55.697792&sll=37.231274%2C55.697792&sspn=0.736978%2C0.229558&z=11.42',
    'MSC_NORTHWESTERN': 'https://yandex.ru/maps/213/moscow/search/%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BE-%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.426788%2C55.827373&sll=37.426788%2C55.827373&sspn=0.558525%2C0.173393&z=11.82',
    'MSC_NORTH': 'https://yandex.ru/maps/213/moscow/search/%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.459994%2C55.858690&sll=37.459994%2C55.858690&sspn=0.637145%2C0.197640&z=11.63',
    'MSC_NORTHEASTERN': 'https://yandex.ru/maps/213/moscow/search/%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BE-%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.626618%2C55.870162&sll=37.626618%2C55.870162&sspn=0.562410%2C0.174406&z=11.81',
    'MSC_EAST': 'https://yandex.ru/maps/213/moscow/search/%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.700416%2C55.817776&sll=37.797909%2C55.852814&sspn=1.013744%2C0.314508&z=11.96',
    'MSC_SOUTHEASTERN': 'https://yandex.ru/maps/213/moscow/search/%D0%AE%D0%B3%D0%BE-%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.814196%2C55.699274&sll=37.814196%2C55.699274&sspn=0.489606%2C0.152499&z=12.01',
    'MSC_CENTER': 'https://yandex.ru/maps/213/moscow/search/%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.614006%2C55.753719&sll=37.614006%2C55.753719&sspn=0.279262%2C0.086861&z=12.82',
    'SPB': 'https://yandex.ru/maps/2/saint-petersburg/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=30.304908%2C59.918072&sll=30.304908%2C59.918072&sspn=1.164486%2C0.345675&z=10.76'
}


def get_source_html(town_pairs: dict) -> None:
    """
    Обычное сохранение через driver.page_source почему-то не сохраняет весь исходник, или сохраняет, но без некоторых тегов, используется pyautogui
    """
    with open('proxy\\proxy.txt', encoding='utf8') as file:
        raw_proxy = file.readlines()
    proxies = [prox.strip() for prox in raw_proxy[:-2]]

    i=0
    cit_names = [name for name in town_pairs.keys()]
    while len(os.listdir('source_html\\')) < len(city_comp1.keys()):

        # http/https/socks4-5
        prox_type = proxies[i].split()[1].split(',')[0].lower()
        prox_ip = proxies[i].split()[0]
        chrome_options = webdriver.ChromeOptions()
        # Input here
        # chrome_options.add_argument('--proxy-server={}://{}'.format(prox_type, prox_ip))
        # chrome_options.add_argument(f'user-agent={headers[random.randint(0, len(headers.keys())-1)]}')
        # chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36')
        driver = webdriver.Chrome(executable_path='chromedriver_win32\\chromedriver.exe', seleniumwire_options=proxy_options)
        driver.maximize_window()

        try:  
            for number, city in enumerate(cit_names[6:]):
                number+=6
                print('[INFO] proxy now:', proxies[i])
                driver.get(town_pairs[city])
                # driver.get(url='https://www.reg.ru/web-tools/myip')
                print('[INFO] URL NOW:', town_pairs[city])
                time.sleep(5)
                while True:
                    # find_board_el = driver.find_element_by_class_name('search-list-meta-view__breadcrumbs') # не сохраняет html после
                    if driver.find_elements(by="class name", value='add-business-view'):
                        element = driver.find_element(by='class name', value='search-list-meta-view')
                        ActionChains(driver).move_to_element(element).perform()
                        time.sleep(2)
                        with open(f'source_html\\{city}.html', 'w', encoding='utf8') as f:
                            f.write(driver.page_source)
                        break
                    else:
                        # move to element не сохраняет код html, используем pyautogui
                        pyautogui.moveTo(100, 500)
                        pyautogui.scroll(-500)
                        time.sleep(2)
                        # actions = ActionChains(driver)
                        # actions.move_to_element(find_board_el).perform()
                        # time.sleep(1)
                time.sleep(10)
        except ConnectionRefusedError:
            # Если будет блочить, то на след цикл меняем прокси
            print('Блок')
        except Exception as _ex:
            print(_ex)
            with open(f'source_html\\{city}.html', 'w', encoding='utf8') as f:
                f.write(driver.page_source)
        finally:
            if number < len(cit_names)-1:
                cit_names = cit_names[number:]
            else: break
            driver.close()
            driver.quit()
            i+=1
            continue


def get_url_hrefs(file_path: str) -> STATUS:
    """
    Создаем линки компаний из исходников, котоыре были получены в функции get_source_html
    """
    
    html_files = os.listdir(file_path)
    # read html
    for html_file in html_files:
        print(html_file)
        with open(os.path.join(file_path,html_file), 'r', encoding="utf8") as file:
            raw = file.read()

        # create links
        bs = BeautifulSoup(raw, 'lxml')
        with open(os.path.join('url_links', html_file.split(".")[0]+'.txt'), 'w') as file:  
            for link in bs.find_all('a', {'class':'search-snippet-view__link-overlay'}):
                file.write('https://yandex.ru'+link.get('href')+'reviews'+'\n')

    return '[INFO] Создание и запись ссылок было выполнено'


def get_reviews(file_path: str) -> list:
    """
    Вытягиваем отзывы, имена авторов, дату отзыва, название компании
    """

    with open('proxy\\proxy.txt', encoding='utf8') as file:
        raw_proxy = file.readlines()
    proxies = [prox.strip() for prox in raw_proxy[:-2]]
    # prox_type = proxies_pairs[i].split()[1].split(',')[0].lower()
    # prox_ip = proxies_pairs[i].split()[0]
    href_files = os.listdir(file_path)
    reviews_info = []
    for href in href_files:

        with open(os.path.join(file_path, href), 'r', encoding='utf8') as file:
            urls = [url.strip() for url in file.readlines()]
        
        
        i=0
        city_name = href.split('.')[0]
        pos = 0
        # Вытягиваем данные из файла отдельного города
        for url in urls:

            # Подбираем рабочий проксик
            for idx, proxy in enumerate(proxies[pos:]):
                prox_type = proxy.split()[1].split(',')[0].lower()
                prox_ip = proxy.split()[0]
                pair = {prox_type:prox_ip}
                response = requests.get(url=url, proxies=pair)
                if response.status_code == requests.codes['ok']:
                    print(f'[WARNING] Proxy now: {pair}')
                    pos=idx
                    break
            # response = requests.get(url=url, headers=headers, prox)
            soup = BeautifulSoup(response.text, 'lxml')

            i+=1
            print('[INFO] Прогресс выполнения:', i, f'/ {len(urls)}', url)
            
            try:
                # Нужны названия компаний, отзыв, дата отзыва, человек его оставивший
                company_name = soup.find('h1', class_='orgpage-header-view__header').text.strip()
                reviews = soup.find_all('span', class_='business-review-view__body-text')
                authors = soup.find_all('span', {'itemprop':'name'})
                reviews_dates = soup.find_all('span', class_='business-review-view__date')
                
                reviews = [review.text.strip() for review in reviews] 
                authors = [author.text.strip() for author in authors]
                reviews_dates = [date.text.strip() for date in reviews_dates]
                company_name, city = [company_name] * len(reviews), [city_name] * len(reviews)
                
                if len(reviews) == 0:
                    ('[INFO] Прогресс выполнения:', i, f'/{len(urls)}', url, 'Отзывов нет')
                    continue
                
                for review in zip(company_name, city, authors, reviews_dates, reviews):
                    reviews_info.append([*review])
            except Exception as _ex:
                print(_ex)

            time.sleep(3)
        pd.DataFrame(reviews_info, columns=['Company', 'City', 'Name', 'Date', 'Review']).to_csv(os.path.join('csv_reviews', city_name+'.csv'), index=False)  
        print(f'Переходим на следующий регион. Текущий город был {city_name}')
        time.sleep(10)        
    pd.DataFrame(reviews_info, columns=['Company', 'City', 'Name', 'Date', 'Review']).to_csv('ALL_REVIEW.csv', index=False)       

    return f'[INFO] Были обработаны следующие файлы: {", ".join(href_files)}!'


def main():
    # get_source_html(city_comp1)
    # print(get_url_hrefs('source_html\\'))
    get_reviews('url_links\\')

if __name__ == '__main__':
    main()