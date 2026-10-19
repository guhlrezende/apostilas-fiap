import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
PASTA = "cloud-aws"
T = "Cloud e AWS"
S = ["demos/cloud.js"]
S_SQL = ["demos/cloud.js"]

# ---------------- CAP 3 ----------------
body3 = recap("No Capítulo 2 você viu quem pode fazer o quê (IAM) e de quem é cada responsabilidade. Agora o cenário concreto: uma startup tem várias pessoas que precisam acessar a mesma máquina, e quer hospedar um <b>site institucional</b> na nuvem. Três problemas: máquinas <b>Linux</b>, o <b>site</b>, e máquinas <b>Windows</b>. A resposta para os três é o mesmo serviço: o EC2.") + '''
<section class="sec" id="ec2">
  <h2><span class="sn">1</span>EC2: o computador por hora</h2>
  <p class="gancho">Uma máquina inteira, sem comprar nada.</p>
  <p>O <b>EC2</b> (<i>Elastic Compute Cloud</i>) fornece a infraestrutura computacional: processador, memória, armazenamento, rede e sistema operacional. Ele cria <b>máquinas virtuais</b>, chamadas na AWS de <b>instâncias</b>. A AWS gerencia os <b>hosts físicos</b>; você enxerga e administra só a instância (sistema operacional e aplicação). Dá para rodar várias instâncias ao mesmo tempo, isoladas entre si, na mesma infraestrutura.</p>
  <p>Toda instância nasce de uma <b>AMI</b> (<i>Amazon Machine Image</i>): uma imagem pronta que funciona como molde. <b>A instância é uma cópia em execução da AMI</b>, e dá para criar várias instâncias idênticas a partir da mesma imagem.</p>
  <h3>Famílias e tipos</h3>
  <div class="tablewrap"><table>
    <tr><th>Família</th><th>Uso típico</th></tr>
    <tr><td><b>Propósito geral</b> (T, M)</td><td>sites de baixo tráfego, bancos pequenos ou médios</td></tr>
    <tr><td><b>Otimizada para processamento</b> (C)</td><td>sites de alta performance, processamento de vídeo</td></tr>
    <tr><td><b>Otimizada para memória</b> (R, X)</td><td>bancos em memória (como o Redis)</td></tr>
    <tr><td><b>Otimizada para armazenamento</b> (I, D)</td><td>data warehousing, logs</td></tr>
    <tr><td><b>Computação acelerada</b> (P, G)</td><td>machine learning, gráficos 3D (GPU)</td></tr>
  </table></div>
  <p>O nome é um código. Digite um e veja cada parte decodificada:</p>
  <div class="demo" data-demo="instancia"></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">A instância precisa de endereço para o site ser acessado. Qual IP usar?</div><p>Há três, e escolher errado quebra o seu site no primeiro reinício.</p></div>
</section>

<section class="sec" id="ips">
  <h2><span class="sn">2</span>Os três IPs e o disco</h2>
  <p class="gancho">O IP público muda quando a máquina reinicia.</p>
  <div class="tablewrap"><table>
    <tr><th>Tipo</th><th>Características</th></tr>
    <tr><td><b>IP público</b></td><td>atribuído dinamicamente; <b>muda a cada reinício</b>; costumava ser gratuito, mas hoje a AWS cobra por hora todo endereço IPv4 público (confira a página de preços da VPC) da instância; não pode ser movido entre instâncias</td></tr>
    <tr><td><b>IP privado</b></td><td>usado nas sub-redes internas da VPC; <b>mantido</b> mesmo com o reinício</td></tr>
    <tr><td><b>IP elástico</b></td><td><b>fixo</b>; tem cobrança por hora (como os demais IPv4 públicos); <b>pode ser movido</b> entre instâncias</td></tr>
  </table></div>
  <p>Quem aponta um domínio para o IP público quebra o site a cada reinício. O IP elástico resolve isso, ao custo de pagar por ele. E o <b>disco</b>? O <b>EBS</b> (<i>Elastic Block Store</i>) é o volume de armazenamento da VM, como o <code>C:</code> ou <code>/dev/sda1</code>: dá para anexar mais espaço a uma instância existente, e ele <b>persiste</b> mesmo se a instância for parada. Já instâncias com "armazenamento local" (como as <code>c6gd</code>, com SSD NVMe) têm um disco muito rápido que <b>não sobrevive</b> à parada da instância (complemento).</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Vamos pôr o site no ar. Qual o passo a passo?</div><p>Linux, Apache e três regras de firewall.</p></div>
</section>

<section class="sec" id="linux">
  <h2><span class="sn">3</span>Exercício: um site em uma VM Linux</h2>
  <p class="gancho">Do clique em "Launch" ao navegador mostrando a página.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Criar a instância</b><p>Escolha a AMI (Amazon Linux), o tipo (uma instância pequena; as pequenas costumam aparecer em laboratórios, mas o tipo aceito no nível gratuito muda, confira o vigente) e gere o <b>par de chaves</b>: baixe a chave <b>privada</b>, necessária para o SSH.</p></div>
      <div class="st"><b>2. Liberar as portas no Security Group</b><p><b>SSH</b> (porta 22) para administrar pelo terminal; <b>HTTP</b> (80) e <b>HTTPS</b> (443) para o site ser acessado. O Security Group é o <b>firewall da instância</b>.</p></div>
      <div class="st"><b>3. Conectar por SSH</b><p>Com a chave privada, abra o terminal da instância.</p></div>
      <div class="st"><b>4. Instalar e iniciar o Apache</b><p>Comandos abaixo. <code>start</code> liga <b>agora</b>; <code>enable</code> liga <b>a cada boot</b>.</p></div>
      <div class="st"><b>5. Escrever a página</b><p>Edite <code>/var/www/html/index.html</code>.</p></div>
      <div class="st"><b>6. Abrir o IP público</b><p>Digite o IP público da instância no navegador. O site aparece.</p></div>
      <div class="st"><b>7. Encerrar a instância</b><p><b>Terminate instance</b> ao terminar, para não continuar gastando crédito.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
<pre><code><span class="c"># atualizar a lista de pacotes (yum é o gerenciador do Amazon Linux)</span>
<span class="f">sudo</span> yum update

<span class="c"># instalar o servidor web Apache (o pacote se chama httpd); -y confirma sozinho</span>
<span class="f">sudo</span> yum install httpd -y

<span class="c"># iniciar agora, e iniciar sempre que a máquina ligar</span>
<span class="f">sudo</span> systemctl start httpd
<span class="f">sudo</span> systemctl enable httpd        <span class="c"># (atalho: sudo systemctl enable --now httpd)</span>

<span class="f">sudo</span> vim /var/www/html/index.html  <span class="c"># a página inicial do site</span></code></pre>
  <div class="nota lembra"><span class="lbl">start x enable</span>O <code>start</code> liga o serviço só nesta sessão: se a instância reiniciar, o Apache não volta sozinho. O <code>enable</code> não liga nada agora; apenas marca para <b>iniciar no próximo boot</b>. Por isso se usam os dois.</div>
  <h3>E uma VM Windows?</h3>
  <p>O fluxo é parecido, mas o acesso remoto é por <b>RDP</b> (<i>Remote Desktop Protocol</i>, porta <b>3389</b>), e não por SSH. A chave gerada na criação serve para <b>decifrar a senha de administrador</b> que a AWS gera; depois, conecta-se com o cliente de Área de Trabalho Remota.</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: porta aberta é porta de entrada</span>Liberar o SSH (22) ou o RDP (3389) para <code>0.0.0.0/0</code> deixa a administração da máquina exposta à internet inteira. Em uso real, limite a origem ao seu IP. (Capítulo 7.)</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>EC2</b>: máquinas virtuais (instâncias) criadas a partir de uma <b>AMI</b>. A AWS gerencia o hardware; você, a instância.",
    "Famílias: propósito geral (T, M), processamento (C), memória (R, X), armazenamento (I, D), acelerada (P, G).",
    "<b>IP público</b> muda a cada reinício; <b>privado</b> permanece; <b>elástico</b> é fixo, pago e movível.",
    "<b>EBS</b> é o disco da VM e persiste. Armazenamento local (NVMe) é muito rápido, mas não sobrevive à parada.",
    "Linux: SSH (22), HTTP (80), HTTPS (443). Windows: RDP (3389). O <b>Security Group</b> é o firewall.",
    "<code>start</code> liga agora; <code>enable</code> liga no boot. <b>Termine</b> a instância ao acabar."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que apontar um domínio para o IP público de uma instância é arriscado?", [("a","Porque o IP público é sempre bloqueado pela AWS."),("b","Porque ele muda quando a instância reinicia, e o domínio passa a apontar para o lugar errado."),("c","Porque o IP público não funciona com HTTP.")], "O IP público é dinâmico. Para endereço fixo, use o IP elástico.") + quiz(2, "c", "Qual porta libera o acesso remoto a uma VM Windows?", [("a","22 (SSH)."),("b","80 (HTTP)."),("c","3389 (RDP).")], "No Linux o acesso administrativo é por SSH. No Windows, por RDP.") + quiz(3, "a", "O que faz <code>systemctl enable httpd</code>?", [("a","Marca o Apache para iniciar automaticamente nos próximos boots, sem iniciá-lo agora."),("b","Inicia o Apache imediatamente."),("c","Instala o Apache.")], "Para ligar agora é o <code>start</code>. Os dois resolvem problemas diferentes: o 'agora' e o 'depois de reiniciar'.") + flash([
    ("O que é uma AMI?", "Uma imagem pré-definida que serve de molde: a instância é uma cópia em execução dela."),
    ("O que é um Security Group?", "O firewall da instância: define quais portas e origens podem entrar."),
    ("IP elástico em uma frase?", "IP fixo (cobrado por hora) que pode ser movido entre instâncias."),
    ("EBS?", "Volume de armazenamento em blocos de uma VM, equivalente ao disco, que persiste.")]) + ponte("Uma máquina ligada o dia inteiro só para servir um HTML. Dá para pagar menos?", "Dá: o S3 serve o site sem nenhuma máquina.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "ec2", T, "EC2: máquinas virtuais", "Capítulo 3 · Aula 3",
        "Criar uma máquina na nuvem, entender os três IPs e pôr um site no ar com Apache.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "decodificador de instâncias"], body3, scripts=S)

# ---------------- CAP 4 ----------------
body4 = recap("No Capítulo 3 o site rodou numa instância EC2 com Apache, ligada 24 horas por dia, só para entregar arquivos HTML. Duas perguntas aparecem: <i>será que precisamos pagar uma máquina ligada só para isso?</i> E <i>como compartilhar arquivos entre equipes</i>, por exemplo, para treinar modelos de machine learning?") + '''
<section class="sec" id="s3">
  <h2><span class="sn">1</span>S3: objetos, não máquinas</h2>
  <p class="gancho">Aqui não existe sistema operacional para cuidar.</p>
  <p>O <b>S3</b> (<i>Simple Storage Service</i>) é um serviço de <b>armazenamento de objetos</b>. Dois conceitos:</p>
  <ul>
    <li><b>Bucket</b>: o contêiner dos objetos. O nome precisa ser <b>globalmente único</b> em toda a AWS (não só na sua conta).</li>
    <li><b>Objeto</b>: um par chave-valor: qualquer arquivo (HTML, imagem, CSV, JSON), endereçado por uma <b>chave</b> (o "caminho" no bucket). Cada objeto tem uma <b>URL única</b>: <code>https://nome-do-bucket.s3.regiao.amazonaws.com/arquivo</code>.</li>
  </ul>
  <div class="nota cuidado"><span class="lbl">Limitação</span>Não existe edição parcial de um objeto. Para mudar uma linha de um CSV, é preciso <b>substituir o objeto inteiro</b>. (Complemento: o <i>versionamento</i> do S3 guarda as versões anteriores, o que evita perder o arquivo antigo ao substituir.)</div>
  <div class="tablewrap"><table>
    <tr><th></th><th>EC2</th><th>S3</th></tr>
    <tr><td><b>O que é</b></td><td>máquina virtual</td><td>armazenamento de objetos</td></tr>
    <tr><td><b>Sistema operacional</b></td><td>você gerencia</td><td>não existe</td></tr>
    <tr><td><b>Servidor web</b></td><td>você instala e configura</td><td>o próprio S3 serve o site estático</td></tr>
    <tr><td><b>Quem configura a infraestrutura</b></td><td>você</td><td>a AWS</td></tr>
    <tr><td><b>Ideal para</b></td><td>aplicações que executam código</td><td>arquivos e conteúdo estático</td></tr>
  </table></div>
  <p>O ponto central da aula é uma <mark class="hl">mudança de modelo mental</mark>: dá para publicar um site estático <b>sem nenhuma máquina virtual</b>. O "servidor" é o próprio serviço de armazenamento. <i>Complemento:</i> para o bucket se comportar como site, com um documento padrão (como o <code>index.html</code>), ainda se ativa o recurso de hospedagem de site estático; sem ele, a URL do objeto abre o arquivo, mas não funciona como site.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Subi o arquivo e a URL deu AccessDenied. O que faltou?</div><p>Duas camadas de proteção, e é preciso entender as duas.</p></div>
