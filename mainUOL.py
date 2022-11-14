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
            pkPortalCru = next(_pkPortal)
            pkPortal = f'id_pk={pkPortalCru}'
            nomeSessao = linksMenuNoticias.select_one('.custom-title').get_text()
            linkSessao = linksMenuNoticias.a.get('href')
            print(pkPortal)
            print(linkSessao)
            dbPortal.atualizarColuna('dt_hr_pesquisa', pkPortal, dataHora)
            dbPortal.atualizarColuna('nome_sessao', pkPortal, nomeSessao)
            dbPortal.atualizarColuna('link_site', pkPortal, linkSessao)
            resposta = requests.get(linkSessao)
            html = BeautifulSoup(resposta.text, 'html.parser')
            for linksMaterias in html.select('.thumbnails-item.align-horizontal'):
                linkMateria = linksMaterias.a.get('href')
                resposta = requests.get(linkMateria)
                html = BeautifulSoup(resposta.text, 'html.parser')
                for dadosMateria in html.select('.container.article'):
                    pkNoticias = f'id_pk={next(_pkNoticias)}'
                    tituloMateria = dadosMateria.select_one('.custom-title').get_text().replace("'", '"')
                    dataMateria = dadosMateria.select_one('.p-author.time').get_text().replace('h', ':').strip()[:16]
                    dataMateria = datetime.strptime(dataMateria, '%d/%m/%Y %H:%M')
                    textoMateria = ''
                    for textoCru in dadosMateria.select_one('.text').find_all('p'):
                        textoMateria += textoCru.get_text(' | ', strip=True).replace("'", '"')
                    dbMaterias.atualizarColuna('referencia_site', pkNoticias, pkPortalCru)
                    dbMaterias.atualizarColuna('dt_materia', pkNoticias, dataMateria)
                    dbMaterias.atualizarColuna('link_materia', pkNoticias, linkMateria)
                    dbMaterias.atualizarColuna('titulo_materia', pkNoticias, tituloMateria)
                    dbMaterias.atualizarColuna('texto_materia', pkNoticias, textoMateria)
        except (AttributeError, TypeError, Exception):
            pass
    dbPortal.fecharConexao()
    dbMaterias.fecharConexao()
    dbLog.fecharConexao()


coreUOL()
