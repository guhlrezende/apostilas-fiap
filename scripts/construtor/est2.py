import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
from trace_python import trace_html
import est
PASTA, T, S = est.PASTA, est.T, est.S

# ---------------- CAP 4 ----------------
tr_media = trace_html("Média de uma lista de notas", """notas = [7, 8.5, 6, 9]
soma = 0
for n in notas:
    soma = soma + n
media = soma / len(notas)
print(media)""", notas={1: "Uma <b>lista</b> com 4 notas.", 2: "A variável <code>soma</code> começa em zero: é o acumulador.", 3: "O <code>for</code> pega um elemento da lista por vez e o chama de <code>n</code>.", 4: "A cada volta, acrescenta a nota atual à soma.", 5: "Terminado o laço: 30,5 dividido por 4 notas (<code>len</code> conta os elementos).", 6: "7.625: é exatamente a <b>média aritmética</b> do Capítulo 5."})
tr_if = trace_html("Decidir com and, elif e else", """nota = 7.5
frequencia = 50
if nota >= 7 and frequencia >= 75:
    print("Aprovado!")
elif nota >= 5 and frequencia >= 75:
    print("Recuperacao.")
else:
    print("Reprovado.")""", notas={3: "<code>and</code> exige as duas condições. A nota passa (7,5 ≥ 7), mas a frequência não (50 &lt; 75). Resultado: falso.", 5: "A segunda condição também tem <code>frequencia &gt;= 75</code>: também falsa.", 7: "Nenhuma condição foi verdadeira, então cai no <code>else</code>. Uma nota boa não salva uma frequência baixa."})