</section>

<section class="sec" id="publico">
  <h2><span class="sn">2</span>Publicar um site: as duas camadas</h2>
  <p class="gancho">Destravar a porta não é abrir a porta.</p>
  <ol>
    <li><b>Criar o bucket</b>: escolha a região e um nome único.</li>
    <li><b>Desbloquear o acesso público</b>: por padrão a AWS <b>bloqueia todo acesso público</b> de um bucket novo, como proteção contra exposição acidental. Você desmarca e confirma que sabe do risco.</li>
    <li><b>Fazer o upload</b> do <code>index.html</code>.</li>
    <li><b>Testar a URL</b>: ainda dá <code>AccessDenied</code>!</li>
    <li><b>Editar a política do bucket</b> com um JSON que autoriza a leitura pública dos objetos.</li>
    <li><b>Testar de novo</b>: agora o site abre.</li>
  </ol>
<pre><code>{
  <span class="s">"Version"</span>: <span class="s">"2012-10-17"</span>,
  <span class="s">"Statement"</span>: [{
    <span class="s">"Principal"</span>: {<span class="s">"AWS"</span>: <span class="s">"*"</span>},               <span class="c">// qualquer pessoa</span>
    <span class="s">"Effect"</span>: <span class="s">"Allow"</span>,
    <span class="s">"Action"</span>: [<span class="s">"s3:GetObject"</span>],         <span class="c">// só ler objetos</span>
    <span class="s">"Resource"</span>: [<span class="s">"arn:aws:s3:::meu-bucket/*"</span>]  <span class="c">// todos os objetos do bucket</span>
  }]
}</code></pre>
  <p>Por que o passo 5 é necessário, se o 2 já "liberou"? Porque desbloquear <b>só remove uma trava</b> que impediria políticas públicas de funcionar. <b>Não concede acesso.</b> São duas camadas independentes: uma destrava a porta, a outra a abre. Combine as duas e veja o resultado:</p>
  <div class="demo" data-demo="s3acesso"></div>
  <div class="nota lembra"><span class="lbl">A mesma sintaxe do IAM</span>A política do bucket usa o <code>Effect</code>/<code>Action</code>/<code>Resource</code> do Capítulo 2. Aqui ela é <b>baseada em recurso</b> (está colada no próprio bucket) e tem um <code>Principal</code> dizendo <i>quem</i>.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Quanto isso custa? E como se compara a EBS e EFS?</div><p>Cobrança, e uma tabela de três armazenamentos.</p></div>
