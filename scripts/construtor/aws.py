import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *

PASTA = "cloud-aws"
TITULO = "Cloud e AWS"
T = "Cloud e AWS"
S = ["demos/cloud.js"]
CAPS = [
 dict(n=1, file="cap-1-o-que-e-nuvem.html", titulo="O que é nuvem", aula="Aula 1", tempo=35,
      resumo="IaaS, PaaS e SaaS, modelos de infraestrutura, TCO, regiões e zonas de disponibilidade e formas de cobrança.",
      pergunta="Colocar coisas na nuvem é fácil. Como saber quem pode mexer, e de quem é a responsabilidade de proteger?"),
 dict(n=2, file="cap-2-seguranca-e-iam.html", titulo="Segurança e IAM", aula="Aula 2", tempo=40,
      resumo="Responsabilidade compartilhada, usuários, grupos, políticas e roles, e o Deny que sempre vence.",
      pergunta="Já sei quem pode o quê. Como crio de fato uma máquina e a conecto?"),
 dict(n=3, file="cap-3-ec2.html", titulo="EC2: máquinas virtuais", aula="Aula 3", tempo=40,
      resumo="Instâncias, AMI, tipos, os três IPs, EBS e o passo a passo de subir um site com Apache.",
      pergunta="Uma máquina ligada o dia inteiro só para servir um HTML. Dá para pagar menos?"),
 dict(n=4, file="cap-4-s3.html", titulo="S3: arquivos sem servidor", aula="Aula 4", tempo=40,
      resumo="Buckets e objetos, site estático sem máquina virtual, as duas camadas de acesso e EBS x EFS x S3.",
      pergunta="Guardo arquivos sem servidor. E o banco de dados, precisa mesmo de uma máquina?"),
 dict(n=5, file="cap-5-rds.html", titulo="RDS: banco gerenciado", aula="Aula 5", tempo=40,
      resumo="MySQL na nuvem sem administrar servidor, endpoint, Security Group e o risco de abrir a porta ao mundo.",
      pergunta="Tenho arquivos no S3 e um banco no RDS. Quem leva os dados de um para o outro?"),
 dict(n=6, file="cap-6-lambda.html", titulo="Lambda: código sob demanda", aula="Aula 6", tempo=45,
      resumo="Funções serverless, limites, e o fluxo completo CSV no S3, Lambda e inserção no RDS.",
      pergunta="Os serviços funcionam juntos. Como eles se conectam por baixo, e como não gastar o que não devo?"),
 dict(n=7, file="cap-7-rede-e-boas-praticas.html", titulo="Rede, custos e boas práticas (complemento)", aula="Complemento", tempo=40,
      resumo="VPC, sub-redes, Security Group x NACL, os pilares de uma boa arquitetura, CLI e boto3, e como evitar custo surpresa.",
      pergunta=""),
]

if __name__ == "__main__" or True:
    manifest(PASTA, "cloud-aws", TITULO, CAPS)
    hub(PASTA, TITULO, "Plataformas, Serviços Cognitivos e Cloud Computing", "Apostila de Cloud e AWS",
        "Do que é nuvem até um fluxo completo com arquivo no S3, função Lambda e banco no RDS. Com simuladores para ver cada regra de acesso funcionando.",
        ["<b>7</b> capítulos", "<b>~4h40</b> de estudo ativo", "simuladores de permissão e de fluxo"],
        '<p>A disciplina anda em <mark class="hl">degraus</mark>: primeiro você aluga uma máquina (EC2), depois descobre que dá para guardar arquivos sem máquina (S3), depois um banco sem máquina (RDS) e por fim código sem máquina (Lambda). No fim, os quatro trabalham juntos. Cada capítulo mostra o que o anterior custava de trabalho, e como o próximo tira esse trabalho de você.</p>',
        'Os conceitos valem para qualquer nuvem; os nomes e telas são da <b>AWS</b>. <b>Preços, limites e regras do nível gratuito mudam</b>: aqui só aparecem ordens de grandeza e o que foi dito em aula. Confira sempre a página oficial antes de decidir algo que envolva dinheiro.')

# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo. Você não precisa saber nada de nuvem: basta já ter usado um serviço online, como um drive. Daqui em diante, cada capítulo abre lembrando o que ficou em aberto no anterior.", "Ponto de partida") + '''
<section class="sec" id="definicao">
  <h2><span class="sn">1</span>O que é computação em nuvem</h2>
  <p class="gancho">A nuvem é o computador de outra pessoa. Com contrato.</p>
  <p>Computação em nuvem é a entrega <b>sob demanda</b> de poder computacional, armazenamento, aplicativos e outros recursos de TI <b>pela internet</b>, com preço <mark class="hl">conforme o uso</mark>. Na prática, é um conjunto enorme de servidores de um provedor que disponibilizam infraestrutura (servidores, armazenamento, aplicações) para você alugar, em vez de comprar e manter os seus. Os provedores mais conhecidos: <b>AWS</b> (a pioneira), Microsoft Azure, Google Cloud, IBM Cloud e Oracle Cloud.</p>
  <p>Por que as empresas migram? Três motivos aparecem sempre: <b>custo</b> (pagar só pelo que usa), <b>agilidade</b> (um servidor em minutos, e não em semanas) e <b>segurança</b> (a infraestrutura física fica com quem faz disso o seu negócio). Na AWS, os argumentos clássicos são disponibilidade, escalabilidade, gestão e um melhor <i>time to market</i> (chegar ao mercado mais rápido).</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">"Nuvem" cobre desde alugar uma máquina crua até usar um e-mail pronto. Qual a diferença?</div><p>Os modelos de serviço.</p></div>
</section>

<section class="sec" id="modelos">
  <h2><span class="sn">2</span>IaaS, PaaS e SaaS</h2>
  <p class="gancho">Quanto da pilha é seu?</p>
  <div class="grid3">
    <div class="card rv"><b>IaaS</b><br><small class="muted">Infraestrutura como serviço</small><p>Você aluga poder computacional, rede e armazenamento, e administra o sistema operacional para cima. Mais controle, mais responsabilidade. <i>Ex.: AWS EC2, Google Compute Engine.</i></p></div>
    <div class="card rv"><b>PaaS</b><br><small class="muted">Plataforma como serviço</small><p>O foco é implementar e gerir a <b>aplicação</b>; a nuvem gerencia o sistema operacional. <i>Ex.: AWS Elastic Beanstalk, Google App Engine.</i></p></div>
    <div class="card rv"><b>SaaS</b><br><small class="muted">Software como serviço</small><p>Você só <b>usa</b> o software, pela internet, sem controle sobre o servidor. <i>Ex.: Google Drive, Office 365.</i></p></div>
  </div>
  <div class="demo" data-demo="pilha"></div>
  <h3>E onde fica a infraestrutura?</h3>
  <div class="tablewrap"><table>
    <tr><th>Modelo</th><th>O que é</th><th>Exemplo</th></tr>
    <tr><td><b>Local</b> (<i>on-premises</i>)</td><td>infraestrutura privada, dentro da empresa</td><td>a sala de servidores</td></tr>
    <tr><td><b>Híbrido</b></td><td>parte na nuvem, parte na empresa</td><td>dados sensíveis locais, site na nuvem</td></tr>
    <tr><td><b>Nuvem</b></td><td>toda a infraestrutura na nuvem</td><td>startups costumam começar assim</td></tr>
  </table></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Se eu pago só pelo que uso, como estimo o custo? E sempre é mais barato?</div><p>Com o TCO, e com uma conta honesta.</p></div>
</section>

<section class="sec" id="custo">
  <h2><span class="sn">3</span>TCO: o custo total de verdade</h2>
  <p class="gancho">O preço da etiqueta não é o custo.</p>
  <p>O <b>TCO</b> (<i>Total Cost of Ownership</i>, custo total de propriedade) soma as despesas <b>diretas e indiretas</b>. No modelo local, o custo direto são os equipamentos, e os indiretos são energia, espaço, refrigeração, segurança física e a equipe que cuida de tudo. Na nuvem, você <b>paga somente pelo que usa</b>. Mexa nos controles e veja quando cada lado vence:</p>
  <div class="demo" data-demo="custo"></div>
  <div class="nota lembra"><span class="lbl">A lição</span>Nuvem não é "sempre mais barata". Ela vence quando o uso é <b>variável ou imprevisível</b>, ou quando você ainda não sabe quanto vai precisar (você não compra um servidor para um projeto que pode não dar certo). Para uma carga alta, constante e previsível, o servidor próprio pode compensar. Por isso a pergunta certa é "qual o TCO do <i>meu</i> caso?".</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Onde, no mundo, ficam esses servidores?</div><p>Em regiões e zonas de disponibilidade.</p></div>