body4 = recap("A base está planejada (Capítulo 2) e você sabe que tipo de coluna é cada uma (Capítulo 3). Falta a ferramenta que carrega, calcula e desenha. Este capítulo apresenta <b>Python</b> e <b>R</b> lado a lado, do zero até ler um arquivo para um data frame.") + '''
<section class="sec" id="logica">
  <h2><span class="sn">1</span>Lógica, algoritmo e linguagem</h2>
  <p class="gancho">A linguagem é o último passo, não o primeiro.</p>
  <p>Três ideias, nesta ordem: <b>lógica de programação</b> (organizar instruções de forma coerente e em sequência), <b>algoritmo</b> (uma sequência <b>finita, lógica e bem definida</b> de instruções que realiza uma tarefa, como uma receita) e <b>linguagem de programação</b> (o conjunto de regras que permite escrever o algoritmo para o computador). O mesmo algoritmo pode ser escrito em Python, R ou outra linguagem.</p>
  <p>Para ser uma linguagem de programação é preciso ter <b>controle de fluxo</b> (decidir), <b>variáveis</b> (guardar dados), <b>operações lógicas e matemáticas</b> (calcular e comparar) e <b>execução de algoritmos</b>. Por isso <b>HTML não é linguagem de programação</b>: é de <i>marcação</i>. Descreve o que aparece na tela, mas não tem condicional, nem laço, nem manipula dados sozinha.</p>
  <div class="nota cuidado"><span class="lbl">Vibe coding e alucinação</span>Programar sem entender o código, só copiando de uma IA, traz riscos: <b>alucinação</b> (código errado que parece certo), dificuldade de corrigir erros, dependência e aprendizado superficial. Um exemplo real aparece logo adiante: um material de aula traz <code>log(a, base=b)</code> em Python, que <b>dá erro</b> (a sintaxe é de R). Quem só copia não percebe; quem entende, testa e corrige.</div>
</section>

<section class="sec" id="ambientes">
  <h2><span class="sn">2</span>Onde escrever o código</h2>
  <p class="gancho">Quatro tipos de ambiente, do mais completo ao mais leve.</p>
  <div class="tablewrap"><table>
    <tr><th>Ambiente</th><th>O que é</th><th>Exemplo</th><th>Limite</th></tr>
    <tr><td><b>IDE</b></td><td>escreve, executa, testa e depura no mesmo lugar</td><td>PyCharm (Python), RStudio (R)</td><td>mais pesado</td></tr>
    <tr><td><b>Editor de código</b></td><td>edita com destaque de sintaxe</td><td>VS Code</td><td>precisa configurar extensões</td></tr>
    <tr><td><b>Notebook</b></td><td>executa trechos na hora, mistura texto, código e gráfico</td><td>Jupyter</td><td>ruim para projeto grande e versionamento</td></tr>
    <tr><td><b>Compilador online</b></td><td>roda no navegador, sem instalar</td><td>Google Colab</td><td>depende de internet, menos recursos</td></tr>
  </table></div>
  <p>Sobre o <b>Python</b>: linguagem de alto nível, orientada a objetos e de código aberto, criada por Guido van Rossum no CWI (Holanda), com início em 1989 e versão 1.0 em 1994. Vantagens: gratuita, comunidade grande, código legível, multiplataforma. Desvantagens: execução mais lenta que linguagens compiladas e erros que só aparecem na hora de executar (por exemplo, acessar <code>lista[10]</code> numa lista de 2 itens só quebra quando a linha roda). Dica de estilo: a linha vertical do editor (<i>right margin</i>) marca o limite de caracteres por linha, de 79 a 88. <i>Complemento:</i> 79 é o limite da PEP 8 e 88 é o padrão do formatador Black.</p>
</section>

<section class="sec" id="calculadora">
  <h2><span class="sn">3</span>Python e R como calculadora</h2>
  <p class="gancho">As mesmas contas, com símbolos diferentes.</p>
  <div class="tablewrap"><table>
    <tr><th>Operação</th><th>Python</th><th>R</th></tr>
    <tr><td>atribuir</td><td><code>x = 5</code></td><td><code>x &lt;- 5</code></td></tr>
    <tr><td>potência</td><td><code>a ** b</code></td><td><code>a ^ b</code></td></tr>
    <tr><td>resto da divisão</td><td><code>a % b</code></td><td><code>a %% b</code></td></tr>
    <tr><td>quociente inteiro</td><td><code>a // b</code></td><td><code>a %/% b</code></td></tr>
    <tr><td>raiz quadrada</td><td><code>sqrt(a)</code> (de <code>math</code>)</td><td><code>sqrt(a)</code></td></tr>
    <tr><td>valor absoluto</td><td><code>abs(a)</code></td><td><code>abs(a)</code></td></tr>
    <tr><td>fatorial</td><td><code>factorial(a)</code> (de <code>math</code>)</td><td><code>factorial(a)</code></td></tr>
    <tr><td>logaritmo na base b</td><td><code>log(a, b)</code> (de <code>math</code>)</td><td><code>log(a, base = b)</code></td></tr>
    <tr><td>comentário</td><td><code># texto</code></td><td><code># texto</code></td></tr>
  </table></div>
<pre><code><span class="k">from</span> math <span class="k">import</span> sqrt, factorial, log
a, b = 10, 3
a / b            <span class="c"># 3.3333333333333335</span>
a ** b           <span class="c"># 1000</span>
a % b            <span class="c"># 1</span>
a // b           <span class="c"># 3</span>
sqrt(16)         <span class="c"># 4.0</span>
8 ** (1/3)       <span class="c"># 2.0 (raiz cúbica)</span>
factorial(5)     <span class="c"># 120</span>
log(8, 2)        <span class="c"># 3.0</span></code></pre>
  <div class="nota erro"><span class="lbl">Erro comum: copiar a sintaxe de R para Python</span><code>log(8, base=2)</code> funciona em R (devolve 3), mas em Python dá <b>TypeError: math.log() takes no keyword arguments</b>: o segundo argumento só pode ser passado por posição, <code>log(8, 2)</code>. Funções como <code>sqrt</code>, <code>factorial</code> e <code>log</code> também precisam ser importadas do módulo <code>math</code> em Python; em R já vêm prontas.</div>
  <div class="nota lembra"><span class="lbl">A pegadinha do 1</span>Em Python a primeira posição de uma lista é <b>0</b>. Em R, é <b>1</b>. Quem alterna entre as duas linguagens erra por um.</div>
</section>

<section class="sec" id="decidir">
  <h2><span class="sn">4</span>Decidir e repetir</h2>
  <p class="gancho">Condicionais e laços, para o programa reagir e não repetir código à mão.</p>
  <p>Os operadores lógicos são <code>and</code> (todas as condições verdadeiras), <code>or</code> (pelo menos uma) e <code>not</code> (inverte). Em R, <code>&amp;&amp;</code>, <code>||</code> e <code>!</code>. Acompanhe a decisão linha a linha:</p>
  ''' + tr_if + '''
<pre><code><span class="c"># R: a mesma decisão</span>
nota &lt;- 7.5
frequencia &lt;- 50
if (nota &gt;= 7 &amp;&amp; frequencia &gt;= 75) {
  print("Aprovado!")
} else if (nota &gt;= 5 &amp;&amp; frequencia &gt;= 75) {
  print("Recuperacao.")
} else {
  print("Reprovado.")
}</code></pre>
  <p>O <code>for</code> repete para cada elemento de uma sequência (número <b>conhecido</b> de vezes); o <code>while</code> repete <b>enquanto</b> uma condição for verdadeira, e precisa atualizar a variável para não virar laço infinito. Atenção: <code>range(1, 6)</code> vai de 1 a <b>5</b>, o fim não entra. Aqui o laço calcula a média de quatro notas, a primeira medida da estatística descritiva:</p>
  ''' + tr_media + '''
<pre><code><span class="c"># R: mesma média, sem laço (R é vetorizado)</span>
notas &lt;- c(7, 8.5, 6, 9)
mean(notas)    <span class="c"># 7.625</span></code></pre>
  <p>Para <b>reaproveitar</b> código, usa-se <b>função</b>: <code>def area_triangulo(b, h): return (b * h) / 2</code> em Python e <code>area_triangulo &lt;- function(b, h) (b * h) / 2</code> em R. Funções dividem o programa em partes pequenas, reutilizáveis e testáveis.</p>
</section>

<section class="sec" id="objetos">
  <h2><span class="sn">5</span>Objetos e o data frame</h2>
  <p class="gancho">Onde os dados moram.</p>
  <p>Declarar um objeto é atribuir valor (<code>x = 5</code>). Nomes começam com letra, sem espaço, sem acento (evite <code>ç</code>), maiúscula é diferente de minúscula e palavras reservadas (<code>if</code>, <code>for</code>) não valem. Python tem quatro tipos nativos de coleção:</p>
  <div class="tablewrap"><table>
    <tr><th>Tipo</th><th>Exemplo</th><th>Ordem?</th><th>Muda?</th><th>Repete?</th></tr>
    <tr><td><b>Lista</b></td><td><code>[2, 3, 6]</code></td><td>sim</td><td>sim</td><td>sim</td></tr>
    <tr><td><b>Tupla</b></td><td><code>(1, "a", True)</code></td><td>sim</td><td>não</td><td>sim</td></tr>
    <tr><td><b>Dicionário</b></td><td><code>{"nome": "Maria", "idade": 28}</code></td><td>ordem de inserção; acesso por chave</td><td>sim</td><td>chave única</td></tr>
    <tr><td><b>Conjunto</b></td><td><code>{"maçã", "banana"}</code></td><td>não</td><td>sim</td><td>não</td></tr>
  </table></div>
<pre><code>lista2 = [2, 3, 6, 9, 8, 5, 10]
lista2[2:5]     <span class="c"># [6, 9, 8]  (posição 2 até a 4; a 5 não entra)</span>
lista2[10:]     <span class="c"># []         fatia fora do tamanho devolve lista vazia</span>
lista2[10]      <span class="c"># IndexError: posição única inexistente dá erro</span>
set([1, 2, 3, 2, 1])   <span class="c"># {1, 2, 3}  conjunto elimina duplicatas</span></code></pre>
  <p>Em R, o equivalente é o <b>vetor</b> <code>c(2, 3, 6, 9, 8, 5, 10)</code>, e <code>x[3:5]</code> devolve 6, 9, 8 (posições de 1 a 7). Posição inexistente em R devolve <code>NA</code>, e não erro.</p>
  <p>Para <b>dados em tabela</b> essas estruturas não bastam. O <b>data frame</b> é uma tabela de linhas e colunas em que cada coluna pode ter um tipo diferente, parecida com planilha ou com tabela de banco de dados. Em R é nativo; em Python vem da biblioteca <b>pandas</b>:</p>
<pre><code><span class="k">import</span> pandas <span class="k">as</span> pd
tabela = pd.DataFrame({"Nome": ["Ana", "Bruno"], "Idade": [25, 34]})
print(tabela)
<span class="c">#     Nome  Idade
# 0    Ana     25
# 1  Bruno     34</span>

<span class="c"># R</span>
tabela &lt;- data.frame(Nome = c("Ana", "Bruno"), Idade = c(25, 34))</code></pre>
  <p>Comandos úteis: <code>type(x)</code> (classe do objeto), <code>del x</code> (apaga da memória), <code>help("print")</code> (documentação). Bibliotecas extras se instalam com <code>pip install nome</code> e se carregam com <code>import</code>; em R, <code>install.packages("nome")</code> e <code>library(nome)</code>. As mais usadas: pandas e NumPy (dados), Matplotlib e Seaborn (gráficos), scikit-learn (machine learning).</p>
</section>

<section class="sec" id="arquivos">
  <h2><span class="sn">6</span>Ler e escrever arquivos</h2>
  <p class="gancho">Quase todo erro de "meus dados estão estranhos" nasce aqui.</p>
  <p>O arquivo precisa estar no <b>diretório de trabalho</b> (<code>os.getcwd()</code> em Python, <code>getwd()</code> em R) ou você passa o caminho completo. Dois parâmetros decidem se a leitura dá certo: <b><code>sep</code></b> (o separador de colunas) e <b><code>decimal</code></b> (o separador decimal). No Brasil, o CSV costuma usar <code>;</code> como separador, porque a vírgula é o decimal. Teste as combinações:</p>
  <div class="demo" data-demo="csv"></div>
<pre><code><span class="c"># Python (pandas)</span>
df = pd.read_csv("DadosAula.csv", sep=";", decimal=",", header=0)
df = pd.read_excel("DadosAula.xlsx", engine="openpyxl")   <span class="c"># .xlsx precisa do openpyxl</span>
df.to_csv("Novo.csv", sep=";", index=False)               <span class="c"># index=False: sem a coluna 0, 1, 2...</span>

<span class="c"># R</span>
df &lt;- read.csv2("DadosAula.csv")          <span class="c"># read.csv2 já assume sep = ";" e dec = ","</span>
library(readxl); df &lt;- read_excel("DadosAula.xlsx")
write.csv2(df, "Novo.csv", row.names = FALSE)</code></pre>
  <div class="nota lembra"><span class="lbl">Confira sempre depois de ler</span>Três linhas salvam horas: <code>df.shape</code> (linhas e colunas, no R <code>dim(df)</code>), <code>df.dtypes</code> (tipo de cada coluna, no R <code>str(df)</code>) e <code>df.head()</code> (as primeiras linhas, no R <code>head(df)</code>). Se o arquivo mudar, o Python <b>não atualiza sozinho</b>: salve e rode de novo.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">7</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Lógica → algoritmo → linguagem</b>. HTML é marcação, não linguagem de programação. Cuidado com <b>vibe coding</b> e alucinação.",
    "<b>Ambientes</b>: IDE (PyCharm, RStudio), editor (VS Code), notebook (Jupyter) e online (Colab).",
    "Python x R: <code>**</code> x <code>^</code>, <code>%</code> x <code>%%</code>, <code>//</code> x <code>%/%</code>, <code>=</code> x <code>&lt;-</code>, índice começa em <b>0</b> x <b>1</b>. <code>log(8, base=2)</code> só funciona em R.",
    "<b>if/elif/else</b>, <b>for</b> e <b>while</b>, <b>funções</b>; lista, tupla, dicionário, conjunto; <b>data frame</b> (pandas) para dados em tabela.",
    "Ler arquivo: <code>sep</code> e <code>decimal</code> certos; depois confira <code>shape</code>, <code>dtypes</code> e <code>head</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Ao ler um CSV brasileiro com read_csv sem sep=';', o que costuma acontecer?", [("a","Os dados vêm perfeitos."),("b","Tudo vem em uma coluna só, com o cabeçalho inteiro como nome."),("c","O pandas converte para Excel.")], "O separador do arquivo é ';' e o padrão do pandas é ','. Por isso a conferência de shape logo depois de ler.") + quiz(2, "a", "Qual a diferença entre lista2[10:] e lista2[10] numa lista de 7 itens?", [("a","A fatia devolve lista vazia; a posição única dá IndexError."),("b","Ambas dão erro."),("c","Ambas devolvem lista vazia.")], "Fatias fora do tamanho são toleradas; posição única inexistente não.") + quiz(3, "c", "Supondo que <code>from math import sqrt, log</code> já foi feito, qual item funciona em R mas dá erro em Python?", [("a","sqrt(16)"),("b","8 ** (1/3)"),("c","log(8, base=2)")], "O argumento base= só existe no log do R. Em Python: math.log(8, 2).") + flash([
    ("O que é um algoritmo?", "Uma sequência finita, lógica e bem definida de instruções que realiza uma tarefa."),
    ("Para que serve o index=False no to_csv?", "Evita gravar no arquivo a coluna 0, 1, 2... que o pandas cria."),
    ("O que faz read.csv2 em R?", "Lê CSV assumindo sep = ';' e dec = ',', o padrão brasileiro."),
    ("O que é um data frame?", "Uma tabela de linhas e colunas em que cada coluna pode ter um tipo diferente.")]) + ponte("Com a base carregada, vem a pergunta central da estatística descritiva: como resumir tudo isso em poucos números?", "Com medidas de tendência central, dispersão e posição.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "python-e-r", T, "Python e R na prática", "Capítulo 4 · Aulas 3 e 4",
        "Lógica, ambientes, contas, decisões, laços, objetos e leitura de arquivos, em Python e R.",
        ["<b>~55 min</b>", "3 demos · 3 testes · 4 flashcards", "código rastreado e leitura de CSV"], body4, scripts=S)

# ---------------- CAP 5 ----------------
body5 = recap("No Capítulo 4 você calculou a média de quatro notas com um laço, e leu um arquivo para um data frame. Agora resumimos uma coluna inteira em poucos números: onde ela está (<b>tendência central</b>), quanto varia (<b>dispersão</b>) e como se distribui (<b>posição</b>). Este capítulo é um complemento: faz parte da estatística descritiva univariada da ementa.") + '''
<section class="sec" id="centro">
  <h2><span class="sn">1</span>Tendência central: média, mediana e moda</h2>
  <p class="gancho">Três jeitos de responder "qual o valor típico?".</p>
  <ul>
    <li><b>Média</b> (<code>x̄ = Σxᵢ / n</code>): a soma dividida pela quantidade. Usa todos os valores, por isso é sensível a valores extremos.</li>
    <li><b>Mediana</b>: o valor do meio dos dados ordenados (se n é par, a média dos dois do meio). Não liga para extremos.</li>
    <li><b>Moda</b>: o valor mais frequente. Pode não existir ou haver mais de uma. É a única que serve para variável nominal.</li>
  </ul>
  <div class="ex rv"><span class="t">Exemplo resolvido: 9 salários (R$ mil)</span>
    <div class="l"><div>Dados ordenados: <code>3,0 · 3,2 · 3,5 · 3,8 · 4,0 · 4,2 · 4,5 · 5,0 · 5,5</code>.</div></div>
    <div class="l"><div><b>Média</b>: soma = 36,7; <code>36,7 / 9 = <b>4,08</b></code> (4,0778).</div></div>
    <div class="l"><div><b>Mediana</b>: n = 9, o 5º valor ordenado é <b>4,0</b>.</div></div>
    <div class="l"><div><b>Moda</b>: nenhum valor se repete, então <b>não há moda</b>.</div></div>
    <div class="l"><div>Agora entra um novo funcionário que ganha <b>40</b>: média = 76,7 / 10 = <b>7,67</b> e a mediana sobe só de 4,0 para <b>4,1</b>. A média quase dobrou por causa de uma pessoa; a mediana mal se mexeu.</div></div>
  </div>
  <div class="nota lembra"><span class="lbl">A média mente?</span>Quando a distribuição é <b>assimétrica</b> ou há valores extremos (salário, preço de imóvel, tempo de espera), a mediana descreve melhor o "caso típico". Diferença grande entre média e mediana é um sinal de alerta.</div>
