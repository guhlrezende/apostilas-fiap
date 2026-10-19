import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
PASTA = "cloud-aws"
T = "Cloud e AWS"
S = ["demos/cloud.js"]

# ---------------- CAP 6 ----------------
body6 = recap("Até aqui cada serviço apareceu sozinho: EC2 (máquina), S3 (arquivos), RDS (banco). A startup agora quer somar as <b>horas de cada funcionário em cada projeto</b>, e todo mês chega um arquivo atualizado para ser processado e inserido no banco. Dois problemas: como <b>processar arquivos</b>, e como <b>executar código</b> na nuvem sem manter um servidor ligado esperando.") + '''
<section class="sec" id="lambda">
  <h2><span class="sn">1</span>Lambda: código que só existe quando roda</h2>
  <p class="gancho">Para um arquivo que chega uma vez por mês, ter uma máquina ligada é desperdício.</p>
  <p>A <b>AWS Lambda</b> executa código <b>sob demanda, sem gerenciar servidor</b> (<i>serverless</i>). Você sobe só o código, a AWS o roda quando algo o aciona e cobra <b>por execução</b>, considerando duração e memória usada. Linguagens: Python, Node.js, Java, Go, .NET, Ruby. Usos citados: <b>ETL</b> (extrair, transformar, carregar), integração com APIs e com mensageria.</p>
  <div class="tablewrap"><table>
    <tr><th>Característica</th><th>Valor citado na aula</th></tr>
    <tr><td>Cobrança</td><td>por chamada, conforme duração e memória ("pay per use")</td></tr>
    <tr><td>Nível gratuito</td><td>1 milhão de solicitações por mês</td></tr>
    <tr><td>Tempo limite</td><td><b>15 minutos</b> por execução</td></tr>
    <tr><td>Execuções simultâneas</td><td>até 1000 (o limite padrão pode ser menor em contas novas)</td></tr>
    <tr><td>Pacote de implantação</td><td>até 250 MB descompactado</td></tr>
    <tr><td>Memória máxima</td><td>3008 MB no slide</td></tr>
  </table></div>
  <div class="nota cuidado"><span class="lbl">Complemento: limites mudam</span>Os números do slide são de uma época anterior. Hoje a documentação da AWS permite memórias maiores (até cerca de 10 GB), por exemplo. O <b>tempo limite de 15 minutos</b> segue válido e é o que define o tipo de trabalho adequado: tarefas curtas e pontuais, e não processos longos. Confira sempre a documentação atual.</div>
  <p>Compare com a EC2: ela cobra enquanto está ligada, mesmo esperando. A Lambda cobra <b>só quando roda</b>. Para um arquivo mensal, a diferença é enorme.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Quem avisa a função de que o arquivo chegou?</div><p>O próprio S3, por um gatilho.</p></div>
</section>

<section class="sec" id="fluxo">
  <h2><span class="sn">2</span>O fluxo completo: S3, gatilho, Lambda, RDS</h2>
  <p class="gancho">Quatro serviços, um fluxo.</p>
<pre><code>CSV  →  S3  <span class="c">--(gatilho)--&gt;</span>  Lambda  <span class="c">--(INSERT INTO)--&gt;</span>  RDS</code></pre>
  <p>O laboratório, em ordem: <b>(1)</b> criar o bucket; <b>(2)</b> criar o MySQL no RDS e anotar o endpoint; <b>(3)</b> criar a tabela; <b>(4)</b> criar a função Lambda (runtime Python) com um <b>perfil de execução</b> (a role do laboratório); <b>(5)</b> subir o código empacotado; <b>(6)</b> criar o <b>gatilho do S3</b>; <b>(7)</b> subir o CSV no bucket; <b>(8)</b> ver o log no <b>CloudWatch</b>; <b>(9)</b> consultar o RDS. Faça você o passo 7: o banco abaixo é de verdade, e a tabela tem a mesma chave primária composta do laboratório.</p>
  <div class="demo" data-demo="lambdalab"></div>
  <div class="ex rv"><span class="t">O que você acabou de ver</span>
    <div class="l"><div>A <b>chave primária</b> é (<code>idProjeto</code>, <code>idFuncionario</code>): o funcionário 1 pode estar em dois projetos, mas o <b>mesmo par</b> não pode aparecer duas vezes.</div></div>
    <div class="l"><div>Na <b>segunda</b> subida do mesmo CSV, todas as linhas violam a chave primária. O código faz <code>rollback</code>: <b>ou entram todas, ou nenhuma</b>.</div></div>
    <div class="l"><div>O erro apareceria no <b>CloudWatch</b>, onde tudo o que a função imprime (<code>print</code>) vira log.</div></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E o código por dentro? Como a função sabe o que fazer?</div><p>Passo a passo.</p></div>
</section>

<section class="sec" id="codigo">
  <h2><span class="sn">3</span>O código, por dentro</h2>
  <p class="gancho">Ler o arquivo, quebrar em linhas, inserir, confirmar.</p>
<pre><code><span class="k">import</span> boto3, pymysql
<span class="c"># versão resumida: troque pelos valores do seu laboratório</span>
bucket, arquivo = <span class="s">"meu-bucket"</span>, <span class="s">"horasalocadas.csv"</span>
endpoint, usuario, senha, banco = <span class="s">"..."</span>, <span class="s">"..."</span>, <span class="s">"..."</span>, <span class="s">"..."</span>   <span class="c"># na prática: variáveis de ambiente</span>
s3 = boto3.<span class="f">client</span>(<span class="s">'s3'</span>)

<span class="k">def</span> <span class="f">lambda_handler</span>(event, context):      <span class="c"># o ponto de entrada que a AWS chama</span>
    <span class="f">inserir_dados_mysql</span>()
    <span class="k">return</span> {<span class="s">'statusCode'</span>: <span class="n">200</span>, <span class="s">'body'</span>: <span class="s">'Processamento realizado com sucesso!'</span>}

<span class="k">def</span> <span class="f">ler_arquivo_csv_s3</span>():
    response = s3.<span class="f">get_object</span>(Bucket=bucket, Key=arquivo)
    dados = response[<span class="s">'Body'</span>].<span class="f">read</span>().<span class="f">decode</span>(<span class="s">'utf-8'</span>)
    <span class="k">return</span> dados.<span class="f">splitlines</span>()               <span class="c"># lista de linhas do CSV</span>

<span class="k">def</span> <span class="f">inserir_dados_mysql</span>():
    linhas = <span class="f">ler_arquivo_csv_s3</span>()
    conexao = pymysql.<span class="f">connect</span>(host=endpoint, user=usuario, passwd=senha, db=banco)
    <span class="k">try</span>:
        <span class="k">with</span> conexao.<span class="f">cursor</span>() <span class="k">as</span> cursor:
            <span class="k">for</span> linha <span class="k">in</span> linhas[<span class="n">1</span>:]:               <span class="c"># [1:] pula o cabeçalho</span>
                <span class="k">if not</span> linha.<span class="f">strip</span>(): <span class="k">continue</span>
                p = linha.<span class="f">split</span>(<span class="s">";"</span>)               <span class="c"># este CSV usa ponto e vírgula</span>
                cursor.<span class="f">execute</span>(<span class="s">"INSERT INTO projetoFuncionario (idProjeto, idFuncionario, horas) VALUES (%s, %s, %s)"</span>, (p[<span class="n">0</span>], p[<span class="n">1</span>], p[<span class="n">2</span>]))
        conexao.<span class="f">commit</span>()                     <span class="c"># grava tudo de uma vez</span>
    <span class="k">except</span> Exception:
        conexao.<span class="f">rollback</span>()                   <span class="c"># desfaz a execução inteira</span>
        <span class="k">raise</span>
    <span class="k">finally</span>:
        conexao.<span class="f">close</span>()</code></pre>
  <ul>
    <li><b><code>lambda_handler(event, context)</code></b> é a função que a AWS chama. O nome precisa bater com o handler configurado.</li>
    <li><b>O código ignora o <code>event</code></b>: o bucket e o arquivo estão fixos no código. Para o seu laboratório, troque pelo seu bucket e pelo seu endpoint. (Melhor: usar o <code>event</code>, que traz o nome do bucket e do arquivo que dispararam a função.)</li>
    <li><b><code>%s</code> com tupla</b> em vez de montar o SQL concatenando texto: o driver escapa os valores e evita SQL injection.</li>
    <li><b><code>commit()</code> só no fim, <code>rollback()</code> no erro</b>: transação de verdade (Bancos de Dados, Capítulo 8).</li>
    <li>O <b>pacote</b> (<code>.zip</code>) leva a pasta do <code>pymysql</code> junto: a Lambda já traz o <code>boto3</code>, mas <b>não traz o driver do MySQL</b>. (Alternativa mais limpa: <i>layers</i>.)</li>
  </ul>
  <div class="nota erro"><span class="lbl">Cuidado: senha no código</span>O arquivo do exemplo traz endpoint, usuário e senha escritos no próprio <code>.py</code>. Funciona no laboratório, mas em produção a senha vai para <b>variáveis de ambiente</b> da Lambda ou, melhor, para o <b>Secrets Manager</b>. Nunca no repositório.</div>
  <div class="nota lembra"><span class="lbl">Por que a role (LabRole)</span>A Lambda precisa <b>ler o S3</b>, o que exige permissão. Em vez de uma chave de acesso no código, a função <b>assume uma role</b>. É o Capítulo 2 na prática: a role não tem senha e serve para um <b>serviço</b> ganhar permissão.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Lambda</b>: código sob demanda, sem servidor; cobra por execução. Limite de <b>15 min</b> por execução.",
    "Fluxo do laboratório: <b>CSV → S3 → gatilho → Lambda → RDS</b>, com log no <b>CloudWatch</b>.",
    "<code>lambda_handler(event, context)</code> é o ponto de entrada. O <code>event</code> traz quem disparou.",
    "Role de execução no lugar de chave de acesso. <b>Senha</b> em variável de ambiente ou Secrets Manager, nunca no código.",
    "Mesmo CSV duas vezes: <b>erro de chave primária</b> e <code>rollback</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "O que dispara a função no laboratório?", [("a","Um horário fixo."),("b","O upload do CSV no bucket, por meio do gatilho do S3."),("c","Uma chamada manual no console, sempre.")], "O gatilho do S3 avisa a Lambda quando o objeto é criado. Isso é o 'event-driven'.") + quiz(2, "c", "Por que a função precisa de uma role?", [("a","Para ficar mais rápida."),("b","Para guardar a senha do banco."),("c","Para ter permissão de ler o S3 sem uma chave de acesso no código.")], "A role entrega credenciais temporárias ao serviço. Isso evita segredo fixo.") + quiz(3, "a", "Qual o tempo máximo de uma execução da Lambda?", [("a","15 minutos."),("b","1 hora."),("c","Ilimitado.")], "Por isso a Lambda serve para tarefas curtas. Processos longos pedem outra solução.") + flash([
    ("O que é serverless?", "Você não administra servidor: sobe o código e a nuvem o executa e cobra por uso."),
    ("O que é um gatilho?", "Uma regra que dispara a função quando um evento acontece (por exemplo, um objeto criado no S3)."),
    ("Onde ver os prints da função?", "No CloudWatch Logs."),
    ("Por que usar %s no INSERT?", "Para o driver escapar os valores, evitando SQL injection.")]) + ponte("Os serviços funcionam juntos. Como eles se conectam por baixo, e como não gastar o que não devo?", "Com a rede da AWS (VPC) e algumas boas práticas de custo.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
chapter(PASTA, 6, "lambda", T, "Lambda: código sob demanda", "Capítulo 6 · Aula 6",
        "Executar código sem servidor e ligar S3, Lambda e RDS num fluxo completo.",
        ["<b>~45 min</b>", "1 demo · 3 testes · 4 flashcards", "fluxo S3 → Lambda → banco"], body6, scripts=S, sql=True)

# ---------------- CAP 7 ----------------
body7 = recap("Nos capítulos 3 a 6 você usou quatro serviços e viu, três vezes, o mesmo padrão: <b>duas camadas</b> (a trava e a autorização, o endereço e o firewall). Este capítulo, que é <b>complemento</b> (não foi dado em aula), explica a rede por baixo disso tudo e junta as boas práticas para não ter surpresa no custo nem na segurança.", "Onde paramos") + '''
<section class="sec" id="vpc">
  <h2><span class="sn">1</span>VPC: a sua rede dentro da AWS</h2>
  <p class="gancho">Quando o RDS "só é alcançável de dentro da VPC", de que rede se fala?</p>
  <p>A <b>VPC</b> (<i>Virtual Private Cloud</i>) é uma rede virtual <b>isolada</b>, só sua, dentro de uma região. Dentro dela você divide o espaço de endereços em <b>sub-redes</b> (<i>subnets</i>), cada uma em uma zona de disponibilidade.</p>
  <div class="tablewrap"><table>
    <tr><th>Peça</th><th>Papel</th></tr>
    <tr><td><b>Sub-rede pública</b></td><td>tem rota para a internet por um <b>Internet Gateway</b>; abriga o que precisa ser alcançado de fora (um servidor web)</td></tr>
    <tr><td><b>Sub-rede privada</b></td><td>sem rota direta da internet; abriga o que não deve ser exposto (um banco)</td></tr>
    <tr><td><b>NAT Gateway</b></td><td>deixa recursos privados <b>saírem</b> para a internet (atualizações, por exemplo) sem que a internet <b>entre</b> neles</td></tr>
    <tr><td><b>Security Group</b></td><td>firewall da <b>instância</b></td></tr>
    <tr><td><b>NACL</b></td><td>firewall da <b>sub-rede</b></td></tr>
  </table></div>
  <p>É por isso que o banco "ideal" nem deveria ter acesso público: ele fica numa sub-rede <b>privada</b>, e só a aplicação (numa pública ou na mesma VPC) chega até ele.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Existem dois firewalls. Por que, e qual a diferença?</div><p>Um lembra o que passou. O outro não.</p></div>
