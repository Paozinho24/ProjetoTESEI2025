import ConexaoBanco
import sqlite3
from datetime import datetime

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
            try:
                # Registrar movimentação de cadastro
                cur.execute('INSERT INTO Movimentacoes (Reagente_Id, TipoDeMovimentacao, Motivo, Responsavel, Projeto) VALUES (?, ?, ?, ?, ?)',
                            (id, 'Cadastro', 'Cadastro', 'Sistema', None))
                con.commit()
            except Exception:
                try:
                    con.rollback()
                except Exception:
                    pass
            return id

        except Exception:
            con.rollback()
            raise
        finally:
            try:
                con.close()
            except Exception:
                pass
    
    def atualizar_Reagente(self, id, nome, formula=None, cas=None, unidade=None, quantidade=None, armario=None, prateleira=None, posicao=None):
        """
        Atualiza o reagente (tabela Reagentes) e a localização correspondente (tabela Localizacao).
        Se não existir registro de Localizacao para esse reagente, insere-o.
        Retorna True se sucesso.
        """
        con = self.con.ConectaBanco()
        if con is None:
            raise sqlite3.Error("Sem conexão com o banco de dados.")

        try:
            cur = con.cursor()
            # Atualiza tabela Reagentes
            cur.execute("UPDATE Reagentes SET Nome = ?, Formula = ?, CAS = ?, Unidade = ? WHERE Id = ?",
                        (nome, formula, cas, unidade, id))

            # Verifica se já existe localização
            cur.execute('SELECT 1 FROM Localizacao WHERE [fk_Reagentes_Localização] = ? LIMIT 1', (id,))
            exists = cur.fetchone()

            if exists:
                cur.execute('UPDATE Localizacao SET Posicao = ?, Prateleira = ?, Armario = ?, Quantidade = ? WHERE [fk_Reagentes_Localização] = ?',
                            (posicao or "", prateleira or "", armario or "", quantidade or 0, id))
            else:
                # Insere apenas se qualquer campo de localização for fornecido
                if any(v is not None for v in (posicao, prateleira, armario, quantidade)):
                    cur.execute('INSERT INTO Localizacao ([fk_Reagentes_Localização], Posicao, Prateleira, Armario, Quantidade) VALUES (?, ?, ?, ?, ?)',
                                (id, posicao or "", prateleira or "", armario or "", quantidade or 0))

            con.commit()
            try:
                # Registrar movimentação de atualização
                cur.execute('INSERT INTO Movimentacoes (Reagente_Id, TipoDeMovimentacao, QuantidadeMovimentada, Motivo, Responsavel, Projeto) VALUES (?, ?, ?, ?, ?, ?)',
                            (id, 'Atualização', quantidade or 0, 'Cadastro de Novo Reagente', 'Sistema', None))
                con.commit()
            except Exception:
                try:
                    con.rollback()
                except Exception:
                    pass
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

    def listar_movimentacoes_periodo(self, data_inicio: str, data_fim: str):
        """Retorna as movimentações entre data_inicio e data_fim.
        data_inicio e data_fim devem estar no formato 'YYYY-MM-DD' ou 'YYYY-MM-DD HH:MM:SS'.
        Retorna lista de tuplas: (Id, Reagente_Id, TipoDeMovimentacao, QuantidadeMovimentada, Motivo, Responsavel, Projeto, DataHora)
        """
        con = self.con.ConectaBanco()
        if con is None:
            raise sqlite3.Error("Sem conexão com o banco de dados.")
        try:
            cur = con.cursor()
            # normalizar datas para incluir tempo se necessário
            if len(data_inicio) == 10:
                data_inicio_q = data_inicio + ' 00:00:00'
            else:
                data_inicio_q = data_inicio
            if len(data_fim) == 10:
                data_fim_q = data_fim + ' 23:59:59'
            else:
                data_fim_q = data_fim

            sql = '''SELECT Id, Reagente_Id, TipoDeMovimentacao, QuantidadeMovimentada, Motivo, Responsavel, Projeto, DataHora
                     FROM Movimentacoes
                     WHERE DataHora BETWEEN ? AND ?
                     ORDER BY DataHora ASC''' 
            cur.execute(sql, (data_inicio_q, data_fim_q))
            rows = cur.fetchall()
            return rows
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
            rows = cur.fetchall()
            # print(rows)
            formatted = []
            for r in rows:
                nome = r[0]
                cpf = r[1]
                senha = r[2] 
                email = r[3] 
                formatted.append((nome, cpf, senha, email))
            return formatted
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
            row = cur.fetchone()
            if not row:
                return None
            nome = row[0]
            cpf_val = row[1]
            senha = row[2] if len(row) > 2 else None
            email = row[3] if len(row) > 3 else None
            try:
                cpf_str = str(cpf_val).zfill(11)
            except Exception:
                cpf_str = str(cpf_val)
            return (nome, cpf_str, senha, email)
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

    def retirar_reagente(self, reagente_id, quantidade_retirada, motivo, responsavel, projeto=None):
        """Retira uma quantidade do reagente (Localizacao) e registra uma movimentação.
        Retorna True se sucesso, lança exceção em erro.
        """
        con = self.con.ConectaBanco()
        if con is None:
            raise sqlite3.Error("Sem conexão com o banco de dados.")

        try:
            cur = con.cursor()

            # Obter quantidade atual (se existir)
            cur.execute('SELECT Quantidade FROM Localizacao WHERE [fk_Reagentes_Localização] = ? LIMIT 1', (reagente_id,))
            row = cur.fetchone()
            atual = 0
            if row and len(row) > 0 and row[0] is not None:
                try:
                    atual = float(row[0])
                except Exception:
                    atual = 0

            # Validar quantidade_retirada
            try:
                qtd = float(quantidade_retirada)
            except Exception:
                raise ValueError("Quantidade inválida")

            if qtd <= 0:
                raise ValueError("Quantidade a retirar deve ser maior que zero")

            if qtd > atual:
                raise ValueError("Quantidade insuficiente no estoque")

            nova = atual - qtd

            # Atualiza ou insere registro de localização
            cur.execute('SELECT 1 FROM Localizacao WHERE [fk_Reagentes_Localização] = ? LIMIT 1', (reagente_id,))
            exists = cur.fetchone()
            if exists:
                cur.execute('UPDATE Localizacao SET Quantidade = ? WHERE [fk_Reagentes_Localização] = ?', (nova, reagente_id))
            else:
                cur.execute('INSERT INTO Localizacao ([fk_Reagentes_Localização], Posicao, Prateleira, Armario, Quantidade) VALUES (?, ?, ?, ?, ?)', (reagente_id, '', '', '', nova))

            con.commit()

            # Inserir movimentação — tentar com a coluna QuantidadeMovimentada e falhar para alternativa
            # Registrar movimentação com DataHora explícita (junto com QuantidadeMovimentada quando possível)
            datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                cur.execute('INSERT INTO Movimentacoes (Reagente_Id, TipoDeMovimentacao, QuantidadeMovimentada, Motivo, Responsavel, Projeto, DataHora) VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (reagente_id, 'Retirada', qtd, motivo or '', responsavel or '', projeto, datahora))
                con.commit()
            except Exception:
                try:
                    # fallback para schema que não possua QuantidadeMovimentada
                    cur.execute('INSERT INTO Movimentacoes (Reagente_Id, TipoDeMovimentacao, Motivo, Responsavel, Projeto, DataHora) VALUES (?, ?, ?, ?, ?, ?)',
                                (reagente_id, 'Retirada', motivo or '', responsavel or '', projeto, datahora))
                    con.commit()
                except Exception:
                    try:
                        con.rollback()
                    except Exception:
                        pass
                    raise

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
            
