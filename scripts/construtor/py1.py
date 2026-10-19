from py_manifest import *
T = TITULO
S = ["demos/cap-1-4.js"]

# ================= CAP 1 =================
tr_swap = trace_html("Trocar o conteúdo de A e B", """a = 5
b = 9
temp = a
a = b
b = temp
print(a, b)""", notas={1: "<code>a</code> guarda 5.", 2: "<code>b</code> guarda 9.", 3: "Se fizéssemos <code>a = b</code> já, o 5 se perderia. Guardamos o 5 em uma <b>variável temporária</b>.", 4: "Agora é seguro: <code>a</code> recebe o valor de <code>b</code>.", 5: "<code>b</code> recebe o que estava guardado em <code>temp</code>.", 6: "Trocou! (Em Python existe um atalho: <code>a, b = b, a</code>.)"})
tr_div = trace_html("Divisão: / x // x %", """x = 17
y = 5
print(x / y)
print(x // y)
print(x % y)
print(x ** 2)""", notas={3: "<code>/</code> <b>sempre</b> devolve <code>float</code>, mesmo quando divide certinho.", 4: "<code>//</code> é a divisão inteira: arredonda para baixo.", 5: "<code>%</code> devolve o resto da divisão.", 6: "<code>**</code> é a potência."})
tr_tipos = trace_html("Quatro tipos, quatro caixas", """nome = "Ana"
idade = 19
altura = 1.68
estudante = True
print(type(nome), type(idade))
print(type(altura), type(estudante))
idade = idade + 1
print(idade)""", notas={1: "<code>str</code>: texto, sempre entre aspas.", 2: "<code>int</code>: inteiro.", 3: "<code>float</code>: número com casas decimais (ponto, não vírgula).", 4: "<code>bool</code>: só <code>True</code> ou <code>False</code>, com a primeira letra maiúscula.", 5: "<code>type()</code> pergunta o tipo ao Python. Você não declarou nenhum: ele <b>descobriu pelo valor</b>.", 7: "A <b>variável</b> pode mudar. O Python lê o lado direito primeiro (19 + 1) e depois guarda em <code>idade</code>."})

