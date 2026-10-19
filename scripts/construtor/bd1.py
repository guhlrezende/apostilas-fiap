from bld import *
T = "Bancos de Dados e SQL"
S = ["bases.js"]

# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo, então não precisa saber nada de bancos. Basta já ter usado uma planilha. Daqui em diante, cada capítulo abre lembrando o que ficou em aberto no anterior.", "Ponto de partida") + '''

<section class="sec" id="dado-informacao">
  <h2><span class="sn">1</span>Dado não é informação</h2>
  <p class="gancho">Antes de guardar qualquer coisa, qual é a coisa?</p>
  <p><b>Dados</b> são fatos ou valores brutos, registros que podem ser gravados e têm algum significado inerente: nomes, telefones, endereços. Veja um exemplo do material: <i>"o aluno A tirou 10 na prova de Matemática em 03/04/2025"</i>. Cada pedaço (aluno, nota, disciplina, data) é um dado.</p>
  <p>A <mark class="hl">informação</mark> nasce quando você organiza e interpreta esses dados para responder uma pergunta: <i>"qual foi a média da turma em Matemática?"</i> A mesma tabela de dados gera informações diferentes conforme a pergunta. Por isso um banco de dados precisa guardar o dado de um jeito que permita perguntar muitas coisas depois.</p>
  <div class="ex rv"><span class="t">Exemplo: do dado à informação</span>
    <div class="l"><div><b>Dados:</b> João, 10, Matemática · Maria, 9, Português · Ana, 8, Matemática.</div></div>
    <div class="l"><div><b>Pergunta:</b> qual a nota média em Matemática?</div></div>
    <div class="l"><div><b>Informação:</b> (10 + 8) ÷ 2 = <b>9</b>. Os dados sozinhos não diziam isso. Foi a pergunta que os transformou.</div></div>
  </div>
''' + ponte("Onde guardar esses dados para poder perguntar muita coisa, para muita gente, sem bagunça?", "Em um banco de dados. E quem cuida dele para você é o SGBD.") + '''
</section>

<section class="sec" id="sgbd">
  <h2><span class="sn">2</span>Banco de dados e SGBD</h2>
  <p class="gancho">Uma pasta de planilhas já é um banco de dados?</p>
  <p>Segundo Elmasri e Navathe (a bibliografia da disciplina), <b>um banco de dados é uma coleção de dados relacionados</b>. O slide completa: uma coleção organizada de informações tratadas como uma unidade, para <b>coletar, armazenar e recuperar</b> informações para uso por aplicativos. Um detalhe curioso: um banco de dados <b>pode ser mantido manualmente</b>. Um fichário de papel é um banco de dados. O que mudou foi o jeito de operar.</p>
  <p>Quem opera é o <abbr class="gl" data-def="Sistema Gerenciador de Banco de Dados. Em inglês, DBMS (Database Management System). Exemplos: MySQL, PostgreSQL, Oracle, SQL Server, SQLite, MariaDB.">SGBD</abbr>: o software que permite <b>definir, construir, manipular e compartilhar</b> bancos de dados. Você não mexe nos arquivos do disco. Você pede ao SGBD, normalmente em SQL, e ele cuida do resto.</p>

  <h3>Por que não bastam arquivos soltos?</h3>
  <p>Num sistema "tradicional", cada programa guarda seus próprios arquivos, e os mesmos dados acabam copiados em vários lugares. O SGBD existe para resolver cinco problemas:</p>
  <div class="tablewrap"><table>
    <tr><th>Requisito</th><th>O problema que resolve</th></tr>
    <tr><td><b>Controle de redundância</b></td><td>O mesmo dado em locais diferentes ocupa espaço e se contradiz.</td></tr>
    <tr><td><b>Consistência</b></td><td>Todo usuário enxerga os mesmos valores.</td></tr>
    <tr><td><b>Compartilhamento e concorrência</b></td><td>Duas pessoas não podem alterar o mesmo dado ao mesmo tempo e corromper o resultado.</td></tr>
    <tr><td><b>Segurança</b></td><td>Autenticação (quem é você) e autorização (o que você pode fazer).</td></tr>
    <tr><td><b>Backup e recuperação</b></td><td>Um registro (log) de todas as transações permite restaurar depois de uma falha.</td></tr>
  </table></div>
  <p>Há ainda vantagens extras: busca mais rápida por <b>índices</b> (estruturas em árvore, as <i>B-tree</i>, que você vê no Capítulo 8), persistência, ferramentas de backup, vários usuários e <b>regras (constraints)</b>, como "só pode existir um número de matrícula por aluno".</p>

  <h3>Por dentro de um SGBD</h3>
  <p>Quando você manda uma consulta, ela atravessa camadas. Avance:</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Você escreve SQL</b><p><code>SELECT nome FROM Funcionario WHERE idFuncionario = 1;</code> É a linguagem em que você conversa com o SGBD.</p></div>
      <div class="st"><b>2. O processador de consultas</b><p>Interpreta o comando, gerencia memória e <b>otimiza</b>: decide o caminho mais rápido até os dados (por exemplo, usar um índice).</p></div>
      <div class="st"><b>3. O dicionário de dados</b><p>Um catálogo com a definição da <b>estrutura</b> (tabelas, colunas, tipos, chaves) e dos usuários. É a camada central do desenho do livro e a que mais se esquece.</p></div>
      <div class="st"><b>4. Os dados armazenados</b><p>Só aqui o disco entra. O resultado volta pelo mesmo caminho até você.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>

  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Existem vários jeitos de organizar dados dentro do SGBD. Qual a disciplina usa, e por quê?</div><p>O mais famoso de todos: o modelo relacional.</p></div>
