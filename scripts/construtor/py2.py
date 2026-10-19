from py_manifest import *
T = TITULO
S = ["demos/cap-1-4.js"]
S5 = ["demos/cap-5-8.js"]

# ================= CAP 3 =================
tr_nota = trace_html("elif: o primeiro verdadeiro vence", """nota = 6
if nota >= 7:
    print("Aprovado")
elif nota >= 5:
    print("Recuperação")
else:
    print("Reprovado")
print("Fim")""", notas={1: "<code>nota = 6</code>.", 2: "6 &gt;= 7 é <b>False</b>: o Python <b>pula</b> o bloco indentado.", 4: "6 &gt;= 5 é <b>True</b>: entra neste bloco.", 5: "Executa o bloco e <b>ignora todo o resto</b> da cadeia (o else nem é avaliado).", 8: "Depois da cadeia, o programa segue normalmente. Esta linha não está indentada, então não pertence ao if."})
tr_bis = trace_html("Ano bissexto", """ano = 1900
div4 = ano % 4 == 0
div100 = ano % 100 == 0
div400 = ano % 400 == 0
if (div4 and not div100) or div400:
    print("bissexto")
else:
    print("não bissexto")""", notas={2: "1900 é divisível por 4.", 3: "Mas também por 100...", 4: "...e não por 400.", 5: "(True e <b>não</b> True) → False; ou False → <b>False</b>.", 8: "1900 <b>não</b> foi bissexto, apesar de ser múltiplo de 4. A regra: múltiplo de 4, exceto os de 100, exceto os de 400 (por isso 2000 foi bissexto)."})
tr_match = trace_html("match-case com vários valores", """dia = 6
match dia:
    case 1 | 2 | 3 | 4 | 5:
        print("Dia útil")
    case 6 | 7:
        print("Fim de semana")
    case _:
        print("Dia inválido")""", notas={1: "Valor a testar.", 2: "O <code>match</code> compara <code>dia</code> com cada <code>case</code>, de cima para baixo.", 3: "6 não está entre 1 e 5 (o <code>|</code> lê como \"ou\").", 5: "6 está entre 6 e 7: entra aqui.", 6: "Executa e sai do match. O <code>case _</code> (curinga) só roda se nenhum outro casar."})