</section>

<section class="sec" id="dispersao">
  <h2><span class="sn">2</span>Dispersão: o quanto os dados se espalham</h2>
  <p class="gancho">Duas turmas com a mesma média podem ser bem diferentes.</p>
  <ul>
    <li><b>Amplitude</b>: máximo menos mínimo (sensível a extremos).</li>
    <li><b>Variância</b> amostral: <code>s² = Σ(xᵢ − x̄)² / (n − 1)</code>. Média dos quadrados dos desvios, com <b>n − 1</b> no denominador porque se estima a média com a própria amostra.</li>
    <li><b>Desvio padrão</b>: <code>s = √s²</code>, na mesma unidade do dado.</li>
    <li><b>Coeficiente de variação</b>: <code>CV = s / x̄</code>, em %. Permite comparar variabilidade de variáveis em escalas diferentes.</li>
  </ul>
  <div class="ex rv"><span class="t">Continuando o exemplo dos 9 salários</span>
    <div class="l"><div>Desvios em relação a 4,0778: −1,078; −0,878; −0,578; −0,278; −0,078; +0,122; +0,422; +0,922; +1,422.</div></div>
    <div class="l"><div>Quadrados somam <b>5,416</b>. <code>s² = 5,416 / 8 = <b>0,677</b></code>.</div></div>
    <div class="l"><div><code>s = √0,677 = <b>0,823</b></code> (R$ 823 em torno da média). <code>CV = 0,823 / 4,078 = <b>20,2%</b></code>.</div></div>
    <div class="l"><div>Com o valor extremo 40 incluído: <b>s = 11,39</b> e <b>CV = 148,4%</b>. Um único dado transformou um grupo homogêneo em um grupo "disperso".</div></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado: n ou n − 1?</span>Se você dividir por <b>n</b> em vez de <b>n − 1</b>, os 9 salários dão variância 0,602 em vez de 0,677. Em Python, <code>pandas.Series.var()</code> e <code>statistics.variance</code> usam n − 1, mas <code>numpy.var()</code> usa <b>n</b> por padrão (use <code>ddof=1</code>). Em R, <code>var()</code> e <code>sd()</code> usam n − 1. Para dados de uma <b>amostra</b>, o certo é n − 1.</div>
