from py_manifest import *
T = TITULO
S5 = ["demos/cap-5-8.js"]

# ================= CAP 6 =================
tr_mat = trace_html("Mexendo numa matriz", """matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matriz.append([10, 11, 12])
matriz[1].insert(0, 100)
del matriz[0][1]
print(matriz[1][2])
print(len(matriz))""", notas={1: "Uma lista de listas: 3 linhas, 3 colunas.", 2: "<code>append</code> acrescenta uma <b>linha</b> inteira.", 3: "<code>matriz[1]</code> é a segunda linha; o <code>insert</code> põe o 100 no <b>início</b> dela (que agora tem 4 elementos).", 4: "<code>del matriz[0][1]</code> remove o 2 da primeira linha.", 5: "<code>matriz[1][2]</code>: linha 1, coluna 2. A linha é [100, 4, 5, 6], e o índice 2 é o <b>5</b>.", 6: "Agora há 4 linhas."})
tr_aninhado = trace_html("for aninhado: somar todos os elementos", """m = [[1, 2], [3, 4]]
total = 0
for y in range(2):
    for x in range(2):
        total = total + m[y][x]
print(total)""", notas={3: "O laço de fora escolhe a <b>linha</b> y.", 4: "O laço de dentro percorre as <b>colunas</b> x dessa linha.", 5: "Soma o elemento da linha y, coluna x.", 6: "1 + 2 + 3 + 4 = 10."}, max_passos=40)
tr_primo = trace_html("Função: eh_primo", """def eh_primo(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True

print(eh_primo(9))
print(eh_primo(7))""", notas={9: "Chamada com <code>n = 9</code>. O controle <b>entra</b> na função.", 2: lambda v: "%d não é menor que 2: segue." % v["n"], 4: lambda v: "Só é preciso testar divisores até a raiz quadrada: <code>range(2, %d)</code>." % (int(v["n"] ** 0.5) + 1), 5: lambda v: "%d %% %d == %d: %s" % (v["n"], v["d"], v["n"] % v["d"], "achou um divisor." if v["n"] % v["d"] == 0 else "não divide, tenta o próximo."), 6: "<code>return False</code> <b>encerra a função</b> na hora e devolve o valor a quem chamou.", 7: "Nenhum divisor encontrado: <code>return True</code>.", 10: "Nova chamada, agora com 7: o <code>n</code> da função é outro."}, max_passos=50)