body3 = recap("No Capítulo 2 o programa passou a ler dados, calcular e formatar. Mas ele ainda fazia <b>sempre a mesma coisa</b>, de cima para baixo. Agora ele vai aprender a escolher: executar um bloco ou outro conforme uma condição.") + '''
<section class="sec" id="if">
  <h2><span class="sn">1</span>if, elif e else</h2>
  <p class="gancho">Uma pergunta de sim ou não decide o caminho.</p>
  <p>Uma <b>estrutura condicional</b> executa (ou ignora) um bloco de código dependendo de uma condição. A condição é uma expressão que vira <code>True</code> ou <code>False</code>:</p>
<pre><code><span class="k">if</span> idade &gt;= <span class="n">18</span>:
    <span class="f">print</span>(<span class="s">"Você é maior de idade."</span>)
<span class="k">else</span>:
    <span class="f">print</span>(<span class="s">"Você é menor de idade."</span>)</code></pre>
  <p>Para mais de duas saídas entra o <code>elif</code> ("senão se"). O Python avalia <b>de cima para baixo</b> e executa só o <b>primeiro</b> bloco cuja condição for verdadeira:</p>
''' + tr_nota + '''
  <div class="nota cuidado"><span class="lbl">Cuidado: a indentação é a sintaxe</span>Em Python não há chaves <code>{ }</code>: o que pertence a cada bloco é definido pelo <b>recuo</b> (4 espaços, por convenção). A linha <code>print("Fim")</code> sem recuo <i>não</i> faz parte do if. Misturar espaços e tabs ou errar o recuo dá <code>IndentationError</code>.</div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b><code>=</code> não é <code>==</code>.</b> <code>idade = 18</code> <i>atribui</i>; <code>idade == 18</code> <i>compara</i>. Dentro de um if, use sempre <code>==</code>. Outro clássico: <code>if x == 1 or 2:</code> está <b>errado</b> (o <code>2</code> sozinho é sempre verdadeiro). O certo é <code>if x == 1 or x == 2:</code> (ou <code>x in (1, 2)</code>).</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E quando a decisão depende de duas coisas ao mesmo tempo?</div><p>Combinamos condições com operadores lógicos.</p></div>
</section>

<section class="sec" id="logicos">
  <h2><span class="sn">2</span>Comparação e operadores lógicos</h2>
  <p class="gancho">Perguntas pequenas combinadas em uma pergunta grande.</p>
  <div class="grid2">
    <div class="card rv"><b>Comparação</b><p><code>==</code> igual · <code>!=</code> diferente · <code>&lt;</code> <code>&gt;</code> <code>&lt;=</code> <code>&gt;=</code></p></div>
    <div class="card rv"><b>Lógicos</b><p><code>and</code> (E): as duas · <code>or</code> (OU): pelo menos uma · <code>not</code> (NÃO): inverte</p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Correção ao slide</span>O slide mostra os símbolos <code>&amp;&amp;</code>, <code>||</code> e <code>!</code> ao lado de E/OU/NÃO. <b>Esses símbolos não existem em Python</b> (são de C, Java e JavaScript). Em Python os operadores lógicos se escrevem por extenso: <code>and</code>, <code>or</code>, <code>not</code>.</div>
  <div class="demo" data-demo="cond"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: ano bissexto</span>
    <div class="l"><div>Regra: bissexto se for múltiplo de 4, <b>exceto</b> os múltiplos de 100, <b>exceto</b> os múltiplos de 400.</div></div>
    <div class="l"><div>Em lógica: <code>(ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0</code>.</div></div>
    <div class="l"><div>Teste mentalmente: 2024 (sim), 1900 (não), 2000 (sim). Confira o passo a passo para 1900:</div></div>
  </div>
''' + tr_bis + '''
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Um menu com muitas opções vira uma escada de elif enorme. Existe algo mais limpo?</div><p>Existe, a partir do Python 3.10: o match-case.</p></div>
</section>

<section class="sec" id="match">
  <h2><span class="sn">3</span>match-case: menus e faixas</h2>
  <p class="gancho">Comparar uma variável com vários valores possíveis.</p>
  <p>O <code>match</code> (Python <b>3.10 ou mais novo</b>) compara um valor com cada <code>case</code>. O <code>case _</code> é o curinga, que pega o que sobrou (o equivalente ao <code>else</code>). Dentro de um case, o <code>|</code> lê como "ou", e um <b>guard</b> (<code>case ... if condição</code>) acrescenta uma condição extra:</p>
''' + tr_match + '''
<pre><code>idade = <span class="n">15</span>
<span class="k">match</span> idade:
    <span class="k">case</span> n <span class="k">if</span> n &lt;= <span class="n">12</span>:
        <span class="f">print</span>(<span class="s">"criança"</span>)
    <span class="k">case</span> n <span class="k">if</span> n &lt;= <span class="n">17</span>:
        <span class="f">print</span>(<span class="s">"adolescente"</span>)
    <span class="k">case</span> _:
        <span class="f">print</span>(<span class="s">"adulto"</span>)</code></pre>
  <p>Menu clássico do exercício (1 ver perfil, 2 editar perfil, 3 sair):</p>
<pre><code>opcao = <span class="f">int</span>(<span class="f">input</span>(<span class="s">"1-Ver perfil  2-Editar perfil  3-Sair: "</span>))
<span class="k">match</span> opcao:
    <span class="k">case</span> <span class="n">1</span>:
        <span class="f">print</span>(<span class="s">"Mostrando o perfil"</span>)
    <span class="k">case</span> <span class="n">2</span>:
        <span class="f">print</span>(<span class="s">"Editando o perfil"</span>)
    <span class="k">case</span> <span class="n">3</span>:
        <span class="f">print</span>(<span class="s">"Saindo"</span>)
    <span class="k">case</span> _:
        <span class="f">print</span>(<span class="s">"Opção inválida"</span>)</code></pre>
  <div class="nota lembra"><span class="lbl">Quando usar qual</span>Para <b>faixas</b> e condições compostas, o <code>if/elif</code> costuma ser mais claro. O <code>match</code> brilha para <b>valores exatos</b> (menus, dias, comandos). Uma pegadinha: dentro de <code>case</code>, um nome sozinho (como o <code>n</code> acima) <b>captura</b> o valor, e não compara com uma variável existente.</div>
  <h3>Os seis exercícios da aula, com soluções de estudo (complemento)</h3>
<pre><code><span class="c"># 1) positivo, negativo ou zero</span>
n = <span class="f">float</span>(<span class="f">input</span>(<span class="s">"Número: "</span>))
<span class="k">if</span> n &gt; <span class="n">0</span>:   <span class="f">print</span>(<span class="s">"positivo"</span>)
<span class="k">elif</span> n &lt; <span class="n">0</span>: <span class="f">print</span>(<span class="s">"negativo"</span>)
<span class="k">else</span>:        <span class="f">print</span>(<span class="s">"zero"</span>)

<span class="c"># 2) par ou ímpar (o resto da divisão por 2)</span>
n = <span class="f">int</span>(<span class="f">input</span>(<span class="s">"Inteiro: "</span>))
<span class="f">print</span>(<span class="s">"par"</span> <span class="k">if</span> n % <span class="n">2</span> == <span class="n">0</span> <span class="k">else</span> <span class="s">"ímpar"</span>)

<span class="c"># 4) vogal ou consoante (um caractere; o len(c) == 1 evita que "" ou "ae" contem como vogal)</span>
c = <span class="f">input</span>(<span class="s">"Letra: "</span>).<span class="f">lower</span>()
<span class="f">print</span>(<span class="s">"vogal"</span> <span class="k">if</span> <span class="f">len</span>(c) == <span class="n">1</span> <span class="k">and</span> c <span class="k">in</span> <span class="s">"aeiou"</span> <span class="k">else</span> <span class="s">"consoante"</span>)

<span class="c"># 5) desconto de 10% acima de 10 unidades</span>
preco, qtd = <span class="f">float</span>(<span class="f">input</span>(<span class="s">"Preço: "</span>)), <span class="f">int</span>(<span class="f">input</span>(<span class="s">"Quantidade: "</span>))
total = preco * qtd
<span class="k">if</span> qtd &gt; <span class="n">10</span>:
    total = total * <span class="n">0.9</span>
<span class="f">print</span>(<span class="s">f"Total: R$ {total:.2f}"</span>)

<span class="c"># 6) pode votar? (mínimo 16 anos)</span>
idade = <span class="f">int</span>(<span class="f">input</span>(<span class="s">"Idade: "</span>))
<span class="f">print</span>(<span class="s">"pode votar"</span> <span class="k">if</span> idade &gt;= <span class="n">16</span> <span class="k">else</span> <span class="s">"não pode votar"</span>)</code></pre>
  <p class="muted">O exercício 3 (bissexto) é o do exemplo acima. A forma <code>valor_a if condição else valor_b</code> é o <b>operador ternário</b>: uma decisão numa expressão só.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<code>if</code>/<code>elif</code>/<code>else</code>: executa o <b>primeiro</b> bloco verdadeiro, de cima para baixo.",
    "A <b>indentação</b> define o bloco. Sem chaves.",
    "<code>=</code> atribui; <code>==</code> compara. Em Python: <code>and</code>, <code>or</code>, <code>not</code> (nada de <code>&amp;&amp;</code> ou <code>||</code>).",
    "<b>Bissexto:</b> <code>(ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0</code>.",
    "<code>match</code>/<code>case</code> (Python 3.10+): menus e valores exatos; <code>|</code> é \"ou\"; <code>case _</code> é o curinga; guard com <code>if</code>.",
    "<code>x == 1 or 2</code> é um erro clássico: escreva <code>x == 1 or x == 2</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Com <code>nota = 8</code>, qual bloco da cadeia <code>if nota &gt;= 7 / elif nota &gt;= 5 / else</code> executa?", [("a","Os dois primeiros."),("b","Só o primeiro (Aprovado)."),("c","O else.")], "O Python para no primeiro verdadeiro. Como 8 &gt;= 7, executa esse bloco e ignora o elif e o else, mesmo que 8 &gt;= 5 também fosse verdadeiro.") + quiz(2, "c", "Qual condição diz 'maior de idade E com carteira'?", [("a","idade >= 18 && tem_carteira"),("b","idade >= 18 & tem_carteira"),("c","idade >= 18 and tem_carteira")], "Em Python o E lógico é <code>and</code>. O <code>&amp;&amp;</code> é de outras linguagens.") + quiz(3, "a", "O ano 1900 é bissexto?", [("a","Não: é múltiplo de 4 e de 100, mas não de 400."),("b","Sim: é múltiplo de 4."),("c","Sim: é múltiplo de 100.")], "A regra tem exceções em cascata: múltiplos de 100 não são bissextos, a menos que sejam múltiplos de 400 (como 2000).") + flash([
    ("Qual a diferença entre = e ==?", "= atribui um valor a uma variável. == compara dois valores e devolve True ou False."),
    ("O que faz o case _?", "É o curinga do match: roda quando nenhum outro case casou (como o else)."),
    ("Para que serve o %?", "Resto da divisão: n % 2 == 0 testa par; ano % 4 == 0 testa múltiplo de 4."),
    ("Por que a indentação importa?", "Em Python ela define quais linhas pertencem ao bloco do if, do laço ou da função.")]) + ponte("Decide uma vez. E se eu tiver muitos valores, ou precisar repetir a decisão?", "Aí entram as coleções, as listas, e depois os laços.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "decisoes", T, "Decisões: if, lógica e match-case", "Capítulo 3 · Aulas 2, 4 e 7",
        "Fazer o programa escolher o caminho: condições, operadores lógicos e o match-case.",
        ["<b>~45 min</b>", "4 demos · 3 testes · 4 flashcards", "código rastreado"], body3, scripts=S)

# ================= CAP 4 =================
tr_alias = trace_html("Copiar lista: a pegadinha do b = a", """a = [1, 2, 3]
b = a
b.append(4)
c = a.copy()
c.append(5)
print(a)
print(c)""", notas={2: "<code>b = a</code> <b>não copia</b>: cria um segundo nome para a <b>mesma</b> lista.", 3: "Mudar pelo nome <code>b</code> muda a lista que o <code>a</code> também aponta.", 4: "<code>copy()</code> cria uma lista <b>nova</b>, independente.", 5: "Mexer em <code>c</code> não afeta <code>a</code>.", 6: "<code>a</code> (e <code>b</code>) têm o 4, mas não o 5."})
body4 = recap("No Capítulo 3 o programa passou a decidir. Mas cada decisão olhava um valor só. Quando você tem 100 notas, não vai criar 100 variáveis (<code>nota1</code>, <code>nota2</code>, ...). Falta uma forma de guardar uma <b>coleção</b> sob um único nome.") + '''
<section class="sec" id="lista">
  <h2><span class="sn">1</span>Lista: a fila de caixas numeradas</h2>
  <p class="gancho">Uma variável só, muitos valores, na ordem.</p>
  <p>Uma <b>lista</b> é uma coleção <mark class="hl">ordenada</mark> (a posição faz parte da identidade do dado) e <mark class="hl g">mutável</mark> (dá para mudar o conteúdo depois de criada). O índice começa em <b>0</b>, e <code>-1</code> pega o último elemento sem você calcular <code>len(lista) - 1</code>.</p>