</section>

<section class="sec" id="posicao">
  <h2><span class="sn">3</span>Posição: quartis, IQR, boxplot e outliers</h2>
  <p class="gancho">Quatro fatias com o mesmo número de observações.</p>
  <p>Os <b>quartis</b> dividem os dados ordenados em quatro partes: <b>Q1</b> (25% abaixo), <b>Q2</b> (a mediana) e <b>Q3</b> (75% abaixo). A <b>distância interquartil</b> é <code>IQR = Q3 − Q1</code>. O <b>boxplot</b> desenha a caixa de Q1 a Q3, o traço da mediana e "bigodes" até os valores mais extremos que <b>não são outliers</b>. Pela regra de Tukey, é <b>outlier</b> o que passa de <code>Q3 + 1,5·IQR</code> ou fica abaixo de <code>Q1 − 1,5·IQR</code>.</p>
  <p>Nos 9 salários: Q1 = 3,5, Q3 = 4,5, IQR = 1,0; limite superior 6,0 e inferior 2,0, então <b>não há outlier</b> (o máximo é 5,5). Com o 40 incluído, Q1 = 3,575, Q3 = 4,875, IQR = 1,3 e limite superior 6,825: o <b>40 é outlier</b>. Teste você mesmo, editando os valores e usando o botão do valor extremo:</p>
  <div class="demo" data-demo="descritiva"></div>
