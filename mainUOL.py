from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def coreUOL():
    url = 'https://noticias.uol.com.br/'
    resposta = requests.get(url)
    html = BeautifulSoup(resposta.text, 'html.parser')
    
    _pkPortal = count(0)
    _pkNoticias = count(0)
    for linksMenuNoticias in html.select('.heading-style'):
        try:
            nomeSessao = linksMenuNoticias.select_one('.custom-title').get_text()
            linkSessao = linksMenuNoticias.a.get('href')
            resposta = requests.get(linkSessao)
            html = BeautifulSoup(resposta.text, 'html.parser')
            print(nomeSessao)
            # print(link)
            for linksMaterias in html.select('.thumbnails-item.align-horizontal'):
                linkMateria = linksMaterias.a.get('href')
                resposta = requests.get(linkMateria)
                html = BeautifulSoup(resposta.text, 'html.parser')
                # print(link)
                for dadosMateria in html.select('.container.article'):
                    tituloMateria = dadosMateria.select_one('.custom-title').get_text()
                    dataMateria = dadosMateria.select_one('.p-author.time').get_text().replace('h', ':').strip()[:16]
                    dataMateria = datetime.strptime(dataMateria, '%d/%m/%Y %H:%M')
                    textoMateria = ''
                    for textoCru in dadosMateria.select_one('.text').find_all('p'):
                        textoMateria += textoCru.get_text(' | ', strip=True)
                    print(dataMateria)
                    print(tituloMateria)
                    print(textoMateria)
        except (AttributeError, TypeError):
            pass
        


coreUOL()
