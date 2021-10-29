from bs4 import BeautifulSoup
import lxml
import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver as wd
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
import pyautogui
import pyperclip
from random import randint
# import sys

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

DELAY = 10


def get_source_html(city_dict: dict) -> None:
    
    login = 'dnxfuf'
    password = '24lhnBJG9a'
    proxy_options = {
        'proxy': {
            'https': f'http://{login}:{password}@193.57.136.78:24531'
        },
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    
    driver = webdriver.Chrome(executable_path='chromedriver_win32\\chromedriver.exe', seleniumwire_options=proxy_options)
    driver.maximize_window()
    cit_names = [city for city in city_dict.keys()]

    
    for number, city in enumerate(cit_names):
            
        driver.get(city_dict[city])
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x3AX1-LfntMc-header-title-ij8cu')))
        print(f'[INFO] PROGRESS {number}/{len(cit_names)-1}. CURRENT CITY: {city}')

        while True:
            for _ in range(8):
                # Роллим вниз, цепляться за элемент мы не можем, так как у гугла другие формы. 
                # pyautogui.moveTo(randint(75, 127), randint(413, 513))
                pyautogui.scroll(-500)
                time.sleep(1)

            element = driver.find_element(by='xpath', value='//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')
            try:
                element.click()
                # Получение ссылок
                with open(f'google_data\\hrefs\\{city}.txt', 'a', encoding='utf8') as file:
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    for url in soup.find_all('a', class_='a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd'):
                        file.write(url['href']+'\n')
            except WebDriverException:
                # Проверка, если клавиша следующей страницы не будет доступна
                print('Страницы закончились')
                break

            time.sleep(10)
    print(f'Были обработаны следующие города {", ".join(cit_names)}')


def get_full_review_link(file_path:str):
    
    login = 'dnxfuf'
    password = '24lhnBJG9a'
    proxy_options = {
        'proxy': {
            'https': f'http://{login}:{password}@193.57.136.78:24531'
        },
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }

    driver = webdriver.Chrome(executable_path='chromedriver_win32\\chromedriver.exe', seleniumwire_options=proxy_options)
    files = os.listdir(file_path)
    for file in files[13:]:
        short_data = []
        city = file.split('.')[0]
        with open(f'{os.path.join(file_path, file)}', encoding='utf8') as file:
            urls = [url.strip() for url in file.readlines()]
        
        for url in tqdm(urls):
            try:
                # print(url)
                driver.get(url)
                driver.maximize_window()
                WebDriverWait(driver, 10)
                _ = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'x3AX1-LfntMc-header-title-ij8cu')))
                soup = BeautifulSoup(driver.page_source, 'lxml')
                time.sleep(3)
                pyautogui.hotkey('ctrl', 'shift', 'j')              
                # pyautogui.moveTo(x=1620, y=242)
                # time.sleep(0.2)
                # pyautogui.click()
                # time.sleep(0.7)
                pyautogui.moveTo(x=1280, y=270)
                time.sleep(1)
                pyautogui.click()
                reviews_url_button = driver.find_element(by='xpath', value='//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button')
                numb_reviews = int(reviews_url_button.text.split(' ')[0])
                reviews_url_button.click()
                WebDriverWait(driver, 10)
                # Сделать пока не загрузится элемент
                # Двигаться должны по процентам, именить на абс
                clicks = [(1620, 242), (1308, 560), (1548, 529), (1646, 631), (1656, 642)]
                click_types = ['left', 'left', 'left', 'right', 'left']

                for j in range(len(clicks)):
                    pyautogui.moveTo(*clicks[j])
                    pyautogui.click(button=click_types[j])
                    time.sleep(2)

                    if (1620, 242) == clicks[j]:
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(1.5)
                        pyautogui.press('backspace')
                        time.sleep(2)
                        pyautogui.press([x for x in 'listen'])
                        time.sleep(2)

                request_from_google = pyperclip.paste()
                print(request_from_google)
                reviews_url = driver.current_url

            except TimeoutException:
                print(f'Loading take to much time. URL: {url} skipped')
            except NoSuchElementException:
                # Клавиши отзывов нет
                print('Отзывов нет')
                numb_reviews = 0
                reviews_url = False
                request_from_google = False
            except Exception as _ex:
                print(_ex)
            finally:
                pyautogui.hotkey('ctrl', 'shift', 'j')
                if soup.find('h1'):
                    company_name = soup.find('h1').find('span').text
                else:
                    company_name = 'Сайт не загрузился'
                print(company_name)
                if soup.find('button', {'data-item-id':"address"}):
                    address = soup.find('button', {'data-item-id':"address"})['aria-label']
                else: address = 'Не указан'

                if soup.find('button', {'data-tooltip':'Перейти на сайт'}):
                    link = soup.find('button', {'data-tooltip':'Перейти на сайт'})['aria-label']
                else: link = 'Не указан'

                if soup.find('button', {'data-tooltip':'Скопировать номер'}):
                    phone = soup.find('button', {'data-tooltip':'Скопировать номер'})['aria-label']
                else: phone = 'Не указан'
                
                short_data.append([city, company_name, address, link, phone, numb_reviews, url, reviews_url, request_from_google])
        pd.DataFrame(short_data, columns=['City', 'Company', 'Address', 'Site', 'Phone', 'Count of reviews', 'Main URL', 'Reviews url', 'JSON ANS']).to_csv(os.path.join(f'google_data\\company_info\\{city}.csv'), index=False)
        print('2 минуты отдыхаем')
        # driver.close()
        # driver.quit()
        time.sleep(120)

def main():
    get_full_review_link('google_data\\hrefs\\')

if __name__ == '__main__':
    main()