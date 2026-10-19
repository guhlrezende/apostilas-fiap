from bld import *
T = "Bancos de Dados e SQL"
S = ["bases.js"]

# ---------------- CAP 3: DDL ----------------
body3 = recap("No Capítulo 2 você desenhou a startup alpha: funcionário e projeto em N:N, projeto ligado a um único programa. Mas era um desenho. Falta transformar isso em <b>tabelas com tipos de dados, chaves e regras</b> que o banco faça valer sozinho. É o modelo lógico e a DDL.") + '''

<section class="sec" id="cenario">
  <h2><span class="sn">1</span>Três problemas concretos</h2>
  <p class="gancho">Desenhar é fácil. Impedir que alguém grave lixo é outra história.</p>
  <p>A alpha precisa alocar funcionários em projetos e pagar por hora trabalhada. Isso levanta três perguntas que toda modelagem lógica responde:</p>
  <ol>
    <li><b>Que tipo de dado</b> cada campo deve ter (data, número, texto)?</li>
    <li><b>Como garantir</b> que ninguém insira dado inválido (funcionário sem CPF, projeto sem data)?</li>
    <li><b>Como criar</b> de fato as tabelas?</li>
  </ol>
  <p>A grande ideia da aula: <mark class="hl">as regras de negócio podem morar no próprio banco</mark>, e não só na aplicação. Assim nenhum programa, nem um script mal escrito, nem um acesso direto consegue burlá-las.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Quais são essas regras que o banco sabe impor?</div><p>As restrições (constraints), e duas chaves que sustentam o relacionamento entre tabelas.</p></div>
</section>

<section class="sec" id="chaves">
  <h2><span class="sn">2</span>Chaves e restrições</h2>
  <p class="gancho">PK, FK e cinco regras que cabem numa linha cada.</p>
  <div class="grid2">
    <div class="card rv"><b>Chave primária (PK)</b><p>Identifica <b>unicamente</b> cada registro da própria tabela. Só existe uma por tabela, mas pode ser <b>composta</b> por mais de uma coluna, como <code>PRIMARY KEY (idProjeto, idFuncionario)</code> na tabela associativa.</p></div>
    <div class="card rv"><b>Chave estrangeira (FK)</b><p>É uma coluna que <b>referencia a PK de outra tabela</b>. É o mecanismo do relacionamento: impede, por exemplo, uma alocação para um projeto que não existe. Isso se chama <b>integridade referencial</b>.</p></div>
  </div>
  <div class="tablewrap"><table>
    <tr><th>Restrição</th><th>Resolve o problema de...</th><th>Exemplo</th></tr>
    <tr><td><code>NOT NULL</code></td><td>campo obrigatório ficar vazio</td><td><code>nome VARCHAR(50) NOT NULL</code></td></tr>
    <tr><td><code>DEFAULT</code></td><td>ter um valor sensato quando nada é informado</td><td><code>pais VARCHAR(30) DEFAULT 'Brasil'</code></td></tr>
    <tr><td><code>UNIQUE</code></td><td>duplicidade (dois clientes com o mesmo CPF)</td><td><code>CPF CHAR(11) UNIQUE</code></td></tr>
    <tr><td><code>CHECK</code></td><td>limitar o intervalo aceitável</td><td><code>CHECK (idade &gt;= 18)</code></td></tr>
    <tr><td><code>AUTO_INCREMENT</code></td><td>gerar identificadores sem controle manual</td><td><code>idFuncionario INT AUTO_INCREMENT</code></td></tr>
  </table></div>
  <p>Teste as regras de verdade. Rode o script, depois tente quebrar cada uma: repita o <code>INSERT</code> com o mesmo CPF, ponha <code>idade</code> 15, ou deixe o CPF de fora.</p>
''' + sqlbox("vazia", """CREATE TABLE cliente (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  cpf   CHAR(11) NOT NULL UNIQUE,
  idade INT CHECK (idade >= 18),
  pais  VARCHAR(30) DEFAULT 'Brasil'
);
INSERT INTO cliente (cpf, idade) VALUES ('11111111111', 30);
SELECT * FROM cliente;""", "Restrições em ação") + '''
  <div class="nota cuidado"><span class="lbl">Cuidado: SQLite x MySQL</span>O navegador roda <b>SQLite</b>. Nele a chave automática se escreve <code>INTEGER PRIMARY KEY AUTOINCREMENT</code>; no MySQL, <code>INT NOT NULL AUTO_INCREMENT</code>. O resto (NOT NULL, UNIQUE, CHECK, DEFAULT, FOREIGN KEY) é igual. No MySQL, o <code>CHECK</code> só passou a ser realmente aplicado a partir da versão 8.0.16.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E os tipos de dados? Qual escolher para cada coluna?</div><p>A escolha muda o espaço usado e o que o banco aceita.</p></div>
</section>

<section class="sec" id="tipos">
  <h2><span class="sn">3</span>Tipos de dados</h2>
  <p class="gancho">Tudo cabe em texto. Por que não usar só VARCHAR?</p>
  <p>Porque o tipo define <b>quanto espaço</b> o dado usa e <b>que operações</b> fazem sentido (somar datas, comparar números). No MySQL, os principais:</p>
  <div class="tablewrap"><table>
    <tr><th>Grupo</th><th>Tipos</th><th>Observação</th></tr>
    <tr><td><b>Inteiros</b></td><td><code>TINYINT</code> (1 byte), <code>SMALLINT</code> (2), <code>MEDIUMINT</code> (3), <code>INT</code> (4), <code>BIGINT</code> (8)</td><td><code>TINYINT</code> vai de -128 a 127 (ou 0 a 255 sem sinal). Por isso <code>horas</code> na alpha é <code>tinyint</code>: cabe de sobra.</td></tr>
    <tr><td><b>Decimais</b></td><td><code>FLOAT</code>, <code>DECIMAL</code>, <code>NUMERIC</code></td><td><code>DECIMAL(10,2)</code> é o padrão para dinheiro (exato, sem erro de arredondamento binário).</td></tr>
    <tr><td><b>Data e hora</b></td><td><code>DATE</code>, <code>TIME</code>, <code>DATETIME</code>, <code>TIMESTAMP</code>, <code>YEAR</code></td><td>No MySQL 8 o modo padrão recusa datas "zeradas" como <code>0000-00-00</code>.</td></tr>
    <tr><td><b>Texto</b></td><td><code>CHAR(n)</code>, <code>VARCHAR(n)</code>, <code>TEXT</code></td><td>Veja a comparação abaixo.</td></tr>
  </table></div>
  <h3>CHAR x VARCHAR</h3>
  <p><code>CHAR(4)</code> sempre ocupa 4 bytes (completa com espaços). <code>VARCHAR(4)</code> ocupa o tamanho do texto <b>mais 1 byte</b>. Por isso <code>VARCHAR</code> é melhor para textos de tamanho variável, e <code>CHAR</code> para valores de tamanho fixo (CPF de 11 dígitos, sigla de estado).</p>
  <div class="tablewrap"><table>
    <tr><th>Valor</th><th class="n">CHAR(4)</th><th class="n">VARCHAR(4)</th></tr>
    <tr><td><code>''</code> (vazio)</td><td class="n">4 bytes</td><td class="n">1 byte</td></tr>
    <tr><td><code>'ab'</code></td><td class="n">4 bytes</td><td class="n">3 bytes</td></tr>
    <tr><td><code>'abcd'</code></td><td class="n">4 bytes</td><td class="n">5 bytes</td></tr>
  </table></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Com tipos e regras na cabeça, como se escreve a tabela inteira?</div><p>Com <code>CREATE</code>, e depois <code>ALTER</code> quando a estrutura precisar mudar.</p></div>
</section>

<section class="sec" id="ddl">
  <h2><span class="sn">4</span>DDL: criar e alterar a estrutura</h2>
  <p class="gancho">DDL define a estrutura. DML mexe nos dados. Não confunda.</p>
  <div class="grid2">
    <div class="card rv"><b>DDL</b> (Data Definition Language)<p>Define a <b>estrutura</b>: <code>CREATE</code>, <code>ALTER</code>, <code>DROP</code>. Usada uma vez, ou quando a estrutura muda.</p></div>
    <div class="card rv"><b>DML</b> (Data Manipulation Language)<p>Manipula os <b>dados dentro</b> da estrutura: <code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>, <code>SELECT</code>. É o que você usa o tempo todo. (Capítulo 4.)</p></div>
  </div>
  <p>Este é o DDL da alpha, a versão corrigida do que o slide mostra. A tabela do meio é a associativa do N:N, com PK composta e duas FKs:</p>
''' + sqlbox("vazia", """CREATE TABLE Projeto (
  idProjeto INTEGER PRIMARY KEY AUTOINCREMENT,
  sigla     VARCHAR(10) NOT NULL,
  dtInicio  DATE,
  dtTermino DATE
);
CREATE TABLE Funcionario (
  idFuncionario INTEGER PRIMARY KEY AUTOINCREMENT,
  CPF           VARCHAR(11) NOT NULL UNIQUE,
  nome          VARCHAR(50) NOT NULL,
  sobrenome     VARCHAR(50) NOT NULL,
  email         VARCHAR(50),
  habilidades   TEXT
);
CREATE TABLE ProjetoFuncionario (
  idProjeto     INT NOT NULL,
  idFuncionario INT NOT NULL,
  horas         INT,
  dtInicio      DATE,
  dtTermino     DATE,
  ativo         INT,
  PRIMARY KEY (idProjeto, idFuncionario),
  FOREIGN KEY (idProjeto)     REFERENCES Projeto(idProjeto),
  FOREIGN KEY (idFuncionario) REFERENCES Funcionario(idFuncionario)
);
SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';""", "Criando as três tabelas", expect=3) + '''
  <div class="tablewrap"><table>
    <tr><th>Em MySQL</th><th>Para quê</th><th>No navegador (SQLite)</th></tr>
    <tr><td><code>CREATE DATABASE alpha;</code> e <code>USE alpha;</code></td><td>criar e escolher a base (<code>SCHEMA</code> é sinônimo de <code>DATABASE</code>)</td><td>não existe: cada base é um arquivo</td></tr>
    <tr><td><code>SHOW TABLES;</code></td><td>listar as tabelas</td><td><code>SELECT name FROM sqlite_master WHERE type='table';</code></td></tr>
    <tr><td><code>DESC Projeto;</code></td><td>mostrar as colunas de <b>uma</b> tabela</td><td><code>PRAGMA table_info(Projeto);</code></td></tr>
    <tr><td><code>ALTER TABLE T ADD coluna ...;</code></td><td>acrescentar coluna no fim</td><td>igual</td></tr>
    <tr><td><code>ALTER TABLE T MODIFY COLUMN c ...;</code></td><td>mudar o tipo de uma coluna</td><td>não existe no SQLite</td></tr>
    <tr><td><code>ALTER TABLE T DROP COLUMN c;</code></td><td>remover coluna (e os dados dela)</td><td>igual (a partir da versão 3.35)</td></tr>
  </table></div>

  <h3>Integridade referencial na prática</h3>
  <p>Agora uma base com as FKs declaradas. Tente apagar um projeto que tem alocações, e depois alocar alguém que não existe:</p>
''' + sqlbox("alpha_fk", """-- 1) apagar um projeto que tem alocações
DELETE FROM Projeto WHERE idProjeto = 3;""", "FK bloqueando um DELETE") + sqlbox("alpha_fk", """-- 2) alocar um funcionário que não existe
INSERT INTO ProjetoFuncionario (idFuncionario, idProjeto, ativo, horas) VALUES (999, 1, 1, 4);""", "FK bloqueando um INSERT") + '''
  <p>No MySQL as mensagens são <code>ERROR 1451</code> (não dá para apagar a linha-pai) e <code>ERROR 1452</code> (a linha-pai não existe). O banco defendeu a consistência sem você escrever uma linha de validação.</p>

  <h3>As pegadinhas do slide (para você não cair)</h3>
  <div class="tablewrap"><table>
    <tr><th>No slide</th><th>O problema</th><th>O certo</th></tr>
    <tr><td><code>idFuncionario NOT NULL,</code></td><td>faltou o tipo: dá erro de sintaxe</td><td><code>idFuncionario INT NOT NULL,</code></td></tr>
    <tr><td><code>CREATE SCHEMA ALPHA AUTHORIZATION 'JSilva';</code></td><td><code>AUTHORIZATION</code> é do SQL padrão e do SQL Server, e não existe no MySQL</td><td><code>CREATE DATABASE ALPHA;</code></td></tr>
    <tr><td><code>dtFim</code> num slide e <code>dtTermino</code> em outro</td><td>a mesma tabela com colunas diferentes</td><td>fique com <code>dtTermino</code>, como o resto do material</td></tr>
    <tr><td>tabela <code>Funcionario</code> sem <code>sobrenome</code></td><td>os <code>INSERT</code> da aula seguinte usam <code>sobrenome</code> e dão erro de coluna desconhecida</td><td><code>ALTER TABLE Funcionario ADD sobrenome VARCHAR(50) NOT NULL;</code></td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Complemento: CHECK ou TRIGGER?</span>As duas impõem regras, mas de jeitos diferentes. O <b>CHECK</b> é declarativo e olha só a própria linha ("idade &gt;= 18"). Já o <b>trigger</b> (Capítulo 7) é imperativo: pode consultar outras tabelas e ter efeitos colaterais, mas é mais difícil de manter. A regra prática: use CHECK quando der, e trigger só quando o CHECK não alcançar.</div>
  <div class="nota cuidado"><span class="lbl">Complemento: AUTO_INCREMENT exposto</span>Usar o número sequencial como identificador visível numa API (<code>/cliente/17</code>) deixa o sistema previsível: quem vê o 17 tenta o 18, e se faltar checagem de permissão acessa dados alheios. Em APIs públicas se costuma expor um identificador aleatório (como UUID) e guardar o sequencial só por dentro.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Modelo lógico</b> define como os dados são guardados: tabelas, tipos, chaves e relacionamentos.",
    "<b>PK</b> identifica a linha (pode ser composta). <b>FK</b> referencia a PK de outra tabela e garante a integridade referencial.",
    "<b>Restrições:</b> NOT NULL, DEFAULT, UNIQUE, CHECK e AUTO_INCREMENT. Regras no banco ninguém burla.",
    "<b>DDL</b> = estrutura (CREATE, ALTER, DROP). <b>DML</b> = dados (INSERT, UPDATE, DELETE, SELECT).",
    "<b>CHAR</b> tem tamanho fixo; <b>VARCHAR</b> ocupa o tamanho do texto mais 1 byte.",
    "N:N vira <b>tabela associativa</b> com PK composta e duas FKs."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Para que serve uma chave estrangeira?", [("a","Para deixar a consulta mais rápida, apenas."),("b","Para identificar unicamente a linha da própria tabela."),("c","Para referenciar a PK de outra tabela e impedir ligações com linhas inexistentes.")], "A identificação única é papel da PK. A FK cria o relacionamento e protege a integridade referencial (as mensagens 1451 e 1452 do MySQL).") + quiz(2, "a", "Por que a PK da tabela ProjetoFuncionario é composta por (idProjeto, idFuncionario)?", [("a","Porque cada par funcionário-projeto deve aparecer uma só vez, mesmo que cada id se repita em outras linhas."),("b","Porque o MySQL não aceita PK simples em tabela associativa."),("c","Para economizar espaço em disco.")], "Um funcionário está em vários projetos e um projeto tem vários funcionários, então nenhum id sozinho é único. O par é.") + quiz(3, "b", "Qual comando é DDL?", [("a","UPDATE Funcionario SET nome = 'Ana';"),("b","ALTER TABLE Funcionario ADD sobrenome VARCHAR(50);"),("c","INSERT INTO Funcionario VALUES (...);")], "ALTER muda a estrutura (DDL). UPDATE e INSERT manipulam os dados (DML).") + flash([
    ("Por que pôr regra no banco?", "Porque nenhuma aplicação ou script consegue burlar uma regra que o próprio banco impõe."),
    ("CHAR(4) x VARCHAR(4)?", "CHAR sempre ocupa 4 bytes. VARCHAR ocupa o tamanho do texto mais 1 byte."),
    ("O que é tabela associativa?", "A tabela do meio de um N:N: PK composta pelas duas chaves e, se preciso, dados do relacionamento."),
    ("DDL x DML?", "DDL cria e altera a estrutura. DML lê e altera os dados dentro dela.")]) + ponte("As tabelas existem, mas estão vazias. Como coloco, procuro e mudo os dados?", "Com a DML: INSERT, SELECT, UPDATE e DELETE, o CRUD inteiro.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter("banco-de-dados", 3, "modelo-logico-ddl", T, "Modelo lógico e DDL", "Capítulo 3 · Aula 3",
        "Transformar o desenho em tabelas, com tipos, chaves e regras que o próprio banco faz valer.",
        ["<b>~40 min</b>", "4 demos · 3 testes · 4 flashcards", "SQL executável"], body3, scripts=S, sql=True)

# ---------------- CAP 4: DML ----------------
body4 = recap("No Capítulo 3 você criou as tabelas da alpha com PK, FK e restrições, e viu o banco recusar dados inválidos. Só que a estrutura estava <b>vazia</b>. Agora a startup precisa incluir funcionários, achar quem tem certas habilidades, mudar dados e filtrar projetos por período.") + '''