</section>

<section class="sec" id="relacional">
  <h2><span class="sn">3</span>O modelo relacional, de Codd</h2>
  <p class="gancho">Como organizar dados para que o computador não precise "seguir ponteiros"?</p>
  <p>Na década de 1960 os bancos eram <b>hierárquicos</b> (IBM). Em 1970, <b>Edgar "Ted" Codd</b>, também da IBM, propôs outro caminho: guardar tudo em <b>tabelas</b>, <mark class="hl g">sem ponteiros</mark>, ligadas só pelos <b>valores</b> dos dados. É o modelo relacional, e é o que esta disciplina usa. Depois vieram os bancos orientados a objetos (anos 1980), a web (1990) e, a partir dos anos 2000, o NoSQL e o Big Data.</p>
  <div class="tablewrap"><table>
    <tr><th>Aluno</th><th>Nota</th><th>Disciplina</th></tr>
    <tr><td>João</td><td>10</td><td>Matemática</td></tr>
    <tr><td>Maria</td><td>9</td><td>Português</td></tr>
  </table></div>
  <p>Três ideias sustentam o modelo:</p>
  <ul>
    <li><b>Tabelas</b> (conjuntos de linhas). Cada linha é um registro; cada coluna, um atributo.</li>
    <li><b>Sem ponteiros</b>: duas tabelas se ligam porque uma guarda o valor que identifica uma linha da outra.</li>
    <li><b>Chaves</b>: a <b>chave primária (PK)</b> identifica unicamente cada linha da própria tabela; a <b>chave estrangeira (FK)</b> guarda a PK de outra tabela e cria a ligação.</li>
  </ul>
  <p>Os SGBDs relacionais mais usados: MySQL, PostgreSQL, Oracle, SQL Server, SQLite, MariaDB e DB2. O MySQL e o MariaDB falam praticamente o mesmo SQL, porque o MariaDB nasceu em 2009 como um <i>fork</i> do MySQL, feito pelo mesmo criador logo depois da compra do MySQL pela Oracle.</p>
  <div class="nota lembra"><span class="lbl">Lembra</span>Repare nas duas palavras que vão voltar em todo capítulo: <b>PK</b> (identifica a linha) e <b>FK</b> (aponta para a PK de outra tabela). Quem entende as duas já domina a base de qualquer modelagem.</div>

  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O professor perguntou, olhando uma base de faculdade: "é possível melhorar? Existem redundâncias?"</div><p>Há um método para responder isso sem depender do "achismo": a normalização.</p></div>
