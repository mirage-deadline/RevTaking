from bs4 import BeautifulSoup
import requests
import re
import lxml
import pandas as pd
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire import webdriver
import pyautogui
from random import randint
import os

cities = {
    'RND' : 'https://www.google.com/maps/search/%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2-%D0%BD%D0%B0-%D0%94%D0%BE%D0%BD%D1%83,+%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@47.2613873,39.3485092,10z/data=!5m1!1e1?hl=ru-RU',
    'VOLG': 'https://www.google.com/maps/search/%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@48.6613438,44.3903791,11z/data=!5m1!1e1?hl=ru-RU',
    'VORON': 'https://www.google.com/maps/search/%D0%92%D0%BE%D1%80%D0%BE%D0%BD%D0%B5%D0%B6+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@51.6822776,39.1306,12z/data=!5m1!1e1?hl=ru-RU',
    'KRASN': 'https://www.google.com/maps/search/%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@45.0536923,38.7365652,10z/data=!5m1!1e1?hl=ru-RU',
    'EKT': 'https://www.google.com/maps/search/%D0%B5%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@56.8446374,60.4605029,11z/data=!5m1!1e1?hl=ru-RU',
    'CHELB': 'https://www.google.com/maps/search/%D0%A7%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@55.1759169,61.2102545,11z/data=!5m1!1e1?hl=ru-RU',
    'NIN': 'https://www.google.com/maps/search/%D0%BD%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9+%D0%BD%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@56.2964183,43.8153948,11z/data=!3m1!4b1!5m1!1e1?hl=ru-RU',
    'SAMARA': 'https://www.google.com/maps/search/%D1%81%D0%B0%D0%BC%D0%B0%D1%80%D0%B0+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@53.2194884,50.0398245,11z/data=!3m1!4b1!5m1!1e1?hl=ru-RU',
    'KZN': 'https://www.google.com/maps/search/%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@55.8167648,49.0140383,11z/data=!3m1!4b1!5m1!1e1?hl=ru-RU',
    'UFA': 'https://www.google.com/maps/search/%D0%A3%D1%84%D0%B0+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@54.7621763,55.6951711,10z/data=!5m1!1e1?hl=ru-RU',
    'SARAT': 'https://www.google.com/maps/search/%D0%A1%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@51.5451723,45.9026372,11z/data=!5m1!1e1?hl=ru-RU',
    'YO-OLA': 'https://www.google.com/maps/search/%D0%99%D0%BE%D1%88%D0%BA%D0%B0%D1%80-%D0%9E%D0%BB%D0%B0+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@56.6368966,47.8365435,12z/data=!5m1!1e1?hl=ru-RU',
    'MSC': 'https://www.google.com/maps/search/%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@55.6485501,37.5418106,11z/data=!5m1!1e1?hl=ru-RU',
    'SPB': 'https://www.google.com/maps/search/%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/@59.9170516,30.2683084,12z/data=!5m1!1e1?hl=ru-RU',
}

test = {
    'DZA': 'https://www.google.com/maps/search/%D0%B4%D0%B6%D0%B0%D0%BD%D0%BA%D0%BE%D0%B9+%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5+%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D1%8F/@45.0212787,32.947435,8.25z/data=!5m1!1e1?hl=ru-RU'
}


def get_source_html(city_dict: dict) -> None:
    
    login = '1'
    password = '1'
    proxy_options = {
        'proxy': {
            'https': f'1'
        },
        'user-agent': '1'
    }
    driver = webdriver.Chrome(executable_path='chromedriver_win32\\chromedriver.exe', seleniumwire_options=proxy_options)
    driver.maximize_window()
    cit_names = [city for city in city_dict.keys()]

    
    for number, city in enumerate(cit_names):
            
        driver.get(city_dict[city])
        time.sleep(5)
        print(f'[INFO] PROGRESS {number}/{len(cit_names)}. CURRENT CITY: {city}')

        while True:
            for j in range(7):
                # Роллим вниз, цепляться за элемент мы не можем, так как у гугла другие формы. 
                pyautogui.moveTo(randint(75, 127), randint(413, 513))
                pyautogui.scroll(-500)
                time.sleep(1)
            element = driver.find_element(by='xpath', value='//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')
            try:
                element.click()
                with open(f'google_data\\source_html\\{city}.html', 'a', encoding='utf8') as file:
                    file.write(driver.page_source)
            except WebDriverException:
                # Проверка, если клавиша следующей страницы не будет доступна
                print('Страницы закончились')
                break

            time.sleep(10)
    print(f'Были обработаны следующие города {", ".join(cit_names)}')

def get_hrefs(file_path: str) -> None:
    
    for file in os.listdir(file_path):
        city = file.split('.')[0]
        with open(os.path.join(file_path, file), 'r', encoding='utf8') as file:
            raw = file.read()
        with open('test.txt', 'w', encoding='utf8') as f:
            f.write(raw)
        # a = re.findall(r'href= \d (.*) class=\d', raw)
        # print(a)   
        # soup = BeautifulSoup(raw, 'lxml')
        # print(len(soup.find_all('a', class_ = 'a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd')))
        # path_to_save = 'google_data\\' + 'hrefs\\'
        # with open(os.path.join(path_to_save, f'{city}.txt'), 'w', encoding='utf8') as file:
        #     for link in soup.find_all('a', class_ = 'a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd'):
        #         file.write(link['href']+'\n')
        #     print(f'Были обработаны ссылки по городу {city}')

def main():
    # get_source_html(cities)
    get_hrefs(file_path='google_data\\source_html')

if __name__ == '__main__':
    main()