<pre><code>numeros = [<span class="n">1</span>, <span class="n">2</span>, <span class="n">3</span>, <span class="n">4</span>, <span class="n">5</span>]
nomes   = [<span class="s">"Alice"</span>, <span class="s">"Bob"</span>, <span class="s">"Charlie"</span>]
mista   = [<span class="n">1</span>, <span class="s">"Bob"</span>, <span class="n">3.14</span>, <span class="n">True</span>]   <span class="c"># tipos misturados são permitidos</span>
vazia   = []

numeros[<span class="n">0</span>]    <span class="c"># 1: o primeiro</span>
numeros[-<span class="n">1</span>]   <span class="c"># 5: o último</span></code></pre>
  <p>Para que serve: armazenar e organizar dados, <b>iterar</b> sobre eles (Capítulo 5), simular filas e pilhas, guardar dados estruturados (uma lista de listas é uma tabela, Capítulo 6) e passar coleções para funções. Brinque com as operações e com as fatias:</p>
  <div class="demo" data-demo="listbox"></div>
  <div class="tablewrap"><table>
    <tr><th>Método</th><th>Faz</th><th>Detalhe</th></tr>
    <tr><td><code>append(x)</code></td><td>põe x no final</td><td>rápido</td></tr>
    <tr><td><code>insert(i, x)</code></td><td>põe x na posição i</td><td>desloca os seguintes (mais caro)</td></tr>
    <tr><td><code>extend(outra)</code></td><td>junta todos os elementos de outra lista</td><td><code>append([1,2])</code> poria a lista inteira como <b>um</b> elemento</td></tr>
    <tr><td><code>remove(x)</code></td><td>tira a primeira ocorrência do <b>valor</b> x</td><td>dá <code>ValueError</code> se x não existir</td></tr>
    <tr><td><code>pop()</code> / <code>pop(i)</code></td><td>remove <b>e devolve</b> o último (ou o do índice i)</td><td>pelo índice, não pelo valor</td></tr>
    <tr><td><code>sort()</code> / <code>reverse()</code></td><td>ordena / inverte <b>no lugar</b></td><td>devolvem <code>None</code></td></tr>
    <tr><td><code>len(l)</code>, <code>l.count(x)</code>, <code>l.index(x)</code></td><td>tamanho, quantas vezes aparece, posição</td><td></td></tr>
  </table></div>
  <div class="nota erro"><span class="lbl">Erro comum</span><b><code>lista = lista.sort()</code>.</b> O <code>sort()</code> ordena no lugar e devolve <code>None</code>, então a variável vira <code>None</code>. Use <code>lista.sort()</code> sozinho, ou <code>nova = sorted(lista)</code> para obter uma cópia ordenada.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Mutável é uma vantagem. Será que também é um risco?</div><p>É, e o risco tem nome: dois nomes para a mesma lista.</p></div>
