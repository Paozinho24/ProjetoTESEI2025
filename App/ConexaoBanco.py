import sqlite3
from sqlite3 import Error
from pathlib import Path

SCHEMA_SQL = '''BEGIN TRANSACTION;

PRAGMA foreign_keys = ON;

-- Tabelas base
CREATE TABLE IF NOT EXISTS "Localizacao" (
    "fk_Reagentes_Localização" INT(11),
    "Posicao"      VARCHAR(50),
    "Prateleira"   VARCHAR(50),
    "Armario"      VARCHAR(50),
    "Quantidade"   DECIMAL(10, 2),
    "Id_Localizacao" INTEGER,
    PRIMARY KEY("Id_Localizacao"),
    FOREIGN KEY("fk_Reagentes_Localização") REFERENCES "Reagentes"("Id")
);

CREATE TABLE IF NOT EXISTS "Reagentes" (
    "Id"      INT(11) PRIMARY KEY,
    "Nome"    VARCHAR(100) NOT NULL,
    "Formula" VARCHAR(50),
    "CAS"     VARCHAR(20),
    "Unidade" VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "Tecnicos" (
    "Id"    INTEGER NOT NULL,
    "Nome"  VARCHAR(110) NOT NULL,
    "CPF"   VARCHAR(11) NOT NULL,
    "Senha" VARCHAR(10) NOT NULL,
    "Email" INTEGER NOT NULL,
    PRIMARY KEY("Id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "Movimentacoes" (
    "Id"                    INTEGER PRIMARY KEY AUTOINCREMENT,
    "Reagente_Id"           INTEGER NOT NULL,
    "TipoDeMovimentacao"    VARCHAR(200) NOT NULL,
    "QuantidadeMovimentada" DECIMAL(10,2),
    "Motivo"                VARCHAR(200) NOT NULL,
    "Responsavel"           VARCHAR(110) NOT NULL,
    "Projeto"               VARCHAR(150),
    "DataHora"              DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("Reagente_Id") REFERENCES "Reagentes"("Id")
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Índice para acelerar JOINs/consultas por reagente
CREATE INDEX IF NOT EXISTS "idx_mov_reagente" ON "Movimentacoes"("Reagente_Id");

-- VIEW com JOIN que já traz o Nome do reagente
CREATE VIEW IF NOT EXISTS "MovimentacoesDetalhe" AS
SELECT
    m.Id,
    m.Reagente_Id,
    r.Nome AS NomeReagente,
    m.TipoDeMovimentacao,
    m.QuantidadeMovimentada,
    m.Motivo,
    m.Responsavel,
    m.Projeto,
    m.DataHora
FROM Movimentacoes m
JOIN Reagentes r ON r.Id = m.Reagente_Id;

-- Usuário admin inicial (só se ainda não existir)
INSERT INTO "Tecnicos" ("Nome", "CPF", "Senha", "Email")
SELECT 'admin', 'admin', 'admin2424', 'k.g.a2014@outlook.com'
WHERE NOT EXISTS (SELECT 1 FROM "Tecnicos" WHERE "Nome"='admin' AND "CPF"='admin');

COMMIT;
'''
class Conexao:

    @staticmethod
    def ConectaBanco():
        try:
            # Usar caminho absoluto relativo ao diretório do projeto
            base = Path(__file__).resolve().parents[1]
            db_dir = base / 'BancoDeDados'
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / 'BancoProjetoTese.db'

            first_time = not db_path.exists()
            con = sqlite3.connect(str(db_path))

            if first_time:
                try:
                    cur = con.cursor()
                    cur.executescript(SCHEMA_SQL)
                    con.commit()
                    print(f"Banco criado em: {db_path}")
                except Exception as ex:
                    print('Erro ao criar schema:', ex)

            return con
        except Error as ex:
            print("Erro ao conectar:", ex)
            return None