</section>

<section class="sec" id="normalizacao">
  <h2><span class="sn">4</span>Normalização: cada informação em um lugar só</h2>
  <p class="gancho">Se o mesmo dado aparece em várias linhas, o que acontece quando ele muda?</p>
  <p>O próprio Codd formalizou regras para eliminar redundância e inconsistência: as <b>formas normais</b>. A ideia: cada informação fica guardada <mark class="hl">em um único lugar</mark>. Sem isso aparecem três problemas, as <b>anomalias</b>:</p>
  <div class="grid3">
    <div class="card rv"><b>Inserção</b><p>Não dá para cadastrar um cliente sem inventar um pedido.</p></div>
    <div class="card rv"><b>Atualização</b><p>O dado repetido em várias linhas exige mudar todas as cópias. Esquecer uma gera contradição.</p></div>
    <div class="card rv"><b>Exclusão</b><p>Apagar o único pedido de alguém apaga, sem querer, os dados do cliente.</p></div>
  </div>
  <p>Veja a anomalia de atualização acontecer. A tabela <code>pedido_flat</code> repete o nome e a cidade da Júlia em cada pedido dela. Mude a cidade em <b>uma</b> linha só e depois olhe os clientes distintos:</p>
''' + sqlbox("loja", "UPDATE pedido_flat SET cliente_cidade = 'Campinas' WHERE idPedido = 1;\nSELECT DISTINCT cliente_nome, cliente_cidade FROM pedido_flat;", "Anomalia de atualização") + '''
  <p>A Júlia agora mora em <b>duas cidades</b> ao mesmo tempo. Foi isso que a redundância causou. A versão normalizada separa o cliente (uma linha só) dos pedidos. Repita o mesmo ajuste nela e veja o resultado:</p>
