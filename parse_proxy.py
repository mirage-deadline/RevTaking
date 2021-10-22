from bs4 import BeautifulSoup
import requests
import lxml

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

def get_proxy(url: str) -> None:
    r = requests.Session()
    response = r.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    proxy_ips = soup.find_all('tr')
    with open("resp_text.html", "w", encoding='utf8') as file:
        file.write(response.text)
    return proxy_ips



print(get_proxy(url='https://hidemy.name/ru/proxy-list/#list'))