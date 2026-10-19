from py_manifest import *
T = TITULO
S5 = ["demos/cap-5-8.js"]

# ================= CAP 8 =================
body8 = recap("No Capítulo 7 você aprendeu a guardar e compartilhar código. Agora é hora de usar tudo o que veio antes (variáveis, condições, listas, laços, funções) num problema em que <b>ninguém entrega a fórmula</b>: um jogo de senha. O ponto da atividade é que <i>programar começa antes do teclado</i>, na estratégia.") + '''
<section class="sec" id="dinamica">
  <h2><span class="sn">1</span>A dinâmica: o cofre de 4 dígitos</h2>
  <p class="gancho">Descobrir a senha do adversário antes que ele descubra a sua.</p>
  <p>Na atividade em grupo, cada grupo protegia um cofre (IoT) com uma <b>senha de 4 dígitos</b> e tentava abrir o do adversário. A cada tentativa, o cofre respondia com duas pistas, <b>sem dizer qual dígito</b> gerou cada uma:</p>
  <div class="grid2">
    <div class="card rv"><b style="color:var(--green)">ótimo</b><p>Um dígito do chute existe na senha <b>e está na posição certa</b>.</p></div>
    <div class="card rv"><b style="color:var(--c1)">bom</b><p>Um dígito do chute existe na senha, mas está em <b>outra posição</b>.</p></div>
  </div>
  <p>Teste a resposta do cofre com a sua própria senha e chute (a senha 4071 e o chute 0111 dão 1 ótimo e 1 bom: o dígito 1 está certo na última posição, e o 0 existe, mas em outro lugar):</p>
  <div class="demo" data-demo="cofrepistas"></div>
  <div class="nota cuidado"><span class="lbl">O que deu errado</span>O grupo não conseguiu combinar uma estratégia: cada pessoa chutava por conta própria, e as pistas não eram aproveitadas. Sem uma regra comum, <b>as respostas anteriores não ajudam</b> nos chutes seguintes. O que faltou é justamente o que um algoritmo entrega: uma regra acordada antes de começar.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Dá para sentir o tamanho do problema antes de resolver?</div><p>Dá: jogue contra o cofre.</p></div>
</section>

<section class="sec" id="jogar">
  <h2><span class="sn">2</span>Sinta o problema</h2>
  <p class="gancho">São 10 × 10 × 10 × 10 = 10.000 senhas. Quantas tentativas você precisa?</p>
  <p>Jogue algumas partidas. Ligue "mostrar quantas senhas ainda são possíveis" para ver o efeito de cada resposta: <b>cada pista elimina hipóteses</b>.</p>
  <div class="demo" data-demo="cofrejogo"></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se um programa jogasse? Que regra ele seguiria?</div><p>Antes da regra, o que "pensar como um computador" significa aqui.</p></div>
</section>

<section class="sec" id="pilares">
  <h2><span class="sn">3</span>Os quatro pilares do pensamento computacional</h2>
  <p class="gancho">A mesma atividade, vista por quatro lentes.</p>
  <div class="tablewrap"><table>
    <tr><th>Pilar</th><th>O que é</th><th>No cofre</th></tr>
    <tr><td><b>Decomposição</b></td><td>quebrar o problema em partes menores</td><td>separar "quais dígitos existem" de "em que posição estão"</td></tr>
    <tr><td><b>Reconhecimento de padrões</b></td><td>achar o que se repete ou se parece</td><td>comparar duas respostas que diferem em um só dígito</td></tr>
    <tr><td><b>Abstração</b></td><td>ficar só com o que importa, ignorando o resto</td><td>reduzir cada tentativa a um par de números: (ótimo, bom)</td></tr>
    <tr><td><b>Algoritmo</b></td><td>uma sequência de passos clara, que sempre funciona</td><td>uma regra fixa para escolher o próximo chute</td></tr>
  </table></div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Qual é essa regra?</div><p>Uma ideia simples: só chute o que ainda pode ser a resposta.</p></div>
</section>

<section class="sec" id="estrategia">
  <h2><span class="sn">4</span>Um algoritmo que elimina hipóteses</h2>
  <p class="gancho">Cada resposta é uma peneira. Só passa quem daria <i>a mesma resposta</i>.</p>
  <p>Estratégia de <b>consistência</b> (complemento, não foi dada em aula):</p>
  <ol>
    <li>Comece com a lista das 10.000 senhas possíveis.</li>
    <li>Chute uma senha <b>que ainda está na lista</b>.</li>
    <li>Com a resposta (ótimo, bom), <b>descarte toda senha que não teria dado a mesma resposta</b> a esse chute.</li>
    <li>Repita até dar 4 ótimos.</li>
  </ol>
  <p>Todo o coração do programa é a função que compara um chute com uma senha:</p>
<pre><code><span class="k">from</span> itertools <span class="k">import</span> product
<span class="k">from</span> collections <span class="k">import</span> Counter

<span class="k">def</span> <span class="f">pistas</span>(segredo, chute):
    <span class="an" tabindex="0" data-t="zip percorre as duas senhas em paralelo, posição a posição. Soma 1 para cada posição igual.">otimo = <span class="f">sum</span>(s == c <span class="k">for</span> s, c <span class="k">in</span> <span class="f">zip</span>(segredo, chute))</span>
    <span class="an" tabindex="0" data-t="Counter conta quantas vezes cada dígito aparece. O &amp; fica com o mínimo de cada um: os dígitos em comum, em qualquer posição.">comuns = <span class="f">sum</span>((<span class="f">Counter</span>(segredo) &amp; <span class="f">Counter</span>(chute)).<span class="f">values</span>())</span>
    <span class="k">return</span> otimo, comuns - otimo        <span class="c"># bom = em comum menos os que já são ótimos</span>

candidatos = [<span class="s">""</span>.<span class="f">join</span>(p) <span class="k">for</span> p <span class="k">in</span> <span class="f">product</span>(<span class="s">"0123456789"</span>, repeat=<span class="n">4</span>)]   <span class="c"># 10.000 senhas</span>

<span class="k">def</span> <span class="f">filtra</span>(candidatos, chute, resposta):
    <span class="k">return</span> [c <span class="k">for</span> c <span class="k">in</span> candidatos <span class="k">if</span> <span class="f">pistas</span>(c, chute) == resposta]</code></pre>
  <p>Veja o algoritmo trabalhando, sobre a senha 4071. A coluna "possíveis" mostra como cada resposta derruba a lista:</p>
  <div class="demo" data-demo="cofresolver"></div>
  <p>Para a senha 4071, o Python (conferido rodando) resolve em <b>8 tentativas</b>: 0000 → 0111 → 2012 → 3031 → 4041 → 4051 → 4061 → 4071, e a lista cai de 10.000 para 2.916, 384, 98, 36, 10, 4 e 3 antes do acerto. Rodando o algoritmo (conferido) em todas as 10.000 senhas possíveis, a média é de cerca de 8,7 tentativas e o pior caso é 13.</p>
  <div class="nota lembra"><span class="lbl">Complemento: quão bom dá para ser?</span>Em 1977, Donald Knuth mostrou que o Mastermind clássico (4 posições, 6 cores) sempre se resolve em até <b>5 jogadas</b>, escolhendo o chute que minimiza o pior caso. Nosso algoritmo escolhe o <i>primeiro</i> candidato, e não o melhor, e por isso é mais simples e um pouco mais lento. Existe sempre esse compromisso entre simplicidade e otimização.</div>
  <div class="nota exemplo"><span class="lbl">Como o grupo poderia ter jogado</span>Divida papéis <b>antes</b> de começar: uma pessoa chuta, outra anota cada (chute, resposta) numa tabela, e uma terceira elimina hipóteses. É um algoritmo executado por pessoas, e mostra que pensar em passos serve fora do computador também.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "O cofre responde com <b>ótimo</b> (dígito certo, posição certa) e <b>bom</b> (dígito existe, posição errada).",
    "Quatro pilares: <b>decomposição</b>, <b>padrões</b>, <b>abstração</b>, <b>algoritmo</b>.",
    "Há <b>10.000</b> senhas. Chutar sem usar as pistas é força bruta.",
    "<b>Estratégia de consistência:</b> chute só o que ainda é possível e descarte o que não daria a mesma resposta.",
    "<code>zip</code> compara posição a posição; <code>Counter</code> conta repetições; <code>itertools.product</code> gera as combinações.",
    "Sem regra combinada, as respostas anteriores <b>não são aproveitadas</b>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Senha 4071 e chute 0111. Quantos 'ótimo' e quantos 'bom'?", [("a","2 ótimos e 0 bons."),("b","1 ótimo e 1 bom."),("c","0 ótimos e 2 bons.")], "O último 1 está na posição certa (ótimo). O 0 existe na senha, mas em outra posição (bom). O segundo 1 do chute não tem par: só há um 1 na senha.") + quiz(2, "c", "Qual pilar corresponde a reduzir cada tentativa a um par de números (ótimo, bom)?", [("a","Decomposição."),("b","Reconhecimento de padrões."),("c","Abstração: ficar só com o que importa.")], "Abstrair é ignorar os detalhes que não ajudam e guardar só o essencial. Aqui, todo o chute vira um par.") + quiz(3, "a", "Depois de uma resposta (ótimo, bom), quais senhas devem ser descartadas?", [("a","As que NÃO teriam dado a mesma resposta ao mesmo chute."),("b","As que têm o primeiro dígito do chute."),("c","Nenhuma: só o chute em si.")], "Se a senha verdadeira deu aquela resposta, qualquer candidata que desse outra resposta ao mesmo chute não pode ser a verdadeira.") + flash([
    ("Quantas senhas de 4 dígitos existem?", "10 × 10 × 10 × 10 = 10.000 (de 0000 a 9999)."),
    ("O que faz o zip?", "Percorre duas sequências em paralelo, posição a posição."),
    ("Por que usar Counter?", "Para contar quantas vezes cada dígito aparece e achar os dígitos em comum, mesmo repetidos."),
    ("O que um algoritmo traz ao trabalho em grupo?", "Uma regra acordada antes de começar, em que cada resposta é aproveitada.")]) + ponte("Escrevi programas inteiros. O que mais o Python tem que eu ainda não usei?", "Strings, arquivos, tratamento de erros e módulos: o complemento final.", "Para onde vamos agora · Capítulo 9") + '''
