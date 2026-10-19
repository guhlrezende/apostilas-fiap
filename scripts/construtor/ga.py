import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *

PASTA = "gestao-agil"
TITULO = "Gestão Ágil e Pitch"
T = TITULO
S = ["demos/agil.js"]
CAPS = [
 dict(n=1, file="cap-1-trabalho-invisivel.html", titulo="Por que projetos de IA falham", aula="Aulas 2 e 3", tempo=40,
      resumo="O caso do modelo com 92% de acurácia que não serviu, métricas que importam e o trabalho invisível.",
      pergunta="Como deixar o trabalho visível e manter o cliente por perto? Com um framework: o Scrum."),
 dict(n=2, file="cap-2-scrum.html", titulo="O framework Scrum", aula="Aulas 2 e 3", tempo=50,
      resumo="Origem, pilares, valores, papéis, artefatos e eventos, com a Sprint como ciclo de aprendizado.",
      pergunta="O Product Backlog precisa de itens bem escritos. Como se escreve um item que todos entendem do mesmo jeito?"),
 dict(n=3, file="cap-3-user-story.html", titulo="User Story, critérios de aceite e Done", aula="Aulas 2 e 3", tempo=45,
      resumo="Como escrever história, critério e tarefa, definir a meta da Sprint e saber o que é pronto de verdade.",
      pergunta="Com histórias claras, falta organizar o fluxo de trabalho. Quanto trabalho em paralelo é demais?"),
 dict(n=4, file="cap-4-kanban-e-wip.html", titulo="Kanban e limite de trabalho em andamento", aula="Aula 3", tempo=40,
      resumo="O quadro, a diferença entre Scrum, Kanban e ferramenta, e por que começar menos termina mais.",
      pergunta="O trabalho está visível e fluindo. Falta apresentá-lo em 5 minutos para quem decide."),
 dict(n=5, file="cap-5-pitch.html", titulo="O pitch de 5 minutos", aula="Aula 6", tempo=40,
      resumo="Regras de tempo, como montar os slides, o que dizer e o ensaio por segundos.",
      pergunta="O pitch explica o valor. Mas como mostrar a arquitetura a quem não programa?"),
 dict(n=6, file="cap-6-uml.html", titulo="UML: diagrama de componentes", aula="Aula 6", tempo=45,
      resumo="Por que desenhar, os tipos de diagrama, os símbolos e um exemplo completo com hardware, nuvem e painel.",
      pergunta=""),
]
manifest(PASTA, "gestao-agil", TITULO, CAPS)
hub(PASTA, TITULO, "Gestão Ágil, Scrum, Kanban, Pitch e UML", "Apostila de Gestão Ágil e Pitch",
    "Como organizar um projeto de IA em Sprints, escrever histórias que todos entendem, limitar o trabalho em andamento, apresentar em 5 minutos e desenhar a arquitetura.",
    ["<b>6</b> capítulos", "<b>~4h20</b> de estudo ativo", "simuladores de Sprint, WIP e pitch"],
    '<p>A história começa em um fracasso: um modelo de IA com <mark class="hl">92% de acurácia que ninguém conseguiu usar</mark>. Daí vêm as perguntas que organizam a apostila: como manter o trabalho visível (Scrum e Kanban), como dizer o que se quer construir (User Story e critérios de aceite), como saber que está pronto (Definition of Done), como mostrar para quem decide (pitch) e como explicar a arquitetura sem código (UML). Cada capítulo responde à pergunta que o anterior deixou.</p>',
    'O que veio da aula está marcado pelo número da aula. O que veio do <b>Guia do Scrum</b> e de boas práticas de mercado (limites de tempo dos eventos, INVEST, lei de Little) está marcado como <b>complemento</b>. Os números dos simuladores foram conferidos por simulação independente.')

# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo. Sem pressupostos: basta saber que um modelo de IA é avaliado por métricas. Ele mostra por que um projeto pode ter métrica boa e ainda assim falhar, e é a razão de existir de tudo que vem depois.", "Ponto de partida") + '''
<section class="sec" id="caso">
  <h2><span class="sn">1</span>O caso dos 92%</h2>
  <p class="gancho">Boa acurácia, projeto fracassado.</p>
  <p>Uma empresa pediu a uma equipe uma solução de IA para <b>classificar automaticamente as solicitações do atendimento ao cliente</b> e identificar as mais <b>urgentes</b>. Depois de várias semanas, a equipe entregou um modelo com <b>92% de acurácia</b>. Só que a solução <b>não identificava corretamente as solicitações urgentes</b> (o objetivo do projeto) e <b>não podia ser integrada</b> ao sistema usado pelos atendentes.</p>
  <p>Pergunta: o projeto foi bem-sucedido? O que a equipe poderia ter feito <i>durante</i> o desenvolvimento para descobrir esses problemas antes da entrega final?</p>
  <div class="grid2">
    <div class="card rv"><b>O que deu errado</b><p>Faltaram critérios de sucesso combinados com a empresa; só se olhou a acurácia, e não métricas das urgentes; a integração com o sistema dos atendentes não foi verificada cedo; nada foi mostrado ao cliente até o fim.</p></div>
    <div class="card rv"><b>O que teria ajudado</b><p>Definir critérios de sucesso antes de codar; medir <b>precisão, recall e F1</b> para os casos urgentes; protótipos e versões parciais regulares; feedback contínuo de empresa e usuários; pensar em valor e possibilidade de uso, e não só em desempenho técnico.</p></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Como um modelo pode ter 92% de acurácia e falhar justamente no que importa?</div><p>Com um número e uma tabela.</p></div>
</section>

<section class="sec" id="metricas">
  <h2><span class="sn">2</span>Por que a acurácia enganou</h2>
  <p class="gancho">Quando uma classe é rara, acertar o comum é fácil.</p>
  <p>Suponha (números ilustrativos) que, de <b>1.000</b> solicitações, <b>80</b> sejam urgentes. Um "modelo" que sempre responde <i>não urgente</i> acerta 920 de 1.000: <b>92%</b> de acurácia, sem aprender nada e sem nunca achar uma urgente. Mexa nos controles e compare com outros modelos:</p>
  <div class="demo" data-demo="acuracia"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: a matriz de confusão do modelo do caso</span>
    <div class="l"><div>Das <b>80</b> urgentes, o modelo acertou <b>10</b> (VP = 10) e errou <b>70</b> (FN = 70). Das <b>920</b> não urgentes, marcou <b>10</b> como urgentes (FP = 10) e acertou <b>910</b> (VN = 910).</div></div>
    <div class="l"><div><b>Acurácia</b> = (VP + VN) / total = (10 + 910) / 1.000 = <b>92%</b>.</div></div>
    <div class="l"><div><b>Precisão</b> (dos que ele chamou de urgentes, quantos eram) = VP / (VP + FP) = 10 / 20 = <b>50%</b>.</div></div>
    <div class="l"><div><b>Recall</b> (das urgentes reais, quantas ele achou) = VP / (VP + FN) = 10 / 80 = <b>12,5%</b>.</div></div>
    <div class="l"><div><b>F1</b> = 2·precisão·recall / (precisão + recall) = 2·0,5·0,125 / 0,625 = <b>0,20</b>.</div></div>
    <div class="l"><div>Leitura: a acurácia diz 92%; o F1 das urgentes diz 0,20. O número que importa depende do objetivo do negócio, e o objetivo aqui era <b>achar as urgentes</b>.</div></div>
  </div>
  <div class="nota lembra"><span class="lbl">Regra prática</span>Com classe rara, <b>sempre compare a acurácia com o chute da classe majoritária</b> e olhe recall e precisão da classe que importa. É o mesmo assunto da apostila de Machine Learning, agora como problema de gestão.</div>
</section>