</section>

<section class="sec" id="mutavel">
  <h2><span class="sn">2</span>Mutável: a pegadinha do "b = a"</h2>
  <p class="gancho">Você achou que copiou a lista. Não copiou.</p>
  <p>Em Python, uma variável guarda uma <b>referência</b> ao objeto. Quando você escreve <code>b = a</code> com listas, os dois nomes apontam para a <b>mesma</b> lista. Quem muda por um nome muda para o outro. Acompanhe:</p>
''' + tr_alias + '''
  <p>Para uma cópia independente, use <code>a.copy()</code> (ou <code>a[:]</code>, ou <code>list(a)</code>). Esse é o mesmo problema que faz uma função que recebe uma lista poder <b>alterar</b> a lista de quem a chamou.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se eu quiser guardar algo que não pode mudar, ou achar um valor pelo nome em vez da posição?</div><p>Há outras coleções.</p></div>
</section>

<section class="sec" id="colecoes">
  <h2><span class="sn">3</span>As quatro coleções nativas (complemento)</h2>
  <p class="gancho">Cada uma resolve um problema diferente.</p>
  <div class="tablewrap"><table>
    <tr><th>Coleção</th><th>Escrita</th><th>Ordenada?</th><th>Mutável?</th><th>Use para</th></tr>
    <tr><td><b>list</b></td><td><code>[1, 2, 3]</code></td><td>sim</td><td>sim</td><td>sequência que cresce e muda</td></tr>
    <tr><td><b>tuple</b> (tupla)</td><td><code>(1, 2, 3)</code></td><td>sim</td><td><b>não</b></td><td>dados fixos (coordenada, data)</td></tr>
    <tr><td><b>dict</b> (dicionário)</td><td><code>{"nome": "Ana", "idade": 19}</code></td><td>pela inserção</td><td>sim</td><td>achar um valor pela <b>chave</b></td></tr>
    <tr><td><b>set</b> (conjunto)</td><td><code>{1, 2, 3}</code></td><td>não</td><td>sim</td><td>valores <b>sem repetição</b>, testar pertencimento</td></tr>
  </table></div>