</section>

<section class="sec" id="infra">
  <h2><span class="sn">4</span>Regiões e zonas de disponibilidade</h2>
  <p class="gancho">Um data center, uma zona, uma região.</p>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>Data center</b><p>O prédio com os servidores (dezenas de milhares deles, segundo o material da aula).</p></div>
      <div class="st"><b>Zona de disponibilidade (AZ)</b><p>Contém um ou mais data centers e é <b>projetada para isolar falhas</b>: energia, rede e conectividade redundantes. São nomeadas por letra: <code>us-east-1a</code>, <code>us-east-1b</code>...</p></div>
      <div class="st"><b>Região</b><p>Uma área geográfica <b>separada e independente</b>, com <b>duas ou mais AZs</b> segundo o slide (hoje a AWS fala em pelo menos três, confira) com redundância total. Exemplos: <code>us-east-1</code> (Norte da Virgínia) e <code>sa-east-1</code> (São Paulo, lançada em 2011).</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
  <p>Como escolher uma região? Três critérios:</p>
  <div class="grid3">
    <div class="card rv"><b>Compliance</b><p>Leis que dizem onde os dados do cliente podem ficar (inclusive fora do país).</p></div>
    <div class="card rv"><b>Proximidade</b><p>Região mais perto dos usuários tem <b>menor latência</b>.</p></div>
    <div class="card rv"><b>Custo</b><p>O preço varia por região, e <b>nem todo serviço existe em todas</b>.</p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado: replicar não é automático</span>Ter várias AZs não significa que seus dados estejam em todas. A <b>replicação entre AZs é ativada pelo cliente</b>. As <i>Local Zones</i> são extensões de uma região mais perto dos usuários (latência muito baixa; o slide fala em menos de 10 ms, confira o valor atual), e também precisam ser ativadas. O slide citava 39 regiões e 124 AZs, números que <b>crescem</b>: confira no site da AWS.</div>
  <h3>Como se cobra</h3>
  <div class="tablewrap"><table>
    <tr><th>Tipo</th><th>Exemplo</th><th>Cobrança</th></tr>
    <tr><td><b>Computação</b></td><td>EC2</td><td>uso de CPU e memória, por hora ou por segundo</td></tr>
    <tr><td><b>Armazenamento</b></td><td>S3</td><td>por GB guardado</td></tr>
    <tr><td><b>Tráfego de rede</b></td><td>download</td><td>por GB que <b>sai</b> da AWS; a entrada normalmente não é cobrada</td></tr>
  </table></div>
  <p>E três jeitos de pagar menos: <b>pagar pelo que usa</b>, <b>reservar</b> capacidade (paga menos por se comprometer) e a <b>economia de escala</b> (paga menos conforme a nuvem cresce).</p>
  <div class="nota exemplo"><span class="lbl">Aviso do material da disciplina</span>O acesso à AWS no curso é pelo <b>AWS Academy</b>, por convite do professor. <b>Não crie conta própria</b> para as atividades, e se alguma tela pedir <b>dados de cartão</b>, você está no lugar errado. Para quem quer fazer a trilha completa, o curso dá uma <i>badge</i> resgatável.</div>
  <h3>Três formas de acessar a AWS</h3>
  <p><b>Console</b> (a interface web), <b>CLI</b> (linha de comando) e <b>acesso programático</b> por SDKs em várias linguagens, como a biblioteca <code>boto3</code> do Python.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Nuvem</b> = recursos de TI sob demanda, pela internet, pagos conforme o uso.",
    "<b>IaaS</b> (você administra o SO), <b>PaaS</b> (foco na aplicação), <b>SaaS</b> (só usa). Quanto mais perto do SaaS, menos controle e menos trabalho.",
    "Infraestrutura: <b>local</b>, <b>híbrida</b> ou <b>nuvem</b>.",
    "<b>TCO</b> soma custos diretos e indiretos. Nuvem não é sempre mais barata: vence com uso variável.",
    "<b>Data center</b> → <b>AZ</b> (isolamento de falhas) → <b>região</b> (2 ou mais AZs). Escolha por compliance, proximidade e custo.",
    "Cobrança: computação (hora/segundo), armazenamento (GB), tráfego que <b>sai</b> (GB)."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Uma empresa usa o Google Drive para guardar documentos. Que modelo de serviço é?", [("a","IaaS."),("b","PaaS."),("c","SaaS: ela só usa o software, sem controle sobre o servidor.")], "No SaaS o provedor cuida de tudo, da infraestrutura à aplicação. IaaS seria alugar uma máquina virtual, e PaaS, uma plataforma para rodar o seu código.") + quiz(2, "b", "Por que ter várias zonas de disponibilidade melhora a resiliência?", [("a","Porque elas ficam no mesmo prédio."),("b","Porque cada uma é isolada, com energia e rede próprias, então uma falha não derruba as outras."),("c","Porque os dados são replicados sozinhos entre elas.")], "O isolamento é o ponto. Mas a replicação dos dados entre AZs é uma configuração do cliente, não é automática.") + quiz(3, "a", "Qual o critério de escolha de região ligado a 'onde a lei permite guardar os dados'?", [("a","Compliance."),("b","Proximidade."),("c","Custo.")], "Compliance é o cumprimento de regras legais e regulatórias, como as de residência de dados.") + flash([
    ("IaaS, PaaS e SaaS em uma linha cada?", "IaaS: você aluga a infraestrutura e cuida do SO. PaaS: você cuida só da aplicação. SaaS: você só usa o software."),
    ("O que é TCO?", "Custo total de propriedade: soma os custos diretos e os indiretos de uma solução."),
    ("O que é uma AZ?", "Uma zona de disponibilidade: um ou mais data centers isolados de falhas dentro de uma região."),
    ("Quais tráfegos de rede são cobrados?", "Normalmente o que sai da AWS (download). A entrada geralmente não é cobrada.")]) + ponte("Colocar coisas na nuvem é fácil. Como saber quem pode mexer, e de quem é a responsabilidade de proteger?", "Com o modelo de responsabilidade compartilhada e o serviço IAM.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "o-que-e-nuvem", T, "O que é nuvem", "Capítulo 1 · Aula 1",
        "Como funciona a computação em nuvem, quanto custa de verdade e onde ficam os servidores.",
        ["<b>~35 min</b>", "2 demos · 3 testes · 4 flashcards", "simulador de custo"], body1, scripts=S)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 você viu o que é nuvem e como ela se organiza. Agora o cenário muda: você criou uma conta e precisa <b>compartilhar</b> os recursos com colegas. Quem entra? O que pode fazer? E, se algo vazar, de quem é a culpa? A segurança na nuvem começa por essas perguntas.") + '''