<section class="sec" id="crud">
  <h2><span class="sn">1</span>CRUD: as quatro operações</h2>
  <p class="gancho">Quatro verbos resolvem quase todo sistema.</p>
  <p><b>DML</b> (Data Manipulation Language) é a parte do SQL que altera e consulta os <b>dados</b>. Todo o <b>CRUD</b> sai dela:</p>
  <div class="tablewrap"><table>
    <tr><th>CRUD</th><th>Comando</th><th>Faz</th></tr>
    <tr><td><b>C</b>reate</td><td><code>INSERT</code></td><td>inclui uma linha</td></tr>
    <tr><td><b>R</b>ead</td><td><code>SELECT</code></td><td>consulta (o slide escreve "Request", o nome comum é <i>Read</i>)</td></tr>
    <tr><td><b>U</b>pdate</td><td><code>UPDATE</code></td><td>altera linhas existentes</td></tr>
    <tr><td><b>D</b>elete</td><td><code>DELETE</code></td><td>exclui linhas</td></tr>
  </table></div>
  <p>As quatro perguntas da aula, e a resposta de cada uma: <i>incluir e consultar funcionários</i> (<code>INSERT</code> e <code>SELECT</code>); <i>filtrar por habilidades</i> (<code>WHERE</code> com <code>LIKE</code>, <code>AND</code>, <code>OR</code>); <i>atualizar habilidades</i> (<code>UPDATE</code>); <i>filtrar projetos por período</i> (<code>BETWEEN</code>).</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: SQLite x MySQL</span>Os exemplos rodam no navegador (SQLite). Três diferenças aparecem neste capítulo: <code>NOW()</code> vira <code>datetime('now')</code>, <code>CONCAT(a, b)</code> vira <code>a || b</code>, e <code>DATE_SUB(d, INTERVAL 35 DAY)</code> vira <code>date(d, '-35 day')</code>. O resto (INSERT, SELECT, WHERE, LIKE, BETWEEN) é igual.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Como entra o primeiro funcionário?</div><p>Com um INSERT, e o banco vai conferir cada regra do Capítulo 3.</p></div>
