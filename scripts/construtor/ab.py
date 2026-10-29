import os, sys, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bld import *

PASTA = "ai-builder"
TITULO = "Ferramentas de AI Builder"
S = ["demos/ab.js"]

def code(src):
    return "<pre><code>" + H.escape(src, quote=False) + "</code></pre>"

def ler(rel):
    return open(os.path.join(REPO, PASTA, "exemplos", rel), encoding="utf-8").read()

CAPS = [
 dict(n=1, file="cap-1-apis-http-json.html", titulo="APIs, HTTP, JSON e webhooks", aula="Fase 1 · semana 1", tempo=45,
      resumo="A língua que todas as ferramentas falam: requisição, resposta, códigos de status, JSON, webhook e onde guardar chaves.",
      pergunta="Sei como os sistemas conversam. Dá para ligar vários deles sem escrever um programa inteiro?"),
 dict(n=2, file="cap-2-n8n.html", titulo="n8n: automação que você hospeda", aula="Fase 2 · semanas 2 e 3", tempo=60,
      resumo="Workflow, nó, gatilho e item; expressões; credenciais; o nó AI Agent; um fluxo completo com IA e tratamento de erro.",
      pergunta="O n8n não é a única opção. Quando Make ou Zapier resolvem melhor?"),
 dict(n=3, file="cap-3-make-e-zapier.html", titulo="Make e Zapier", aula="Fase 2 · semana 3", tempo=40,
      resumo="Cenários, módulos e bundles no Make; Zaps, ações e tasks no Zapier; como cada um cobra e qual escolher.",
      pergunta="Para rodar o n8n no meu PC, a documentação manda usar Docker. O que é isso?"),
 dict(n=4, file="cap-4-docker.html", titulo="Docker: imagem, container, volume e compose", aula="Fase 3 · semana 4", tempo=55,
      resumo="Imagem x container, Dockerfile e cache de camadas, portas, volumes, Docker Compose e o n8n rodando local.",
      pergunta="Já sei rodar ferramentas. Como faço a IA escrever o código das minhas?"),
 dict(n=5, file="cap-5-vibe-coding-cursor.html", titulo="Vibe coding com Cursor", aula="Fase 4 · semana 5", tempo=45,
      resumo="O que é vibe coding, o editor Cursor (Tab, agente, @ e rules), o laço seguro de trabalho e os riscos.",
      pergunta="E quando eu quero um protótipo inteiro, com tela e deploy, em uma tarde?"),
 dict(n=6, file="cap-6-v0-bolt-replit.html", titulo="Protótipos com v0, Bolt e Replit", aula="Fase 4 · semana 5", tempo=40,
      resumo="Três geradores de aplicativo: o que cada um faz bem, onde roda o código, plano gratuito e o que conferir antes de publicar.",
      pergunta="O protótipo precisa de dados de verdade. Como crio a minha própria API, sem virar engenheiro de backend?"),
 dict(n=7, file="cap-7-sua-api.html", titulo="Sua API sem backend profundo", aula="Fase 4 · semana 6", tempo=50,
      resumo="Uma API em FastAPI com validação, chave e testes; a documentação automática; empacotar com Docker e chamar do n8n.",
      pergunta="Com dados chegando, como uso IA para analisar sem publicar número errado?"),
 dict(n=8, file="cap-8-dados-com-ia.html", titulo="Análise de dados com IA", aula="Fase 4 · semana 7", tempo=40,
      resumo="O fluxo pergunta, dados, código e conferência; o exemplo com pandas; LGPD e o que nunca colar num chat.",
      pergunta="Tenho as ferramentas e os projetos. Como mostro isso a quem vai me contratar?"),
 dict(n=9, file="cap-9-portfolio.html", titulo="Portfólio de AI Builder", aula="Fase 5 · semana 8", tempo=40,
      resumo="O que um recrutador quer ver, como medir horas economizadas, o README que convence e a lista de projetos da trilha.",
      pergunta=""),
]

manifest(PASTA, "ai-builder", TITULO, CAPS)
hub(PASTA, TITULO, "Trilha própria · complemento à faculdade", "Apostila de Ferramentas de AI Builder",
    "Uma trilha de oito semanas para sair do zero em n8n, Make, Zapier, Docker, Cursor, v0, Bolt e Replit e terminar com um portfólio de quem constrói com IA.",
    ["<b>9</b> capítulos", "<b>~7h</b> de estudo ativo", "~5h por semana de prática"],
    '<p>Esta apostila não vem de uma disciplina: é uma <mark class="hl">trilha de estudo própria</mark>, montada a partir da documentação oficial de cada ferramenta. Ela segue cinco fases. <b>Fase 1</b>: a língua comum (APIs e JSON). <b>Fase 2</b>: automação sem código (n8n, Make e Zapier). <b>Fase 3</b>: infraestrutura mínima (Docker). <b>Fase 4</b>: construir com IA (Cursor, v0, Bolt, Replit, sua API e análise de dados). <b>Fase 5</b>: transformar tudo em portfólio. Cada fase termina com algo funcionando, não só com leitura.</p>'
    '<div class="tablewrap"><table><tr><th>Semana</th><th>Capítulo</th><th>Entrega da semana</th></tr>'
    '<tr><td>1</td><td>1</td><td>chamar uma API pública e ler o JSON</td></tr>'
    '<tr><td>2 e 3</td><td>2 e 3</td><td>um fluxo no n8n com IA e o mesmo fluxo no Make ou Zapier</td></tr>'
    '<tr><td>4</td><td>4</td><td>n8n rodando no seu PC com Docker Compose</td></tr>'
    '<tr><td>5</td><td>5 e 6</td><td>um protótipo com tela publicado</td></tr>'
    '<tr><td>6</td><td>7</td><td>sua API com testes, chamada pelo n8n</td></tr>'
    '<tr><td>7</td><td>8</td><td>uma análise com números conferidos</td></tr>'
    '<tr><td>8</td><td>9</td><td>repositório com README e métricas</td></tr></table></div>',
    'Tudo aqui é <b>complemento</b> (não foi dado em aula). Planos gratuitos, limites e preços foram conferidos nas páginas oficiais em <b>29/10/2026</b> e <b>mudam</b>: confira de novo antes de decidir. Os códigos da pasta <code>exemplos/</code> foram rodados; o que não pôde ser rodado aqui está marcado.')

# ---------------- CAP 1 ----------------
b = recap("Este é o primeiro capítulo da trilha. Não precisa saber programar: basta já ter usado um aplicativo que puxa dados de outro (o banco que mostra o Pix, o mapa que mostra o trânsito).", "Ponto de partida") + '''
<section class="sec" id="api">
  <h2><span class="sn">1</span>O que é uma API</h2>
  <p class="gancho">Todo sistema que você vai ligar nesta trilha conversa por API. Então, o que é isso?</p>
  <p><b>Intuição.</b> Pense no balcão de um cartório. Você não entra no arquivo e procura a certidão: você preenche um pedido no formato que o cartório aceita, entrega no balcão e recebe a certidão (ou um "faltou documento"). A API é esse balcão: um conjunto de pedidos que um sistema aceita, com regras sobre o formato.</p>
  <p><b>Definição.</b> <abbr class="gl" data-def="Application Programming Interface: o conjunto de operações que um sistema expõe para outros programas usarem.">API</abbr> é a interface que um programa oferece para outros programas. Quase todas as APIs web usam <b>HTTP</b> (o mesmo protocolo do navegador) e trocam dados em <b>JSON</b>. Quando o n8n "busca as linhas da planilha" ou o Claude "chama uma ferramenta", por baixo está um pedido HTTP.</p>
  ''' + ponte("Se o pedido tem formato, qual é o formato de um pedido HTTP?", "As cinco peças de uma requisição.") + '''
</section>

<section class="sec" id="http">
  <h2><span class="sn">2</span>A requisição e a resposta</h2>
  <p class="gancho">Um pedido HTTP tem sempre as mesmas peças. Quais são, e o que cada uma diz?</p>
  <div class="tablewrap"><table>
    <tr><th>Peça</th><th>O que diz</th><th>Exemplo</th></tr>
    <tr><td><b>Método</b></td><td>a intenção</td><td><code>GET</code> ler, <code>POST</code> enviar dados, <code>PUT</code>/<code>PATCH</code> alterar, <code>DELETE</code> apagar</td></tr>
    <tr><td><b>URL</b> (rota)</td><td>onde</td><td><code>https://api.loja.com/pedidos/42</code></td></tr>
    <tr><td><b>Cabeçalhos</b></td><td>informações sobre o pedido</td><td><code>content-type: application/json</code>, a chave de acesso</td></tr>
    <tr><td><b>Corpo</b></td><td>os dados enviados (em POST/PUT)</td><td><code>{"cliente":"Ana","valor":1500}</code></td></tr>
    <tr><td><b>Status</b> (na resposta)</td><td>como foi</td><td>2xx deu certo, 4xx erro seu, 5xx erro do servidor</td></tr>
  </table></div>
  <p>Os códigos que você mais vai ver: <b>200</b> ok, <b>201</b> criado, <b>400</b> pedido mal formado, <b>401</b> sem autorização (chave errada ou ausente), <b>403</b> proibido, <b>404</b> não existe, <b>405</b> método não permitido, <b>422</b> dados inválidos, <b>429</b> excesso de pedidos, <b>500</b> o servidor quebrou.</p>
  <p>A demo abaixo usa a API de triagem do capítulo 7. As respostas são as mesmas que os testes automáticos de <code>exemplos/test_api.py</code> conferiram rodando a API de verdade:</p>
  <div class="demo" data-demo="http"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: ler um erro</span>
    <div class="l"><div>O n8n mostra <code>401 Unauthorized</code>. O 4 diz que o problema é <b>do seu lado</b>, não do servidor.</div></div>
    <div class="l"><div>401 especificamente é autorização: a credencial do nó está vazia, vencida ou no cabeçalho errado.</div></div>
    <div class="l"><div>Se fosse 422, a chave estaria certa e o problema seria um campo do JSON. Se fosse 500, insistir mais tarde poderia resolver.</div></div>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span>Tentar de novo sem ler o código. 4xx quase nunca se resolve repetindo; 429 e 5xx às vezes sim (com espera entre as tentativas).</div>
  ''' + ponte("O corpo e a resposta vêm em JSON. Como ler JSON sem se perder?", "Três estruturas e você lê qualquer um.") + '''
</section>

<section class="sec" id="json">
  <h2><span class="sn">3</span>JSON em dez minutos</h2>
  <p class="gancho">Todo dado que passa entre as ferramentas é JSON. O que preciso saber para ler e montar um?</p>
  <p>JSON tem só três ideias: <b>objeto</b> (chaves e valores entre <code>{ }</code>), <b>lista</b> (valores em ordem entre <code>[ ]</code>) e <b>valores simples</b> (texto entre aspas, número, <code>true</code>/<code>false</code>, <code>null</code>). Elas se encaixam umas nas outras:</p>
''' + code('''{
  "cliente": { "nome": "Ana Souza", "email": "ana@exemplo.com" },
  "pedido":  { "valor": 1500, "itens": ["teclado", "mouse"] },
  "urgente": false
}''') + '''
  <p>Para chegar a um valor, você segue o caminho: <code>cliente.nome</code> dá <code>"Ana Souza"</code>; <code>pedido.itens[0]</code> dá <code>"teclado"</code> (listas contam a partir de zero). É exatamente o que você vai escrever nas expressões do n8n no próximo capítulo.</p>
  <div class="nota erro"><span class="lbl">Erro comum</span>Vírgula sobrando no último item, aspas simples no lugar de duplas ou comentário dentro do JSON. Qualquer um desses torna o JSON inválido, e a API devolve 400 ou 422.</div>
  ''' + ponte("Até aqui, quem pergunta é você. E quando o outro sistema precisa avisar que algo aconteceu?", "Webhook: o sistema liga para você.") + '''
</section>

<section class="sec" id="webhook">
  <h2><span class="sn">4</span>Webhook x polling</h2>
  <p class="gancho">Como uma automação fica sabendo que chegou um pedido novo?</p>
  <p>Há dois jeitos. No <b>polling</b>, a sua automação pergunta de tempos em tempos: "tem pedido novo?". Funciona, mas gasta execuções à toa e tem atraso. No <b>webhook</b>, você entrega uma URL ao outro sistema e ele faz um <code>POST</code> nela quando o evento acontece. É imediato e só roda quando há o que fazer. Por isso os gatilhos das ferramentas de automação preferem webhook quando o serviço oferece.</p>
  <div class="card sorter rv" data-demo="sorter" data-opts="w:Webhook|p:Polling">
    <div class="item" data-ans="w"><p>O formulário do site precisa disparar o fluxo no segundo em que o cliente clica em enviar.</p><span class="why">Evento pontual e urgente: o formulário avisa por webhook.</span></div>
    <div class="item" data-ans="p"><p>Um site do governo publica uma tabela, sem nenhuma forma de aviso, e você quer saber se mudou.</p><span class="why">Quem não oferece webhook só pode ser consultado de tempos em tempos.</span></div>
    <div class="item" data-ans="w"><p>O gateway de pagamento informa quando um Pix foi confirmado.</p><span class="why">Pagamentos são o caso clássico de webhook: o gateway chama a sua URL a cada confirmação.</span></div>
    <div class="item" data-ans="p"><p>Uma planilha antiga, num serviço que só tem leitura pela API, recebe linhas durante o dia.</p><span class="why">Sem evento disponível, o jeito é ler periodicamente e comparar.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + ponte("Tanto o pedido quanto o webhook exigem uma chave. Onde ela mora?", "Segredos: a regra que não tem exceção.") + '''
