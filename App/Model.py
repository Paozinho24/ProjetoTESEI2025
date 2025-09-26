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
            
            
    def listar_reagentes_localizacao(self, nome_parcial=None):
          
            con = self.con.ConectaBanco()
            if con is None:
                raise sqlite3.Error("Sem conexão com o banco de dados.")
            try:
                cursor = con.cursor()

                sql = """
                    SELECT
                        r.Id,
                        r.Nome,
                        r.CAS,
                        r.Formula,
                        r.Unidade,
                        COALESCE(l.Quantidade, 0)      AS Quantidade,
                        COALESCE(l.Armario, '')         AS Armario,
                        COALESCE(l.Prateleira, '')      AS Prateleira,
                        COALESCE(l.Posicao, '')         AS Posicao
                    FROM Reagentes r
                    LEFT JOIN Localizacao l ON l.Id = r.Id
                """

                params = ()
                if nome_parcial is not None and nome_parcial.strip() != "":
                    sql += " WHERE r.Nome LIKE ?"
                    params = ("%{}%".format(nome_parcial.strip()),)

                sql += " ORDER BY r.Nome;"

                cursor.execute(sql, params)
                linhas = cursor.fetchall()
                return linhas
            finally:
                        try:
                            con.close()
                        except Exception:
                            pass