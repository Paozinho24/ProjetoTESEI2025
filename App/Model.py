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
            # print("PASSEI AQUI")
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

    def cadastrar_Reagente(self, nome, formula=None, cas=None, unidade=None, quantidade=None, armario=None, prateleira=None, posicao=None, id=None):

        con = self.con.ConectaBanco()
        #verificação se banco tá rodando 
        
        if con is None:
            raise sqlite3.Error("Sem conexão com o banco de dados.")

        try:
            cur = con.cursor()

            # Gera próximo Id 
            if id is None:
                cur.execute("SELECT COALESCE(MAX(Id), 0) + 1 FROM Reagentes")
                id = cur.fetchone()[0]

            # Inserir reagente
            cur.execute( "INSERT INTO Reagentes (Id, Nome, Formula, CAS, Unidade) VALUES (?, ?, ?, ?, ?)", (id, nome, formula, cas, unidade))

            # Inserir localização
            if any(v is not None for v in (posicao, prateleira, armario, quantidade)):
                cur.execute(
                    'INSERT INTO Localizacao ([fk_Reagentes_Localização], Posicao, Prateleira, Armario, Quantidade) '
                    'VALUES (?, ?, ?, ?, ?)',
                    (id, posicao or "", prateleira or "", armario or "", quantidade or 0)
                )

            con.commit()
            return id

        except Exception:
            con.rollback()
            raise
        finally:
            try:
                con.close()
            except Exception:
                pass
            
    # PARA O NOME DO USUÁRIO APARECER NA TELA PRINCIPAL
    def getNomeUsuario(self, cpf: str) -> str:
        con = self.con.ConectaBanco()
        cur = con.cursor()
        cur.execute("SELECT Nome FROM Tecnicos WHERE CPF = ? LIMIT 1", (cpf,))
        row = cur.fetchone()
        con.close()
        return row[0] 

    # ListaOsUsuáriosDoSistema
    def listar_tecnicos(self):
        con = self.con.ConectaBanco()
        try:
            cur = con.cursor()
            cur.execute("SELECT Nome, CPF, Senha, Email FROM Tecnicos ORDER BY Nome")
            return cur.fetchall()
        finally:
            try:
                con.close()
            except Exception:
                pass
    #
    def PegarCPF(self, cpf):
        con = self.con.ConectaBanco()
        try:
            cur = con.cursor()
            cur.execute("SELECT Nome, CPF, Senha, Email FROM Tecnicos WHERE CPF = ? LIMIT 1", (cpf,))
            return cur.fetchone()
        finally:
            try:
                con.close()
            except Exception:
                pass

    def inserir_tecnico(self, nome, cpf, senha, email=None):
        con = self.con.ConectaBanco()
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO Tecnicos (Nome, CPF, Senha, Email) VALUES (?, ?, ?, ?)", (nome, cpf, senha, email))
            con.commit()
            return True
        except Exception:
            try:
                con.rollback()
            except Exception:
                pass
            raise
        finally:
            try:
                con.close()
            except Exception:
                pass

    def atualizar_tecnico(self, nome, cpf, senha, email, original_cpf):
        con = self.con.ConectaBanco()
        try:
            cur = con.cursor()
            cur.execute("UPDATE Tecnicos SET Nome = ?, CPF = ?, Senha = ?, Email = ? WHERE CPF = ?", (nome, cpf, senha, email, original_cpf))
            con.commit()
            return True
        except Exception:
            try:
                con.rollback()
            except Exception:
                pass
            raise
        finally:
            try:
                con.close()
            except Exception:
                pass

    def deletar_tecnico(self, cpf):
        con = self.con.ConectaBanco()
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM Tecnicos WHERE CPF = ?", (cpf,))
            con.commit()
            return True
        except Exception:
            try:
                con.rollback()
            except Exception:
                pass
            raise
        finally:
            try:
                con.close()
            except Exception:
                pass
