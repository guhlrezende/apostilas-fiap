from cy_manifest import *
T = TITULO
S = ["demos/cyber.js"]

# ---------------- CAP 6 ----------------
body6 = recap("No Capítulo 5 você viu o catálogo de ataques. Cada um sugeriu uma defesa pontual (HTTPS, backup, parametrizar, 2FA). Este capítulo, que é <b>complemento</b> (não foi dado em aula), junta as defesas em um quadro só e explica as ferramentas por trás delas: criptografia e hash.", "Onde paramos") + '''
<section class="sec" id="cia">
  <h2><span class="sn">1</span>O que estamos protegendo: a tríade CIA</h2>
  <p class="gancho">Segurança não é "ninguém entra". São três objetivos.</p>
  <div class="grid3">
    <div class="card rv"><b style="color:var(--c0)">Confidencialidade</b><p>Só quem tem permissão <b>lê</b> a informação. Violada por vazamento, espionagem, MITM.</p></div>
    <div class="card rv"><b style="color:var(--c1)">Integridade</b><p>A informação <b>não é alterada</b> sem autorização. Violada por adulteração de dados ou resposta DNS falsa.</p></div>
    <div class="card rv"><b style="color:var(--c2)">Disponibilidade</b><p>O sistema está <b>acessível</b> quando precisa. Violada por DDoS e ransomware.</p></div>
  </div>
  <p>Todo ataque do Capítulo 5 fere um (ou mais) dos três. Perguntar "qual dos três está em risco?" ajuda a escolher a defesa certa.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Para proteger a confidencialidade, como esconder o conteúdo de quem não deve ver?</div><p>Com criptografia.</p></div>
</section>

<section class="sec" id="cripto">
  <h2><span class="sn">2</span>Criptografia: simétrica e assimétrica</h2>
  <p class="gancho">Embaralhar de um jeito que só a chave desfaz.</p>
  <p><b>Criptografar</b> é transformar um dado legível (texto claro) em um ilegível (texto cifrado) com um algoritmo e uma <b>chave</b>; <b>decifrar</b> é o caminho inverso. Veja a ideia na cifra mais antiga e simples, a de César, que também mostra por que ela é fraca:</p>
  <div class="demo" data-demo="cesar"></div>
  <div class="tablewrap"><table>
    <tr><th></th><th>Simétrica</th><th>Assimétrica</th></tr>
    <tr><td><b>Chave</b></td><td><b>uma só</b>, a mesma para cifrar e decifrar</td><td>um <b>par</b>: chave <b>pública</b> (cifra) e chave <b>privada</b> (decifra)</td></tr>
    <tr><td><b>Velocidade</b></td><td>rápida</td><td>mais lenta</td></tr>
    <tr><td><b>Problema</b></td><td>como combinar a chave com segurança?</td><td>resolve a troca de chaves, mas custa mais</td></tr>
    <tr><td><b>Exemplos</b></td><td>AES</td><td>RSA, curvas elípticas</td></tr>
  </table></div>
  <p>No dia a dia as duas trabalham juntas. No <b>HTTPS</b> (TLS), a assimétrica serve para <b>autenticar o servidor</b> (o certificado) e combinar uma chave com segurança; depois, a conversa inteira corre com uma chave <b>simétrica</b>, mais rápida. É por isso que o cadeado cobre as duas coisas: <i>com quem</i> você fala e <i>o sigilo</i> do que fala.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E a senha? Se o site a guarda cifrada, quem tem a chave lê todas.</div><p>Por isso as senhas não se cifram: usa-se hash.</p></div>
</section>

<section class="sec" id="hash">
  <h2><span class="sn">3</span>Hash: a impressão digital que não tem volta</h2>
  <p class="gancho">Conferir sem guardar.</p>
  <p>Uma <b>função de hash</b> transforma qualquer entrada em um resumo de <b>tamanho fixo</b>, de um jeito que <b>não dá para reverter</b> e em que uma mudança mínima altera tudo (o <i>efeito avalanche</i>). Use o SHA-256 do próprio navegador e compare:</p>
  <div class="demo" data-demo="hash"></div>
  <p>Daí o uso para <b>senhas</b>: o sistema guarda só o hash. No login, calcula o hash do que você digitou e compara. Quem rouba o banco não tem as senhas, apenas hashes. Mas há dois cuidados:</p>
  <ul>
    <li><b>Sal (<i>salt</i>)</b>: um texto aleatório, diferente por usuário, misturado à senha antes do hash. Sem ele, senhas iguais geram hashes iguais, e tabelas prontas de hashes (<i>rainbow tables</i>) quebram as comuns.</li>
    <li><b>Hash lento de propósito</b>: para senhas, use algoritmos desenhados para serem <b>caros</b> (bcrypt, scrypt, Argon2), e não o SHA-256 puro, que é rápido demais e facilita a força bruta (lembra da calculadora do capítulo anterior?).</li>
  </ul>
  <div class="nota cuidado"><span class="lbl">Hash também serve à integridade</span>Sites de download publicam o hash do arquivo. Você calcula o hash do que baixou: se bater, o arquivo não foi adulterado no caminho.</div>
</section>

<section class="sec" id="camadas">
  <h2><span class="sn">4</span>Defesa em profundidade</h2>
  <p class="gancho">Nenhuma defesa sozinha basta. Empilhe.</p>
  <div class="tablewrap"><table>
    <tr><th>Camada de defesa</th><th>Protege contra</th><th>Prática</th></tr>
    <tr><td><b>Pessoas</b></td><td>phishing, engenharia social</td><td>treinamento, confirmação por outro canal, nunca passar códigos</td></tr>
    <tr><td><b>Identidade</b></td><td>força bruta, roubo de senha</td><td>senhas longas e únicas, <b>2FA/MFA</b>, gerenciador de senhas</td></tr>
    <tr><td><b>Dispositivo</b></td><td>malware</td><td>atualizações, antivírus, menos programas instalados</td></tr>
    <tr><td><b>Rede</b></td><td>MITM, DDoS, tráfego malicioso</td><td>firewall, segmentação, HTTPS, VPN, DNS seguro</td></tr>
    <tr><td><b>Aplicação</b></td><td>SQL injection, XSS</td><td>consultas parametrizadas, escape de saída, validação</td></tr>
    <tr><td><b>Dados</b></td><td>vazamento, ransomware</td><td>criptografia, <b>backup 3-2-1</b> (3 cópias, 2 mídias, 1 fora do local)</td></tr>
    <tr><td><b>Acesso</b></td><td>abuso interno, conta comprometida</td><td><b>menor privilégio</b>: cada um só pode o que precisa</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">2FA em uma linha</span>Combina <i>algo que você sabe</i> (senha) com <i>algo que você tem</i> (celular, chave física) ou <i>algo que você é</i> (biometria). Mesmo que a senha vaze, falta o segundo fator. Prefira aplicativo autenticador ou chave física a SMS, que pode ser desviado.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Tríade CIA</b>: confidencialidade, integridade, disponibilidade. Todo ataque fere pelo menos um.",
    "<b>Simétrica</b>: uma chave, rápida (AES). <b>Assimétrica</b>: par público/privada (RSA). O <b>TLS</b> usa as duas.",
    "<b>Hash</b>: resumo de tamanho fixo, <b>sem volta</b>, com efeito avalanche. Para senhas: <b>sal</b> + hash lento (bcrypt, Argon2).",
    "<b>Defesa em profundidade</b>: várias camadas (pessoas, identidade, dispositivo, rede, aplicação, dados, acesso).",
    "<b>Backup 3-2-1</b> e <b>menor privilégio</b> reduzem o estrago quando algo falha."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Por que senhas devem ser guardadas como hash, e não cifradas?", [("a","Porque o hash é mais fácil de ler."),("b","Porque cifrar é proibido."),("c","Porque o hash não tem volta: quem rouba o banco não obtém as senhas, e a conferência se faz comparando hashes.")], "Se a senha fosse cifrada, quem tivesse a chave (ou a roubasse junto) leria todas. O hash elimina essa possibilidade.") + quiz(2, "a", "Qual a função do sal (salt) no armazenamento de senhas?", [("a","Fazer com que senhas iguais gerem hashes diferentes e inutilizar tabelas prontas de hashes."),("b","Deixar o hash menor."),("c","Cifrar a senha.")], "O sal é aleatório e único por usuário, e é guardado junto ao hash.") + quiz(3, "b", "No HTTPS, para que serve a criptografia assimétrica?", [("a","Cifrar todo o conteúdo da conversa, por ser mais rápida."),("b","Autenticar o servidor e combinar com segurança a chave simétrica usada na conversa."),("c","Compactar os dados.")], "A assimétrica é mais lenta. Ela abre a conversa; a simétrica, mais rápida, leva o conteúdo.") + flash([
    ("O que é a tríade CIA?", "Confidencialidade, integridade e disponibilidade: os três objetivos da segurança da informação."),
    ("Simétrica x assimétrica?", "Simétrica usa uma chave para cifrar e decifrar. Assimétrica usa um par: pública cifra, privada decifra."),
    ("O que é o efeito avalanche?", "Uma mudança mínima na entrada altera quase todo o hash."),
    ("O que é backup 3-2-1?", "3 cópias, em 2 tipos de mídia, com 1 delas fora do local.")]) + ponte("Você percorreu o caminho do dado e o do ataque.", "Volte à visão geral e refaça os testes sem olhar as respostas.", "Fim da apostila") + '''
