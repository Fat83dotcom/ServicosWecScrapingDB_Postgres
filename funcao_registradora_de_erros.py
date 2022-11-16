from database import OperacoesTabelasBD
from datetime import datetime


def registradorErros(classe_erro, desc_erro, func_name):
    try:
        dataHora: str = str(datetime.now())
        dbLogErro = OperacoesTabelasBD('log_erro')
        dbLogErro.inserirColunas(f"('{dataHora}', '{classe_erro}', '{desc_erro}', '{func_name}')", \
            coluna='(dt_hr_erro, classe_erro, descricao_erro, nome_funcao_origem)')
    except Exception as e:
        with open(f'logs/log_erro_{dataHora}.txt', 'w') as arquivo:
            erro = f'{str(e.__class__.__name__)}, {str(e)}'
            arquivo.write(erro)