</section>

<section class="sec" id="insert">
  <h2><span class="sn">2</span>INSERT: incluir</h2>
  <p class="gancho">Você diz em que colunas e com que valores. O resto o banco completa.</p>
  <div class="formula">INSERT INTO tabela (coluna1, coluna2, ...) VALUES (valor1, valor2, ...);</div>
  <p>O <code>idFuncionario</code> não aparece na lista: o <code>AUTO_INCREMENT</code> gera sozinho. Rode e depois tente inserir uma segunda pessoa com <b>o mesmo CPF</b> (como faz o slide):</p>
''' + sqlbox("alpha", """INSERT INTO Funcionario (CPF, nome, sobrenome, habilidades, email)
VALUES ('98765432110', 'Luana', 'Santos', 'python, sql, aws', 'luana@email.com');
SELECT idFuncionario, nome FROM Funcionario WHERE CPF = '98765432110';""", "Incluindo a Luana", expect=1) + sqlbox("alpha", """INSERT INTO Funcionario (CPF, nome, sobrenome, habilidades, email)
VALUES ('12345678901', 'Alice', 'Pereira', 'python, sql, aws, mongodb', 'alice@email.com');""", "O mesmo CPF de outra pessoa") + '''
  <p>O banco recusou por causa do <code>UNIQUE</code> do CPF (no MySQL: <code>ERROR 1062 Duplicate entry</code>). No slide, o segundo INSERT repete o CPF da Luana de propósito, ou por descuido, e também usa uma <b>aspa tipográfica</b> (<code>’</code>) no lugar da aspa simples, o que dá erro de sintaxe antes mesmo da checagem. <b>Cuidado ao copiar código de slide.</b></p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Os dados entraram. Como leio só o que me interessa?</div><p>Com SELECT, e as cláusulas que filtram, ordenam e limitam.</p></div>