</section>'''
chapter(PASTA, 8, "o-cofre", T, "Algoritmo na prática: o cofre", "Capítulo 8 · Aula 9",
        "Aplicar o pensamento computacional a um jogo de senha, com um algoritmo que elimina hipóteses.",
        ["<b>~40 min</b>", "3 demos · 3 testes · 4 flashcards", "jogue contra o cofre"], body8, scripts=S5)

# ================= CAP 9 =================
tr_erro = trace_html("try/except: pedir de novo até acertar", """while True:
    texto = input("Digite um numero: ")
    try:
        n = int(texto)
        break
    except ValueError:
        print("Isso nao e um numero inteiro.")
print(n * 2)""", entradas=["abc", "21"], notas={2: ["Primeira volta: a pessoa digita <code>abc</code>.", "Segunda volta: a pessoa digita <code>21</code>."], 4: lambda v: "<code>int('abc')</code> falha e levanta um <code>ValueError</code>." if v.get("texto") == "abc" else "<code>int('21')</code> funciona: <code>n</code> vira 21.", 6: "O erro é <b>capturado</b> aqui: o programa não quebra.", 7: "Mostra o aviso e o <code>while True</code> volta ao início.", 5: "Sem erro: o <code>break</code> sai do laço.", 8: "O programa segue normalmente."}, max_passos=40)
tr_dict = trace_html("Contar palavras com dicionário", """palavras = ["sol", "lua", "sol", "mar", "sol"]
contagem = {}
for p in palavras:
    contagem[p] = contagem.get(p, 0) + 1
print(contagem)""", notas={2: "Um dicionário vazio.", 4: "<code>get(p, 0)</code> devolve o valor da chave, ou <b>0</b> se ela ainda não existir. Soma 1 e guarda de volta.", 5: "\"sol\" apareceu 3 vezes."}, max_passos=40)

body9 = recap("Nos capítulos anteriores você montou o essencial da linguagem e resolveu um problema de estratégia. Este capítulo é <b>complemento</b> (não foi dado em aula): as peças que aparecem em quase todo programa real e que você ainda não usou. Todos os exemplos de código foram executados.", "Onde paramos") + '''
<section class="sec" id="strings">
  <h2><span class="sn">1</span>Strings: mais do que aspas</h2>
  <p class="gancho">Texto é uma sequência, e muito do que você aprendeu em listas vale aqui.</p>
  <p>Uma <code>str</code> é uma sequência de caracteres: dá para indexar (<code>"python"[0]</code> é <code>'p'</code>), fatiar (<code>"python"[1:4]</code> é <code>'yth'</code>) e percorrer com <code>for</code>. Mas ela é <b>imutável</b>: os métodos devolvem uma <b>nova</b> string, e a original não muda.</p>
