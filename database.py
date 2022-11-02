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
        valores = args[0]
        sql = "INSERT INTO %s %s VALUES %s" % (nome_tabela, nome_colunas, valores)
        return sql

    def geradorSQLUpdate(self, *args, nome_colunas=None, nome_tabela=None, condicao=None):
        valores = args[0]
        sql = "UPDATE %s SET %s='%s' WHERE %s" % (nome_tabela, nome_colunas, valores, condicao)
        return sql


class OperacoesTabelasBD(BancoDeDados):
    
    def __init__(self, tabela) -> None:
        self.tablela = tabela
        self.Bd = BancoDeDados(
        dbname=CONFIG['banco_dados'],
        user=CONFIG['usuario'],
        port=CONFIG['porta'],
        password=CONFIG['senha'],
        host=CONFIG['host'])
    

    def atualizarColuna(self, coluna, condicao, atualizacao):
        sql = self.geradorSQLUpdate(
            atualizacao, nome_tabela=self.tablela,
            nome_colunas=coluna, condicao=condicao)
        
        try:
            self.Bd.executar(sql)
            self.Bd.enviar()
        except Exception:
            self.Bd.abortar()
    
    def inserirColunas(self, *args, coluna):
        try:
            sql = self.geradorSQLInsert(*args, nome_colunas=coluna, nome_tabela=self.tablela)
            self.Bd.executar(sql)
            self.Bd.enviar()
        except Exception as erro:
            self.Bd.abortar()
            print(erro)
    
    def fecharConexao(self):
        return self.Bd.fecharConexao()



if __name__ == '__main__':
    teste = OperacoesTabelasBD('portalcnn')
    teste.atualizarColuna('link_materia', 'id_pk=0', 'fiuerfiuerhfieurhfieurfheirufhe' )