</section>

<section class="sec" id="sg-nacl">
  <h2><span class="sn">2</span>Security Group x NACL</h2>
  <p class="gancho">Stateful ou stateless: a pergunta que cai em prova.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>Security Group</th><th>NACL</th></tr>
    <tr><td><b>Onde atua</b></td><td>na <b>instância</b></td><td>na <b>sub-rede</b></td></tr>
    <tr><td><b>Memória</b></td><td><b>stateful</b>: se a entrada foi permitida, a resposta sai automaticamente</td><td><b>stateless</b>: entrada e saída são avaliadas <b>separadamente</b>; é preciso permitir as duas</td></tr>
    <tr><td><b>Regras</b></td><td>só <b>Allow</b></td><td><b>Allow e Deny</b>, avaliadas em ordem numérica</td></tr>
    <tr><td><b>Padrão</b></td><td>nega tudo que entra, até haver regra</td><td>a padrão da VPC permite tudo</td></tr>
  </table></div>
  <div class="stepper rv">
    <div class="stage">
      <div class="st"><b>Um pedido chega na porta 443</b><p>O pacote passa primeiro pela <b>NACL</b> da sub-rede (regra de entrada) e depois pelo <b>Security Group</b> da instância.</p></div>
      <div class="st"><b>A resposta volta</b><p>No <b>Security Group</b> (stateful) a resposta é liberada <b>automaticamente</b>, porque a entrada foi permitida. Na <b>NACL</b> (stateless) é preciso uma regra de <b>saída</b> que deixe a resposta passar.</p></div>
      <div class="st"><b>Na prática</b><p>A maior parte das pessoas configura só os <b>Security Groups</b> e deixa a NACL no padrão. A NACL é uma segunda camada, útil para <b>bloquear</b> um IP ou uma faixa inteira (algo que o Security Group, que só tem Allow, não faz).</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>
