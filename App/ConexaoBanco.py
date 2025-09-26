import sqlite3
from sqlite3 import Error

class Conexao:
    # Mantém sua forma de conexão simples
    @staticmethod
    def ConectaBanco():
        try:
            caminho = "BancoDeDados/BancoProjetoTese.db"  # relativo à pasta de execução
            con = sqlite3.connect(caminho)
            return con
        except Error as ex:
            print("Erro ao conectar:", ex)
            return None
