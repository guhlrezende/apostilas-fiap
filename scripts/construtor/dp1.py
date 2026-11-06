from dp_base import *
S = ["demos/dp-core.js", "demos/cap-1.js"]
S2 = ["demos/dp-core.js", "demos/cap-2.js"]


def cap1():
    corpo = ""
    corpo += secao("cliente-servidor", 1, "Cliente e servidor",
        "Digito um endereço, aperto Enter e a página aparece. Quem fez o quê nesse meio tempo?",
        camada("Intuição", "É um pedido em balcão. Você (o <b>cliente</b>, quase sempre o navegador) chega e pede uma coisa. Quem atende (o <b>servidor</b>, um computador que fica ligado esperando) entrega o que foi pedido ou diz que não tem. <b>Quem começa a conversa é sempre o cliente</b>: o servidor não toca a campainha sozinho.") +
        camada("Definição", "<b>Cliente</b> é o programa que faz o pedido. <b>Servidor</b> é o programa (e, por extensão, a máquina) que fica esperando pedidos e responde. Entre os dois podem existir intermediários, como proxies e caches. A conversa segue um combinado chamado <b>HTTP</b>. <span class='muted'>(Fora da IBM: a descrição de cliente-servidor e de HTTP vem do MDN. As páginas da IBM que tentei ler sobre isso devolveram só o índice geral.)</span>") +
        ex("o menor servidor possível, na minha máquina", [
            "Criei uma pasta temporária com um único arquivo <code>index.html</code> e rodei <code>python -m http.server 8765 --bind 127.0.0.1</code>. Isso liga um servidor web que só aceita pedidos <b>do próprio computador</b> (o <code>127.0.0.1</code>).",
            "Em outro terminal, o <code>curl</code> fez o papel de cliente: <code>curl -si http://127.0.0.1:8765/</code>. A resposta veio com a primeira linha <code>HTTP/1.0 200 OK</code>, alguns cabeçalhos e depois o conteúdo do arquivo (45 bytes).",
            "Com o servidor desligado, o mesmo pedido falhou: o cliente não tinha ninguém para atender. Quem pede e ninguém responde é o erro mais básico da web.",
        ]) +
        code('''
$ python -m http.server 8765 --bind 127.0.0.1     # num terminal: liga o servidor
$ curl -si http://127.0.0.1:8765/ | head -8        # em outro: o cliente pede
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.5
Date: Fri, 06 Nov 2026 17:42:28 GMT
Content-type: text/html
Content-Length: 45
Last-Modified: Fri, 06 Nov 2026 17:42:25 GMT

<!doctype html><title>oi</title><h1>ola</h1>
$ curl -sS http://127.0.0.1:8765/                   # com o servidor desligado
curl: (7) Failed to connect to 127.0.0.1:8765 after 0 ms: Could not connect to server
''') +
        '<p class="muted" style="font-size:.85rem">Rodado de verdade em 06/11/2026, num Windows 11 com Git Bash. A data e o tamanho são os da execução; a versão do Python depende da sua máquina.</p>' +
        erro("Achar que o site \"está no ar\" porque abre no seu computador. Quando você abre <code>index.html</code> com duplo clique, o navegador lê o arquivo direto do disco (endereço <code>file://</code>): não existe servidor nem HTTP nessa conversa. Para o mundo ver, uma máquina precisa estar <b>ligada, com um servidor rodando, e alcançável pela internet</b>. É disso que o resto da apostila trata."),
        ponte("Cliente pede, servidor responde. Mas como é, exatamente, um pedido?", "Com o HTTP: método, caminho, cabeçalhos e código de status."))

    corpo += secao("http", 2, "HTTP: a conversa em pedido e resposta",
        "O servidor sabe que a minha página inicial é o <code>index.html</code>. Como ele sabe o que eu pedi, e como me diz se deu certo?",
        camada("Intuição", "É um formulário de pedido com campos fixos. Na frente vai <b>o que você quer fazer</b> (pegar, enviar, apagar) e <b>onde</b> (o caminho). Atrás vão informações extras (os <b>cabeçalhos</b>). A resposta volta no mesmo formato, com um <b>número</b> na frente que resume o resultado: o código de status.") +
        camada("Definição", "A <b>requisição</b> tem uma linha inicial (<code>MÉTODO caminho HTTP/versão</code>), cabeçalhos e, às vezes, um corpo. A <b>resposta</b> tem uma linha inicial (<code>HTTP/versão código texto</code>), cabeçalhos e, quase sempre, um corpo. O <b>método</b> diz a intenção: <code>GET</code> pede um recurso, <code>HEAD</code> pede só os cabeçalhos, <code>POST</code> envia dados, <code>PUT</code> substitui, <code>DELETE</code> apaga, <code>OPTIONS</code> pergunta o que é permitido. (Fora da IBM, MDN.)") +
        tabela(["Código", "Família", "Significa", "Quem errou?"], [
            ["200", "2xx sucesso", "OK, o corpo vem junto", "ninguém"],
            ["201", "2xx sucesso", "criado (comum depois de um POST)", "ninguém"],
            ["301", "3xx redirecionamento", "mudou de lugar; veja o cabeçalho <code>Location</code>", "ninguém, só avisa"],
            ["400", "4xx erro do cliente", "o pedido veio malformado", "quem pediu"],
            ["401 e 403", "4xx erro do cliente", "401: falta se identificar; 403: identificado, mas sem permissão", "quem pediu"],
            ["404", "4xx erro do cliente", "o caminho não existe", "quem pediu (ou o link quebrou)"],
            ["500", "5xx erro do servidor", "o código ou a configuração do servidor falhou", "quem mantém o servidor"],
        ]) +
        ex("lendo uma resposta real", [
            "Pedi os cabeçalhos de um site público de teste: <code>curl -sI https://example.com</code>. A primeira linha veio <code>HTTP/1.1 200 OK</code>: família 2xx, deu certo.",
            "O cabeçalho <code>Content-Type: text/html; charset=utf-8</code> diz o tipo do corpo. O <code>curl -s -o /dev/null -w \"%{http_code} %{content_type} %{size_download} bytes\"</code> deu <b>200 text/html; charset=utf-8 577 bytes</b>: a página inteira tem 577 bytes.",
            "Um caminho que não existe, <code>/nao-existe-xyz</code>, devolveu <b>404</b>. E <code>http://iana.org</code> (sem o www e sem cifra) devolveu <b>301</b> com destino <code>https://www.iana.org/</code>: o servidor mandou ir para outro endereço.",
            "No PowerShell 5.1, <code>Invoke-WebRequest -UseBasicParsing</code> mostra os mesmos fatos em propriedades: <code>StatusCode</code> 200 e <code>StatusDescription</code> OK.",
        ]) +
        code('''
$ curl -sI https://example.com
HTTP/1.1 200 OK
Date: Fri, 06 Nov 2026 17:40:11 GMT
Content-Type: text/html; charset=utf-8
Server: cloudflare
Accept-Ranges: bytes
$ curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download} bytes\\n" https://example.com
200 text/html; charset=utf-8 577 bytes
$ curl -s -o /dev/null -w "%{http_code}\\n" https://example.com/nao-existe-xyz
404
$ curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\\n" http://iana.org
301 -> https://www.iana.org/
PS> $r = Invoke-WebRequest -Uri https://example.com -UseBasicParsing
PS> $r.StatusCode; $r.StatusDescription
200
OK
''') +
        '<p class="muted" style="font-size:.85rem">Rodado de verdade em 06/11/2026 (mostrei só algumas linhas dos cabeçalhos; a lista completa varia de servidor para servidor). <b>Atenção ao shell:</b> os comandos <code>curl -sI</code>, <code>-o /dev/null</code> e <code>head</code> são para o <b>Git Bash</b> (ou para o <code>curl.exe</code>). No PowerShell 5.1, <code>curl</code> é apelido de <code>Invoke-WebRequest</code> e essas opções dão erro; por isso o exemplo em PowerShell usa <code>Invoke-WebRequest</code> direto.</p>' +
        '<p>Agora monte você mesmo. O servidor desta demo é de mentira, mas o formato é o do HTTP de verdade:</p>' +
        '<div class="demo" data-demo="httpSim"></div>' +
        erro("Dois tropeços que aprendi comparando. (1) <b>Confundir 404 com 500.</b> No meu servidor local, pedir uma rota que não existe dá 404 (erro de quem pediu); já um bug no código do servidor dá 500 (erro de quem mantém). Quando o site \"quebra\" depois de um deploy, 500 aponta para o seu código e 404 costuma apontar para caminho ou nome de arquivo. (2) <b>POST em página estática.</b> O servidor simples do Python respondeu <b>501</b> a um <code>POST</code> na raiz, porque ele só sabe entregar arquivos. Outros servidores respondem 405. O recado é o mesmo: a rota existe, mas não aceita esse método."),
        ponte("Entendi o pedido. Mas, na internet, como a mensagem encontra o servidor certo entre milhões de máquinas?", "Com o endereço IP e as portas."))

    corpo += secao("ip-portas", 3, "IP e portas: o endereço e a porta de entrada",
        "O pedido sai do meu computador. Para onde ele vai, e como o servidor sabe que é um pedido de site e não outra coisa?",
        camada("Intuição", "A IBM usa a comparação de um hotel: o <b>endereço IP</b> é o prédio, a <b>porta</b> é o quarto. O IP leva a mensagem até a máquina certa; a porta leva até o programa certo dentro dela. Uma máquina pode ter um servidor web, um acesso remoto e um banco de dados, cada um em seu quarto.") +
        camada("Definição", "O <b>IP</b> identifica um dispositivo numa rede (existem os de versão 4, como <code>203.0.113.10</code>, e os de versão 6, bem mais longos). A <b>porta</b> é um número de 0 a 65535 que escolhe o serviço. Os números mais famosos são convenção: <b>80</b> para HTTP, <b>443</b> para HTTPS e <b>22</b> para SSH. (IBM, rede; as portas padrão são convenção de uso, sem página da IBM lida.)") +
        tabela(["Serviço", "Porta padrão", "Para quê"], [
            ["HTTP", "80", "site sem cifra"],
            ["HTTPS", "443", "site com TLS (capítulo 3)"],
            ["SSH", "22", "acessar o servidor pelo terminal (apostila de Terminal e Git)"],
            ["servidor de teste local", "à sua escolha (usei 8765)", "só você enxerga"],
        ]) +
        ex("testando se uma porta responde", [
            "O <code>Test-NetConnection example.com -Port 443</code> tenta abrir uma conexão com a porta 443 do servidor. Veio <b>TcpTestSucceeded : True</b>: tem um serviço ouvindo.",
            "Em seguida testei <code>127.0.0.1</code> na porta <code>8765</code> com o servidor Python desligado: <b>TcpTestSucceeded : False</b>. Ninguém ouvindo, ninguém atende.",
            "É o mesmo fato do erro <code>curl: (7)</code> que vimos: IP certo, porta sem programa.",
        ]) +
        code('''
PS> Test-NetConnection example.com -Port 443 | Format-List ComputerName,RemotePort,TcpTestSucceeded
ComputerName     : example.com
RemotePort       : 443
TcpTestSucceeded : True
PS> Test-NetConnection 127.0.0.1 -Port 8765 | Format-List ComputerName,RemotePort,TcpTestSucceeded
ComputerName     : 127.0.0.1
RemotePort       : 8765
TcpTestSucceeded : False
''') +
        '<p class="muted" style="font-size:.85rem">O <code>Test-NetConnection</code> é do PowerShell no Windows. No Git Bash, o <code>curl</code> dá a mesma informação de outro jeito. Rodado em 06/11/2026.</p>' +
        erro("Esquecer que a porta também precisa estar <b>liberada</b> no caminho. Num servidor de verdade, um firewall pode bloquear a 80 ou a 443 e o site \"some\" mesmo com o nginx rodando. Uma causa comum de site que some é o firewall não liberar a 22 (SSH), a 80 e a 443. Num servidor remoto isso é <mark class='hl p'>não testado aqui</mark>."),
        ponte("Sei que o pedido vai para um IP e uma porta. Mas ninguém digita 203.0.113.10: usamos nomes. Quem transforma o nome em número?", "Com o DNS."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>Cliente</b> pede, <b>servidor</b> responde. Quem começa é sempre o cliente.",
        "HTTP é o combinado da conversa: <b>requisição</b> (método, caminho, cabeçalhos, corpo) e <b>resposta</b> (código, cabeçalhos, corpo).",
        "Métodos: <code>GET</code> pega, <code>HEAD</code> só cabeçalhos, <code>POST</code> envia, <code>PUT</code> troca, <code>DELETE</code> apaga.",
        "Status: <b>2xx</b> deu certo, <b>3xx</b> vá para outro lugar, <b>4xx</b> o pedido está errado, <b>5xx</b> o servidor falhou.",
        "<b>IP</b> escolhe a máquina; <b>porta</b> escolhe o serviço. Padrões: 80 HTTP, 443 HTTPS, 22 SSH.",
        "Abrir o arquivo por duplo clique (<code>file://</code>) não é publicar: falta um servidor alcançável."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Seu site devolve <b>404</b> depois do deploy. Quem, em geral, deve procurar o erro?", [("a", "O código do servidor, porque 404 é erro de servidor."), ("b", "O caminho ou o nome do arquivo pedido: 404 é da família 4xx, erro de quem pediu."), ("c", "O cabo de rede do servidor.")], "A família 4xx indica pedido que não deu certo (caminho inexistente, por exemplo). Erro de código do servidor é 5xx, como o 500.") + \
        quiz(2, "c", "O que o cabeçalho <code>Location</code> numa resposta <b>301</b> faz?", [("a", "Informa a posição geográfica do servidor."), ("b", "Cifra a conexão."), ("c", "Diz para onde o cliente deve ir agora.")], "301 significa que o recurso mudou. O navegador lê o <code>Location</code> e faz um novo pedido ali. Vimos <code>http://iana.org</code> devolver 301 para <code>https://www.iana.org/</code>.") + \
        quiz(3, "a", "O servidor está ligado, mas o <code>Test-NetConnection</code> à porta 8765 diz <code>False</code>. A causa mais provável?", [("a", "Nenhum programa está ouvindo nessa porta (ou um firewall bloqueia)."), ("b", "O IP está no formato errado."), ("c", "O método HTTP é GET.")], "Porta fechada ou bloqueada. O IP leva até a máquina, mas é a porta que leva ao programa.") + \
        flash([
            ("Quem inicia a conversa HTTP?", "O cliente. O servidor só responde."),
            ("Diferença entre 401 e 403?", "401: falta se identificar (login ou token). 403: você foi identificado, mas não tem permissão."),
            ("O que o IP e o que a porta identificam?", "IP: a máquina na rede. Porta: o serviço dentro dela."),
            ("Portas padrão de HTTP, HTTPS e SSH?", "80, 443 e 22.")]) + \
        fontes("mdn_http", "ibm_net") + \
        ponte("Entendi pedido, resposta, IP e porta. Mas ninguém digita IP: como o nome vira número?", "Com o DNS e o domínio.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
    recap_html = recap("Este é o começo da apostila e ela é <b>complemento</b>: nada foi dado em aula. A pergunta que move tudo é simples: <b>como um arquivo que está no meu computador vira um site que qualquer pessoa abre?</b> Este capítulo monta a base (cliente, servidor, HTTP, IP e portas). Os próximos mostram o caminho até o ar.", "De onde partimos")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 1, "como-a-web-funciona", TITULO, "Como a web funciona: cliente, servidor, HTTP, IP e portas", "Capítulo 1 · Complemento",
            "Quem pede, quem responde, o idioma da conversa e o endereço de entrega, com um simulador de requisição HTTP.",
            chips(body, 40), body, scripts=S)


def cap2():
    corpo = ""
    corpo += secao("nomes", 1, "Domínio, subdomínio e IP",
        "Ninguém lembra de 104.20.23.154. Por que eu digito um nome, e de quem é esse nome?",
        camada("Intuição", "É a agenda do celular. Você toca em \"Maria\" e o aparelho disca o número. O <b>DNS</b> é uma agenda gigante e distribuída da internet: ele guarda a relação entre <b>nomes</b> que humanos leem e <b>números</b> que máquinas usam. (IBM.)") +
        camada("Definição", "<b>Domínio</b> é o nome registrado, como <code>meusite.example</code>. Ele é lido da direita para a esquerda: <code>.example</code> é o domínio de topo (<b>TLD</b>), <code>meusite</code> é o nome que você registra, e na frente podem entrar <b>subdomínios</b> (<code>www</code>, <code>blog</code>, <code>loja</code>). O registro do domínio é alugado de um <b>registrador</b>; apontar o nome para um servidor é outra etapa, feita nos <b>registros DNS</b>. Um IP pode servir vários domínios, e um domínio pode apontar para vários IPs.") +
        '<p class="muted">Nos exemplos desta apostila uso <code>meusite.example</code>, <code>.example</code> é um domínio de topo reservado para exemplos, e os IPs fictícios são de faixas de exemplo. Assim nada aqui aponta para um site de verdade.</p>',
        ponte("Se eu digito meusite.example, quem descobre o IP, e quantas perguntas isso custa?", "Vamos seguir uma consulta do início ao fim."))

    corpo += secao("consulta", 2, "A consulta, passo a passo",
        "O navegador só tem o nome. Quem ele pergunta, e em que ordem?",
        camada("Intuição", "É procurar um telefone pedindo indicação. Você pergunta ao <b>resolvedor</b> (um serviço que faz a pesquisa por você: o do seu provedor ou um público). Se ele não sabe, ele pergunta ao <b>raiz</b> \"quem cuida de .example?\", depois ao servidor do <b>TLD</b> \"quem cuida de meusite.example?\" e por fim ao <b>servidor autoritativo</b> daquele domínio, que é quem tem a resposta oficial. Tudo que aprende, o resolvedor guarda por um tempo, o <b>TTL</b>.") +
        camada("Definição", "<b>Resolvedor recursivo</b>: faz a busca por você. <b>Servidor raiz</b>: sabe quem cuida de cada TLD. <b>Servidor de TLD</b>: sabe quem cuida de cada domínio sob ele. <b>Servidor autoritativo</b>: guarda os registros do domínio. <b>TTL</b> (time to live): quantos segundos a resposta pode ser guardada em cache. (IBM descreve essa cadeia e os tipos de registro.)") +
        '<div class="demo" data-demo="dnsSim"></div>' +
        ex("lendo o que o simulador mostrou", [
            "Consulta fria de <code>meusite.example</code>: <b>5 passos</b> (navegador pergunta ao resolvedor, resolvedor ao raiz, ao TLD, ao autoritativo, e a resposta volta). IP <code>203.0.113.10</code>, TTL de <b>300 s</b>.",
            "A mesma consulta em seguida, com o relógio em 0: <b>2 passos</b>, porque o resolvedor respondeu do cache. Avançando 300 s, o TTL vence e voltam os <b>5 passos</b>.",
            "<code>www.meusite.example</code> é um <b>CNAME</b> (apelido) para <code>meusite.example</code>: <b>6 passos</b>, porque depois de ler o apelido o resolvedor consulta de novo o nome de verdade.",
            "<code>blog.meusite.example</code> é um CNAME para um nome de <b>outra zona</b> (<code>meusite-blog.hospedagem.example</code>): <b>7 passos</b>, pois é preciso achar também quem cuida da outra zona. O cache guarda o <b>menor</b> TTL da cadeia (aqui, 60 s).",
            "<code>loja.meusite.example</code> não tem registro: o autoritativo responde <b>NXDOMAIN</b>, que quer dizer \"esse nome não existe\".",
        ]) +
        '<p class="muted">Simplificações da demo: um só resolvedor com um só cache por nome, sem consulta ao cache dos servidores de TLD e sem IPv6. O DNS de verdade guarda e reaproveita muito mais coisa no caminho.</p>' +
        '<p>E no mundo real? Consultei um domínio público de teste. O <code>nslookup</code> do Windows funciona nos dois shells:</p>' +
        code('''
$ nslookup example.com 1.1.1.1
Servidor:  one.one.one.one
Address:  1.1.1.1

Não é resposta autoritativa:
Nome:    example.com
Addresses:  2606:4700:10::ac42:93f3
	  2606:4700:10::6814:179a
	  172.66.147.243
	  104.20.23.154
$ nslookup -type=NS com. 1.1.1.1          # quem cuida do TLD .com
com	nameserver = a.gtld-servers.net
com	nameserver = b.gtld-servers.net
...
$ nslookup -type=NS example.com 1.1.1.1   # quem é autoritativo do domínio
example.com	nameserver = hera.ns.cloudflare.com
example.com	nameserver = elliott.ns.cloudflare.com
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026, perguntando a um resolvedor público (<code>1.1.1.1</code>) em vez do meu. Os IPs de <code>example.com</code> podem ser outros quando você rodar. "Não é resposta autoritativa" (em inglês, <i>Non-authoritative answer</i>) quer dizer que a resposta <b>não veio direto de um servidor autoritativo</b> do domínio, e sim por um resolvedor. Ele pode ter guardado a resposta de antes ou ter ido buscá-la agora; o aviso não diz qual dos dois.</p>' +
        erro("Dois deslizes. (1) <b>Achar que a mudança de DNS é instantânea.</b> Depois de trocar um registro, quem tinha o antigo no cache continua com ele até o TTL vencer. Na demo você vê isso: dentro dos 300 s, a resposta antiga vale. O que muita gente chama de \"propagação\" é, na prática, caches expirando (essa leitura é minha, não de uma fonte). (2) <b>Testar sempre no mesmo resolvedor</b> e se confundir. Perguntar a um resolvedor diferente (como o <code>1.1.1.1</code> acima) ajuda a ver se o problema é cache local."),
        ponte("Sei como o nome vira IP. Mas que tipos de registro existem, e qual eu uso para apontar o meu domínio para uma hospedagem?", "Com os tipos de registro."))

    corpo += secao("registros", 3, "Os tipos de registro e como apontar o domínio",
        "Quando eu contrato uma hospedagem, ela manda eu \"criar um registro\". Qual, e o que cada tipo faz?",
        camada("Intuição", "Cada tipo é uma linha diferente da agenda: um para \"nome para número\", outro para \"apelido para outro nome\", outro para \"quem recebe o e-mail\". Você escolhe o tipo conforme o que a hospedagem pedir.") +
        tabela(["Tipo", "O que guarda", "Exemplo"], [
            ["A", "nome para IPv4", "<code>meusite.example → 203.0.113.10</code>"],
            ["AAAA", "nome para IPv6", "nome para um endereço longo, de versão 6"],
            ["CNAME", "apelido para outro nome", "<code>www → meusite.example</code>"],
            ["MX", "quem recebe e-mail do domínio", "nome do servidor de e-mail"],
            ["TXT", "texto livre (verificações, políticas)", "provas de que o domínio é seu"],
            ["NS", "quais servidores são autoritativos", "<code>hera.ns.cloudflare.com</code> (do exemplo real)"],
            ["SOA", "dados administrativos da zona", "número de série e tempos"],
        ]) +
        ex("conferindo registros de verdade", [
            "O <code>Resolve-DnsName www.iana.org -Type CNAME</code> devolveu um <b>CNAME</b> para <code>www.iana.org.cdn.cloudflare.net</code>, com TTL de <b>3600</b> s: o site usa um apelido apontando para uma rede de distribuição.",
            "O <code>Resolve-DnsName example.com -Type TXT</code> devolveu dois textos, entre eles <code>v=spf1 -all</code>: um TXT usado para política de e-mail. Só mostro que TXT existe; a leitura dele não é matéria desta apostila.",
            "Regra prática (conhecimento geral, sem fonte lida para isso): o passo \"aponte seu domínio para a hospedagem\" costuma pedir um <b>A</b> (para um IP) ou um <b>CNAME</b> (para um nome da plataforma). Qual dos dois, a documentação de cada hospedagem diz.",
        ]) +
        code('''
PS> Resolve-DnsName www.iana.org -Type CNAME -Server 1.1.1.1 -DnsOnly | Format-Table Name,Type,TTL,NameHost
Name         Type  TTL NameHost
----         ----  --- --------
www.iana.org CNAME 3600 www.iana.org.cdn.cloudflare.net
PS> Resolve-DnsName example.com -Type A -Server 1.1.1.1 -DnsOnly | Format-Table Name,Type,TTL,IPAddress
Name        Type TTL IPAddress
----        ---- --- ---------
example.com    A 230 172.66.147.243
example.com    A 230 104.20.23.154
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026. O TTL de uma resposta em cache muda de uma consulta para outra (em três consultas seguidas vi valores diferentes, 9, 7 e 214, e não confirmei o motivo: pode ser mais de um servidor de cache atrás do mesmo endereço).</p>' +
        erro("Colocar o valor errado ou o tipo errado. Um <b>A</b> precisa de um IP; um <b>CNAME</b> precisa de um <b>nome</b>. Trocar os dois (IP num CNAME, nome num A) faz o registro não funcionar. Depois de salvar, <b>espere o TTL</b> do registro antigo e confira com <code>nslookup nome 1.1.1.1</code> antes de achar que o provedor está com problema. Criar o registro no painel de um registrador é <mark class='hl p'>não testado aqui</mark>, e eu não descrevo telas que não vi."),
        ponte("O nome aponta para o servidor certo. Mas como sei que quem respondeu é mesmo o dono do site, e que ninguém lê a conversa no caminho?", "Com HTTPS, TLS e o certificado."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "DNS traduz <b>nome</b> em <b>número</b> (IP). Domínio é lido da direita para a esquerda: TLD, nome, subdomínios.",
        "Cadeia da consulta: <b>navegador → resolvedor → raiz → TLD → autoritativo</b> e volta. Cache de resposta evita repetir tudo.",
        "<b>TTL</b> é o prazo (em segundos) em que uma resposta pode ficar no cache. Mudou o registro? Quem já tem o antigo só atualiza quando o TTL vence.",
        "<b>A</b>: nome para IPv4. <b>AAAA</b>: IPv6. <b>CNAME</b>: apelido para outro nome. <b>MX</b>: e-mail. <b>TXT</b>: texto. <b>NS</b>: quem é autoritativo.",
        "<b>NXDOMAIN</b> significa que o nome não existe, o que é diferente de \"servidor fora do ar\".",
        "Conferir de fora: <code>nslookup nome 1.1.1.1</code> (Git Bash e PowerShell) ou <code>Resolve-DnsName</code> (PowerShell)."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Você mudou o registro A do seu domínio, e metade dos amigos ainda vê o site antigo. O motivo mais provável?", [("a", "O servidor está com defeito."), ("b", "O registro A só vale para quem usa Windows."), ("c", "O cache dos resolvedores ainda guarda a resposta antiga, até o TTL vencer.")], "O TTL define por quanto tempo a resposta antiga pode ser reaproveitada. Quem consultou antes continua vendo o IP antigo até esse prazo acabar.") + \
        quiz(2, "b", "Para que serve um registro CNAME?", [("a", "Para apontar um nome diretamente para um IP."), ("b", "Para criar um apelido que aponta para outro nome."), ("c", "Para indicar quem recebe o e-mail do domínio.")], "CNAME é apelido de nome. Apontar nome para IP é o A (ou AAAA); e-mail é o MX.") + \
        quiz(3, "a", "Na demo, <code>meusite.example</code> consultada duas vezes seguidas leva 5 passos na primeira e 2 na segunda. Por quê?", [("a", "Na segunda, o resolvedor responde do cache, pois o TTL (300 s) ainda não venceu."), ("b", "Na segunda, o servidor raiz já conhece você."), ("c", "O IPv6 passou a ser usado.")], "O resolvedor guardou a resposta. Avançando o relógio para 300 s, o cache expira e voltam os 5 passos.") + \
        flash([
            ("O que é um resolvedor?", "O serviço que faz a pesquisa de DNS por você e guarda respostas em cache."),
            ("Quem tem a resposta oficial sobre um domínio?", "O servidor autoritativo daquele domínio (os NS dizem quais são)."),
            ("O que é TTL?", "O tempo, em segundos, que uma resposta pode ficar no cache."),
            ("NXDOMAIN quer dizer o quê?", "Que o nome consultado não existe no DNS.")]) + \
        fontes("ibm_dns") + \
        ponte("O nome chegou ao IP certo. Falta saber se a conversa é privada e se o servidor é quem diz ser.", "Com HTTPS, TLS e o certificado.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
    recap_html = recap("No capítulo 1 você viu que um pedido HTTP vai para um IP e uma porta. A pergunta que ficou: ninguém digita um IP, então <b>como um nome vira número?</b> Este capítulo, que também é <b>complemento</b>, responde com o DNS, e mostra uma consulta inteira com cache e TTL.")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 2, "dns-e-dominio", TITULO, "DNS e domínio: uma consulta passo a passo", "Capítulo 2 · Complemento",
            "Como um nome vira um endereço, quem responde em cada degrau, e por que uma mudança de DNS demora a aparecer.",
            chips(body, 40), body, scripts=S2)