body6 = recap("No Capítulo 5 você repetiu comandos com laços sobre listas. Duas necessidades aparecem em seguida: <b>dados em duas dimensões</b> (tabelas, grades de dados) e <b>blocos de código com nome</b>, para não repetir a mesma lógica em vários lugares.") + '''
<section class="sec" id="matriz">
  <h2><span class="sn">1</span>Matriz: uma lista de listas</h2>
  <p class="gancho">Uma tabela cabe numa variável só?</p>
  <p>Uma <b>matriz</b> é uma estrutura bidimensional: cada elemento tem um índice de <b>linha</b> e um de <b>coluna</b>, ambos começando em 0. Em Python é simplesmente uma <b>lista de listas</b>, e se acessa com <code>matriz[y][x]</code>: <i>y</i> escolhe a linha, <i>x</i> a coluna.</p>
<pre><code>matriz = [
    [<span class="n">1</span>, <span class="n">2</span>, <span class="n">3</span>],
    [<span class="n">4</span>, <span class="n">5</span>, <span class="n">6</span>],
    [<span class="n">7</span>, <span class="n">8</span>, <span class="n">9</span>],
]
matriz[<span class="n">1</span>][<span class="n">2</span>]    <span class="c"># 6: segunda linha, terceira coluna</span></code></pre>
  <div class="demo" data-demo="matriz"></div>
  <p>Para <b>percorrer</b>, um <code>for</code> dentro do outro: o de fora escolhe a linha, o de dentro anda pelas colunas. Para acrescentar, remover e inserir, as mesmas operações de lista valem, aplicadas à linha certa:</p>
''' + tr_mat + tr_aninhado + '''
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Trocar y e x.</b> É <code>matriz[y][x]</code> (linha primeiro), e não <code>[x][y]</code>. E criar uma matriz com <code>[[0] * 3] * 3</code> é uma armadilha: as três linhas são a <b>mesma</b> lista (lembra do <code>b = a</code> do Capítulo 4?). O certo: <code>[[0] * 3 for _ in range(3)]</code>.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Percorrer uma matriz, calcular um primo, contar vogais: tudo isso eu vou querer reutilizar.</div><p>Dar um nome ao bloco de código é a ideia da função.</p></div>
</section>

<section class="sec" id="funcoes">
  <h2><span class="sn">2</span>Funções: blocos com nome</h2>
  <p class="gancho">Escreva uma vez, use quantas vezes quiser.</p>
  <p>Uma <b>função</b> é um bloco de código reutilizável, definido com <code>def</code>. Ela recebe <b>parâmetros</b> (entradas) e devolve um resultado com <code>return</code>:</p>
<pre><code><span class="k">def</span> <span class="f">media</span>(numeros):
    <span class="k">return</span> <span class="f">sum</span>(numeros) / <span class="f">len</span>(numeros)

<span class="f">print</span>(<span class="f">media</span>([<span class="n">7</span>, <span class="n">8</span>, <span class="n">9</span>]))   <span class="c"># 8.0</span></code></pre>
  <p>Acompanhe o controle <i>entrando</i> e <i>saindo</i> da função <code>eh_primo</code>. Repare que dentro dela as variáveis são as da função (<code>n</code> e <code>d</code>), e não as do programa principal:</p>
''' + tr_primo + '''
  <div class="grid2">
    <div class="card rv"><b>return x print</b><p><code>print</code> só <b>mostra</b> na tela. <code>return</code> <b>devolve</b> o valor a quem chamou, para você guardar numa variável ou usar numa conta. Uma função sem <code>return</code> devolve <code>None</code>.</p></div>
    <div class="card rv"><b>Escopo (complemento)</b><p>Variáveis criadas <b>dentro</b> da função são <b>locais</b>: só existem lá. O mundo de fora não as enxerga, e a função não deveria depender de variáveis globais.</p></div>
  </div>
<pre><code><span class="k">def</span> <span class="f">saudacao</span>(nome, idioma=<span class="s">"pt"</span>):       <span class="c"># idioma tem valor padrão</span>
    <span class="k">if</span> idioma == <span class="s">"pt"</span>:
        <span class="k">return</span> <span class="s">f"Olá, {nome}!"</span>
    <span class="k">return</span> <span class="s">f"Hello, {nome}!"</span>

<span class="f">saudacao</span>(<span class="s">"Ana"</span>)                <span class="c"># 'Olá, Ana!'</span>
<span class="f">saudacao</span>(<span class="s">"Ana"</span>, <span class="s">"en"</span>)          <span class="c"># 'Hello, Ana!'</span>
<span class="f">saudacao</span>(idioma=<span class="s">"en"</span>, nome=<span class="s">"Bia"</span>)   <span class="c"># argumentos nomeados: a ordem não importa</span></code></pre>
  <h3>Os exercícios de função, resolvidos</h3>
<pre><code><span class="c"># calculadora com 4 funções</span>
<span class="k">def</span> <span class="f">soma</span>(a, b): <span class="k">return</span> a + b
<span class="k">def</span> <span class="f">subtrai</span>(a, b): <span class="k">return</span> a - b
<span class="k">def</span> <span class="f">multiplica</span>(a, b): <span class="k">return</span> a * b
<span class="k">def</span> <span class="f">divide</span>(a, b):
    <span class="k">if</span> b == <span class="n">0</span>:
        <span class="k">return</span> <span class="s">"não dá para dividir por zero"</span>
    <span class="k">return</span> a / b

<span class="c"># contar vogais</span>
<span class="k">def</span> <span class="f">conta_vogais</span>(texto):
    <span class="k">return</span> <span class="f">sum</span>(<span class="n">1</span> <span class="k">for</span> c <span class="k">in</span> texto.<span class="f">lower</span>() <span class="k">if</span> c <span class="k">in</span> <span class="s">"aeiou"</span>)

<span class="c"># fatorial: 5! = 5 * 4 * 3 * 2 * 1 = 120</span>
<span class="k">def</span> <span class="f">fatorial</span>(n):
    resultado = <span class="n">1</span>
    <span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">2</span>, n + <span class="n">1</span>):
        resultado *= i
    <span class="k">return</span> resultado</code></pre>
  <div class="nota exemplo"><span class="lbl">Para um projeto seu</span>Matriz, funções, condicionais e laços são os ingredientes de qualquer programa interativo de tamanho médio. Escolha um projeto pequeno seu (um controle de gastos, uma agenda, um quiz), divida em funções com uma responsabilidade cada e monte a partir dessas peças antes de procurar soluções prontas: é o melhor jeito de fixar tudo isto.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">3</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Matriz</b> = lista de listas. <code>matriz[y][x]</code>: linha primeiro, coluna depois, ambos a partir de 0.",
    "Percorrer: <code>for</code> aninhado. Linha: <code>append</code>, <code>insert</code>, <code>del</code>, <code>pop</code> funcionam como em listas.",
    "<code>[[0] * 3] * 3</code> repete a <b>mesma</b> linha. Use compreensão: <code>[[0] * 3 for _ in range(3)]</code>.",
    "<b>Função</b>: <code>def nome(parametros):</code>; <code>return</code> devolve e encerra; sem return, devolve <code>None</code>.",
    "<b>Escopo</b>: variável de dentro da função é local. <b>return</b> não é <b>print</b>.",
    "Parâmetro com valor padrão (<code>idioma=\"pt\"</code>) e argumentos nomeados."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Dada <code>m = [[1, 2, 3], [4, 5, 6]]</code>, o que é <code>m[1][0]</code>?", [("a","4: linha 1 (a segunda), coluna 0."),("b","2"),("c","1")], "O primeiro índice escolhe a linha (a de índice 1 é [4, 5, 6]) e o segundo a coluna (a de índice 0 é o 4).") + quiz(2, "c", "Qual a diferença entre <code>return</code> e <code>print</code> dentro de uma função?", [("a","Nenhuma."),("b","print devolve o valor e return mostra na tela."),("c","return devolve o valor a quem chamou; print só mostra na tela.")], "Com <code>return</code> você pode guardar o resultado (<code>x = media(...)</code>). Com <code>print</code> o valor aparece e se perde.") + quiz(3, "b", "O que acontece quando uma função executa <code>return False</code> no meio do código?", [("a","O laço continua."),("b","A função termina na hora e devolve False."),("c","O programa inteiro para.")], "<code>return</code> encerra a função naquele ponto, mesmo dentro de um laço, e devolve o valor.") + flash([
    ("Como acessar uma matriz?", "matriz[y][x]: linha primeiro, coluna depois."),
    ("O que é escopo local?", "Variável criada dentro da função só existe lá dentro."),
    ("O que a função devolve sem return?", "None."),
    ("Por que testar divisores só até a raiz de n?", "Porque se n tem um divisor maior que a raiz, ele também tem um menor, que já teria sido encontrado.")]) + ponte("Meu código funciona no meu computador. Como guardo as versões e compartilho com outras pessoas?", "Com o Git e o GitHub.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
chapter(PASTA, 6, "matrizes-e-funcoes", T, "Matrizes e funções", "Capítulo 6 · Aula 7",
        "Dados em duas dimensões e código com nome: as duas peças que montam programas de verdade.",
        ["<b>~45 min</b>", "4 demos · 3 testes · 4 flashcards", "código rastreado"], body6, scripts=S5)

# ================= CAP 7 =================
body7 = recap("No Capítulo 6 você terminou de aprender as peças principais da linguagem. Agora uma pergunta prática: onde esse código <b>mora</b>? Se você apagar um arquivo sem querer, ou quiser voltar a como estava ontem, ou trabalhar com outra pessoa no mesmo programa, o computador sozinho não resolve.") + '''
<section class="sec" id="git">
  <h2><span class="sn">1</span>Git e GitHub: duas coisas diferentes</h2>
  <p class="gancho">Quem guarda o histórico, e quem guarda a cópia na nuvem?</p>
  <div class="grid2">
    <div class="card rv"><b>Git</b><p>Um <b>sistema de controle de versão</b>, que roda no seu computador. Registra o histórico de mudanças do projeto: permite voltar a versões anteriores, comparar alterações e trabalhar em paralelo sem perder trabalho.</p></div>
    <div class="card rv"><b>GitHub</b><p>Uma plataforma que <b>hospeda repositórios Git na nuvem</b>. É o intermediário entre o código local e uma cópia remota na internet: backup, colaboração e compartilhamento.</p></div>
  </div>
  <p>Um <b>repositório</b> é a pasta do projeto com o histórico. No GitHub ele pode ser <b>público</b> (qualquer pessoa vê o código, mesmo sem conta; ótimo para portfólio, material de estudo e open source) ou <b>privado</b> (só você e quem você convidar).</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Como uma mudança vira "histórico"?</div><p>Ela passa por quatro lugares.</p></div>