<pre><code>aluno = {<span class="s">"nome"</span>: <span class="s">"Ana"</span>, <span class="s">"idade"</span>: <span class="n">19</span>}
aluno[<span class="s">"nome"</span>]            <span class="c"># 'Ana'</span>
aluno[<span class="s">"curso"</span>] = <span class="s">"TI"</span>    <span class="c"># acrescenta uma chave nova</span>
<span class="f">set</span>([<span class="n">1</span>, <span class="n">2</span>, <span class="n">2</span>, <span class="n">3</span>, <span class="n">3</span>])        <span class="c"># {1, 2, 3}: os repetidos somem</span></code></pre>
  <p>Na ciência de dados, o <b>DataFrame</b> do pandas é uma tabela que se constrói sobre essas ideias (colunas como listas, linhas como dicionários). Se você chegou até aqui, o resto é questão de prática.</p>
  <h3>Complemento: list comprehension</h3>
  <p>Uma forma compacta e "pythônica" de construir listas a partir de outras:</p>
<pre><code>quadrados = [x ** <span class="n">2</span> <span class="k">for</span> x <span class="k">in</span> <span class="f">range</span>(<span class="n">1</span>, <span class="n">6</span>)]          <span class="c"># [1, 4, 9, 16, 25]</span>
pares     = [x <span class="k">for</span> x <span class="k">in</span> <span class="f">range</span>(<span class="n">10</span>) <span class="k">if</span> x % <span class="n">2</span> == <span class="n">0</span>]   <span class="c"># [0, 2, 4, 6, 8]</span></code></pre>
  <h3>Exercícios do slide, resolvidos</h3>
