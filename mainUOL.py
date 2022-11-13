from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def coreUOL():
    dbLog = OperacoesTabelasBD('"Core_logservicos"')
    dbPortal = OperacoesTabelasBD('portalUOL')
    dbMaterias = OperacoesTabelasBD('materiasportalUOL')
    dataHora: str = str(datetime.now())
    dbLog.inserirColunas((dataHora, 'UOL'), coluna='(dt_hr_exec_func, func_portal)')

    url = 'https://noticias.uol.com.br/'
    resposta = requests.get(url)
    html = BeautifulSoup(resposta.text, 'html.parser')
    
    _pkPortal = count(0)
    _pkNoticias = count(0)
    for linksMenuNoticias in html.select('.heading-style'):
        try:
            pkPortal = next(_pkPortal)
            nomeSessao = linksMenuNoticias.select_one('.custom-title').get_text()
            linkSessao = linksMenuNoticias.a.get('href')
            print(pkPortal)
            print(linkSessao)
            dbPortal.inserirColunas(f'({pkPortal})', coluna='(id_pk)')
            print(100 * '#')
            # print(nomeSessao)
            resposta = requests.get(linkSessao)
            html = BeautifulSoup(resposta.text, 'html.parser')
            for linksMaterias in html.select('.thumbnails-item.align-horizontal'):
                linkMateria = linksMaterias.a.get('href')
                resposta = requests.get(linkMateria)
                html = BeautifulSoup(resposta.text, 'html.parser')
                print(linkMateria)
                for dadosMateria in html.select('.container.article'):
                    pkNoticias = next(_pkNoticias)
                    dbMaterias.inserirColunas(f'({pkNoticias})', coluna='(id_pk)')
                    # dbMaterias.inserirColunas(pkPortal, coluna=)
                    print(pkNoticias)
                    print(100 * '*')
                    tituloMateria = dadosMateria.select_one('.custom-title').get_text()
                    dataMateria = dadosMateria.select_one('.p-author.time').get_text().replace('h', ':').strip()[:16]
                    dataMateria = datetime.strptime(dataMateria, '%d/%m/%Y %H:%M')
                    textoMateria = ''
                    for textoCru in dadosMateria.select_one('.text').find_all('p'):
                        textoMateria += textoCru.get_text(' | ', strip=True)
                    # print(dataMateria)
                    # print(tituloMateria)
                    # print(textoMateria)
        except (AttributeError, TypeError, Exception):
            pass
    dbPortal.fecharConexao()
    dbMaterias.fecharConexao()
    dbLog.fecharConexao()


coreUOL()
