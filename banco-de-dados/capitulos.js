/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */
window.APOSTILA = {
  "id": "banco-de-dados",
  "titulo": "Bancos de Dados e SQL",
  "caps": [
    {
      "n": 1,
      "file": "cap-1-dados-e-sgbd.html",
      "titulo": "Dados, SGBD e normalização",
      "aula": "Aula 1",
      "tempo": 30,
      "resumo": "Dado x informação, o que um SGBD faz, o modelo relacional de Codd e por que normalizar.",
      "pergunta": "Já sei o que é um banco. Como desenho o que vai dentro dele, antes de criar qualquer tabela?"
    },
    {
      "n": 2,
      "file": "cap-2-modelagem-er.html",
      "titulo": "Modelagem entidade-relacionamento",
      "aula": "Aula 2",
      "tempo": 35,
      "resumo": "Schema, os três níveis de modelo, entidades, atributos, relacionamentos e cardinalidade.",
      "pergunta": "O desenho está pronto no papel. Como ele vira tabelas de verdade, com regras que o banco faz valer?"
    },
    {
      "n": 3,
      "file": "cap-3-modelo-logico-ddl.html",
      "titulo": "Modelo lógico e DDL",
      "aula": "Aula 3",
      "tempo": 40,
      "resumo": "Chaves primária e estrangeira, restrições, tipos de dados e CREATE, ALTER e DESC.",
      "pergunta": "As tabelas existem, mas estão vazias. Como coloco, procuro e mudo os dados?"
    },
    {
      "n": 4,
      "file": "cap-4-dml.html",
      "titulo": "DML: INSERT, SELECT, UPDATE, DELETE",
      "aula": "Aula 4",
      "tempo": 45,
      "resumo": "O CRUD em SQL, filtros com WHERE, AND, OR, LIKE e BETWEEN, e o perigo de esquecer o WHERE.",
      "pergunta": "Consigo achar linhas. Mas e se eu quiser resumos, como médias e totais por projeto?"
    },
    {
      "n": 5,
      "file": "cap-5-agregacoes.html",
      "titulo": "Agregações, GROUP BY e HAVING",
      "aula": "Aula 5",
      "tempo": 35,
      "resumo": "MIN, MAX, AVG, SUM, COUNT, DISTINCT, agrupar por subgrupos e filtrar grupos.",
      "pergunta": "Os resumos estão por id. E se o nome do projeto mora em outra tabela?"
    },
    {
      "n": 6,
      "file": "cap-6-joins-union.html",
      "titulo": "JOINs e UNION",
      "aula": "Aula 6",
      "tempo": 45,
      "resumo": "INNER, LEFT, RIGHT e FULL JOIN, apelidos de tabela e UNION x UNION ALL.",
      "pergunta": "Meus comandos ficaram enormes e eu reescrevo os mesmos JOINs. Dá para guardar isso no banco?"
    },
    {
      "n": 7,
      "file": "cap-7-views-procedures-triggers.html",
      "titulo": "Programando no banco",
      "aula": "Aula 7",
      "tempo": 40,
      "resumo": "View, Function, Stored Procedure e Trigger, e por que existe o DELIMITER.",
      "pergunta": "Tenho o essencial de SQL. O que separa um banco que funciona de um que funciona bem?"
    },
    {
      "n": 8,
      "file": "cap-8-alem-do-basico.html",
      "titulo": "Para ir além (complemento)",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Índices, transações e ACID, subconsultas, injeção de SQL e quando usar NoSQL.",
      "pergunta": ""
    }
  ]
};