<pre><code>nums = [<span class="n">4</span>, <span class="n">8</span>, <span class="n">15</span>, <span class="n">16</span>]
<span class="f">sum</span>(nums)                              <span class="c"># 1) soma: 43</span>
<span class="s">", "</span>.<span class="f">join</span>([<span class="s">"a"</span>, <span class="s">"b"</span>, <span class="s">"c"</span>])           <span class="c"># 2) juntar strings: 'a, b, c'</span>
<span class="f">max</span>(nums), <span class="f">min</span>(nums)                    <span class="c"># 3) maior e menor: (16, 4)</span>
<span class="s">"Bob"</span> <span class="k">in</span> [<span class="s">"Alice"</span>, <span class="s">"Bob"</span>]              <span class="c"># 4) nome na lista? True</span>
[x * <span class="n">2</span> <span class="k">for</span> x <span class="k">in</span> nums]                  <span class="c"># 6) cada número vezes 2</span>
<span class="f">all</span>(<span class="f">len</span>(s) &gt; <span class="n">3</span> <span class="k">for</span> s <span class="k">in</span> [<span class="s">"casa"</span>, <span class="s">"sol"</span>])  <span class="c"># 7) todas com mais de 3 letras? False</span>
<span class="f">sorted</span>(nums, reverse=<span class="n">True</span>)          <span class="c"># 8) ordem decrescente</span>
<span class="f">len</span>([x <span class="k">for</span> x <span class="k">in</span> nums <span class="k">if</span> x % <span class="n">2</span> == <span class="n">0</span>])    <span class="c"># 9) quantos são pares: 3</span></code></pre>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Lista</b>: ordenada e <b>mutável</b>. Índice começa em 0; <code>-1</code> é o último.",
    "<code>append</code> (final), <code>insert</code> (posição), <code>extend</code> (junta elementos), <code>remove</code> (por <b>valor</b>), <code>pop</code> (por <b>índice</b>, e devolve).",
    "<code>sort()</code> e <code>reverse()</code> mudam <b>no lugar</b> e devolvem <code>None</code>; <code>sorted()</code> devolve uma cópia.",
    "<code>b = a</code> <b>não copia</b> a lista. Use <code>a.copy()</code>.",
    "<b>tupla</b> (imutável), <b>dicionário</b> (chave → valor), <b>conjunto</b> (sem repetição).",
    "Fatia <code>l[a:b]</code> vai do índice <code>a</code> ao <code>b - 1</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Dada <code>l = [10, 20, 30, 40]</code>, o que é <code>l[1:3]</code>?", [("a","[10, 20, 30]"),("b","[20, 30, 40]"),("c","[20, 30]")], "A fatia começa no índice 1 (incluído) e vai até o 3 (<b>excluído</b>): fica o 20 e o 30.") + quiz(2, "a", "Depois de <code>a = [1, 2]; b = a; b.append(3)</code>, quanto vale <code>a</code>?", [("a","[1, 2, 3]: a e b são a mesma lista."),("b","[1, 2]"),("c","Dá erro.")], "Atribuir uma lista a outra variável só cria outro nome para o mesmo objeto.") + quiz(3, "b", "Qual a diferença entre <code>remove(5)</code> e <code>pop(5)</code>?", [("a","Nenhuma."),("b","remove tira o valor 5; pop tira o elemento do índice 5."),("c","pop só funciona no fim.")], "<code>remove</code> procura pelo valor. <code>pop(i)</code> usa o índice, e ainda devolve o elemento removido.") + flash([
    ("Lista é mutável: o que isso quer dizer?", "Dá para mudar o conteúdo depois de criada, sem criar outra lista."),
    ("sort() x sorted()?", "sort() ordena no lugar e devolve None. sorted() devolve uma nova lista ordenada."),
    ("Para que serve um dicionário?", "Guardar pares chave → valor e achar um valor pela chave."),
    ("Como copiar uma lista de verdade?", "Com a.copy() (ou a[:]). b = a só cria outro nome para a mesma lista.")]) + ponte("Tenho uma coleção de valores. Como aplico o mesmo tratamento a cada um sem escrever 100 vezes?", "Com os laços de repetição.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "listas", T, "Listas e outras coleções", "Capítulo 4 · Aula 5",
        "Guardar muitos valores sob um nome só, mexer neles com segurança e conhecer as outras coleções.",
        ["<b>~40 min</b>", "2 demos · 3 testes · 4 flashcards", "código rastreado"], body4, scripts=S)

