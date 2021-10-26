from aiohttp.client import request
import requests
from bs4 import BeautifulSoup
import lxml
from requests.api import head

url = 'https://www.google.com/maps/place/%D0%93%D0%9A+%D0%9B%D0%B5%D0%B3%D0%B8%D1%81/@55.7586456,37.4926319,11z/data=!4m9!1m2!2m1!1z0LzQvtGB0LrQstCwINC-0YXRgNCw0L3QvdC-0LUg0L_RgNC10LTQv9GA0LjRj9GC0LjQtQ!3m5!1s0x46b54a5ef2252ad9:0xb1bbb9281de1572b!8m2!3d55.7586456!4d37.6327076!15sCjTQvNC-0YHQutCy0LAg0L7RhdGA0LDQvdC90L7QtSDQv9GA0LXQtNC_0YDQuNGP0YLQuNC1WjYiNNC80L7RgdC60LLQsCDQvtGF0YDQsNC90L3QvtC1INC_0YDQtdC00L_RgNC40Y_RgtC40LWSARZzZWN1cml0eV9ndWFyZF9zZXJ2aWNlmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU5uYm1JelIwNW5FQUU!5m1!1e1?hl=ru-RU'
headers = {
       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebt/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36' 
    }

response = requests.get(url, headers=headers)
# print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
address = soup.find_all('div', class_='siAUzd-neVct')
print(address)
with open('smth.html', 'w', encoding='utf8') as file:
    file.write(response.text)


# 103.85.233.38:1080 SOCKS4