</section>

<section class="sec" id="chaves">
  <h2><span class="sn">5</span>Chaves de API e segredos</h2>
  <p class="gancho">A chave de API é a sua senha para aquele serviço. Quem a vê pode gastar no seu nome.</p>
  <p>A regra: <mark class="hl p">chave nunca fica no código nem no repositório</mark>. Ela vai em uma <b>variável de ambiente</b> (no seu PC, num arquivo <code>.env</code> listado no <code>.gitignore</code>) ou no cofre de credenciais da ferramenta (o n8n, o Make e o Zapier têm um). O código só lê o nome da variável, como em <code>os.environ.get("API_KEY")</code> no exemplo do capítulo 7.</p>
  <div class="nota cuidado"><span class="lbl">Se vazou</span>Apagar o commit não basta, porque o histórico do Git guarda a chave. O certo é <b>revogar</b> a chave no painel do serviço e gerar outra.</div>
  ''' + ponte("Com HTTP, JSON, webhook e chaves, você já entende o que uma ferramenta de automação faz por baixo.", "Hora de usar a primeira delas.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "API: o balcão de pedidos de um sistema. Quase sempre HTTP com JSON.",
    "Requisição: método, URL, cabeçalhos e corpo. Resposta: status e corpo.",
    "2xx ok, 4xx erro de quem pediu (401 chave, 404 não existe, 422 dados inválidos), 5xx erro do servidor.",
    "JSON: objeto <code>{}</code>, lista <code>[]</code> e valores simples. Caminho: <code>pedido.itens[0]</code>.",
    "Webhook: o sistema avisa você. Polling: você pergunta de tempos em tempos.",
    "Chave em variável de ambiente ou no cofre da ferramenta. Vazou, revoga.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "A API respondeu 422 a um POST. O que é mais provável?", [("a", "O servidor caiu"), ("b", "A rota não existe"), ("c", "Algum campo do JSON está faltando ou com tipo errado"), ("d", "Excesso de pedidos")], "422 quer dizer que o pedido chegou e foi entendido, mas os dados não passaram na validação. Rota inexistente seria 404; servidor caído, 5xx; excesso, 429.") + '''
  ''' + quiz(2, "a", "No JSON do capítulo, qual caminho leva a <code>&quot;mouse&quot;</code>?", [("a", "pedido.itens[1]"), ("b", "pedido.itens[2]"), ("c", "itens.mouse"), ("d", "pedido[1]")], "A lista começa no índice 0: <code>itens[0]</code> é teclado e <code>itens[1]</code> é mouse.") + '''
  ''' + quiz(3, "b", "Por que webhook costuma ser melhor que polling?", [("a", "Porque dispensa autenticação"), ("b", "Porque só roda quando há evento e chega na hora"), ("c", "Porque funciona com qualquer site"), ("d", "Porque usa GET")], "O webhook é disparado pelo próprio evento, sem consultas à toa. Ele ainda exige cuidado com autenticação e só existe se o serviço oferecer.") + '''
  ''' + quiz(4, "d", "Você subiu uma chave no GitHub por engano e apagou o commit. E agora?", [("a", "Pronto, resolvido"), ("b", "Tornar o repositório privado resolve"), ("c", "Trocar o nome da variável"), ("d", "Revogar a chave no serviço e gerar outra")], "O histórico e as cópias já podem ter a chave. Só a revogação a torna inútil.") + '''
  ''' + flash([
    ("O que diz o método HTTP?", "A intenção: GET lê, POST envia, PUT/PATCH alteram, DELETE apaga."),
    ("401 x 403", "401: não sei quem você é (chave ausente ou errada). 403: sei quem é, mas você não pode."),
    ("Webhook", "URL sua que outro sistema chama com POST quando um evento acontece."),
    ("Objeto x lista em JSON", "Objeto: chaves e valores em {}. Lista: valores em ordem em [], contando do zero."),
    ("Onde guardar uma chave de API?", "Variável de ambiente ou cofre de credenciais da ferramenta. Nunca no código."),
  ]) + '''
  ''' + ponte("Sei como os sistemas conversam. Dá para ligar vários deles sem escrever um programa inteiro?", "Sim: com uma ferramenta de automação. A primeira é a que você pode hospedar.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "apis-http-json", TITULO, "APIs, HTTP, JSON e webhooks", "Capítulo 1 · Fase 1", "A língua comum de todas as ferramentas da trilha. Sem isso, cada erro vira mistério.",
        ["<b>~45 min</b>", "2 demos · 4 testes · 5 flashcards"], b, S)

# ---------------- CAP 2 ----------------
b = recap("No capítulo 1 você viu que sistemas conversam por HTTP e JSON, que webhooks avisam eventos e que chaves moram fora do código. Ficou a pergunta: dá para ligar vários sistemas sem programar tudo?") + '''
<section class="sec" id="o-que-e">
  <h2><span class="sn">1</span>O que é o n8n</h2>
  <p class="gancho">Uma automação é uma receita: "quando X acontecer, faça Y e Z". Como o n8n representa isso?</p>
  <p>O n8n é uma ferramenta de automação visual. Você monta um <b>workflow</b> (fluxo) ligando <b>nós</b> numa tela. O primeiro nó é o <b>gatilho</b> (<i>trigger</i>): um webhook, um horário, um formulário, um e-mail novo. Os seguintes fazem ações: ler planilha, chamar API, filtrar, mandar mensagem, chamar um modelo de IA.</p>
  <p>O conceito que mais confunde iniciante é o <b>item</b>. Cada nó recebe uma <mark class="hl">lista de itens</mark> (cada item é um JSON) e, em regra, roda uma vez para cada um. Se a planilha devolve 30 linhas, o nó seguinte recebe 30 itens e manda 30 mensagens. Isso é ótimo quando você quer, e um desastre quando não percebe.</p>
  <div class="ex rv"><span class="t">Exemplo resolvido: quantas mensagens saem?</span>
    <div class="l"><div>Gatilho: todo dia às 8h. Nó 1: lê a planilha de prazos e devolve 12 linhas.</div></div>
    <div class="l"><div>Nó 2 (filtro): passa só as linhas com prazo para hoje. Sobram 3 itens.</div></div>
    <div class="l"><div>Nó 3 (Telegram): roda uma vez por item. Saem <b>3 mensagens</b>. Sem o filtro, sairiam 12.</div></div>
  </div>
  ''' + ponte("Antes de montar fluxos, onde o n8n roda?", "Na nuvem deles ou no seu computador.") + '''
</section>

<section class="sec" id="onde">
  <h2><span class="sn">2</span>Onde rodar: nuvem ou o seu PC</h2>
  <p class="gancho">O n8n tem duas formas de uso. Qual faz sentido para estudar?</p>
  <div class="grid2">
    <div class="card rv"><b>n8n Cloud</b><p>Você cria a conta e usa no navegador. A página de preços (29/10/2026) mostra um teste gratuito com limites (1.000 execuções, sem cartão) e planos pagos depois. Bom para começar hoje.</p></div>
    <div class="card rv"><b>Self-hosted (Community Edition)</b><p>A versão padrão do n8n é publicada no GitHub e você roda no seu computador ou servidor, sem pagar licença. O jeito recomendado é com Docker, que é o capítulo 4.</p></div>
  </div>
  <div class="nota lembra"><span class="lbl">Sugestão da trilha</span>Comece no Cloud nas semanas 2 e 3 para não travar na instalação. Na semana 4, depois do Docker, leve o mesmo fluxo para o seu PC.</div>
  ''' + ponte("O dado de um nó precisa chegar no seguinte. Como eu digo 'use o nome do cliente aqui'?", "Com expressões.") + '''
