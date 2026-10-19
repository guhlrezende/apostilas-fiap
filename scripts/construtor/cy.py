from cy_manifest import *
S = ["demos/cyber.js"]
T = TITULO
# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo, então você não precisa saber nada de redes. Basta já ter usado a internet. A ideia de toda a apostila: <b>para se defender, é preciso entender como as coisas funcionam</b>. E tudo na internet é feito por protocolos.", "Ponto de partida") + '''
<section class="sec" id="osi">
  <h2><span class="sn">1</span>O modelo OSI: sete camadas, uma responsabilidade cada</h2>
  <p class="gancho">Como organizar algo tão complexo quanto a internet?</p>
  <p>O <b>modelo OSI</b> foi desenvolvido pela <b>ISO</b> (<i>International Organization for Standardization</i>) na <b>década de 1980</b>. É um modelo <b>teórico, de referência</b>: serve para descrever como os dados são transmitidos e recebidos e, principalmente, para <mark class="hl">diagnosticar problemas</mark> de rede camada a camada ("o cabo está ligado? o IP está certo? a porta está aberta?").</p>
  <div class="tablewrap"><table>
    <tr><th>#</th><th>Camada</th><th>Responsabilidade</th><th>Exemplos</th></tr>
    <tr><td>7</td><td><b>Aplicação</b></td><td>interface com o software final: e-mail, navegação, transferência de arquivos</td><td>HTTP, SMTP, DNS</td></tr>
    <tr><td>6</td><td><b>Apresentação</b></td><td>converte formatos e <b>criptografa</b> os dados</td><td>JPEG, AES, TLS</td></tr>
    <tr><td>5</td><td><b>Sessão</b></td><td>abre, gerencia e encerra sessões; autenticação</td><td>SSH, RPC</td></tr>
    <tr><td>4</td><td><b>Transporte</b></td><td>controla a transferência entre dispositivos: entrega, fluxo, segmentação</td><td>TCP, UDP</td></tr>
    <tr><td>3</td><td><b>Rede</b></td><td>endereça e <b>roteia</b> dados entre redes diferentes</td><td>IP, OSPF</td></tr>
    <tr><td>2</td><td><b>Enlace</b></td><td>entrega dentro da rede local, em quadros, com detecção de erro e controle de fluxo</td><td>Ethernet, Wi-Fi</td></tr>
    <tr><td>1</td><td><b>Física</b></td><td>transmite os bits pelo meio: sinais elétricos, ópticos ou de rádio</td><td>cabos, fibra, Wi-Fi, Bluetooth</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Macete (complemento)</span>Para decorar de cima para baixo (7 a 1): <b>A</b>plicação, <b>A</b>presentação, <b>S</b>essão, <b>T</b>ransporte, <b>R</b>ede, <b>E</b>nlace, <b>F</b>ísica. Há várias frases mnemônicas; invente a sua. O importante não é a ordem decorada, é saber <i>o que cada camada resolve</i>.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Se cada camada cuida de uma coisa, como a mensagem passa por todas elas?</div><p>Cada camada embrulha a mensagem com o seu cabeçalho. É o encapsulamento.</p></div>
</section>

<section class="sec" id="encapsulamento">
  <h2><span class="sn">2</span>Encapsulamento: a mensagem desce e sobe</h2>
  <p class="gancho">Como uma carta numa série de envelopes.</p>
  <p>Quem envia começa na camada de <b>aplicação</b> e desce até a <b>física</b>; a cada camada, a mensagem ganha um <b>cabeçalho</b> (<i>header</i>) com a informação que aquela camada precisa (portas, endereços IP, endereços MAC). Quem recebe faz o caminho inverso, e cada camada <b>retira</b> o seu cabeçalho e entrega o restante à de cima.</p>
  <div class="demo" data-demo="osi"></div>
  <div class="nota exemplo"><span class="lbl">Por que isso importa para segurança</span>Um ataque costuma <b>escolher uma camada</b>. DNS spoofing e SQL injection atuam na aplicação; ARP spoofing, no enlace; um DDoS pode sobrecarregar a rede ou o transporte. Saber a camada ajuda a saber <b>onde</b> defender: um firewall que só olha a camada 3 (IP) não enxerga o conteúdo de uma requisição HTTP maliciosa.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Duas camadas usam endereços: a de enlace (MAC) e a de rede (IP). Qual a diferença?</div><p>Uma serve para a rede local, outra para o mundo.</p></div>
</section>

