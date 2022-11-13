from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def coreUOL():
    url = 'https://noticias.uol.com.br/'
    resposta = requests.get(url)
    html = BeautifulSoup(resposta.text, 'html.parser')
    
    for linksMenuNoticias in html.select('.heading-style'):
        try:
            # print(linksMenuNoticias)
            nomeSessao = linksMenuNoticias.select_one('.custom-title').get_text()
            link = linksMenuNoticias.a.get('href')
            resposta = requests.get(link)
            html = BeautifulSoup(resposta.text, 'html.parser')
            print(nomeSessao)
            # print(link)
            for linkMaterias in html.select('.thumbnails-item.align-horizontal'):
                link = linkMaterias.a.get('href')
                resposta = requests.get(link)
                html = BeautifulSoup(resposta.text, 'html.parser')
                # print(link)
                for dadosMaterias in html.select('.container.article'):
                    tituloMateria = dadosMaterias.select_one('.custom-title').get_text()
                    dataMateria = dadosMaterias.select_one('.p-author.time').get_text().replace('h', ':').strip()[:16]
                    dataMateria = datetime.strptime(dataMateria, '%d/%m/%Y %H:%M')
                    
                    print(dataMateria)
                    print(tituloMateria)
        except (AttributeError, TypeError):
            pass
        print(100 * '*')
        


coreUOL()
