import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
import ga
PASTA, T, S = ga.PASTA, ga.T, ga.S

# ---------------- CAP 4 ----------------
body4 = recap("Com histórias claras e uma DoD combinada, o time tem <b>o que</b> fazer. O Capítulo 4 trata de <b>como o trabalho flui</b>: um quadro que torna o trabalho visível e um limite simples que impede o time de começar mais do que consegue terminar.") + '''
<section class="sec" id="tres-coisas">
  <h2><span class="sn">1</span>Scrum, Kanban e Trello</h2>
  <p class="gancho">Três coisas diferentes que se misturam na conversa.</p>
  <div class="grid2">
    <div class="card rv"><b>Scrum</b><p>Organiza o trabalho em <b>ciclos curtos</b> (Sprints), com meta, papéis e revisão.</p></div>
    <div class="card rv"><b>Kanban</b><p>Visualiza e melhora o <b>fluxo</b>: mostra o trabalho, expõe gargalos e limita o que está em andamento.</p></div>
  </div>
  <div class="nota lembra"><span class="lbl">E o Trello?</span>É uma <b>ferramenta visual</b> (um quadro de cartões). Ela não decide prioridade, valor ou qualidade por ninguém. Dá para usar o Trello para Scrum, para Kanban ou para nenhum dos dois.</div>
</section>

<section class="sec" id="quadro">
  <h2><span class="sn">2</span>O quadro de cinco colunas</h2>
  <p class="gancho">Cada coluna é um estado do trabalho.</p>
  <div class="tl rv">
    <div class="ev"><b>Product Backlog</b><span>O que pode gerar valor (o PO ordena).</span></div>
    <div class="ev"><b>Sprint Backlog</b><span>O que faremos nesta Sprint.</span></div>
    <div class="ev"><b>Em andamento</b><span>Alguém está trabalhando agora. Aqui vale o limite de WIP.</span></div>
    <div class="ev"><b>Em validação</b><span>O resultado atende ao critério de aceite? Alguém revisou? Há evidência?</span></div>
    <div class="ev"><b>Done</b><span>Atende à Definition of Done: demonstrável.</span></div>
  </div>
  <p>A coluna que mais exige conversa é a <b>"Em validação"</b>: é nela que aparecem as perguntas que o "concluído" esconde. Um cartão só entra em Done quando alguém consegue responder <i>sim</i> a todas.</p>
</section>

<section class="sec" id="wip">
  <h2><span class="sn">3</span>Limite de WIP: começar menos para terminar mais</h2>
  <p class="gancho">Muitas tarefas iniciadas não é o mesmo que muito valor entregue.</p>
  <p><b>WIP</b> (<i>work in progress</i>) é o trabalho começado e não terminado. Mais tarefas simultâneas significam mais troca de contexto, mais trabalho parado e <b>menos entregas finalizadas</b>. Um limite simples (por exemplo, no máximo 3 cartões em "Em andamento") expõe o gargalo cedo e muda a pergunta de "o que posso começar agora?" para <b>"o que podemos terminar antes de começar algo novo?"</b>.</p>
  <p>Veja com números. Uma equipe de <b>3 pessoas</b> tem <b>12 tarefas</b> de <b>3 dias</b> cada, e uma pessoa trabalha em uma tarefa de cada vez dentro dela (uma tarefa absorve no máximo uma pessoa). Mude o limite:</p>
  <div class="demo" data-demo="wip"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: três limites</span>
    <div class="l"><div><b>WIP = 3</b>: cada pessoa fica com uma tarefa e termina em 3 dias. Entregas aos 3, 6, 9 e 12 dias, três de cada vez. <b>Primeira entrega: 3 dias. Tempo médio até a entrega: 7,5 dias.</b></div></div>
    <div class="l"><div><b>WIP = 12</b>: todas começam no dia 0 e cada uma recebe 3/12 = 0,25 de dia de trabalho por dia. Todas terminam juntas no dia 12. <b>Primeira entrega: 12 dias. Tempo médio: 12 dias.</b></div></div>
    <div class="l"><div><b>WIP = 1</b>: uma tarefa de cada vez, e duas pessoas ficam sem tarefa. Entregas aos 3, 6, ..., 36 dias. <b>Tempo médio: 19,5 dias.</b></div></div>
    <div class="l"><div>O <b>trabalho total é o mesmo</b> (36 pessoas-dias). O WIP muda <b>quando</b> cada coisa fica pronta, e portanto quando o cliente pode dar feedback. O melhor aqui é WIP igual ao número de pessoas.</div></div>
  </div>
  <div class="nota lembra"><span class="lbl">Complemento: a lei de Little</span>Em um fluxo estável, <b>tempo médio no sistema = WIP / vazão</b>. Com WIP = 3 e vazão de 1 tarefa por dia, cada tarefa leva 3 dias <b>em andamento</b>, igual ao tempo da primeira entrega na simulação. O 'tempo médio até entregar' da demo (7,5 dias) é outra medida: conta desde o dia 0, incluindo a espera na fila. Para reduzir o tempo de entrega, ou aumenta-se a vazão, ou <b>reduz-se o WIP</b>, e a segunda opção é de graça.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Scrum</b> = ciclos (Sprints). <b>Kanban</b> = fluxo e limite de WIP. <b>Trello</b> = só a ferramenta visual.",
    "Quadro: Product Backlog → Sprint Backlog → Em andamento → <b>Em validação</b> → Done.",
    "<b>WIP</b> alto = troca de contexto, trabalho parado, menos entregas. Pergunta certa: o que podemos <b>terminar</b> antes de começar algo novo?",
    "No exemplo (3 pessoas, 12 tarefas de 3 dias): WIP 3 → 1ª entrega aos 3 dias, média 7,5; WIP 12 → tudo no dia 12.",
    "<b>Lei de Little</b> (complemento): tempo médio = WIP / vazão."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "No exemplo, o que acontece quando o WIP vai de 3 para 12?", [("a","A equipe entrega mais tarefas no total."),("b","O total de trabalho é o mesmo, mas a primeira entrega vai de 3 para 12 dias."),("c","Nada: o WIP não afeta o prazo.")], "O WIP não cria capacidade; só espalha o esforço e adia as entregas.") + quiz(2, "c", "O Trello é...", [("a","Um framework ágil."),("b","Sinônimo de Kanban."),("c","Uma ferramenta visual, que não decide prioridade nem qualidade.")], "Scrum e Kanban são formas de trabalhar; o Trello é onde você desenha o quadro.") + quiz(3, "a", "Qual coluna do quadro guarda as perguntas 'atende ao critério de aceite? alguém revisou? há evidência?'", [("a","Em validação."),("b","Product Backlog."),("c","Sprint Backlog.")], "É a coluna que impede que 'concluído' vire 'Done' sem checagem.") + flash([
    ("O que é WIP?", "Work in progress: trabalho começado e ainda não terminado."),
    ("Por que limitar o WIP?", "Para expor gargalos cedo e terminar mais coisas, em vez de começar tudo e entregar tarde."),
    ("O que diz a lei de Little?", "Em fluxo estável, tempo médio no sistema = WIP dividido pela vazão."),
    ("Qual a pergunta que o WIP muda?", "De 'o que posso começar?' para 'o que podemos terminar antes de começar algo novo?'.")]) + ponte("O trabalho está visível e fluindo. Falta apresentá-lo em 5 minutos para quem decide.", "O pitch da Sprint Review.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "kanban-e-wip", T, "Kanban e limite de trabalho em andamento", "Capítulo 4 · Aula 3",
        "O quadro, a diferença entre Scrum, Kanban e ferramenta, e o efeito do WIP.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "simulador de limite de WIP"], body4, scripts=S)

# ---------------- CAP 5 ----------------
body5 = recap("Nos capítulos anteriores você organizou o trabalho: Sprint, histórias, quadro. A <b>Sprint Review</b> é onde esse trabalho aparece para quem decide, e costuma ser curta. O pitch é o formato dela. A ideia deste capítulo é simples: <b>caber, convencer e ser lembrado</b>.") + '''
<section class="sec" id="tempo">
  <h2><span class="sn">1</span>As regras do tempo</h2>
  <p class="gancho">Cinco minutos, e o relógio não negocia.</p>
  <ul>
    <li>O pitch tem <b>5 minutos</b>. Não pode passar, nem acabar antes de <b>4 min 30 s</b>. O ideal é cerca de <b>4 min 50 s</b>.</li>
    <li>Depois vem o <b>feedback</b> da empresa, de cerca de 10 minutos.</li>
    <li>Um slide com tópicos ou gráfico importante ocupa <b>até 30 s</b>. Uma imagem que só apoia a fala, <b>2 a 3 s</b>.</li>
  </ul>
  <p>Planeje os segundos de cada slide e veja o total. Os valores iniciais foram escolhidos para dar certo; estrague-os de propósito e leia os avisos:</p>
  <div class="demo" data-demo="pitch"></div>