<section class="sec" id="invisivel">
  <h2><span class="sn">3</span>O verdadeiro problema: trabalho invisível</h2>
  <p class="gancho">Código continuar sendo escrito não significa que o projeto vai bem.</p>
  <p>O alerta não é "não sabemos o que fazer". É <b>"cada pessoa entendeu uma coisa diferente"</b>: parece normal até o retrabalho aparecer. Antes de decidir tecnologia ou arquitetura, uma pergunta precisa estar respondida: <b>qual problema estamos tentando resolver?</b> O caminho entre o problema e o valor tem etapas, e em cada seta o contexto pode se perder:</p>
  <div class="tl rv">
    <div class="ev"><b>Problema</b><span>O que dói, para quem?</span></div>
    <div class="ev"><b>Necessidade</b><span>O que a pessoa precisa conseguir fazer?</span></div>
    <div class="ev"><b>User Story</b><span>A necessidade escrita para todos entenderem igual (Capítulo 3).</span></div>
    <div class="ev"><b>Sprint</b><span>O ciclo curto em que se constrói e se aprende (Capítulo 2).</span></div>
    <div class="ev"><b>Valor</b><span>O que ficou utilizável e útil.</span></div>
  </div>
  <div class="nota lembra"><span class="lbl">A primeira Sprint pode não ter tela</span>Contrariando a intuição de que "Sprint = funcionalidade entregue", a primeira pode gerar valor só <b>reduzindo incerteza</b>: validar regras de negócio, entender o domínio, identificar risco técnico, prototipar. <b>Clareza também é uma entrega.</b></div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Acurácia alta não basta</b>: com classe rara, o chute da maioria já acerta muito (aqui, 92%).",
    "<b>Precisão</b> = VP/(VP+FP). <b>Recall</b> = VP/(VP+FN). <b>F1</b> = média harmônica. Meça na classe que importa.",
    "Falhas do caso: sem critérios de sucesso, sem métricas das urgentes, integração não verificada, sem feedback contínuo.",
    "O perigo é o <b>trabalho invisível</b>: cada um entendeu uma coisa. Caminho: problema → necessidade → história → Sprint → valor.",
    "A primeira Sprint pode ser só <b>reduzir incerteza</b>. Clareza também é entrega."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que 92% de acurácia pode ser enganoso em um problema com 8% de casos urgentes?", [("a","Porque 92% é sempre um número baixo."),("b","Porque um modelo que nunca marca nada como urgente já acerta 92%."),("c","Porque a acurácia não pode ser calculada com duas classes.")], "Quando uma classe é rara, acertar a maioria é fácil. O que importa é o desempenho na classe rara (recall e precisão).") + quiz(2, "a", "Qual métrica diz quantas das urgentes reais o modelo encontrou?", [("a","Recall."),("b","Precisão."),("c","Acurácia.")], "Recall = VP / (VP + FN): dos que eram urgentes de verdade, quantos o modelo achou.") + quiz(3, "c", "O que significa 'trabalho invisível' na gestão de projetos?", [("a","Trabalho feito fora do horário."),("b","Código sem comentários."),("c","Pessoas trabalhando com entendimentos diferentes do mesmo problema, sem perceber.")], "O sinal de alerta é cada um ter entendido uma coisa diferente: o retrabalho só aparece depois.") + flash([
    ("O que é o F1?", "A média harmônica de precisão e recall: só é alto se os dois forem."),
    ("O que a primeira Sprint pode entregar sem tela?", "Redução de incerteza: regras de negócio validadas, domínio entendido, riscos técnicos identificados."),
    ("Qual a pergunta que vem antes de qualquer tecnologia?", "Qual problema estamos tentando resolver?"),
    ("O que a equipe do caso deveria ter feito?", "Definir critérios de sucesso com o cliente, medir métricas específicas e mostrar protótipos com frequência.")]) + ponte("Como deixar o trabalho visível e manter o cliente por perto?", "Com um framework de ciclos curtos e feedback: o Scrum.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "trabalho-invisivel", T, "Por que projetos de IA falham", "Capítulo 1 · Aulas 2 e 3",
        "Um modelo com 92% de acurácia que não serviu, e o que isso ensina sobre gestão.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "matriz de confusão interativa"], body1, scripts=S)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 o projeto falhou porque o trabalho estava invisível e o cliente longe. O <b>Scrum</b> é um framework feito para o contrário: ciclos curtos, inspeção constante e feedback de quem usa o produto.") + '''
<section class="sec" id="origem">
  <h2><span class="sn">1</span>De onde vem e quando usar</h2>
  <p class="gancho">Um nome emprestado do rugby.</p>
  <p>O Scrum se inspira no artigo <i>The New New Product Development Game</i> (1986), de Ikujiro Nonaka e Hirotaka Takeuchi, que descreve equipes <b>pequenas, multidisciplinares e auto-organizadas</b> desenvolvendo produtos complexos. A metáfora é a do <i>scrum</i> do rugby: o time avança junto. Nos anos 1990, Jeff Sutherland e Ken Schwaber estruturaram essas ideias no framework que se conhece hoje.</p>
  <p>Ele serve a projetos de <b>alta incerteza</b>, como software e IA, com abordagem <b>iterativa</b>: ciclos curtos de entrega e feedback constante, o que reduz desperdício e expõe gargalos cedo.</p>
</section>

<section class="sec" id="pilares">
  <h2><span class="sn">2</span>Pilares e valores</h2>
  <p class="gancho">A base de tudo é inspecionar e se adaptar.</p>
  <div class="grid2">
    <div class="card rv"><b>3 pilares</b><p><b>Transparência</b>: as informações são acessíveis a todos os envolvidos. <b>Inspeção</b>: verificações constantes do andamento. <b>Adaptação</b>: ajustes conforme o que a inspeção mostrar.</p></div>
    <div class="card rv"><b>5 valores</b><p><b>Compromisso, foco, abertura, respeito e coragem.</b> Sem abertura não há transparência; sem coragem, ninguém levanta o problema que a inspeção encontrou.</p></div>
  </div>
</section>

<section class="sec" id="papeis">
  <h2><span class="sn">3</span>Os três papéis</h2>
  <p class="gancho">Responsabilidade, não hierarquia.</p>
  <ul>
    <li><b>Product Owner (PO)</b>: maximiza o valor do produto. Ordena as prioridades, mantém o <b>Product Backlog</b> compreensível e <b>representa os stakeholders</b> (clientes, usuários finais, investidores, gerentes e líderes de negócio, reguladores).</li>
    <li><b>Scrum Master (SM)</b>: ajuda o time a melhorar o processo. Facilita, remove impedimentos e estimula a melhoria contínua. Não é chefe.</li>
    <li><b>Developers</b>: transformam a necessidade em um <b>incremento utilizável</b>. Planejam a Sprint, constroem, testam e validam. São autogerenciáveis. Em um curso com empresa parceira, o Scrum Master costuma ser um integrante do grupo, que também desenvolve (isso é a regra do curso, e não do Scrum).</li>
  </ul>
  <div class="card sorter rv" data-demo="sorter" data-opts="po:Product Owner|sm:Scrum Master|dev:Developers">
    <div class="item" data-ans="po"><p>Ordena o Product Backlog e decide o que traz mais valor.</p><span class="why">Maximizar valor e gerenciar o Backlog é o papel do PO.</span></div>
    <div class="item" data-ans="sm"><p>Percebe que o time está travado esperando um acesso e resolve o impedimento.</p><span class="why">Remover impedimentos e facilitar o processo é o papel do Scrum Master.</span></div>
    <div class="item" data-ans="dev"><p>Constrói, testa e valida o incremento da Sprint.</p><span class="why">Transformar a necessidade em incremento utilizável é dos Developers.</span></div>
    <div class="item" data-ans="po"><p>Conversa com clientes e usuários para captar e priorizar as demandas.</p><span class="why">O PO é o principal representante dos stakeholders dentro do time.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <h3>Que competências um time de IA precisa?</h3>
  <p>Observando um projeto de IA, os Developers juntos precisam cobrir: entendimento do <b>problema de negócio</b>; <b>engenharia e análise de dados</b>; <b>desenvolvimento e avaliação de modelos</b>; <b>software, API ou interface</b>; <b>testes e documentação</b>; <b>comunicação com os stakeholders</b>; e <b>ética, privacidade e análise de riscos</b>. É o eixo negócio → dados → modelo → produto → risco. Boa pergunta para dividir responsabilidades: quem do time cobre cada uma?</p>
</section>

<section class="sec" id="artefatos">
  <h2><span class="sn">4</span>Os artefatos: três perguntas</h2>
  <p class="gancho">Cada artefato responde a uma pergunta.</p>
  <div class="tablewrap"><table>
    <tr><th>Artefato</th><th>Pergunta</th><th>Quem cuida</th></tr>
    <tr><td><b>Product Backlog</b></td><td>O que pode gerar valor?</td><td>PO: lista ordenada de tudo que o produto precisa</td></tr>
    <tr><td><b>Sprint Backlog</b></td><td>O que faremos agora?</td><td>Developers: itens escolhidos para a Sprint e o plano para entregá-los</td></tr>
    <tr><td><b>Incremento</b></td><td>O que ficou utilizável?</td><td>Developers: o resultado entregável de cada Sprint</td></tr>
  </table></div>
  <p>Regra de ouro: <b>se algo "pronto" não pode ser demonstrado, ainda existe trabalho escondido</b>. Cada artefato tem também um compromisso (Guia do Scrum, complemento): o Product Backlog tem a <b>meta do produto</b>, o Sprint Backlog tem a <b>meta da Sprint</b> e o Incremento tem a <b>Definition of Done</b> (Capítulo 3).</p>
</section>

<section class="sec" id="eventos">
  <h2><span class="sn">5</span>Os eventos e a Sprint</h2>
  <p class="gancho">A Sprint é um ciclo de aprendizado, não um prazo.</p>
  <p>O objetivo de uma Sprint não é cumprir tarefas: é <b>aprender rápido se o que está sendo construído resolve o problema</b>. O ciclo é <i>planejar → executar → revisar → adaptar</i>, e a Sprint dura <b>no máximo um mês</b>. Percorra os quatro eventos (os limites de tempo são <b>complemento</b> (vêm do Guia do Scrum, e não do slide) e valem para uma Sprint de 1 mês):</p>
  <div class="demo" data-demo="ciclo"></div>
  <div class="nota cuidado"><span class="lbl">Erro comum: Review não é relatório</span>A Sprint Review não é uma cerimônia para mostrar que "fizemos tudo". É o momento de <b>colocar o produto na frente de quem usa</b> e deixar o feedback mudar o Backlog. Se nada mudou depois da Review, ela não cumpriu seu papel.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Scrum</b>: times pequenos, ciclos curtos, feedback. Origem em Nonaka e Takeuchi (1986); estruturado por Sutherland e Schwaber nos anos 1990.",
    "<b>3 pilares</b>: transparência, inspeção, adaptação. <b>5 valores</b>: compromisso, foco, abertura, respeito, coragem.",
    "<b>PO</b> (valor e Backlog), <b>SM</b> (processo e impedimentos), <b>Developers</b> (incremento). Papéis, não chefias.",
    "<b>Artefatos</b>: Product Backlog (o que pode gerar valor?), Sprint Backlog (o que faremos agora?), Incremento (o que ficou utilizável?).",
    "<b>Eventos</b>: Planning, Sprint (com Daily), Review, Retrospective. Sprint de até 1 mês."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Qual evento olha para o processo de trabalho, e não para o produto?", [("a","Sprint Review."),("b","Sprint Retrospective."),("c","Sprint Planning.")], "A Retrospective inspeciona como o time trabalha e define melhorias. A Review inspeciona o produto.") + quiz(2, "c", "Quem representa os stakeholders dentro do time Scrum?", [("a","O Scrum Master."),("b","Os Developers."),("c","O Product Owner.")], "O PO capta e prioriza as demandas dos stakeholders no Product Backlog.") + quiz(3, "a", "Qual pergunta o Sprint Backlog responde?", [("a","O que faremos agora?"),("b","O que pode gerar valor?"),("c","O que ficou utilizável?")], "Product Backlog é 'o que pode gerar valor'; Incremento é 'o que ficou utilizável'.") + flash([
    ("Quais os 3 pilares do Scrum?", "Transparência, inspeção e adaptação."),
    ("O que faz o Scrum Master?", "Facilita o processo, remove impedimentos e estimula a melhoria contínua. Não é chefe."),
    ("Qual o objetivo de uma Sprint?", "Aprender rápido se o que está sendo construído resolve o problema, e não apenas cumprir tarefas."),
    ("Quanto dura uma Sprint?", "No máximo um mês.")]) + ponte("O Product Backlog precisa de itens bem escritos. Como se escreve um item que todos entendem do mesmo jeito?", "Com a User Story.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "scrum", T, "O framework Scrum", "Capítulo 2 · Aulas 2 e 3",
        "Pilares, valores, papéis, artefatos e eventos do Scrum.",
        ["<b>~50 min</b>", "2 demos · 3 testes · 4 flashcards", "percorra o ciclo da Sprint"], body2, scripts=S)

# ---------------- CAP 3 ----------------
body3 = recap("No Capítulo 2 você viu que o Product Backlog é uma lista ordenada do que pode gerar valor. Agora, <b>como se escreve cada item</b> para que o PO, o time e o cliente entendam igual, como se prioriza e como se sabe que algo está <b>pronto de verdade</b>.") + '''
<section class="sec" id="story">
  <h2><span class="sn">1</span>A User Story</h2>
  <p class="gancho">Uma frase com papel, ação e benefício.</p>
  <p>A técnica é escrever o item como <b>"Como &lt;papel&gt;, quero &lt;ação&gt;, para &lt;benefício&gt;"</b>. Ela força a pergunta que evita trabalho invisível: <i>quem precisa, do quê, e para quê?</i> Exemplo clássico: "Como aluno, quero ver minhas notas no portal para acompanhar meu desempenho."</p>
  <p>Toda história pode (e deve) vir com <b>critérios de aceite</b>: regras objetivas que dizem quando ela está <b>pronta</b>. No exemplo: mostrar as notas de todas as disciplinas; exibir a média final e o status (aprovado ou reprovado). Monte a sua:</p>
  <div class="demo" data-demo="story"></div>
  <div class="nota lembra"><span class="lbl">Complemento: INVEST</span>Uma boa história costuma ser <b>I</b>ndependente, <b>N</b>egociável, <b>V</b>aliosa, <b>E</b>stimável, <b>P</b>equena (<i>small</i>) e <b>T</b>estável. Se não dá para testar, o critério de aceite está vago. Uma forma comum de escrever critérios testáveis é <i>Dado</i> (contexto), <i>Quando</i> (ação), <i>Então</i> (resultado): "Dado que a biblioteca tem 120 livros emprestados e 15 em atraso, quando a bibliotecária abre o painel, então vê os dois totais e a lista dos atrasados."</div>