</section>

<section class="sec" id="select">
  <h2><span class="sn">3</span>SELECT: consultar, filtrar, ordenar</h2>
  <p class="gancho">Quais colunas, de quais tabelas, sob quais condições.</p>
  <div class="formula">SELECT colunas FROM tabelas WHERE condição ORDER BY coluna LIMIT n;</div>
  <ul>
    <li><code>*</code> traz todas as colunas.</li>
    <li><code>WHERE</code> filtra as <b>linhas</b>.</li>
    <li><code>ORDER BY</code> ordena. O padrão é crescente (<code>ASC</code>); <code>DESC</code> inverte.</li>
    <li><code>LIMIT n</code> corta o resultado em <i>n</i> linhas.</li>
  </ul>
''' + sqlbox("alpha", "SELECT nome, sobrenome FROM Funcionario ORDER BY sobrenome DESC LIMIT 3;", "Os três últimos sobrenomes (de Z a A)") + '''
  <p>O resultado traz Camila <b>Teixeira</b>, Rodrigo <b>Tavares</b> e Carlos <b>Souza</b>.</p>
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Achar que <code>LIMIT 1</code> devolve "o primeiro".</b> Sem <code>ORDER BY</code>, o SQL <b>não garante</b> ordem nenhuma. Na prática o MySQL costuma devolver pela chave primária, mas isso é detalhe de implementação. Para pegar "o primeiro" de verdade, ordene.</div>

  <h3>Operadores de comparação e lógicos</h3>
  <div class="tablewrap"><table>
    <tr><th>Operador</th><th>Significado</th></tr>
    <tr><td><code>=</code></td><td>igual</td></tr>
    <tr><td><code>&lt;&gt;</code> (ou <code>!=</code>)</td><td>diferente</td></tr>
    <tr><td><code>&gt;</code> <code>&gt;=</code> <code>&lt;</code> <code>&lt;=</code></td><td>maior, maior ou igual, menor, menor ou igual (a tabela do slide esqueceu <code>&gt;</code> e <code>&lt;</code>)</td></tr>
    <tr><td><code>AND</code> / <code>OR</code></td><td>E, OU entre condições</td></tr>
    <tr><td><code>BETWEEN a AND b</code></td><td>entre a e b, <b>incluindo</b> os dois extremos</td></tr>
    <tr><td><code>LIKE</code></td><td>filtra parte de um texto; <code>%</code> significa "qualquer coisa"</td></tr>
  </table></div>
  <p>O slide define "alocação integral" como acima de 4 horas e "parcial" como até 6. Confira quantas linhas cada uma devolve:</p>