<section class="sec" id="mac">
  <h2><span class="sn">3</span>MAC, NIC.br e sistemas autônomos (o que ficou pendente)</h2>
  <p class="gancho">Três nomes que apareceram em aula e merecem uma explicação.</p>
  <div class="grid3">
    <div class="card rv"><b>MAC address</b><p>Endereço físico de <b>48 bits</b>, gravado de fábrica na placa de rede (NIC), escrito em 12 hexadecimais (<code>00:1A:2B:3C:4D:5E</code>). Vive na <b>camada 2</b>: serve para a entrega <b>dentro da rede local</b>. O <b>IP</b> (camada 3) resolve o caminho entre redes, e o <b>ARP</b> faz a ponte (descobre o MAC de um IP).</p></div>
    <div class="card rv"><b>Sistema Autônomo (AS)</b><p>Uma rede (ou conjunto) sob <b>uma administração técnica</b>, com sua própria política de roteamento e blocos de IP: uma operadora, uma universidade, um grande provedor. Cada AS tem um número, o <b>ASN</b>. É entre ASNs que o protocolo <b>BGP</b> troca rotas, e a internet é, no fundo, uma rede de ASNs.</p></div>
    <div class="card rv"><b>NIC.br</b><p>Núcleo de Informação e Coordenação do Ponto BR: executa as decisões do <b>CGI.br</b>. Mantém o <b>Registro.br</b> (domínios .br), o <b>IX.br</b> (os PTTs, pontos onde as redes se interligam), o <b>CERT.br</b> (resposta a incidentes) e o <b>CETIC.br</b> (pesquisas).</p></div>
  </div>
  <div class="nota lembra"><span class="lbl">Sobre ByteByteGo e Miro</span>Os dois nomes citados em aula não são conceitos de rede: <b>ByteByteGo</b> é uma marca de conteúdo educacional sobre arquitetura de sistemas e redes, conhecida por diagramas didáticos, e o <b>Miro</b> é uma ferramenta de quadro branco colaborativo online, usada para desenhar diagramas.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>OSI</b>: 7 camadas (aplicação, apresentação, sessão, transporte, rede, enlace, física). Modelo de <b>referência</b>, útil para diagnosticar.",
    "<b>Encapsulamento</b>: cada camada acrescenta o seu cabeçalho ao descer, e o retira ao subir.",
    "<b>MAC</b> (48 bits, camada 2, rede local) x <b>IP</b> (camada 3, entre redes). O <b>ARP</b> liga os dois.",
    "<b>AS/ASN</b>: rede sob uma administração; o <b>BGP</b> troca rotas entre ASNs.",
    "<b>NIC.br</b> mantém Registro.br, IX.br, CERT.br e CETIC.br.",
    "Saber a <b>camada</b> de um ataque ajuda a escolher a defesa."]) + '''
  <h3>Teste rápido</h3>
  <div class="card sorter rv" data-demo="sorter" data-opts="l7:Aplicação (7)|l4:Transporte (4)|l3:Rede (3)|l2:Enlace (2)">
    <div class="item" data-ans="l4"><p><b>TCP</b>: controla a entrega confiável entre dois dispositivos.</p><span class="why">Transporte: TCP e UDP vivem na camada 4.</span></div>
    <div class="item" data-ans="l3"><p><b>IP</b>: endereça e roteia pacotes entre redes diferentes.</p><span class="why">Rede: é a camada do IP.</span></div>
    <div class="item" data-ans="l2"><p><b>Ethernet / MAC address</b>: entrega dentro da rede local.</p><span class="why">Enlace: quadros e endereços físicos.</span></div>
    <div class="item" data-ans="l7"><p><b>HTTP</b>: a conversa entre o navegador e o servidor web.</p><span class="why">Aplicação: a interface com o software final.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + quiz(1, "b", "Por que o modelo OSI é chamado de modelo de referência?", [("a","Porque é obrigatório em toda rede."),("b","Porque descreve uma organização em camadas para entender e diagnosticar redes, mesmo que as redes reais (como o TCP/IP) não o sigam ao pé da letra."),("c","Porque só existe no papel e ninguém o usa.")], "Na prática a internet usa a pilha TCP/IP (mais enxuta). O OSI continua sendo o vocabulário comum para falar de problemas por camada.") + flash([
    ("O que é encapsulamento?", "Cada camada acrescenta o seu cabeçalho à mensagem ao descer; no destino, cada uma retira o seu ao subir."),
    ("MAC x IP?", "MAC é o endereço físico de 48 bits, para a rede local (camada 2). IP é o endereço lógico, para rotear entre redes (camada 3)."),
    ("O que é um sistema autônomo?", "Uma rede sob uma única administração técnica, identificada por um ASN, que troca rotas com outras via BGP."),
    ("Para que serve o ARP?", "Descobre o MAC address de um dispositivo a partir do IP, na rede local.")]) + ponte("O OSI organiza as camadas. Como cada dispositivo é endereçado e como os dados viajam de fato?", "Com o IP, o TCP e o UDP.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "modelo-osi", T, "Redes e o modelo OSI", "Capítulo 1 · Aula 1",
        "As sete camadas, como a mensagem desce e sobe por elas, e os endereços que cada uma usa.",
        ["<b>~35 min</b>", "1 demo · 1 jogo · 1 teste · 4 flashcards", "animação do encapsulamento"], body1, scripts=S)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 você viu as camadas do OSI e que a camada de rede usa o <b>IP</b> e a de transporte usa o <b>TCP</b> ou o <b>UDP</b>. Agora abrimos essas três peças: como um endereço IP é feito, e como duas máquinas combinam a conversa.") + '''