</section>'''
chapter(PASTA, 6, "defesa", T, "Defesa: criptografia, hash e camadas", "Capítulo 6 · Complemento",
        "Os três objetivos da segurança, as ferramentas por trás das defesas e como empilhá-las.",
        ["<b>~45 min</b>", "2 demos · 3 testes · 4 flashcards", "complemento, não foi dado em aula"], body6, scripts=S)

# ---------------- CAP 7 ----------------
body7 = recap("No Capítulo 6 você montou as defesas por camada. Falta uma forma de olhar um ataque <b>inteiro</b>, como uma sequência, e perguntar em que etapa ele poderia ter sido interrompido. É o que a <b>Cyber Kill Chain</b> propõe. Este capítulo é <b>complemento</b> (não foi dado em aula) e usa um exemplo genérico, para que você aplique o modelo aos casos que estudar.", "Onde paramos") + '''
<section class="sec" id="modelo">
  <h2><span class="sn">1</span>As sete etapas</h2>
  <p class="gancho">Um ataque não acontece de uma vez. Ele tem fases.</p>
  <p>A <b>Cyber Kill Chain</b> foi proposta pela Lockheed Martin (2011), inspirada no conceito militar de "cadeia de destruição". A ideia central: se um ataque tem várias etapas encadeadas, <mark class="hl g">interromper <b>qualquer uma</b> quebra a cadeia</mark>. Quanto mais cedo, melhor e mais barato.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Reconhecimento</b> <small class="muted">(Reconnaissance)</small><p>O atacante <b>pesquisa o alvo</b>: e-mails de funcionários, tecnologias usadas, redes sociais, servidores expostos. <i>Exemplo:</i> descobre pelo LinkedIn quem é do financeiro.</p></div>
      <div class="st"><b>2. Armamento</b> <small class="muted">(Weaponization)</small><p>Prepara a <b>arma</b>: combina um código malicioso com um vetor de entrega. <i>Exemplo:</i> cria uma planilha com macro maliciosa.</p></div>
      <div class="st"><b>3. Entrega</b> <small class="muted">(Delivery)</small><p>Faz a arma <b>chegar à vítima</b>: e-mail de phishing, site infectado, pen drive. <i>Exemplo:</i> manda a planilha como "fatura em atraso".</p></div>
      <div class="st"><b>4. Exploração</b> <small class="muted">(Exploitation)</small><p>A arma <b>dispara</b>, explorando uma falha (de software ou humana). <i>Exemplo:</i> a vítima abre o arquivo e habilita a macro.</p></div>
      <div class="st"><b>5. Instalação</b> <small class="muted">(Installation)</small><p>O atacante garante <b>persistência</b>: instala um programa que sobrevive a reinícios. <i>Exemplo:</i> uma tarefa agendada que reabre o acesso.</p></div>
      <div class="st"><b>6. Comando e controle</b> <small class="muted">(C2)</small><p>A máquina comprometida <b>liga para o atacante</b> e recebe ordens. <i>Exemplo:</i> comunicação por HTTPS ou por DNS tunneling (Capítulo 4).</p></div>
      <div class="st"><b>7. Ações no objetivo</b> <small class="muted">(Actions on Objectives)</small><p>Enfim o que o atacante queria: <b>roubar dados, criptografar, destruir</b>, ou se mover pela rede até alvos maiores.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Se cada etapa pode ser interrompida, qual defesa interrompe qual?</div><p>Esse é o uso prático do modelo.</p></div>
