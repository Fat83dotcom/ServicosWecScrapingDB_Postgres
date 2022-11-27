from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count
from funcao_registradora_de_erros import registradorErros

# https://www.terra.com.br/noticias/ 

def coreTerra():
    try:
        url = 'https://www.terra.com.br/noticias/'
        resposta = requests.get(url)
        html = BeautifulSoup(resposta.text, 'html.parser')
        for links in html.select('.app-t360-table__header__menu'):
            link = links.a.get('href')
            nomeSessao = links.select_one('.app-t360-table__header__menu__item').get_text()
            print(link)
            print(nomeSessao)
    except (AttributeError, TypeError, Exception) as e:
        registradorErros(e.__class__.__name__, str(e).replace("'", '"'), 'coreTerra')


coreTerra()