<pre><code>nome = <span class="s">"  Ana Souza  "</span>
nome.<span class="f">strip</span>()                 <span class="c"># 'Ana Souza'    (tira espaços das pontas)</span>
nome.<span class="f">strip</span>().<span class="f">upper</span>()        <span class="c"># 'ANA SOUZA'</span>
<span class="s">"sol,lua,mar"</span>.<span class="f">split</span>(<span class="s">","</span>)   <span class="c"># ['sol', 'lua', 'mar']</span>
<span class="s">" - "</span>.<span class="f">join</span>([<span class="s">"a"</span>, <span class="s">"b"</span>])      <span class="c"># 'a - b'</span>
<span class="s">"banana"</span>.<span class="f">replace</span>(<span class="s">"a"</span>, <span class="s">"o"</span>) <span class="c"># 'bonono'</span>
<span class="s">"banana"</span>.<span class="f">find</span>(<span class="s">"na"</span>)        <span class="c"># 2 (posição; -1 se não achar)</span>
<span class="s">"python"</span>.<span class="f">startswith</span>(<span class="s">"py"</span>)  <span class="c"># True</span>
<span class="s">"ana"</span> <span class="k">in</span> <span class="s">"banana"</span>          <span class="c"># True</span></code></pre>
  <div class="nota erro"><span class="lbl">Erro comum</span>Esquecer que strings são imutáveis: <code>nome.upper()</code> sozinho <b>não muda</b> <code>nome</code>. É preciso guardar: <code>nome = nome.upper()</code>.</div>
