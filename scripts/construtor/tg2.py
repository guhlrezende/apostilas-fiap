from tg_base import *
S3 = ["demos/tg-core.js", "demos/cap-3.js"]


def cap3():
    corpo = ""
    corpo += secao("permissoes", 1, "Permissões: quem pode ler, escrever e executar",
        "Um arquivo que 'não abre' e um script que 'não roda' costumam ser a mesma coisa. O que o sistema olha antes de deixar você usar um arquivo?",
        camada("Intuição", "Cada arquivo tem três crachás de acesso: um para o <b>dono</b>, um para o <b>grupo</b> dele e um para <b>todo o resto</b> (outros). Em cada crachá o sistema marca três permissões separadas: <b>ler</b>, <b>escrever</b> e <b>executar</b>.") +
        camada("Definição", "O <code>ls -l</code> mostra isso em 10 caracteres: o primeiro é o tipo (<code>-</code> arquivo, <code>d</code> pasta) e os outros nove são três trios <code>rwx</code> (dono, grupo, outros), com <code>-</code> onde falta a permissão. Em <b>octal</b>, cada letra vale um número: <b>r = 4</b>, <b>w = 2</b>, <b>x = 1</b>, e você soma por trio. O <code>chmod</code> muda isso; o <code>umask</code> define o padrão de arquivos novos.") +
        ex("do número para as letras, e de volta", [
            "<code>755</code> são três dígitos: dono <b>7</b> = 4+2+1 = <code>rwx</code>; grupo <b>5</b> = 4+0+1 = <code>r-x</code>; outros <b>5</b> = <code>r-x</code>. Fica <code>rwxr-xr-x</code>: o dono faz tudo, os outros leem e executam. É o normal de script e de pasta.",
            "<code>644</code>: dono <b>6</b> = 4+2 = <code>rw-</code>; grupo e outros <b>4</b> = <code>r--</code>. Fica <code>rw-r--r--</code>: o normal de um arquivo de texto.",
            "<code>600</code> = <code>rw-------</code>: só o dono lê e escreve. É o que se espera de um arquivo privado.",
            "O <code>umask</code> do meu Git Bash mostrou <code>0022</code>. Como regra de bolso, um arquivo novo começa em 666 e o umask tira 022: 666 − 022 = <b>644</b>. Conferi: todo arquivo que criei saiu como <code>-rw-r--r--</code>.",
        ]) +
        '<p>Brinque com a calculadora. Marque as caixas e veja o número; digite um número e veja as caixas:</p>' +
        '<div class="demo" data-demo="chmodCalc"></div>' +
        code('''
$ ls -l log.txt
-rw-r--r-- 1 voce 197609 125 Nov  6 14:00 log.txt      # tipo(-) dono(rw-) grupo(r--) outros(r--)
$ umask
0022
$ chmod 755 script.sh     # dono rwx, grupo e outros r-x   [[(não testado aqui, num Linux de verdade)|No Git Bash do Windows o chmod não muda estas permissões, como mostrei]]
$ chmod +x script.sh      # liga o x para todos
$ chmod u+x script.sh     # liga o x só para o dono (u = user)
PS> icacls log.txt        # no Windows as permissões são ACLs, outro modelo
''') +
        naotestado("O <code>chmod</code> e as permissões <code>rwx</code> são conceito de Linux (as páginas da IBM tratam de Linux). Eu só tinha o Git Bash no Windows, e lá o resultado engana: rodei <code>chmod 600 seg.txt</code> e a listagem continuou <code>-rw-r--r--</code> (644). Um arquivo que começa com <code>#!</code> (um script) já aparece como <code>-rwxr-xr-x</code> sem eu ter dado <code>chmod +x</code>. Ou seja, o bit <code>x</code> no Windows não funciona como no Linux. No PowerShell o equivalente de verdade seria <code>icacls</code>, que usa ACLs; eu só rodei <code>icacls log.txt</code> para ver que existe, não mexi em permissão.") +
        erro("Dar <code>chmod 777</code> para 'resolver' um erro de permissão. Isso libera escrita para qualquer usuário. O certo é descobrir <i>quem</i> precisa de <i>qual</i> permissão e dar só isso (a calculadora acima avisa quando você marca tudo)."),
        ponte("Sei o que são permissões. Mas por que o <code>git</code> roda de qualquer pasta e o meu script só com <code>./</code> na frente?", "Com variáveis de ambiente e o PATH."))

    corpo += secao("ambiente", 2, "Variáveis de ambiente e PATH",
        "Digito <code>git</code> em qualquer pasta e funciona. Digito o nome do meu script e dá erro. Como o shell decide onde procurar?",
        camada("Intuição", "O shell tem uma memória de post-its: nomes com valores. São as <b>variáveis</b>. Uma delas, o <b>PATH</b>, é uma lista de pastas. Quando você digita só um nome, o shell abre cada pasta da lista, na ordem, procurando um programa com esse nome. Se não achar, desiste.") +
        camada("Definição", "Uma <b>variável de ambiente</b> é um nome com valor que o shell guarda. Só os programas que ele inicia (os 'filhos') enxergam a variável se ela for <b>exportada</b>. O <b>PATH</b> é a variável com as pastas de busca, separadas por <code>:</code> no bash e por <code>;</code> no Windows. No PowerShell lê-se e escreve-se com <code>$env:NOME</code>.") +
        ex("o filho só enxerga o que foi exportado", [
            "<code>X=um</code> cria a variável no shell. Quando um programa filho tenta lê-la (<code>bash -c 'echo \"filho:[$X]\"'</code>), vê <code>filho:[]</code>: <b>vazio</b>.",
            "Depois de <code>export X</code>, o mesmo comando mostra <code>filho:[um]</code>. O <code>export</code> é o que repassa a variável aos filhos.",
            "<code>which git</code> mostrou <code>/ucrt64/bin/git</code> no Git Bash, e <code>(Get-Command git).Source</code> mostrou <code>C:\\Program Files\\Git\\cmd\\git.exe</code> no PowerShell. Cada shell tem a sua lista de pastas e achou o <code>git</code> em um lugar diferente. Conferi abrindo o <code>bash.exe</code> da pasta do Git for Windows: esse <code>/ucrt64</code> existe dentro da instalação (<code>ucrt64\\bin\\git.exe</code>) e não há pasta <code>mingw64</code>. O prefixo depende da versão do Git for Windows (versões mais antigas costumam mostrar <code>/mingw64/bin/git</code>; isso eu não testei), então o caminho no seu computador pode ser outro.",
        ]) +
        code('''
$ X=um
$ bash -c 'echo "filho:[$X]"'    # o programa filho não vê a variável
filho:[]
$ export X
$ bash -c 'echo "filho:[$X]"'
filho:[um]
$ which git                       # onde o shell achou o programa (o caminho varia com a versão do Git)
/ucrt64/bin/git
$ type cd                         # nem todo comando é programa: o cd é do próprio shell
cd is a shell builtin
$ N=Ana; echo "oi $N"; echo 'oi $N'     # aspas duplas expandem a variável; simples não
oi Ana
oi $N
PS> $env:MINHA = 'valor'          # vale para esta sessão e para os filhos
PS> (Get-Command git).Source
C:\\Program Files\\Git\\cmd\\git.exe
PS> [Environment]::SetEnvironmentVariable('TG_X','1','Process')   # escopo Process: só nesta sessão
''') +
        '<p>No PowerShell a variável tem três escopos: <b>Process</b> (a sessão atual), <b>User</b> e <b>Machine</b> (Microsoft Learn, about_Environment_Variables). Eu rodei o escopo Process e conferi que um <code>powershell</code> filho enxerga <code>$env:MINHA</code>.</p>' +
        naotestado("Gravar uma variável <b>permanente</b>. No PowerShell seria <code>[Environment]::SetEnvironmentVariable('NOME','valor','User')</code>; no bash, colocar o <code>export</code> no arquivo de perfil, como o <code>~/.bashrc</code> (a IBM, tutorial 105.1, trata disso). Não rodei nenhum dos dois: o primeiro mexe no registro do seu usuário e eu não quis alterar o computador por causa de um teste.") +
        erro("Achar que o valor dura para sempre. <code>export X=1</code> e <code>$env:X = '1'</code> valem só enquanto aquela janela existir. Fechou o terminal, perdeu. Outro erro clássico: <b>colocar segredo (senha, chave de API) em variável e depois imprimir ou salvar o ambiente</b>. Variáveis ajudam a não deixar segredo no código, mas continuam sendo texto que quem acessa a sessão consegue ver."),
        ponte("Sei onde o shell procura programas. Como guardo uma sequência de comandos num arquivo e rodo quando quiser?", "Com scripts."))

    corpo += secao("scripts", 3, "Scripts: comandos guardados em um arquivo",
        "Repeti os mesmos cinco comandos pela terceira vez no mesmo dia. Dá para escrever uma vez só?",
        camada("Intuição", "Um script é uma receita: os comandos que você digitaria, na ordem, num arquivo. O shell lê o arquivo e executa linha por linha. A vantagem é repetir sem errar e poder usar decisões (<code>if</code>) e repetições (<code>for</code>).") +
        camada("Definição", "A primeira linha de um script bash costuma ser o <b>shebang</b> (<code>#!/bin/bash</code>), que diz qual shell executa. Cada comando termina com um <b>código de saída</b>: <b>0</b> é sucesso, qualquer outro número é falha. O código do último comando fica na variável <code>$?</code>. Para rodar pelo caminho, o arquivo precisa de permissão de execução.") +
        '<p class="muted">Base: tutorial 105.2 da IBM (scripts), mais os testes que fiz.</p>' +
        code('''
#!/bin/bash
# saudacao.sh  (os trechos sublinhados explicam)
nome="${1:-mundo}"            # [[$1|primeiro argumento que você passa ao script]] ; se vier vazio, usa "mundo"
for i in 1 2 3; do           # repete 3 vezes
  echo "$i: oi, $nome"
done
if [ "$nome" = "erro" ]; then exit 1; fi    # [[exit 1|sai avisando que falhou]]
exit 0
''') +
        ex("rodando e lendo o código de saída", [
            "<code>./saudacao.sh Ana</code> imprime 3 linhas (<code>1: oi, Ana</code>, <code>2: oi, Ana</code>, <code>3: oi, Ana</code>) e o <code>echo $?</code> logo depois mostra <b>0</b>.",
            "<code>bash saudacao.sh erro</code> imprime as mesmas 3 linhas, mas termina com <code>exit 1</code>: o <code>$?</code> vale <b>1</b>.",
            "<code>saudacao.sh</code> sem <code>./</code> falha com <code>command not found</code> e o <code>$?</code> vale <b>127</b>: a pasta atual não está no PATH, então o shell não procurou ali.",
        ]) +
        code('''
$ ./saudacao.sh Ana
1: oi, Ana
2: oi, Ana
3: oi, Ana
$ echo $?
0
$ bash saudacao.sh erro > /dev/null; echo $?
1
$ saudacao.sh
bash: saudacao.sh: command not found
$ echo $?
127
PS> .\\saud.ps1 Ana        # o equivalente em PowerShell: .\\ na frente também é obrigatório
PS> powershell -NoProfile -File .\\saud.ps1 erro; $LASTEXITCODE
1
''') +
        '<p>O script do PowerShell que usei (<code>saud.ps1</code>) é este. Repare na chave em <code>${i}</code>:</p>' +
        code('''
param($nome = "mundo")                         # [[param|declara os argumentos do script]]
foreach ($i in 1..3) { "${i}: oi, $nome" }     # [[${i}|as chaves evitam que o PowerShell leia "i:" como nome de unidade]]
if ($nome -eq "erro") { exit 1 }
exit 0
''') +
        erro("Três armadilhas reais. (1) <b>Esquecer o <code>./</code></b>: o script não está no PATH (código 127, acima). (2) <b>Escrever <code>\"$i: oi\"</code> no PowerShell.</b> Rodei assim e deu <code>Referência de variável inválida. ':' não era seguido de um caractere de nome de variável válido</code>: o PowerShell leu <code>$i:</code> como se fosse uma unidade (como <code>C:</code>). O conserto é <code>\"${i}: oi\"</code> ou <code>\"$($i): oi\"</code>. (3) <b>Confiar no <code>chmod +x</code> do Git Bash:</b> no Windows ele não é a fonte da verdade (veja o aviso da seção 1); rodar com <code>bash saudacao.sh</code> sempre funciona.") +
        naotestado("A <b>política de execução</b> do PowerShell (<code>Set-ExecutionPolicy</code>), que pode bloquear scripts <code>.ps1</code> em outros computadores. No ambiente em que testei ela estava em <code>Bypass</code>, então não vi o bloqueio. Se você receber um erro de 'execução de scripts desabilitada', procure a documentação da Microsoft antes de mudar a política: ela é uma configuração de segurança.") +
        '<details class="cola"><summary>Complemento do complemento: if, for e case (IBM 105.2)</summary><div class="in-body"><p>A IBM apresenta as estruturas de controle do shell: <code>if ... then ... fi</code> para decidir, <code>for ... do ... done</code> e <code>while</code> para repetir, <code>case</code> para várias opções, e a <b>substituição de comando</b> (<code>$(comando)</code>, que usa a saída de um comando como valor). Usei <code>if</code> e <code>for</code> no script acima e rodei; <code>while</code>, <code>case</code> e <code>$(...)</code> li, mas não testei.</p></div></details>',
        ponte("Meus scripts rodam. E quando o programa não termina, ou está em outra máquina? Quem vê e encerra processos, e como eu entro num servidor?", "Com processos, curl e SSH."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "Permissão = dono, grupo e outros × <b>r</b> (4), <b>w</b> (2), <b>x</b> (1). <code>755</code> = <code>rwxr-xr-x</code>; <code>644</code> = <code>rw-r--r--</code>; <code>600</code> = <code>rw-------</code>.",
        "Evite <code>chmod 777</code>. No Git Bash do Windows o <code>chmod</code> e o bit <code>x</code> <b>não se comportam como no Linux</b>.",
        "Variável de ambiente: o filho só vê o que foi <code>export</code>ado. PowerShell: <code>$env:NOME</code>. Dura só a sessão (Process).",
        "<b>PATH</b> é a lista de pastas onde o shell procura o programa. Fora do PATH, use caminho: <code>./script.sh</code> ou <code>.\\script.ps1</code>.",
        "Script: shebang, comandos, <code>exit</code>. Código <b>0</b> = sucesso, outro = falha, em <code>$?</code>. Comando não achado = <b>127</b>.",
        "PowerShell: <code>\"${i}: texto\"</code> (com chaves), senão <code>$i:</code> vira unidade."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Qual é a notação simbólica de <code>chmod 640</code>?", [("a", "<code>rw-r-----</code>"), ("b", "<code>rwxr-----</code>"), ("c", "<code>rw-rw----</code>")], "6 = 4+2 = <code>rw-</code> (dono); 4 = <code>r--</code> (grupo); 0 = <code>---</code> (outros). Dá <code>rw-r-----</code>.") + \
        quiz(2, "c", "Você roda <code>X=um</code> (sem export) e depois um programa filho tenta ler <code>$X</code>. O que ele vê?", [("a", "<code>um</code>"), ("b", "Um erro que trava o programa."), ("c", "Vazio: só o que foi exportado chega ao filho.")], "Sem <code>export</code>, a variável é só do shell. Depois do <code>export X</code>, o filho enxerga <code>um</code>.") + \
        quiz(3, "b", "<code>meu_script.sh</code> está na pasta atual, mas digitar só o nome dá <code>command not found</code> (código 127). Por quê?", [("a", "Porque o arquivo está corrompido."), ("b", "Porque a pasta atual não está no PATH; é preciso <code>./meu_script.sh</code>."), ("c", "Porque scripts só rodam como administrador.")], "O shell só procura nas pastas do PATH. Com <code>./</code> você dá o caminho e ele não precisa procurar.") + \
        flash([
            ("Como converter 7, 5 e 5 em letras?", "7 = rwx, 5 = r-x, 5 = r-x. Soma: r vale 4, w vale 2, x vale 1."),
            ("O que é o PATH?", "Lista de pastas onde o shell procura o programa quando você digita só o nome."),
            ("Para que serve o código de saída?", "Dizer se o comando deu certo: 0 é sucesso, qualquer outro número é falha. Fica em $?"),
            ("Por que o PowerShell reclama de &quot;$i: texto&quot;?", "Porque lê $i: como nome de unidade (como C:). Use ${i}: dentro das aspas.")]) + \
        fontes("ibm_1045", "ibm_1051", "ibm_1052", "ms_env") + \
        ponte("Meus scripts rodam. E quando o programa não termina, ou está em outra máquina? Quem vê e encerra processos, e como eu entro num servidor?", "Com processos, curl e SSH.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
    body = recap("O capítulo 2 ensinou a ligar comandos com pipes. Uma pergunta ficou no ar: por que um script meu 'não roda' e como o shell sabe onde achar cada programa? Este capítulo, <b>complemento</b> como o resto, responde com permissões, variáveis de ambiente, PATH e o primeiro script.") + AVISO_COMP + corpo
    chapter(PASTA, 3, "permissoes-ambiente-scripts", TITULO, "Permissões, variáveis de ambiente, PATH e scripts", "Capítulo 3 · Complemento",
            "Quem pode fazer o quê com um arquivo, onde o shell procura programas e como guardar comandos em um script.",
            chips(body, 40), body, scripts=S3)


def cap4():
    corpo = ""
    corpo += secao("processos", 1, "Processos: o que está rodando",
        "Rodei um comando que não termina e o terminal ficou preso. Como vejo o que está rodando e como encerro?",
        camada("Intuição", "Cada programa em execução é um <b>processo</b>, como um funcionário com crachá numerado. O número é o <b>PID</b>. Você pode deixar um processo trabalhando 'ao fundo' e continuar usando o terminal, ou encerrar um que travou, chamando-o pelo número.") +
        camada("Definição", "No bash, <code>comando &amp;</code> manda o processo para o <b>fundo</b>. <code>jobs</code> lista os que você lançou, <code>ps</code> lista processos, e <code>kill PID</code> pede para encerrar. <code>Ctrl+C</code> interrompe o que está na frente. No PowerShell: <code>Get-Process</code> lista, <code>Start-Process</code> inicia e <code>Stop-Process -Id PID</code> encerra.") +
        ex("um processo que vai ao fundo e é encerrado", [
            "<code>sleep 300 &amp;</code> começa uma espera de 300 segundos <b>ao fundo</b>. O terminal volta na hora, e o shell guarda o PID do último processo na variável <code>$!</code> (o número muda a cada vez, por isso não o mostro).",
            "<code>jobs</code> responde <code>[1]+  Running  sleep 300 &amp;</code>: o trabalho número 1 está rodando.",
            "<code>kill $!</code> encerra esse processo. Um segundo <code>jobs</code> mostra <code>[1]+  Terminated  sleep 300</code>. No PowerShell fiz o análogo: iniciei um <code>powershell</code> escondido com <code>Start-Process -PassThru</code>, confirmei com <code>Get-Process -Id</code> que existia, encerrei com <code>Stop-Process -Id</code> e conferi que sumiu.",
            "Cuidado com <b>qual</b> número usar. No Git Bash, o <code>ps</code> mostra duas colunas: <code>PID</code> (o número do próprio bash, o mesmo de <code>$!</code> e do <code>kill</code>) e <code>WINPID</code> (o número do Windows). Rodei os dois lados: o <code>sleep</code> tinha PID 2639 e WINPID 4548; o <code>Get-Process -Id 4548</code> achou o processo e com o 2639 não achou nada. Então o <code>Stop-Process -Id</code> pede o <b>WINPID</b>, e o <code>kill</code> do bash pede o <b>PID</b>. Os números mudam a cada execução.",
        ]) +
        code('''
$ sleep 300 &            # [[&|manda para o fundo e libera o terminal]]
$ jobs
[1]+  Running                    sleep 300 &
$ ps | grep sleep          # [[PID e WINPID|a 1ª coluna é o número do bash; a 4ª (WINPID) é o do Windows]]
     2639    2638    2638       4548  ?         197609 14:16:07 /usr/bin/sleep
PS> Get-Process -Id 4548     # o WINPID: o PowerShell enxerga o sleep
$ kill $!                # [[$!|PID do último processo lançado ao fundo]]
$ jobs
[1]+  Terminated                 sleep 300
PS> $p = Start-Process powershell -ArgumentList '-NoProfile','-Command','Start-Sleep 300' -PassThru -WindowStyle Hidden
PS> Get-Process -Id $p.Id      # confirma que está vivo
PS> Stop-Process -Id $p.Id     # encerra só este processo, pelo número
''') +
        erro("Encerrar o processo errado. Antes de qualquer <code>kill</code> ou <code>Stop-Process</code>, <b>confira o PID</b> (<code>ps</code>, <code>Get-Process</code>). Encerrar pelo nome pode pegar mais de um processo; use o número. Em um computador compartilhado ou de trabalho, não encerre o que você não iniciou.") +
        '<p class="muted">A IBM não cobriu processos nas páginas que li: esta seção é só o que rodei, mais o conceito geral. Não testei <code>top</code>, <code>htop</code> nem <code>Ctrl+C</code> na prática.</p>',
        ponte("Sei ver e encerrar processos locais. E falar com um site ou com uma máquina distante, como faço?", "Com o curl e o SSH."))

    corpo += secao("curl", 2, "curl: um navegador sem janela",
        "Quero saber se um site responde, sem abrir o navegador. E, mais adiante, baixar algo por script.",
        camada("Intuição", "O <code>curl</code> faz o que o navegador faz (pede uma página a um servidor), mas devolve o resultado como texto no terminal. É ótimo para testar se algo está no ar e para automatizar.") +
        camada("Definição", "<code>curl URL</code> imprime a resposta. Opções úteis: <code>-s</code> (silencioso, sem barra de progresso), <code>-o arquivo</code> (guarda em arquivo; <code>/dev/null</code> descarta), <code>-w</code> (imprime um dado da resposta, como o código HTTP) e <code>-I</code> (só os cabeçalhos). O código <b>200</b> quer dizer 'deu certo'.") +
        ex("o site responde?", [
            "<code>curl -s -o /dev/null -w \"%{http_code}\\n\" https://example.com</code>: baixa a página, joga o corpo fora e imprime só o código HTTP. A resposta foi <b>200</b>.",
            "<code>curl -sI https://example.com</code> mostra os cabeçalhos; a primeira linha foi <code>HTTP/1.1 200 OK</code>. Essa linha depende do curl e do servidor: o meu curl não tinha suporte a HTTP/2 (conferi, a opção <code>--http2</code> foi recusada), e um curl com HTTP/2 mostraria <code>HTTP/2 200</code>. Por isso, em script, confira o código com o <code>-w</code> do exemplo anterior, não o texto da primeira linha.",
            "No PowerShell 5.1: <code>(Invoke-WebRequest -UseBasicParsing https://example.com).StatusCode</code> também deu <b>200</b>, e <code>curl.exe -s -o NUL -w \"%{http_code}\" https://example.com</code> deu <b>200</b> (o <code>.exe</code> é obrigatório, veja abaixo).",
        ]) +
        code('''
$ curl -s -o /dev/null -w "%{http_code}\\n" https://example.com
200
$ curl -sI https://example.com | head -1
HTTP/1.1 200 OK            # no meu curl; com HTTP/2 seria HTTP/2 200
PS> (Invoke-WebRequest -UseBasicParsing https://example.com).StatusCode
200
PS> curl.exe -s -o NUL -w "%{http_code}" https://example.com    # com .exe: é o curl de verdade
200
''') +
        erro("Digitar <code>curl</code> no PowerShell 5.1 achando que é o curl. Lá, <code>curl</code> é um <b>apelido</b> (alias) de <code>Invoke-WebRequest</code>: confirmei com <code>(Get-Command curl).CommandType</code>, que devolveu <code>Alias</code>. As opções <code>-s</code>, <code>-o</code> e <code>-w</code> não valem. Para o curl de verdade, escreva <code>curl.exe</code>. Outro cuidado: nunca coloque token ou senha na URL de um comando; ela pode ficar gravada no histórico do terminal.") +
        '<p class="muted">A IBM não tem página de curl nas fontes que li. Os exemplos usam <code>example.com</code>, domínio reservado para exemplos.</p>',
        ponte("Falar com um site é fácil. E entrar em outra máquina, sem que ninguém na rede veja minha senha?", "Com o SSH."))

    corpo += secao("ssh", 3, "SSH: entrar em outra máquina com um par de chaves",
        "Preciso trabalhar num servidor que está em outro lugar. Mandar senha pela internet parece ruim. Qual é a alternativa?",
        camada("Intuição", "Um cadeado e uma chave. Você fabrica os dois juntos. O <b>cadeado</b> (chave <b>pública</b>) você pode entregar a qualquer um e instalar no servidor. A <b>chave</b> (chave <b>privada</b>) nunca sai de você. Quem tem o cadeado consegue conferir que você tem a chave certa, sem a chave viajar pela rede.") +
        camada("Definição", "<b>SSH</b> é um protocolo para acessar outra máquina pela rede com canal criptografado. A autenticação pode ser por senha ou por <b>par de chaves</b>: a pública vai para o arquivo <code>authorized_keys</code> do servidor; a privada fica no seu computador, de preferência protegida por uma <b>passphrase</b>. O <code>ssh-agent</code> guarda a chave destravada na memória para você não digitar a passphrase toda hora. (IBM Developer, artigo de 2014.)") +
        ex("gerando um par de chaves de teste", [
            "<code>ssh -V</code> mostra o cliente instalado. No Git Bash deu <code>OpenSSH_10.6p1</code>. No PowerShell depende do PATH: com a pasta <code>usr\\bin</code> do Git na frente (o meu caso) saiu o mesmo <code>OpenSSH_10.6p1</code>, e o cliente do próprio Windows (<code>C:\\Windows\\System32\\OpenSSH</code>) deu <code>OpenSSH_for_Windows_9.5p2</code>. Podem existir <b>dois</b> clientes diferentes no mesmo computador.",
            "Gerei um par numa <b>pasta temporária</b>, com <code>-N \"\"</code> (sem passphrase, só porque era descartável) e depois apaguei os dois arquivos. Saíram <b>2 arquivos</b>: <code>chave_teste</code> (a privada) e <code>chave_teste.pub</code> (a pública). Rodei de novo no Git Bash e no <code>ssh-keygen</code> do Windows, sempre numa pasta temporária (nunca na sua <code>~/.ssh</code>, para não misturar com chaves de verdade). Uma pegadinha do PowerShell 5.1: o <code>-N \"\"</code> some no caminho até o programa e vem <code>Too many arguments</code>; escreva <code>-N '\"\"'</code>.",
            "O artigo da IBM usa DSA como exemplo; eu usei <code>ed25519</code>, que funcionou aqui. Para uso de verdade, <b>use passphrase</b> e confira qual tipo de chave o servidor aceita.",
        ]) +
        code('''
$ ssh -V
OpenSSH_10.6p1, OpenSSL 3.5.9 29 Sep 2026
$ ssh-keygen -t ed25519 -f chave_teste -N "" -C "teste-descartavel"    # [[-N ""|passphrase vazia, só para teste. No uso real, defina uma]]
Generating public/private ed25519 key pair.
Your identification has been saved in chave_teste
Your public key has been saved in chave_teste.pub
The key fingerprint is:
SHA256:<omitido> teste-descartavel    # a impressão digital real foi omitida de propósito
The key's randomart image is:
(o desenho de randomart que vem aqui foi omitido)
$ ls
chave_teste  chave_teste.pub
PS> ssh-keygen -t ed25519 -f chave_ps -N '""' -C teste    # no PowerShell 5.1, as aspas vazias precisam deste jeito
''') +
        '<p>O caminho até entrar num servidor, em passos. Esta parte é conceito (IBM, 2014), <b>não testada aqui</b>:</p>' +
        '''<div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Você gera o par</b><p><code>ssh-keygen</code> cria a chave privada e a pública. Defina uma passphrase.</p></div>
      <div class="st"><b>2. A pública vai para o servidor</b><p>O conteúdo da <code>.pub</code> entra no <code>authorized_keys</code> do usuário no servidor. (Há o <code>ssh-copy-id</code> para isso; <mark class="hl p">não testado aqui</mark>.)</p></div>
      <div class="st"><b>3. Você se conecta</b><p><code>ssh usuario@servidor</code>, em que <i>usuario</i> e <i>servidor</i> são os dados reais da máquina que você tem permissão para acessar.</p></div>
      <div class="st"><b>4. O servidor confere</b><p>Ele usa a sua chave pública para checar que você tem a privada correspondente. A privada nunca viaja pela rede.</p></div>
      <div class="st"><b>5. Você entra</b><p>Sem senha trafegando. Se a privada tiver passphrase, é ela que você digita (ou o <code>ssh-agent</code> lembra).</p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>''' +
        naotestado("Entrar em um servidor de verdade (não tenho um servidor de teste), <code>ssh-copy-id</code>, <code>authorized_keys</code>, <code>ssh-agent</code> e a instalação do cliente OpenSSH no Windows 11 pelo <code>Add-WindowsCapability</code> (Microsoft Learn). No meu computador o cliente já estava instalado, então não precisei instalar. O servidor OpenSSH só é necessário se você quiser <i>receber</i> conexões.") +
        erro("Compartilhar ou apagar sem backup a chave <b>privada</b>. A pública pode ir para o servidor, para o GitHub, para quem precisar. A <b>privada nunca</b>: quem a tem entra como você. E se você perder a única cópia, perde o acesso. Nunca cole uma chave privada em chat, e-mail ou repositório.") +
        '<p class="muted">Nesta apostila não há credencial real em lugar nenhum: a chave que gerei era descartável, ficou numa pasta temporária e foi apagada.</p>',
        ponte("Agora que domino o terminal, como guardo o histórico do que faço nos arquivos, e volto atrás quando erro?", "Com o Git."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>Processo</b> = programa rodando, com um <b>PID</b>. <code>&amp;</code> manda ao fundo; <code>jobs</code>, <code>ps</code> e <code>kill PID</code> no bash; <code>Get-Process</code> e <code>Stop-Process -Id</code> no PowerShell.",
        "Confira o PID antes de encerrar. Não encerre o que você não iniciou.",
        "<b>curl</b> pede uma URL e mostra a resposta. <code>-s</code> silencia, <code>-o</code> guarda, <code>-w</code> formata, <code>-I</code> só cabeçalhos. Código 200 = deu certo.",
        "No PowerShell 5.1, <code>curl</code> é <b>alias</b> de <code>Invoke-WebRequest</code>. Use <code>curl.exe</code>.",
        "<b>SSH</b>: par de chaves. A <b>pública</b> vai ao servidor, a <b>privada</b> nunca sai de você (use passphrase).",
        "Nada de credencial em URL, chat ou repositório."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Você lança <code>sleep 300 &amp;</code>. Para que serve o <code>&amp;</code>?", [("a", "Para encerrar o comando depois de 300 segundos."), ("b", "Para rodar ao fundo e liberar o terminal."), ("c", "Para juntar dois comandos num só.")], "O <code>&amp;</code> no fim manda o processo para o fundo. O <code>jobs</code> lista os que estão lá.") + \
        quiz(2, "a", "No PowerShell 5.1 você digita <code>curl -s https://example.com</code> e dá erro de parâmetro. Qual a causa?", [("a", "<code>curl</code> é um alias de <code>Invoke-WebRequest</code>; o curl de verdade é <code>curl.exe</code>."), ("b", "O PowerShell não acessa a internet."), ("c", "O <code>-s</code> só existe no Linux.")], "O alias tem outras opções. Com <code>curl.exe</code> as opções do curl funcionam.") + \
        quiz(3, "c", "Qual das duas chaves do SSH você pode entregar a um servidor ou ao GitHub?", [("a", "A privada, porque é ela que prova quem você é."), ("b", "Nenhuma das duas."), ("c", "A pública. A privada fica só com você.")], "A pública é o cadeado: pode ser distribuída. A privada é a chave: quem a tem entra como você.") + \
        flash([
            ("O que é um PID?", "O número que identifica um processo em execução. É com ele que você encerra o processo certo."),
            ("O que o código HTTP 200 significa?", "Que o servidor respondeu com sucesso."),
            ("Por que 'curl' no PowerShell 5.1 não é o curl?", "Porque lá é um apelido de Invoke-WebRequest. O de verdade é curl.exe."),
            ("Chave pública x privada no SSH?", "A pública vai para o servidor (authorized_keys). A privada fica com você e nunca é compartilhada.")]) + \
        fontes("ibm_ssh", "ms_ssh", extra="<p>Processos e curl: nenhuma página da IBM que li cobre. O que está aqui foi rodado por mim no Git Bash e no PowerShell 5.1.</p>") + \
        ponte("Domino o terminal. Como guardo o histórico do que faço nos arquivos, e volto atrás quando erro?", "Com o Git.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
    body = recap("No capítulo 3 você escreveu um script e viu como o PATH decide o que roda. Falta olhar para fora do seu arquivo: o que está rodando agora, como falar com um site e como entrar em outra máquina. Este capítulo continua sendo <b>complemento</b>.") + AVISO_COMP + corpo
    chapter(PASTA, 4, "processos-ssh-curl", TITULO, "Processos, SSH e curl", "Capítulo 4 · Complemento",
            "Ver e encerrar processos, conversar com um site pelo terminal e entender o par de chaves do SSH, sem nenhuma credencial real.",
            chips(body, 35), body, scripts=[])