<section class="sec" id="compartilhada">
  <h2><span class="sn">1</span>Responsabilidade compartilhada</h2>
  <p class="gancho">A AWS protege o prédio. Você protege o que põe dentro.</p>
  <p>A regra mental para decorar: a AWS cuida da segurança <b>DA</b> nuvem, e o cliente cuida da segurança <b>NA</b> nuvem.</p>
  <div class="grid2">
    <div class="card rv"><b style="color:var(--c0)">Responsabilidade da AWS</b><ul><li>Segurança física (acesso controlado aos data centers)</li><li>Detecção de intrusão</li><li>Isolamento entre instâncias de clientes diferentes</li><li>Hardware e virtualização</li></ul></div>
    <div class="card rv"><b style="color:var(--c1)">Responsabilidade do cliente</b><ul><li>Patches de segurança (o SO das suas instâncias)</li><li>Gestão de contas e permissões (<b>IAM</b>)</li><li>Firewall (<i>Security Group</i>) e rede (<i>VPC</i>)</li><li>Criptografia: em trânsito (<b>TLS</b>) e em repouso (<b>KMS</b>)</li><li>Seus dados e sua aplicação</li></ul></div>
  </div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Achar que "está na nuvem, então a AWS protege".</b> A maioria dos vazamentos em nuvem vem de configuração do cliente (um bucket aberto, uma porta liberada para o mundo, uma senha fraca), e não de invasão aos data centers.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">A gestão de contas é do cliente. Como se faz essa gestão na AWS?</div><p>Com o IAM.</p></div>