</section>

<section class="sec" id="tres">
  <h2><span class="sn">2</span>História, critério e tarefa não são a mesma coisa</h2>
  <p class="gancho">Três camadas, três perguntas.</p>
  <ul>
    <li><b>User Story</b>: representa <b>valor</b>. "Como gestor da frota, quero visualizar o custo consolidado dos veículos para entender onde os recursos estão sendo consumidos."</li>
    <li><b>Critério de aceite</b>: define <b>como validar</b> esse valor. "Apresentar o custo total", "permitir ver o custo por veículo".</li>
    <li><b>Tarefa</b>: o <b>trabalho técnico</b> para entregar. "Definir os campos", "tratar os dados", "implementar o cálculo", "construir a visualização".</li>
  </ul>
  <div class="card sorter rv" data-demo="sorter" data-opts="us:User Story|ca:Critério de aceite|tf:Tarefa">
    <div class="item" data-ans="us"><p>Como bibliotecária, quero ver os livros em atraso para decidir quem avisar.</p><span class="why">Papel, ação e benefício: é a história, a unidade de valor.</span></div>
    <div class="item" data-ans="ca"><p>A lista deve mostrar o título, o aluno e os dias de atraso, do maior para o menor.</p><span class="why">Regra verificável que diz quando a história está pronta: critério de aceite.</span></div>
    <div class="item" data-ans="tf"><p>Criar a tabela de empréstimos no banco e escrever a consulta que calcula os dias de atraso.</p><span class="why">Trabalho técnico necessário: tarefa.</span></div>
    <div class="item" data-ans="ca"><p>A tela deve destacar em vermelho os atrasos acima de 7 dias.</p><span class="why">É uma condição de aceite: dá para olhar e dizer se está certo ou errado.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <p>Uma boa tarefa continua conectada à história. Se ninguém sabe responder <b>"por que estamos fazendo isso?"</b>, o trabalho já ficou invisível.</p>
