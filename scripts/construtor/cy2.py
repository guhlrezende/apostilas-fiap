from cy_manifest import *
T = TITULO
S = ["demos/cyber.js"]
S_SQL = ["../banco-de-dados/bases.js", "demos/cyber.js", "../banco-de-dados/demos/cap-8.js"]

# ---------------- CAP 3 ----------------
body3 = recap("No Capítulo 2 você viu que o IP identifica cada máquina por um número. Só que ninguém digita <code>142.250.78.46</code> para abrir um site: digitamos <code>google.com</code>. Alguém precisa traduzir o nome para o número, e esse alguém é uma hierarquia inteira de servidores.") + '''
<section class="sec" id="o-que-e">
  <h2><span class="sn">1</span>DNS: de nome para endereço</h2>
  <p class="gancho">A agenda de contatos da internet.</p>
  <p>O <b>DNS</b> (<i>Domain Name System</i>) é o sistema que <b>aponta nomes de domínio para endereços IP</b>. Sem ele, você teria de decorar o IP de cada site. É uma <b>hierarquia de servidores</b> organizada em árvore, e nenhum servidor sozinho sabe tudo. Ao digitar um endereço, o computador faz uma <b>consulta DNS</b>: pergunta ao servidor DNS mais próximo, que responde com o IP ou <b>encaminha</b> a pergunta a outro servidor que possa saber.</p>
  <h3>Os três níveis (e o que cada um sabe)</h3>
  <div class="grid3">
    <div class="card rv"><b>1. Raiz</b><p>Não conhece os sites: conhece <b>quem cuida de cada TLD</b> (.com, .org, .br...). (Há 13 identidades de servidores raiz, cada uma replicada em centenas de locais.)</p></div>
    <div class="card rv"><b>2. TLD</b><p>O servidor do domínio de topo (<i>.com</i>, <i>.br</i>). Conhece <b>quem é autoritativo</b> para cada domínio sob ele.</p></div>
    <div class="card rv"><b>3. Autoritativo</b><p>Guarda os <b>registros finais</b> do domínio e <b>responde diretamente</b>. É o fim da cadeia: tem o IP de verdade.</p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado</span>É comum ver os três níveis descritos com o mesmo texto, como se todos guardassem "os TLDs". Não é: <b>raiz</b> conhece os TLDs, <b>TLD</b> conhece os autoritativos, <b>autoritativo</b> tem o IP final.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Como essas três perguntas acontecem, em ordem, quando você abre um site?</div><p>Acompanhe passo a passo.</p></div>
</section>

<section class="sec" id="resolucao">
  <h2><span class="sn">2</span>A consulta, passo a passo</h2>
  <p class="gancho">Descobrir <code>www.exemplo.com.br</code> numa cache vazia.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Você pergunta ao resolvedor</b><p>O navegador pergunta ao <b>resolvedor</b> (o servidor DNS configurado, geralmente o do provedor ou um público): "qual o IP de <code>www.exemplo.com.br</code>?". Antes, ele confere o <b>cache</b>: se já sabe e a resposta ainda é válida, responde na hora e acabou.</p></div>
      <div class="st"><b>2. O resolvedor consulta a raiz</b><p>Sem cache, ele pergunta a um servidor <b>raiz</b>. A raiz não sabe o IP, mas responde: "para <code>.br</code>, pergunte a estes servidores".</p></div>
      <div class="st"><b>3. Consulta ao TLD</b><p>O servidor de <code>.br</code> também não sabe o IP, mas sabe quem é <b>autoritativo</b> por <code>exemplo.com.br</code> e indica.</p></div>
      <div class="st"><b>4. Consulta ao autoritativo</b><p>O servidor autoritativo tem o <b>registro A</b> e responde com o IP.</p></div>
      <div class="st"><b>5. A resposta volta e vai para o cache</b><p>O resolvedor devolve o IP ao seu computador e <b>guarda</b> a resposta pelo tempo do <b>TTL</b>. A próxima pessoa que perguntar a mesma coisa recebe a resposta pronta.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <p>Agora faça você uma consulta de verdade. Troque o domínio e o tipo de registro e observe o <b>TTL</b>:</p>
  <div class="demo" data-demo="dnsquery"></div>
</section>

<section class="sec" id="registros">
  <h2><span class="sn">3</span>Registros, cache e tipos de DNS</h2>
  <p class="gancho">O "registro DNS" é a informação guardada no servidor autoritativo.</p>
  <div class="tablewrap"><table>
    <tr><th>Registro</th><th>O que faz</th><th>Exemplo</th></tr>
    <tr><td><code>A</code></td><td>aponta um nome para um endereço <b>IPv4</b></td><td><code>exemplo.com → 203.0.113.7</code></td></tr>
    <tr><td><code>AAAA</code></td><td>aponta um nome para um endereço <b>IPv6</b></td><td>(complemento)</td></tr>
    <tr><td><code>CNAME</code></td><td>cria um <b>alias</b>: um nome que aponta para outro nome</td><td><code>www → exemplo.com</code></td></tr>
    <tr><td><code>MX</code></td><td>diz <b>qual servidor de e-mail</b> recebe as mensagens do domínio</td><td><code>exemplo.com → mail.exemplo.com</code></td></tr>
    <tr><td><code>NS</code></td><td>indica os servidores de nomes <b>autoritativos</b> do domínio</td><td></td></tr>
    <tr><td><code>TXT</code></td><td>guarda texto livre: <b>verificação de domínio</b>, chaves públicas, regras anti-spam</td><td></td></tr>
  </table></div>
  <ul>
    <li><b>Cache DNS</b>: armazena respostas recentes para <b>acelerar</b> as consultas seguintes, sem precisar perguntar ao autoritativo toda vez. Cada resposta tem um <b>TTL</b> (tempo de vida); ao expirar, é perguntada de novo. É por isso que uma mudança de DNS leva tempo para "propagar".</li>
    <li><b>DNS público</b> (Google 8.8.8.8, Cloudflare 1.1.1.1, OpenDNS): servidores abertos a qualquer pessoa, geralmente gratuitos. <b>DNS privado</b>: de uso interno de uma empresa ou organização, que controla os nomes da própria rede.</li>
  </ul>
  <h3>Duas ferramentas do dia a dia (ARP e tracert)</h3>
<pre><code>nslookup google.com      <span class="c"># pergunta ao DNS (Windows, Linux e macOS)</span>
arp -a                   <span class="c"># mostra a tabela ARP: IP → MAC dos vizinhos da rede local</span>
tracert google.com.br    <span class="c"># Windows  (traceroute no Linux/macOS): lista os roteadores do caminho</span></code></pre>
  <p>O <b>ARP</b> (<i>Address Resolution Protocol</i>) mapeia um IP ao MAC de um dispositivo <b>na rede local</b>: antes de falar com alguém, o host consulta a própria tabela ARP e, se não houver entrada, envia um <i>ARP Request</i>. O <b>tracert</b> rastreia o caminho de um pacote até o destino e mostra os IPs de todos os roteadores intermediários, o que ajuda a achar onde há atraso ou falha.</p>
  <div class="nota exemplo"><span class="lbl">Atividade prática da aula (no seu computador)</span>Subir um servidor web local com <code>python -m http.server 8080</code>, capturar o tráfego com o <b>Wireshark</b> e observar o que passa em HTTP. Faça isso <b>só na sua própria máquina e rede</b>: capturar tráfego de terceiros sem autorização é crime. O Capítulo 4 usa essa prática para explicar o ataque.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>DNS</b> traduz nome em IP, numa hierarquia: <b>raiz</b> (conhece os TLDs) → <b>TLD</b> (conhece os autoritativos) → <b>autoritativo</b> (tem o IP).",
    "Registros: <b>A</b> (IPv4), <b>AAAA</b> (IPv6), <b>CNAME</b> (alias), <b>MX</b> (e-mail), <b>NS</b> (servidores de nomes), <b>TXT</b> (texto/verificação).",
    "<b>Cache</b> acelera; o <b>TTL</b> diz por quanto tempo a resposta vale.",
    "<b>Público</b> (aberto a todos) x <b>privado</b> (interno de uma organização).",
    "<b>ARP</b>: IP → MAC na rede local. <b>tracert</b>: mostra o caminho dos pacotes."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Qual servidor DNS tem o registro final com o IP de um domínio?", [("a","O autoritativo."),("b","O servidor raiz."),("c","O servidor de TLD.")], "A raiz indica o TLD, o TLD indica o autoritativo, e o autoritativo responde com o IP.") + quiz(2, "b", "Para que serve o registro MX?", [("a","Apontar um nome para um IP."),("b","Indicar qual servidor de e-mail recebe as mensagens do domínio."),("c","Guardar uma chave de verificação.")], "MX vem de <i>Mail eXchange</i>. O registro que aponta para um IP é o A, e o TXT guarda textos como verificações.") + quiz(3, "c", "Por que uma mudança de DNS demora a 'propagar'?", [("a","Porque o DNS é lento."),("b","Porque os servidores raiz precisam aprovar."),("c","Porque os resolvedores guardam a resposta antiga em cache até o TTL expirar.")], "Cada resolvedor reaproveita a resposta pelo tempo do TTL. Só depois que ela expira é que ele pergunta de novo e vê o valor novo.") + flash([
    ("O que faz o cache DNS?", "Guarda respostas recentes para acelerar consultas futuras, até o TTL expirar."),
    ("CNAME em uma frase?", "Um alias: um nome que aponta para outro nome."),
    ("O que o ARP resolve?", "Descobre o MAC address de um dispositivo a partir do IP, na rede local."),
    ("O que o tracert mostra?", "Os roteadores por onde o pacote passa até o destino, com os tempos de cada salto.")]) + ponte("O DNS confia em quem responde. O que acontece se alguém mentir?", "É o assunto do próximo capítulo.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "dns", T, "DNS: a agenda da internet", "Capítulo 3 · Aula 2",
        "Como um nome vira um endereço, passo a passo, e o que cada servidor da hierarquia sabe.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "consulta DNS real"], body3, scripts=S)

# ---------------- CAP 4 ----------------
body4 = recap("No Capítulo 3 você viu que o DNS responde com o que o servidor guarda, e que o resolvedor <b>acredita</b> na resposta e a guarda em cache. Essa confiança é o ponto fraco. Neste capítulo, três maneiras de explorá-la, e as defesas.") + '''
<section class="sec" id="spoofing">
  <h2><span class="sn">1</span>DNS spoofing: a resposta falsa</h2>
  <p class="gancho">Você digitou o endereço certo e foi parar no site errado.</p>
  <p>O <b>DNS spoofing</b> (ou envenenamento de cache) <b>corrompe as informações guardadas no cache DNS</b> para redirecionar o tráfego a um site malicioso. O atacante <b>intercepta as consultas</b> entre o usuário e o servidor DNS e envia <b>respostas falsas</b>; a vítima passa a acessar o site do atacante, que costuma ser uma cópia do original, para <b>roubar senhas ou dados financeiros</b>. É justamente o <b>cache</b> que é envenenado.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>Normal</b><p>Você pergunta o IP de <code>banco.exemplo</code>. O DNS responde <code>203.0.113.7</code> (o IP verdadeiro). Você acessa o site real.</p></div>
      <div class="st"><b>1. O atacante se posiciona</b><p>Ele fica onde enxerga ou influencia as consultas (uma rede Wi-Fi aberta, um roteador comprometido).</p></div>
      <div class="st"><b>2. A resposta falsa chega primeiro</b><p>Ele responde à sua consulta com <code>198.51.100.66</code> (o IP do <b>site falso</b>). O resolvedor aceita e <b>guarda em cache</b>.</p></div>
      <div class="st"><b>3. Você é enganado</b><p>Você digitou o endereço certo, e o navegador mostra uma página igual à do banco. Se você digitar a senha, o atacante a recebe.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <p><b>Defesas:</b> <b>HTTPS</b> com certificado válido (o site falso não consegue um certificado do banco, e o navegador avisa); <b>DNSSEC</b> (as respostas DNS são assinadas digitalmente, e o resolvedor confere a assinatura); <b>DNS cifrado</b> (DoH e DoT); e nunca ignorar o aviso de certificado do navegador. Um IoT simples também pode checar o IP devolvido contra um IP de referência conhecido.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se o atacante nem quisesse enganar você, e sim usar o DNS como um cano para sair da rede?</div><p>É o DNS tunneling.</p></div>
