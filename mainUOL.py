from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def registradorErros(func_name, classe_erro, desc_erro):
    try:
        dataHora: str = str(datetime.now())
        dbLogErro = OperacoesTabelasBD('log_erro')
        dbLogErro.inserirColunas(f"('{dataHora}', '{classe_erro}', '{desc_erro}', '{func_name}')", \
            coluna='(dt_hr_erro, classe_erro, descricao_erro, nome_funcao_origem)')
    except Exception as e:
        with open(f'logs/log_erro_{dataHora}.txt', 'w') as arquivo:
            erro = f'{str(e.__class__.__name__)}, {str(e)}'
            arquivo.write(erro)


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
                    
                    dbPortal.atualizarColuna('dt_hr_pesquisa', pkPortal, dataHora)
                    dbPortal.atualizarColuna('nome_sessao', pkPortal, nomeSessao)
                    dbPortal.atualizarColuna('link_site', pkPortal, linkSessao)
                    dbMaterias.atualizarColuna('referencia_site', pkNoticias, pkPortalCru)
                    dbMaterias.atualizarColuna('dt_materia', pkNoticias, dataMateria)
                    dbMaterias.atualizarColuna('link_materia', pkNoticias, linkMateria)
                    dbMaterias.atualizarColuna('titulo_materia', pkNoticias, tituloMateria)
                    dbMaterias.atualizarColuna('texto_materia', pkNoticias, textoMateria)
        except (AttributeError, TypeError, Exception) as e:
            registradorErros('coreUOL', e.__class__.__name__, str(e).replace("'", '"'))
    dbPortal.fecharConexao()
    dbMaterias.fecharConexao()
    dbLog.fecharConexao()


coreUOL()
