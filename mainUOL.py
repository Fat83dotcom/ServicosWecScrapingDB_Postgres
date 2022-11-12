from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def coreUOL():
    url = 'https://www.uol.com.br/'
    resposta = requests.get(url)
    html = BeautifulSoup(resposta.text, 'html.parser')
    
    for linksMenuPrincipal in html.select('.menuDesktop__item'):
        nomeSessao = linksMenuPrincipal.select_one('.menuDesktop__link__title').get_text().title()
        link = linksMenuPrincipal.a.get('href')
        print(nomeSessao)
        print(link)


coreUOL()