</section>

<section class="sec" id="codigo">
  <h2><span class="sn">4</span>Tudo isso em uma linha de código</h2>
  <p class="gancho">Entender a conta é o que permite confiar na linha.</p>
<pre><code><span class="k">import</span> pandas <span class="k">as</span> pd
sal = pd.Series([3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5])
sal.mean()      <span class="c"># 4.0777...  média</span>
sal.median()    <span class="c"># 4.0        mediana</span>
sal.std()       <span class="c"># 0.8227...  desvio padrão (n - 1)</span>
sal.quantile([.25, .75])   <span class="c"># 3.5 e 4.5</span>
sal.describe()  <span class="c"># count, mean, std, min, 25%, 50%, 75%, max de uma vez</span>

<span class="c"># R</span>
sal &lt;- c(3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5)
mean(sal); median(sal); sd(sal)
quantile(sal, c(.25, .75))
summary(sal)    <span class="c"># mínimo, quartis, mediana, média e máximo</span>
boxplot(sal)</code></pre>
  <p>Os valores de quartis aqui usam <b>interpolação linear</b> (o padrão de pandas, NumPy e R). Planilhas e livros podem usar outros métodos e dar valores levemente diferentes, sobretudo com poucos dados. O que importa é saber qual método está em uso e ser consistente.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Média</b> usa todos os valores (sensível a extremos). <b>Mediana</b> é o valor do meio (robusta). <b>Moda</b> é o mais frequente (a única para nominal).",
    "<b>Variância amostral</b> divide por <b>n − 1</b>; <b>desvio padrão</b> = √variância; <b>CV</b> = desvio / média.",
    "<b>Quartis</b>, <b>IQR</b> = Q3 − Q1 e a regra de Tukey: outlier fora de [Q1 − 1,5·IQR; Q3 + 1,5·IQR].",
    "9 salários: média 4,08, mediana 4,0, desvio 0,823, CV 20,2%. Com o 40: média 7,67, mediana 4,1, desvio 11,39.",
    "Cuidado: <code>numpy.var</code> usa n por padrão; pandas e R usam n − 1."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Um valor extremo muito alto entra nos dados. O que acontece com a média e a mediana?", [("a","A média sobe bastante; a mediana quase não muda."),("b","A mediana sobe mais que a média."),("c","Nenhuma muda.")], "A média usa todos os valores, então o extremo a puxa. A mediana só depende da posição central.") + quiz(2, "b", "Por que a variância amostral divide por n − 1 e não por n?", [("a","Para deixar o número menor."),("b","Porque a média já foi estimada com a própria amostra, o que subestima a dispersão se dividirmos por n."),("c","Porque o último valor não conta.")], "É a correção de Bessel: divide por n − 1 para o estimador não ser viesado para baixo.") + quiz(3, "c", "Q1 = 10 e Q3 = 20. Qual o limite superior para outliers pela regra de Tukey?", [("a","25."),("b","30."),("c","35: Q3 + 1,5 × IQR = 20 + 1,5 × 10.")], "IQR = 10; 1,5 × 10 = 15; 20 + 15 = 35. Acima disso, outlier.") + flash([
    ("Média ou mediana para salários?", "Em geral a mediana, porque salários são assimétricos e têm valores extremos."),
    ("O que é o coeficiente de variação?", "Desvio padrão dividido pela média, em %. Compara variabilidade entre variáveis de escalas diferentes."),
    ("Como o boxplot mostra outliers?", "Como pontos além dos bigodes, fora de Q1 − 1,5·IQR e Q3 + 1,5·IQR."),
    ("Qual a armadilha do numpy.var?", "Divide por n por padrão. Para amostra use ddof=1.")]) + ponte("Resumir uma variável é o começo. O que muda quando há duas variáveis ao mesmo tempo?", "Aparece a correlação, e com ela uma armadilha famosa.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "descritiva", T, "Estatística descritiva (complemento)", "Capítulo 5 · Complemento",
        "Média, mediana, moda, desvio, quartis, boxplot e outliers, com conta à mão e calculadora ao vivo.",
        ["<b>~50 min</b>", "1 demo · 3 testes · 4 flashcards", "calculadora descritiva com boxplot"], body5, scripts=S)

