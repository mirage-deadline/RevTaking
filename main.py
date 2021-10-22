from bs4 import BeautifulSoup
import lxml
import os
import pandas as pd
import pyautogui
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

STATUS = str

city_comp1 = {}

headers = {
}

def get_source_html(town_pairs: dict) -> None:
    """
    Обычное сохранение через driver.page_source почему-то не сохраняет весь исходник, или сохраняет, но без некоторых тегов, используется pyautogui
    """
    driver = webdriver.Chrome(executable_path='C:\\Users\\Dmitry\\Downloads\\chromedriver_win32\\chromedriver.exe')
    driver.maximize_window()
    for city in town_pairs.keys():
        try:        
            driver.get(town_pairs[city])
            time.sleep(3)
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
        except Exception as _ex:
            print(_ex)
        finally:
            driver.close()
            driver.quit()


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
    href_files = os.listdir(file_path)
    reviews_info = []
    for href in href_files:

        with open(os.path.join(file_path, href), 'r', encoding='utf8') as file:
            urls = [url.strip() for url in file.readlines()]
        
        
        i=0
        city_name = href.split('.')[0]
        for url in urls:
            
            response = requests.get(url=url, headers=headers)
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
        print('Переходим на следующий регион. Текущий регион был')
        time.sleep(10)        
    pd.DataFrame(reviews_info, columns=['Company', 'City', 'Name', 'Date', 'Review']).to_csv('ALL_REVIEW.csv', index=False)       

    return f'[INFO] Были обработаны следующие файлы: {", ".join(href_files)}!'


def main():
    get_source_html(city_comp1)
    print(get_url_hrefs('source_html\\'))
    get_reviews('url_links\\')

if __name__ == '__main__':
    main()