</section>

<section class="sec" id="boas-praticas">
  <h2><span class="sn">3</span>Boas práticas: arquitetura, custo e acesso</h2>
  <p class="gancho">Uma lista curta que evita os erros mais caros.</p>
  <h3>Os pilares de uma boa arquitetura (AWS Well-Architected)</h3>
  <div class="grid3">
    <div class="card rv"><b>Excelência operacional</b><p>Automatizar, monitorar (CloudWatch) e aprender com falhas.</p></div>
    <div class="card rv"><b>Segurança</b><p>Privilégio mínimo, criptografia, rastreabilidade (IAM, KMS).</p></div>
    <div class="card rv"><b>Confiabilidade</b><p>Recuperar-se de falhas: várias AZs, backups.</p></div>
    <div class="card rv"><b>Eficiência de desempenho</b><p>Usar o tipo de recurso certo e escalar com a demanda.</p></div>
    <div class="card rv"><b>Otimização de custos</b><p>Pagar só pelo que precisa; desligar o que sobra.</p></div>
    <div class="card rv"><b>Sustentabilidade</b><p>Reduzir o impacto energético do que se executa.</p></div>
  </div>
  <h3>Acessando por código</h3>
<pre><code><span class="c"># CLI: listar os seus buckets</span>
aws s3 ls

