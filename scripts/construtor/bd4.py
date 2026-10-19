from bld import *
T = "Bancos de Dados e SQL"
S = ["bases.js"]

def trace(titulo, code, steps):
    import json
    d = json.dumps({"titulo": titulo, "code": code, "steps": steps}, ensure_ascii=False)
    d = d.replace("</", "<\\/")
    return f'<div class="demo" data-demo="trace"><script type="application/json">{d}</script></div>'

# ---------------- CAP 7 ----------------
tr_func = trace("Função IMC, passo a passo", [
    "DELIMITER //",
    "CREATE FUNCTION IMC (peso FLOAT, altura FLOAT)",
    "RETURNS FLOAT DETERMINISTIC",
    "BEGIN",
    "  RETURN peso/(altura*altura);",
    "END//",
    "DELIMITER ;",
    "SELECT IMC(70, 1.70);"], [
    {"l": 0, "v": {}, "o": "", "n": "O cliente do MySQL trata <code>;</code> como fim de comando. Como o corpo da função terá <code>;</code>, trocamos o delimitador para <code>//</code>."},
    {"l": 1, "v": {}, "o": "", "n": "Nome da função e parâmetros com tipo. Ainda nada é executado: só está sendo <b>definida</b>."},
    {"l": 2, "v": {}, "o": "", "n": "<code>RETURNS FLOAT</code>: toda função devolve <b>um valor</b>, e o tipo é declarado. <code>DETERMINISTIC</code> promete que a mesma entrada dá sempre a mesma saída."},
    {"l": 4, "v": {}, "o": "", "n": "O corpo, entre <code>BEGIN</code> e <code>END</code>. Aqui ele devolve a conta do IMC."},
    {"l": 5, "v": {}, "o": "", "n": "O <code>//</code> fecha a criação. Só agora o MySQL guarda a função no banco."},
    {"l": 6, "v": {}, "o": "", "n": "Volta o delimitador para <code>;</code>."},
    {"l": 7, "v": {"peso": 70, "altura": 1.7}, "o": "", "n": "Chamada dentro de um SELECT: os argumentos entram nos parâmetros."},
    {"l": 4, "v": {"peso": 70, "altura": 1.7, "retorno": 24.2215}, "o": "IMC(70, 1.70)\n24.2215", "n": "70 / (1,7 × 1,7) = 70 / 2,89 = <b>24,2215</b>. O valor volta como se fosse uma coluna do SELECT."}])
tr_proc = trace("Procedure com parâmetro, passo a passo", [
    "DELIMITER //",
    "CREATE PROCEDURE sp_exibir_funcionario(id INT)",
    "BEGIN",
    "  SELECT * FROM funcionario FP WHERE idFuncionario = id;",
    "END //",
    "DELIMITER ;",
    "CALL sp_exibir_funcionario(1);"], [
    {"l": 1, "v": {}, "o": "", "n": "Define a procedure com um parâmetro <code>id</code>."},
    {"l": 3, "v": {}, "o": "", "n": "O corpo guarda um (ou mais) comandos SQL. Nada roda ainda."},
    {"l": 6, "v": {"id": 1}, "o": "", "n": "<code>CALL</code> chama a procedure e passa <code>id = 1</code>."},
    {"l": 3, "v": {"id": 1}, "o": "idFuncionario  nome  sobrenome  habilidades\n1              Ana   Silva      MySQL, SQL", "n": "O SELECT guardado roda com <code>id = 1</code>. Diferente da function, <b>não há RETURN</b>: o resultado é a própria consulta."}])