body1 = recap("Este é o primeiro capítulo. Você não precisa saber programar: precisa só de curiosidade e de um computador. Daqui em diante, cada capítulo abre lembrando a pergunta que o anterior deixou em aberto.", "Ponto de partida") + '''
<section class="sec" id="porque-python">
  <h2><span class="sn">1</span>Por que Python</h2>
  <p class="gancho">Antes do primeiro comando: com que ferramenta estamos trabalhando?</p>
  <p>Python foi criado por <b>Guido van Rossum</b> e lançado em <b>1991</b>, no CWI, na Holanda, com um objetivo bem claro: ter uma sintaxe <mark class="hl">limpa e fácil de ler</mark>, inspirada na linguagem ABC. (O nome vem do grupo de humor Monty Python, e não da cobra.) Isso importa na prática: uma linguagem pensada para a leitura humana deixa você entender o código dos outros sem decorar símbolos.</p>
  <p>Python é de <b>alto nível</b>: fica perto da linguagem humana e esconde o hardware. Você escreve <code>soma = 2 + 2</code> sem saber como o processador guarda o número em binário. Linguagens de <b>baixo nível</b> (como Assembly) mostram esses detalhes. O preço da abstração é velocidade de execução; o ganho é velocidade de <i>desenvolvimento</i>, e no começo é isso que importa.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O computador entende binário. Como o meu texto em Python vira algo que ele executa?</div><p>Há três caminhos, e vale conhecer os três.</p></div>
</section>

<section class="sec" id="traducao">
  <h2><span class="sn">2</span>Compilada, interpretada, transpilada</h2>
  <p class="gancho">Quem traduz o seu código, e quando?</p>
  <div class="grid3">
    <div class="card rv"><b>Compilada</b><p>O código é <b>todo traduzido</b> para código de máquina <b>antes</b> de rodar, gerando um executável. Rápida; mas qualquer mudança exige recompilar. Ex.: C, C++, Rust.</p></div>
    <div class="card rv"><b>Interpretada</b><p>O código é traduzido <b>durante</b> a execução, linha a linha. Você edita e testa na hora. Ex.: Python.</p></div>
    <div class="card rv"><b>Transpilada</b><p>Traduz de uma linguagem de alto nível para <b>outra</b> de alto nível. Ex.: TypeScript vira JavaScript. <span class="muted">(complemento)</span></p></div>
  </div>
  <div class="card sorter rv" data-demo="sorter" data-opts="comp:Compilada|inter:Interpretada|trans:Transpilada">
    <div class="item" data-ans="inter"><p>Você escreve um arquivo <code>.py</code> e o roda direto, e um erro de execução só aparece quando a linha problemática é executada (erros de sintaxe aparecem antes de rodar qualquer linha).</p><span class="why">Interpretada: o Python traduz e executa enquanto lê.</span></div>
    <div class="item" data-ans="comp"><p>Você precisa gerar um executável antes de testar, e qualquer mudança exige gerar de novo (é o passo de <i>build</i> de um projeto C++).</p><span class="why">Compilada: a tradução completa vem antes da execução.</span></div>
    <div class="item" data-ans="trans"><p>O código em TypeScript é convertido em JavaScript, que o navegador entende.</p><span class="why">Transpilada: de uma linguagem de alto nível para outra de alto nível.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <div class="nota lembra"><span class="lbl">Complemento: Python também "compila"</span>Na verdade o Python traduz seu código para um formato intermediário (<i>bytecode</i>, os arquivos <code>.pyc</code>) e só então o interpreta. Por isso se diz "interpretada" no sentido prático: você não gera um executável nativo. O detalhe mostra que a divisão não é tão rígida quanto o slide sugere.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">O programa precisa guardar valores enquanto trabalha. Onde?</div><p>Em variáveis.</p></div>
</section>

<section class="sec" id="variaveis">
  <h2><span class="sn">3</span>Variáveis, constantes e tipos</h2>
  <p class="gancho">Uma caixa com nome, e o que cabe nela.</p>
  <p>Uma <b>variável</b> é um nome associado a um valor na memória, e o valor pode mudar. Uma <b>constante</b> é um valor que não deveria mudar: Python não impede, mas por <i>convenção</i> escreve-se em MAIÚSCULAS (<code>PI = 3.14159</code>). Marcar algo como constante evita que alguém sobrescreva sem querer um valor que devia ser fixo, como uma taxa ou um limite de tentativas.</p>
  <p>Cada valor tem um <b>tipo</b>. Python é <b>dinamicamente tipado</b>: você não declara o tipo (como <code>int x = 5</code> em C), o interpretador descobre pelo valor.</p>
  <div class="tablewrap"><table>
    <tr><th>Tipo</th><th>Representa</th><th>Exemplos</th></tr>
    <tr><td><code>int</code></td><td>inteiros</td><td><code>42</code>, <code>-10</code></td></tr>
    <tr><td><code>float</code></td><td>números com casas decimais</td><td><code>3.14</code></td></tr>
    <tr><td><code>str</code></td><td>texto</td><td><code>'Olá, mundo!'</code></td></tr>
    <tr><td><code>bool</code></td><td>verdadeiro ou falso</td><td><code>True</code>, <code>False</code></td></tr>
    <tr><td><code>list</code></td><td>coleção ordenada e mutável</td><td><code>[1, 2, 3]</code> (Capítulo 4)</td></tr>
  </table></div>
  <p>Acompanhe, linha por linha, o que o Python faz com os quatro tipos:</p>
''' + tr_tipos + '''
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Misturar tipos.</b> <code>"idade: " + 19</code> dá erro (<code>TypeError</code>): não dá para somar texto com número. Converta com <code>str(19)</code>, ou use uma f-string (Capítulo 2). O oposto também: <code>"3" + "4"</code> dá <code>"34"</code> (concatena), e não 7.</div>
  <h3>Operadores matemáticos</h3>
  <div class="tablewrap"><table>
    <tr><th><code>+</code> <code>-</code> <code>*</code></th><th><code>/</code></th><th><code>//</code></th><th><code>%</code></th><th><code>**</code></th></tr>
    <tr><td>soma, subtração, multiplicação</td><td>divisão (sempre <code>float</code>)</td><td>divisão inteira</td><td>resto</td><td>potência</td></tr>
  </table></div>
''' + tr_div + '''
  <p>O <code>%</code> é a base de todo teste de paridade: <code>n % 2 == 0</code> significa "n é par". E <code>/</code> versus <code>//</code> é um dos tropeços mais comuns de quem começa: <code>10 / 2</code> dá <code>5.0</code> (com decimal), e <code>10 // 2</code> dá <code>5</code>.</p>
</section>

<section class="sec" id="troca">
  <h2><span class="sn">4</span>Um desafio clássico: trocar A e B</h2>
  <p class="gancho">Parece trivial, e tem uma armadilha.</p>
  <p>O slide propõe: dadas duas variáveis, <b>trocar o conteúdo</b> de uma pela outra. A tentativa ingênua (<code>a = b</code> e depois <code>b = a</code>) falha, porque a primeira linha já apagou o valor antigo de <code>a</code>. A solução clássica usa uma variável temporária:</p>
''' + tr_swap + '''
  <p>Em Python existe a forma curta <code>a, b = b, a</code>, que faz a mesma troca numa linha. Vale conhecer as duas: a temporária mostra a lógica, e a curta é a que você usa no dia a dia.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Python: criada por <b>Guido van Rossum</b> em <b>1991</b>, de alto nível e feita para ser legível.",
    "<b>Compilada</b>: traduz tudo antes. <b>Interpretada</b>: traduz enquanto executa. <b>Transpilada</b>: converte para outra linguagem de alto nível.",
    "<b>Variável</b> muda; <b>constante</b> (em MAIÚSCULAS, por convenção) não deveria.",
    "Tipos básicos: <code>int</code>, <code>float</code>, <code>str</code>, <code>bool</code> (e <code>list</code>). Tipagem <b>dinâmica</b>.",
    "<code>/</code> sempre devolve <code>float</code>; <code>//</code> é divisão inteira; <code>%</code> é o resto; <code>**</code> é potência.",
    "Para trocar duas variáveis: use uma <b>temporária</b>, ou <code>a, b = b, a</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual o resultado de <code>17 // 5</code> e de <code>17 % 5</code>?", [("a","3,4 e 2"),("b","4 e 3"),("c","3 e 2")], "17 dividido por 5 dá 3 com resto 2. <code>//</code> devolve o quociente inteiro (3), e <code>%</code> o resto (2). <code>17 / 5</code> seria 3.4.") + quiz(2, "b", "Por que <code>a = b</code> seguido de <code>b = a</code> NÃO troca os valores?", [("a","Porque Python não permite duas atribuições seguidas."),("b","Porque a primeira linha apaga o valor antigo de a, e a segunda copia o mesmo valor de volta."),("c","Porque b é constante.")], "Depois de <code>a = b</code>, ambos valem o valor de b. Faltou guardar o valor antigo de a em algum lugar, a variável temporária.") + quiz(3, "a", "<code>type(3.0)</code> devolve:", [("a","float: o ponto decimal faz dele um float, mesmo com valor inteiro."),("b","int, porque 3.0 é igual a 3."),("c","str")], "O tipo vem da forma como o valor é escrito. <code>3</code> é int; <code>3.0</code> é float.") + flash([
    ("Compilada x interpretada?", "Compilada traduz o programa inteiro antes de rodar. Interpretada traduz durante a execução, linha a linha."),
    ("O que é tipagem dinâmica?", "Você não declara o tipo da variável: o Python descobre pelo valor guardado."),
    ("Para que serve o %?", "Devolve o resto da divisão. Base do teste de par e ímpar (<code>n % 2 == 0</code>)."),
    ("Como trocar duas variáveis?", "Com uma variável temporária, ou com <code>a, b = b, a</code>.")]) + ponte("Já sei guardar valores. Como faço o programa receber dados de quem o usa?", "Com a função <code>input()</code>, e um cuidado: ela sempre devolve texto.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "linguagens-e-variaveis", T, "Linguagens, variáveis e tipos", "Capítulo 1 · Aula 1",
        "Como o Python vira ação no computador, onde ele guarda valores, e as primeiras contas.",
        ["<b>~35 min</b>", "4 demos · 3 testes · 4 flashcards", "código rastreado"], body1, scripts=S)

# ================= CAP 2 =================
tr_soma = trace_html("Somar dois números lidos do usuário", """num = int(input('Digite um numero: '))
num2 = int(input('Digite outro numero: '))
resultado = num + num2
print(resultado)""", entradas=["7", "5"], notas={1: "<code>input()</code> devolve o <b>texto</b> '7'. O <code>int()</code> converte para o número 7.", 2: "Mesma coisa para o segundo valor.", 3: "Agora a soma é aritmética: 7 + 5.", 4: "Se não tivéssemos convertido, <code>'7' + '5'</code> daria <code>'75'</code>."})
tr_fah = trace_html("Fahrenheit para Celsius", """Fah = float(input("Temperatura em Fahrenheit: "))
C = (Fah - 32) * 5 / 9
print(C)
print(f"Em Celsius: {C:.2f}")
print(f"Com 4 casas: {C:.4f}")""", entradas=["94.3"], notas={1: "<code>float()</code> porque a entrada tem casa decimal. <code>int('94.3')</code> daria erro.", 2: "Os parênteses forçam a subtração antes da multiplicação. Sem eles, o resultado seria outro.", 3: "O valor bruto tem muitas casas: 34.611111...", 4: "<code>:.2f</code> arredonda <b>só na hora de mostrar</b>. A variável <code>C</code> continua com o valor completo."})
tr_tempo = trace_html("Tempo de percurso: horas e minutos", """distancia = float(input("Distancia em km: "))
vel_med = float(input("Velocidade media em km/h: "))
resultado = distancia / vel_med
horas = int(resultado)
minutos = int((resultado - horas) * 60)
print(f"Tempo: {horas}h e {minutos}min")""", entradas=["150", "60"], notas={3: "150 / 60 = 2.5 horas.", 4: "<code>int()</code> descarta a parte decimal: sobram 2 horas inteiras.", 5: "O que sobrou (0.5 hora) vira minutos: 0.5 × 60 = 30.", 6: "Esta é a versão corrigida do exercício: mostra horas <b>e</b> minutos."})

body2 = recap("No Capítulo 1 você guardou valores em variáveis e viu os tipos. Faltava o programa <b>conversar</b>: receber dados de quem o usa, calcular e devolver uma resposta bem escrita.") + '''
<section class="sec" id="input">
  <h2><span class="sn">1</span>input(): sempre texto</h2>
  <p class="gancho">O usuário digitou 7. O que chegou ao programa?</p>
  <p>A função <code>input()</code> lê o que a pessoa digita e <b>sempre devolve um <code>str</code></b> (texto), mesmo que ela digite um número. Para fazer conta, você precisa converter: <code>int(...)</code> para inteiros, <code>float(...)</code> para números com casas decimais. Esse é o bug número 1 dos primeiros exercícios.</p>