<span class="c"># Python com boto3: o mesmo, por código (as credenciais vêm da role ou da configuração local)</span>
<span class="k">import</span> boto3
s3 = boto3.<span class="f">client</span>(<span class="s">"s3"</span>)
<span class="k">for</span> b <span class="k">in</span> s3.<span class="f">list_buckets</span>()[<span class="s">"Buckets"</span>]:
    <span class="f">print</span>(b[<span class="s">"Name"</span>])</code></pre>
  <h3>Antes de sair do laboratório</h3>
  <p>Marque o que você já conferiu. O navegador lembra.</p>
  <div class="thread rv" data-demo="checks" data-key="saida">
    <div class="nd" data-n="1"><b>Encerrei as instâncias EC2</b> (Terminate), e liberei IPs elásticos que não uso.<br><label><input type="checkbox"> feito</label></div>
    <div class="nd" data-n="2"><b>Excluí a instância do RDS</b> (e o snapshot final, se não precisar).<br><label><input type="checkbox"> feito</label></div>
    <div class="nd" data-n="3"><b>Esvaziei ou removi os buckets</b> que não vou usar, e confirmei que nenhum ficou público sem querer.<br><label><input type="checkbox"> feito</label></div>
    <div class="nd" data-n="4"><b>Fechei as regras de Security Group</b> com 0.0.0.0/0 em SSH, RDP e portas de banco.<br><label><input type="checkbox"> feito</label></div>
    <div class="nd" data-n="5"><b>Nenhuma chave de acesso ou senha</b> ficou em arquivo de código ou repositório.<br><label><input type="checkbox"> feito</label></div>
    <p class="muted" style="margin:6px 0 0"><b class="chk-n">0 de 5</b> itens conferidos.</p>
  </div>
  <div class="nota cuidado"><span class="lbl">Custo surpresa: como evitar</span>Crie um <b>orçamento com alerta</b> (AWS Budgets) logo no começo de qualquer conta real, use <b>tags</b> para saber de que projeto é cada recurso, e lembre que <b>recurso esquecido ligado</b> é a causa mais comum de conta alta. As regras do nível gratuito mudam com o tempo: leia a página oficial antes de confiar nelas.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento da apostila</h2>
  ''' + resumo([
    "<b>VPC</b>: sua rede virtual isolada. Sub-rede <b>pública</b> (rota para a internet) x <b>privada</b> (sem rota direta). <b>NAT</b> permite sair sem deixar entrar.",
    "<b>Security Group</b>: instância, <b>stateful</b>, só Allow. <b>NACL</b>: sub-rede, <b>stateless</b>, Allow e Deny.",
    "Seis pilares: excelência operacional, segurança, confiabilidade, desempenho, custo e sustentabilidade.",
    "CLI e <code>boto3</code> acessam a AWS por código; prefira <b>roles</b> a chaves.",
    "Termine instâncias, exclua bancos, feche portas, alerte o orçamento."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Qual a diferença central entre Security Group e NACL?", [("a","Nenhuma: são o mesmo firewall."),("b","O Security Group é stateful e age na instância; a NACL é stateless e age na sub-rede."),("c","O Security Group só funciona para Windows.")], "Stateful: a resposta de uma conexão permitida volta sozinha. Stateless: cada sentido é avaliado separadamente.") + quiz(2, "a", "Onde o ideal é colocar um banco de dados?", [("a","Numa sub-rede privada, acessível só pela aplicação."),("b","Numa sub-rede pública, com 0.0.0.0/0 liberado."),("c","No S3.")], "Quanto menos exposto, melhor. A aplicação chega ao banco por dentro da VPC.") + quiz(3, "c", "Qual a causa mais comum de conta de nuvem inesperadamente alta?", [("a","Usar o console em vez da CLI."),("b","Escolher a região errada."),("c","Recursos esquecidos ligados.")], "Instância, banco e IP elástico ociosos continuam gerando custo. Desligue o que não usa e use alertas de orçamento.") + flash([
    ("O que é uma VPC?", "Uma rede virtual isolada dentro da AWS, dividida em sub-redes."),
    ("Stateful x stateless?", "Stateful lembra a conexão (resposta liberada sozinha). Stateless avalia cada pacote de entrada e de saída separadamente."),
    ("Para que serve o NAT Gateway?", "Permite que recursos privados acessem a internet sem serem acessíveis de fora."),
    ("O que é privilégio mínimo?", "Conceder só as permissões estritamente necessárias.")]) + '''
  <div class="ponte rv"><div class="t">E agora?</div><div class="q">Você percorreu a escada: máquina, arquivos, banco e código.</div><p>O melhor exercício é refazer o laboratório do começo ao fim, <b>conferindo cada regra de acesso</b> e encerrando tudo no final. Volte à <a href="index.html">visão geral</a> para revisar, e leve a mesma lente de segurança da apostila de Cibersegurança.</p></div>
</section>'''
chapter(PASTA, 7, "rede-e-boas-praticas", T, "Rede, custos e boas práticas (complemento)", "Capítulo 7 · Complemento",
        "A rede por baixo dos serviços, os dois firewalls e como evitar surpresas de custo e de segurança.",
        ["<b>~40 min</b>", "1 checklist · 3 testes · 4 flashcards", "complemento, não foi dado em aula"], body7, scripts=S)
print("aws caps 6-7 ok")