</section>

<section class="sec" id="expressoes">
  <h2><span class="sn">3</span>Expressões: puxar dados de um nó para outro</h2>
  <p class="gancho">Como escrever "Olá, Ana" quando o nome muda a cada item?</p>
  <p>Em qualquer campo de um nó você pode escrever uma <b>expressão</b> entre chaves duplas. Dentro delas vale um JavaScript simplificado, e <code>$json</code> é o item atual que chegou do nó anterior. A documentação oficial usa o exemplo <code>{{$json.body.city}}</code>: o campo <code>city</code> dentro de <code>body</code>. É o caminho de JSON do capítulo 1, com <code>$json</code> na frente.</p>
  <div class="demo" data-demo="expr"></div>
  <div class="nota erro"><span class="lbl">Erro comum</span>O nome do campo mudou na origem (alguém renomeou a coluna da planilha) e a expressão continua apontando para o nome antigo. Resultado: campo vazio sem erro nenhum, ou erro ao ler algo de um objeto que não existe. Sempre abra a aba de entrada do nó e confira os nomes.</div>
  ''' + ponte("Expressões resolvem o dado. E as senhas dos serviços que o fluxo usa?", "Ficam no cofre: credenciais.") + '''
</section>

<section class="sec" id="credenciais">
  <h2><span class="sn">4</span>Credenciais</h2>
  <p class="gancho">Onde colocar a chave do Google, do Telegram ou do modelo de IA?</p>
  <p>O n8n tem um lugar próprio para <b>credenciais</b>. Você cadastra uma vez (por chave de API ou por login OAuth, quando o serviço oferece) e escolhe a credencial no nó. Ela fica guardada separada do fluxo; quando você exporta o workflow em JSON para compartilhar, a chave não vai junto. É a aplicação da regra do capítulo 1: segredo fora da receita.</p>
  ''' + ponte("Com gatilho, nós, expressões e credenciais, falta a parte que dá nome à vaga: a IA.", "O nó de agente.") + '''
</section>

<section class="sec" id="ia">
  <h2><span class="sn">5</span>IA dentro do fluxo: o nó AI Agent</h2>
  <p class="gancho">Como colocar um modelo de linguagem no meio de uma automação, e não só no fim?</p>
  <p>O n8n tem nós de IA. O mais usado é o <b>AI Agent</b>, que junta três peças: um <b>modelo de chat</b> (Claude, GPT, Gemini, conectados pela credencial), <b>ferramentas</b> que o agente pode decidir usar (consultar planilha, chamar uma API, buscar na web) e uma <b>memória</b> da conversa. Para tarefas sem decisão, como resumir ou classificar um texto, um nó de chamada direta ao modelo basta e é mais previsível.</p>
  <h3>Projeto guiado da semana: triagem de pedidos com IA</h3>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Gatilho</b><p>Nó <b>Form Trigger</b> (ou Webhook) com os campos nome, e-mail e mensagem.</p></div>
      <div class="st"><b>2. Classificar</b><p>Nó de modelo de chat com o prompt: "Classifique a mensagem em uma destas categorias: orçamento, suporte, reclamação. Responda só com a categoria." e a mensagem via <code>{{ $json.mensagem }}</code>.</p></div>
      <div class="st"><b>3. Decidir</b><p>Nó <b>Switch</b>: cada categoria segue um caminho. Trate também o caso "outra resposta", porque o modelo pode fugir do combinado.</p></div>
      <div class="st"><b>4. Agir</b><p>Orçamento vira linha na planilha; reclamação manda alerta no Telegram; suporte gera resposta automática por e-mail.</p></div>
      <div class="st"><b>5. Medir</b><p>Anote quanto tempo a triagem manual levava e quantos pedidos chegam por semana. É o número do seu portfólio (capítulo 9).</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <div class="nota cuidado"><span class="lbl">IA não é determinística</span>O mesmo texto pode receber categorias diferentes em execuções diferentes. Peça saída curta e fechada, trate a resposta inesperada e teste com mensagens de verdade antes de ligar o fluxo em produção.</div>
  ''' + ponte("E quando um nó falha às 3 da manhã?", "Tratamento de erro.") + '''
</section>

<section class="sec" id="erros">
  <h2><span class="sn">6</span>Quando dá errado</h2>
  <p class="gancho">Fluxo que falha em silêncio é pior que fluxo nenhum. Como ficar sabendo?</p>
  <p>Três hábitos: (1) a aba <b>Executions</b> guarda cada execução com o dado que passou em cada nó, então reproduza o erro olhando a entrada do nó que quebrou; (2) monte um workflow separado começando pelo nó <b>Error Trigger</b>, que dispara quando outro fluxo falha, e mande um aviso para você; (3) em nós que chamam APIs instáveis, ative novas tentativas com espera.</p>
  ''' + ponte("O n8n resolve quase tudo, mas não é a única ferramenta do mercado.", "Make e Zapier no próximo capítulo.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">7</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Workflow = gatilho + nós. Cada nó recebe uma lista de itens e roda uma vez por item.",
    "Cloud para começar rápido; Community Edition self-hosted (com Docker) para rodar no seu PC.",
    "Expressão: <code>{{ $json.campo }}</code> lê o item atual. Confira os nomes na aba de entrada.",
    "Credenciais ficam no cofre do n8n, fora do workflow exportado.",
    "AI Agent = modelo + ferramentas + memória. Para classificar ou resumir, a chamada direta basta.",
    "Executions para investigar; Error Trigger para ser avisado.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Um nó de planilha devolve 50 linhas e o próximo nó envia e-mail. Sem nada no meio, quantos e-mails saem?", [("a", "1"), ("b", "50"), ("c", "Depende do gatilho"), ("d", "Nenhum, falta um laço")], "O n8n roda o nó uma vez por item. 50 itens, 50 e-mails. Se não era isso, filtre ou agregue antes.") + '''
  ''' + quiz(2, "a", "A expressão <code>{{ $json.cliente.telefone }}</code> volta vazia. O primeiro passo é:", [("a", "Abrir a entrada do nó e conferir se o campo existe com esse nome"), ("b", "Trocar o modelo de IA"), ("c", "Reinstalar o n8n"), ("d", "Apagar a credencial")], "Campo vazio quase sempre é nome diferente ou dado ausente no item. A aba de entrada mostra exatamente o JSON que chegou.") + '''
  ''' + quiz(3, "d", "Para classificar uma mensagem em três categorias fixas, o mais previsível é:", [("a", "Um AI Agent com dez ferramentas"), ("b", "Pedir uma resposta livre e longa"), ("c", "Não usar IA"), ("d", "Uma chamada direta ao modelo pedindo só a categoria, e um Switch tratando a resposta inesperada")], "Sem decisão sobre ferramentas, o agente só acrescenta variação. Saída fechada mais tratamento do inesperado deixa o fluxo confiável.") + '''
  ''' + quiz(4, "c", "Você quer ser avisado quando qualquer fluxo falhar. Use:", [("a", "Um nó Wait"), ("b", "Um webhook público"), ("c", "Um workflow com Error Trigger que manda alerta"), ("d", "A aba Executions toda manhã")], "O Error Trigger dispara sozinho na falha. Olhar Executions é investigar depois, não ser avisado.") + '''
  ''' + flash([
    ("Item no n8n", "Cada JSON da lista que passa entre os nós. Em regra, o nó roda uma vez por item."),
    ("O que é $json?", "O item atual que chegou do nó anterior, usado dentro de {{ }}."),
    ("Community Edition", "A versão padrão do n8n, publicada no GitHub, que você mesmo hospeda."),
    ("Três peças do AI Agent", "Modelo de chat, ferramentas e memória."),
    ("Error Trigger", "Nó que inicia um workflow quando outro workflow falha."),
  ]) + '''
  ''' + ponte("O n8n não é a única opção. Quando Make ou Zapier resolvem melhor?", "Os dois concorrentes mais conhecidos, e como cada um cobra.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "n8n", TITULO, "n8n: automação que você hospeda", "Capítulo 2 · Fase 2", "A ferramenta de automação que você pode rodar no seu próprio computador, com nós de IA.",
        ["<b>~60 min</b>", "1 demo · 4 testes · 5 flashcards"], b, S)

# ---------------- CAP 3 ----------------
b = recap("No capítulo 2 você montou fluxos no n8n: gatilho, itens, expressões, credenciais e o nó de agente. Ficou a pergunta: quando as alternativas resolvem melhor?") + '''
<section class="sec" id="make">
  <h2><span class="sn">1</span>Make: cenários visuais</h2>
  <p class="gancho">O Make faz o mesmo que o n8n? Quase. O que muda?</p>
  <p>No Make o fluxo se chama <b>cenário</b> e cada passo é um <b>módulo</b>. Os dados viajam em <b>bundles</b> (o equivalente ao item do n8n). Ferramentas próprias do Make: o <b>router</b> divide o fluxo em caminhos, o <b>iterator</b> quebra uma lista em vários bundles e o <b>aggregator</b> junta vários de volta em um. Filtros ficam nas ligações entre módulos.</p>
  <p><b>Como cobra.</b> Segundo a página de preços (29/10/2026), a unidade de cobrança do Make são <b>créditos</b>, e o plano gratuito dá <b>1.000 créditos por mês</b>. Cada módulo executado consome créditos; a regra exata de consumo está na página oficial e muda, então estime com um cenário real antes de assinar.</p>
  ''' + ponte("O Zapier também liga serviços. Por que tanta gente começa por ele?", "Simplicidade, e uma cobrança diferente.") + '''
</section>