tr_trg = trace("Trigger de auditoria, passo a passo", [
    "CREATE TRIGGER trg_antes_atualizar_funcionario",
    "  BEFORE UPDATE ON funcionario",
    " FOR EACH ROW",
    "INSERT INTO FuncionarioAuditoria",
    "SET habilidades = OLD.habilidades,",
    "    data = NOW(), usuario = CURRENT_USER();",
    "",
    "UPDATE funcionario",
    "SET habilidades = CONCAT(habilidades, ', python')",
    "WHERE idFuncionario = 1;"], [
    {"l": 0, "v": {"funcionario.habilidades (id 1)": "MySQL, SQL", "FuncionarioAuditoria": "(vazia)"}, "o": "", "n": "A trigger fica <b>ligada à tabela</b> e ao evento. A partir de agora ela dispara sozinha."},
    {"l": 7, "v": {"funcionario.habilidades (id 1)": "MySQL, SQL", "FuncionarioAuditoria": "(vazia)"}, "o": "", "n": "Você roda um UPDATE normal. Você não chama a trigger: o <b>evento</b> chama."},
    {"l": 3, "v": {"OLD.habilidades": "MySQL, SQL", "NEW.habilidades": "MySQL, SQL, python", "FuncionarioAuditoria": "(vazia)"}, "o": "", "n": "Como a trigger é <code>BEFORE</code>, ela roda <b>antes</b> da mudança ser gravada. <code>OLD</code> é a linha como estava; <code>NEW</code> é como vai ficar."},
    {"l": 4, "v": {"OLD.habilidades": "MySQL, SQL", "FuncionarioAuditoria": "1 linha: 'MySQL, SQL'"}, "o": "", "n": "A trigger grava a versão <b>antiga</b> na tabela de auditoria."},
    {"l": 9, "v": {"funcionario.habilidades (id 1)": "MySQL, SQL, python", "FuncionarioAuditoria": "1 linha: 'MySQL, SQL'"}, "o": "", "n": "Só então o UPDATE é gravado. Resultado: a tabela tem o valor novo e a auditoria guarda o antigo, com a data e o usuário. Responde \"quem mudou isto?\"."}])