''' + tr_soma + '''
  <div class="nota erro"><span class="lbl">Erro comum</span><b>Esquecer de converter.</b> Sem o <code>int()</code>, <code>'7' + '5'</code> vira <code>'75'</code> (concatenação), e <code>'7' * 2</code> vira <code>'77'</code>. Se a pessoa digitar casas decimais e você usou <code>int()</code>, o Python dá <code>ValueError</code>: use <code>float()</code>. (No Capítulo 9 você vê como tratar essa digitação errada sem o programa quebrar.)</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E agora que a entrada virou número, que contas faço com ela?</div><p>As quatro operações da aula, em quatro problemas de verdade.</p></div>
</section>

<section class="sec" id="exercicios">
  <h2><span class="sn">2</span>Quatro problemas, quatro contas</h2>
  <p class="gancho">Transformar o enunciado em fórmula, e a fórmula em código.</p>
  <p>Os exercícios do primeiro bloco aplicam os operadores. Veja como cada um vira código:</p>
<pre><code><span class="c"># 1) Área de um círculo de raio r:  área = π · r²</span>
PI = <span class="n">3.14159</span>
raio = <span class="f">float</span>(<span class="f">input</span>(<span class="s">"Raio: "</span>))
area = PI * raio ** <span class="n">2</span>
<span class="f">print</span>(<span class="s">f"A área é {area:.2f}"</span>)