</section>

<section class="sec" id="tunneling">
  <h2><span class="sn">2</span>DNS tunneling: o túnel dentro do DNS</h2>
  <div class="nota lembra"><span class="lbl">Complemento</span>O DNS tunneling, a comparação HTTP x HTTPS e as defesas DNSSEC, DoH e DoT não vieram do slide da aula: são pesquisa de estudo, para completar o assunto.</div>
  <p class="gancho">O tráfego que quase ninguém inspeciona.</p>
  <p>O <b>DNS tunneling</b> esconde dados e comandos dentro do tráfego DNS, usando o protocolo como um <b>canal secreto</b> entre uma máquina comprometida e um servidor do atacante. O ataque não depende de uma falha do protocolo, e sim de um hábito de configuração: a maioria dos firewalls <b>não filtra nem inspeciona o DNS de saída</b>, porque ele é visto como tráfego de infraestrutura, essencial para tudo funcionar.</p>
  <ol>
    <li><b>Comprometimento:</b> a vítima instala um malware.</li>
    <li><b>Infraestrutura:</b> o atacante registra um domínio e configura um servidor de nomes autoritativo próprio para ele.</li>
    <li><b>Codificação:</b> o malware coloca os dados <b>dentro de subdomínios</b> de consultas DNS (em base32 ou base64).</li>
    <li><b>Tráfego "normal":</b> as consultas saem como DNS comum, passam pelo resolvedor e chegam ao servidor do atacante, que decodifica o dado e responde com novos comandos escondidos (por exemplo, em registros TXT).</li>
  </ol>
  <p>Usos: <b>comando e controle (C2)</b>, <b>exfiltração de dados</b> e entrega de novos payloads. Veja como um texto vira consultas (o domínio é fictício):</p>
  <div class="demo" data-demo="tunel"></div>
  <div class="nota lembra"><span class="lbl">Dois ângulos do mesmo ponto cego</span>O <b>spoofing</b> ataca o <b>cache</b> (envenena o que já está guardado). O <b>tunneling</b> ataca a <b>confiança implícita</b> que a rede dá ao protocolo. Em ambos, a defesa começa em <b>não tratar o DNS como inofensivo</b>: monitorar volume, tamanho e aparência dos nomes consultados.</div>