body7 = recap("No Capítulo 6 você juntou tabelas com JOIN, mas os comandos ficaram grandes: alguns JOINs com várias tabelas você reescreve toda hora, e certos dados precisam de tratamento antes de aparecer. O professor fez três perguntas: <i>como reaproveitar SQL extenso?</i> <i>como agrupar vários comandos numa chamada?</i> <i>como programar trechos reutilizáveis?</i>") + '''

<section class="sec" id="mapa">
  <h2><span class="sn">1</span>Quatro objetos, quatro jeitos de guardar código no banco</h2>
  <p class="gancho">Em vez de copiar e colar o mesmo SQL, dê um nome a ele.</p>
  <div class="tablewrap"><table>
    <tr><th>Objeto</th><th>Para que serve</th><th>Como se usa</th></tr>
    <tr><td><b>View</b></td><td>salvar uma <b>consulta</b> (por exemplo, vários JOINs)</td><td><code>SELECT * FROM minha_view;</code> como se fosse uma tabela</td></tr>
    <tr><td><b>Function</b></td><td>um cálculo ou regra que <b>devolve um valor</b></td><td><code>SELECT minha_funcao(...);</code>, serve dentro de outras consultas</td></tr>
    <tr><td><b>Procedure</b></td><td>um ou mais comandos guardados, com parâmetros</td><td><code>CALL minha_proc(...);</code></td></tr>
    <tr><td><b>Trigger</b></td><td>código que dispara <b>sozinho</b> num INSERT, UPDATE ou DELETE</td><td>não se chama: o evento chama</td></tr>
  </table></div>
  <div class="nota cuidado"><span class="lbl">Cuidado: o que roda no navegador</span>O SQLite do navegador tem <b>views</b> e <b>triggers</b>, mas <b>não tem functions nem procedures</b> (isso é do MySQL e de outros). Por isso as views e triggers abaixo são executáveis (com a sintaxe do SQLite, que difere um pouco), e as functions e procedures vêm com um passo a passo do código MySQL das aulas.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Começando pelo mais simples: como guardo um JOIN grande com um nome?</div><p>Com uma view.</p></div>
</section>

<section class="sec" id="view">
  <h2><span class="sn">2</span>View: a consulta com nome</h2>
  <p class="gancho">Escreveu o JOIN uma vez? Chame de novo pelo nome.</p>
  <p>Uma view é uma consulta salva. Ela <b>não guarda dados</b> (a consulta roda de novo a cada uso), esconde o JOIN e pode mostrar só algumas colunas, o que ajuda em relatórios e em controle de acesso.</p>
''' + sqlbox("alpha", """CREATE VIEW ViewProjetosEmAndamento AS
  SELECT P.nome AS nomeProjeto, F.nome, PF.horas
  FROM ProjetoFuncionario PF
  LEFT JOIN Projeto P ON PF.idProjeto = P.idProjeto
  LEFT JOIN Funcionario F ON PF.idFuncionario = F.idFuncionario
  ORDER BY P.nome, F.nome;

SELECT * FROM ViewProjetosEmAndamento;""", "Criando e usando uma view", expect=21) + '''
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Confiar no nome.</b> A <code>ViewProjetosEmAndamento</code> do slide <b>não filtra "em andamento"</b>: ela traz as 21 alocações, sem nenhum WHERE. O nome é só um nome. Quem lê o código, e não o rótulo, não se engana.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E quando preciso de uma conta que devolve um valor, como o IMC?</div><p>Uma function.</p></div>
</section>

<section class="sec" id="function">
  <h2><span class="sn">3</span>Function: devolve um valor</h2>
  <p class="gancho">Por que toda função do MySQL começa com um tal de DELIMITER?</p>
  <p>O cliente do MySQL entende <code>;</code> como "fim do comando". Mas dentro de <code>BEGIN ... END</code> há vários <code>;</code>, e o cliente cortaria no primeiro. Por isso se <b>troca o delimitador</b> (<code>//</code> ou <code>$$</code>), cria-se o objeto e se volta para <code>;</code>. Percorra o código:</p>
''' + tr_func + '''
  <p>Uma segunda função do slide lê uma tabela e usa variável. Ela soma as horas de um funcionário (o Carlos, id 2, está em dois projetos e dá 11):</p>
<pre><code><span class="k">CREATE FUNCTION</span> fn_total_horas_funcionario(p_idFuncionario <span class="k">INT</span>)
<span class="k">RETURNS INT DETERMINISTIC</span>
<span class="k">BEGIN</span>
    <span class="k">DECLARE</span> v_total <span class="k">INT DEFAULT</span> <span class="n">0</span>;
    <span class="k">SELECT SUM</span>(horas) <span class="k">INTO</span> v_total
    <span class="k">FROM</span> ProjetoFuncionario <span class="k">WHERE</span> idFuncionario = p_idFuncionario;
    <span class="k">RETURN</span> v_total;
<span class="k">END</span></code></pre>
  <div class="nota lembra"><span class="lbl">Complemento, conferido rodando</span>Para um funcionário <b>sem projeto</b> (a Vanessa, por exemplo), essa função devolve <b>NULL</b>, e não 0: o <code>SUM</code> de nenhuma linha é <code>NULL</code> e sobrescreve o <code>DEFAULT 0</code> da variável. Para devolver 0, use <code>COALESCE(SUM(horas), 0)</code>. Além disso, o slide marca a função como <code>DETERMINISTIC</code>, mas ela lê uma tabela, e o resultado muda quando os dados mudam. O MySQL aceitou assim no teste; marcar como <code>READS SQL DATA</code> seria mais fiel.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se eu quiser guardar um bloco de comandos, e não um valor?</div><p>Uma stored procedure.</p></div>
</section>

<section class="sec" id="procedure">
  <h2><span class="sn">4</span>Stored procedure: comandos guardados</h2>
  <p class="gancho">Uma function responde "quanto?". Uma procedure executa "faça isto".</p>
''' + tr_proc + '''
  <div class="tablewrap"><table>
    <tr><th></th><th>Function</th><th>Procedure</th></tr>
    <tr><td><b>Devolve</b></td><td>um valor, com <code>RETURN</code></td><td>nada (o resultado é a própria consulta que ela roda)</td></tr>
    <tr><td><b>Como se chama</b></td><td>dentro de um SELECT: <code>SELECT IMC(70, 1.7)</code></td><td>sozinha: <code>CALL sp_exibir_funcionario(1)</code></td></tr>
    <tr><td><b>Pode agrupar vários comandos</b></td><td>pouco usual</td><td>sim, é o uso principal</td></tr>
  </table></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se eu quisesse que algo acontecesse automaticamente quando alguém altera um dado?</div><p>Aí nenhuma chamada serve: o banco precisa reagir sozinho. É a trigger.</p></div>
</section>

<section class="sec" id="trigger">
  <h2><span class="sn">5</span>Trigger: o banco reage sozinho</h2>
  <p class="gancho">"Quem excluiu o registro XYZ?" Só dá para responder se alguém anotou na hora.</p>
  <p>Uma trigger (gatilho) fica ligada a <b>uma tabela</b> e a <b>um evento</b> (<code>INSERT</code>, <code>UPDATE</code> ou <code>DELETE</code>), em um momento (<code>BEFORE</code> ou <code>AFTER</code>), e roda <b>uma vez por linha afetada</b> (<code>FOR EACH ROW</code>). Usos do slide: <b>validar dados</b> e <b>auditar</b>. Dentro dela, <code>OLD</code> é a linha antes da mudança (existe em UPDATE e DELETE) e <code>NEW</code> é a linha depois (existe em INSERT e UPDATE).</p>
''' + tr_trg + '''
  <p>Agora rode você, no SQLite. A sintaxe muda um pouco (o corpo fica entre <code>BEGIN</code> e <code>END</code>, e no lugar de <code>NOW()</code> e <code>CURRENT_USER()</code> uso <code>date('now')</code> e um texto):</p>
''' + sqlbox("alpha", """CREATE TABLE FuncionarioAuditoria (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  habilidades VARCHAR(100) NOT NULL,
  usuario VARCHAR(50) NOT NULL,
  data DATE,
  acao VARCHAR(50)
);
CREATE TRIGGER trg_antes_atualizar_funcionario
BEFORE UPDATE ON Funcionario
FOR EACH ROW
BEGIN
  INSERT INTO FuncionarioAuditoria (habilidades, usuario, data)
  VALUES (OLD.habilidades, 'estudante', date('now'));
END;

UPDATE Funcionario SET habilidades = habilidades || ', python' WHERE idFuncionario = 1;
SELECT * FROM FuncionarioAuditoria;""", "Trigger de auditoria em ação", expect=1) + '''
  <p>A tabela de auditoria guardou <code>MySQL, SQL</code> (o valor <b>antigo</b>), e a <code>Funcionario</code> agora tem <code>MySQL, SQL, python</code>. Detalhe do código do slide: essa trigger <b>não tem condição</b>, então dispara em <b>qualquer</b> UPDATE de <code>funcionario</code>, mesmo que ele não mude as habilidades.</p>
  <h3>Exercício 3 do slide: auditar só mudança de nome de projeto (a solução é complemento)</h3>
  <p>A solução usa uma condição para disparar só quando o nome muda (no MySQL, <code>IF OLD.nome &lt;&gt; NEW.nome</code> dentro de <code>BEGIN...END</code>; no SQLite, <code>WHEN</code> no cabeçalho). Mude o nome do projeto 1 e depois só a descrição do 2, e veja que só a primeira mudança é registrada:</p>
''' + sqlbox("alpha", """CREATE TABLE ProjetoAuditoria (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome_antigo TEXT, nome_novo TEXT, usuario TEXT, data DATE
);
CREATE TRIGGER trg_projeto_nome
BEFORE UPDATE ON Projeto
FOR EACH ROW WHEN OLD.nome <> NEW.nome
BEGIN
  INSERT INTO ProjetoAuditoria (nome_antigo, nome_novo, usuario, data)
  VALUES (OLD.nome, NEW.nome, 'estudante', date('now'));
END;

UPDATE Projeto SET nome = 'Omega 2' WHERE idProjeto = 1;
UPDATE Projeto SET descricao = 'novo texto' WHERE idProjeto = 2;
SELECT * FROM ProjetoAuditoria;""", "Só auditar quando o nome muda", expect=1) + '''
  <div class="nota cuidado"><span class="lbl">Complemento: BEFORE ou AFTER?</span><b>BEFORE</b> roda antes de gravar, então serve para <b>validar ou ajustar</b> o dado que vai entrar (e até impedir a operação). <b>AFTER</b> roda depois de gravar, e serve para <b>reagir</b> ao que já aconteceu (auditoria, atualizar totais). Triggers também escondem lógica: quem lê só o <code>UPDATE</code> não vê o que ela faz, e muitas triggers encadeadas dificultam o diagnóstico.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>View</b>: consulta salva, usada como tabela. Não guarda dados.",
    "<b>Function</b>: devolve um valor (<code>RETURN</code>) e se usa dentro de um SELECT.",
    "<b>Procedure</b>: comandos guardados, chamada com <code>CALL</code>, sem RETURN.",
    "<b>Trigger</b>: dispara sozinha num INSERT, UPDATE ou DELETE. <code>OLD</code> é o valor antes; <code>NEW</code>, o depois.",
    "<b>DELIMITER</b> troca o fim de comando para que os <code>;</code> do corpo não cortem a criação.",
    "O nome de um objeto <b>não garante</b> o que ele faz: leia o código."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual objeto você usaria para registrar automaticamente quem mudou um dado?", [("a","View"),("b","Function"),("c","Trigger")], "Só a trigger dispara por conta própria quando o evento acontece. View e function precisam ser chamadas.") + quiz(2, "a", "Para que serve o DELIMITER ao criar uma function?", [("a","Trocar o terminador de comando, para os ; do corpo não encerrarem a criação."),("b","Delimitar o intervalo de datas da função."),("c","Limitar quantas linhas a função devolve.")], "O cliente corta no primeiro ponto e vírgula. Trocando o delimitador para // ou $$, o BEGIN...END chega inteiro ao servidor.") + quiz(3, "b", "Numa trigger BEFORE UPDATE, OLD.habilidades é:", [("a","O novo valor, que vai ser gravado."),("b","O valor que a coluna tinha antes da alteração."),("c","Sempre NULL.")], "OLD é a linha como estava; NEW é como vai ficar.") + flash([
    ("View guarda dados?", "Não. Guarda a consulta, que roda de novo a cada uso."),
    ("Function x procedure?", "Function devolve um valor e vai dentro de um SELECT. Procedure é chamada com CALL e não tem RETURN."),
    ("O que é FOR EACH ROW?", "A trigger roda uma vez para cada linha afetada pelo comando."),
    ("OLD e NEW?", "OLD: a linha antes da mudança (UPDATE, DELETE). NEW: a linha depois (INSERT, UPDATE).")]) + ponte("Tenho o essencial de SQL. O que separa um banco que funciona de um que funciona bem?", "Índices, transações, subconsultas e segurança. É o complemento final.", "Para onde vamos agora · Capítulo 8") + '''
