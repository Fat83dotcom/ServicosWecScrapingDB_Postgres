from datetime import datetime
from bs4 import BeautifulSoup
import requests
from database import OperacoesTabelasBD
from itertools import count



def coreCnn():
    dbPortal = OperacoesTabelasBD('portalcnn')
    dbMaterias = OperacoesTabelasBD('materiasportal')
    dataHora: str = str(datetime.now())
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
        dbPortal.atualizarColuna('dt_hr_pesquisa',f'id_pk={pk}', dataHora)
        dbPortal.atualizarColuna('sessao_site', f'id_pk={pk}', links)
        for noticias in html.select('.home__list__item'):
            _pkeyNoticias = next(_pkNoticias)
            tituloMateria = noticias.a.get_text().strip()
            linkMateria = noticias.a.get('href').strip()
            dbMaterias.atualizarColuna('sessao_site', f'id_pk={_pkeyNoticias}', links)
            dbMaterias.atualizarColuna('link_materia', f'id_pk={_pkeyNoticias}', linkMateria)
            dbMaterias.atualizarColuna('titulo_materia', f'id_pk={_pkeyNoticias}', tituloMateria)
            resp = requests.get(linkMateria)
            html1 = BeautifulSoup(resp.text, 'html.parser')
            for materia in html1.select('.posts'):
                dataMateria = materia.select_one('.post__data').get_text(strip=True)[:11].strip()
                texto = materia.select_one('.post__content').get_text(' | ', strip=True)
                dbMaterias.atualizarColuna('dt_materia', f'id_pk={_pkeyNoticias}',
                datetime.strptime(dataMateria, '%d/%m/%Y'))
                dbMaterias.atualizarColuna('texto_materia', f'id_pk={_pkeyNoticias}', texto)

coreCnn()