<section class="sec" id="zapier">
  <h2><span class="sn">2</span>Zapier: Zaps e tasks</h2>
  <p class="gancho">Qual a ferramenta mais simples para quem nunca automatizou nada?</p>
  <p>No Zapier o fluxo é um <b>Zap</b>: um <b>trigger</b> e uma ou mais <b>actions</b>. A interface é linear e cheia de integrações prontas. A cobrança é por <b>task</b>: segundo a página de preços (29/10/2026), uma task é gasta quando uma ação conclui com sucesso. Triggers, ações que falham e ferramentas internas como Filter, Formatter e Paths <b>não</b> contam. O plano gratuito dá <b>100 tasks por mês</b> e só permite Zaps de <b>dois passos</b> (um trigger e uma ação); Zaps com vários passos começam no plano pago.</p>
  <div class="ex rv"><span class="t">Exemplo resolvido: cabe no gratuito?</span>
    <div class="l"><div>Zap pensado: formulário (trigger) → criar linha na planilha → mandar e-mail → mandar mensagem no Slack. São 3 ações.</div></div>
    <div class="l"><div>Primeiro problema: são 4 passos. O gratuito só aceita 2. Já não cabe.</div></div>
    <div class="l"><div>Mesmo pago, 40 envios por mês × 3 ações = <b>120 tasks</b>. Isso passaria das 100 do plano gratuito.</div></div>
    <div class="l"><div>No gratuito, o que cabe é 1 Zap de 2 passos rodando até 100 vezes por mês.</div></div>
  </div>
  ''' + ponte("Três ferramentas parecidas. Como escolher sem achismo?", "Pelo que cada uma cobra e pede de você.") + '''
</section>

<section class="sec" id="comparar">
  <h2><span class="sn">3</span>Qual escolher</h2>
  <p class="gancho">Não existe a melhor. Existe a melhor para o caso. Quais critérios decidem?</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>n8n</th><th>Make</th><th>Zapier</th></tr>
    <tr><td>Onde roda</td><td>nuvem deles ou seu servidor</td><td>nuvem deles</td><td>nuvem deles</td></tr>
    <tr><td>Cobra por</td><td>execução de workflow (Cloud); self-hosted sem licença</td><td>créditos</td><td>tasks (ações concluídas)</td></tr>
    <tr><td>Curva</td><td>a mais técnica (expressões, código)</td><td>intermediária</td><td>a mais simples</td></tr>
    <tr><td>Brilha em</td><td>fluxos longos, dados sensíveis no seu servidor, IA com agentes</td><td>transformação de dados visual com routers e iterators</td><td>ligar dois apps rápido, por quem não é técnico</td></tr>
  </table></div>
  <div class="card sorter rv" data-demo="sorter" data-opts="n:n8n|m:Make|z:Zapier">
    <div class="item" data-ans="n"><p>O escritório não aceita que os dados dos clientes passem por servidor de terceiros.</p><span class="why">Só o n8n pode rodar no servidor da própria empresa.</span></div>
    <div class="item" data-ans="z"><p>A dona de uma loja pequena quer que todo pedido novo vire linha numa planilha, e ela mesma vai manter.</p><span class="why">Dois passos, pessoa não técnica: o caso clássico do Zapier, e cabe no gratuito se forem até 100 pedidos por mês.</span></div>
    <div class="item" data-ans="m"><p>Um JSON de pedido traz uma lista de produtos; cada produto precisa ir para um sistema diferente conforme a categoria.</p><span class="why">Quebrar a lista (iterator) e dividir por caminhos (router) é o ponto forte do Make.</span></div>
    <div class="item" data-ans="n"><p>Um fluxo de 1.500 passos por dia, com chamadas de IA, que ficaria caro cobrado por ação.</p><span class="why">Self-hosted, o n8n não cobra por execução: o custo é o servidor.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <div class="nota lembra"><span class="lbl">Para o portfólio</span>Monte o projeto do capítulo 2 também no Make ou no Zapier. Comparar a mesma automação em duas ferramentas, com o custo de cada uma, é uma entrega que mostra critério, não só mão na massa.</div>
  ''' + ponte("O n8n self-hosted pede Docker. É hora de entender essa peça.", "No próximo capítulo.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Make: cenário, módulos, bundles, router, iterator e aggregator. Cobra em créditos (1.000/mês no gratuito, em 29/10/2026).",
    "Zapier: Zap = trigger + actions. Cobra por task concluída; trigger, falha e Filter/Formatter/Paths não contam.",
    "Zapier gratuito: 100 tasks/mês e Zaps de 2 passos.",
    "n8n: o único dos três que você pode hospedar; o mais técnico.",
    "Escolha pelo onde roda, como cobra e quem vai manter.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "No Zapier, um Zap com trigger + 2 ações rodou 30 vezes, e todas as ações deram certo. Quantas tasks?", [("a", "30"), ("b", "60"), ("c", "90"), ("d", "0, triggers não contam")], "Só as ações concluídas contam: 2 por execução × 30 = 60. O trigger não conta.") + '''
  ''' + quiz(2, "c", "No Make, qual peça transforma uma lista de 5 produtos em 5 bundles?", [("a", "Router"), ("b", "Aggregator"), ("c", "Iterator"), ("d", "Filtro")], "O iterator quebra a lista. O aggregator faz o caminho inverso; o router divide por caminhos.") + '''
  ''' + quiz(3, "a", "Dados sensíveis não podem sair da empresa. Qual ferramenta atende?", [("a", "n8n self-hosted"), ("b", "Zapier"), ("c", "Make"), ("d", "Qualquer uma, com senha forte")], "Make e Zapier rodam na nuvem deles: o dado passa por lá. Só o n8n roda no servidor da empresa.") + '''
  ''' + flash([
    ("Bundle", "O pacote de dados que passa entre módulos no Make (o item do n8n)."),
    ("O que gasta task no Zapier?", "Cada ação concluída com sucesso. Trigger, falha e ferramentas internas não."),
    ("Limite do Zapier gratuito", "100 tasks por mês e Zaps de dois passos (conferido em 29/10/2026)."),
    ("Router x iterator", "Router divide o fluxo em caminhos. Iterator quebra uma lista em vários bundles."),
  ]) + '''
  ''' + ponte("Para rodar o n8n no meu PC, a documentação manda usar Docker. O que é isso?", "A ferramenta que empacota um programa com tudo o que ele precisa.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "make-e-zapier", TITULO, "Make e Zapier", "Capítulo 3 · Fase 2", "Os dois concorrentes do n8n, como cada um cobra e qual escolher em cada caso.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards"], b, S)

# ---------------- CAP 4 ----------------
b = recap("Nos capítulos 2 e 3 você usou ferramentas na nuvem. O n8n também roda no seu PC, e a documentação dele recomenda Docker. Por que um programa precisa de outro programa para rodar?") + '''
<section class="sec" id="porque">
  <h2><span class="sn">1</span>O problema que o Docker resolve</h2>
  <p class="gancho">"Na minha máquina funciona." Por que essa frase existe?</p>
  <p>Um programa depende de muita coisa além dele: a versão do Python ou do Node, bibliotecas, variáveis, pastas. Na máquina de outra pessoa, qualquer diferença quebra. O Docker empacota o programa <b>junto com tudo de que ele precisa</b> num formato que roda igual em qualquer computador com Docker. E isola: o que roda lá dentro não bagunça o seu sistema.</p>
  ''' + ponte("Esse pacote tem nome, e o programa rodando tem outro.", "Imagem e container.") + '''
</section>