</section>'''
chapter("banco-de-dados", 7, "views-procedures-triggers", T, "Programando no banco", "Capítulo 7 · Aula 7",
        "Guardar código dentro do banco para reaproveitar: views, functions, procedures e triggers.",
        ["<b>~40 min</b>", "6 demos · 3 testes · 4 flashcards", "SQL executável"], body7, scripts=S, sql=True)

# ---------------- CAP 8 ----------------
body8 = recap("Ao longo dos capítulos 1 a 7 você viu o essencial: modelar, criar, manipular, resumir, juntar e programar o banco. Este último capítulo é <b>complemento</b>: não foi dado em aula, mas é o que separa quem sabe escrever SQL de quem sabe construir sistemas confiáveis. Tudo aqui é conhecimento geral de bancos de dados, e os exemplos rodam de verdade.", "Onde paramos") + '''

<section class="sec" id="indices">
  <h2><span class="sn">1</span>Índices: a diferença entre achar e procurar</h2>
  <p class="gancho">Por que o slide dizia que o SGBD é bom em buscas rápidas?</p>
  <p>Sem índice, para achar o funcionário "Ana" o banco lê a tabela <b>inteira</b>, linha por linha (<i>full scan</i>). Com um <b>índice</b> (normalmente uma <b>B-tree</b>, uma árvore balanceada ordenada pela coluna), ele desce a árvore em poucos passos, como achar uma palavra num dicionário aberto no meio. O custo da busca passa de proporcional ao tamanho da tabela para proporcional ao <i>logaritmo</i> dele.</p>
  <p>Peça ao banco para mostrar o <b>plano</b> de execução (<code>EXPLAIN</code>) antes e depois de criar um índice:</p>
