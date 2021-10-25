from parse_proxy import get_proxy
from requests_testadapter import Resp
import requests
import os
from bs4 import BeautifulSoup
import lxml

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)



def get_proxys():
    requests_session = requests.session()
    requests_session.mount('file://', LocalFileAdapter())
    response = requests_session.get(url='file://resp_text.html')
    soup = BeautifulSoup(response.text, 'lxml')
    elements = soup.find_all('tr')
    list_proxys = []
    for external_td in elements:
        internal_elements = external_td.find_all('td')
        proxy = []
        for el in internal_elements:
            try:
                if int(internal_elements[3].text[:-3]) > 300:
                    continue
                proxy.append(el.text)
            except ValueError:
                continue
            
        list_proxys.append(proxy)
    
    with open('prox.txt', 'w', encoding='utf8') as file:
        [file.write(','.join([x for x in elements])) for elements in list_proxys]
    # return list_proxys
    # return elements

get_proxys()