</section>

<section class="sec" id="dicionarios">
  <h2><span class="sn">2</span>Dicionários na prática</h2>
  <p class="gancho">Contar, agrupar, achar por nome.</p>
  <p>O padrão mais útil: <b>contar ocorrências</b>. O <code>get(chave, padrão)</code> evita o <code>KeyError</code> de ler uma chave que ainda não existe:</p>
''' + tr_dict + '''
<pre><code>aluno = {<span class="s">"nome"</span>: <span class="s">"Ana"</span>, <span class="s">"idade"</span>: <span class="n">19</span>}
<span class="k">for</span> chave, valor <span class="k">in</span> aluno.<span class="f">items</span>():     <span class="c"># percorre os pares</span>
    <span class="f">print</span>(chave, <span class="s">"=&gt;"</span>, valor)
<span class="s">"idade"</span> <span class="k">in</span> aluno                       <span class="c"># True: testa se a chave existe</span>
aluno.<span class="f">get</span>(<span class="s">"curso"</span>, <span class="s">"não informado"</span>)   <span class="c"># 'não informado' (sem erro)</span></code></pre>
</section>

<section class="sec" id="erros">
  <h2><span class="sn">3</span>Erros: ler o traceback e tratar</h2>
  <p class="gancho">Todo programa quebra. A diferença é saber ler o recado.</p>
  <p>Quando algo dá errado, o Python imprime um <b>traceback</b>. Leia <b>de baixo para cima</b>: a última linha diz <i>o tipo e o motivo</i> do erro, e as de cima mostram o caminho até lá.</p>
<pre><code>Traceback (most recent call last):
  File "ex.py", line 3, in &lt;module&gt;
    <span class="an" tabindex="0" data-t="A linha onde o erro ocorreu.">resultado = idade + "anos"</span>