''' + sqlbox("alpha", """EXPLAIN QUERY PLAN SELECT * FROM Funcionario WHERE nome = 'Ana';
CREATE INDEX idx_func_nome ON Funcionario(nome);
EXPLAIN QUERY PLAN SELECT * FROM Funcionario WHERE nome = 'Ana';
EXPLAIN QUERY PLAN SELECT * FROM Funcionario WHERE nome LIKE '%na';""", "Antes e depois do índice") + '''
  <p>Leia os três planos: o primeiro diz <b>SCAN</b> (lê tudo), o segundo diz <b>SEARCH ... USING INDEX</b> (desce a árvore) e o terceiro volta a <b>SCAN</b>, porque <code>LIKE '%na'</code> começa com curinga e o índice, ordenado pelo começo do texto, não ajuda. (No MySQL o comando é <code>EXPLAIN SELECT ...</code>, com uma saída mais detalhada.)</p>
  <div class="tablewrap"><table>
    <tr><th>Índices ajudam</th><th>Índices custam</th></tr>
    <tr><td>leituras com <code>WHERE</code>, <code>JOIN</code> e <code>ORDER BY</code> sobre a coluna indexada</td><td>espaço em disco, e cada <code>INSERT</code>, <code>UPDATE</code> e <code>DELETE</code> precisa atualizar o índice (escritas ficam mais lentas)</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Lembra</span>PK e <code>UNIQUE</code> já criam índice automaticamente. Indexe as colunas que você <b>de fato filtra e junta</b>, e não todas. Colunas com poucos valores distintos (como sexo) ajudam pouco.</div>
