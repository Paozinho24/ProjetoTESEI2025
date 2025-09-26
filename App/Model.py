import ConexaoBanco
import sqlite3

class Model:
    def __init__(self):
       
        self.con = ConexaoBanco.Conexao()

    def validar_login(self, cpf, senha):
    
        con = self.con.ConectaBanco()
        if con is None:
            raise sqlite3.Error("Sem conexão csom o banco de dados.")

        try:
            cursor = con.cursor()
            sql = "SELECT 1 FROM Tecnicos WHERE CPF = ? AND Senha = ?"
            parametros = (cpf, senha)
            cursor.execute(sql, parametros)
            linha = cursor.fetchone()

            if linha is None:
                return False
            else:
                return True
        finally:
            try:
                con.close()
            except Exception:
                pass
