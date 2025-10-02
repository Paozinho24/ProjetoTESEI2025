import sqlite3
from sqlite3 import Error

class Conexao:
   
    @staticmethod
    def ConectaBanco():
        try:
            caminho = "BancoDeDados/BancoProjetoTese.db" 
            con = sqlite3.connect(caminho)
            print("Solicitou algo do Banco") 
            return con
        except Error as ex:
            print("Erro ao conectar:", ex)
            return None
    
 