</section>

<section class="sec" id="iam">
  <h2><span class="sn">2</span>IAM: quem pode fazer o quê</h2>
  <p class="gancho">Autenticação diz quem você é. Autorização diz o que você pode fazer.</p>
  <p>O <b>IAM</b> (<i>Identity and Access Management</i>) é o serviço <b>gratuito</b> de identificação e controle de acesso. Ele define <b>quem</b> acessa, <b>quais recursos</b> e <b>como</b>. A regra fundamental é o <mark class="hl">privilégio mínimo</mark>: uma conta nova nasce <b>sem permissão nenhuma</b>, e tudo precisa ser concedido explicitamente.</p>
  <div class="tablewrap"><table>
    <tr><th>Objeto</th><th>O que é</th><th>Detalhe</th></tr>
    <tr><td><b>User</b> (usuário)</td><td>conta de uma pessoa ou aplicativo, com login e senha</td><td>identidade permanente</td></tr>
    <tr><td><b>Group</b> (grupo)</td><td>conjunto de usuários com a mesma autorização</td><td>facilita conceder permissões (devs, infra, admins)</td></tr>
    <tr><td><b>Policy</b> (política)</td><td>documento JSON que diz quais recursos e que nível de acesso</td><td>é o que concede ou nega de fato</td></tr>
    <tr><td><b>Role</b> (função)</td><td>conjunto de permissões que pode ser <b>assumido</b> temporariamente</td><td><b>sem login e senha</b>; serve a usuários e a <b>serviços</b></td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Ponto de prova</span>A diferença central entre <b>User</b> e <b>Role</b>: o User tem credenciais fixas; a Role não tem e é assumida temporariamente (por baixo, a AWS entrega credenciais que expiram). É por isso que uma função Lambda recebe uma role, e não uma chave de acesso escrita no código.</div>
  <h3>Anatomia de uma política</h3>
<pre><code>{
  <span class="s">"Version"</span>: <span class="s">"2012-10-17"</span>,
  <span class="s">"Statement"</span>: [
    {
      <span class="an" tabindex="0" data-t="Allow ou Deny.">"Effect"</span>: <span class="s">"Allow"</span>,
      <span class="an" tabindex="0" data-t="A operação, no formato serviço:Operação. O curinga * vale: ec2:Describe* = todas as ações de leitura do EC2.">"Action"</span>: <span class="s">"ec2:Describe*"</span>,
      <span class="an" tabindex="0" data-t="Sobre quais recursos vale. * significa todos.">"Resource"</span>: <span class="s">"*"</span>
    }
  ]
}</code></pre>
  <p>Esta política permite <b>somente leitura</b> do EC2: listar e descrever, mas não criar, parar ou destruir. Há dois tipos: políticas <b>baseadas em identidade</b> (anexadas a um usuário, grupo ou role) e <b>baseadas em recurso</b> (anexadas ao recurso, como um bucket S3, dizendo quem o acessa).</p>
  <h3>A regra de ouro: o Deny vence</h3>
  <p>Quando várias políticas se aplicam, a avaliação segue uma ordem fixa: <b>1)</b> um <b>Deny explícito</b> sempre vence; <b>2)</b> se não há Deny, um <b>Allow</b> permite; <b>3)</b> se nada casa, vale o <b>Deny implícito</b>. Anexe políticas e teste ações:</p>
  <div class="demo" data-demo="iam"></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E a conta de administrador criada junto com a conta da AWS?</div><p>O root pede cuidado especial.</p></div>
</section>

