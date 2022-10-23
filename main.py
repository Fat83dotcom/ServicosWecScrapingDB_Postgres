from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count


def coreCnn():
    dbLog = OperacoesTabelasBD('Core_logservicos')
    dbPortal = OperacoesTabelasBD('portalcnn')
    dbMaterias = OperacoesTabelasBD('materiasportal')
    dataHora: str = str(datetime.now())
    dbLog.inserirColunas((dataHora, 'CNN'), coluna='(dt_hr_exec_func, func_portal)')
    url = [
        'https://www.cnnbrasil.com.br/politica/',
        'https://www.cnnbrasil.com.br/nacional/',
        'https://www.cnnbrasil.com.br/business/',
        'https://www.cnnbrasil.com.br/internacional/',
        'https://www.cnnbrasil.com.br/esporte/',
        'https://www.cnnbrasil.com.br/saude/',
        'https://www.cnnbrasil.com.br/tecnologia/',
        'https://www.cnnbrasil.com.br/entretenimento/',
        'https://www.cnnbrasil.com.br/estilo/',
        'https://www.cnnbrasil.com.br/loterias/',
    ]
    _pkNoticias = count(0)
    for pk, links in enumerate(url):
        resposta = requests.get(links)
        html = BeautifulSoup(resposta.text, 'html.parser')
        nomeSessao = links.split('/')[-2]
        dbPortal.atualizarColuna('dt_hr_pesquisa',f'id_pk={pk}', dataHora)
        dbPortal.atualizarColuna('link_site', f'id_pk={pk}', links)
        dbPortal.atualizarColuna('nome_sessao', f'id_pk={pk}', nomeSessao)
        for noticias in html.select('.home__list__item'):
            _pkeyNoticias = next(_pkNoticias)
            tituloMateria = noticias.a.get_text().strip()
            linkMateria = noticias.a.get('href').strip()
            dbMaterias.atualizarColuna('referencia_site', f'id_pk={_pkeyNoticias}', pk)
            dbMaterias.atualizarColuna('link_materia', f'id_pk={_pkeyNoticias}', linkMateria)
            dbMaterias.atualizarColuna('titulo_materia', f'id_pk={_pkeyNoticias}', tituloMateria)
            resp = requests.get(linkMateria)
            html1 = BeautifulSoup(resp.text, 'html.parser')
            for materia in html1.select('.posts'):
                dataMateria = materia.select_one('.post__data').get_text(strip=True)[:11].strip()
                textoCru = materia.find_all('p')
                textoMateria = ''
                for palavras in textoCru:
                    palavra = palavras.get_text(' | ', strip=True)
                    textoMateria += palavra
                dbMaterias.atualizarColuna('dt_materia', f'id_pk={_pkeyNoticias}',
                datetime.strptime(dataMateria, '%d/%m/%Y'))
                dbMaterias.atualizarColuna('texto_materia', f'id_pk={_pkeyNoticias}', textoMateria)
    dbPortal.fecharConexao()
    dbMaterias.fecharConexao()
    dbLog.fecharConexao()


coreCnn()