<span class="an" tabindex="0" data-t="O tipo do erro e o motivo, em linguagem do Python. Comece sempre por aqui.">TypeError: unsupported operand type(s) for +: 'int' and 'str'</span></code></pre>
  <div class="tablewrap"><table>
    <tr><th>Erro</th><th>Quando aparece</th></tr>
    <tr><td><code>SyntaxError</code> / <code>IndentationError</code></td><td>o código está escrito errado (dois-pontos, parêntese, recuo)</td></tr>
    <tr><td><code>NameError</code></td><td>usou uma variável que não existe (ou errou o nome)</td></tr>
    <tr><td><code>TypeError</code></td><td>operação com tipos incompatíveis (<code>int + str</code>)</td></tr>
    <tr><td><code>ValueError</code></td><td>o tipo está certo, mas o valor não serve (<code>int("abc")</code>)</td></tr>
    <tr><td><code>IndexError</code> / <code>KeyError</code></td><td>índice fora da lista / chave que não está no dicionário</td></tr>
    <tr><td><code>ZeroDivisionError</code></td><td>divisão por zero</td></tr>
  </table></div>
  <p>Para <b>tratar</b> um erro previsto (como o usuário digitar texto onde se espera número), use <code>try</code> e <code>except</code>. O programa abaixo pede de novo até a pessoa acertar (as duas digitações do exemplo são <code>abc</code> e <code>21</code>):</p>
''' + tr_erro + '''
  <div class="nota cuidado"><span class="lbl">Cuidado</span>Capture <b>o erro específico</b> (<code>except ValueError</code>), e não um genérico <code>except:</code> que engole tudo, inclusive erros de digitação seus. Esconder erros é pior do que deixá-los aparecer.</div>
</section>

<section class="sec" id="arquivos">
  <h2><span class="sn">4</span>Arquivos e módulos</h2>
  <p class="gancho">Guardar dados além do fim do programa, e usar código dos outros.</p>
<pre><code><span class="c"># escrever e ler um arquivo de texto</span>
<span class="k">with</span> <span class="f">open</span>(<span class="s">"notas.txt"</span>, <span class="s">"w"</span>, encoding=<span class="s">"utf-8"</span>) <span class="k">as</span> f:
    f.<span class="f">write</span>(<span class="s">"Ana;9.5\\nBia;8.0\\n"</span>)

<span class="k">with</span> <span class="f">open</span>(<span class="s">"notas.txt"</span>, encoding=<span class="s">"utf-8"</span>) <span class="k">as</span> f:
    <span class="k">for</span> linha <span class="k">in</span> f:
        nome, nota = linha.<span class="f">strip</span>().<span class="f">split</span>(<span class="s">";"</span>)
        <span class="f">print</span>(nome, <span class="f">float</span>(nota))</code></pre>
  <ul>
    <li>Modos: <code>"r"</code> ler (padrão), <code>"w"</code> escrever (<b>apaga</b> o que havia), <code>"a"</code> acrescentar no final.</li>
    <li>O <code>with</code> garante que o arquivo é <b>fechado</b> mesmo se der erro no meio.</li>
    <li>Informe <code>encoding="utf-8"</code> para acentos não virarem símbolos estranhos.</li>
  </ul>
  <p>Um <b>módulo</b> é código pronto que você importa. A biblioteca padrão já traz muito: <code>math</code>, <code>random</code>, <code>datetime</code>, <code>csv</code>, <code>json</code>. Bibliotecas de terceiros se instalam com <code>pip install nome</code> (por exemplo, <code>pandas</code> e <code>numpy</code> nas disciplinas de dados).</p>
<pre><code><span class="k">import</span> math, random
math.<span class="f">sqrt</span>(<span class="n">16</span>)            <span class="c"># 4.0</span>
random.<span class="f">randint</span>(<span class="n">1</span>, <span class="n">10</span>)    <span class="c"># inteiro aleatório de 1 a 10</span></code></pre>
  <div class="nota lembra"><span class="lbl">Complemento: ambiente virtual</span>Cada projeto deve ter suas próprias bibliotecas, para versões diferentes não brigarem. O jeito padrão é um <b>ambiente virtual</b>: <code>python -m venv .venv</code> (e ativá-lo). E nunca versione essa pasta: ela entra no <code>.gitignore</code> (Capítulo 7).</div>
</section>