<section class="sec" id="root">
  <h2><span class="sn">3</span>Root, MFA e chaves de acesso</h2>
  <p class="gancho">A chave mestra não vai no bolso.</p>
  <ul>
    <li>O usuário <b>root</b> nasce com a conta e tem <b>acesso total</b>. Habilite o <b>MFA</b> (autenticação multifator) nele e <b>não o use no dia a dia</b>: crie contas IAM para você e para seus colegas.</li>
    <li>Dois jeitos de autenticar: <b>usuário e senha</b> para o console (gestão de recursos) e <b>chave de acesso</b> (<i>Access Key</i> e <i>Secret Key</i>) para o acesso <b>programático</b> (SDKs, CLI, <code>boto3</code>).</li>
  </ul>
  <div class="nota cuidado"><span class="lbl">Chaves de acesso são segredos</span>Nunca as coloque no código nem num repositório (lembra do Git?). Prefira <b>roles</b> sempre que um serviço da AWS precisar de acesso, e se uma chave vazar, desative-a na hora. <span class="muted">(Complemento: hoje a própria AWS recomenda o IAM Identity Center, antigo AWS SSO, em vez de usuários IAM de longa duração para pessoas.)</span></div>
  <div class="nota lembra"><span class="lbl">Laboratório do curso</span>A tarefa da aula era associar usuários a grupos (S3-Support, EC2-Support, EC2-Admin), logar com um deles e <b>conferir que só dava para fazer o que a política do grupo permitia</b> (por exemplo, apenas listar, parar e iniciar instâncias). É parecido com a demo acima, na prática (a demo usa nomes e permissões simplificados).</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "AWS cuida da segurança <b>DA</b> nuvem; o cliente, <b>NA</b> nuvem (contas, SO, firewall, criptografia, dados).",
    "<b>IAM</b>: User, Group, Policy, Role. Conta nova nasce <b>sem permissão</b> (privilégio mínimo).",
    "<b>Role</b>: sem login e senha, assumida temporariamente, vale para serviços.",
    "Política: <code>Effect</code>, <code>Action</code>, <code>Resource</code>. <b>Deny explícito vence</b> qualquer Allow; sem nada, <b>Deny implícito</b>.",
    "<b>Root</b> com MFA e fora do uso diário. <b>Chave de acesso</b> para código, <b>senha</b> para o console."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Um usuário tem uma política que permite ec2:* e outra que nega ec2:TerminateInstances. Ele consegue terminar uma instância?", [("a","Não: o Deny explícito vence o Allow."),("b","Sim: o Allow é mais amplo."),("c","Depende da ordem em que as políticas foram criadas.")], "Não há desempate por ordem nem por amplitude. Um Deny explícito que casa sempre prevalece.") + quiz(2, "c", "Por que dar uma role a uma função Lambda, em vez de colocar uma chave de acesso no código?", [("a","Porque roles são mais baratas."),("b","Porque a Lambda não aceita chaves."),("c","Porque a role não tem credencial fixa para vazar: a AWS entrega credenciais temporárias.")], "Segredo no código é risco: ele vai para o repositório e vaza. A role elimina o segredo fixo.") + quiz(3, "b", "Quem é responsável por aplicar patches de segurança no sistema operacional de uma instância EC2?", [("a","A AWS."),("b","O cliente."),("c","Ninguém: instâncias não precisam de patches.")], "Na EC2 (IaaS) o sistema operacional é do cliente. A AWS cuida do hardware e do isolamento.") + flash([
    ("Autenticação x autorização?", "Autenticação: quem é você. Autorização: o que você pode fazer."),
    ("O que é privilégio mínimo?", "Dar só as permissões necessárias. Contas novas nascem sem nenhuma."),
    ("Por que usar MFA no root?", "Porque o root tem acesso total: uma senha roubada sozinha não deve bastar."),
    ("O que é uma política baseada em recurso?", "Uma política anexada ao próprio recurso (como um bucket), que diz quem pode acessá-lo.")]) + ponte("Já sei quem pode o quê. Como crio de fato uma máquina e a conecto?", "Com o EC2.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "seguranca-e-iam", T, "Segurança e IAM", "Capítulo 2 · Aula 2",
        "Quem protege o quê na nuvem, e como o IAM decide quem pode fazer cada coisa.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "avaliador de políticas"], body2, scripts=S)
print("aws caps 1-2 ok")