''' + sqlbox("loja", "UPDATE cliente_n SET cidade = 'Campinas' WHERE cliente_id = 10;\nSELECT p.idPedido, c.nome, c.cidade, p.produto\nFROM pedido_n p JOIN cliente_n c ON c.cliente_id = p.cliente_id;", "Mesma mudança, agora normalizada") + '''
  <h3>As formas normais, em ordem de rigor</h3>
  <div class="tablewrap"><table>
    <tr><th>Forma</th><th>Exige</th><th>O que elimina</th><th>Exemplo de violação</th></tr>
    <tr><td><b>1FN</b></td><td>valores <b>atômicos</b> (indivisíveis)</td><td>grupos repetitivos</td><td>colunas <code>telefone1, telefone2, telefone3</code>, ou uma célula com "python, sql, aws"</td></tr>
    <tr><td><b>2FN</b></td><td>1FN e nada depende de <b>parte</b> da chave</td><td>dependências parciais</td><td>com PK composta (pedido, produto), o nome do produto depende só do produto</td></tr>
    <tr><td><b>3FN</b></td><td>2FN e nada depende de outro atributo não-chave</td><td>dependências transitivas</td><td><code>cliente_nome</code> e <code>cliente_cidade</code> dentro de Pedido: dependem do cliente, não do pedido</td></tr>
    <tr><td><b>BCNF</b></td><td>todo determinante é uma <b>superchave</b></td><td>casos raros de chaves candidatas sobrepostas</td><td>versão mais rígida da 3FN</td></tr>
  </table></div>
  <div class="nota cuidado"><span class="lbl">Cuidado</span>Normalizar demais fragmenta o banco e custa JOINs (Capítulo 6). Por isso muitos sistemas de produção param na <b>3FN</b>, e às vezes <b>desnormalizam de propósito</b> por performance. É um trade-off, não um erro.</div>
  <div class="nota exemplo"><span class="lbl">Sua vez: exercício do slide</span>"Uma empresa quer guardar produtos, clientes e fornecedores. Quantas tabelas? Que relacionamentos?" Resposta de partida: <b>3 entidades, logo 3 tabelas</b>. Produto e fornecedor costumam ser N:1 (cada produto tem um fornecedor), e cliente e produto se ligam por meio de <b>pedidos</b>, que viram uma 4ª tabela (e uma tabela de itens, para o N:N). No Capítulo 2 você faz esse raciocínio com cardinalidade.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Dado</b> é o fato bruto; <b>informação</b> é o dado interpretado para responder uma pergunta.",
    "<b>SGBD</b> define, constrói, manipula e compartilha bancos. Resolve redundância, consistência, concorrência, segurança e backup.",
    "<b>Relacional</b> (Codd, 1970): tabelas sem ponteiros, ligadas por chaves. <b>PK</b> identifica a linha; <b>FK</b> aponta para a PK de outra tabela.",
    "<b>Normalização:</b> cada informação em um só lugar. Anomalias de inserção, atualização e exclusão.",
    "<b>1FN</b> atômico · <b>2FN</b> sem dependência parcial · <b>3FN</b> sem dependência transitiva · <b>BCNF</b> determinante é superchave.",
    "Na prática, a <b>3FN</b> é o ponto de equilíbrio. Desnormalizar é uma escolha consciente."]) + '''

  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Uma coluna <code>habilidades</code> guarda 'python, sql, aws' numa única célula. Qual forma normal ela viola?", [("a","2FN"),("b","1FN: o valor não é atômico."),("c","3FN")], "A 1FN exige valores indivisíveis. O ideal seria uma tabela de habilidades ligada ao funcionário. (No Capítulo 4 você vê por que filtrar essa coluna com LIKE é impreciso.)") + quiz(2, "c", "A cidade de um cliente aparece repetida em todos os pedidos dele. Que problema isso causa?", [("a","Anomalia de exclusão apenas."),("b","Nenhum, só ocupa espaço."),("c","Anomalia de atualização: mudar a cidade em uma linha deixa as outras desatualizadas.")], "É a redundância clássica. Basta esquecer uma cópia para o cliente 'morar' em duas cidades, como você viu no exemplo.") + quiz(3, "a", "A diferença entre PK e FK é:", [("a","PK identifica unicamente a linha na própria tabela; FK guarda a PK de outra tabela para ligá-las."),("b","PK é opcional e FK é obrigatória."),("c","As duas identificam a linha na própria tabela.")], "Toda tabela tem uma PK. A FK é a ponte que cria o relacionamento e permite ao SGBD impedir ligações para linhas que não existem.") + flash([
    ("O que é um SGBD?", "O software que define, constrói, manipula e compartilha bancos de dados (DBMS em inglês)."),
    ("Por que 'sem ponteiros'?", "No modelo relacional as tabelas se ligam pelos valores (chaves), e não por endereços de memória."),
    ("3FN em uma frase?", "Nenhum atributo não-chave depende de outro atributo não-chave: só da chave."),
    ("Quando desnormalizar?", "Quando a performance de leitura compensa a redundância, sabendo que é um trade-off.")]) + ponte("Já sei o que é um banco e por que normalizar. Como desenho o que vai dentro dele, antes de criar qualquer tabela?", "Com um diagrama que qualquer pessoa do negócio consegue ler: o modelo entidade-relacionamento.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter("banco-de-dados", 1, "dados-e-sgbd", T, "Dados, SGBD e normalização", "Capítulo 1 · Aula 1",
        "O que é um banco de dados, o que um SGBD faz por você e por que cada informação deve morar em um lugar só.",
        ["<b>~30 min</b>", "2 demos · 3 testes · 4 flashcards", "SQL executável"], body1, scripts=S, sql=True)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 você viu o que é um SGBD, o modelo relacional (tabelas, PK e FK) e por que cada dado deve morar em um lugar só. Ficou a pergunta: <i>antes de criar tabelas, como eu desenho o que o banco precisa guardar?</i>") + '''