</section>

<section class="sec" id="slides">
  <h2><span class="sn">2</span>Como montar os slides</h2>
  <p class="gancho">O slide apoia a fala, não a substitui.</p>
  <ul>
    <li><b>Sem texto corrido</b>: tópicos curtos, de até meia frase.</li>
    <li>Figuras, tabelas, gráficos e infográficos no lugar de parágrafos.</li>
    <li><b>Cor</b> no texto para destacar o que importa naquele momento.</li>
    <li><b>Linguagem clara</b>, sem jargão técnico desnecessário: quem decide nem sempre é técnico.</li>
  </ul>
  <div class="nota cuidado"><span class="lbl">Cuidado: o slide é seu roteiro, não o do público</span>Se o público consegue ler o slide inteiro em 5 s, ele para de ouvir você. Se você lê o slide em voz alta, ele dispensa você. Texto no slide é o que o público não deveria precisar ouvir.</div>
</section>

<section class="sec" id="dizer">
  <h2><span class="sn">3</span>O que dizer</h2>
  <p class="gancho">Uma história que o cliente reconheça como a dele.</p>
  <ul>
    <li><b>Storytelling</b>, com as User Stories dentro da história: uma pessoa, um problema, um dia ruim, uma saída. Exemplo de arco: uma bibliotecária precisa dizer, todo fim de semana, quantos livros ainda não voltaram; não sabe, porque a informação está espalhada em fichas e planilhas; com a solução, vira uma lista só.</li>
    <li>Conectar com a <b>missão e os valores da empresa parceira</b> (estão no site dela).</li>
    <li><b>Dados e evidências</b>: mercado, testes feitos, validações.</li>
    <li><b>Critérios de sucesso em destaque</b>: redução de custo, agilidade, engajamento, inovação, experiência.</li>
    <li>Demonstração ao vivo <b>somente se muito bem testada</b>. A solução tem que rodar sem problema.</li>
  </ul>
  <div class="ex rv"><span class="t">Uma estrutura em 5 atos (exemplo de roteiro, não regra)</span>
    <div class="l"><div><b>1. A pessoa</b> (até 25 s): quem é, o que faz.</div></div>
    <div class="l"><div><b>2. O problema</b> (40 s): a cena em que o problema aparece, com um dado.</div></div>
    <div class="l"><div><b>3. A história e seus critérios</b> (45 s): a User Story e como saberemos que deu certo.</div></div>
    <div class="l"><div><b>4. A solução</b> (1 min): funcionando, ou o diagrama (Capítulo 6).</div></div>
    <div class="l"><div><b>5. A evidência e o próximo passo</b> (2 min): o que já foi testado, o valor e o que vem na próxima Sprint.</div></div>
  </div>
  <p>Resumo do que importa: a apresentação é <b>apoio</b>; a <b>ideia</b> é o mais importante. E <b>não dividir em "bloquinhos"</b> (cada pessoa fala a sua parte e cala): o pitch é um bate-bola em que a bola nunca cai.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>5 min</b>, nunca menos de <b>4 min 30 s</b>, ideal <b>4 min 50 s</b>. Feedback depois, cerca de 10 min.",
    "Slide com tópicos: até <b>30 s</b>. Imagem de apoio: <b>2 a 3 s</b>.",
    "<b>Sem texto corrido</b>, com figuras, tabelas, gráficos e cor para destacar. Linguagem clara.",
    "<b>Storytelling</b> com User Stories, missão da empresa, evidências e critérios de sucesso em destaque.",
    "<b>Bate-bola</b>, não bloquinhos. Demonstração ao vivo só se muito bem testada."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Um pitch de 4 min 10 s está dentro da regra?", [("a","Sim, 5 minutos é só o máximo."),("b","Sim, qualquer tempo abaixo de 5 min vale."),("c","Não: não pode acabar antes de 4 min 30 s.")], "O pitch deve ficar entre 4 min 30 s e 5 min; o ideal é cerca de 4 min 50 s.") + quiz(2, "a", "Quanto tempo uma imagem que só apoia a fala deve ficar na tela?", [("a","2 a 3 segundos."),("b","30 segundos."),("c","1 minuto.")], "Slide com tópicos ou gráfico importante: até 30 s. Imagem de apoio: 2 a 3 s.") + quiz(3, "b", "Por que evitar o pitch em 'bloquinhos' (cada um fala sua parte)?", [("a","Porque é proibido."),("b","Porque quebra o ritmo: o ideal é um bate-bola em que um passa a bola ao outro sem deixá-la cair."),("c","Porque só uma pessoa pode falar.")], "A apresentação precisa soar como uma história única, e não como seções coladas.") + flash([
    ("Qual o tempo ideal do pitch?", "Cerca de 4 min 50 s, nunca passando de 5 min nem ficando abaixo de 4 min 30 s."),
    ("Quanto tempo para um slide com tópicos?", "Até 30 segundos."),
    ("O que entra na história do pitch?", "Uma pessoa, um problema, as User Stories, a solução, evidências e os critérios de sucesso."),
    ("Quando fazer demonstração ao vivo?", "Somente se estiver muito bem testada.")]) + ponte("O pitch explica o valor. Mas como mostrar a arquitetura a quem não programa?", "Com UML.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "pitch", T, "O pitch de 5 minutos", "Capítulo 5 · Aula 6",
        "Regras de tempo, slides, história e o ensaio por segundos.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "relógio do pitch"], body5, scripts=S)

# ---------------- CAP 6 ----------------
body6 = recap("O pitch mostra o valor. Mas e se o cliente perguntar <i>como</i> a solução funciona por dentro? Uma solução de IA brilhante que ninguém entende não gera confiança. O <b>UML</b> é uma linguagem visual para explicar a arquitetura <b>sem mostrar código</b>.") + '''
<section class="sec" id="por-que">
  <h2><span class="sn">1</span>Por que desenhar</h2>
  <p class="gancho">Se o cliente não entende o seu diagrama, não compra a sua solução.</p>
  <p><b>UML</b> (<i>Unified Modeling Language</i>) é uma linguagem visual para representar sistemas. O objetivo não é desenhar bonito: é <b>clareza, comunicação e tomada de decisão</b>. O caminho é <b>ideia → diagrama claro → implementação</b>. Como explicar sem código, por exemplo, uma solução em que um <i>sensor</i> envia dados a uma <i>API</i>, que alimenta um <i>modelo</i> cujo resultado aparece em um <i>dashboard</i>? Com caixas e linhas rotuladas.</p>
  <div class="nota cuidado"><span class="lbl">Infográfico não é UML</span>Uma arquitetura de nuvem desenhada com ícones de serviços é um infográfico: bonito, mas cada pessoa lê de um jeito. O mesmo desenho em UML usa <b>caixas padronizadas e linhas rotuladas pelo protocolo</b> (DNS, HTTP/HTTPS, SSH), e todos leem igual.</div>
</section>

<section class="sec" id="tipos">
  <h2><span class="sn">2</span>Três tipos de diagrama</h2>
  <p class="gancho">Cada um responde a uma pergunta diferente.</p>
  <div class="tablewrap"><table>
    <tr><th>Diagrama</th><th>Pergunta que responde</th><th>Mostra</th></tr>
    <tr><td><b>Componentes</b></td><td>Quais são as peças e como se conectam?</td><td>cliente, servidor web, servidor de aplicação, banco, dispositivos</td></tr>
    <tr><td><b>Sequência</b></td><td>Em que ordem as mensagens trafegam?</td><td>ator, site, navegador e banco trocando mensagens</td></tr>
    <tr><td><b>Classes</b></td><td>Que dados e estruturas existem?</td><td>classes, atributos e multiplicidade (<code>1</code>, <code>1..*</code>)</td></tr>
  </table></div>
  <p>Para explicar arquitetura a quem decide, o <b>diagrama de componentes</b> é o mais útil. Ferramenta gratuita no navegador: <b>UMLetino</b>. Os símbolos principais:</p>
  <div class="tablewrap"><table>
    <tr><th>Elemento</th><th>Significado</th></tr>
    <tr><td>Boneco (<i>actor</i>)</td><td>quem usa o sistema</td></tr>
    <tr><td>Seta sólida / pontilhada</td><td>conexão contínua / esporádica</td></tr>
    <tr><td>"Pilha" (cilindro)</td><td>banco de dados</td></tr>
    <tr><td>Caixa 3D (<code>«device»</code>, <code>«execution environment»</code>)</td><td>algo com CPU e memória: PC, servidor, microcontrolador</td></tr>
    <tr><td>Classe simples</td><td>biblioteca, framework ou software</td></tr>
    <tr><td>Caixa de borda pontilhada</td><td>agrupar outros blocos (por exemplo, "User Story 1")</td></tr>
    <tr><td>Caixas em camadas</td><td>front-end e back-end</td></tr>
  </table></div>
</section>

<section class="sec" id="exemplo">
  <h2><span class="sn">3</span>Um exemplo completo: detectar fadiga de motorista</h2>
  <p class="gancho">Hardware, nuvem e painel em um só desenho.</p>
  <p><b>User Story:</b> "Como gestor de operações, quero monitorar o nível de fadiga dos motoristas em tempo real para reduzir riscos de acidentes e melhorar a segurança da operação." <b>Critérios de aceite:</b> capturar câmera (expressão facial) e sensores (tempo de direção, velocidade); detectar fadiga com IA (olhos fechando, distração); alerta sonoro ao motorista e alerta no painel do gestor; guardar histórico; dashboard em tempo real e relatórios simples.</p>
  <p>O desenho de componentes que atende a essa história: o <b>motorista</b> é detectado pela <b>câmera</b> e por um sensor de pressão no volante, ligados aos pinos (GPIO) de um <b>microcontrolador</b> (ESP32) que roda um algoritmo em C++ e aciona um <b>buzzer</b>. O microcontrolador conversa com um <b>servidor na nuvem</b> por MQTT ou WebSocket. No back-end, um servidor em Python roda o modelo de detecção, os alertas e o dashboard, ligados a um banco. O <b>gestor</b> acessa o dashboard pelo navegador, por HTTPS. Tudo dentro de uma caixa tracejada, "User Story 1", com front-end e back-end separados. Clique nas caixas e nas linhas:</p>
  <div class="demo" data-demo="uml"></div>
  <div class="nota lembra"><span class="lbl">Como ler o diagrama</span>Cada <b>caixa</b> tem uma responsabilidade, e cada <b>linha</b> tem um rótulo com a forma de comunicação (um pino físico, MQTT, HTTPS). Se você consegue explicar, para cada caixa, "o que ela faz" e, para cada linha, "o que passa por ela", o diagrama cumpriu seu papel.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo (e da apostila)</h2>
  ''' + resumo([
    "<b>UML</b> comunica arquitetura sem código: clareza, comunicação e decisão.",
    "<b>Infográfico</b> com ícones não é UML: UML usa caixas padronizadas e linhas rotuladas com o protocolo.",
    "Três diagramas: <b>componentes</b> (peças e conexões), <b>sequência</b> (ordem das mensagens) e <b>classes</b> (dados e relações).",
    "Símbolos: ator, seta sólida/pontilhada, cilindro (banco), caixa 3D (<code>«device»</code>), caixa tracejada para agrupar.",
    "Fio condutor da apostila: problema → história → critérios → Sprint → quadro → pitch → diagrama."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Qual diagrama UML mostra as peças de uma solução e como elas se conectam?", [("a","Diagrama de classes."),("b","Diagrama de componentes."),("c","Diagrama de sequência.")], "Componentes mostram a arquitetura; sequência mostra a ordem das mensagens; classes mostram os dados.") + quiz(2, "c", "O que a caixa tracejada 'User Story 1' no exemplo representa?", [("a","Um banco de dados."),("b","Um erro."),("c","O agrupamento dos blocos que atendem àquela história.")], "A borda pontilhada agrupa outros blocos; aqui, tudo que entrega aquela história.") + quiz(3, "a", "Por que rotular as linhas com protocolos (HTTPS, MQTT...)?", [("a","Para que todos leiam a comunicação do mesmo jeito, sem ambiguidade."),("b","Para enfeitar o diagrama."),("c","Porque o UML exige cores.")], "A linha rotulada é o que diferencia um diagrama técnico de um infográfico solto.") + flash([
    ("O que é UML?", "Uma linguagem visual padronizada para representar sistemas."),
    ("O que é um diagrama de componentes?", "Um desenho das peças de um sistema e de como elas se comunicam."),
    ("O que a caixa 3D com «device» representa?", "Algo com CPU e memória: um computador, um servidor, um microcontrolador."),
    ("Infográfico x UML?", "Infográfico usa ícones e cada um interpreta de um jeito. UML usa símbolos padronizados e linhas rotuladas.")]) + '''
  <div class="ponte rv"><div class="t">Fim da apostila</div><div class="q">Do projeto que falhou ao diagrama que convence.</div><p>Se algum ponto ficou solto, refaça a demo do capítulo correspondente. Um projeto bem conduzido é o que você consegue explicar a qualquer pessoa em cinco minutos.</p></div>
</section>'''
chapter(PASTA, 6, "uml", T, "UML: diagrama de componentes", "Capítulo 6 · Aula 6",
        "Desenhar a arquitetura para quem decide: tipos de diagrama, símbolos e um exemplo completo.",
        ["<b>~45 min</b>", "1 demo · 3 testes · 4 flashcards", "diagrama interativo"], body6, scripts=S)
print("ga caps 4-6 ok")