</section>

<section class="sec" id="fluxo">
  <h2><span class="sn">2</span>O caminho de uma mudança</h2>
  <p class="gancho">Editar não é salvar no histórico. Salvar no histórico não é enviar para a nuvem.</p>
  <p>Um <b>commit</b> é um "ponto de salvamento": uma fotografia do estado dos arquivos naquele momento, com uma mensagem dizendo o que mudou. Até o commit existir, o Git só <i>percebe</i> que algo mudou. O fluxo básico:</p>
  <ol>
    <li>Alterar arquivos no projeto.</li>
    <li><code>git add</code>: escolher o que vai entrar no próximo commit (a <b>staging</b>, a "mesa de preparação").</li>
    <li><code>git commit -m "mensagem"</code>: tirar a foto.</li>
    <li><code>git push</code>: enviar os commits para o GitHub.</li>
  </ol>
  <p>Experimente cada passo e observe onde a mudança está depois de cada botão:</p>
  <div class="demo" data-demo="gitsim"></div>
<pre><code>git add .                                  <span class="c"># prepara todas as mudanças</span>
git commit -m "corrige o cálculo do desconto"
git push                                   <span class="c"># envia para o GitHub</span></code></pre>
  <div class="nota cuidado"><span class="lbl">add . ou arquivo específico?</span><code>git add .</code> prepara <b>tudo</b> o que mudou. Para ser seletivo, <code>git add arquivo.py</code> prepara só aquele. A seletividade serve para que cada commit conte <b>uma história só</b> (uma correção, uma funcionalidade), o que facilita entender e desfazer depois.</div>
