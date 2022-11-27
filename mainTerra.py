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
        for linkMenu in html.find_all('li', {'class':'app-t360-table__header__menu__item'}):
            link = linkMenu.a.get('href').strip()
            nomeSessao: str = linkMenu.get_text().strip()
            print(link)
            print(nomeSessao)
            resposta = requests.get(link)
            html = BeautifulSoup(resposta.text, 'html.parser')
            for noticia in html.find_all('div', {'class':'card-news__text'}):
                linkNoticia = noticia.h2.a.get('href')
                resposta = requests.get(linkNoticia)
                html = BeautifulSoup(resposta.text, 'html.parser')
                if 'poder360' in str(linkNoticia):
                    print(linkNoticia)
                    print('Sem Conteudo ainda')
                elif 'cartacapital' in str(linkNoticia):
                    print(linkNoticia)
                    print('Sem Conteudo ainda')
                elif 'terra.com' in str(linkNoticia):
                    conteudoPagina = html.find_all('article', {'class':'article'})
                    print(100 * '#')
                    print(linkNoticia)
                    print(conteudoPagina)
                    print(100 * '#')
                else:
                    print(linkNoticia)
                    print('Conteudo externo')
            print(100 * '*')
    except (AttributeError, TypeError, Exception) as e:
        registradorErros(e.__class__.__name__, str(e).replace("'", '"'), 'coreTerra')


coreTerra()