<section class="sec" id="ip">
  <h2><span class="sn">1</span>O protocolo IP e os endereços</h2>
  <p class="gancho">Cada pacote sabe de onde vem e para onde vai.</p>
  <p>O <b>IP</b> é um protocolo <b>sem conexão</b>: não há estabelecimento prévio. Cada pacote carrega o <b>endereço de origem</b>, o <b>de destino</b> e a sequência dos dados, e é tratado de forma <b>independente</b> dos demais. É a tecnologia que entrega os dados ao destino correto <i>independentemente da rede física</i> por baixo. Existem duas versões em uso:</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>IPv4</th><th>IPv6</th></tr>
    <tr><td><b>Tamanho</b></td><td>32 bits</td><td>128 bits</td></tr>
    <tr><td><b>Endereços</b></td><td>cerca de 4,3 bilhões (4.294.967.296)</td><td>mais de 340 undecilhões (3,4 × 10³⁸)</td></tr>
    <tr><td><b>Escrita</b></td><td><code>192.168.10.77</code> (4 números de 0 a 255)</td><td><code>2001:db8::1</code> (hexadecimal, em grupos)</td></tr>
    <tr><td><b>Por que existe</b></td><td>a <b>escassez</b> de endereços motivou o IPv6</td><td>mais endereços, roteamento mais eficiente e, segundo o slide, segurança e QoS integrados (o IPsec deixou de ser obrigatório no IPv6, então não conte com isso)</td></tr>
  </table></div>
  <p>Cada um dos 4 números do IPv4 ocupa 8 bits (1 byte), e por isso vai de 0 a 255. Você pode testar a sua conexão IPv6 em <i>test-ipv6.com</i>. E há um detalhe vital para redes: os primeiros bits do endereço dizem <b>qual rede</b>, e os restantes <b>qual dispositivo</b> dentro dela. A <b>máscara</b> (ou prefixo, como <code>/24</code>) marca onde termina uma parte e começa a outra. Mexa:</p>
  <div class="demo" data-demo="ipcalc"></div>
  <div class="nota lembra"><span class="lbl">Complemento: IPs privados e NAT</span>Três faixas são <b>privadas</b>, só valem dentro da sua rede: <code>10.0.0.0/8</code>, <code>172.16.0.0/12</code> e <code>192.168.0.0/16</code>. O seu roteador faz <b>NAT</b>: troca o IP privado dos seus dispositivos pelo IP público dele ao sair para a internet. Foi uma das soluções que adiou o esgotamento do IPv4.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O IP só entrega pacotes soltos, sem garantia. Quem organiza uma conversa de verdade?</div><p>A camada de transporte, com TCP e UDP.</p></div>
</section>

