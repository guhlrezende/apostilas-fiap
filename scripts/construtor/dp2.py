from dp_base import *
S3 = ["demos/dp-core.js", "demos/cap-3.js"]
S4 = ["demos/dp-core.js", "demos/cap-4.js"]


def cap3():
    corpo = ""
    corpo += secao("tls", 1, "O que o TLS garante",
        "O endereço começa com https e aparece um cadeado. Mas protegido contra o quê, exatamente?",
        camada("Intuição", "Sem cifra, a conversa HTTP é um cartão-postal: quem carrega pode ler. O <b>TLS</b> põe a conversa num envelope lacrado e ainda confere o remetente. O <b>HTTPS</b> é o mesmo HTTP do capítulo 1, só que dentro desse envelope.") +
        camada("Definição", "<b>TLS</b> (Transport Layer Security) dá três garantias à conversa: <b>confidencialidade</b> (quem intercepta não lê), <b>integridade</b> (se alguém alterar no caminho, dá para perceber) e <b>autenticação</b> (você fala com o servidor que diz ser, por meio do certificado). O SSL é o nome do antecessor, que as pessoas ainda usam de forma solta. (IBM.)") +
        ex("HTTP puro contra HTTPS, rodando", [
            "Pedi <code>http://example.com</code> (sem cifra) com <code>curl -sI</code>. A resposta veio <b>200 OK</b>, pela porta 80: o servidor entregou a página <b>sem cifra e sem mandar ir para HTTPS</b>. Ou seja, nem todo site redireciona sozinho.",
            "Já <code>http://iana.org</code> respondeu <b>301</b> para <code>https://www.iana.org/</code>: esse site manda o visitante para a versão cifrada.",
            "Com o <code>openssl s_client -connect example.com:443</code> vi a negociação: protocolo <b>TLSv1.3</b>, cifra <b>TLS_AES_256_GCM_SHA384</b> e <b>Verification: OK</b>. Isso é o handshake do TLS, que acontece antes de o HTTP trafegar.",
        ]) +
        code('''
$ curl -sI http://example.com | head -1
HTTP/1.1 200 OK                                   # sem cifra, e sem redirecionar
$ curl -s -o /dev/null -w "%{http_code} %{redirect_url}\\n" http://iana.org
301 https://www.iana.org/                         # este site manda para HTTPS
$ echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | grep -E "Protocol|Cipher is|Verification"
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Protocol: TLSv1.3
Verification: OK
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026. O <code>openssl</code> é o do Git Bash; no PowerShell puro ele costuma não existir. As cifras e versões dependem do servidor e da sua versão do <code>openssl</code>.</p>' +
        erro("Achar que HTTPS esconde <b>com quem</b> você fala. O conteúdo (caminho, cabeçalhos, corpo) vai cifrado, mas o nome do servidor ainda é consultado no DNS e a conexão vai para um IP: quem observa a rede consegue saber que você visitou aquele servidor, só não vê o que foi dito. (Minha leitura geral do funcionamento; a página da IBM não entra nesse detalhe.)"),
        ponte("O TLS promete que o servidor é quem diz ser. Mas o que o navegador confere, de fato, para acreditar?", "Com o certificado e a cadeia de autoridades."))

    corpo += secao("certificado", 2, "O certificado e o que o navegador confere",
        "Qualquer um pode dizer \"sou o meusite.example\". O que prova isso?",
        camada("Intuição", "É um documento com foto, como o RG. O <b>certificado</b> diz \"este servidor responde por estes nomes, de tal data a tal data\" e vem <b>assinado por uma autoridade</b> em que o navegador já confia (a <b>CA</b>, autoridade certificadora). Como o RG, só vale se for do nome certo, estiver na validade e tiver sido emitido por um órgão reconhecido.") +
        camada("Definição", "No início da conexão, o servidor apresenta o certificado. O navegador faz <b>três conferências</b>: (1) o <b>nome</b> do endereço aberto está entre os nomes do certificado, (2) a data de hoje está dentro da <b>validade</b> e (3) a <b>cadeia</b> de assinaturas chega a uma autoridade raiz que o navegador já conhece. Se qualquer uma falhar, aparece o aviso. (IBM descreve certificado, autoridade e handshake.) Um certificado com curinga, como <code>*.exemplo.test</code>, cobre <b>um nível</b>: <code>www.exemplo.test</code> sim, <code>a.b.exemplo.test</code> não (regra geral de certificados, sem fonte lida aqui).") +
        '<div class="demo" data-demo="certCheck"></div>' +
        ex("um certificado de verdade, aberto", [
            "O <code>openssl x509</code> mostrou, para <code>example.com</code>: emissor <code>Cloudflare TLS Issuing ECC CA 3</code>, válido de <b>26/09/2026</b> a <b>25/12/2026</b> (<b>90 dias</b>) e nomes <code>example.com</code> e <code>*.example.com</code>.",
            "Com <code>-showcerts</code>, o <code>openssl s_client</code> listou a cadeia que o servidor enviou: <b>4</b> certificados (o do site e três acima dele, o último uma raiz). No fim, o <code>openssl</code> imprimiu <code>Verify return code: 0 (ok)</code>: a cadeia chegou a uma autoridade que a lista do <code>openssl</code> reconhece. É o equivalente, no terminal, da conferência que o navegador faz.",
            "Conferindo as três perguntas para a data de hoje (06/11/2026): o nome bate, a data está dentro de 26/09 a 25/12, a cadeia termina numa raiz conhecida. Resultado: <b>3 de 3</b>, cadeado.",
        ]) +
        code('''
$ echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
subject=CN=example.com
issuer=C=US, O=SSL Corporation, CN=Cloudflare TLS Issuing ECC CA 3
notBefore=Sep 26 22:49:11 2026 GMT
notAfter=Dec 25 22:56:35 2026 GMT
X509v3 Subject Alternative Name:
    DNS:example.com, DNS:*.example.com
$ echo | openssl s_client -connect example.com:443 -servername example.com -showcerts 2>/dev/null | grep -E "^ *[0-9] s:|Verify return code"
 0 s:CN=example.com
 1 s:C=US, O=SSL Corporation, CN=Cloudflare TLS Issuing ECC CA 3
 2 s:C=US, O=SSL Corporation, CN=SSL.com TLS Transit ECC CA R2
 3 s:C=US, O=SSL Corporation, CN=SSL.com TLS ECC Root CA 2022
Verify return code: 0 (ok)
''') +
        '<p>Ainda no mundo real, três sites públicos feitos <b>de propósito</b> para quebrar (<code>badssl.com</code>) mostram o que o <code>curl</code> diz quando uma das conferências falha. As mensagens saem do Windows em português, porque o <code>curl</code> daqui usa o Schannel:</p>' +
        code('''
$ curl -sS https://expired.badssl.com
curl: (35) schannel: next InitializeSecurityContext failed: SEC_E_CERT_EXPIRED (0x80090328) - O certificado recebido expirou.
$ curl -sS https://wrong.host.badssl.com
curl: (60) schannel: SNI or certificate check failed: SEC_E_WRONG_PRINCIPAL (0x80090322) - O nome principal do destino está incorreto.
$ curl -sS https://self-signed.badssl.com
curl: (60) schannel: SEC_E_UNTRUSTED_ROOT (0x80090325) - A cadeia de certificação foi emitida por uma autoridade que não é de confiança.
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026. Os três erros são exatamente as três conferências da demo: <b>validade</b> (expirado), <b>nome</b> (wrong.host) e <b>autoridade</b> (autoassinado). Num curl com OpenSSL as mensagens têm outro texto.</p>' +
        erro("Resolver o aviso de certificado <b>desligando a verificação</b> (a opção <code>-k</code> do curl, ou clicar em \"continuar mesmo assim\"). Isso apaga justamente a garantia de autenticação. O conserto de verdade é arrumar o certificado: renovar o vencido, emitir um que cubra o nome certo ou usar uma autoridade confiável. Certificado vencido costuma ser esquecimento de renovação."),
        ponte("O cadeado só vale se o certificado estiver certo. E ele resolve tudo em segurança de site?", "Não. Veja o que ele não garante."))

    corpo += secao("limites", 3, "O que o cadeado não garante",
        "Se tem cadeado, posso confiar no site?",
        camada("Intuição", "O cadeado diz \"esta conversa é privada e é mesmo com este endereço\". Não diz \"este endereço é de gente honesta\". É como conferir que o envelope está lacrado e que o endereço do destinatário bate, sem saber quem mora lá.") +
        camada("Definição", "O TLS protege o <b>caminho</b> entre navegador e servidor. Ele <b>não</b> protege contra: um site malicioso que também tem certificado válido (o certificado prova o domínio, não a intenção); um servidor com falha de segurança no código; dados que o próprio site guarda mal depois que chegam; nem o seu computador infectado. (Isto é conhecimento geral de segurança; as páginas da IBM que li explicam o que o TLS faz, não listam esses limites item a item.)") +
        tabela(["O cadeado garante", "O cadeado NÃO garante"], [
            ["a conversa não é lida no caminho", "que o dono do site é confiável"],
            ["o conteúdo não é alterado no caminho", "que o código do site não tem falhas"],
            ["o servidor controla aquele nome de domínio", "que seus dados ficam seguros depois de chegarem"],
        ]) +
        ex("o que fazer quando é você que publica", [
            "Meta: seu site <b>só</b> abrir por HTTPS. Procure, na documentação da plataforma escolhida, se há opção de forçar HTTPS ou redirecionar.",
            "Teste de fora: <code>curl -sI http://seudominio</code> deveria dar um <b>3xx</b> com <code>Location: https://...</code> (o <code>iana.org</code> deu 301; conforme a plataforma pode ser 301, 302, 307 ou 308). Esse comando é para Git Bash ou <code>curl.exe</code>: no PowerShell 5.1, <code>curl</code> é apelido de <code>Invoke-WebRequest</code> e <code>-sI</code> falha. Se der 200 (como o <code>example.com</code> deu), o HTTP puro continua disponível.",
            "Certificado: a maioria das plataformas de hospedagem estática cuida do certificado para você; num VPS próprio, você mesmo emite e renova. O Certbot (da EFF) é, segundo a página oficial que li em 06/11/2026, uma ferramenta que facilita obter e configurar HTTPS com certificados do Let's Encrypt; essa página <b>não traz os comandos</b> (só pergunta qual software e sistema você usa), então eu não os mostro.",
        ]) +
        naotestado("Emitir certificado com Certbot ou configurar HTTPS no nginx não foram rodados aqui (o nginx não está instalado e eu não tenho um servidor com domínio). O que o capítulo mostra de certificado é leitura de certificados públicos já existentes.") +
        erro("Esquecer da renovação. Certificado tem prazo (o de <code>example.com</code> acima dura 90 dias). Se a emissão é automática, ótimo; se é manual, ponha um lembrete. Quando vence, todos os visitantes veem o aviso de segurança e o seu site \"parece invadido\"."),
        ponte("A conexão é segura e o nome está certo. Agora a pergunta prática: em que tipo de lugar o meu site pode morar?", "Com os tipos de hospedagem."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>HTTPS = HTTP + TLS.</b> O TLS dá confidencialidade, integridade e autenticação.",
        "O certificado diz <b>quais nomes</b> o servidor responde, <b>até quando</b> e <b>quem assinou</b>.",
        "O navegador confere <b>três coisas</b>: nome, validade e cadeia até uma autoridade conhecida.",
        "Curinga <code>*.dominio</code> cobre <b>um nível</b> de subdomínio.",
        "Cadeado não garante que o site é honesto nem que o código dele é seguro.",
        "Nunca resolva erro de certificado desligando a verificação (<code>-k</code>); corrija o certificado."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "O navegador mostra aviso de segurança em <code>https://loja.exemplo.test</code>, e o certificado só lista <code>www.exemplo.test</code>. Qual conferência falhou?", [("a", "A validade."), ("b", "O nome: o endereço aberto não está entre os nomes do certificado."), ("c", "A porta 443 estar fechada.")], "É a conferência de nome. Os erros da validade e da autoridade são outros: expirado e raiz não confiável.") + \
        quiz(2, "c", "Um certificado com <code>*.exemplo.test</code> cobre qual endereço?", [("a", "<code>exemplo.test</code> e todos os níveis abaixo dele."), ("b", "<code>a.b.exemplo.test</code>."), ("c", "<code>www.exemplo.test</code>.")], "O curinga cobre um nível. O nome sem subdomínio (<code>exemplo.test</code>) e o de dois níveis (<code>a.b.exemplo.test</code>) precisam constar à parte.") + \
        quiz(3, "a", "Seu site tem cadeado válido. O que ainda pode estar errado?", [("a", "O código do site ter uma falha, ou o dono não ser confiável: o cadeado não prova isso."), ("b", "O TLS não estar ativo."), ("c", "Nada: cadeado garante tudo.")], "O TLS protege o caminho e confirma o domínio. Ele não audita o site.") + \
        flash([
            ("As três garantias do TLS?", "Confidencialidade, integridade e autenticação."),
            ("As três conferências do navegador num certificado?", "Nome, validade e cadeia até uma autoridade confiável."),
            ("O que é uma CA?", "Autoridade certificadora: quem assina certificados e é reconhecida pelos navegadores."),
            ("Por que não usar curl -k para \"resolver\" o erro?", "Porque desliga a verificação e apaga a garantia de autenticação. O certo é consertar o certificado.")]) + \
        fontes("ibm_tls", "badssl", "certbot") + \
        ponte("A conversa está protegida. Falta escolher onde o site mora.", "Com os tipos de hospedagem.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
    recap_html = recap("No capítulo 2 o nome virou um IP pelo DNS. A pergunta que ficou: <b>como confiar que quem respondeu é o dono do site e que ninguém lê a conversa?</b> Este capítulo, que segue sendo <b>complemento</b>, responde com HTTPS, TLS e o certificado, e abre certificados reais de sites públicos.")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 3, "https-tls-certificado", TITULO, "HTTPS, TLS e certificado", "Capítulo 3 · Complemento",
            "O que o cadeado prova, o que o navegador confere num certificado e o que o cadeado nunca prometeu.",
            chips(body, 40), body, scripts=S3)


def cap4():
    corpo = ""
    corpo += secao("modelos", 1, "IaaS, PaaS e SaaS: quanto você administra",
        "Hospedar quer dizer \"alugar um computador\", \"alugar uma plataforma\" ou \"usar um programa pronto\"? Qual a diferença?",
        camada("Intuição", "É a diferença entre morar de aluguel num terreno vazio (você constrói tudo), num apartamento (a estrutura é do prédio, você cuida do interior) e num hotel (só chegar e usar). Quanto mais para cima, <b>menos você administra</b>, e menos você controla.") +
        camada("Definição", "<b>IaaS</b> (infraestrutura como serviço): você recebe máquinas e rede e cuida do sistema operacional e das aplicações. <b>PaaS</b> (plataforma como serviço): você recebe a plataforma pronta e cuida só do código e dos dados. <b>SaaS</b> (software como serviço): você usa o programa pronto pela internet, como um e-mail ou um editor online. (IBM.)") +
        tabela(["", "Quem cuida do sistema operacional?", "Quem cuida do código?", "Exemplo de uso"], [
            ["IaaS", "você", "você", "um servidor virtual onde você instala o que quiser"],
            ["PaaS", "a plataforma", "você", "você envia o código e ele roda"],
            ["SaaS", "o provedor", "o provedor", "usar o programa pronto"],
        ]) +
        '<p class="muted">Dos produtos concretos, a base de leitura só registra que a IBM cita o <b>Heroku</b> como PaaS. <b>Elastic Beanstalk</b> e <b>App Engine</b> são exemplos que eu lembrei por conta própria, não vieram da IBM. Não conferi se algum deles existe hoje nem seus planos: pesquise antes.</p>',
        ponte("Esses são os modelos. Mas, na prática, onde coloco um site: em que tipo de lugar?", "Em cinco tipos de hospedagem."))

    corpo += secao("tipos", 2, "Estático, PaaS, container, VPS e serverless",
        "Tenho um site e quero colocá-lo no ar. O que existe entre \"arrastar uma pasta\" e \"montar meu servidor\"?",
        camada("Intuição", "Cada tipo é um degrau de controle. Num extremo, a plataforma só entrega seus arquivos. No outro, você tem uma máquina inteira, e tudo (inclusive o erro) é seu.") +
        tabela(["Tipo", "O que é", "Você cuida de", "Quando usar"], [
            ["Hospedagem estática", "só entrega arquivos prontos (HTML, CSS, JS, imagens)", "o conteúdo", "portfólio, documentação, site que não tem servidor próprio (as apostilas, por exemplo)"],
            ["PaaS", "a plataforma roda o seu código", "o código e os dados", "aplicação com servidor, sem querer administrar máquina"],
            ["Container", "pacote com a aplicação e o que ela precisa; compartilha o sistema do host", "a imagem e a configuração", "quando o ambiente precisa ser igual do seu computador à produção"],
            ["VPS", "uma fatia de um servidor físico com sistema próprio", "o sistema, a segurança e as atualizações (se não gerenciado)", "controle total, vários sites, aprender administração"],
            ["Serverless (funções)", "você envia código e paga pelo tempo de execução", "só o código", "tarefas pontuais e APIs leves, com uso irregular"],
        ]) +
        '<p>Há ainda a <b>hospedagem compartilhada</b> (barata e limitada) e a <b>dedicada</b> (um servidor físico só seu), que a IBM coloca em volta do VPS. Containers merecem uma apostila própria; aqui basta saber que são uma forma de empacotar a aplicação. (IBM: VPS, containers, serverless, PaaS.)</p>' +
        ex("os limites que a IBM aponta", [
            "<b>Serverless</b>: você não administra servidor e paga por execução, mas tem menos controle, pode sofrer uma demora na primeira chamada (a <b>partida a frio</b>) e fica preso ao fornecedor.",
            "<b>VPS</b>: pode ser <b>gerenciado</b> (o provedor cuida de parte do trabalho) ou <b>não gerenciado</b> (tudo é seu: atualização, firewall, backup).",
            "<b>Balanceador de carga e CDN</b> aparecem quando o site cresce: o primeiro distribui pedidos entre vários servidores (rodízio, IP de origem, menos conexões), o segundo guarda cópias do conteúdo perto do visitante. A IBM detalha o balanceador; sobre CDN ela só dá uma frase, então não aprofundo.",
            "<b>IBM Cloud</b> tem dois exemplos concretos nas fontes: arquivos estáticos num bucket público com <code>index.html</code> (Cloud Object Storage) e um serviço para rodar containers a partir do GitHub (Code Engine, tutorial de 2024). Não os testei e não conferi preço.",
        ]) +
        erro("Escolher a hospedagem pelo preço e descobrir tarde o que ela não faz. Plano gratuito, por exemplo, costuma ter <b>limites</b> (de tamanho, de tráfego, de tempo ocioso). Eles mudam, e por isso esta apostila não cita nenhum número: abra a página oficial do serviço e leia os limites <b>na data em que você for usar</b>."),
        ponte("Tenho as opções. Como decido sem decorar tabela?", "Com perguntas sobre o seu projeto."))

    corpo += secao("decisao", 3, "Uma árvore de decisão",
        "Meu projeto tem estas características. Qual tipo faz sentido, e por quê?",
        camada("Intuição", "A decisão não é \"qual o melhor\", é \"qual o menor que resolve\". Se o site é só arquivo, um servidor seu é peso demais. Se precisa de banco, a plataforma tem de oferecer um. Se você quer controle total mas não sabe administrar, o preço do controle vai ser tempo e risco.") +
        camada("Definição", "A demo abaixo é uma árvore de regras simples escrita por mim: ela combina o que o site tem (só arquivos, código, código e banco), orçamento, controle desejado, conhecimento de administração e picos de acesso. É um <b>ponto de partida</b>, não uma regra do mercado.") +
        '<div class="demo" data-demo="ondeHospedar"></div>' +
        ex("três cenários rodados na demo", [
            "<b>Portfólio só com HTML e CSS, orçamento zero, sem precisar de controle, picos: não.</b> A demo recomenda <b>hospedagem estática</b> (GitHub Pages, Cloudflare Pages, Netlify ou Vercel) e alerta para conferir o plano gratuito na página oficial.",
            "<b>Aplicação com banco de dados, com picos fortes de acesso, sem controle de servidor.</b> A demo recomenda <b>serverless ou PaaS com escala automática, mais banco gerenciado</b>, e avisa da partida a frio e da dependência do fornecedor.",
            "<b>Aplicação com banco, controle total desejado, sabe administrar Linux, picos: não.</b> A demo recomenda <b>VPS (ou IaaS) com nginx como proxy reverso e a aplicação num container</b>, e lembra que backup, atualização e monitoramento passam a ser seus.",
            "Troque \"sabe administrar\" para <b>não</b> no terceiro cenário (mantendo picos: não) e a recomendação muda para PaaS com banco gerenciado, com o aviso de que VPS sem gerenciamento é arriscado para quem está começando.",
            "Marque <b>picos: sim</b> no terceiro cenário e o resultado continua sendo VPS, mas a demo acrescenta o cuidado de que uma máquina só não escala sozinha (balanceador e mais de uma máquina, ou serverless para a parte que oscila).",
        ]) +
        erro("Acreditar que a recomendação da demo (ou de qualquer tabela) vale como dado de mercado. Ela traduz as ideias da IBM e as minhas escolhas de ensino. Preço, cota e recursos de cada serviço mudam: a regra é <b>decidir pelo requisito e conferir o serviço na hora de contratar</b>."),
        ponte("Já sei onde cada tipo de projeto pode morar. Mãos à obra: como eu coloco um site estático no ar?", "Por três caminhos, com comandos."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>IaaS</b>: você administra do sistema para cima. <b>PaaS</b>: você cuida do código. <b>SaaS</b>: você só usa.",
        "Estático = só arquivos. PaaS = a plataforma roda seu código. VPS = máquina virtual sua. Serverless = função cobrada por execução. Container = aplicação empacotada.",
        "Serverless: paga por execução, mas tem <b>partida a frio</b> e prende ao fornecedor.",
        "VPS não gerenciado: <b>atualização, firewall e backup são seus</b>.",
        "Decida pelo <b>requisito</b> (o menor que resolve). Preço e limites: confira na página oficial, na data do uso.",
        "Balanceador de carga distribui pedidos; CDN guarda cópias perto do visitante."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Um blog feito só de HTML, CSS e imagens, sem login, sem banco. Qual o tipo de hospedagem mais simples?", [("a", "Hospedagem estática."), ("b", "VPS com banco de dados."), ("c", "Serverless com função para cada página.")], "Se tudo são arquivos prontos, uma hospedagem estática basta. Quanto menos você administra, menos você tem de errar.") + \
        quiz(2, "c", "Qual a principal desvantagem de um VPS <b>não gerenciado</b> para quem está começando?", [("a", "Não permite instalar nada."), ("b", "Não tem sistema operacional."), ("c", "Atualização, segurança e backup ficam por sua conta.")], "O VPS dá controle, e o preço do controle é responsabilidade. O gerenciado divide parte desse trabalho com o provedor.") + \
        quiz(3, "b", "O que significa \"partida a frio\" no serverless?", [("a", "A função só roda no inverno."), ("b", "A primeira chamada depois de um tempo parado pode demorar mais."), ("c", "O banco de dados é apagado.")], "É a demora extra quando a função precisa ser iniciada. A IBM lista isso entre as limitações do modelo.") + \
        quiz(4, "b", "No PaaS, quem cuida do sistema operacional?", [("a", "Você."), ("b", "A plataforma."), ("c", "O visitante.")], "No PaaS você envia o código e a plataforma cuida do sistema e do servidor. No IaaS o sistema é seu.") + \
        flash([
            ("IaaS, PaaS e SaaS em uma frase cada?", "IaaS: você recebe a infraestrutura. PaaS: você recebe a plataforma e cuida do código. SaaS: você usa o programa pronto."),
            ("Quando a hospedagem estática serve?", "Quando o site é só arquivo pronto: HTML, CSS, JS e imagens."),
            ("O que é partida a frio?", "A demora extra da primeira chamada a uma função serverless que estava parada."),
            ("Por que não decorar números de plano gratuito?", "Porque limites e preços mudam; confira na página oficial na data do uso.")]) + \
        fontes("ibm_iaas", "ibm_paas", "ibm_containers", "ibm_serverless", "ibm_vps", "ibm_lb", "ibm_cos", "ibm_codeengine") + \
        ponte("Sei qual tipo escolher. Falta fazer o site chegar lá.", "Com três caminhos para publicar um site estático.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
    recap_html = recap("Nos capítulos anteriores você viu como a web funciona, como o nome vira IP e como a conexão é protegida. A pergunta agora é prática: <b>em que tipo de lugar o site mora?</b> Este capítulo, <b>complemento</b> como os outros, organiza as opções e ajuda a escolher pelo requisito.")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 4, "tipos-de-hospedagem", TITULO, "Tipos de hospedagem e quando usar cada um", "Capítulo 4 · Complemento",
            "Estático, PaaS, container, VPS e serverless, e uma árvore de decisão que mostra o raciocínio.",
            chips(body, 40), body, scripts=S4)