<section class="sec" id="schema">
  <h2><span class="sn">1</span>Schema, estado e os três níveis de modelo</h2>
  <p class="gancho">"Modelar" quer dizer o quê, exatamente?</p>
  <p>Um <b>modelo de dados</b> descreve a <b>estrutura</b> do banco usando conceitos de <b>abstração</b>, que escondem detalhes de armazenamento. Essa estrutura (nomes de tabelas, colunas, tipos, restrições) é o <abbr class="gl" data-def="Descrição do banco: tabelas, colunas, tipos e regras. Não são os dados em si.">schema</abbr>. Os dados que estão lá em um dado momento são o <b>estado</b> (ou <i>snapshot</i>). Ao criar o banco, o estado inicial é <b>vazio</b>; a cada alteração o estado muda, e o SGBD garante que ele sempre respeite o schema.</p>
  <p>A modelagem acontece em três níveis, cada um respondendo uma pergunta:</p>
  <div class="grid3">
    <div class="card rv"><b style="color:var(--c0)">Conceitual</b><p><mark class="hl b">O que</mark> vai ser salvo? Entidades, atributos e relacionamentos, na visão do usuário. Independe de SGBD.</p></div>
    <div class="card rv"><b style="color:var(--c1)">Lógico</b><p><mark class="hl">Como</mark> vai ser salvo? Tabelas, chaves, tipos de dados e relacionamentos.</p></div>
    <div class="card rv"><b style="color:var(--c2)">Físico</b><p><mark class="hl g">Onde</mark> vai ser salvo? A implementação num SGBD específico, normalmente em SQL (<code>CREATE TABLE</code>).</p></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O nível conceitual não tem tabelas nem tipos. Do que ele é feito?</div><p>De três peças, e um diagrama para enxergá-las.</p></div>
</section>

<section class="sec" id="mer">
  <h2><span class="sn">2</span>Entidade, atributo e relacionamento</h2>
  <p class="gancho">Três substantivos e um verbo descrevem quase qualquer negócio.</p>
  <p>O <b>Modelo Entidade-Relacionamento (MER)</b>, criado por Peter Chen em um artigo no MIT, descreve a base com:</p>
  <ul>
    <li><b>Entidade:</b> um objeto da vida real sobre o qual guardamos dados. Ex.: Funcionário, Empresa, Aluno.</li>
    <li><b>Atributo:</b> uma propriedade da entidade. Ex.: nome e salário do Funcionário.</li>
    <li><b>Relacionamento:</b> a ligação entre entidades. Ex.: um funcionário <i>trabalha em</i> uma empresa.</li>
  </ul>
  <p>O <b>DER</b> (Diagrama de Entidade e Relacionamento) é a representação gráfica do MER, com uma noção espacial: retângulos para entidades, losangos para relacionamentos, elipses para atributos. Ferramentas CASE para desenhar: <b>brModelo</b> (gratuita, feita por universidades brasileiras, usada na disciplina), StarUML, DBDesigner (embutido no MySQL Workbench), Astah e Erwin.</p>
  <div class="ex rv"><span class="t">Exemplo do material: loja de roupas</span>
    <div class="l"><div><b>Entidades:</b> Cliente, Produto, Pedido.</div></div>
    <div class="l"><div><b>Relacionamento:</b> Compra (liga Cliente a Pedido, e Pedido a Produto).</div></div>
    <div class="l"><div><b>Atributos de Cliente:</b> nome, CPF, e-mail. Cada entidade ganha os seus.</div></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Um cliente faz quantos pedidos? Um produto está em quantos pedidos?</div><p>Essa pergunta tem nome: cardinalidade. E decide quantas tabelas você vai precisar.</p></div>
</section>

