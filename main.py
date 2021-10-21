from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
import time
from win32con import *
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

city_comp = {
    'ekt': ['https://yandex.ru/maps/54/yekaterinburg/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=60.868184%2C56.843386&sctx=ZAAAAAgBEAAaKAoSCZjArbt5TE5AERlYx%2FFDa0xAEhIJZAJ%2BjSTB5T8Ry%2FRLxFvn2D8iBgABAgMEBSgKOABAmldIAWoCcnWdAc3MTD2gAQCoAQC9AR%2BF2J7CAYEBj%2FbovgaxsPCsrgOOqcTTBMXYhPYEmb7F2wSDv8eABOWs6vgD45Hy4gPXruuVBN2W5%2FgDxMHm%2FJ4GxuP3xocEiY3DlATkvrqllgTAiYG9BM7wzOkFr7qXjwez8pr8BI%2BY9d8D7LLdpwT4k5rfBaPCqp8Eq9WvmASP6am3BJWHk%2FkF6gEA8gEA%2BAEAggIn0J7RhdGA0LDQvdC90L7QtSDQv9GA0LXQtNC%2F0YDQuNGP0YLQuNC1igIJMTg0MTA1Mzc0&sll=60.868184%2C56.843386&sspn=1.301065%2C0.421560&z=10.6', 150],
    'msc_all': ['https://yandex.ru/maps/213/moscow/search/%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.646930%2C55.725146&sll=37.646930%2C55.725146&sspn=1.394447%2C0.465284&z=10.5', 1500],
    'msc_south': ['https://yandex.ru/maps/213/moscow/search/%D0%AE%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%9E%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.691003%2C55.635770&sctx=ZAAAAAgCEAAaKAoSCYOJP4o610JAEa%2BWnl380ktAEhIJbpayFwit4D8Rqu3%2B5rnNxD8iBgABAgMEBSgKOABAiJ8BSAFqAnJ1nQHNzEw9oAEAqAEAvQHRarSpwgGGAZvEvP8Gu4CpwQSOv7nkBO6AmPATyPeUvtQC08D%2Bi%2BQDkaCwrqMEvpj83AO6sOyanAWyzr29iAL0n8SRrAWgqsqEBObm89CMB7bJroYFl5nQjgWXyozfA4%2Bo5IAE4PLA3AT1h%2FrLqgaCo7qYBe%2FU9OIGoYamiQW%2BoaCBywLana2OBZKs1oUF6gEA8gEA%2BAEAggJe0K7QttC90YvQuSDQsNC00LzQuNC90LjRgdGC0YDQsNGC0LjQstC90YvQuSDQvtC60YDRg9CzINCe0YXRgNCw0L3QvdC%2B0LUg0L%2FRgNC10LTQv9GA0LjRj9GC0LjQtYoCCTE4NDEwNTM3NA%3D%3D&sll=37.691003%2C55.635770&sspn=0.521122%2C0.162581&z=11.92', 150],
    'msc_southwestern': ['https://yandex.ru/maps/213/moscow/search/%D1%8E%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.550650%2C55.622827&sll=37.550650%2C55.622827&sspn=0.711874%2C0.222165&z=11.47',300],
    'msc_west': ['https://yandex.ru/maps/213/moscow/search/%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D1%8F/?ll=37.231274%2C55.697792&sll=37.231274%2C55.697792&sspn=0.736978%2C0.229558&z=11.42', 500],
    'msc_northwestern': ['https://yandex.ru/maps/213/moscow/search/%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BE-%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.426788%2C55.827373&sll=37.426788%2C55.827373&sspn=0.558525%2C0.173393&z=11.82', 500],
    'msc_north': ['https://yandex.ru/maps/213/moscow/search/%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.459994%2C55.858690&sll=37.459994%2C55.858690&sspn=0.637145%2C0.197640&z=11.63', 500],
    'msc_northestern': ['https://yandex.ru/maps/213/moscow/search/%D0%A1%D0%B5%D0%B2%D0%B5%D1%80%D0%BE-%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.626618%2C55.870162&sll=37.626618%2C55.870162&sspn=0.562410%2C0.174406&z=11.81', 500],
    'msc_east': ['https://yandex.ru/maps/213/moscow/search/%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.700416%2C55.817776&sll=37.797909%2C55.852814&sspn=1.013744%2C0.314508&z=11.96',500],
    'msc_southeastern': ['https://yandex.ru/maps/213/moscow/search/%D0%AE%D0%B3%D0%BE-%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.814196%2C55.699274&sll=37.814196%2C55.699274&sspn=0.489606%2C0.152499&z=12.01', 500],
    'msc_center': ['https://yandex.ru/maps/213/moscow/search/%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%BA%D1%80%D1%83%D0%B3%20%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D0%B5/?ll=37.614006%2C55.753719&sll=37.614006%2C55.753719&sspn=0.279262%2C0.086861&z=12.82', 500],
}

def crap(city: dict, town_name:str) -> None:
    '''
    Из-за того, что скролл страницы не подходит в текущем случае, так как есть блок отвечающий за прокрутку, то используется 
    способ либы pyautogui, прокручивая страницу вниз в необходимом месте, после чего полностью подгруженная страница html сохраняется локально, без сохранения
    подгрузить исходник не выйдет, так как апдейт не проходит и отображаются блоки первых 6 элементов
     '''

    driver = webdriver.Chrome(executable_path='C:\\Users\\Dmitry\\Downloads\\chromedriver_win32\\chromedriver.exe')

    driver.get(city[town_name][0])
    driver.maximize_window()

    pyautogui.moveTo(100, 500)
    time.sleep(2)
    for _ in range(city[town_name][1]):
        pyautogui.scroll(-500)
    pyautogui.moveTo(380, 1025)
    pyautogui.click()
    SEQUENCE = town_name

    #Сохраняем полученный html
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.typewrite(SEQUENCE + '.html')
    time.sleep(1)
    pyautogui.press('enter')
    # Время можно поставить меньше, зависит от скорости загрузки
    time.sleep(360)



def get_links():

    with open('C:\\Users\\Dmitry\\Downloads\\msc.html', 'r', encoding="utf8") as file:
        raw = file.read()
    bs = BeautifulSoup(raw, 'lxml')
    links = []
    for link in bs.find_all('a', {'class':'search-snippet-view__link-overlay'}):
        print(link['href'])
        with open('msc.txt', 'a') as f:
            f.write(str(link['href'])+'\n')
        links.append(link)
    return len(links)

crap(city_comp, 'msc_south')
# print(get_links())