''' + sqlbox("alpha", "SELECT * FROM ProjetoFuncionario WHERE horas > 4;", "Alocação integral (horas > 4)", expect=17) + sqlbox("alpha", "SELECT * FROM ProjetoFuncionario WHERE horas <= 6;", "Alocação parcial (horas <= 6)", expect=12) + '''
  <p>17 + 12 = 29, mas a tabela só tem <b>21</b> alocações. Oito linhas (as de 5 e 6 horas) aparecem <b>nas duas listas</b>: os critérios do slide se sobrepõem. Para separar de verdade, o corte tem de ser o mesmo número (por exemplo <code>&gt; 6</code> e <code>&lt;= 6</code>).</p>

  <h3>LIKE: poderoso e traiçoeiro</h3>
''' + sqlbox("alpha", "SELECT nome, habilidades FROM Funcionario WHERE habilidades LIKE 'sql%';", "Começa com 'sql'", expect=10) + sqlbox("alpha", "SELECT nome, habilidades FROM Funcionario WHERE habilidades LIKE '%sql%';", "Tem 'sql' em qualquer lugar", expect=18) + '''
  <p><code>'sql%'</code> devolve 10 pessoas, <code>'%sql'</code> (termina com) devolve 2 e <code>'%sql%'</code> devolve 18. Duas pegadinhas que o slide não avisa:</p>
  <ol>
    <li>O <code>LIKE</code> <b>não diferencia maiúscula de minúscula</b> nessa base (no MySQL isso depende da <i>collation</i>): <code>'sql%'</code> acha "SQL Server".</li>
    <li>Ele procura <b>texto, não palavra</b>. Procurar <code>'%sql%'</code> acha também "MySQL" e "PostgreSQL". Filtrar habilidade com LIKE numa coluna de texto separado por vírgula é <b>impreciso</b>. O jeito certo é uma tabela de habilidades ligada ao funcionário (é a 1FN do Capítulo 1 cobrando a conta).</li>
  </ol>