</section>

<section class="sec" id="transacoes">
  <h2><span class="sn">2</span>Transações e ACID</h2>
  <p class="gancho">Transferir dinheiro são dois UPDATEs. E se o segundo falhar?</p>
  <p>Uma <b>transação</b> agrupa comandos que devem acontecer <b>todos ou nenhum</b>. Se algo dá errado no meio, o <code>ROLLBACK</code> desfaz tudo; se está tudo certo, o <code>COMMIT</code> confirma. As propriedades que um SGBD confiável garante se chamam <b>ACID</b>:</p>
  <div class="grid2">
    <div class="card rv"><b>A</b>tomicidade<p>Tudo ou nada.</p></div>
    <div class="card rv"><b>C</b>onsistência<p>O banco sai de um estado válido para outro estado válido (respeitando as regras).</p></div>
    <div class="card rv"><b>I</b>solamento<p>Transações simultâneas não enxergam o meio uma da outra.</p></div>
    <div class="card rv"><b>D</b>urabilidade<p>O que foi confirmado (<code>COMMIT</code>) sobrevive a uma falha.</p></div>
  </div>
''' + sqlbox("vazia", """CREATE TABLE conta (id INTEGER PRIMARY KEY, dono TEXT, saldo REAL);
INSERT INTO conta VALUES (1, 'Ana', 100), (2, 'Bia', 50);

BEGIN;
UPDATE conta SET saldo = saldo - 80 WHERE id = 1;   -- debita a Ana
SELECT dono, saldo FROM conta;                       -- no meio da transação
ROLLBACK;                                            -- desiste: desfaz tudo
SELECT dono, saldo FROM conta;                       -- como se nada tivesse acontecido""", "Transferência desfeita com ROLLBACK") + '''
  <p>Dentro da transação a Ana ficou com 20; depois do <code>ROLLBACK</code> voltou a ter 100. Num sistema real, o segundo passo (creditar a Bia) viria antes do <code>COMMIT</code>, e uma falha entre os dois jamais deixaria o dinheiro "sumido".</p>
</section>

<section class="sec" id="subconsultas">
  <h2><span class="sn">3</span>Subconsultas, CTE e funções de janela</h2>
  <p class="gancho">Quando uma consulta precisa da resposta de outra.</p>
  <p>Uma <b>subconsulta</b> é um SELECT dentro de outro. Quais alocações têm mais horas que a <b>média geral</b>? A média precisa ser calculada antes:</p>