<span class="c"># 3) Total gasto: 3 livros a R$ 25 e 2 canetas a R$ 5</span>
total = <span class="n">3</span> * <span class="n">25</span> + <span class="n">2</span> * <span class="n">5</span>        <span class="c"># 85</span>
<span class="f">print</span>(<span class="s">f"R$ {total:.2f}"</span>)  <span class="c"># R$ 85.00</span></code></pre>
  <p>O problema 2 (Fahrenheit para Celsius) é o melhor para observar a formatação: o valor bruto com 94,3 °F é <code>34.611111111111114</code>, e o <code>:.2f</code> mostra <code>34.61</code>.</p>
''' + tr_fah + '''
  <p>E o problema 4 (150 km a 60 km/h). A primeira versão da aula calculava <code>horas</code> e <code>minutos</code>, mas imprimia só o <code>resultado</code> (2.5), o que é uma <b>pendência clássica</b>: calculou e esqueceu de mostrar. A versão corrigida:</p>
''' + tr_tempo + '''
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Esse <code>:.2f</code> controla o que aparece. Que outros formatos existem?</div><p>Brinque com eles.</p></div>
</section>

<section class="sec" id="fstring">
  <h2><span class="sn">3</span>f-strings: texto com variáveis dentro</h2>
  <p class="gancho">Montar uma frase com valores sem somar pedaços de texto.</p>
  <p>Uma <b>f-string</b> começa com <code>f</code> antes das aspas e aceita variáveis (e até contas) dentro de <code>{ }</code>. Depois de dois-pontos vem o <b>formato</b>: <code>{valor:.2f}</code> mostra 2 casas decimais. Teste vários:</p>
  <p class="muted">Em aula só apareceram os formatos <code>:.2f</code> e <code>:.4f</code>; os demais da demo (vírgula, %, notação científica, largura e alinhamento) são <b>complemento</b>.</p>
  <div class="demo" data-demo="fmt"></div>
  <div class="nota lembra"><span class="lbl">Lembra</span>O formato <b>só muda o que aparece</b> no <code>print</code>. A variável continua guardando o valor completo. Por isso você formata na hora de mostrar, e não antes de calcular (arredondar no meio da conta acumula erro).</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<code>input()</code> <b>sempre</b> devolve <code>str</code>. Converta com <code>int()</code> ou <code>float()</code>.",
    "<code>int()</code> quebra com casas decimais digitadas: use <code>float()</code> nesse caso.",
    "Parênteses mandam na ordem das contas: <code>(Fah - 32) * 5 / 9</code>.",
    "<b>f-string</b>: <code>f\"texto {variavel:.2f}\"</code>. O formato só afeta a saída.",
    "<code>int(2.5)</code> corta a parte decimal (dá 2); é como se calculam horas e minutos separados."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "O que <code>print(input() + input())</code> mostra se o usuário digitar 3 e depois 4?", [("a","7"),("b","34"),("c","Um erro")], "Os dois <code>input()</code> devolvem texto, e <code>+</code> entre textos concatena: '3' + '4' = '34'.") + quiz(2, "a", "Com <code>x = 2.0 / 3</code>, o que mostra <code>print(f\"{x:.2f}\")</code>?", [("a","0.67, e x continua guardando 0.6666666666666666."),("b","0.67, e x passa a valer 0.67."),("c","0")], "O formato só atua na saída. A variável mantém o valor completo.") + quiz(3, "c", "Para ler a temperatura 36.5 digitada, qual conversão usar?", [("a","int(input())"),("b","str(input())"),("c","float(input())")], "<code>int('36.5')</code> dá <code>ValueError</code>. Com casas decimais, é float.") + flash([
    ("Por que converter o input?", "Porque ele devolve texto, e conta com texto concatena (ou dá erro) em vez de somar."),
    ("O que faz :.2f?", "Mostra o número com 2 casas decimais, arredondando só na saída."),
    ("int(7.9) dá quanto?", "7. O int() corta a parte decimal, não arredonda."),
    ("O que é uma f-string?", "Uma string com f antes das aspas, que aceita {variáveis} e formatos dentro.")]) + ponte("O programa lê e calcula, mas faz sempre a mesma coisa. Como ele decide o que fazer?", "Com as estruturas condicionais: if, elif e else.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "entrada-e-f-strings", T, "Entrada, operadores e f-strings", "Capítulo 2 · Aula 2",
        "Ler dados do usuário, fazer contas com eles e mostrar a resposta bem formatada.",
        ["<b>~35 min</b>", "4 demos · 3 testes · 4 flashcards", "código rastreado"], body2, scripts=S)
print("py caps 1-2 ok")