''' + sqlbox("alpha", """UPDATE Funcionario SET habilidades = habilidades || ', aws' WHERE idFuncionario = 1;
INSERT INTO Funcionario (CPF, nome, sobrenome, habilidades, email)
VALUES ('98765432110', 'Luana', 'Santos', 'python, sql, aws', 'luana@email.com');
SELECT idFuncionario, nome, habilidades FROM Funcionario
WHERE habilidades LIKE '%aws%' AND habilidades LIKE '%sql%';""", "AND: quem tem aws e sql (depois de duas mudanças)", expect=2) + '''
  <p>O resultado de <code>AND</code> depende do que os comandos anteriores deixaram: na base original, ninguém tem "aws", e ele devolveria <b>0 linhas</b>. O estado do banco muda o que a consulta responde.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se eu quiser mudar ou apagar? Qual a diferença de errar um SELECT e errar um UPDATE?</div><p>Errar um SELECT custa uma releitura. Errar um UPDATE custa dados.</p></div>
</section>

<section class="sec" id="update-delete">
  <h2><span class="sn">4</span>UPDATE e DELETE: o poder do WHERE</h2>
  <p class="gancho">Um comando de duas palavras que pode acabar com sua tabela.</p>
  <div class="grid2">
    <div class="card rv"><b>UPDATE</b><pre style="margin:6px 0 0"><code>UPDATE Funcionario