''' + sqlbox("alpha", "SELECT idFuncionario, idProjeto, horas\nFROM ProjetoFuncionario\nWHERE horas > (SELECT AVG(horas) FROM ProjetoFuncionario);", "Alocações acima da média (6,33)", expect=9) + '''
  <p>Quando a consulta fica longa, uma <b>CTE</b> (<code>WITH</code>) dá nome a cada etapa e deixa o código legível. Quem soma mais de 10 horas no total?</p>
''' + sqlbox("alpha", "WITH total AS (\n  SELECT idFuncionario, SUM(horas) AS h\n  FROM ProjetoFuncionario\n  GROUP BY idFuncionario\n)\nSELECT f.nome, t.h\nFROM total t JOIN Funcionario f ON f.idFuncionario = t.idFuncionario\nWHERE t.h > 10;", "Consulta em etapas, com CTE", expect=1) + '''
  <p>E as <b>funções de janela</b> (<code>RANK() OVER (...)</code>) calculam sobre um conjunto de linhas sem colapsá-las como o GROUP BY faz. Disponíveis no MySQL 8 e no SQLite moderno:</p>
''' + sqlbox("alpha", "SELECT f.nome, pf.horas,\n       RANK() OVER (ORDER BY pf.horas DESC) AS posicao\nFROM ProjetoFuncionario pf\nJOIN Funcionario f ON f.idFuncionario = pf.idFuncionario\nORDER BY posicao, f.nome;", "Ranking sem agrupar") + '''
</section>

<section class="sec" id="injecao">
  <h2><span class="sn">4</span>Injeção de SQL: o ataque que mais derruba sistemas</h2>
  <p class="gancho">O erro de montar SQL com texto que veio do usuário.</p>
  <p>Se o programa monta a consulta <b>colando</b> o que o usuário digitou dentro do texto SQL, o usuário pode digitar <i>pedaços de SQL</i>. Brinque com a tela de busca abaixo: ela roda de verdade sobre a base alpha. Primeiro com um nome normal, depois com os botões de ataque. Por fim, marque "consulta parametrizada".</p>
  <div class="demo" data-demo="inject"></div>
  <p>A defesa é <b>nunca concatenar</b>. Em vez disso, use <b>consultas parametrizadas</b> (<i>prepared statements</i>): o SQL é fixo, com um marcador (<code>?</code>), e o valor viaja à parte, sempre tratado como <b>dado</b>, nunca como código. É assim em qualquer linguagem. Também vale dar ao usuário do banco da aplicação o <b>mínimo de permissões</b> (se ele não pode fazer <code>DROP</code>, o ataque do botão três falha de qualquer jeito). Esse ataque aparece no catálogo de ameaças da apostila de Cibersegurança.</p>
</section>

