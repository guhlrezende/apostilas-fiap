from bld import *
T = "Bancos de Dados e SQL"
S = ["bases.js"]

# ---------------- CAP 5: agregações ----------------
body5 = recap("No Capítulo 4 você aprendeu a incluir, achar, mudar e apagar linhas. Só que o gestor da startup não quer ler 21 alocações: ele quer <b>indicadores</b>. Quantos funcionários há em cada projeto? Qual a média de horas? Qual projeto aloca mais gente? Isso é <b>análise exploratória</b> (EDA) com SQL.") + '''

<section class="sec" id="funcoes">
  <h2><span class="sn">1</span>Funções de agregação: muitas linhas, um valor</h2>
  <p class="gancho">Em vez de olhar linha por linha, resuma.</p>
  <p>As <b>funções de agregação</b> pegam várias linhas e devolvem <mark class="hl">um valor só</mark>:</p>
  <div class="tablewrap"><table>
    <tr><th>Função</th><th>Devolve</th></tr>
    <tr><td><code>MIN(col)</code></td><td>o menor valor</td></tr>
    <tr><td><code>MAX(col)</code></td><td>o maior valor</td></tr>
    <tr><td><code>AVG(col)</code></td><td>a média</td></tr>
    <tr><td><code>SUM(col)</code></td><td>a soma</td></tr>
    <tr><td><code>COUNT(col)</code></td><td>quantas linhas têm valor <b>não nulo</b> em <i>col</i> (<code>COUNT(*)</code> conta linhas, e <code>COUNT(DISTINCT col)</code> conta valores sem repetição)</td></tr>
  </table></div>
  <p>O cenário usa a base <b>alpha</b>: <code>Funcionario</code> (25 linhas), <code>Projeto</code> (10) e <code>ProjetoFuncionario</code> (21 alocações). Tente a primeira pergunta: a média e a soma de horas do projeto 1.</p>
''' + sqlbox("alpha", "SELECT AVG(horas) AS media, SUM(horas) AS soma, COUNT(horas) AS pessoas\nFROM ProjetoFuncionario\nWHERE idProjeto = 1;", "Projeto 1 (Omega): média 7, soma 14, 2 pessoas", expect=1) + '''
  <p>E o resumo geral. Rode e depois mude as funções para ver o que cada uma devolve:</p>
''' + sqlbox("alpha", "SELECT MAX(horas) AS maximo, MIN(horas) AS minimo, AVG(horas) AS media,\n       COUNT(*) AS alocacoes, COUNT(DISTINCT idFuncionario) AS pessoas\nFROM ProjetoFuncionario;", "Resumo de todas as alocações", expect=1) + '''
  <div class="ex rv"><span class="t">Por que COUNT(*) e COUNT(DISTINCT) divergem?</span>
    <div class="l"><div>Há <b>21 alocações</b> (linhas da tabela associativa).</div></div>
    <div class="l"><div>Mas o Carlos (id 2) está em <b>dois</b> projetos, então ele aparece em duas linhas.</div></div>
    <div class="l"><div><code>COUNT(DISTINCT idFuncionario)</code> conta <b>pessoas</b>: <b>20</b>. E dos 25 funcionários cadastrados, 5 não estão em nenhum projeto.</div></div>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b>COUNT(coluna) ignora NULL.</b> <code>COUNT(*)</code> conta todas as linhas; <code>COUNT(horas)</code> conta só as que têm <code>horas</code> preenchido. O mesmo vale para <code>AVG</code>, <code>SUM</code>, <code>MIN</code> e <code>MAX</code>: <b>NULL fica de fora</b> das contas. E o <code>SUM</code> de nenhuma linha devolve <code>NULL</code>, não zero.</div>
''' + sqlbox("alpha", "SELECT COUNT(*) AS linhas, COUNT(NULLIF(horas, 8)) AS sem_as_de_8h FROM ProjetoFuncionario;", "COUNT ignorando NULL (NULLIF troca 8 por NULL)", expect=1) + '''
  <p>O <code>NULLIF(horas, 8)</code> vira <code>NULL</code> quando <code>horas</code> vale 8. Das 21 alocações, 9 têm 8 horas, então o <code>COUNT</code> enxerga 12.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Quero a média de horas <i>de cada projeto</i>, e não da tabela inteira. Preciso rodar uma consulta por projeto?</div><p>Não: o GROUP BY faz isso numa só.</p></div>
</section>

<section class="sec" id="groupby">
  <h2><span class="sn">2</span>GROUP BY: uma resposta por grupo</h2>
  <p class="gancho">A mesma função, aplicada a cada subgrupo.</p>
  <p>O <code>GROUP BY</code> divide as linhas em grupos pelo valor de uma coluna e aplica a agregação <b>a cada grupo</b>. Veja quantas pessoas há em cada projeto (a barra mostra o tamanho):</p>
  <div class="demo" data-demo="sql" data-db="alpha" data-bar="1" data-titulo="Funcionários por projeto"><pre class="q">SELECT idProjeto, COUNT(1) AS QtdProgramadores
FROM ProjetoFuncionario
GROUP BY idProjeto;</pre></div>
  <p>São 10 grupos (um por projeto). A regra que o SQL impõe (complemento, não dada em aula): toda coluna do <code>SELECT</code> que <b>não</b> está dentro de uma função de agregação tem de estar no <code>GROUP BY</code>. (Um detalhe: o <code>COUNT(1)</code> do slide conta linhas, igual a <code>COUNT(*)</code>.)</p>
  <h3>O alias AS</h3>
  <p><code>AS</code> dá um nome legível à coluna do resultado (<code>AS QtdProgramadores</code>). Não muda nada nos dados, só o cabeçalho. Útil em relatórios, e necessário para ordenar por uma conta.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Agora só quero os projetos com mais de um funcionário. Posso filtrar com WHERE?</div><p>Não, e a razão é a ordem em que o SQL executa as cláusulas.</p></div>
</section>

<section class="sec" id="having">
  <h2><span class="sn">3</span>HAVING: filtrar grupos (e a ordem de execução)</h2>
  <p class="gancho">WHERE olha linhas. HAVING olha grupos.</p>
  <p>O <code>WHERE</code> roda <b>antes</b> do agrupamento, então não enxerga o resultado de um <code>COUNT</code>. Para filtrar pelo valor agregado, use <code>HAVING</code>:</p>
''' + sqlbox("alpha", "SELECT idProjeto, COUNT(1) AS qtd\nFROM ProjetoFuncionario\nGROUP BY idProjeto\nHAVING COUNT(1) > 1;", "Projetos com mais de um funcionário", expect=9) + '''
  <p>Dos 10 projetos, 9 passam (o projeto 10 tem uma pessoa só). Isso sugere uma imagem para guardar: a <b>ordem lógica</b> em que o SQL processa um comando é diferente da ordem em que você o escreve.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. FROM</b><p>Escolhe a tabela (ou junta várias, no Capítulo 6).</p></div>
      <div class="st"><b>2. WHERE</b><p>Filtra <b>linhas</b>. Ainda não existem grupos nem agregações.</p></div>
      <div class="st"><b>3. GROUP BY</b><p>Forma os grupos com as linhas que sobraram.</p></div>
      <div class="st"><b>4. HAVING</b><p>Filtra <b>grupos</b>, agora que as agregações existem.</p></div>
      <div class="st"><b>5. SELECT</b><p>Calcula as colunas do resultado (e os aliases).</p></div>
      <div class="st"><b>6. ORDER BY e LIMIT</b><p>Ordena e corta. Por isso o ORDER BY consegue usar um alias do SELECT, e o WHERE não consegue.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <div class="nota lembra"><span class="lbl">Lembra (complemento)</span>Esta ordem lógica explica três erros clássicos: usar um alias no <code>WHERE</code> (ele ainda não existe), usar <code>COUNT()</code> no <code>WHERE</code> (ainda não há grupos) e filtrar por <code>HAVING</code> algo que caberia num <code>WHERE</code> (funciona, mas processa mais linhas do que precisava).</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">As respostas às três perguntas do gestor estão a um passo.</div><p>Vamos fechar o cenário, e ver de onde vem o problema do próximo capítulo.</p></div>
</section>

<section class="sec" id="cenario">
  <h2><span class="sn">4</span>Respondendo ao gestor</h2>
  <p class="gancho">Três perguntas, três consultas.</p>
  <div class="grid3">
    <div class="card rv"><b>1. Quantos por projeto?</b><p><code>GROUP BY idProjeto</code> com <code>COUNT</code>. (Acima.)</p></div>
    <div class="card rv"><b>2. Média de horas?</b><p><code>AVG(horas)</code> da tabela toda: cerca de <b>6,33</b> horas.</p></div>
    <div class="card rv"><b>3. Qual projeto aloca mais?</b><p>Ordene a contagem em ordem decrescente. Empate no topo: <b>AlphaBI</b> e <b>NeuralNet</b>, com 3 pessoas cada.</p></div>
  </div>
  <p>A terceira consulta mostra um problema. Para responder com <b>nomes</b> de projeto (e não ids) precisamos trazer a coluna <code>nome</code>, que mora em outra tabela. Aqui vai uma prévia de como isso se resolve, com um <code>JOIN</code> (o assunto do próximo capítulo). Em qual projeto se somam mais horas?</p>
''' + sqlbox("alpha", "SELECT p.nome, SUM(pf.horas) AS total_horas\nFROM ProjetoFuncionario pf\nJOIN Projeto p ON p.idProjeto = pf.idProjeto\nGROUP BY p.nome\nORDER BY total_horas DESC\nLIMIT 3;", "Top 3 projetos por horas somadas", expect=3) + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Agregações</b> resumem muitas linhas em um valor: MIN, MAX, AVG, SUM, COUNT.",
    "<code>COUNT(*)</code> conta linhas; <code>COUNT(col)</code> ignora NULL; <code>COUNT(DISTINCT col)</code> conta valores únicos.",
    "<b>GROUP BY</b> faz uma agregação por grupo. Colunas fora da agregação devem estar no GROUP BY.",
    "<b>WHERE</b> filtra linhas (antes do agrupamento); <b>HAVING</b> filtra grupos (depois).",
    "Ordem lógica: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.",
    "<b>AS</b> dá nome legível à coluna do resultado."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "COUNT(*) dá 21 e COUNT(DISTINCT idFuncionario) dá 20 na tabela de alocações. Por quê?", [("a","Porque um funcionário tem NULL no id."),("b","Porque há um funcionário alocado em dois projetos, então ele aparece em duas linhas."),("c","Porque o DISTINCT remove linhas ao acaso.")], "COUNT(*) conta as alocações (linhas). COUNT(DISTINCT) conta pessoas. O Carlos está em dois projetos.") + quiz(2, "c", "Quero projetos com mais de 5 pessoas. Onde ponho a condição?", [("a","No WHERE, porque filtra."),("b","No SELECT."),("c","No HAVING, porque depende de uma agregação (COUNT).")], "O WHERE roda antes do agrupamento e não enxerga o COUNT. A condição sobre o valor agregado vai no HAVING.") + quiz(3, "a", "O que acontece com o NULL em AVG(horas)?", [("a","Ele é ignorado: a média considera só os valores preenchidos."),("b","Ele vira zero e puxa a média para baixo."),("c","A consulta dá erro.")], "As funções de agregação ignoram NULL (exceto COUNT(*)). Se quiser tratar NULL como zero, use COALESCE(horas, 0).") + flash([
    ("WHERE x HAVING?", "WHERE filtra linhas antes do agrupamento. HAVING filtra grupos depois, e pode usar agregações."),
    ("Para que serve o AS?", "Dá um nome (alias) à coluna ou à tabela no resultado."),
    ("COUNT(*) x COUNT(col)?", "COUNT(*) conta linhas. COUNT(col) conta só as com valor não nulo."),
    ("Ordem lógica do SQL?", "FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT.")]) + ponte("Os resumos estão por id. E se o nome do projeto mora em outra tabela?", "Então precisamos juntar tabelas. É o assunto dos JOINs.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter("banco-de-dados", 5, "agregacoes", T, "Agregações, GROUP BY e HAVING", "Capítulo 5 · Aula 5",
        "Transformar tabelas em indicadores: quantos, quanto, qual a média, e por grupo.",
        ["<b>~35 min</b>", "6 demos · 3 testes · 4 flashcards", "SQL executável"], body5, scripts=S, sql=True)