# ================= CAP 5 =================
tr_for = trace_html("for: somar de 1 a 5", """soma = 0
for n in range(1, 6):
    soma = soma + n
print(soma)""", notas={1: "<code>soma</code> começa em 0: é o <b>acumulador</b>.", 2: "<code>range(1, 6)</code> gera 1, 2, 3, 4, 5 (o 6 <b>não</b> entra). A cada volta, <code>n</code> assume um valor.", 3: "Soma o valor atual ao acumulador. Observe <code>soma</code> crescer a cada volta.", 4: "Depois que o <code>range</code> acaba, o laço termina e o programa segue."}, max_passos=30)
tr_while = trace_html("while: contagem regressiva", """contador = 3
while contador > 0:
    print(contador)
    contador = contador - 1
print("Fogo!")""", notas={1: "Variável de controle.", 2: "A condição é avaliada <b>antes de cada volta</b>.", 3: "Mostra o valor atual.", 4: "<b>Esta linha é essencial</b>: sem ela, a condição nunca ficaria falsa e o laço seria infinito.", 5: "Condição falsa (0 &gt; 0): o <code>while</code> termina."}, max_passos=30)
tr_break = trace_html("break e continue", """soma = 0
for n in range(1, 8):
    if n == 3:
        continue
    if n == 6:
        break
    soma = soma + n
print(soma)""", notas={3: lambda v: "n = %d: é igual a 3? %s." % (v["n"], "Sim" if v["n"] == 3 else "Não, segue para a próxima linha"), 4: "n = 3: o <code>continue</code> pula o resto <b>desta volta</b> e vai para o próximo n.", 5: lambda v: "n = %d: é igual a 6? %s." % (v["n"], "Sim" if v["n"] == 6 else "Não, segue"), 6: "n = 6: o <code>break</code> <b>sai do laço</b> de vez.", 8: "Somou 1 + 2 + 4 + 5 = 12: o 3 foi pulado e o laço parou no 6."}, max_passos=40)
body5 = recap("No Capítulo 4 você guardou muitos valores numa lista. Falta fazer algo com cada um deles <b>sem escrever o mesmo comando 100 vezes</b>. É a ideia da repetição: um laço.") + '''
<section class="sec" id="for">
  <h2><span class="sn">1</span>for: percorrer uma sequência</h2>
  <p class="gancho">"Para cada item desta coleção, faça isto."</p>
  <p>O <code>for</code> percorre uma <b>sequência</b> (uma lista, uma string, um <code>range</code>). O número de voltas é <b>conhecido</b>: é o tamanho da sequência. A cada volta, a variável do laço assume o próximo valor.</p>
<pre><code><span class="k">for</span> numero <span class="k">in</span> [<span class="n">1</span>, <span class="n">2</span>, <span class="n">3</span>, <span class="n">4</span>, <span class="n">5</span>]:
    <span class="f">print</span>(numero)

<span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">10</span>):      <span class="c"># 0, 1, ..., 9</span>
    <span class="f">print</span>(i)</code></pre>
  <p><code>range(n)</code> vai de 0 a n-1; <code>range(a, b)</code> de a a b-1; <code>range(a, b, passo)</code> pula de <i>passo</i> em <i>passo</i>. O padrão mais importante de todo laço é o <b>acumulador</b>: uma variável que começa num valor neutro e vai juntando algo a cada volta.</p>
''' + tr_for + '''
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se eu não souber quantas vezes vou repetir?</div><p>Por exemplo, pedir a senha até a pessoa acertar.</p></div>
</section>

<section class="sec" id="while">
  <h2><span class="sn">2</span>while: repetir enquanto valer a condição</h2>
  <p class="gancho">O laço que depende do que acontece durante a execução.</p>
  <p>O <code>while</code> repete <b>enquanto uma condição for verdadeira</b>, e a avalia antes de cada volta. Use quando o número de repetições <b>não é conhecido antes</b>: "continue pedindo até digitar um número válido".</p>
''' + tr_while + '''
<pre><code>numero = <span class="f">int</span>(<span class="f">input</span>(<span class="s">"Digite um número maior que 10: "</span>))
<span class="k">while</span> numero &lt;= <span class="n">10</span>:
    numero = <span class="f">int</span>(<span class="f">input</span>(<span class="s">"Não é maior que 10. Tente novamente: "</span>))</code></pre>
  <div class="nota cuidado"><span class="lbl">Regra de bolso</span><b><code>for</code></b> quando você sabe (ou pode calcular) quantas vezes vai repetir; <b><code>while</code></b> quando a parada depende de algo que só se descobre rodando.</div>
  <div class="nota erro"><span class="lbl">Erro comum: loop infinito</span>É quando a condição do <code>while</code> <b>nunca</b> fica falsa, quase sempre porque você esqueceu de atualizar a variável de controle (<code>contador = contador - 1</code>). O programa "trava" sem mensagem de erro. Se acontecer, interrompa com <b>Ctrl + C</b> e releia: "o que muda a cada volta e leva a condição a falhar?"</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E se eu quiser sair do laço no meio, ou pular uma volta?</div><p>Há dois comandos para isso.</p></div>
</section>

<section class="sec" id="break">
  <h2><span class="sn">3</span>break, continue e o else do laço</h2>
  <p class="gancho">Controle fino sobre cada volta.</p>
  <ul>
    <li><code>break</code>: <b>sai do laço</b> imediatamente.</li>
    <li><code>continue</code>: <b>pula</b> o resto desta volta e vai para a próxima.</li>
    <li><code>else</code> num laço (complemento): roda quando o laço <b>terminou sem break</b>. Útil em buscas: "se percorri tudo e não achei...".</li>
  </ul>
''' + tr_break + '''
  <p>Jogue o clássico <b>adivinhação com 3 tentativas</b> (exercício do slide), que usa <code>while</code>, <code>break</code> e o <code>else</code> do laço juntos:</p>
  <div class="demo" data-demo="guess"></div>
  <h3>Os exercícios de laço, resolvidos</h3>
<pre><code><span class="c"># 1 a 50</span>
<span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">1</span>, <span class="n">51</span>): <span class="f">print</span>(i)

<span class="c"># soma de 1 a 10 (55) e produto de 1 a 5 (120)</span>
soma, prod = <span class="n">0</span>, <span class="n">1</span>
<span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">1</span>, <span class="n">11</span>): soma += i
<span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">1</span>, <span class="n">6</span>):  prod *= i

<span class="c"># pares de 2 a 10: o terceiro argumento é o passo</span>
<span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">2</span>, <span class="n">11</span>, <span class="n">2</span>): <span class="f">print</span>(i)

<span class="c"># contagem regressiva de 10 a 1 com "Fogo!"</span>
<span class="k">for</span> i <span class="k">in</span> <span class="f">range</span>(<span class="n">10</span>, <span class="n">0</span>, -<span class="n">1</span>): <span class="f">print</span>(i)
<span class="f">print</span>(<span class="s">"Fogo!"</span>)

<span class="c"># somar positivos até o usuário digitar um negativo</span>
total = <span class="n">0</span>
n = <span class="f">float</span>(<span class="f">input</span>(<span class="s">"Número: "</span>))
<span class="k">while</span> n &gt;= <span class="n">0</span>:
    total += n
    n = <span class="f">float</span>(<span class="f">input</span>(<span class="s">"Número: "</span>))
<span class="f">print</span>(total)</code></pre>
  <div class="nota lembra"><span class="lbl">Complemento: enumerate</span>Quando precisar do índice <b>e</b> do valor: <code>for i, valor in enumerate(lista):</code>. É mais limpo que <code>for i in range(len(lista))</code>. E o laço dos notebooks de ML (<code>for k in range(1, 21)</code>) é exatamente este padrão: testar cada valor de uma coleção.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>for</b>: percorre uma sequência (número de voltas conhecido). <b>while</b>: repete enquanto a condição for verdadeira.",
    "<code>range(a, b, passo)</code> vai de <code>a</code> a <code>b - 1</code>. <code>range(10, 0, -1)</code> conta para trás.",
    "<b>Acumulador</b>: variável que começa neutra (0 na soma, 1 no produto) e junta algo a cada volta.",
    "<b>Loop infinito</b>: a condição nunca fica falsa. Atualize a variável de controle; Ctrl + C para parar.",
    "<code>break</code> sai do laço; <code>continue</code> pula a volta; o <code>else</code> do laço roda se não houve break."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Quantas vezes executa <code>for i in range(3, 8):</code>?", [("a","8"),("b","5 (de 3 a 7)"),("c","6")], "O range inclui o início (3) e exclui o fim (8): 3, 4, 5, 6, 7 são 5 valores.") + quiz(2, "c", "Por que este laço nunca termina? <code>n = 5 / while n &gt; 0: print(n)</code>", [("a","Porque o print é lento."),("b","Porque while só roda uma vez."),("c","Porque n nunca muda, então a condição fica sempre verdadeira.")], "Falta atualizar a variável de controle dentro do laço (por exemplo, <code>n = n - 1</code>).") + quiz(3, "a", "Qual a soma de <code>for n in range(1, 8)</code> com <code>if n == 3: continue</code> e <code>if n == 6: break</code>?", [("a","12 (1 + 2 + 4 + 5)"),("b","28"),("c","21")], "O continue pula o 3 e o break encerra no 6 (sem somar). Sobram 1, 2, 4, 5.") + flash([
    ("for x while?", "for percorre uma sequência de tamanho conhecido. while repete até a condição falhar (número de voltas desconhecido)."),
    ("O que é um acumulador?", "Uma variável que começa num valor neutro e junta algo a cada volta do laço."),
    ("break x continue?", "break sai do laço de vez. continue pula só o resto da volta atual."),
    ("O que gera range(2, 11, 2)?", "2, 4, 6, 8, 10: o terceiro argumento é o passo.")]) + ponte("Já repito e decido. Como organizo dados em duas dimensões e blocos reutilizáveis?", "Com matrizes (listas de listas) e funções.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "lacos", T, "Laços: for e while", "Capítulo 5 · Aulas 5 e 6",
        "Repetir sem copiar e colar: for, while, range, break e os cuidados com o loop infinito.",
        ["<b>~40 min</b>", "4 demos · 3 testes · 4 flashcards", "código rastreado"], body5, scripts=S5)
print("py caps 3-5 ok")
