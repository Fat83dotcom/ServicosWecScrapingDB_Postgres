from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def coreG1():
    dbLog = OperacoesTabelasBD('"Core_logservicos"')
    dbPortal = OperacoesTabelasBD('portalG1')
    dbMaterias = OperacoesTabelasBD('materiasportalG1')
    dataHora: str = str(datetime.now())
    dbLog.inserirColunas((dataHora, 'G1'), coluna='(dt_hr_exec_func, func_portal)')

    url = 'https://g1.globo.com/'
    resposta = requests.get(url)
    html = BeautifulSoup(resposta.text, 'html.parser')

    _pkPortal = count(0)
    _pkNoticias = count(0)
    for linkMateria in html.select('.menu-item-link'):
        links = linkMateria.get('href')
        if links is not None and (links.count('/') == 4):
            nomeSessao = linkMateria.select_one('.menu-item-title').get_text().title()
            resposta = requests.get(links)
            html = BeautifulSoup(resposta.text, 'html.parser')
            pkPortal = next(_pkPortal)
            dbPortal.atualizarColuna('dt_hr_pesquisa', f'id_pk={pkPortal}', dataHora)
            dbPortal.atualizarColuna('nome_sessao', f'id_pk={pkPortal}', nomeSessao)
            dbPortal.atualizarColuna('link_site', f'id_pk={pkPortal}', links)


            # print(100*'*')
            # print(pk)
            # # dbPortal.inserirColunas(f'({next(_pkPortal)})', coluna='(id_pk)')
            # print(nomeSessao)
            # print(links)
            # print(100*'*')

            for dadosMateria in html.select('.feed-post-link'):
                linkMateria = dadosMateria.get('href')
                if linkMateria is not None:
                    try:
                        resposta = requests.get(linkMateria)
                        html = BeautifulSoup(resposta.text, 'html.parser')
                        for materia in html.select('.mc-body'):
                            pkNoticias = f'id_pk={next(_pkNoticias)}'
                            
                            # print(next(_pkNoticias))
                            # dbMaterias.inserirColunas(f'({next(_pkNoticias)})', coluna='(id_pk)')
                            tituloMateria = materia.select_one('.title').meta.get('content')
                            dataMateria = materia.select_one(
                                '.content-publication-data__updated').time.get('datetime')
                            textoMateria = materia.find_all('p', class_='content-text__container')
                            dbMaterias.atualizarColuna('referencia_site', pkNoticias, pkPortal)
                            dbMaterias.atualizarColuna('dt_materia', pkNoticias, dataMateria)
                            dbMaterias.atualizarColuna('link_materia', pkNoticias, linkMateria)
                            dbMaterias.atualizarColuna('titulo_materia', pkNoticias, tituloMateria)
                    
                            # print(tituloMateria)
                            # print(dataMateria)
                            # print(textoMateria)
                            
                            palavras = ''
                            for palavra in textoMateria:
                                palavras += f'{str(palavra)} \n'
                            dbMaterias.atualizarColuna('texto_materia', pkNoticias, palavras)
                            # print(palavras)
                            # print(100*'#')
                    except Exception as erro:
                        print(erro)
    dbPortal.fecharConexao()
    dbMaterias.fecharConexao()
    dbLog.fecharConexao()


coreG1()