# ---------------- CAP 6: JOINs ----------------
body6 = recap("No Capítulo 5 você resumiu as alocações com GROUP BY, mas só conseguia falar em <i>idProjeto</i>, porque o nome do projeto mora em outra tabela. Esse é o motivo de normalizar (Capítulo 1): os dados se espalham em tabelas, e o <b>JOIN</b> é como você os junta de volta quando precisa.") + '''

<section class="sec" id="porque">
  <h2><span class="sn">1</span>Por que existe o JOIN</h2>
  <p class="gancho">Normalizar espalha os dados. Como colá-los de novo?</p>
  <p>Numa papelaria, o <b>pedido</b> guarda só o <code>idCliente</code>, e o nome do cliente está na tabela <code>cliente</code>. Para listar "pedido e nome do cliente", você junta as duas tabelas pela coluna que as liga: a FK do pedido com a PK do cliente. Esse é o <code>JOIN</code>.</p>
  <div class="formula">SELECT ... FROM tabelaA JOIN tabelaB ON tabelaA.chave = tabelaB.chave;<small>O ON diz como as linhas se casam: normalmente FK = PK.</small></div>
  <p>A papelaria tem cinco clientes, mas <b>só duas pessoas fizeram pedido</b> (Júlia e Amanda). Guarde isso: é o que faz os tipos de JOIN darem resultados diferentes.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E as linhas que não têm par na outra tabela? Somem, ou ficam?</div><p>Depende do tipo de JOIN. Vamos testar os quatro.</p></div>
</section>

<section class="sec" id="tipos">
  <h2><span class="sn">2</span>INNER, LEFT, RIGHT e FULL</h2>
  <p class="gancho">A diferença está no destino de quem não tem par.</p>
  <div class="demo" data-demo="joins"></div>
  <div class="tablewrap"><table>
    <tr><th>JOIN</th><th>Devolve</th><th>Quem não tem par</th></tr>
    <tr><td><b>INNER</b></td><td>só as linhas casadas dos dois lados</td><td>some</td></tr>
    <tr><td><b>LEFT</b></td><td>todas da tabela da <b>esquerda</b> (a do FROM)</td><td>a direita vem com NULL</td></tr>
    <tr><td><b>RIGHT</b></td><td>todas da tabela da <b>direita</b> (a do JOIN)</td><td>a esquerda vem com NULL</td></tr>
    <tr><td><b>FULL</b></td><td>todas dos dois lados</td><td>o lado sem par vem com NULL</td></tr>
  </table></div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Não saber qual lado é a "esquerda".</b> É a tabela que vem depois do <code>FROM</code>. E repare: <code>A LEFT JOIN B</code> faz exatamente o mesmo que <code>B RIGHT JOIN A</code>. Na prática, quase todo mundo usa só LEFT e escreve a tabela principal primeiro.</div>
  <p>Agora os exercícios da aula, na base da papelaria. Primeiro o <b>INNER</b>, produto e fornecedor (5 produtos, todos com fornecedor):</p>
''' + sqlbox("papelaria", "SELECT P.dscProduto, F.Nome AS fornecedor\nFROM produto P\nINNER JOIN fornecedor F ON P.idFornecedor = F.idFornecedor;", "INNER JOIN: produto e fornecedor", expect=5) + '''
  <p>Em seguida, <b>LEFT</b> e <b>RIGHT</b> entre pedido e cliente. No LEFT, o ponto de partida são os <b>pedidos</b> (4), e Roberto, Mariana e Miguel não aparecem. No RIGHT, o ponto de partida são os <b>clientes</b> (5), e os três sem pedido vêm com <code>idPedido</code> NULL:</p>
''' + sqlbox("papelaria", "SELECT P.idPedido, C.Nome\nFROM pedido P\nLEFT JOIN cliente C ON P.idCliente = C.idCliente;", "LEFT JOIN: parte dos pedidos", expect=4) + sqlbox("papelaria", "SELECT P.idPedido, C.Nome\nFROM pedido P\nRIGHT JOIN cliente C ON P.idCliente = C.idCliente;", "RIGHT JOIN: parte dos clientes", expect=7) + '''
  <div class="nota lembra"><span class="lbl">Complemento: achar quem NÃO tem par</span>O LEFT JOIN com <code>WHERE ... IS NULL</code> é o jeito clássico de achar o que falta: clientes que nunca compraram, funcionários sem projeto. Veja na alpha, onde 5 pessoas não estão em projeto nenhum:</div>
''' + sqlbox("alpha", "SELECT F.nome\nFROM Funcionario F\nLEFT JOIN ProjetoFuncionario PF ON PF.idFuncionario = F.idFuncionario\nWHERE PF.idFuncionario IS NULL;", "Funcionários sem alocação", expect=5) + '''
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se a informação que eu quero estiver espalhada em quatro tabelas?</div><p>Dá para encadear JOINs, e usar apelidos para não se perder.</p></div>
</section>

<section class="sec" id="varias">
  <h2><span class="sn">3</span>Várias tabelas e apelidos</h2>
  <p class="gancho">Cliente, pedido, itens e produto: quem comprou o quê?</p>
  <p>Cada <code>JOIN</code> adiciona uma tabela. O <b>apelido</b> (alias) da tabela (<code>C</code>, <code>P</code>, <code>I</code>, <code>PR</code>) encurta o texto e evita ambiguidade quando duas tabelas têm colunas com o mesmo nome (<code>Nome</code> existe em cliente e em fornecedor):</p>
''' + sqlbox("papelaria", "SELECT C.Nome, P.idPedido, PR.dscProduto\nFROM cliente C\nINNER JOIN pedido P     ON P.idCliente = C.idCliente\nINNER JOIN itempedido I ON I.idPedido = P.idPedido\nINNER JOIN produto PR   ON PR.idProduto = I.idProduto\nORDER BY P.idPedido;", "Quatro tabelas encadeadas", expect=6) + '''
  <p>Resultado: Júlia no pedido 1 (Caderno e Lápis) e no 3 (Borracha); Amanda no pedido 2 (Estojo) e no 4 (Caderno e Lápis). São 6 linhas, uma por item vendido.</p>
  <p>O mesmo vale na alpha: o relatório de "funcionário e projeto onde está alocado" são 21 linhas, uma por alocação:</p>
''' + sqlbox("alpha", "SELECT F.nome AS funcionario, P.nome AS projeto\nFROM ProjetoFuncionario PF\nINNER JOIN Funcionario F ON PF.idFuncionario = F.idFuncionario\nINNER JOIN Projeto P     ON PF.idProjeto = P.idProjeto;", "Relatório de alocações", expect=21) + '''
  <div class="nota cuidado"><span class="lbl">Cuidado: o alias do slide</span>O slide do RIGHT JOIN escreve <code>FP</code> como apelido, mas a tabela foi apelidada como <code>PF</code>. Copiado, dá erro de coluna desconhecida. Sempre confira se o apelido do <code>SELECT</code> é o mesmo do <code>FROM</code>.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O MySQL não tem FULL JOIN. Como obter "todos dos dois lados"?</div><p>Empilhando dois resultados com UNION.</p></div>
</section>

<section class="sec" id="union">
  <h2><span class="sn">4</span>UNION e UNION ALL</h2>
  <p class="gancho">JOIN coloca tabelas lado a lado. UNION empilha resultados.</p>
  <p>O <code>UNION</code> junta os resultados de dois <code>SELECT</code> <b>um embaixo do outro</b>, e eles precisam ter o mesmo número de colunas (e tipos compatíveis). A diferença entre as duas versões:</p>
  <div class="grid2">
    <div class="card rv"><b>UNION</b><p>Remove duplicados.</p></div>
    <div class="card rv"><b>UNION ALL</b><p>Mantém tudo (e é mais rápido, porque não precisa checar duplicidade).</p></div>
  </div>
''' + sqlbox("papelaria", "SELECT Cidade FROM fornecedor\nUNION\nSELECT Cidade FROM cliente;", "UNION: cidades sem repetição", expect=6) + sqlbox("papelaria", "SELECT Cidade FROM fornecedor\nUNION ALL\nSELECT Cidade FROM cliente;", "UNION ALL: com repetição", expect=8) + '''
  <p>São 3 fornecedores e 5 clientes, ou seja, 8 linhas. "São Paulo" aparece <b>3 vezes</b> (um fornecedor e dois clientes). O <code>UNION</code> deixa uma só, e dá 6.</p>
  <h3>FULL JOIN simulado</h3>
  <p>No MySQL, "todos dos dois lados" se obtém juntando um LEFT e um RIGHT com UNION (que ainda elimina as linhas repetidas):</p>
<pre><code><span class="k">SELECT</span> PF.idProjeto, PF.idFuncionario, F.nome
<span class="k">FROM</span> ProjetoFuncionario PF <span class="k">LEFT JOIN</span> Funcionario F <span class="k">ON</span> PF.idFuncionario = F.idFuncionario
<span class="k">UNION</span>
<span class="k">SELECT</span> PF.idProjeto, PF.idFuncionario, F.nome
<span class="k">FROM</span> ProjetoFuncionario PF <span class="k">RIGHT JOIN</span> Funcionario F <span class="k">ON</span> PF.idFuncionario = F.idFuncionario;</code></pre>
  <p>Na alpha dá 26 linhas: as 21 alocações, mais os 5 funcionários sem projeto, que vêm com <code>idProjeto</code> NULL. (O SQLite do navegador já aceita <code>FULL JOIN</code> direto, mas você precisa saber a versão com UNION, porque é a do MySQL.)</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>JOIN</b> junta tabelas pelo <code>ON</code>, normalmente FK = PK.",
    "<b>INNER</b>: só os casados. <b>LEFT</b>: todos da esquerda. <b>RIGHT</b>: todos da direita. <b>FULL</b>: todos dos dois lados.",
    "<code>A LEFT JOIN B</code> é o mesmo que <code>B RIGHT JOIN A</code>. A esquerda é a tabela do <code>FROM</code>.",
    "LEFT JOIN + <code>WHERE ... IS NULL</code> acha o que <b>não tem par</b>.",
    "<b>Alias</b> de tabela encurta e desambigua. Confira se o apelido é o mesmo no SELECT e no FROM.",
    "<b>UNION</b> remove duplicados; <b>UNION ALL</b> mantém. FULL JOIN no MySQL = LEFT + UNION + RIGHT."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Na papelaria, quantos clientes aparecem em <code>cliente C INNER JOIN pedido P</code>?", [("a","Os 5 clientes."),("b","Nenhum."),("c","Só os que fizeram pedido: Júlia e Amanda (4 linhas, porque cada uma tem 2 pedidos).")], "O INNER descarta quem não tem par. Roberto, Mariana e Miguel nunca pediram. São 4 linhas porque Júlia e Amanda têm dois pedidos cada.") + quiz(2, "a", "Como listar os clientes que nunca fizeram pedido?", [("a","LEFT JOIN de cliente com pedido, filtrando <code>WHERE P.idPedido IS NULL</code>."),("b","INNER JOIN de cliente com pedido."),("c","UNION ALL de cliente com pedido.")], "O LEFT mantém todos os clientes, e quem não tem pedido vem com NULL na coluna do pedido. O filtro IS NULL deixa só esses.") + quiz(3, "b", "Qual a diferença entre UNION e UNION ALL?", [("a","UNION junta tabelas lado a lado."),("b","UNION remove linhas duplicadas; UNION ALL mantém todas."),("c","Não há diferença de resultado.")], "As cidades de fornecedores e clientes dão 6 linhas com UNION e 8 com UNION ALL.") + flash([
    ("O que é o ON de um JOIN?", "A condição que casa as linhas das duas tabelas, em geral FK = PK."),
    ("LEFT x INNER?", "O LEFT mantém todas as linhas da esquerda, mesmo sem par. O INNER descarta as sem par."),
    ("Como simular FULL JOIN no MySQL?", "LEFT JOIN UNION RIGHT JOIN."),
    ("Para que serve o alias de tabela?", "Encurtar o texto e distinguir colunas com o mesmo nome em tabelas diferentes.")]) + ponte("Meus comandos ficaram enormes e eu reescrevo os mesmos JOINs. Dá para guardar isso no banco?", "Dá: views, functions, procedures e triggers.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
chapter("banco-de-dados", 6, "joins-union", T, "JOINs e UNION", "Capítulo 6 · Aula 6",
        "Juntar o que a normalização espalhou: INNER, LEFT, RIGHT, FULL e UNION.",
        ["<b>~45 min</b>", "9 demos · 3 testes · 4 flashcards", "SQL executável"], body6, scripts=S + ["demos/cap-6.js"], sql=True)
print("caps 5-6 ok")