SET habilidades = 'python, sql'
WHERE idFuncionario = 1;</code></pre></div>
    <div class="card rv"><b>DELETE</b><pre style="margin:6px 0 0"><code>DELETE FROM Projeto
WHERE idProjeto = 3;</code></pre></div>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Esquecer o WHERE.</b> Sem ele, o <code>UPDATE</code> muda <b>todas</b> as linhas, e o <code>DELETE</code> apaga <b>todas</b>. Escreva o <code>WHERE</code> primeiro, ou confira com um <code>SELECT</code> usando a mesma condição antes de rodar. (O MySQL Workbench tem o modo <i>safe updates</i>, que recusa UPDATE e DELETE sem WHERE com chave.)</div>
  <p>O <code>DELETE</code> do slide apaga o projeto 3 (NeuralNet), que tem 3 alocações. O que acontece depende de a FK existir. Na base do script da aula, que <b>não declara FK</b>, apaga e deixa alocações <b>órfãs</b>. Rode e conte:</p>
''' + sqlbox("alpha", "DELETE FROM Projeto WHERE idProjeto = 3;\nSELECT COUNT(*) AS alocacoes_orfas FROM ProjetoFuncionario WHERE idProjeto = 3;", "Sem FK: alocações órfãs", expect=1) + '''
  <p>As 3 alocações continuam apontando para um projeto que não existe. Com as FKs do Capítulo 3, o mesmo <code>DELETE</code> seria <b>bloqueado</b>. Por isso integridade referencial importa.</p>
  <div class="nota lembra"><span class="lbl">Lembra</span>O <code>AUTO_INCREMENT</code> <b>não reaproveita</b> número apagado: se você apaga o funcionário 26, o próximo recebe 27. E use o <code>CPF</code> (ou outra chave natural) no <code>WHERE</code> quando não souber o id gerado.</div>

  <h3>BETWEEN e datas (e a armadilha do slide)</h3>
''' + sqlbox("alpha", "SELECT nome, dtTermino FROM Projeto WHERE dtTermino BETWEEN '2026-09-17' AND '2026-09-30';", "Projetos que terminam na 2ª quinzena de setembro", expect=1) + '''
  <p>Só o <b>MobileApp</b> (término em 20/09) cai no intervalo. O <code>BETWEEN</code> é <b>inclusivo</b> nos dois extremos. Já o <code>UPDATE</code> do slide tem um problema de lógica: ele faz <code>SET dtInicio = NOW(), dtTermino = DATE_SUB(dtInicio, INTERVAL 35 DAY)</code>. O MySQL executa os <code>SET</code> <b>da esquerda para a direita</b>, então o <code>dtInicio</code> já é o novo, e o término fica <b>35 dias antes</b> do início. Provavelmente a intenção era 35 dias <i>depois</i> (<code>DATE_ADD</code>).</p>
</section>

<section class="sec" id="exercicios">
  <h2><span class="sn">5</span>Exercícios do slide, com solução (as soluções são de estudo: complemento)</h2>
  <p class="gancho">Tente você antes de abrir. Depois confira.</p>
  <p><b>Exercício:</b> (a) inserir um registro seu com as habilidades <code>aws, mysql</code>; (b) acrescentar <code>mariadb</code> às habilidades, sem perder as que já tinha; (c) listar quem tem mariadb; (d) excluir o seu registro.</p>