<section class="sec" id="imagem">
  <h2><span class="sn">2</span>Imagem, container e volume</h2>
  <p class="gancho">Qual a diferença entre o pacote e o programa rodando?</p>
  <div class="grid3">
    <div class="card rv"><b>Imagem</b><p>A receita congelada: sistema mínimo, dependências e o programa. Só leitura. Ex.: <code>n8nio/n8n</code>, <code>python:3.12-slim</code>.</p></div>
    <div class="card rv"><b>Container</b><p>Uma imagem rodando. Dá para ter vários containers da mesma imagem. Apagar o container apaga o que foi escrito dentro dele.</p></div>
    <div class="card rv"><b>Volume</b><p>Uma pasta guardada fora do container, montada dentro dele. Sobrevive quando o container é apagado. É onde ficam dados que importam.</p></div>
  </div>
  <div class="card sorter rv" data-demo="sorter" data-opts="i:Imagem|c:Container|v:Volume">
    <div class="item" data-ans="i"><p>O que você baixa com <code>docker pull n8nio/n8n</code>.</p><span class="why">Pull baixa a imagem; nada roda ainda.</span></div>
    <div class="item" data-ans="v"><p>Onde os seus workflows e credenciais do n8n precisam ficar para não sumirem.</p><span class="why">Só o volume sobrevive ao container ser recriado.</span></div>
    <div class="item" data-ans="c"><p>O que aparece em <code>docker ps</code>.</p><span class="why"><code>docker ps</code> lista containers em execução.</span></div>
    <div class="item" data-ans="i"><p>O resultado de <code>docker build</code> em cima de um Dockerfile.</p><span class="why">Build produz uma imagem nova a partir da receita.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + ponte("O n8n já tem imagem pronta. E para empacotar um programa seu?", "Escreve-se a receita: o Dockerfile.") + '''
</section>

<section class="sec" id="dockerfile">
  <h2><span class="sn">3</span>Dockerfile e o cache de camadas</h2>
  <p class="gancho">Como transformar a API do capítulo 7 numa imagem?</p>
  <p>O Dockerfile é a receita, lida de cima para baixo. Cada instrução gera uma <b>camada</b>, e o Docker reaproveita as camadas que não mudaram. Por isso a ordem importa: dependências (mudam pouco) antes do código (muda sempre).</p>
''' + code(ler("Dockerfile")) + '''
  <p class="muted">Este Dockerfile está em <code>exemplos/</code>. Ele <b>não foi construído aqui</b> (a máquina onde a apostila foi feita não tinha o serviço do Docker rodando); a API que ele empacota foi testada com pytest.</p>
  <div class="nota erro"><span class="lbl">Erro comum</span>Colocar <code>COPY . .</code> antes do <code>pip install</code>. Qualquer vírgula mudada no código invalida a camada e o Docker reinstala todas as dependências a cada build.</div>
  ''' + ponte("O container está rodando. Por que o navegador não abre?", "Porque o container tem a rede dele: é preciso abrir uma porta.") + '''
</section>

<section class="sec" id="portas">
  <h2><span class="sn">4</span>Portas e volumes na prática</h2>
  <p class="gancho">O n8n escuta na 5678 dentro do container. Como isso vira <code>localhost:5678</code> no seu PC?</p>
  <p>A opção <code>-p PC:CONTAINER</code> cria um túnel de uma porta do seu computador para uma porta do container. A opção <code>-v VOLUME:PASTA</code> monta um volume numa pasta de dentro. Mexa e veja o que abre:</p>
  <div class="demo" data-demo="porta"></div>
  ''' + ponte("Digitar um docker run enorme toda vez é pedir para errar.", "O Compose guarda a configuração num arquivo.") + '''
</section>

<section class="sec" id="compose">
  <h2><span class="sn">5</span>Docker Compose: o n8n no seu PC</h2>
  <p class="gancho">Como descrever o container uma vez e subir com um comando?</p>
  <p>O <b>Docker Compose</b> lê um arquivo YAML com os serviços, portas, variáveis e volumes. A documentação do n8n marca o <code>docker run</code> como forma antiga e recomenda o Compose. O arquivo abaixo é a tradução do comando oficial; ele foi validado com <code>docker compose config</code>:</p>
''' + code(ler("compose.yaml")) + '''
  <div class="tablewrap"><table>
    <tr><th>Comando</th><th>O que faz</th></tr>
    <tr><td><code>docker compose up -d</code></td><td>sobe os serviços em segundo plano</td></tr>
    <tr><td><code>docker compose logs -f</code></td><td>acompanha o log (Ctrl+C sai sem parar o serviço)</td></tr>
    <tr><td><code>docker compose down</code></td><td>para e apaga os containers; os volumes ficam</td></tr>
    <tr><td><code>docker ps</code></td><td>lista containers rodando</td></tr>
    <tr><td><code>docker exec -it NOME sh</code></td><td>abre um terminal dentro do container</td></tr>
    <tr><td><code>docker images</code></td><td>lista as imagens baixadas</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Licença do Docker Desktop</span>Segundo a documentação oficial, o Docker Desktop é gratuito para uso pessoal, educação, projetos open source não comerciais e empresas com menos de 250 funcionários <b>e</b> menos de US$ 10 milhões de receita anual. Numa empresa maior, ele exige assinatura.</div>
  ''' + ponte("Infra resolvida. Agora a parte central da vaga: construir com IA.", "Começando pelo editor.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Imagem é a receita congelada; container é a imagem rodando; volume guarda dados fora do container.",
    "Dockerfile: dependências antes do código, para aproveitar o cache de camadas.",
    "<code>-p 5678:5678</code>: porta do PC, dois-pontos, porta do container.",
    "Sem volume, <code>docker compose down</code> leva os dados junto.",
    "Compose: um YAML, <code>up -d</code> para subir, <code>down</code> para parar.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "d", "Com <code>-p 8080:5678</code>, qual endereço abre o n8n?", [("a", "localhost:5678"), ("b", "localhost:80"), ("c", "localhost:8080, mas só se o n8n escutar na 8080"), ("d", "localhost:8080")], "A primeira porta é a do seu PC (8080); a segunda, a do container (5678), onde o n8n já escuta.") + '''
  ''' + quiz(2, "a", "Você roda <code>docker compose down</code> e depois <code>up</code>. Os workflows continuam lá se:", [("a", "Houver um volume montado em /home/node/.n8n"), ("b", "Você usar -d"), ("c", "A imagem for a mais recente"), ("d", "Sempre continuam")], "Down apaga os containers. Só o que estava no volume sobrevive.") + '''
  ''' + quiz(3, "b", "Por que o Dockerfile copia o <code>requirements.txt</code> antes do código?", [("a", "Porque é obrigatório"), ("b", "Para o Docker reaproveitar a camada das dependências quando só o código mudar"), ("c", "Para a imagem ficar menor"), ("d", "Para o código rodar mais rápido")], "Camadas que não mudam vêm do cache. Separar as dependências evita reinstalar tudo a cada mudança no código.") + '''
  ''' + quiz(4, "c", "Uma empresa com 3.000 funcionários quer usar o Docker Desktop. Pela licença:", [("a", "É gratuito para qualquer empresa"), ("b", "É gratuito se for só para teste"), ("c", "Precisa de assinatura paga"), ("d", "É proibido")], "O uso gratuito vale para empresas com menos de 250 funcionários e menos de US$ 10 milhões de receita, além de uso pessoal e educação.") + '''
  ''' + flash([
    ("Imagem x container", "Imagem: a receita, só leitura. Container: a imagem rodando."),
    ("Para que serve um volume?", "Guardar dados fora do container, para sobreviverem quando ele for apagado."),
    ("-p 5678:5678", "Porta do seu PC : porta do container."),
    ("O que o Compose resolve?", "Descreve serviços, portas, variáveis e volumes num arquivo e sobe tudo com um comando."),
    ("Camada no Dockerfile", "Cada instrução gera uma; as que não mudaram vêm do cache."),
  ]) + '''
  ''' + ponte("Já sei rodar ferramentas. Como faço a IA escrever o código das minhas?", "Vibe coding, com responsabilidade.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "docker", TITULO, "Docker: imagem, container, volume e compose", "Capítulo 4 · Fase 3", "Empacotar programas para rodarem igual em qualquer máquina, começando pelo n8n no seu PC.",
        ["<b>~55 min</b>", "2 demos · 4 testes · 5 flashcards"], b, S)

# ---------------- CAP 5 ----------------
b = recap("No capítulo 4 você colocou o n8n para rodar no seu PC com Docker. A partir daqui, a trilha muda de usar ferramentas para construir as suas, com IA escrevendo boa parte do código.") + '''
<section class="sec" id="vibe">
  <h2><span class="sn">1</span>O que é vibe coding, e o que não é</h2>
  <p class="gancho">Se a IA escreve o código, o que sobra para mim?</p>
  <p>"Vibe coding" é o nome que pegou, a partir de 2025, para programar descrevendo o que você quer em linguagem natural e deixando a IA escrever o código. O termo nasceu meio de brincadeira, para protótipos descartáveis em que você aceita o que vier.</p>
  <p>Para trabalho de verdade, o seu papel muda de <b>digitar</b> para <b>especificar e verificar</b>: dizer exatamente o que quer, ler o que mudou, rodar os testes e decidir. A vaga de AI Builder descreve isso: não precisa saber como o modelo funciona por dentro, precisa saber o que pedir e transformar em algo que funciona.</p>
  <div class="nota cuidado"><span class="lbl">O limite</span>Código que você não entende e não testou não vai para algo que outras pessoas usam. Protótipo pode ser no impulso; ferramenta interna, não.</div>
  ''' + ponte("Qual o ambiente para esse trabalho?", "Um editor com IA dentro.") + '''
</section>

<section class="sec" id="cursor">
  <h2><span class="sn">2</span>O Cursor</h2>
  <p class="gancho">Por que um editor próprio, e não só o chat no navegador?</p>
  <p>O <b>Cursor</b> é um editor de código baseado no VS Code com IA integrada. Ele enxerga o projeto inteiro, então a IA trabalha em cima dos seus arquivos, e não de trechos colados. As peças principais:</p>
  <div class="tablewrap"><table>
    <tr><th>Peça</th><th>Para que serve</th></tr>
    <tr><td><b>Tab</b></td><td>autocompletar enquanto você digita</td></tr>
    <tr><td><b>Chat e agente</b></td><td>pedir mudanças em vários arquivos; o agente lê, edita e roda comandos</td></tr>
    <tr><td><b>@ (menções)</b></td><td>apontar arquivos, pastas ou documentação como contexto</td></tr>
    <tr><td><b>Rules</b></td><td>instruções permanentes do projeto</td></tr>
  </table></div>
  <p><b>Rules, conferido na documentação:</b> as regras do projeto ficam em <code>.cursor/rules</code>, em arquivos <code>.mdc</code>. Há quatro tipos: <b>Always</b> (sempre no contexto), <b>Auto Attached</b> (quando arquivos que batem com um padrão aparecem), <b>Agent Requested</b> (a IA decide pela descrição) e <b>Manual</b> (só quando você chama com <code>@nome</code>). Um <code>AGENTS.md</code> simples na raiz também é aceito. O antigo <code>.cursorrules</code> ainda funciona, mas está depreciado.</p>
  <div class="nota lembra"><span class="lbl">E o Claude Code?</span>A extensão do Claude Code instala também no Cursor. Os dois convivem: a apostila do Claude cobre o Claude Code em detalhe.</div>
  <div class="nota cuidado"><span class="lbl">Planos</span>O Cursor tem uma entrada gratuita com uso de IA limitado e planos pagos. Os nomes e limites dos planos mudaram mais de uma vez em 2026: confira a página de preços antes de assinar.</div>
  ''' + ponte("Com o editor aberto, como trabalhar sem perder o controle do que a IA mudou?", "Um laço curto e repetível.") + '''
</section>

<section class="sec" id="laco">
  <h2><span class="sn">3</span>O laço seguro</h2>
  <p class="gancho">Como evitar a pilha de mudanças que ninguém entende?</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Commit limpo</b><p>Antes de pedir, <code>git status</code> sem pendências. Se a IA estragar, <code>git restore .</code> volta tudo.</p></div>
      <div class="st"><b>2. Peça um plano</b><p>"Antes de editar, liste os arquivos que vai mudar e por quê." Corrija o plano, não o código.</p></div>
      <div class="st"><b>3. Um passo pequeno</b><p>Uma funcionalidade por vez. Diff grande é diff que você não lê.</p></div>
      <div class="st"><b>4. Leia o diff</b><p>Procure segredo no código, arquivo que não devia mudar e teste apagado para "passar".</p></div>
      <div class="st"><b>5. Rode a verificação</b><p>Testes, o app abrindo, o fluxo rodando. Peça para a IA mostrar a saída do teste, não dizer que passou.</p></div>
      <div class="st"><b>6. Commit</b><p>Mensagem curta do que mudou. Volte ao passo 2.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <div class="card sorter rv" data-demo="sorter" data-opts="a:Aceitar|r:Revisar antes">
    <div class="item" data-ans="r"><p>A IA "resolveu" o teste que falhava apagando o teste.</p><span class="why">Clássico: o objetivo virou fazer o teste passar, não fazer o código funcionar. Rejeite.</span></div>
    <div class="item" data-ans="a"><p>Renomear uma variável em um arquivo, com os testes passando.</p><span class="why">Mudança pequena, verificável e reversível.</span></div>
    <div class="item" data-ans="r"><p>O diff tem uma linha <code>API_KEY = "sk-..."</code>.</p><span class="why">Segredo no código. Volte para variável de ambiente antes de qualquer commit.</span></div>
    <div class="item" data-ans="r"><p>Você pediu uma tela e o agente também mexeu em 14 arquivos de configuração.</p><span class="why">Escopo maior do que o pedido: entenda cada mudança ou desfaça.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + ponte("O Cursor brilha num projeto que já existe. E para sair do zero até uma tela publicada?", "Os geradores de app.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Vibe coding: programar descrevendo. O seu trabalho vira especificar e verificar.",
    "Cursor: Tab, chat/agente, @ para contexto e rules do projeto.",
    "Rules em <code>.cursor/rules/*.mdc</code> (Always, Auto Attached, Agent Requested, Manual); <code>AGENTS.md</code> também vale; <code>.cursorrules</code> está depreciado.",
    "Laço: commit limpo, plano, passo pequeno, ler o diff, verificar, commit.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Onde ficam as regras de projeto do Cursor, pela documentação atual?", [("a", "Em <code>.cursorrules</code>, o formato recomendado"), ("b", "Nas configurações da conta"), ("c", "Em <code>.cursor/rules</code>, em arquivos <code>.mdc</code>"), ("d", "No README")], "<code>.cursorrules</code> ainda funciona, mas está depreciado. O formato atual são arquivos .mdc em .cursor/rules.") + '''
  ''' + quiz(2, "a", "Qual tipo de regra entra só quando você escreve <code>@nome</code>?", [("a", "Manual"), ("b", "Always"), ("c", "Auto Attached"), ("d", "Agent Requested")], "Manual depende de você chamar. Always entra sempre; Auto Attached por padrão de arquivo; Agent Requested pela decisão da IA.") + '''
  ''' + quiz(3, "b", "O agente disse “todos os testes passam”. O que fazer?", [("a", "Commitar"), ("b", "Pedir a saída do comando de teste, ou rodar você mesmo"), ("c", "Pedir para ele confirmar de novo"), ("d", "Apagar os testes antigos")], "Evidência vale mais que afirmação. A saída do teste mostra o que rodou e o que passou.") + '''
  ''' + flash([
    ("Vibe coding", "Programar descrevendo em linguagem natural; a IA escreve o código e você especifica e verifica."),
    ("Para que serve o @ no Cursor?", "Apontar arquivos, pastas ou documentação como contexto do pedido."),
    ("Por que commit antes de pedir?", "Para poder voltar tudo com um comando se a IA estragar."),
    ("Sinal de alerta no diff", "Teste apagado, segredo no código, arquivo fora do escopo mudado."),
  ]) + '''
  ''' + ponte("E quando eu quero um protótipo inteiro, com tela e deploy, em uma tarde?", "v0, Bolt e Replit.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "vibe-coding-cursor", TITULO, "Vibe coding com Cursor", "Capítulo 5 · Fase 4", "Deixar a IA escrever o código sem perder o controle do que ela mudou.",
        ["<b>~45 min</b>", "1 demo · 3 testes · 4 flashcards"], b, S)

# ---------------- CAP 6 ----------------
b = recap("No capítulo 5 você trabalhou num projeto que já existe, com o Cursor e um laço de verificação. Falta o caminho oposto: sair do zero até um app publicado.") + '''
<section class="sec" id="tres">
  <h2><span class="sn">1</span>Três geradores de app</h2>
  <p class="gancho">Você descreve o app e recebe o app. Onde está a diferença entre eles?</p>
  <div class="grid3">
    <div class="card rv"><b>v0 (Vercel)</b><p>Gera interfaces web a partir de texto ou imagem e publica na Vercel. Forte em tela: páginas, painéis, formulários. Plano gratuito (29/10/2026): <b>7 mensagens por dia</b>, com deploy na Vercel incluído.</p></div>
    <div class="card rv"><b>Bolt (StackBlitz)</b><p>Gera apps completos que rodam <b>dentro do seu navegador</b>: usa WebContainers, um sistema baseado em WebAssembly que executa Node.js no lado do cliente. Por isso consegue rodar o que gerou e corrigir erros na hora. Gratuito: <b>1 milhão de tokens por mês</b>, com teto de 300 mil por dia.</p></div>
    <div class="card rv"><b>Replit</b><p>Um ambiente de programação na nuvem com um agente que cria o projeto, roda e publica. Bom quando o app precisa de servidor e banco. Tem entrada gratuita; o plano Core (US$ 20/mês ou 18 no anual) dá mais uso.</p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Tokens somem rápido</span>No Bolt, segundo a própria página de preços, a maior parte do consumo vem de sincronizar os arquivos do projeto com a IA. Projeto grande gasta mais por mensagem. Comece pequeno.</div>
  ''' + ponte("Com três opções, qual uso para cada protótipo?", "Depende do que o protótipo precisa ter.") + '''
</section>

<section class="sec" id="escolher">
  <h2><span class="sn">2</span>Qual usar</h2>
  <p class="gancho">Tela bonita, app que roda ou app com servidor?</p>
  <div class="card sorter rv" data-demo="sorter" data-opts="v:v0|b:Bolt|r:Replit">
    <div class="item" data-ans="v"><p>Uma landing page do seu portfólio, só front-end, publicada hoje.</p><span class="why">Interface pura com deploy embutido: o forte do v0.</span></div>
    <div class="item" data-ans="b"><p>Um protótipo de calculadora de prazos que precisa rodar e ser testado ali mesmo, no navegador, sem instalar nada.</p><span class="why">O Bolt executa o app no próprio navegador, então você testa enquanto gera.</span></div>
    <div class="item" data-ans="r"><p>Um app com login, banco de dados e uma rotina que roda no servidor toda noite.</p><span class="why">Servidor sempre ligado e banco: o ambiente de nuvem do Replit é feito para isso.</span></div>
    <div class="item" data-ans="v"><p>Transformar o print de uma tela que você desenhou num componente React.</p><span class="why">O v0 aceita imagem como ponto de partida para interface.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + ponte("O protótipo ficou pronto em uma tarde. O que conferir antes de mostrar para alguém?", "A lista do protótipo honesto.") + '''
</section>

<section class="sec" id="conferir">
  <h2><span class="sn">3</span>Antes de publicar</h2>
  <p class="gancho">Protótipo publicado é uma URL que qualquer um pode abrir. O que pode dar errado?</p>
  <div class="demo" data-demo="checks" data-key="publicar">
    <h4>Checklist antes de publicar um protótipo</h4>
    <label style="display:block"><input type="checkbox"> Nenhuma chave de API no código do front-end (o navegador mostra tudo para quem abrir).</label>
    <label style="display:block"><input type="checkbox"> Dados de teste são fictícios: nada de cliente, processo ou CPF reais.</label>
    <label style="display:block"><input type="checkbox"> Abri o app no celular e cliquei em todos os botões.</label>
    <label style="display:block"><input type="checkbox"> O código foi exportado para o GitHub (você não fica preso à ferramenta).</label>
    <label style="display:block"><input type="checkbox"> O README diz o que é protótipo e o que ainda não funciona.</label>
    <p class="muted"><b class="chk-n"></b> marcados</p>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span>Colocar a chave do modelo de IA direto no código da tela para "funcionar rápido". Qualquer visitante abre as ferramentas do navegador e copia. A chamada ao modelo tem de passar por um servidor seu, que é o assunto do próximo capítulo.</div>
  ''' + ponte("O protótipo precisa de dados de verdade e de esconder a chave. Como faço uma API?", "Com poucas linhas de Python.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "v0: interface web e deploy na Vercel (gratuito: 7 mensagens/dia).",
    "Bolt: app completo rodando no navegador com WebContainers (gratuito: 1M tokens/mês, 300 mil/dia).",
    "Replit: ambiente na nuvem com agente, servidor e banco (Core: US$ 20/mês).",
    "Antes de publicar: sem chave no front, dados fictícios, testado no celular, código no GitHub.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Por que o Bolt consegue rodar o app que gerou sem servidor?", [("a", "Porque usa WebContainers, que executam Node.js dentro do navegador"), ("b", "Porque o app é só HTML"), ("c", "Porque usa o Docker do seu PC"), ("d", "Porque publica antes de rodar")], "WebContainers são um sistema baseado em WebAssembly que roda Node.js no próprio navegador.") + '''
  ''' + quiz(2, "c", "Onde a chave do modelo de IA NÃO pode ficar?", [("a", "Numa variável de ambiente do servidor"), ("b", "No cofre de credenciais do n8n"), ("c", "No código JavaScript da página"), ("d", "No arquivo .env fora do Git")], "O código da página vai inteiro para o navegador de quem abre. Lá, qualquer um lê.") + '''
  ''' + flash([
    ("v0", "Gerador de interface web da Vercel, com deploy embutido."),
    ("WebContainers", "Tecnologia da StackBlitz que roda Node.js dentro do navegador; base do Bolt."),
    ("Replit", "Ambiente de programação na nuvem com agente, servidor e deploy."),
    ("Regra da chave no front", "Nunca. Chamada a serviço pago passa por um servidor seu."),
  ]) + '''
  ''' + ponte("O protótipo precisa de dados de verdade. Como crio a minha própria API, sem virar engenheiro de backend?", "FastAPI, em poucas linhas e com testes.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
chapter(PASTA, 6, "v0-bolt-replit", TITULO, "Protótipos com v0, Bolt e Replit", "Capítulo 6 · Fase 4", "Do texto ao app publicado em uma tarde, e o que conferir antes de mostrar.",
        ["<b>~40 min</b>", "2 demos · 2 testes · 4 flashcards"], b, S)

# ---------------- CAP 7 ----------------
b = recap("No capítulo 6 você viu que a chave do modelo não pode ficar na página e que o protótipo precisa de dados de verdade. As duas coisas pedem um servidor seu: uma API.") + '''
<section class="sec" id="fastapi">
  <h2><span class="sn">1</span>Uma API em 30 linhas</h2>
  <p class="gancho">Quanto código é preciso para receber um JSON e devolver outro?</p>
  <p>Com o <b>FastAPI</b> (biblioteca de Python), pouco. Você declara o formato dos dados numa classe, escreve uma função por rota e ele cuida de converter JSON, validar campos e devolver os códigos de erro certos. O exemplo recebe um pedido e decide a fila:</p>
''' + code(ler("api.py")) + '''
  <p>Três coisas do capítulo 1 aparecem aqui: a <b>rota</b> com método (<code>@app.post("/triagem")</code>), a <b>validação</b> do corpo (a classe <code>Pedido</code>; faltou campo, o FastAPI responde 422 sozinho) e a <b>chave</b> lida do ambiente.</p>
  <p>Rodando com <code>uvicorn api:app --reload</code>, o endereço <code>/docs</code> abre uma documentação interativa gerada automaticamente, onde você testa cada rota sem escrever nada.</p>
  ''' + ponte("Como provar que a API faz o que diz?", "Testes automáticos, que também servem de contrato.") + '''
</section>

<section class="sec" id="testes">
  <h2><span class="sn">2</span>Testes: a prova de que funciona</h2>
  <p class="gancho">A IA escreveu a API. Como você sabe que está certa sem testar na mão toda vez?</p>
''' + code(ler("test_api.py")) + '''
  <p>Resultado rodado na criação desta apostila: <code>5 passed</code>. Cada teste fixa um comportamento: valor de 1.500 vai para prioridade, 80 vai para normal, sem chave dá 401, campo faltando dá 422. Se alguém (você ou a IA) mudar a regra sem querer, um teste quebra na hora. É a "verificação" do laço do capítulo 5.</p>
  <div class="ex rv"><span class="t">Exemplo resolvido: a regra do limite</span>
    <div class="l"><div>A regra diz <code>valor &gt;= 1000</code> vai para prioridade. E exatamente 1000?</div></div>
    <div class="l"><div>Com <code>&gt;=</code>, 1000 é prioridade. Se a IA "otimizar" para <code>&gt;</code>, 1000 vira normal.</div></div>
    <div class="l"><div>Os testes atuais usam 1500 e 80, então não pegariam essa mudança. Um bom teste a mais: <code>valor: 1000</code> esperando prioridade. Limite é onde os bugs moram.</div></div>
  </div>
  ''' + ponte("A API funciona no seu PC. Como ela vai para outro lugar e é chamada por uma automação?", "Docker e o nó HTTP do n8n.") + '''
</section>

<section class="sec" id="ligar">
  <h2><span class="sn">3</span>Empacotar e ligar no n8n</h2>
  <p class="gancho">Como juntar as peças da trilha?</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Empacotar</b><p>O Dockerfile do capítulo 4 já é desta API: <code>docker build -t triagem .</code></p></div>
      <div class="st"><b>2. Rodar com a chave</b><p><code>docker run --rm -p 8000:8000 -e API_KEY=minha-chave triagem</code>. A chave entra por variável, nunca na imagem.</p></div>
      <div class="st"><b>3. Chamar do n8n</b><p>Nó <b>HTTP Request</b>: método POST, URL <code>http://SEU_HOST:8000/triagem</code>, cabeçalho <code>x-api-key</code> vindo de uma credencial, corpo JSON com <code>{{ $json.cliente }}</code> e <code>{{ $json.valor }}</code>.</p></div>
      <div class="st"><b>4. Decidir</b><p>Um Switch lê <code>{{ $json.fila }}</code> da resposta e segue o caminho certo.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <div class="nota cuidado"><span class="lbl">localhost dentro de container</span>Se o n8n também roda em Docker, <code>localhost</code> dentro dele é o próprio container do n8n, não o seu PC. Coloque os dois serviços no mesmo <code>compose.yaml</code> e chame a API pelo nome do serviço (ex.: <code>http://triagem:8000</code>).</div>
  ''' + ponte("Dados chegando de verdade. Como usar IA para analisá-los sem publicar número errado?", "O próximo capítulo.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "FastAPI: classe define o formato, função define a rota; validação e 422 vêm prontos.",
    "<code>/docs</code> gera documentação interativa automaticamente.",
    "Testes fixam o comportamento; teste os limites (exatamente 1000).",
    "Chave por variável de ambiente; <code>-e API_KEY=...</code> no docker run.",
    "No n8n, nó HTTP Request; entre containers, chame pelo nome do serviço.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "O cliente manda <code>{&quot;cliente&quot;:&quot;Davi&quot;}</code> com a chave certa. O que a API responde?", [("a", "200 com fila normal"), ("b", "422, porque falta o campo obrigatório valor"), ("c", "401"), ("d", "500")], "O campo <code>valor</code> não tem padrão na classe Pedido, então é obrigatório. O FastAPI recusa com 422 antes da função rodar.") + '''
  ''' + quiz(2, "d", "Com a regra <code>valor &gt;= 1000</code>, para onde vai um pedido de exatamente 1000?", [("a", "Normal"), ("b", "Depende de urgente"), ("c", "Erro"), ("d", "Prioridade")], "Maior ou igual inclui o próprio 1000.") + '''
  ''' + quiz(3, "a", "O n8n roda em Docker e chama <code>http://localhost:8000</code>, mas a API roda em outro container. O que acontece?", [("a", "Falha: localhost aponta para o próprio container do n8n"), ("b", "Funciona sempre"), ("c", "Funciona se a porta for 5678"), ("d", "Dá 401")], "Cada container tem a sua rede. Use um compose com os dois serviços e chame pelo nome.") + '''
  ''' + quiz(4, "c", "Onde a chave da API deve entrar no container?", [("a", "Escrita no Dockerfile"), ("b", "Num arquivo copiado para a imagem"), ("c", "Por variável de ambiente na hora de rodar"), ("d", "No nome da imagem")], "Imagem pode ser compartilhada; o que está nela vaza junto. A chave entra só na execução.") + '''
  ''' + flash([
    ("O que o FastAPI faz sozinho?", "Converte JSON, valida campos pela classe e responde 422 quando falta ou sobra algo errado."),
    ("Para que serve /docs?", "Documentação interativa gerada automaticamente, para testar as rotas."),
    ("Por que testar limites?", "É onde a troca de >= por > passa despercebida."),
    ("Nó do n8n para chamar sua API", "HTTP Request, com a chave vinda de uma credencial."),
  ]) + '''
  ''' + ponte("Com dados chegando, como uso IA para analisar sem publicar número errado?", "O fluxo com conferência.", "Para onde vamos agora · Capítulo 8") + '''
</section>'''
chapter(PASTA, 7, "sua-api", TITULO, "Sua API sem backend profundo", "Capítulo 7 · Fase 4", "Uma API pequena, testada e empacotada, que suas automações e protótipos podem chamar.",
        ["<b>~50 min</b>", "0 demos · 4 testes · 4 flashcards"], b, S)

# ---------------- CAP 8 ----------------
b = recap("No capítulo 7 você criou uma API que recebe dados de verdade. Agora vem a pergunta que todo gestor faz: o que esses dados dizem? E a IA pode responder, desde que você confira.") + '''
<section class="sec" id="fluxo">
  <h2><span class="sn">1</span>O fluxo de análise com IA</h2>
  <p class="gancho">Por que não colar a planilha no chat e pedir "me dá os insights"?</p>
  <p>Porque um modelo de linguagem pode <b>inventar um número com toda a confiança</b>. Ele é ótimo para escrever o código da análise e para explicar o resultado; a conta em si tem de ser feita por código que você roda. O fluxo:</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Pergunta de negócio</b><p>Específica: "qual canal resolve mais rápido e com mais sucesso?", e não "analise os dados".</p></div>
      <div class="st"><b>2. Dados limpos e sem dado pessoal</b><p>Só as colunas que a pergunta precisa. Sem nome, CPF ou e-mail.</p></div>
      <div class="st"><b>3. IA escreve o código</b><p>Peça código em pandas que responda à pergunta, e não a resposta direta.</p></div>
      <div class="st"><b>4. Você roda e confere</b><p>Refaça uma das contas por outro caminho. Se as duas não batem, nada vai para o relatório.</p></div>
      <div class="st"><b>5. IA ajuda a contar a história</b><p>Com os números conferidos na mão, peça o texto. Revise se o texto não exagerou o que os números dizem.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  ''' + ponte("Como fica isso em código?", "Um exemplo com a conferência embutida.") + '''
</section>

<section class="sec" id="exemplo">
  <h2><span class="sn">2</span>O exemplo, rodado</h2>
  <p class="gancho">Como a conferência vira parte do programa, e não um passo que você esquece?</p>
''' + code(ler("analise.py")) + '''
  <p>Saída da execução (feita na criação desta apostila):</p>
''' + code('''          atendimentos  minutos_medio  taxa_resolucao
canal
E-mail               3          18.33            0.33
Telefone             2          10.00            1.00
WhatsApp             3           5.00            1.00
Conferido: média do e-mail = 18.33 min''') + '''
  <div class="ex rv"><span class="t">Exemplo resolvido: ler sem exagerar</span>
    <div class="l"><div>WhatsApp: média de 5 minutos e 100% resolvido. E-mail: 18,33 minutos e só 33% resolvido (1 de 3).</div></div>
    <div class="l"><div>Conferência do e-mail na mão: (18 + 22 + 15) / 3 = 55 / 3 = 18,33. Bate com a tabela.</div></div>
    <div class="l"><div>O que <b>não</b> dá para dizer: "o WhatsApp é 3,7 vezes melhor". São 8 atendimentos no total; com tão pouco dado, a conclusão honesta é "vale coletar mais antes de mudar o processo".</div></div>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span>Aceitar a frase bonita que a IA escreveu sobre os dados sem checar se ela bate com a tabela. O texto costuma generalizar mais do que os números permitem.</div>
  ''' + ponte("E o que nunca deve ir para dentro de um chat de IA?", "A parte da LGPD.") + '''
</section>

<section class="sec" id="lgpd">
  <h2><span class="sn">3</span>Dados pessoais e LGPD</h2>
  <p class="gancho">A planilha tem nome, CPF e telefone de clientes. Posso colar no chat?</p>
  <p>A Lei Geral de Proteção de Dados (Lei 13.709/2018) exige base legal e finalidade para tratar dado pessoal, e mandar a planilha para um serviço externo é tratamento. Em empresa, a regra prática: <b>só use ferramentas aprovadas pela empresa e só com os dados necessários</b>. Para análise, quase sempre dá para remover ou pseudonimizar as colunas pessoais antes.</p>
  <div class="card sorter rv" data-demo="sorter" data-opts="s:Pode ir|n:Não vai">
    <div class="item" data-ans="s"><p>Tabela com canal, minutos e se foi resolvido, sem identificar ninguém.</p><span class="why">Sem dado pessoal, o risco é baixo.</span></div>
    <div class="item" data-ans="n"><p>A planilha completa de clientes, com CPF, para "a IA achar padrões".</p><span class="why">Dado pessoal sem necessidade. Remova as colunas que a pergunta não usa.</span></div>
    <div class="item" data-ans="n"><p>Um processo sob segredo de justiça, para resumir, numa conta pessoal de IA.</p><span class="why">Sigilo e ferramenta não aprovada. Só no ambiente que a empresa autorizou, se autorizar.</span></div>
    <div class="item" data-ans="s"><p>O código da análise, sem os dados, para a IA revisar.</p><span class="why">O código não carrega dado pessoal.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + ponte("Tudo pronto para virar portfólio.", "O último capítulo.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "IA escreve o código e a narrativa; a conta é do código que você roda.",
    "Pergunta específica, dados mínimos, código, conferência, texto.",
    "Conferência embutida: refazer uma conta por outro caminho com <code>assert</code>.",
    "Pouco dado, conclusão modesta.",
    "LGPD: ferramenta aprovada, dados necessários, colunas pessoais fora.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "No exemplo, qual a taxa de resolução do e-mail?", [("a", "100%"), ("b", "18,33%"), ("c", "33%"), ("d", "66%")], "Dos 3 atendimentos por e-mail, 1 foi resolvido: 1/3 ≈ 0,33.") + '''
  ''' + quiz(2, "a", "Para que serve o <code>assert</code> no fim do script?", [("a", "Interromper o programa se as duas contas não baterem"), ("b", "Deixar o código mais rápido"), ("c", "Mandar o resultado por e-mail"), ("d", "Esconder erros")], "Se a média calculada à mão diferir da tabela, o programa para com a mensagem de erro em vez de seguir com número errado.") + '''
  ''' + quiz(3, "b", "A melhor forma de pedir ajuda da IA com uma planilha de clientes é:", [("a", "Colar tudo e pedir insights"), ("b", "Tirar as colunas pessoais e pedir o código que responde a uma pergunta específica"), ("c", "Pedir para a IA guardar a planilha"), ("d", "Mandar só o CPF")], "Dados mínimos e pergunta específica reduzem risco e aumentam a qualidade.") + '''
  ''' + flash([
    ("Por que não pedir o número direto ao chat?", "O modelo pode inventar um valor com confiança. A conta tem de ser código rodado."),
    ("Conferência", "Refazer uma conta por outro caminho e comparar antes de publicar."),
    ("LGPD em uma frase", "Dado pessoal só com base legal, finalidade e o mínimo necessário."),
    ("Sinal de exagero", "Conclusão forte tirada de poucos registros."),
  ]) + '''
  ''' + ponte("Tenho as ferramentas e os projetos. Como mostro isso a quem vai me contratar?", "Portfólio com números.", "Para onde vamos agora · Capítulo 9") + '''
</section>'''
chapter(PASTA, 8, "dados-com-ia", TITULO, "Análise de dados com IA", "Capítulo 8 · Fase 4", "Usar IA para analisar sem publicar número errado, e sem expor dado pessoal.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards"], b, S)

# ---------------- CAP 9 ----------------
b = recap("Nos capítulos 1 a 8 você aprendeu as ferramentas e montou um fluxo com IA, uma API, um protótipo e uma análise. Falta a parte que transforma estudo em contratação: mostrar.") + '''
<section class="sec" id="o-que-querem">
  <h2><span class="sn">1</span>O que um recrutador de AI Builder quer ver</h2>
  <p class="gancho">Certificado ou coisa funcionando?</p>
  <p>Vagas de AI Builder costumam deixar claro: o que conta é o que você construiu. Os itens que aparecem nas descrições são automações que economizaram horas de verdade, ferramentas internas publicadas, dashboards funcionando, agentes resolvendo um problema de negócio e demos construídas do zero em poucos dias. Repare no padrão: <mark class="hl">cada item tem um resultado</mark>, não só uma tecnologia.</p>
  ''' + ponte("Resultado precisa de número. Como medir horas economizadas sem inventar?", "Uma conta simples, com a origem de cada número.") + '''
</section>

<section class="sec" id="medir">
  <h2><span class="sn">2</span>Medir horas economizadas</h2>
  <p class="gancho">"Economizou tempo" não convence. Quanto, e como você sabe?</p>
  <div class="formula">horas por mês = (minutos antes − minutos depois) × vezes por mês ÷ 60<small>Meça "antes" cronometrando algumas vezes; "vezes por mês" vem do histórico, não da memória.</small></div>
  <div class="ex rv"><span class="t">Exemplo resolvido (números hipotéticos)</span>
    <div class="l"><div>Montar um documento padrão levava 30 minutos; com a automação, 3. Economia: 27 minutos por documento.</div></div>
    <div class="l"><div>O histórico mostra 40 documentos por mês.</div></div>
    <div class="l"><div>27 × 40 = 1.080 minutos; ÷ 60 = <b>18 horas por mês</b>.</div></div>
    <div class="l"><div>No currículo: "reduzi de 30 para 3 minutos por documento, cerca de 18 h/mês com o volume atual". Com o volume real, a conta é a mesma.</div></div>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span>Arredondar para cima ou somar ganhos que não aconteceram ("vai economizar 100 horas quando todo mundo usar"). Na entrevista, a primeira pergunta é "como você mediu?".</div>
  ''' + ponte("O número está certo. Onde ele mora?", "No README de cada projeto.") + '''
</section>

<section class="sec" id="readme">
  <h2><span class="sn">3</span>O README que convence</h2>
  <p class="gancho">O recrutador abre o seu repositório por 30 segundos. O que ele precisa ver?</p>
''' + code('''# Triagem de pedidos com IA

**Problema:** pedidos chegavam por formulário e eram separados à mão.
**Solução:** n8n recebe o formulário, um modelo classifica, uma API própria
decide a fila e o fluxo avisa o responsável.
**Resultado:** triagem de ~4 min para segundos; ~6 h/mês com o volume de teste.

![demo](docs/demo.gif)

## Como rodar
docker compose up -d   # n8n + API
# importe workflow.json no n8n e cadastre as credenciais

## Como foi medido
Cronometrei 10 triagens manuais (média 4 min) e usei 90 pedidos/mês do histórico.

## Limitações
- Classificação erra em mensagens com dois assuntos (3 de 50 nos testes).
- Dados de exemplo são fictícios.''') + '''
  <p>A ordem importa: problema, solução, resultado e uma demo visual no topo; como rodar no meio; como mediu e limitações no fim. Admitir limitação conta a seu favor: mostra que você testou.</p>
  ''' + ponte("Quais projetos colocar?", "Os que a própria trilha já produziu.") + '''
</section>

<section class="sec" id="projetos">
  <h2><span class="sn">4</span>Os projetos da trilha</h2>
  <p class="gancho">O que sai de cada fase, pronto para o portfólio?</p>
  <div class="demo" data-demo="checks" data-key="portfolio">
    <h4>Portfólio de AI Builder</h4>
    <label style="display:block"><input type="checkbox"> Fluxo de triagem com IA no n8n, com tratamento de erro (cap. 2).</label>
    <label style="display:block"><input type="checkbox"> O mesmo fluxo no Make ou Zapier, com a comparação de custo (cap. 3).</label>
    <label style="display:block"><input type="checkbox"> compose.yaml que sobe n8n e API juntos (caps. 4 e 7).</label>
    <label style="display:block"><input type="checkbox"> Protótipo publicado com link e GIF (cap. 6).</label>
    <label style="display:block"><input type="checkbox"> API com testes passando no README (cap. 7).</label>
    <label style="display:block"><input type="checkbox"> Análise com conferência e conclusão honesta (cap. 8).</label>
    <label style="display:block"><input type="checkbox"> Cada README com problema, resultado, como mediu e limitações.</label>
    <p class="muted"><b class="chk-n"></b> prontos</p>
  </div>
  <div class="nota lembra"><span class="lbl">Repositório público</span>Nada de dado de cliente, de empresa ou de processo real nos exemplos. Use dados fictícios e diga no README que são fictícios.</div>
  ''' + ponte("A trilha termina aqui. A próxima volta é repetir com problemas maiores.", "Escolha um processo real e chato, e automatize.") + '''
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento da trilha</h2>
  ''' + resumo([
    "Portfólio de AI Builder mostra resultado, não só tecnologia.",
    "Horas/mês = (antes − depois) × vezes por mês ÷ 60, com a origem de cada número.",
    "README: problema, solução, resultado e demo no topo; como rodar; como mediu; limitações.",
    "Dados fictícios em repositório público.",
  ]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "d", "Uma tarefa caiu de 20 para 5 minutos e acontece 60 vezes por mês. Quantas horas por mês?", [("a", "5"), ("b", "10"), ("c", "20"), ("d", "15")], "(20 − 5) × 60 = 900 minutos; 900 ÷ 60 = 15 horas.") + '''
  ''' + quiz(2, "a", "Qual frase de currículo resiste à pergunta “como você mediu?”", [("a", "Reduzi de 30 para 3 min por documento, cerca de 18 h/mês com 40 documentos/mês"), ("b", "Economizei muito tempo da equipe"), ("c", "Vai economizar 100 h quando todos usarem"), ("d", "Automação revolucionária com IA")], "Só a primeira traz antes, depois e volume, cada um verificável.") + '''
  ''' + quiz(3, "c", "Por que listar limitações no README?", [("a", "Porque é obrigatório no GitHub"), ("b", "Para diminuir o projeto"), ("c", "Mostra que você testou e conhece onde a solução falha"), ("d", "Não se deve listar")], "Quem testou de verdade sabe onde quebra. Isso passa mais confiança que um projeto sem defeito declarado.") + '''
  ''' + flash([
    ("Fórmula de horas economizadas", "(minutos antes − minutos depois) × vezes por mês ÷ 60."),
    ("Topo do README", "Problema, solução, resultado e uma demo visual."),
    ("Dado em repositório público", "Sempre fictício, e dito no README."),
    ("O que vagas de AI Builder pedem", "Automações com horas economizadas, ferramentas publicadas, dashboards, agentes e demos feitas do zero."),
  ]) + '''
</section>'''
chapter(PASTA, 9, "portfolio", TITULO, "Portfólio de AI Builder", "Capítulo 9 · Fase 5", "Transformar o que a trilha produziu em prova de que você constrói com IA.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards"], b, S)
print("ai-builder ok")
