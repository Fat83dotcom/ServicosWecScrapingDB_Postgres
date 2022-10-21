from mimetypes import init
import psycopg2
from abc import ABC
from databaseSettings import CONFIG


class BancoDeDados(ABC):
    def __init__(self, host='', port='', dbname='', user='', password='') -> None:
        self.con = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password)
        self.cursor = self.con.cursor()

    def fecharConexao(self):
        self.con.close()

    def executar(self, sql):
        self.cursor.execute(sql)

    def enviar(self):
        self.con.commit()

    def abortar(self):
        self.con.rollback()

    def buscarDados(self):
        return self.cursor.fetchall()

    def buscarUmDado(self):
        return self.cursor.fetchone()

    def buscarIntervalo(self, intervalo):
        return self.cursor.fetchmany(intervalo)

    def geradorSQLInsert(self, *args, nome_colunas=None,  nome_tabela=None):
        valores = f'{args}'
        sql = f"INSERT INTO {nome_tabela} {nome_colunas} VALUES {valores}"
        return sql

    def geradorSQLUpdate(self, *args, nome_colunas=None, nome_tabela=None, condicao=None):
        valores = args[0]
        sql = f"UPDATE {nome_tabela} SET {nome_colunas}=('{valores}') WHERE {condicao}"
        print(sql)
        return sql


class OperacoesTabelasBD(BancoDeDados):
    
    def __init__(self, tabela) -> None:
        super().__init__()
        db_set = CONFIG
        self.tablela = tabela
        self.Bd = BancoDeDados(
        dbname=db_set['banco_dados'],
        user=db_set['usuario'],
        port=db_set['porta'],
        password=db_set['senha'],
        host=db_set['host'])
    

    def atualizarColuna(self, coluna, condicao, atualizacao):
        sql = self.geradorSQLUpdate(
            atualizacao, nome_tabela=self.tablela,
            nome_colunas=coluna, condicao=condicao)
        
        try:
            self.Bd.executar()
            self.Bd.enviar()
        except Exception:
            self.Bd.abortar
        