''' + sqlbox("alpha", """-- (a)
INSERT INTO Funcionario (CPF, nome, sobrenome, habilidades, email)
VALUES ('00000000001', 'Seu', 'Nome', 'aws, mysql', 'teste@exemplo.com');
-- (b) concatenar mantém o que já havia (no MySQL: CONCAT(habilidades, ', mariadb'))
UPDATE Funcionario SET habilidades = habilidades || ', mariadb' WHERE CPF = '00000000001';
-- (c)
SELECT idFuncionario, nome, habilidades FROM Funcionario WHERE habilidades LIKE '%mariadb%';""", "Resolva e rode", expect=1) + '''
  <div class="ex rv"><span class="t">Por que usar o CPF no WHERE?</span>
    <div class="l"><div>O id é gerado pelo banco, e você não sabe qual foi. O CPF você mesmo informou, e é <b>UNIQUE</b>.</div></div>
    <div class="l"><div>Assim o <code>UPDATE</code> e o <code>DELETE</code> miram exatamente uma linha.</div></div>
  </div>
  <p><b>Exercício extra (slide 21; a resposta é complemento):</b> "projetos do mês atual". A frase é ambígua, e vale responder as duas leituras: projetos que <b>terminam</b> no mês (<code>MONTH(dtTermino) = MONTH(CURDATE())</code> no MySQL), ou projetos <b>em andamento</b> em algum dia do mês, que é <code>dtInicio &lt;= fim_do_mês AND dtTermino &gt;= início_do_mês</code>. Para setembro de 2026, a segunda leitura devolve 7 projetos:</p>
''' + sqlbox("alpha", "SELECT nome FROM Projeto\nWHERE dtInicio <= '2026-09-30' AND dtTermino >= '2026-09-01';", "Projetos em andamento em setembro/2026", expect=7) + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>CRUD</b> = INSERT, SELECT, UPDATE, DELETE. É a DML.",
    "<code>SELECT cols FROM tab WHERE cond ORDER BY col LIMIT n</code>. Sem ORDER BY, a ordem <b>não é garantida</b>.",
    "<b>BETWEEN</b> é inclusivo. <b>LIKE</b> com <code>%</code> busca texto, não palavra.",
    "<b>UPDATE/DELETE sem WHERE</b> afetam a tabela inteira. Teste a condição com SELECT antes.",
    "Sem FK, o DELETE deixa linhas <b>órfãs</b>. Com FK, o banco bloqueia.",
    "Duas condições com cortes diferentes (&gt; 4 e &lt;= 6) podem <b>se sobrepor</b>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Você roda <code>UPDATE Funcionario SET email = 'x@exemplo.com';</code> sem WHERE. O que acontece?", [("a","O banco recusa, porque falta o WHERE."),("b","Todos os funcionários ficam com o mesmo e-mail."),("c","Só a primeira linha é alterada.")], "O SQL não exige WHERE. Sem ele, o comando age em todas as linhas. Por isso se escreve (ou se testa com SELECT) a condição primeiro.") + quiz(2, "c", "<code>horas BETWEEN 4 AND 6</code> equivale a:", [("a","horas &gt; 4 AND horas &lt; 6"),("b","horas = 4 OR horas = 6"),("c","horas &gt;= 4 AND horas &lt;= 6")], "BETWEEN inclui os dois extremos. As alternativas a e b deixam valores de fora.") + quiz(3, "a", "Por que <code>LIKE '%sql%'</code> não é um bom filtro de 'sabe SQL'?", [("a","Porque busca texto: acha também MySQL e PostgreSQL."),("b","Porque só funciona em maiúsculas."),("c","Porque o % não é permitido no meio.")], "O LIKE não conhece 'palavras'. O ideal é uma tabela de habilidades ligada ao funcionário.") + flash([
    ("O que é CRUD?", "Create, Read, Update, Delete: INSERT, SELECT, UPDATE, DELETE."),
    ("LIMIT 1 garante o primeiro?", "Não. Sem ORDER BY a ordem não é garantida."),
    ("O que é uma linha órfã?", "Uma linha que aponta (por FK) para uma linha-pai que não existe mais."),
    ("O que o % faz no LIKE?", "Representa qualquer sequência de caracteres, de qualquer tamanho.")]) + ponte("Consigo achar linhas. Mas e se eu quiser resumos, como médias e totais por projeto?", "Com as funções de agregação, o GROUP BY e o HAVING.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter("banco-de-dados", 4, "dml", T, "DML: INSERT, SELECT, UPDATE, DELETE", "Capítulo 4 · Aula 4",
        "Colocar dados nas tabelas, achar o que interessa, mudar e apagar sem estragar nada.",
        ["<b>~45 min</b>", "12 demos · 3 testes · 4 flashcards", "SQL executável"], body4, scripts=S, sql=True)
print("caps 3-4 ok")