</section>

<section class="sec" id="defesa">
  <h2><span class="sn">2</span>Onde cada defesa interrompe</h2>
  <p class="gancho">Mapear controles nas etapas mostra onde você tem buraco.</p>
  <div class="tablewrap"><table>
    <tr><th>Etapa</th><th>Defesas típicas</th></tr>
    <tr><td>1. Reconhecimento</td><td>reduzir o que se expõe publicamente, monitorar varreduras, treinamento sobre o que se publica</td></tr>
    <tr><td>2. Armamento</td><td>(acontece do lado do atacante) inteligência de ameaças, para conhecer as técnicas em uso</td></tr>
    <tr><td>3. Entrega</td><td>filtro de e-mail, bloqueio de anexos perigosos, <b>treinamento anti-phishing</b>, filtro de DNS e de web</td></tr>
    <tr><td>4. Exploração</td><td><b>atualizações</b> de software, desabilitar macros por padrão, antivírus/EDR</td></tr>
    <tr><td>5. Instalação</td><td>controle de aplicações permitidas, monitorar tarefas e serviços novos, <b>menor privilégio</b></td></tr>
    <tr><td>6. C2</td><td>filtro e <b>inspeção de saída</b> (inclusive DNS), bloqueio de domínios maliciosos, segmentação de rede</td></tr>
    <tr><td>7. Ações no objetivo</td><td><b>backup offline</b>, criptografia dos dados, detecção de exfiltração, planos de resposta a incidentes</td></tr>
  </table></div>
  <p>Os modelos de ação defensiva costumam falar em seis verbos: <b>detectar, negar, interromper, degradar, enganar e conter</b>. Cada defesa da tabela cai em um deles, e uma defesa madura combina vários, em várias etapas.</p>
  <div class="nota lembra"><span class="lbl">Limites do modelo, e o que veio depois</span>A Kill Chain é linear e foi pensada para ataques vindos de fora. Ela descreve mal ameaças internas e ataques em que o atacante repete etapas dentro da rede. O <b>MITRE ATT&amp;CK</b> é um catálogo mais fino e atual de <b>táticas e técnicas</b> reais, e é hoje a referência mais usada em equipes de defesa. As duas se complementam: a Kill Chain dá a visão geral, o ATT&amp;CK o detalhe.</div>
  <div class="nota exemplo"><span class="lbl">Como usar ao estudar um caso real</span>Para analisar qualquer incidente: (1) leia a linha do tempo de fontes confiáveis; (2) <b>encaixe cada fato</b> na etapa correspondente; (3) onde o fato não existir, anote que ainda não se sabe; (4) para cada etapa, pergunte <b>que controle teria interrompido</b> e se existia. A tabela acima é o ponto de partida.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">3</span>Fechamento da apostila</h2>
  ''' + resumo([
    "<b>Kill Chain</b> (Lockheed Martin, 2011): <b>reconhecimento, armamento, entrega, exploração, instalação, comando e controle, ações no objetivo</b>.",
    "Interromper <b>qualquer etapa</b> quebra a cadeia: quanto mais cedo, melhor.",
    "Mapear defesas por etapa mostra <b>onde faltam controles</b>.",
    "Verbos de defesa: detectar, negar, interromper, degradar, enganar, conter.",
    "<b>ATT&amp;CK</b> detalha táticas e técnicas; complementa a Kill Chain."]) + '''
  <h3>Teste rápido</h3>
  <div class="card sorter rv" data-demo="sorter" data-opts="rec:Reconhecimento|ent:Entrega|exp:Exploração|c2:Comando e controle|obj:Ações no objetivo">
    <div class="item" data-ans="rec"><p>O atacante vasculha as redes sociais para descobrir quem trabalha no financeiro.</p><span class="why">Reconhecimento: pesquisa sobre o alvo, antes de qualquer contato.</span></div>
    <div class="item" data-ans="ent"><p>Chega à vítima um e-mail com um anexo malicioso.</p><span class="why">Entrega: o atacante faz a arma chegar ao alvo.</span></div>
    <div class="item" data-ans="exp"><p>A vítima habilita a macro e o código malicioso passa a rodar.</p><span class="why">Exploração: a arma dispara, aproveitando uma falha (aqui, humana e de configuração).</span></div>
    <div class="item" data-ans="c2"><p>O computador infectado começa a consultar um domínio estranho a cada minuto para receber ordens.</p><span class="why">Comando e controle: o canal de comunicação com o atacante.</span></div>
    <div class="item" data-ans="obj"><p>Os arquivos da empresa são criptografados e aparece um pedido de resgate.</p><span class="why">Ações no objetivo: o que o atacante queria desde o início.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  ''' + quiz(1, "a", "Por que a Kill Chain valoriza interromper o ataque cedo?", [("a","Porque, quebrada qualquer etapa, a cadeia não se completa, e as primeiras etapas custam menos para defender."),("b","Porque as etapas finais não importam."),("c","Porque só as três primeiras etapas existem.")], "Se o atacante precisa de todas as etapas, basta falhar uma. Quanto mais cedo, menos estrago e menos custo.") + quiz(2, "c", "Qual defesa atua principalmente na etapa 6 (comando e controle)?", [("a","Treinamento contra phishing."),("b","Backup offline."),("c","Inspeção do tráfego de saída, inclusive o DNS.")], "Na etapa 6 a máquina comprometida precisa 'falar' com o atacante. Controlar e inspecionar o que sai da rede pode cortar esse canal.") + flash([
    ("O que é a Cyber Kill Chain?", "Um modelo que descreve um ataque em sete etapas encadeadas, para identificar onde interrompê-lo."),
    ("O que acontece na etapa de armamento?", "O atacante prepara a arma: junta código malicioso a um vetor de entrega."),
    ("Qual o limite do modelo?", "É linear e focado em ataques externos; descreve mal ameaças internas e etapas repetidas."),
    ("O que é o MITRE ATT&CK?", "Um catálogo de táticas e técnicas de ataque reais, mais detalhado que a Kill Chain.")]) + '''
  <div class="ponte rv"><div class="t">E agora?</div><div class="q">Você percorreu o caminho do dado e o do ataque.</div><p>Volte à <a href="index.html">visão geral</a> e refaça os testes sem olhar. E leve a mesma lente para a nuvem, na apostila de AWS, onde parte da defesa passa a ser responsabilidade do provedor.</p></div>
</section>'''
if PUBLICAR_KILL_CHAIN:
    chapter(PASTA, 7, "kill-chain", T, "A cadeia do ataque (Kill Chain)", "Capítulo 7 · Complemento",
            "Olhar um ataque inteiro como sequência de etapas e saber onde cada defesa o interrompe.",
            ["<b>~35 min</b>", "1 jogo · 2 testes · 4 flashcards", "complemento, não foi dado em aula"], body7, scripts=S)
print("cy caps 6-7 ok")
