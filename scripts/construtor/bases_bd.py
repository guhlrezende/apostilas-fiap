import os
import re, json, sqlite3, sys
sys.stdout.reconfigure(encoding="utf-8")
SRC = "C:/life_os/areas/educacao/aulas/1TIAPR-2026/cognitive-data-science/"
alpha = open(SRC+"aula-26-09-24/script-criacao-base-alpha.sql", encoding="utf-8").read()
ins = "\n".join(re.findall(r"INSERT INTO .*?;", alpha, flags=re.S))
ddl = lambda fk: """CREATE TABLE Funcionario (
  idFuncionario INTEGER PRIMARY KEY AUTOINCREMENT,
  CPF CHAR(11) NOT NULL UNIQUE,
  nome VARCHAR(50) NOT NULL,
  sobrenome VARCHAR(50) NOT NULL,
  habilidades VARCHAR(100),
  email VARCHAR(30)
);
CREATE TABLE Projeto (
  idProjeto INTEGER PRIMARY KEY AUTOINCREMENT,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100),
  dtInicio DATE,
  dtTermino DATE
);
CREATE TABLE ProjetoFuncionario (
  idFuncionario INT NOT NULL,
  idProjeto INT NOT NULL,
  ativo INT NOT NULL,
  horas INT NOT NULL,
  PRIMARY KEY (idFuncionario, idProjeto)""" + (""",
  FOREIGN KEY (idFuncionario) REFERENCES Funcionario(idFuncionario),
  FOREIGN KEY (idProjeto) REFERENCES Projeto(idProjeto)""" if fk else "") + """
);
"""
alpha_sql = ddl(False) + ins + "\n"
alpha_fk_sql = ddl(True) + ins + "\n"
pap = open(SRC+"aula-26-10-08/DDL_DML_Papelaria_JOINS.sql", encoding="utf-8").read()
pap = re.sub(r"^-{3,}.*$", "", pap, flags=re.M)
pap = re.sub(r"CREATE DATABASE .*?;|USE .*?;|DROP TABLE IF EXISTS .*?;", "", pap)
pap = pap.replace("`", "")
pap = re.sub(r"int NOT NULL AUTO_INCREMENT", "INTEGER", pap)
pap = re.sub(r",\s*KEY \w+ \(\w+\)", "", pap)
pap = re.sub(r"CONSTRAINT \w+ ", "", pap).replace("decimal(10,2)", "DECIMAL(10,2)").strip()
loja = """CREATE TABLE pedido_flat (
  idPedido INTEGER, cliente_id INTEGER, cliente_nome TEXT, cliente_cidade TEXT, produto TEXT, preco REAL
);
INSERT INTO pedido_flat VALUES
  (1, 10, 'Júlia',  'São Paulo',      'Caderno', 10),
  (2, 10, 'Júlia',  'São Paulo',      'Lápis',    5),
  (3, 10, 'Júlia',  'São Paulo',      'Estojo',  20),
  (4, 20, 'Amanda', 'Belo Horizonte', 'Régua',   15);
CREATE TABLE cliente_n (cliente_id INTEGER PRIMARY KEY, nome TEXT, cidade TEXT);
CREATE TABLE pedido_n (idPedido INTEGER PRIMARY KEY, cliente_id INTEGER REFERENCES cliente_n(cliente_id), produto TEXT, preco REAL);
INSERT INTO cliente_n VALUES (10, 'Júlia', 'São Paulo'), (20, 'Amanda', 'Belo Horizonte');
INSERT INTO pedido_n VALUES (1, 10, 'Caderno', 10), (2, 10, 'Lápis', 5), (3, 10, 'Estojo', 20), (4, 20, 'Régua', 15);
"""
for n, s in (("alpha", alpha_sql), ("alpha_fk", alpha_fk_sql), ("papelaria", pap), ("loja", loja)):
    sqlite3.connect(":memory:").executescript(s)
# FK de verdade?
db = sqlite3.connect(":memory:"); db.execute("PRAGMA foreign_keys=ON"); db.executescript(alpha_fk_sql)
for stmt in ("DELETE FROM Projeto WHERE idProjeto = 3", "INSERT INTO ProjetoFuncionario VALUES (999, 1, 1, 4)"):
    try: db.execute(stmt); print("sem erro:", stmt)
    except Exception as e: print("erro:", stmt, "->", e)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "banco-de-dados", "bases.js"), "w", encoding="utf-8") as f:
    f.write("/* Bases das aulas, em dialeto SQLite (o navegador roda SQLite). Geradas a partir dos scripts do MySQL das aulas. */\nEstudo.sqlDBs = Estudo.sqlDBs || {};\n")
    alpha_sql = alpha_sql.replace("'Gustavo', 'Ribeiro'", "'Gabriel', 'Ribeiro'").replace("gustavo.ribeiro@", "gabriel.ribeiro@")  # nome de exemplo neutro
    alpha_fk_sql = alpha_fk_sql.replace("'Gustavo', 'Ribeiro'", "'Gabriel', 'Ribeiro'").replace("gustavo.ribeiro@", "gabriel.ribeiro@")
    for n, s in (("alpha", alpha_sql), ("alpha_fk", alpha_fk_sql), ("papelaria", pap), ("loja", loja), ("vazia", "")):
        f.write(f"Estudo.sqlDBs.{n} = " + json.dumps(s, ensure_ascii=False) + ";\n")
print("bases ok")