</section>

<section class="sec" id="mitm">
  <h2><span class="sn">3</span>ARP spoofing e man in the middle</h2>
  <p class="gancho">Quando o atacante vira o carteiro.</p>
  <p>No <b>man in the middle</b> (MITM), o atacante se coloca <b>entre</b> você e o servidor e passa a ler (ou alterar) o que trafega. Formas comuns: um <b>Wi-Fi público falso</b>, o <b>DNS spoofing</b> e o <b>ARP spoofing</b>. Neste último, o atacante responde a pedidos ARP dizendo "o IP do roteador é <i>este MAC</i>" (o dele), e os dispositivos da rede local passam a mandar o tráfego para ele em vez de para o roteador.</p>
  <p>E é aqui que a atividade prática da aula fecha o ciclo. O servidor <code>python -m http.server</code> usa <b>HTTP</b>, que trafega em <b>texto aberto</b>. Na captura do Wireshark, tudo que entra e sai (URLs, formulários, senhas) aparece legível. Com <b>HTTPS</b>, o conteúdo é cifrado com TLS, e quem está no meio vê só bytes sem sentido.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>HTTP</th><th>HTTPS</th></tr>
    <tr><td><b>Conteúdo para quem captura</b></td><td>legível (texto aberto)</td><td>cifrado (só dá para ver com quem se comunica e quanto)</td></tr>
    <tr><td><b>Identidade do servidor</b></td><td>não verificada</td><td>verificada por <b>certificado</b></td></tr>
    <tr><td><b>Um atacante no meio pode alterar?</b></td><td>sim, sem ninguém notar</td><td>não, sem que o navegador avise</td></tr>
  </table></div>
  <div class="nota cuidado"><span class="lbl">Cuidado</span>O cadeado não diz que o site é <b>confiável</b>, só que a conexão é <b>cifrada</b> e o certificado confere com o domínio. Um site de phishing também pode ter HTTPS. Confira sempre o <b>domínio</b>.</div>
  <p><b>Defesas:</b> HTTPS sempre, <b>nunca</b> ignorar aviso de certificado, VPN em Wi-Fi público, e em redes corporativas, recursos como <i>Dynamic ARP Inspection</i> nos switches.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>DNS spoofing</b>: resposta DNS falsa (cache envenenado) leva a um site do atacante. Defesas: HTTPS, <b>DNSSEC</b>, DNS cifrado (DoH/DoT).",
    "<b>DNS tunneling</b>: dados escondidos em subdomínios. Explora a falta de inspeção do DNS de saída. Sinais: nomes longos e aleatórios, volume alto, muitos TXT.",
    "<b>ARP spoofing</b>: o atacante diz ser o roteador na rede local, e vira um MITM.",
    "<b>MITM</b>: ler ou alterar o que trafega. Com <b>HTTP</b> dá para ler tudo; com <b>HTTPS</b> não.",
    "O cadeado indica conexão cifrada, e <b>não</b> site confiável."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que o DNS tunneling passa por muitos firewalls?", [("a","Porque o DNS é cifrado por padrão."),("b","Porque o DNS de saída costuma ser liberado e pouco inspecionado."),("c","Porque o atacante quebra o firewall.")], "É uma falha de configuração, e não do protocolo: o DNS é essencial, então fica liberado e sem inspeção profunda.") + quiz(2, "c", "O que o HTTPS impede, no cenário do Wireshark?", [("a","Que alguém tenha acesso à rede."),("b","Que o site exista."),("c","Que quem captura o tráfego leia o conteúdo.")], "O TLS cifra a conversa. Quem captura vê só bytes sem sentido, e não as URLs, formulários ou senhas.") + quiz(3, "a", "Qual a diferença central entre spoofing e tunneling de DNS?", [("a","Spoofing engana a vítima com uma resposta falsa; tunneling usa o DNS como canal escondido para dados e comandos."),("b","Nenhuma: são o mesmo ataque."),("c","Spoofing só funciona em IPv6.")], "O spoofing ataca o que o resolvedor guarda; o tunneling aproveita que o DNS é raramente inspecionado.") + flash([
    ("O que é DNSSEC?", "Um conjunto de extensões que assina digitalmente as respostas DNS, para o resolvedor poder verificar que não foram forjadas."),
    ("Sinais de DNS tunneling?", "Subdomínios longos e aleatórios, muitas consultas a um só domínio, muitas respostas TXT, domínio recém-registrado."),
    ("O que é ARP spoofing?", "Responder pedidos ARP com o MAC do atacante para desviar o tráfego da rede local para ele."),
    ("O cadeado garante um site confiável?", "Não: garante conexão cifrada e certificado compatível com o domínio. Phishing também pode usar HTTPS.")]) + ponte("Esses ataques miram a rede. Quais miram a pessoa, a máquina e a aplicação?", "O próximo capítulo faz o catálogo completo.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "ataques-a-rede", T, "Ataques à rede e ao DNS", "Capítulo 4 · Aulas 2 e 6",
        "Três formas de explorar a confiança da rede, e como cada uma é detectada e evitada.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "foco defensivo"], body4, scripts=S)

# ---------------- CAP 5 ----------------
body5 = recap("Os capítulos 1 a 4 deram a base de rede e os ataques à rede e ao DNS (DNS spoofing, DNS tunneling, ARP spoofing e MITM). Agora o mapa completo. <b>Atenção:</b> da Aula 6, só a <b>lista</b> de ataques veio da aula; as explicações, exemplos e defesas deste capítulo são de estudo e ainda não foram conferidos com o slide. Um jeito fácil de organizar: alguns ataques miram a <b>pessoa</b>, outros o <b>computador</b>, outros a <b>rede</b> e outros a <b>aplicação</b>.") + '''
<section class="sec" id="visao">
  <h2><span class="sn">1</span>O mapa dos ataques</h2>
  <p class="gancho">Antes de decorar nomes, pergunte: o que está sendo atacado?</p>
  <div class="tablewrap"><table>
    <tr><th>Ataque</th><th>Alvo</th><th>Em uma frase</th></tr>
    <tr><td>Phishing</td><td>Pessoa</td><td>mensagem falsa para roubar senha ou dado</td></tr>
    <tr><td>Spear phishing / whaling</td><td>Pessoa</td><td>phishing sob medida para uma pessoa ou um executivo</td></tr>
    <tr><td>Engenharia social</td><td>Pessoa</td><td>manipular alguém para ele mesmo abrir a porta</td></tr>
    <tr><td>Malware, ransomware, trojan</td><td>Máquina</td><td>programa malicioso; o ransomware sequestra os arquivos</td></tr>
    <tr><td>DoS / DDoS</td><td>Rede / serviço</td><td>derrubar um serviço com excesso de requisições</td></tr>
    <tr><td>Man in the middle, DNS spoofing</td><td>Rede</td><td>ficar no meio da conversa, ou desviar com resposta falsa (Capítulo 4)</td></tr>
    <tr><td>Força bruta</td><td>Aplicação</td><td>testar senhas até acertar</td></tr>
    <tr><td>SQL injection / XSS</td><td>Aplicação</td><td>injetar código por um campo do site</td></tr>
  </table></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O elo mais fraco costuma ser a pessoa. Como ela é atacada?</div><p>Começamos por ela.</p></div>
</section>

<section class="sec" id="pessoa">
  <h2><span class="sn">2</span>Ataques contra a pessoa</h2>
  <p class="gancho">Quebrar um sistema é difícil. Convencer alguém é mais fácil.</p>
  <h3>Phishing</h3>
  <p>Mensagem que <b>finge ser de alguém confiável</b> (banco, escola, Correios) para você clicar num link, baixar um anexo ou digitar a senha. Por e-mail é o phishing; por SMS, <i>smishing</i>; por ligação, <i>vishing</i>. <b>Sinais:</b> urgência ("sua conta será bloqueada hoje"), remetente ou link com domínio estranho, pedido de senha ou de código de verificação. <b>Defesa:</b> desconfiar da urgência, conferir o domínio antes de clicar, <b>nunca</b> passar código de verificação, usar 2FA.</p>
  <h3>Spear phishing e whaling</h3>
  <p>O <b>spear phishing</b> é phishing <b>direcionado</b>: o atacante pesquisa a vítima (redes sociais) e escreve uma mensagem que parece real, citando nome, cargo e colegas. O <b>whaling</b> mira <b>executivos</b> (o "peixe grande"): o clássico é o e-mail "do CEO" pedindo uma transferência urgente. <b>Defesa:</b> confirmar pedidos de pagamento ou de dados por <b>outro canal</b> (ligar para a pessoa).</p>
  <h3>Engenharia social</h3>
  <p>Explorar a <b>confiança, o medo ou a vontade de ajudar</b> em vez de quebrar o sistema. O phishing é um tipo. Outros exemplos: alguém liga dizendo ser do suporte e pede a sua senha; alguém entra no prédio <b>atrás de você</b>, sem crachá (<i>tailgating</i>); um pen drive "esquecido" no estacionamento. <b>Defesa:</b> treinamento, regra de nunca passar senha, conferir identidade.</p>
  <p>Treine o olho. Esta mensagem é legítima ou suspeita?</p>
  <div class="card sorter rv" data-demo="sorter" data-opts="ok:Legítima|sus:Suspeita">
    <div class="item" data-ans="sus"><p>"URGENTE: sua conta foi bloqueada. Confirme seus dados em <b>banco-seguro-login.exemplo</b> em até 2 horas ou será encerrada."</p><span class="why">Suspeita: urgência, ameaça e um domínio que não é o do banco. O banco real não pede dados por link.</span></div>
    <div class="item" data-ans="ok"><p>Você abriu o app do banco, pediu um boleto e recebeu no e-mail cadastrado o boleto com o valor e o vencimento que você escolheu.</p><span class="why">Legítima: foi <b>você</b> quem iniciou a ação, e a mensagem confere com o que você pediu.</span></div>
    <div class="item" data-ans="sus"><p>Mensagem "do diretor financeiro": "Estou em reunião e não posso falar. Faça agora uma transferência para este novo fornecedor e me confirme."</p><span class="why">Suspeita: é o padrão de whaling. Pressão de tempo, canal único e mudança de dados de pagamento. Confirme por outro canal.</span></div>
    <div class="item" data-ans="sus"><p>"Passei na frente do seu prédio: me manda o código de 6 dígitos que chegou no seu celular para eu confirmar sua entrega."</p><span class="why">Suspeita: <b>código de verificação nunca se passa</b> a ninguém. É o 2FA sendo roubado por engenharia social.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
</section>

<section class="sec" id="maquina-rede">
  <h2><span class="sn">3</span>Contra a máquina e contra a rede</h2>
  <p class="gancho">Programas maliciosos e excesso de tráfego.</p>
  <h3>Malware, ransomware e trojan</h3>
  <p><b>Malware</b> é o nome geral de software malicioso. O <b>trojan</b> (cavalo de Troia) parece um programa legítimo (crack de jogo, "atualização") mas traz o código malicioso junto. O <b>ransomware</b> <b>criptografa</b> os arquivos e cobra resgate para devolver a chave. <b>Defesa:</b> não instalar de fonte duvidosa, manter o sistema atualizado, antivírus e, acima de tudo, <b>backup offline</b>: uma cópia desconectada não é atingida e permite restaurar sem pagar. Parte do malware usa o <b>DNS tunneling</b> (Capítulo 4) para falar com o atacante.</p>
  <h3>DoS e DDoS</h3>
  <p><b>DoS</b> (<i>Denial of Service</i>) sobrecarrega um serviço até ele parar de responder. <b>DDoS</b> é o mesmo vindo de <b>milhares de máquinas</b> ao mesmo tempo, geralmente uma <b>botnet</b> (computadores e câmeras IoT infectados). Não rouba dado: o objetivo é <b>derrubar</b> (site fora do ar é prejuízo). <b>Defesa:</b> serviços de mitigação e CDN (Cloudflare, AWS Shield), limite de requisições.</p>
</section>

<section class="sec" id="aplicacao">
  <h2><span class="sn">4</span>Contra a aplicação</h2>
  <p class="gancho">O site que pede senha e aceita comentários.</p>
  <h3>Força bruta</h3>
  <p>Testar combinações de senha até acertar. Variações: <b>dicionário</b> (lista de senhas comuns) e <i>credential stuffing</i> (usar senhas vazadas de outro site). <b>Defesa:</b> senha longa, bloqueio após várias tentativas, CAPTCHA e 2FA. Veja quanto o <b>tamanho</b> pesa:</p>
  <div class="demo" data-demo="senha"></div>
  <h3>SQL injection</h3>
  <p>O atacante digita <b>código SQL</b> num campo do site, e o sistema o executa no banco. Se o programa monta a consulta <b>colando</b> o texto do usuário, um texto como <code>' OR '1'='1</code> transforma a condição da consulta em algo sempre verdadeiro (num login, passa sem senha; na demo abaixo, uma busca por nome devolve todos os registros). Teste na demo abaixo, que roda de verdade num banco de exemplo (a mesma da apostila de Bancos de Dados):</p>
  <div class="demo" data-demo="inject"></div>
  <p><b>Defesa:</b> <b>consultas parametrizadas</b> (nunca concatenar texto do usuário no SQL), validação de entrada e <b>menor privilégio</b> para o usuário do banco.</p>
  <h3>XSS (Cross-Site Scripting)</h3>
  <p>O atacante injeta <b>JavaScript</b> numa página (por exemplo, num comentário), e ele roda no navegador de <b>quem abrir a página</b>, podendo roubar a sessão. <b>Defesa:</b> <b>escapar</b> o HTML do que o usuário digita (tratar como texto, e não como marcação) e usar <i>Content Security Policy</i>.</p>
  <div class="demo" data-demo="xss"></div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Organize por <b>alvo</b>: pessoa (phishing, engenharia social), máquina (malware), rede (DDoS, MITM), aplicação (força bruta, SQL injection, XSS).",
    "<b>Spear phishing</b> é direcionado; <b>whaling</b> mira executivos. Confirme pedidos por <b>outro canal</b>.",
    "<b>Ransomware</b> criptografa e cobra resgate. A defesa-chave é o <b>backup offline</b>.",
    "<b>DDoS</b> não rouba dados: derruba o serviço, com uma botnet.",
    "<b>SQL injection</b>: use consultas parametrizadas. <b>XSS</b>: escape a saída.",
    "<b>Código de verificação nunca se passa</b> a ninguém."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que o backup offline é a principal defesa contra ransomware?", [("a","Porque impede o vírus de entrar."),("b","Porque uma cópia desconectada não é criptografada, e permite restaurar sem pagar."),("c","Porque o antivírus não funciona.")], "O ransomware criptografa o que está acessível. O que está fora do alcance dele sobrevive.") + quiz(2, "c", "Qual a diferença entre phishing e spear phishing?", [("a","Nenhuma."),("b","O spear phishing só acontece por telefone."),("c","O phishing é genérico e em massa; o spear phishing é direcionado e usa informações reais da vítima.")], "Quanto mais sob medida, mais convincente. Whaling é o spear phishing contra executivos.") + quiz(3, "a", "A defesa certa contra SQL injection é:", [("a","Consultas parametrizadas, sem concatenar o texto do usuário."),("b","Proibir aspas nos formulários."),("c","Esconder o nome das tabelas.")], "Filtrar caracteres falha. Separar o código SQL do dado digitado é o que resolve de verdade.") + flash([
    ("DoS x DDoS?", "DoS vem de uma origem; DDoS vem de milhares (uma botnet). Ambos buscam derrubar o serviço."),
    ("O que é um trojan?", "Programa que parece legítimo, mas traz código malicioso junto."),
    ("O que é credential stuffing?", "Testar em um site senhas vazadas de outro, apostando que a pessoa reutilizou a senha."),
    ("Como o XSS é evitado?", "Escapando o que o usuário digita ao exibir (texto, e não HTML) e com Content Security Policy.")]) + ponte("Conhecer o ataque é metade do caminho. Como me defendo?", "Com criptografia, hash, autenticação forte e camadas de defesa.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "catalogo-de-ataques", T, "Catálogo de ataques", "Capítulo 5 · Aula 6",
        "Phishing, malware, DDoS, força bruta, SQL injection e XSS, organizados por quem eles atacam.",
        ["<b>~45 min</b>", "3 demos · 1 jogo · 3 testes", "SQL injection de verdade"], body5, scripts=S_SQL, sql=True)
print("cy caps 3-5 ok")