</section>

<section class="sec" id="prioridade">
  <h2><span class="sn">3</span>Prioridade e meta da Sprint</h2>
  <p class="gancho">Importante não é o mesmo que "para agora".</p>
  <p>Uma funcionalidade pode ser importante e ainda assim não precisar ser feita agora. A priorização pesa quatro coisas: <b>valor</b> (impacto para o usuário), <b>risco</b> (o que precisa ser validado cedo), <b>dependência</b> (o que destrava outras partes) e <b>esforço</b> (cabe neste ciclo?).</p>
  <p>A <b>meta da Sprint</b> é o filtro. Exemplo: <i>"Até o final da Sprint, queremos permitir que o gestor visualize o custo consolidado da frota e identifique onde estão as principais fontes de desperdício."</i> Se uma tarefa não contribui para a meta, provavelmente não pertence a esta Sprint.</p>
</section>

<section class="sec" id="done">
  <h2><span class="sn">4</span>"Concluído" não é "Done"</h2>
  <p class="gancho">Rodou na minha máquina não é pronto.</p>
  <p>"Concluído", para muitos, é "rodou na minha máquina". <b>Done</b> é o que está <b>integrado, testado, validado e pronto para demonstrar</b>. A <b>Definition of Done</b> (DoD) é a lista, combinada <b>antes</b> de começar, que diz o que "pronto" significa para o time. Um exemplo de DoD:</p>
  <ul>
    <li>critérios de aceite atendidos;</li>
    <li>código integrado ao repositório principal;</li>
    <li>testes executados e passando;</li>
    <li>resultado validado (com o PO ou com dados reais);</li>
    <li>evidência anexada (print, log, relatório);</li>
    <li>revisado por outra pessoa do time.</li>
  </ul>
  <div class="nota cuidado"><span class="lbl">Cuidado</span>Definir a DoD <b>depois</b> de codar é o mesmo que escolher o critério de sucesso depois de ver o resultado. Combine antes, e escreva onde todos vejam.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>User Story</b>: Como &lt;papel&gt;, quero &lt;ação&gt;, para &lt;benefício&gt;. Representa <b>valor</b>.",
    "<b>Critério de aceite</b>: como validar o valor. <b>Tarefa</b>: o trabalho técnico. Três camadas, três perguntas.",
    "<b>Priorizar</b> pesa valor, risco, dependência e esforço. A <b>meta da Sprint</b> é o filtro do que entra.",
    "<b>Done</b> = integrado, testado, validado, demonstrável. A <b>DoD</b> se combina antes de começar.",
    "Complemento: INVEST e o formato Dado/Quando/Então ajudam a escrever critérios testáveis."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "'Criar a tabela de custos no banco' é...", [("a","Uma User Story."),("b","Um critério de aceite."),("c","Uma tarefa técnica, que só faz sentido se estiver ligada a uma história.")], "É trabalho para entregar o valor, e não o valor em si.") + quiz(2, "b", "Quando é o melhor momento de definir a Definition of Done?", [("a","Depois da entrega, quando se vê o resultado."),("b","Antes de começar a construir."),("c","Só se o cliente pedir.")], "A DoD é um acordo prévio. Definida depois, vira justificativa.") + quiz(3, "a", "Uma funcionalidade importante deve entrar sempre na Sprint atual?", [("a","Não: ela só entra se contribuir com a meta da Sprint e couber no ciclo."),("b","Sim, importância é o único critério."),("c","Sim, se for do PO.")], "Importante e urgente não são sinônimos; a meta da Sprint filtra.") + flash([
    ("Qual o formato de uma User Story?", "Como &lt;papel&gt;, quero &lt;ação&gt;, para &lt;benefício&gt;."),
    ("Para que servem os critérios de aceite?", "Para dizer, de forma objetiva, quando a história está pronta."),
    ("O que é Done?", "Integrado, testado, validado e pronto para demonstrar, seguindo a Definition of Done do time."),
    ("O que a meta da Sprint decide?", "O que entra e o que sai da Sprint: tarefas que não ajudam a meta provavelmente não pertencem a ela.")]) + ponte("Com histórias claras, falta organizar o fluxo de trabalho. Quanto trabalho em paralelo é demais?", "É a pergunta do Kanban.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "user-story", T, "User Story, critérios de aceite e Done", "Capítulo 3 · Aulas 2 e 3",
        "Escrever o item de backlog, validar o valor e saber quando está pronto.",
        ["<b>~45 min</b>", "2 demos · 3 testes · 4 flashcards", "construtor de história com checklist"], body3, scripts=S)
print("ga caps 1-3 ok")