<section class="sec" id="nosql">
  <h2><span class="sn">5</span>E o NoSQL? Quando usar</h2>
  <p class="gancho">O slide de panorama citava documentos, chave-valor, grafos e colunas. O que cada um resolve?</p>
  <div class="tablewrap"><table>
    <tr><th>Tipo</th><th>Ideia</th><th>Bom para</th><th>Exemplos</th></tr>
    <tr><td><b>Documento</b></td><td>registros em JSON, com estrutura flexível</td><td>catálogos, conteúdo, dados que mudam de formato</td><td>MongoDB</td></tr>
    <tr><td><b>Chave-valor</b></td><td>um dicionário gigante: chave aponta para um valor</td><td>cache, sessão de usuário, filas simples</td><td>Redis</td></tr>
    <tr><td><b>Colunas</b></td><td>dados organizados por coluna, distribuídos em muitos servidores</td><td>volumes enormes de escrita, séries de tempo</td><td>Cassandra</td></tr>
    <tr><td><b>Grafo</b></td><td>nós e arestas como cidadãos de primeira classe</td><td>redes sociais, recomendação, caminhos</td><td>Neo4j</td></tr>
  </table></div>
  <p>A escolha é um <b>trade-off</b>: bancos NoSQL costumam trocar parte das garantias de consistência e dos JOINs por escala horizontal e flexibilidade. Para a maioria dos sistemas de negócio (cadastros, pedidos, finanças), o <b>relacional continua sendo a escolha segura</b>. E muitos sistemas usam os dois: o relacional como fonte da verdade e o NoSQL (como o Redis) para acelerar.</p>
  <div class="nota exemplo"><span class="lbl">Ligação com a nuvem</span>Na apostila de AWS você vai encontrar o <b>RDS</b>, que roda MySQL gerenciado pela AWS, e o <b>S3</b>. É nesse tipo de serviço que o banco desta disciplina vai morar em produção.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento da apostila</h2>
  ''' + resumo([
    "<b>Índice</b> (B-tree) acelera leituras e atrasa escritas. <code>LIKE '%x'</code> não usa índice. Confira com <code>EXPLAIN</code>.",
    "<b>Transação</b>: tudo ou nada (<code>COMMIT</code>/<code>ROLLBACK</code>). <b>ACID</b>: atomicidade, consistência, isolamento, durabilidade.",
    "<b>Subconsulta</b>, <b>CTE</b> (<code>WITH</code>) e <b>funções de janela</b> organizam consultas complexas.",
    "<b>Injeção de SQL</b>: nunca concatene entrada do usuário. Use <b>consultas parametrizadas</b> e permissões mínimas.",
    "<b>NoSQL</b> é trade-off (flexibilidade e escala x garantias). O relacional segue sendo o padrão para dados de negócio."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que a consulta <code>WHERE nome LIKE '%na'</code> não se beneficia de um índice em <code>nome</code>?", [("a","Porque LIKE não é permitido com índices."),("b","Porque o índice é ordenado pelo começo do texto, e o padrão começa com curinga."),("c","Porque o índice só funciona com números.")], "O índice B-tree ordena pelo início do valor. Com o curinga na frente, o banco não sabe por onde começar e lê tudo.") + quiz(2, "c", "A melhor defesa contra injeção de SQL é:", [("a","Esconder os nomes das tabelas."),("b","Pedir ao usuário que não digite aspas."),("c","Consultas parametrizadas, que tratam a entrada sempre como dado.")], "Filtros de caracteres falham. Parametrizar separa definitivamente o código (SQL) do dado (o que o usuário digitou).") + quiz(3, "a", "Numa transferência bancária, o que a atomicidade garante?", [("a","Ou o débito e o crédito acontecem juntos, ou nenhum acontece."),("b","Que o dinheiro nunca falte."),("c","Que a operação seja a mais rápida possível.")], "Atomicidade é 'tudo ou nada'. Foi o que o ROLLBACK mostrou.") + flash([
    ("O que é um índice B-tree?", "Uma árvore ordenada que permite achar valores em poucos passos, sem ler a tabela inteira."),
    ("O que é uma CTE?", "Uma consulta com nome (WITH), usada para dividir uma consulta grande em etapas."),
    ("O que significa ACID?", "Atomicidade, Consistência, Isolamento e Durabilidade."),
    ("Quando preferir NoSQL?", "Quando flexibilidade de formato ou escala horizontal pesam mais do que JOINs e garantias fortes.")]) + '''
  <div class="ponte rv"><div class="t">E agora?</div><div class="q">Você percorreu a história inteira da startup alpha.</div><p>Da modelagem ao banco que reage sozinho. Volte à <a href="index.html">visão geral</a> e refaça os exercícios sem olhar. E leve esse conhecimento para a nuvem, na apostila de AWS.</p></div>
</section>'''
chapter("banco-de-dados", 8, "alem-do-basico", T, "Para ir além (complemento)", "Capítulo 8 · Complemento",
        "O que separa um banco que funciona de um que funciona bem: índices, transações, segurança e outros modelos.",
        ["<b>~40 min</b>", "6 demos · 3 testes · 4 flashcards", "complemento, não foi dado em aula"], body8, scripts=S + ["demos/cap-8.js"], sql=True)
print("caps 7-8 ok")