</section>

<section class="sec" id="comparar">
  <h2><span class="sn">3</span>Cobrança e EBS x EFS x S3</h2>
  <p class="gancho">Três armazenamentos que não são concorrentes.</p>
  <p><b>Cobrança do S3:</b> paga-se pelo <b>GB armazenado por mês</b>, pela transferência <b>para fora</b> da AWS e pelas solicitações (<code>PUT</code>, <code>COPY</code>, <code>POST</code>, <code>LIST</code>, <code>GET</code>). <b>Não</b> se paga por transferências <i>dentro</i> do S3, nem do S3 para o CloudFront ou para uma EC2 <b>na mesma região</b>. É um modelo parecido com o do Google Drive: você paga pelo espaço usado, não por uma máquina rodando.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>EBS</th><th>EFS</th><th>S3</th></tr>
    <tr><td><b>Natureza</b></td><td>volume em <b>blocos</b> (HDD/SSD)</td><td><b>sistema de arquivos</b> compartilhado (NFS)</td><td>armazenamento de <b>objetos</b></td></tr>
    <tr><td><b>Anexado a</b></td><td>uma instância por vez</td><td><b>várias</b> instâncias ao mesmo tempo</td><td>nenhuma: acesso por API/URL</td></tr>
    <tr><td><b>Exemplo</b></td><td>o <code>C:</code> da VM</td><td>pasta de rede compartilhada</td><td>backups, imagens, CSVs, HTML</td></tr>
    <tr><td><b>Bom para</b></td><td>disco do SO de uma instância</td><td>servidores editando os <b>mesmos arquivos</b> juntos (só Linux)</td><td>sites estáticos, dados de ML, backups</td></tr>
  </table></div>
  <p>Resposta à segunda pergunta do cenário: para <b>distribuir</b> um conjunto de dados de treino entre equipes, o <b>S3</b>. Para várias instâncias <b>editarem</b> os mesmos arquivos ao mesmo tempo, o <b>EFS</b>.</p>
  <div class="nota exemplo"><span class="lbl">Complemento: CloudFront</span>Para sites com visitantes no mundo todo, costuma-se colocar o <b>CloudFront</b> (uma CDN, rede de distribuição de conteúdo) na frente do bucket: ele guarda cópias perto dos usuários, reduzindo a latência, e permite HTTPS com um domínio próprio.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>S3</b> guarda <b>objetos</b> em <b>buckets</b> (nome único global). Sem SO, sem servidor para cuidar.",
    "Não há edição parcial: substitui-se o objeto inteiro.",
    "Site estático no S3: <b>desbloquear</b> o acesso público <b>e</b> ter uma <b>política do bucket</b> que autorize <code>s3:GetObject</code>. São duas camadas.",
    "Cobrança: GB armazenado, tráfego <b>para fora</b> e solicitações. Dentro da mesma região, para EC2 ou CloudFront, não.",
    "<b>EBS</b>: disco de uma instância. <b>EFS</b>: arquivos compartilhados (Linux). <b>S3</b>: objetos, por URL."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Você desmarcou o bloqueio de acesso público e o site ainda dá AccessDenied. O que falta?", [("a","Reiniciar o bucket."),("b","Trocar a região."),("c","Uma política do bucket que autorize s3:GetObject para os visitantes.")], "Desbloquear só remove a trava. A autorização vem da política do bucket.") + quiz(2, "a", "Qual serviço escolher para várias instâncias EC2 Linux editarem os mesmos arquivos ao mesmo tempo?", [("a","EFS."),("b","EBS."),("c","S3.")], "O EBS é anexado a uma instância por vez, e o S3 não é um sistema de arquivos montável. O EFS é o sistema de arquivos compartilhado.") + quiz(3, "b", "Qual a grande vantagem do S3 sobre uma EC2 para um site estático?", [("a","Ele roda código Python."),("b","Não há máquina ligada para administrar nem para pagar enquanto espera."),("c","Ele usa menos portas.")], "O S3 serve os arquivos direto. Para executar código no servidor (aplicações dinâmicas), a EC2 continua sendo necessária.") + flash([
    ("O que é um bucket?", "O contêiner de objetos do S3, com nome único em toda a AWS."),
    ("O que é um objeto?", "Um arquivo (par chave-valor) guardado em um bucket, com URL própria."),
    ("S3 serve site dinâmico?", "Não: só conteúdo estático. Para código no servidor, EC2 ou Lambda."),
    ("Quando o S3 não cobra transferência?", "Dentro do S3, e do S3 para CloudFront ou EC2 na mesma região.")]) + ponte("Guardo arquivos sem servidor. E o banco de dados, precisa mesmo de uma máquina?", "Não: o RDS entrega o banco já gerenciado.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "s3", T, "S3: arquivos sem servidor", "Capítulo 4 · Aula 4",
        "Guardar e servir arquivos sem nenhuma máquina, e entender por que o acesso tem duas camadas.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "simulador de acesso"], body4, scripts=S)

# ---------------- CAP 5 ----------------
body5 = recap("No Capítulo 4 o S3 resolveu os arquivos sem servidor. A startup também precisa guardar dados num <b>banco relacional</b>, com segurança. Instalar e manter o banco numa EC2 sai caro e dá trabalho. Duas perguntas: como criar um banco na nuvem <b>sem administrar servidor</b>, e como permitir o <b>acesso remoto</b>?") + '''
<section class="sec" id="rds">
  <h2><span class="sn">1</span>RDS: o banco sem o servidor</h2>
  <p class="gancho">Você usa o banco. A AWS cuida do resto.</p>
  <p>O <b>RDS</b> (<i>Relational Database Service</i>) é um serviço <b>gerenciado</b> de bancos relacionais (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server). "Gerenciado" quer dizer que a AWS cuida da instalação, dos <b>patches</b>, dos <b>backups</b> e da infraestrutura. Por baixo, ele roda sobre uma instância EC2, mas você <b>não acessa essa máquina</b>: não há SSH nem sistema operacional.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>Banco dentro de uma EC2</th><th>RDS</th></tr>
    <tr><td><b>Quem instala e atualiza</b></td><td>você</td><td>a AWS</td></tr>
    <tr><td><b>Acesso ao sistema operacional</b></td><td>sim (SSH)</td><td>não</td></tr>
    <tr><td><b>Backup</b></td><td>você configura</td><td>automático</td></tr>
    <tr><td><b>Como se conecta</b></td><td>IP da instância</td><td><b>endpoint</b> fornecido pelo RDS</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">A evolução da disciplina</span>EC2 (servidor que você administra) → S3 (arquivos sem servidor) → RDS (banco sem servidor para administrar) → Lambda (código sem servidor, Capítulo 6). A cada degrau, menos coisa para você cuidar.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Como é criar um e se conectar a ele de casa?</div><p>Doze passos, e uma armadilha parecida com a do S3.</p></div>
</section>

<section class="sec" id="passos">
  <h2><span class="sn">2</span>Criar e conectar: duas camadas de novo</h2>
  <p class="gancho">"Acesso público" não abre a porta.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1 a 3. Criar a instância</b><p>RDS → Criar banco → mecanismo <b>MySQL</b>, modelo de <b>nível gratuito</b> (para não gerar custo), identificador (como <code>db-instancia-xx-aws</code>) e senha do administrador. <b>Guarde a senha</b>: ela não aparece de novo.</p></div>
      <div class="st"><b>4. Acesso público: Sim</b><p>Sem isso, o banco só é alcançável de <b>dentro da VPC</b>, e o seu computador não chega nele.</p></div>
      <div class="st"><b>5 a 7. Security Group e nome do banco</b><p>Use o Security Group padrão e, em "Configuração adicional", já crie a base inicial (no exercício, <code>dbalpha</code>).</p></div>
      <div class="st"><b>8. Copiar o endpoint</b><p>Com a instância "Disponível", copie o <b>endpoint</b>: é o "endereço" do banco, no lugar de um IP.</p></div>
      <div class="st"><b>9. Liberar a porta 3306</b><p>No Security Group, uma regra de <b>entrada TCP na porta 3306</b> (a do MySQL). Sem ela, o cliente fica tentando e dá <i>timeout</i>.</p></div>
      <div class="st"><b>10 e 11. Conectar e criar a tabela</b><p>No MySQL Workbench: nova conexão com o <b>endpoint</b>, porta 3306, usuário e senha. Depois crie a tabela direto na base remota.</p></div>
      <div class="st"><b>12. Excluir a instância</b><p>Ao terminar: RDS → selecionar → Ações → <b>Excluir</b>. Instância ligada <b>consome crédito</b> do laboratório, igual à EC2.</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <p>Combine as duas camadas e veja quando a conexão funciona:</p>
  <div class="demo" data-demo="rdsacesso"></div>
  <div class="nota erro"><span class="lbl">Cuidado: o que o slide faz por didática</span>Liberar a 3306 para <code>0.0.0.0/0</code> expõe o banco à internet inteira, e qualquer robô pode tentar adivinhar a senha. Em produção, a origem deve ser <b>só o seu IP</b> (a opção "Meu IP" do console) ou <b>só as instâncias da aplicação</b>, e o banco nem deveria ter acesso público. É o risco de portas expostas da apostila de Cibersegurança.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E a tabela do exercício? Como ela é?</div><p>Experimente aqui mesmo.</p></div>
</section>

<section class="sec" id="exercicio">
  <h2><span class="sn">3</span>O exercício: a tabela projetos</h2>
  <p class="gancho">O mesmo DDL da apostila de Bancos de Dados, agora numa base de nuvem.</p>
  <p>O exercício pede a base <code>dbalpha</code> e a tabela <code>projetos</code> com <code>idProjeto</code>, <code>sigla</code>, <code>dtInicio</code> e <code>dtTermino</code>, e alguns registros. Uma solução (em SQLite aqui; no MySQL do RDS o <code>idProjeto</code> seria <code>INT AUTO_INCREMENT PRIMARY KEY</code>):</p>
''' + sqlbox("vazia", """CREATE TABLE projetos (
  idProjeto INTEGER PRIMARY KEY AUTOINCREMENT,
  sigla     VARCHAR(10) NOT NULL UNIQUE,
  dtInicio  DATE NOT NULL,
  dtTermino DATE,
  CHECK (dtTermino IS NULL OR dtTermino >= dtInicio)
);
INSERT INTO projetos (sigla, dtInicio, dtTermino) VALUES
  ('NEXA',  '2026-08-01', '2026-12-15'),
  ('ALFA', '2026-09-01', NULL),
  ('IRIS',  '2026-09-10', '2026-09-25');
SELECT * FROM projetos;""", "Criar e consultar a tabela", expect=3) + '''
  <p>Note como as restrições do Capítulo 3 de Bancos de Dados fazem trabalho aqui: <code>UNIQUE</code> na sigla e um <code>CHECK</code> que impede um término anterior ao início.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>RDS</b>: banco relacional <b>gerenciado</b> (patches, backups, infraestrutura). Sem SSH nem SO.",
    "Conexão pelo <b>endpoint</b>, e não por IP.",
    "Para conectar de fora: <b>acesso público</b> <b>e</b> regra de entrada <b>TCP 3306</b> no Security Group. Duas camadas.",
    "<code>0.0.0.0/0</code> na porta do banco só em laboratório. Em produção, só seu IP ou só a aplicação.",
    "<b>Exclua</b> a instância ao terminar: ela consome crédito ligada."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Seu cliente de banco fica tentando e termina em timeout, apesar de o acesso público estar 'Sim'. Qual a causa mais provável?", [("a","O endpoint está errado."),("b","Falta a regra de entrada na porta 3306 no Security Group."),("c","O banco não existe.")], "Acesso público dá um endereço alcançável, mas quem libera a passagem é o Security Group. Sem a regra, o pacote é descartado em silêncio.") + quiz(2, "a", "O que o RDS faz por você que uma EC2 com MySQL instalado não faz?", [("a","Cuida de patches e backups, e esconde o sistema operacional."),("b","Deixa o banco mais rápido sempre."),("c","Dispensa Security Group.")], "Esse é o sentido de 'gerenciado': você usa o banco, e a AWS administra a infraestrutura.") + quiz(3, "c", "Por que não se deve liberar a 3306 para 0.0.0.0/0 em produção?", [("a","Porque a porta não funciona assim."),("b","Porque deixa o banco mais lento."),("c","Porque expõe o banco à internet inteira, e qualquer robô pode tentar adivinhar a senha.")], "O correto é restringir a origem ao seu IP ou às instâncias da aplicação.") + flash([
    ("O que é um endpoint?", "O endereço de rede do banco no RDS, usado no lugar de um IP."),
    ("Por que excluir a instância?", "Porque instância ligada consome crédito, mesmo sem uso."),
    ("RDS x banco numa EC2?", "No RDS a AWS administra instalação, patches e backups, e você não acessa o SO."),
    ("Qual a porta padrão do MySQL?", "3306.")]) + ponte("Tenho arquivos no S3 e um banco no RDS. Quem leva os dados de um para o outro?", "Uma função Lambda, disparada pelo próprio S3.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "rds", T, "RDS: banco gerenciado", "Capítulo 5 · Aula 5",
        "Um banco MySQL na nuvem sem servidor para administrar, e por que abrir a porta ao mundo é um risco.",
        ["<b>~40 min</b>", "2 demos · 3 testes · 4 flashcards", "SQL executável"], body5, scripts=S, sql=True)
print("aws caps 3-5 ok")