# ---------------- CAP 6 ----------------
body6 = recap("Até aqui cada variável foi analisada sozinha (<b>univariada</b>). Este último capítulo, também um complemento, dá o passo seguinte: <b>duas variáveis juntas</b>, a etapa bivariada do Capítulo 1. É a ponte entre a estatística descritiva e a regressão, que é a base de boa parte do machine learning.") + '''
<section class="sec" id="correlacao">
  <h2><span class="sn">1</span>Correlação de Pearson</h2>
  <p class="gancho">Um número entre −1 e 1 que resume a relação linear entre duas variáveis.</p>
  <p>O <b>coeficiente de correlação de Pearson</b> (<b>r</b>) mede a força e o sentido da relação <b>linear</b> entre duas variáveis quantitativas. <b>r = 1</b>: relação linear perfeita crescente. <b>r = −1</b>: perfeita decrescente. <b>r ≈ 0</b>: nenhuma relação <b>linear</b> (pode haver relação curva!). Ele compara o quanto x e y variam juntos com o quanto cada um varia sozinho: <code>r = Σ(x − x̄)(y − ȳ) / √[Σ(x − x̄)² · Σ(y − ȳ)²]</code>.</p>
  <h3>A reta de regressão e o R²</h3>
  <p>A <b>reta de mínimos quadrados</b> <code>ŷ = a + b·x</code> é a que minimiza a soma dos quadrados dos erros. Sua inclinação é <code>b = Sxy / Sxx</code> e o intercepto <code>a = ȳ − b·x̄</code>. O <b>R²</b> (no caso simples, igual a r²) diz a <b>fatia da variação de y explicada pela reta</b>.</p>
  <div class="ex rv"><span class="t">Exemplo resolvido: 5 pontos</span>
    <div class="l"><div><code>x = 1, 2, 3, 4, 5</code> e <code>y = 2, 4, 5, 4, 5</code>. Médias: <code>x̄ = 3</code> e <code>ȳ = 4</code>.</div></div>
    <div class="l"><div><code>Sxy = Σ(x − 3)(y − 4) = (−2)(−2) + (−1)(0) + 0·1 + 1·0 + 2·1 = <b>6</b></code>. <code>Sxx = 4 + 1 + 0 + 1 + 4 = <b>10</b></code>. <code>Syy = 4 + 0 + 1 + 0 + 1 = <b>6</b></code>.</div></div>
    <div class="l"><div>Inclinação <code>b = 6/10 = <b>0,6</b></code>; intercepto <code>a = 4 − 0,6·3 = <b>2,2</b></code>. A reta é <code>ŷ = 2,2 + 0,6x</code>.</div></div>
    <div class="l"><div><code>r = 6 / √(10·6) = 6 / 7,746 = <b>0,775</b></code> e <code>R² = 0,775² = <b>0,60</b></code>: a reta explica 60% da variação de y.</div></div>
  </div>
<pre><code><span class="k">import</span> numpy <span class="k">as</span> np
x = np.array([1, 2, 3, 4, 5]); y = np.array([2, 4, 5, 4, 5])
np.corrcoef(x, y)[0, 1]     <span class="c"># 0.7746</span>
np.polyfit(x, y, 1)         <span class="c"># [0.6, 2.2]  inclinação e intercepto</span>

<span class="c"># R</span>
x &lt;- c(1, 2, 3, 4, 5); y &lt;- c(2, 4, 5, 4, 5)
cor(x, y)                   <span class="c"># 0.7745967</span>
lm(y ~ x)                   <span class="c"># modelo linear: intercepto 2.2 e inclinação 0.6</span></code></pre>
</section>

<section class="sec" id="anscombe">
  <h2><span class="sn">2</span>Sempre olhe o gráfico: o quarteto de Anscombe</h2>
  <p class="gancho">Quatro conjuntos, os mesmos números, desenhos completamente diferentes.</p>
  <p>Em 1973, o estatístico Francis Anscombe construiu quatro conjuntos de 11 pontos com <b>praticamente as mesmas estatísticas</b>: média de y em 7,5, <b>r ≈ 0,816</b> e a mesma reta <code>ŷ ≈ 3 + 0,5x</code>. Alterne entre eles (e brinque com o ruído dos dados gerados):</p>
  <div class="demo" data-demo="correlacao"></div>
  <p>O I é uma nuvem linear comum. O II é uma <b>curva</b>: a reta é o modelo errado. O III é uma reta perfeita estragada por <b>um outlier</b>. No IV, todos os x são iguais menos um, e <b>um ponto sozinho</b> cria a correlação. A lição é a do Capítulo 5 (a média pode mentir): um número resume, mas pode esconder. <b>Resuma e desenhe, nessa ordem.</b></p>
</section>

<section class="sec" id="causa">
  <h2><span class="sn">3</span>Correlação não é causalidade</h2>
  <p class="gancho">Correlacionar não prova que um causa o outro.</p>
  <p>Duas variáveis podem andar juntas porque <b>uma causa a outra</b>, porque <b>uma terceira causa as duas</b> (a <i>variável de confusão</i>) ou por <b>coincidência</b>. O clássico: vendas de sorvete e afogamentos sobem juntos no verão; o calor é a causa comum, e proibir sorvete não salvaria ninguém. Como vimos no Capítulo 2, só o <b>experimento</b> (variáveis controladas e manipuladas) sustenta causa e efeito; um questionário permite falar em <b>associação</b>.</p>
  <div class="nota lembra"><span class="lbl">O mesmo problema no machine learning</span>Um modelo que aprende "fundo verde = cachorro" aprendeu uma correlação que não tem relação com o conceito. É a variável de confusão disfarçada de feature, o tema do Capítulo 2 da apostila de Redes Neurais.</div>
</section>

<section class="sec" id="adiante">
  <h2><span class="sn">4</span>O caminho até o machine learning</h2>
  <p class="gancho">A estatística do segundo semestre é a base do modelo que você já usa.</p>
  <div class="tablewrap"><table>
    <tr><th>Tema</th><th>Pergunta que responde</th><th>Aparece no machine learning como</th></tr>
    <tr><td><b>Probabilidade e distribuições</b></td><td>quão provável é cada resultado?</td><td>saídas de probabilidade, ruído, incerteza</td></tr>
    <tr><td><b>Inferência</b> (testes, p-valor)</td><td>o que a amostra diz sobre a população?</td><td>validação, intervalos de confiança de métricas</td></tr>
    <tr><td><b>Regressão linear simples e múltipla</b></td><td>como y depende de x (ou de vários x)?</td><td>regressão linear, o modelo-base</td></tr>
    <tr><td><b>Regressão logística</b></td><td>qual a chance de pertencer a uma classe?</td><td>classificação binária (a sigmoide do neurônio)</td></tr>
  </table></div>
  <p>Descrever, entender a incerteza, inferir, relacionar, prever: é o percurso clássico. A regressão linear que você acabou de calcular à mão é o mesmo modelo que o scikit-learn ajusta em uma linha, e o neurônio com ativação linear das redes neurais é, no fundo, a mesma conta.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>r</b> de Pearson: de −1 a 1, mede relação <b>linear</b>. <b>R² = r²</b>: fatia da variação de y explicada pela reta.",
    "Reta de mínimos quadrados: <code>b = Sxy/Sxx</code>, <code>a = ȳ − b·x̄</code>. No exemplo: ŷ = 2,2 + 0,6x, r = 0,775, R² = 0,60.",
    "<b>Anscombe</b>: mesmos r e reta (r ≈ 0,816, ŷ ≈ 3 + 0,5x), formas diferentes. Sempre olhe o gráfico.",
    "<b>Correlação ≠ causalidade</b>: causa comum, coincidência. Só experimento sustenta causa.",
    "Probabilidade, inferência, regressão e regressão logística formam a ponte para o machine learning."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "r = 0 significa que as variáveis não têm nenhuma relação?", [("a","Sim, nenhuma."),("b","Não: significa nenhuma relação linear. Pode haver uma relação curva."),("c","Sim, e o R² também é 1.")], "O Pearson só mede o componente linear; o conjunto II de Anscombe é curvo e tem r alto, e uma parábola simétrica pode ter r próximo de 0.") + quiz(2, "c", "No exemplo resolvido, R² = 0,60. O que isso quer dizer?", [("a","Que 60% dos pontos estão sobre a reta."),("b","Que o erro é de 60%."),("c","Que a reta explica 60% da variação de y.")], "R² é a fração da variância de y que o modelo linear explica.") + quiz(3, "a", "Vendas de sorvete e afogamentos sobem juntos. A melhor explicação é...", [("a","Uma terceira variável (o calor) que afeta as duas."),("b","Sorvete causa afogamento."),("c","Afogamento aumenta a venda de sorvete.")], "É o exemplo clássico de variável de confusão: correlação sem causalidade direta.") + flash([
    ("O que é R²?", "A fração da variação de y explicada pelo modelo (no caso simples, r²)."),
    ("O que o quarteto de Anscombe ensina?", "Que estatísticas iguais podem esconder dados muito diferentes: sempre desenhe o gráfico."),
    ("O que é uma variável de confusão?", "Uma terceira variável que influencia as duas que você observa e cria uma correlação aparente."),
    ("Que comando calcula a correlação em R e em Python?", "R: cor(x, y). Python: np.corrcoef(x, y) ou df.corr().")]) + '''
  <div class="ponte rv"><div class="t">Fim da apostila</div><div class="q">Do dado à relação entre duas variáveis.</div><p>Se algum cálculo ficou nebuloso, refaça o exemplo resolvido no papel e confira na demo. Fazer a conta à mão uma vez é o que faz a linha de código deixar de ser mágica.</p></div>
</section>'''
chapter(PASTA, 6, "correlacao", T, "Correlação e o que vem depois (complemento)", "Capítulo 6 · Complemento",
        "Correlação de Pearson, regressão simples, R² e o quarteto de Anscombe.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "o quarteto de Anscombe ao vivo"], body6, scripts=S)
print("est caps 4-6 ok")