<section class="sec" id="cardinalidade">
  <h2><span class="sn">3</span>Cardinalidade: quantos de cada lado?</h2>
  <p class="gancho">A pergunta que define tudo: "quantos elementos de um lado podem se relacionar com um elemento do outro?"</p>
  <p>Cardinalidade é a quantidade <b>máxima e mínima</b> de registros de uma entidade que podem se relacionar com uma instância da outra. Clique em cada tipo e veja as linhas ligando os registros:</p>
  <div class="demo" data-demo="cardinal"></div>
  <h3>A notação (mín, máx), a mais usada</h3>
  <p>O professor destaca a notação <b>(mínimo, máximo)</b>, que é a do brModelo. Ela descreve a <b>participação</b> de cada entidade no relacionamento:</p>
  <div class="tablewrap"><table>
    <tr><th>Notação</th><th>Leitura</th><th>Exemplo</th></tr>
    <tr><td><code>(0,1)</code></td><td>nenhum ou no máximo um</td><td>um funcionário é chefe de nenhum ou de no máximo 1 departamento</td></tr>
    <tr><td><code>(1,1)</code></td><td>exatamente um</td><td>um funcionário trabalha em exatamente 1 departamento</td></tr>
    <tr><td><code>(1,n)</code></td><td>um ou mais</td><td>um funcionário participa de um ou mais projetos</td></tr>
    <tr><td><code>(0,n)</code></td><td>zero ou mais</td><td>(complemento) um cliente pode ter zero ou vários pedidos</td></tr>
  </table></div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Confundir "um ou mais" com "zero ou mais".</b> "Um ou mais" é mínimo <b>1</b>: <code>(1,n)</code>. "Zero ou mais" é <code>(0,n)</code>. No exercício da startup, "cada programa pode conter um ou mais projetos" é <code>(1,n)</code>, e não <code>(0,n)</code>. É um dos lugares onde mais se erra.</div>
  <div class="nota lembra"><span class="lbl">Lembra (complemento)</span>Existe outra notação muito vista em ferramentas de mercado: o <b>pé de galinha</b> (<i>crow's foot</i>), em que o lado "muitos" vira um tridente. É o mesmo conceito com outro desenho; o brModelo usa (mín, máx).</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Hora de aplicar. Como ficam as entidades de uma startup que aloca funcionários em projetos?</div><p>Esse é o cenário que vai atravessar o resto da disciplina.</p></div>
</section>

<section class="sec" id="startup">
  <h2><span class="sn">4</span>A startup alpha: modelando de verdade</h2>
  <p class="gancho">Pense como o banco: o que existe, e como se liga?</p>
  <p>Cenário da aula: uma startup de tecnologia precisa de um banco para os <b>projetos</b> que desenvolve para clientes. Cada projeto aloca <b>um ou mais funcionários</b>, e os projetos derivam de <b>programas</b> (áreas de conhecimento parecidas, como IA ou cloud). Cada programa pode ter vários projetos. Os requisitos do exercício, como um checklist:</p>
  <div class="thread rv" data-demo="checks" data-key="startup">
    <div class="nd" data-n="1"><b>Funcionário</b> participa de 1 ou mais projetos.<br><label><input type="checkbox"> modelei</label></div>
    <div class="nd" data-n="2"><b>Projeto</b> tem 1 ou mais funcionários. Logo, funcionário × projeto é <b>N:N</b>, (1,n) dos dois lados.<br><label><input type="checkbox"> modelei</label></div>
    <div class="nd" data-n="3"><b>Projeto</b> está vinculado a um <b>único programa</b>: lado do projeto é (1,1).<br><label><input type="checkbox"> modelei</label></div>
    <div class="nd" data-n="4"><b>Programa</b> contém um ou mais projetos: lado do programa é (1,n).<br><label><input type="checkbox"> modelei</label></div>
    <div class="nd" data-n="5">Atributos: <b>funcionário</b> (nome, sobrenome, CPF); <b>projeto</b> (código, nome, descrição, data de início e de término); <b>programa</b> (código, nome, sigla, descrição).<br><label><input type="checkbox"> modelei</label></div>
    <p class="muted" style="margin:6px 0 0"><b class="chk-n">0 de 5</b> requisitos conferidos no seu diagrama.</p>
  </div>
  <h3>Do N:N para tabelas</h3>
  <p>Um relacionamento <b>N:N</b> não cabe numa tabela só. Um funcionário em vários projetos e um projeto com vários funcionários exige uma <mark class="hl">tabela associativa</mark> (ou "tabela ponte") no meio, cuja PK é composta pelas duas chaves. Essa tabela ainda pode guardar dados <i>do relacionamento</i>, como as horas de cada pessoa em cada projeto. Você vai criá-la no Capítulo 3. Veja a ideia com os dados reais da startup:</p>
  <div class="demo" data-demo="ponte"></div>
  <div class="nota exemplo"><span class="lbl">Exercício da ACME, pensando junto</span>Departamentos têm nome, número único e um chefe (funcionário), com data de início na chefia. Funcionários têm nome, CPF, endereço, salário, sexo e nascimento, trabalham em <b>um</b> departamento e participam de <b>vários</b> projetos (com as horas por projeto). Cada departamento <b>controla</b> projetos, que têm nome, id único e uma única localização. Há dependentes, com vínculo (filho, filha). <b>Entidades:</b> Departamento, Funcionário, Projeto, Dependente. <b>Relacionamentos:</b> Chefia (1:1), Lotação (1:N), Controle (1:N, departamento e projetos), Participação (N:N, com horas), Dependência (1:N). As "várias regiões" (localizações) de um departamento viram uma entidade ou tabela própria, porque são vários valores.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Schema</b> é a estrutura; <b>estado</b> é o conteúdo de agora. O SGBD garante que o estado respeite o schema.",
    "<b>Conceitual</b> (o quê) → <b>lógico</b> (como) → <b>físico</b> (onde, em SQL).",
    "<b>Entidade</b> (objeto), <b>atributo</b> (propriedade) e <b>relacionamento</b> (ligação). O DER é o desenho do MER.",
    "Cardinalidade: <b>1:1</b>, <b>1:N</b>, <b>N:1</b> e <b>N:N</b>. Notação (mín, máx): (0,1), (1,1), (1,n).",
    "<b>N:N</b> vira uma <b>tabela associativa</b> com PK composta.",
    "\"Um ou mais\" é (1,n), e <b>não</b> (0,n)."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Em qual nível de modelo aparece o <code>CREATE TABLE</code>?", [("a","Conceitual."),("b","Físico (a implementação no SGBD)."),("c","Em nenhum: é só código de aplicação.")], "O conceitual descreve o que guardar, o lógico define como (tabelas, chaves, tipos) e o físico é a implementação em SQL.") + quiz(2, "c", "Cada programa pode ter 'um ou mais' projetos. Qual a cardinalidade do lado do programa?", [("a","(0,n)"),("b","(1,1)"),("c","(1,n)")], "'Um ou mais' é mínimo 1 e máximo n. (0,n) seria 'zero ou mais', e (1,1) seria 'exatamente um'.") + quiz(3, "a", "Funcionário e projeto são N:N. Como isso vira tabelas?", [("a","Uma terceira tabela associativa, com PK composta pelas duas chaves."),("b","Uma coluna 'projetos' na tabela de funcionários, com uma lista."),("c","Duas tabelas, cada uma com uma coluna do outro lado.")], "A lista numa coluna fere a 1FN, e duas colunas cruzadas não resolvem o N:N. A tabela associativa é o padrão.") + flash([
    ("Schema x estado?", "Schema é a estrutura (descrição). Estado é o conteúdo do banco em um dado momento."),
    ("Entidade em uma frase?", "Um objeto da vida real sobre o qual guardamos dados, como Funcionário ou Projeto."),
    ("O que significa (1,n)?", "Participação mínima 1 e máxima n: um ou mais."),
    ("Por que o N:N precisa de uma tabela ponte?", "Porque uma linha não pode apontar para vários valores sem ferir a 1FN. A associativa guarda um par por linha.")]) + ponte("O desenho está pronto no papel. Como ele vira tabelas de verdade, com regras que o banco faz valer?", "Com o modelo lógico e a linguagem de definição de dados, a DDL.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter("banco-de-dados", 2, "modelagem-er", T, "Modelagem entidade-relacionamento", "Capítulo 2 · Aula 2",
        "Desenhar o banco antes de criar qualquer tabela: entidades, atributos, relacionamentos e quantos de cada lado.",
        ["<b>~35 min</b>", "2 demos · 1 checklist · 3 testes", "sem DDL neste capítulo"], body2, scripts=S + ["demos/cap-2.js"], sql=False)
print("caps 1-2 ok")
