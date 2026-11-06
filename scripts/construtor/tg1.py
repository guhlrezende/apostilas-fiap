from tg_base import *
S1 = ["demos/tg-core.js", "demos/cap-1.js"]
S2 = ["demos/tg-core.js", "demos/cap-2.js"]


def cap1():
    corpo = ""
    # ---------- seção 1: terminal, shell, prompt ----------
    corpo += secao("terminal-shell", 1, "Terminal, shell e prompt",
        "Tudo que eu faço com o mouse tem botão. Então por que gente que trabalha com programação ainda digita comando?",
        camada("Intuição", "Pense num balcão de atendimento. O <b>terminal</b> é o balcão (a janela onde você escreve e lê). O <b>shell</b> é o atendente do outro lado: ele lê o seu pedido, entende e chama o programa certo. Dá para trocar de atendente sem trocar de balcão, e cada atendente fala um dialeto.") +
        camada("Definição", "<b>Terminal</b> é o programa de janela que mostra texto e recebe o que você digita. <b>Shell</b> é o programa que interpreta cada linha e executa. O <b>prompt</b> é o texto que aparece antes do cursor, avisando que o shell está esperando e, quase sempre, em qual pasta você está. Bash e PowerShell são shells diferentes.") +
        '<p>No Windows 11 você vai encontrar dois que importam aqui. O <b>Git Bash</b> é o bash (o shell clássico do Linux) que vem junto com o Git for Windows. O <b>PowerShell</b> é o shell da própria Microsoft. Os dois resolvem os mesmos problemas, de jeitos diferentes:</p>' +
        tabela(["", "Git Bash (bash)", "PowerShell"], [
            ["Nome dos comandos", "curtos: <code>ls</code>, <code>cat</code>, <code>grep</code>", "formato Verbo-Substantivo: <code>Get-ChildItem</code>, <code>Get-Content</code>"],
            ["O que passa pelo pipe", "texto", "objetos"],
            ["Jeito de escrever um caminho", "<code>/c/Users/voce</code>", "<code>C:\\Users\\voce</code>"],
            ["Atalhos curtos", "são os próprios comandos", "<code>ls</code> e <code>cat</code> existem, mas são apelidos (alias) de <code>Get-ChildItem</code> e <code>Get-Content</code>"],
        ]) +
        ex("lendo uma linha de comando", [
            "Digite <code>ls -la projeto</code>. O shell corta a linha nos <b>espaços</b>: saem <b>3 pedaços</b>.",
            "O primeiro é o <b>nome</b> do comando (<code>ls</code>). O segundo, <code>-la</code>, são <b>opções</b>: duas coladas, <code>-l</code> (lista longa) e <code>-a</code> (inclui os escondidos). O terceiro, <code>projeto</code>, é o <b>argumento</b>: sobre o que agir.",
            "Aspas juntam palavras. <code>echo oi    mundo</code> mostra <code>oi mundo</code> (o shell entregou 2 argumentos e o echo separou com 1 espaço). Já <code>echo \"oi    mundo\"</code> mostra <code>oi    mundo</code>: as aspas fazem de tudo isso <b>1 argumento</b>, e os espaços ficam.",
        ]) +
        code('''
$ ls -la projeto     # nome (ls) + opções (-la) + argumento (projeto)
$ echo oi    mundo
oi mundo
$ echo "oi    mundo"
oi    mundo
PS> Get-ChildItem -Force projeto     # o mesmo pedido no PowerShell (-Force inclui os escondidos)
''') +
        erro("Digitar um comando de um shell no outro. <code>Get-ChildItem</code> no Git Bash devolve <code>bash: Get-ChildItem: command not found</code> (o mesmo tipo de aviso que você vê para qualquer comando que o bash não conhece). O caminho inverso também falha: o <code>grep</code> não é comando do PowerShell. No meu computador ele rodou, mas só porque a pasta <code>usr\\bin</code> do Git estava no PATH. Tirei essa pasta do PATH da sessão e o PowerShell respondeu <code>O termo 'grep' não é reconhecido como nome de cmdlet, função, arquivo de script ou programa operável</code>. Não conte com isso. Confira o <b>prompt</b> para saber em que janela você está.") +
        '<p class="muted">Separar terminal de shell é a forma usual de explicar. A IBM descreve o bash e a história dos shells (Bourne, csh, ksh, bash), mas não separa as duas ideias com essas palavras. Sobre PowerShell e Git Bash a IBM não tem nada nas páginas que li: essa parte é minha, testada, mais a documentação da Microsoft.</p>',
        ponte("Já sei dar um comando. Mas o terminal só mostra um cifrão piscando: em qual pasta eu estou, e como ando por elas?", "Com os caminhos e o <code>cd</code>."))

    # ---------- seção 2: caminhos ----------
    corpo += secao("caminhos", 2, "Onde estou: pastas e caminhos",
        "Abri o terminal e ele não mostra pasta nenhuma. Em qual pasta estou, e como me mudo?",
        camada("Intuição", "O terminal sempre está <b>dentro de uma pasta</b>, como o Explorador de Arquivos quando você abre uma. Essa é a <b>pasta atual</b>. Todo comando que você dá, sem dizer o contrário, age ali.") +
        camada("Definição", "<code>pwd</code> mostra a pasta atual. <code>cd</code> muda de pasta. Um <b>caminho absoluto</b> começa na raiz (<code>/c/Users/voce</code>) e vale de qualquer lugar. Um <b>caminho relativo</b> começa na pasta atual (<code>projeto</code>). Três atalhos: <code>.</code> é a pasta atual, <code>..</code> é a pasta de cima e <code>~</code> é a sua pasta pessoal.") +
        tabela(["Tarefa", "Git Bash", "PowerShell"], [
            ["Onde estou?", "<code>pwd</code>", "<code>Get-Location</code> (apelido <code>pwd</code>)"],
            ["Entrar numa pasta", "<code>cd projeto</code>", "<code>Set-Location projeto</code> (apelido <code>cd</code>)"],
            ["Listar", "<code>ls</code>, <code>ls -la</code>", "<code>Get-ChildItem</code>, <code>Get-ChildItem -Force</code>"],
        ]) +
        ex("andando por pastas", [
            "Começo em <code>/c/Users/voce/estudo</code>. <code>pwd</code> confirma.",
            "<code>cd projeto</code> entra numa subpasta. O <code>pwd</code> agora termina em <code>/estudo/projeto</code>.",
            "<code>cd ..</code> sobe um nível (volto para <code>estudo</code>). <code>cd ~</code> vai direto para a pasta pessoal: <code>/c/Users/voce</code>.",
            "No Git Bash, <code>/c/</code> é o disco <code>C:</code>. Por isso <code>/c/Users/voce</code> e <code>C:\\Users\\voce</code> são o mesmo lugar escrito de dois modos.",
        ]) +
        code('''
$ pwd
/c/Users/voce/estudo
$ cd projeto
$ pwd
/c/Users/voce/estudo/projeto
$ cd ..              # sobe um nível
$ cd ~               # vai para a sua pasta pessoal
$ pwd
/c/Users/voce
PS> Set-Location projeto
PS> (Get-Location).Path     # o caminho como texto simples
C:\\Users\\voce\\estudo\\projeto
''') +
        NOTA_SANITIZADA +
        erro("Caminho com espaço sem aspas. Se existe a pasta <code>Meus Documentos</code>, <code>cd Meus Documentos</code> dá <code>cd: too many arguments</code> no bash: o shell entregou 2 argumentos. No PowerShell o erro é parecido: rodei e veio <code>Não é possível localizar um parâmetro posicional que aceite o argumento 'Documentos'</code> (um parâmetro sobrando). O conserto é o mesmo nos dois: <code>cd \"Meus Documentos\"</code>. Aprendi isso rodando: com aspas, o <code>pwd</code> terminou em <code>/Meus Documentos</code>."),
        ponte("Sei andar. Como crio, copio, movo e apago as coisas, e como evito apagar o que não devia?", "Com os comandos de arquivo."))

    # ---------- seção 3: arquivos ----------
    corpo += secao("arquivos", 3, "Criar, copiar, mover e apagar",
        "Sei chegar na pasta. Agora preciso mexer no que tem dentro dela, sem o mouse.",
        camada("Intuição", "São os mesmos gestos do Explorador de Arquivos: criar pasta, copiar, recortar e colar (mover), renomear, apagar e abrir para ler. A diferença é que cada gesto vira uma palavra. <b>Mover e renomear são o mesmo comando</b>: renomear é mover para o mesmo lugar com outro nome.") +
        tabela(["Gesto", "Git Bash", "PowerShell"], [
            ["Criar pasta", "<code>mkdir -p a/b</code>", "<code>New-Item -ItemType Directory -Force a\\b</code>"],
            ["Criar arquivo vazio", "<code>touch notas.txt</code>", "<code>New-Item -ItemType File notas.txt</code>"],
            ["Copiar", "<code>cp origem destino</code>", "<code>Copy-Item origem destino</code> (apelido <code>cp</code>)"],
            ["Mover ou renomear", "<code>mv origem destino</code>", "<code>Move-Item origem destino</code> (apelido <code>mv</code>)"],
            ["Apagar", "<code>rm arq</code>, <code>rm -r pasta</code>", "<code>Remove-Item arq</code>, <code>Remove-Item -Recurse pasta</code> (apelido <code>rm</code>)"],
            ["Ler o arquivo", "<code>cat arq</code>", "<code>Get-Content arq</code>"],
            ["Primeiras / últimas linhas", "<code>head -n 2 arq</code>, <code>tail -n 1 arq</code>", "<code>Get-Content arq -TotalCount 2</code>, <code>Get-Content arq -Tail 1</code>"],
            ["Contar linhas", "<code>wc -l arq</code>", "<code>(Get-Content arq).Count</code>"],
        ]) +
        ex("arrumando a pasta e contando", [
            "<code>mkdir -p projeto/src</code> cria <code>projeto</code> e <code>src</code> de uma vez (o <code>-p</code> cria o caminho inteiro). <code>touch projeto/src/main.py</code> cria um arquivo vazio lá dentro.",
            "<code>cp tarefas.txt projeto/</code> copia. Depois <code>mv projeto/tarefas.txt projeto/lista.txt</code> <b>renomeia</b> a cópia. O <code>ls projeto</code> mostra <code>lista.txt</code> e <code>src</code>.",
            "<code>wc -l vendas.csv</code> responde <b>6</b>: 1 linha de cabeçalho mais 5 linhas de venda. O PowerShell dá o mesmo número com <code>(Get-Content vendas.csv).Count</code>.",
            "<code>rm projeto</code> falha com <code>Is a directory</code>: para pasta é preciso <code>-r</code>. O erro me protegeu de um descuido.",
        ]) +
        code('''
$ mkdir -p projeto/src                  # -p: cria o caminho inteiro
$ touch projeto/src/main.py             # arquivo vazio
$ cp tarefas.txt projeto/               # copia para dentro da pasta
$ mv projeto/tarefas.txt projeto/lista.txt   # renomear = mover com outro nome
$ ls projeto
lista.txt  src
$ wc -l vendas.csv
6 vendas.csv
$ rm projeto
rm: cannot remove 'projeto': Is a directory
$ rm -r projeto/src                     # -r: apaga a pasta e o que tem dentro
PS> (Get-Content vendas.csv).Count      # as 6 linhas
6
PS> Get-Content log.txt -TotalCount 2   # as 2 primeiras linhas
10:01 INFO login ana
10:03 ERRO disco cheio
''') +
        erro("Achar que dá para desfazer. No terminal, apagar costuma ser definitivo: não testei se o <code>rm</code> do Git Bash ou o <code>Remove-Item</code> mandam algo para a Lixeira do Windows, então trate como se não mandassem. Antes de qualquer <code>rm -r</code>, rode <code>ls</code> na pasta e confira o que vai embora. E nunca digite <code>rm -r</code> com um caminho que você não leu duas vezes.") +
        '<h3>E quando eu esqueço o comando?</h3>' +
        '<p>Nos dois shells há ajuda embutida. No Git Bash, <code>ls --help</code> mostra o uso (rodei: a primeira linha é <code>Usage: ls [OPTION]... [FILE]...</code>). O <code>man ls</code>, que as páginas de Linux mencionam, <b>não existe no Git Bash</b>: rodei e veio <code>command not found</code>. No PowerShell, <code>Get-Help Get-ChildItem</code> mostra a sintaxe.</p>' +
        '<p>Agora é a sua vez. Este terminal é um simulador com arquivos falsos (os mesmos <code>tarefas.txt</code>, <code>vendas.csv</code> e <code>log.txt</code> dos exemplos). Ele entende os comandos desta apostila, não o PowerShell.</p>' +
        '<div class="demo" data-demo="terminalSim"></div>',
        ponte("Sei mexer em arquivos um por um. E se eu quiser contar quantas linhas de erro tem em um log, sem abrir o arquivo?", "Com pipes e redirecionamento, no capítulo 2."))

    # ---------- fechamento ----------
    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>Terminal</b> é a janela. <b>Shell</b> interpreta e executa. <b>Prompt</b> mostra que está pronto e, em geral, a pasta atual.",
        "Git Bash (bash) e PowerShell resolvem o mesmo problema com dialetos diferentes. Confira o prompt antes de digitar.",
        "Comando = <b>nome</b> + <b>opções</b> + <b>argumentos</b>, separados por espaço. Aspas juntam em um só argumento.",
        "<code>pwd</code>/<code>Get-Location</code>, <code>cd</code>/<code>Set-Location</code>, <code>ls</code>/<code>Get-ChildItem</code>. Caminho absoluto x relativo; <code>.</code>, <code>..</code> e <code>~</code>.",
        "<code>mkdir</code>, <code>touch</code>, <code>cp</code>, <code>mv</code> (também renomeia), <code>rm</code> (sem volta), <code>cat</code>, <code>head</code>, <code>tail</code>, <code>wc -l</code>.",
        "Caminho com espaço pede aspas. Apagar é definitivo: <code>ls</code> antes de <code>rm -r</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Na linha <code>ls -la projeto</code>, qual é o argumento?", [("a", "<code>ls</code>"), ("b", "<code>projeto</code>"), ("c", "<code>-la</code>")], "<code>ls</code> é o nome do comando, <code>-la</code> são opções e <code>projeto</code> é o argumento: sobre o que o comando age.") + \
        quiz(2, "c", "Você está em <code>/c/Users/voce/estudo/projeto</code> e digita <code>cd ..</code>. Onde fica?", [("a", "Na pasta pessoal, <code>/c/Users/voce</code>."), ("b", "Na raiz do disco."), ("c", "Em <code>/c/Users/voce/estudo</code>.")], "<code>..</code> é a pasta de cima, um nível só. Para ir direto à pasta pessoal seria <code>cd ~</code>.") + \
        quiz(3, "a", "Por que <code>cd Meus Documentos</code> dá erro, e como se conserta?", [("a", "O shell entende 2 argumentos por causa do espaço; use aspas: <code>cd \"Meus Documentos\"</code>."), ("b", "Pastas com maiúscula não funcionam no terminal."), ("c", "O cd só entra em pastas sem acento.")], "O espaço separa argumentos. As aspas fazem do nome inteiro um argumento só.") + \
        flash([
            ("Terminal x shell?", "Terminal é a janela onde você digita e lê. Shell é o programa que interpreta a linha e executa (bash, PowerShell)."),
            ("Como renomear um arquivo pelo terminal?", "Com mv (Move-Item no PowerShell): renomear é mover para o mesmo lugar com outro nome."),
            ("O que fazem ., .. e ~ em um caminho?", ". é a pasta atual, .. é a pasta de cima e ~ é a sua pasta pessoal."),
            ("Por que cuidado com rm -r?", "Porque apaga a pasta inteira, sem perguntar e, na prática, sem volta. Confira com ls antes.")]) + \
        fontes("ibm_1031", "ibm_shells", extra="<p>PowerShell, Git Bash e os atalhos de arquivo: nenhuma página da IBM que li cobre. Esses comandos eu rodei no Git Bash (bash 5.3) e no PowerShell 5.1 de um Windows 11.</p>") + \
        ponte("Sei andar e mexer em arquivos. E se eu quiser contar quantas linhas de erro tem em um log, sem abrir o arquivo?", "Com pipes e redirecionamento.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
    recap_html = recap("Este é o primeiro capítulo. Você não precisa saber nada de linha de comando: basta já ter aberto uma pasta no Explorador de Arquivos. Toda esta apostila é <b>complemento</b> (não foi dado em aula); o que veio de leitura ou de pesquisa está marcado, e cada capítulo termina com as fontes.", "Ponto de partida")
    body = recap_html + AVISO_COMP + corpo
    chapter(PASTA, 1, "terminal-e-shell", TITULO, "Terminal, shell e arquivos", "Capítulo 1 · Complemento",
            "O que é terminal, o que é shell, e como andar e mexer em arquivos com Git Bash e PowerShell lado a lado.",
            chips(body, 35), body, scripts=S1)


def cap2():
    corpo = ""
    corpo += secao("canais", 1, "Três canais: entrada, saída e erro",
        "Mandei o resultado de um comando para um arquivo, e a mensagem de erro apareceu na tela mesmo assim. Por quê?",
        camada("Intuição", "Todo comando tem três tubulações. Por uma entra o que ele lê (a <b>entrada</b>, normalmente o teclado). Por outra sai o resultado (a <b>saída</b>). Por uma terceira sai o aviso de que algo deu errado (o <b>erro</b>). Saída e erro caem na mesma tela, e por isso parecem uma coisa só, mas são canais separados.") +
        camada("Definição", "Os canais têm número: <b>0</b> é a entrada padrão (stdin), <b>1</b> é a saída padrão (stdout) e <b>2</b> é o erro padrão (stderr). O <b>redirecionamento</b> manda um canal para um arquivo: <code>&gt;</code> manda a saída e <b>sobrescreve</b>; <code>&gt;&gt;</code> manda a saída e <b>acrescenta</b>; <code>2&gt;</code> manda só o erro; <code>2&gt;&amp;1</code> junta o erro na saída.") +
        ex("sobrescrever, acrescentar e separar o erro", [
            "<code>echo um &gt; a.txt</code> cria o arquivo com <code>um</code>. Depois <code>echo dois &gt; a.txt</code> <b>apaga o conteúdo</b> e deixa só <code>dois</code>.",
            "<code>echo tres &gt;&gt; a.txt</code> <b>acrescenta</b>. O <code>cat a.txt</code> mostra 2 linhas: <code>dois</code> e <code>tres</code>.",
            "<code>ls nao_existe &gt; out.txt</code>: o <code>out.txt</code> fica com <b>0 bytes</b> e a mensagem de erro aparece na tela. O erro não foi pelo canal 1.",
            "<code>ls nao_existe 2&gt; erros.txt</code> manda o erro para o arquivo. E <code>ls nao_existe &gt; out.txt 2&gt;&amp;1</code> manda os dois para o mesmo lugar. Em todos os casos o código de saída do <code>ls</code> foi <b>2</b>.",
        ]) +
        code('''
$ echo um > a.txt
$ echo dois > a.txt        # sobrescreveu: o "um" sumiu
$ echo tres >> a.txt       # >> acrescenta ao final
$ cat a.txt
dois
tres
$ ls nao_existe > out.txt  # o erro NÃO vai para o arquivo
ls: cannot access 'nao_existe': No such file or directory
$ ls nao_existe 2> erros.txt          # só o erro vai para o arquivo
$ ls nao_existe > out.txt 2>&1        # saída e erro juntos no arquivo
PS> Get-ChildItem nao_existe 2> erros_ps.txt   # no PowerShell, 2> funciona igual
''') +
        '<p>No PowerShell os mesmos operadores existem (<code>&gt;</code>, <code>&gt;&gt;</code>, <code>2&gt;</code>, <code>2&gt;&amp;1</code>). Duas diferenças que vi: o erro é um <b>objeto</b> (a mensagem sai no idioma do Windows, aqui em português) e a codificação do arquivo criado com <code>&gt;</code> muda entre versões do PowerShell. No 5.1 que usei, o arquivo saiu em <b>UTF-16 LE</b> (os bytes começam com <code>255 254</code> e cada letra vem seguida de um byte <code>0</code>), e <b>não</b> em UTF-8. Isso tem consequência prática: o Git não lê um <code>.gitignore</code> gravado assim (o teste está no capítulo 5). Para arquivos de configuração, grave com <code>Set-Content -Encoding ascii</code> (ou <code>utf8</code>), ou crie o arquivo pelo Git Bash, e confira o resultado.</p>' +
        erro("Usar <code>&gt;</code> querendo acrescentar. Ele <b>apaga o arquivo antes</b>, sem avisar. Se o arquivo importa, use <code>&gt;&gt;</code> ou mande para um nome novo. E lembre que o erro <b>não</b> acompanha o <code>&gt;</code>: precisa do <code>2&gt;&amp;1</code>, e <b>depois</b> do <code>&gt;</code>. A ordem importa: rodei <code>ls nao_existe 2&gt;&amp;1 &gt; out.txt</code> e o erro continuou na tela (o <code>out.txt</code> ficou vazio); o certo é <code>ls nao_existe &gt; out.txt 2&gt;&amp;1</code>. O simulador desta apostila faz igual."),
        ponte("Mando a saída para um arquivo. E se eu quiser entregá-la direto a outro comando, sem arquivo no meio?", "Com o pipe."))

    corpo += secao("pipe", 2, "Pipe: uma linha de montagem",
        "Contar quantas linhas de erro existem em um log: preciso achar as linhas, salvar num arquivo e contar o arquivo? Tem jeito mais curto?",
        camada("Intuição", "Uma linha de montagem: cada estação recebe a peça da estação anterior, faz a sua parte e passa adiante. Cada comando é uma estação pequena que faz uma coisa só, e você monta a linha que precisa.") +
        camada("Definição", "O <b>pipe</b> (<code>|</code>) liga a <b>saída</b> de um comando na <b>entrada</b> do próximo, sem arquivo intermediário. Só o canal 1 passa: o erro continua indo para a tela. No PowerShell o pipe também existe, mas leva <b>objetos</b> e não texto.") +
        ex("contando erros com três estações", [
            "<code>cat log.txt | grep ERRO | wc -l</code>. O <code>log.txt</code> tem <b>6</b> linhas.",
            "Estação 1 (<code>cat</code>): entrega as <b>6</b> linhas. Estação 2 (<code>grep ERRO</code>): deixa passar só as que têm a palavra, <b>3</b> linhas (10:03, 10:07 e 10:12).",
            "Estação 3 (<code>wc -l</code>): conta as linhas que chegaram e responde <b>3</b>. Sem arquivo intermediário.",
        ]) +
        code('''
$ cat log.txt | grep ERRO | wc -l      # 6 linhas -> 3 linhas -> o número 3
3
PS> Get-Content log.txt | Select-String ERRO | Measure-Object   # no PowerShell, Count = 3
PS> Get-ChildItem -File | Sort-Object Length -Descending | Select-Object -First 2 Name,Length
Name       Length
----       ------
log.txt       125
vendas.csv     78
''') +
        '<p>Repare no último exemplo: o PowerShell ordenou pela <b>propriedade</b> <code>Length</code> (um número), sem tratar nada como texto. Essa é a diferença de fundo: no bash você interpreta colunas de texto; no PowerShell você pede propriedades de objetos. (Fonte para o pipeline de objetos: Microsoft Learn, about_Pipelines.)</p>' +
        '<p>Acompanhe o caminho dos dados, estação por estação. Os dois últimos exemplos mostram a armadilha do erro que não entra no pipe:</p>' +
        '<div class="demo" data-demo="pipeViz"></div>' +
        erro("Esperar que o erro passe pelo pipe. Em <code>ls nao_existe | grep nao</code>, a mensagem de erro aparece na tela e o <code>grep</code> recebe <b>0 linhas</b>. Com <code>ls nao_existe 2&gt;&amp;1 | grep -c nao</code> o erro entra no pipe e o <code>grep</code> conta <b>1</b> linha. A demo acima mostra as duas versões."),
        ponte("Um pipe liga comandos. Mas que comandos valem a pena ligar?", "As ferramentas de texto."))

    corpo += secao("texto", 3, "grep, sort, uniq, cut, sed e awk",
        "Já sei montar a linha de montagem. Quais são as estações que mais uso?",
        camada("Intuição", "Texto de computador (log, CSV, saída de comando) é uma pilha de linhas. Estas ferramentas filtram linhas (<code>grep</code>), ordenam, contam repetidas, recortam colunas e fazem trocas e contas simples. Juntas, respondem perguntas sem abrir o arquivo.") +
        tabela(["Ferramenta", "Para quê", "Equivalente no PowerShell"], [
            ["<code>grep ERRO log.txt</code>", "só as linhas com o padrão (<code>-i</code> ignora maiúsculas, <code>-c</code> conta, <code>-n</code> numera, <code>-v</code> inverte)", "<code>Select-String -Pattern ERRO log.txt</code> (cuidado: ignora maiúsculas e minúsculas por padrão, como o <code>grep -i</code>; para diferenciar, acrescente <code>-CaseSensitive</code>. Num teste com <code>ERRO</code> e <code>erro</code> no arquivo, deu 2 sem a opção e 1 com ela)"],
            ["<code>sort</code>, <code>sort -rn</code>", "ordena; <code>-r</code> inverte; <code>-n</code> compara como número", "<code>Sort-Object</code>"],
            ["<code>uniq -c</code>", "junta linhas <b>vizinhas</b> iguais e conta", "<code>Group-Object</code>"],
            ["<code>cut -d, -f1</code>", "recorta uma coluna (<code>-d</code> separador, <code>-f</code> campo)", "<code>Import-Csv</code> e a propriedade"],
            ["<code>sed 's/ERRO/ERRO!/'</code>", "troca texto em cada linha", "<code>-replace 'ERRO','ERRO!'</code>"],
            ["<code>awk -F, '{...}'</code>", "separa campos e faz conta, filtro e soma", "<code>Import-Csv</code> + <code>Measure-Object</code>"],
        ]) +
        camada("Definição", "<code>grep</code> procura um padrão e imprime as linhas que casam. <code>sed</code> é um editor de fluxo: o uso mais comum é a troca <code>s/antigo/novo/</code>. <code>awk</code> divide cada linha em campos (<code>$1</code>, <code>$2</code>...) e executa uma ação. Aqui só o básico; cada um é uma linguagem inteira.") +
        ex("qual erro é o mais comum, e quanto vendi", [
            "<code>grep ERRO log.txt | cut -d' ' -f3- | sort | uniq -c | sort -rn</code>. O grep deixa as <b>3</b> linhas de erro; o <code>cut</code> pega do campo 3 em diante (<code>disco cheio</code>, <code>timeout</code>, <code>timeout</code>).",
            "O <code>sort</code> agrupa as iguais lado a lado; o <code>uniq -c</code> conta: <b>2</b> <code>timeout</code> e <b>1</b> <code>disco cheio</code>; o <code>sort -rn</code> põe o maior primeiro. Resposta: <code>timeout</code>, com 2 ocorrências.",
            "Vendas: <code>vendas.csv</code> tem 5 vendas (fora o cabeçalho). O <code>awk</code> multiplica quantidade por preço e soma: 10×2 + 3×15 + 25×1 + 5×2 + 2×15 = 20 + 45 + 25 + 10 + 30 = <b>130</b>.",
            "No PowerShell: <code>Import-Csv vendas.csv | ForEach-Object { [int]$_.qtd * [int]$_.preco } | Measure-Object -Sum</code> também dá <b>130</b>.",
        ]) +
        code('''
$ grep ERRO log.txt | cut -d' ' -f3- | sort | uniq -c | sort -rn
      2 timeout
      1 disco cheio
$ awk -F, 'NR>1 {s+=$2*$3} END {print s}' vendas.csv   # [[NR>1|NR é o número da linha: pula o cabeçalho]]  [[s+=$2*$3|soma quantidade vezes preço]]
130
$ sed 's/ERRO/ERRO!/' log.txt | head -3   # troca só no que passa na tela; o arquivo não muda
10:01 INFO login ana
10:03 ERRO! disco cheio
10:05 INFO login bia
PS> (Select-String -Pattern ERRO log.txt).Count
3
PS> Import-Csv vendas.csv | ForEach-Object { [int]$_.qtd * [int]$_.preco } | Measure-Object -Sum | Select-Object -ExpandProperty Sum
130
''') +
        erro("Dois tropeços que eu mesmo vi rodando. (1) <b>Usar <code>uniq -c</code> sem <code>sort</code> antes.</b> O <code>uniq</code> só junta linhas <i>vizinhas</i>: com as linhas <code>b</code>, <code>a</code>, <code>b</code> ele conta <code>1 b</code>, <code>1 a</code>, <code>1 b</code>; com <code>sort</code> antes, sai <code>1 a</code> e <code>2 b</code>. (2) <b>Aspas duplas no programa do awk.</b> Em <code>awk -F, \"NR>1 {s+=$2*$3} END {print s}\"</code> o bash troca <code>$2</code> e <code>$3</code> por vazio antes do awk ver e o resultado é <code>awk: cmd. line:1: NR>1 {s+=*} END {print s}</code> com <code>syntax error</code>. Use <b>aspas simples</b>: elas não deixam o bash mexer no texto.") +
        '<p class="muted">Nota sobre as fontes: o artigo da IBM sobre manipulação de texto (2012) descreve <code>grep</code>, <code>sed</code>, <code>awk</code>, <code>sort</code>, <code>cut</code> e <code>uniq</code>; as flags usadas aqui eu conferi rodando. No simulador da demo, <code>awk</code> e <code>sed</code> só aceitam as formas simples mostradas, nada de programa completo.</p>',
        ponte("Sei montar comandos em fila. Mas por que um script meu 'não roda', e como o shell sabe onde achar cada programa?", "Com permissões, variáveis de ambiente e PATH."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "Três canais: <b>0</b> entrada, <b>1</b> saída, <b>2</b> erro. Saída e erro caem na mesma tela, mas são separados.",
        "<code>&gt;</code> <b>sobrescreve</b>; <code>&gt;&gt;</code> acrescenta; <code>2&gt;</code> só o erro; <code>2&gt;&amp;1</code> junta o erro na saída.",
        "<b>Pipe</b> (<code>|</code>) liga a saída de um comando na entrada do próximo. O <b>erro não passa</b> sem <code>2&gt;&amp;1</code>.",
        "bash: pipe de <b>texto</b>. PowerShell: pipe de <b>objetos</b> (<code>Where-Object</code>, <code>Sort-Object</code>, <code>Select-Object</code>).",
        "<code>grep</code> filtra, <code>sort</code> ordena, <code>uniq -c</code> conta vizinhas (precisa de <code>sort</code> antes), <code>cut</code> recorta, <code>sed</code> troca, <code>awk</code> faz conta por campo.",
        "Programa do awk e do sed vai entre <b>aspas simples</b>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Você roda <code>echo novo &gt; notas.txt</code> em um arquivo que já tinha 10 linhas. O que sobra?", [("a", "As 10 linhas mais a nova."), ("b", "Nada: o arquivo é apagado."), ("c", "Só a linha <code>novo</code>: o <code>&gt;</code> sobrescreve.")], "O <code>&gt;</code> troca o conteúdo inteiro. Para manter as 10 linhas e acrescentar, o certo seria <code>&gt;&gt;</code>.") + \
        quiz(2, "a", "<code>ls nao_existe | grep nao</code> mostra a mensagem de erro na tela e o grep recebe 0 linhas. Por quê?", [("a", "O pipe só leva a saída padrão; o erro vai direto à tela."), ("b", "O grep ignora linhas de erro."), ("c", "O ls não consegue escrever no pipe.")], "O erro é o canal 2 e o pipe só carrega o canal 1. Com <code>2&gt;&amp;1</code> antes do pipe o erro vira parte da saída.") + \
        quiz(3, "b", "Por que <code>uniq -c</code> costuma vir depois de <code>sort</code>?", [("a", "Porque o uniq só funciona com números."), ("b", "Porque o uniq só junta linhas <b>vizinhas</b> iguais; o sort deixa as iguais lado a lado."), ("c", "Porque o sort apaga as linhas repetidas.")], "Sem ordenar, <code>b a b</code> vira três contagens de 1. Ordenado (<code>a b b</code>), vira <code>1 a</code> e <code>2 b</code>.") + \
        flash([
            ("Qual a diferença entre &gt; e &gt;&gt;?", "&gt; apaga e escreve do zero. &gt;&gt; acrescenta ao final."),
            ("O que é 2&gt;&amp;1?", "Manda o erro (canal 2) para onde está indo a saída (canal 1). Serve para o erro entrar no pipe ou no mesmo arquivo."),
            ("Pipe no bash x pipe no PowerShell?", "No bash, passa texto. No PowerShell, passa objetos com propriedades."),
            ("Para que serve cada: grep, sed, awk?", "grep filtra linhas pelo padrão. sed troca texto. awk separa campos e faz conta por linha.")]) + \
        fontes("ibm_1034", "ibm_unixtext", "ms_pipe") + \
        ponte("Sei montar uma linha de montagem. Por que um script meu 'não roda' e como o shell sabe onde achar cada programa?", "Com permissões, variáveis de ambiente e PATH.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
    recap_html = recap("No capítulo 1 você aprendeu a andar por pastas e a criar, copiar, mover e apagar arquivos. A pergunta que ficou: como combinar comandos pequenos para fazer algo maior, sem abrir arquivo nenhum? Este capítulo, que continua sendo <b>complemento</b>, responde com redirecionamento, pipes e as ferramentas de texto.")
    body = recap_html + AVISO_COMP + corpo
    chapter(PASTA, 2, "pipes-e-texto", TITULO, "Pipes, redirecionamento e ferramentas de texto", "Capítulo 2 · Complemento",
            "Como os comandos se encadeiam: entrada, saída e erro, o pipe e as ferramentas que filtram e contam texto.",
            chips(body, 40), body, scripts=S2)