<section class="sec" id="tcp-udp">
  <h2><span class="sn">2</span>TCP e UDP: confiável ou rápido</h2>
  <p class="gancho">Dois jeitos de conversar. Cada um tem o seu preço.</p>
  <div class="grid2">
    <div class="card rv"><b>TCP</b> (<i>Transmission Control Protocol</i>)<p><b>Orientado à conexão</b> e <b>confiável</b>, fim a fim. Estabelece a conexão com o <b>three-way handshake</b>, confirma o que chegou, reenvia o que se perdeu e entrega na ordem. Usado em web, e-mail, transferência de arquivos.</p></div>
    <div class="card rv"><b>UDP</b> (<i>User Datagram Protocol</i>)<p><b>Sem conexão</b>, rápido, <b>sem garantia</b> de entrega nem de ordem. Usado quando a <b>latência</b> importa mais que a precisão: jogos online, streaming de vídeo e voz, onde perder um pacote não faz diferença.</p></div>
  </div>
  <h3>O handshake de três vias</h3>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>Antes de tudo</b><p>Cliente e servidor ainda não têm conexão. O cliente quer abrir uma com o servidor (por exemplo, na porta 443 do HTTPS).</p></div>
      <div class="st"><b>1. SYN</b><p>O cliente envia uma mensagem de <b>sincronização</b> ao servidor: "quero abrir uma conexão".</p></div>
      <div class="st"><b>2. SYN-ACK</b><p>O servidor <b>responde</b> confirmando o pedido e sincronizando o seu lado: "recebi, e eu também quero".</p></div>
      <div class="st"><b>3. ACK</b><p>O cliente envia uma <b>confirmação</b> de volta. Agora a conexão está estabelecida e os dados podem fluir.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <div class="nota lembra"><span class="lbl">Complemento: portas</span>O IP leva o pacote até a <b>máquina</b>; a <b>porta</b> (número de 0 a 65535) escolhe o <b>serviço</b> naquela máquina. Algumas conhecidas: <b>80</b> HTTP, <b>443</b> HTTPS, <b>22</b> SSH, <b>25</b> SMTP, <b>53</b> DNS (que usa UDP para consultas curtas). Uma porta aberta é uma "porta de entrada" para um atacante, daí a ideia de expor <b>só</b> o que é necessário.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">3</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>IP</b>: sem conexão; cada pacote leva origem, destino e dados, e é independente dos outros.",
    "<b>IPv4</b>: 32 bits, ~4,3 bilhões de endereços. <b>IPv6</b>: 128 bits, mais de 340 undecilhões.",
    "A <b>máscara</b> (/24 etc.) separa a parte de <b>rede</b> da parte do <b>dispositivo</b>. Hosts = 2^(32 − prefixo) − 2 (para /30 ou menor; /31 e /32 são casos especiais).",
    "<b>TCP</b>: conexão, confiável, ordenada (handshake SYN → SYN-ACK → ACK). <b>UDP</b>: sem conexão, rápido, sem garantia.",
    "<b>Portas</b> escolhem o serviço: 80 HTTP, 443 HTTPS, 22 SSH, 53 DNS."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Por que o streaming de vídeo costuma usar UDP?", [("a","Porque o UDP é mais seguro."),("b","Porque o UDP garante a entrega de todos os pacotes."),("c","Porque a latência importa mais, e perder um pacote ocasional quase não faz diferença.")], "O UDP não confirma nem reenvia, e por isso é mais rápido. Para vídeo ao vivo, esperar um pacote perdido seria pior que ignorá-lo.") + quiz(2, "a", "Uma rede 192.168.10.0/24 comporta quantos dispositivos?", [("a","254 (256 menos o endereço da rede e o de broadcast)."),("b","256"),("c","24")], "O /24 deixa 8 bits para dispositivos: 2⁸ = 256 endereços, dois reservados. Teste na calculadora.") + quiz(3, "b", "Qual a ordem do handshake do TCP?", [("a","ACK, SYN, SYN-ACK"),("b","SYN, SYN-ACK, ACK"),("c","SYN-ACK, SYN, ACK")], "O cliente pede (SYN), o servidor responde confirmando (SYN-ACK) e o cliente confirma de volta (ACK).") + flash([
    ("Por que o IPv6 existe?", "Porque os 4,3 bilhões de endereços do IPv4 acabaram. O IPv6 tem 128 bits."),
    ("TCP x UDP?", "TCP: conexão e confiabilidade. UDP: velocidade, sem garantia."),
    ("O que a máscara faz?", "Separa os bits da rede dos bits do dispositivo dentro do endereço IP."),
    ("O que é uma porta?", "Um número que escolhe qual serviço da máquina recebe o pacote.")]) + ponte("Ninguém decora números de IP. Como um nome como google.com vira um endereço?", "Com o DNS, a agenda da internet.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "ip-tcp-udp", T, "IP, TCP e UDP", "Capítulo 2 · Aula 1",
        "Como um endereço é feito, como se divide em redes e como duas máquinas combinam a conversa.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "calculadora de IP"], body2, scripts=S)
print("cy caps 1-2 ok")
