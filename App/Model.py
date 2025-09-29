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
            
            
    def listar_reagentes_localizacao(self):
          
            con = self.con.ConectaBanco()
            if con is None:
                raise sqlite3.Error("Sem conexão com o banco de dados.")
            try:
                cursor = con.cursor()

                sql = """
                    SELECT
                        r.Id,
                        r.Nome,
                        COALESCE(r.CAS, ''),
                        COALESCE(r.Formula, ''),
                        COALESCE(r.Unidade, ''),
                        COALESCE(l.Quantidade, 0),
                        COALESCE(l.Armario, ''),
                        COALESCE(l.Prateleira, ''),
                        COALESCE(l.Posicao, '')
                    FROM Reagentes r
                    LEFT JOIN Localizacao l
                        ON l.[fk_Reagentes_Localização] = r.Id
                    """
                params = ()
                sql += " ORDER BY r.Nome;"

                cursor.execute(sql, params)
                linhas = cursor.fetchall()
                return linhas
            finally:
                        try:
                            con.close()
                        except Exception:
                            pass