<section class="sec" id="estilo">
  <h2><span class="sn">5</span>Escrever código que outras pessoas leem</h2>
  <p class="gancho">Você vai ler seu código daqui a três meses, e vai parecer de um desconhecido.</p>
  <ul>
    <li><b>PEP 8</b> é o guia de estilo oficial: nomes de variáveis e funções em <code>minusculo_com_underline</code> (<i>snake_case</i>), constantes em MAIÚSCULAS, 4 espaços de recuo, linhas curtas.</li>
    <li><b>Nomes que dizem o que são</b>: <code>total_de_horas</code> vence <code>x</code>.</li>
    <li><b>Funções pequenas</b>, que fazem uma coisa só.</li>
    <li><b>Comentários explicam o porquê</b>, e não o óbvio (<code># soma 1</code> não ajuda). Funções importantes ganham uma <i>docstring</i>, o texto entre aspas triplas logo abaixo do <code>def</code>.</li>
    <li><b>Depurar</b>: leia o traceback de baixo para cima; use <code>print()</code> para ver os valores; reduza o problema ao menor código que ainda erra.</li>
  </ul>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento da apostila</h2>
  ''' + resumo([
    "<b>Strings</b> são imutáveis: os métodos (<code>strip</code>, <code>split</code>, <code>replace</code>) devolvem novas strings.",
    "<b>Dicionário</b>: <code>get(chave, padrão)</code> evita KeyError; ótimo para contar.",
    "<b>Traceback</b>: leia de baixo para cima. A última linha diz o tipo e o motivo.",
    "<code>try/except ValueError</code> trata um erro previsto. Capture o <b>específico</b>.",
    "<code>with open(...)</code> fecha o arquivo sozinho. <code>\"w\"</code> apaga; <code>\"a\"</code> acrescenta.",
    "<b>PEP 8</b>, nomes claros, funções pequenas: escreva para quem vai ler."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Depois de <code>s = 'ana'</code> e <code>s.upper()</code> (sem atribuir), quanto vale <code>s</code>?", [("a","'ANA'"),("b","'ana': a string não muda, o método devolveu outra."),("c","None")], "Strings são imutáveis. Para guardar o resultado: <code>s = s.upper()</code>.") + quiz(2, "c", "Qual a melhor forma de tratar o usuário digitar texto onde se espera número?", [("a","Um try/except sem tipo, para pegar qualquer erro."),("b","Ignorar: o Python se vira."),("c","try/except ValueError em volta do int(), pedindo de novo.")], "Capturar o erro específico trata o caso previsto e deixa os outros erros aparecerem.") + quiz(3, "a", "O modo <code>\"w\"</code> do <code>open</code>:", [("a","Escreve e apaga o conteúdo anterior do arquivo."),("b","Acrescenta no final."),("c","Só lê.")], "Para acrescentar sem apagar, use <code>\"a\"</code>. Para só ler, <code>\"r\"</code>.") + flash([
    ("Como ler um traceback?", "De baixo para cima: a última linha mostra o tipo e o motivo do erro; as de cima mostram o caminho."),
    ("Para que serve o with?", "Garante que o arquivo seja fechado ao sair do bloco, mesmo se ocorrer um erro."),
    ("O que é o PEP 8?", "O guia de estilo oficial do Python (nomes, recuo, tamanho de linha)."),
    ("dict.get(chave, 0)?", "Devolve o valor da chave, ou 0 se ela não existir, sem dar KeyError.")]) + '''
  <div class="ponte rv"><div class="t">E agora?</div><div class="q">Você percorreu o caminho de variáveis até algoritmos.</div><p>O melhor próximo passo é um projeto seu: um quiz, um controle de gastos, um organizador de notas. Comece pequeno, versione no Git e use o que viu aqui. Volte à <a href="index.html">visão geral</a> sempre que quiser revisar.</p></div>
</section>'''
chapter(PASTA, 9, "alem-do-basico", T, "Para ir além (complemento)", "Capítulo 9 · Complemento",
        "O que quase todo programa real usa: strings, dicionários, erros, arquivos, módulos e estilo.",
        ["<b>~45 min</b>", "2 demos · 3 testes · 4 flashcards", "complemento, não foi dado em aula"], body9, scripts=S5)
print("py caps 8-9 ok")