</section>

<section class="sec" id="comandos">
  <h2><span class="sn">3</span>Os comandos do dia a dia</h2>
  <p class="gancho">Uma lista curta que resolve 90% das situações.</p>
  <div class="tablewrap"><table>
    <tr><th>Comando</th><th>Faz</th></tr>
    <tr><td><code>git init</code></td><td>transforma a pasta atual em um repositório Git</td></tr>
    <tr><td><code>git clone &lt;url&gt;</code></td><td>baixa uma cópia de um repositório do GitHub</td></tr>
    <tr><td><code>git status</code></td><td>mostra o que mudou e o que está na staging (use sempre!)</td></tr>
    <tr><td><code>git add .</code></td><td>prepara as mudanças para o commit</td></tr>
    <tr><td><code>git commit -m "..."</code></td><td>registra a foto no histórico local</td></tr>
    <tr><td><code>git push</code></td><td>envia os commits para o GitHub</td></tr>
    <tr><td><code>git pull</code></td><td>traz do GitHub os commits que você ainda não tem</td></tr>
    <tr><td><code>git log</code></td><td>lista o histórico de commits</td></tr>
    <tr><td><code>git diff</code></td><td>mostra o que mudou, linha a linha</td></tr>
  </table></div>
  <h3>Complemento: branches</h3>
  <p>Uma <b>branch</b> (ramo) é uma linha paralela de commits. Serve para desenvolver algo novo sem mexer na versão estável (a <code>main</code>): você cria um ramo, trabalha nele e, quando estiver pronto, <b>junta</b> (<i>merge</i>) de volta. É o jeito de várias pessoas trabalharem ao mesmo tempo sem pisar umas nas outras. Comandos: <code>git branch</code>, <code>git switch -c nome-do-ramo</code>, <code>git merge nome-do-ramo</code>.</p>
  <h3>Complemento: boas práticas que evitam dor de cabeça</h3>
  <ul>
    <li><b>Mensagens que contam o porquê</b>, não "mudanças" ou "arrumei": <i>"corrige desconto para mais de 10 unidades"</i>.</li>
    <li><b>Nunca commite segredos</b> (senhas, chaves de API, arquivos <code>.env</code>). Em repositório público, qualquer um vê. Se um segredo vazar, <b>revogue-o</b> imediatamente (apagar o commit depois não basta, porque ele fica no histórico).</li>
    <li>Use um arquivo <code>.gitignore</code> para dizer ao Git o que <b>não</b> versionar (arquivos temporários, <code>.env</code>, pastas de dependências).</li>
    <li>Faça <b>commits pequenos e frequentes</b>. E <code>git pull</code> antes de começar a trabalhar, se mais gente mexe no projeto.</li>
  </ul>
  <div class="nota lembra"><span class="lbl">Ligação com o resto do curso</span>Um repositório público bem cuidado funciona como <b>portfólio</b>: cada projeto das disciplinas (um notebook de ML, um projeto de ESP32, um site) pode virar um repositório com um bom README. É assim que esta apostila foi publicada.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Git</b> controla versões (no seu computador). <b>GitHub</b> hospeda repositórios na nuvem.",
    "Repositório <b>público</b> (todos veem) ou <b>privado</b> (só convidados).",
    "Fluxo: editar → <code>git add</code> (staging) → <code>git commit -m</code> (histórico local) → <code>git push</code> (GitHub).",
    "<code>git status</code> mostra onde cada mudança está. <code>git pull</code> traz o que você não tem.",
    "<b>Branch</b>: linha paralela de trabalho. <b>Merge</b>: junta de volta.",
    "<b>Nunca</b> commite segredos. <code>.gitignore</code> lista o que não versionar."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Depois de <code>git commit</code>, as mudanças já estão no GitHub?", [("a","Sim, o commit envia tudo."),("b","Não: ficam só no seu computador até o git push."),("c","Só se o repositório for público.")], "O commit registra no histórico <b>local</b>. É o <code>push</code> que envia para o repositório remoto.") + quiz(2, "c", "Qual a função do <code>git add</code>?", [("a","Baixar arquivos do GitHub."),("b","Apagar arquivos."),("c","Escolher o que entra no próximo commit (staging).")], "O add leva as mudanças para a staging. Só o que está lá entra no commit.") + quiz(3, "a", "Você commitou uma senha num repositório público. O que fazer primeiro?", [("a","Revogar/trocar a senha, porque ela já ficou exposta."),("b","Apagar o arquivo e seguir, que o histórico some."),("c","Mudar o repositório para privado e esquecer.")], "O histórico guarda o commit antigo, e a exposição pode já ter ocorrido (inclusive por robôs). O primeiro passo é invalidar o segredo.") + flash([
    ("Git x GitHub?", "Git é o controle de versão local. GitHub é a plataforma que hospeda repositórios Git na nuvem."),
    ("O que é um commit?", "Uma foto do estado dos arquivos naquele momento, com uma mensagem."),
    ("Para que serve a staging?", "Escolher exatamente o que entra no próximo commit."),
    ("O que é uma branch?", "Uma linha paralela de commits, para desenvolver sem mexer na versão estável.")]) + ponte("Tenho todas as peças. Dá para usá-las num problema de verdade, sem fórmula pronta?", "Dá: um jogo de senha, em que ninguém lhe entrega o algoritmo.", "Para onde vamos agora · Capítulo 8") + '''
</section>'''
chapter(PASTA, 7, "git-e-github", T, "Git e GitHub", "Capítulo 7 · Aula 3",
        "Guardar o histórico do seu código, voltar no tempo e compartilhar com o mundo.",
        ["<b>~35 min</b>", "1 demo · 3 testes · 4 flashcards", "simulador de Git"], body7, scripts=S5)
print("py caps 6-7 ok")
