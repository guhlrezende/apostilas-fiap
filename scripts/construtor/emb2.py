import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
import emb
PASTA, T, S = emb.PASTA, emb.T, emb.S

# ---------------- CAP 4 ----------------
body4 = recap("No Capítulo 3 o LED piscou com um <code>setup()</code> e um <code>loop()</code> que você ainda não abriu. Agora o modelo de execução, o <b>Monitor Serial</b> (a janela do ESP32 para o mundo) e as <b>quatro estruturas</b> que formam qualquer lógica de programação.") + '''
<section class="sec" id="modelo">
  <h2><span class="sn">1</span>O modelo: setup uma vez, loop para sempre</h2>
  <p class="gancho">Você escreve duas funções; o framework as chama.</p>
  <p>Todo programa de ESP32 no estilo Arduino tem as duas funções, e quem as chama é o framework, e não você. Na prática é como se o firmware fizesse:</p>
<pre><code>setup();            <span class="c">// uma vez, logo depois de ligar ou reiniciar</span>
while (true) {
  loop();           <span class="c">// repetidamente, enquanto houver energia</span>
}</code></pre>
  <div class="tablewrap"><table>
    <tr><th>Função</th><th>Quando roda</th><th>Para quê</th></tr>
    <tr><td><code>void setup()</code></td><td>uma única vez</td><td>inicializar: <code>Serial.begin()</code>, <code>pinMode()</code>, conexões, sensores</td></tr>
    <tr><td><code>void loop()</code></td><td>continuamente</td><td>operar: ler sensores, decidir, acionar saídas, imprimir</td></tr>
  </table></div>
  <p>Consequência prática: <b>o valor que precisa sobreviver entre as voltas do <code>loop()</code> não pode ser declarado dentro dele</b>. Variáveis declaradas dentro de uma função são <b>locais</b> (recriadas a cada chamada). Variáveis declaradas <b>fora</b> de qualquer função são <b>globais</b> e mantêm o valor.</p>
</section>

<section class="sec" id="serial">
  <h2><span class="sn">2</span>O Monitor Serial</h2>
  <p class="gancho">Como a placa fala com você.</p>
  <ul>
    <li><code>Serial.begin(115200)</code> abre a comunicação serial a 115200 bits por segundo (a <i>velocidade de comunicação</i>). O Monitor Serial precisa estar configurado na <b>mesma</b> velocidade; senão aparecem caracteres aleatórios.</li>
    <li><code>Serial.println(x)</code> imprime e <b>quebra a linha</b>. <code>Serial.print(x)</code> imprime <b>sem</b> quebrar. Ambos aceitam texto e números.</li>
    <li>Todo comando termina em <code>;</code>: o compilador usa o ponto e vírgula, e não a quebra de linha, como delimitador.</li>
  </ul>
  <p>Experimente: mude se a variável é global ou local, se a impressão quebra linha e o <code>delay</code>:</p>
  <div class="demo" data-demo="serial"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: o contador que não conta</span>
    <div class="l"><div>Código: <code>void loop() { int id = 0; id = id + 1; Serial.println(id); delay(2000); }</code>.</div></div>
    <div class="l"><div>A cada volta, o <code>int id = 0;</code> roda de novo: <code>id</code> é recriado como 0, soma 1 e imprime <b>1</b>. Sempre 1.</div></div>
    <div class="l"><div>Correção: mover <code>int id = 0;</code> para <b>fora</b> do <code>loop()</code>, antes do <code>setup()</code>. Agora <code>id</code> é criado uma só vez, e o <code>id = id + 1</code> acumula: 1, 2, 3...</div></div>
  </div>
</section>

<section class="sec" id="logica">
  <h2><span class="sn">3</span>As quatro estruturas da lógica de programação</h2>
  <p class="gancho">Sequência, decisão, repetição e função.</p>
  <div class="grid2">
    <div class="card rv"><b>1. Instruções sequenciais</b><p>Executadas uma após a outra, na ordem, como uma receita.</p><pre><code>int a = 5;
int b = 2;
int resultado = a + b;</code></pre></div>
    <div class="card rv"><b>2. Condicionais</b><p>Decisões a partir de uma condição.</p><pre><code>int temperatura = 32;
if (temperatura &gt; 30) {
  Serial.println("Ligue o ventilador.");
} else {
  Serial.println("Temperatura agradável.");
}</code></pre></div>
    <div class="card rv"><b>3. Repetição</b><p>Repete sem você escrever cada vez.</p><pre><code>for (int i = 1; i &lt;= 10; i++) {
  Serial.println("Flexão número " + String(i));
}</code></pre></div>
    <div class="card rv"><b>4. Funções</b><p>Um bloco com nome, chamado quando preciso.</p><pre><code>void abrirPorta() {
  Serial.println("Girando a maçaneta...");
  Serial.println("Porta aberta!");
}
void setup() {
  Serial.begin(115200);
  abrirPorta();
}</code></pre></div>
  </div>
  <p>É a mesma lógica que você usa em Python, com duas diferenças: <b>chaves <code>{ }</code> e ponto e vírgula</b> em vez de indentação, e o programa é <b>compilado</b>, em vez de interpretado.</p>
  <div class="nota lembra"><span class="lbl">Uma regra de organização</span>Em qualquer aplicação: (1) defina os sensores e atuadores; (2) atribua os <b>pinos</b> antes do <code>setup()</code> (<code>#define LED 22</code> ou <code>const int LED = 22;</code>); (3) configure cada pino no <code>setup()</code>, com <code>INPUT</code> para sensor e <code>OUTPUT</code> para atuador. Trocar um pino fica sendo editar um só lugar.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<code>setup()</code> roda <b>uma vez</b>; <code>loop()</code> repete <b>para sempre</b>. O framework chama as duas.",
    "<code>Serial.begin(115200)</code> e o monitor na <b>mesma velocidade</b>. <code>println</code> quebra linha; <code>print</code> não.",
    "Estado que sobrevive entre voltas do loop = variável <b>global</b>. Dentro do loop é <b>local</b> e é recriada.",
    "Quatro estruturas: sequência, condicional (<code>if/else</code>), repetição (<code>for</code>) e função.",
    "Organize: pinos antes do <code>setup()</code>, <code>pinMode</code> no <code>setup()</code>, uso no <code>loop()</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Um contador declarado dentro do loop() imprime sempre 1. Por quê?", [("a","Porque o delay reinicia a placa."),("b","Porque a variável local é recriada em 0 a cada volta."),("c","Porque println só imprime 1.")], "Variáveis locais vivem só durante a chamada. Para guardar o valor, declare fora do loop().") + quiz(2, "a", "O Monitor Serial mostra caracteres aleatórios. Qual a causa mais provável?", [("a","Velocidade diferente de 115200 no monitor."),("b","Falta de ponto e vírgula."),("c","O LED está ao contrário.")], "As duas pontas da comunicação precisam usar a mesma velocidade.") + quiz(3, "c", "Qual a diferença entre print e println?", [("a","println só imprime números."),("b","print é mais rápido."),("c","println quebra a linha ao final; print não.")], "Com print, as saídas ficam grudadas na mesma linha.") + flash([
    ("O que roda no setup()?", "A inicialização, uma única vez: Serial.begin, pinMode, configurações."),
    ("Variável global x local?", "Global é declarada fora das funções e mantém o valor. Local é declarada dentro e é recriada a cada chamada."),
    ("Por que o delay trava o programa?", "Porque é uma pausa bloqueante: o processador espera, sem fazer mais nada."),
    ("Qual a diferença de sintaxe C++ x Python?", "C++ usa chaves e ponto e vírgula; Python usa indentação.")]) + ponte("Guardamos valores em variáveis. Que tipos existem, e como imprimir cada um do jeito certo?", "Tipos, strings, operadores e printf.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "setup-loop-serial", T, "setup, loop, Serial e a lógica", "Capítulo 4 · Aulas 2, 4 e 6",
        "O modelo de execução do ESP32, o Monitor Serial, variáveis globais e as quatro estruturas da lógica.",
        ["<b>~45 min</b>", "1 demo · 3 testes · 4 flashcards", "Monitor Serial simulado"], body4, scripts=S)

# ---------------- CAP 5 ----------------
body5 = recap("No Capítulo 4 você viu que variáveis guardam valores. Falta saber <b>que tipos existem</b>, como o texto é guardado (e por que há três jeitos), como comparar e como imprimir tudo isso com formato.") + '''
<section class="sec" id="tipos">
  <h2><span class="sn">1</span>Tipos primitivos</h2>
  <p class="gancho">A variável precisa saber o que guarda.</p>
<pre><code>int idade = 18;            <span class="c">// inteiro</span>
float temperatura = 27.5;  <span class="c">// decimal</span>
char letra = 'N';          <span class="c">// um único caractere (aspas simples)</span>
String nome = "ESP 32";    <span class="c">// texto (classe do Arduino)</span>
bool ligado = true;        <span class="c">// verdadeiro ou falso</span></code></pre>
  <div class="card sorter rv" data-demo="sorter" data-opts="i:int|fl:float|c:char|s:String|b:bool">
    <div class="item" data-ans="b"><p>Se a luz está ligada: sim ou não.</p><span class="why">Dois estados possíveis: bool.</span></div>
    <div class="item" data-ans="fl"><p>A temperatura 27,5 °C.</p><span class="why">Tem parte decimal: float.</span></div>
    <div class="item" data-ans="i"><p>O número de pessoas na sala.</p><span class="why">Contagem inteira: int.</span></div>
    <div class="item" data-ans="c"><p>A letra 'N' (um único caractere).</p><span class="why">Um caractere, entre aspas simples: char.</span></div>
    <div class="item" data-ans="s"><p>A mensagem "Sistema ligado".</p><span class="why">Texto com vários caracteres: String.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <p>No Monitor Serial, um <code>float</code> sai com 2 casas por padrão (<code>20.50</code>) e um <code>bool</code> sai como <code>1</code> ou <code>0</code>, e não como <i>true</i>/<i>false</i>.</p>
</section>

<section class="sec" id="texto">
  <h2><span class="sn">2</span>Três jeitos de guardar texto</h2>
  <p class="gancho">O texto é uma sequência de caracteres, e o final precisa ser marcado.</p>
  <h3>1. char array (C-string)</h3>
<pre><code>char palavra[6] = "ESP32";   <span class="c">// 5 letras, mas o array precisa de 6</span></code></pre>
  <div class="tablewrap"><table>
    <tr><th>índice</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
    <tr><td>valor</td><td>E</td><td>S</td><td>P</td><td>3</td><td>2</td><td><code>\\0</code></td></tr>
  </table></div>
  <p>O sexto espaço guarda o <b>caractere nulo <code>\\0</code></b>, que marca onde o texto termina. Por isso o tamanho é sempre <b>o número de caracteres visíveis + 1</b>; <code>char texto[5] = "ESP32";</code> é erro. <code>palavra[1]</code> vale <code>'S'</code>. Um caractere usa aspas <b>simples</b> (<code>'S'</code>); um texto usa aspas <b>duplas</b> (<code>"ESP32"</code>).</p>
  <h3>2. std::string e 3. String do Arduino</h3>
<pre><code>String texto = "ESP32";
texto += ": funcionando!";     <span class="c">// concatena (equivale a texto = texto + ...)</span>
Serial.println(texto);</code></pre>
  <p>O <code>std::string</code> é da biblioteca padrão do C++. No ESP32 recomenda-se a classe <code>String</code> (S maiúsculo) do Arduino, que gerencia a memória sozinha. Mas há um <b>ponto de atenção real de engenharia</b>: <code>String</code> facilita a manipulação, porém <b>pode fragmentar a memória</b>, ruim em dispositivos com pouca RAM que rodam por muito tempo e concatenam muito. Em código de produção, às vezes o <code>char</code> array é preferível.</p>
</section>

<section class="sec" id="operadores">
  <h2><span class="sn">3</span>Operadores e a pegadinha do = e ==</h2>
  <p class="gancho">Atribuir não é comparar.</p>
  <div class="tablewrap"><table>
    <tr><th>Operador</th><th>Significado</th><th>Exemplo</th></tr>
    <tr><td><code>+ - * /</code></td><td>soma, subtração, multiplicação, divisão</td><td><code>5+3</code>, <code>2*6</code></td></tr>
    <tr><td><code>%</code></td><td>resto da divisão</td><td><code>10 % 3</code> = 1</td></tr>
    <tr><td><code>++ --</code></td><td>incremento e decremento</td><td><code>x++</code></td></tr>
    <tr><td><code>=</code></td><td><b>atribui</b></td><td><code>a = 5;</code></td></tr>
    <tr><td><code>== !=</code></td><td><b>compara</b> (igual, diferente)</td><td><code>idade == 20</code> → <code>true</code> ou <code>false</code></td></tr>
    <tr><td><code>&gt; &lt; &gt;= &lt;=</code></td><td>maior, menor, maior ou igual, menor ou igual</td><td><code>temp &gt; 35</code></td></tr>
  </table></div>
  <p>O resultado de uma comparação é um <code>bool</code>, que o Monitor Serial imprime como <code>1</code> (verdadeiro) ou <code>0</code> (falso). Comentários usam <code>//</code>.</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: divisão de inteiros</span>Em C++, <code>10 / 4</code> com dois <code>int</code> dá <b>2</b>, e não 2,5: a divisão entre inteiros é inteira. Para ter decimais, ao menos um dos lados precisa ser <code>float</code> (<code>10.0 / 4</code>). Teste junto com o <code>printf</code> na demo abaixo.</div>
</section>

<section class="sec" id="printf">
  <h2><span class="sn">4</span>Imprimir com formato: printf</h2>
  <p class="gancho">Concatenar String é caro; o printf é direto.</p>
<pre><code>float media = 27.456;
Serial.printf("A temperatura média é: %.2f ºC\\r\\n", media);   <span class="c">// 27.46</span>

String nome = "ESP32";
Serial.printf("Placa: %s\\r\\n", nome.c_str());   <span class="c">// %s com String exige .c_str()</span></code></pre>
  <p>Marcadores: <code>%d</code> inteiro, <code>%.2f</code> decimal com 2 casas (<code>%.7f</code>, 7 casas), <code>%c</code> caractere, <code>%s</code> texto. O <code>printf</code> <b>não quebra linha sozinho</b>: coloque <code>\\n</code> (ou <code>\\r\\n</code>, que funciona bem no Monitor Serial). Teste:</p>
  <div class="demo" data-demo="formato"></div>
  <h3>Operador ternário</h3>
<pre><code>bool ligado = true;
Serial.println(ligado ? "ligado" : "desligado");   <span class="c">// condição ? se_verdadeiro : se_falso</span></code></pre>
  <div class="ex rv"><span class="t">Exemplo resolvido: Celsius para Fahrenheit</span>
    <div class="l"><div>Fórmula: <code>F = C × 1,8 + 32</code>. Para <b>27,5 °C</b>: <code>27,5 × 1,8 = 49,5</code>; <code>49,5 + 32 = <b>81,5 °F</b></code>.</div></div>
    <div class="l"><div>Em código: <code>float c = 27.5; float f = c * 1.8 + 32; Serial.printf("%.1f C = %.1f F\\r\\n", c, f);</code> imprime <code>27.5 C = 81.5 F</code>.</div></div>
  </div>
</section>

<section class="sec" id="leitura">
  <h2><span class="sn">5</span>Ler comandos pelo Monitor Serial</h2>
  <p class="gancho">A comunicação é de mão dupla.</p>
<pre><code>void loop() {
  if (Serial.available() &gt; 0) {                 <span class="c">// só entra se há algo no buffer</span>
    String cmd = Serial.readStringUntil('\\n');   <span class="c">// lê até o Enter</span>
    cmd.trim();                                  <span class="c">// tira espaços e \\r</span>
    if (cmd == "ligar")         digitalWrite(LED, HIGH);
    else if (cmd == "desligar") digitalWrite(LED, LOW);
  }
}</code></pre>
  <p><code>Serial.available()</code> diz se há algo esperando. <code>Serial.readStringUntil('\\n')</code> é <b>bloqueante</b>: trava o <code>loop()</code>, acumulando caracteres até achar o <code>\\n</code> ou estourar o tempo limite (<i>timeout</i>). Por isso se testa <code>available() &gt; 0</code> <b>antes</b>: é o padrão "verificar antes de bloquear". (O slide da aula fala em 5 s de tempo limite; o padrão do núcleo Arduino costuma ser 1 s, e <code>Serial.setTimeout()</code> muda. Confira na sua versão.)</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Tipos: <code>int</code>, <code>float</code>, <code>char</code> (aspas simples), <code>String</code> (aspas duplas), <code>bool</code> (imprime 1 ou 0).",
    "<b>char array</b> precisa de <b>tamanho + 1</b> por causa do <code>\\0</code>. <code>String</code> é prático, mas pode <b>fragmentar a memória</b>.",
    "<code>=</code> atribui; <code>==</code> compara. Divisão de <b>inteiros é inteira</b>: <code>10/4 = 2</code>.",
    "<code>printf</code>: <code>%d</code>, <code>%.2f</code>, <code>%c</code>, <code>%s</code> (com <code>.c_str()</code>); não quebra linha sozinho.",
    "Ler pelo Serial: <code>available() &gt; 0</code> antes de <code>readStringUntil('\\n')</code>, que bloqueia."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual o tamanho mínimo do array para guardar a palavra 'ESP32' como char array?", [("a","5."),("b","4."),("c","6: 5 letras mais o caractere nulo \\0.")], "O \\0 marca o fim do texto e ocupa uma posição.") + quiz(2, "a", "Quanto é 10 / 4 com dois int em C++?", [("a","2."),("b","2,5."),("c","3.")], "A divisão entre inteiros descarta a parte decimal. Com float (10.0 / 4), seria 2,5.") + quiz(3, "b", "Por que testar Serial.available() > 0 antes de readStringUntil?", [("a","Porque readStringUntil não existe sem isso."),("b","Para não travar o loop() esperando o tempo limite quando não há nada digitado."),("c","Para acelerar o printf.")], "readStringUntil bloqueia; verificar antes evita bloquear sem necessidade.") + flash([
    ("Qual a diferença entre = e ==?", "= atribui um valor; == compara dois valores e devolve true ou false."),
    ("Por que String pode ser um problema no ESP32?", "Concatenações repetidas podem fragmentar a RAM, que é pouca."),
    ("Para que serve o operador ternário?", "É um if/else compacto que devolve um valor: condição ? a : b."),
    ("O que faz o %s com uma String?", "Imprime o texto, desde que você passe nome.c_str().")]) + ponte("Até aqui o ESP32 só mandou sinais. Como ele passa a ler o mundo, começando por um botão?", "Com um pino de entrada.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "tipos-e-strings", T, "Tipos, strings, operadores e printf", "Capítulo 5 · Aula 5",
        "Tipos primitivos, os três jeitos de guardar texto, operadores, printf e leitura pelo Serial.",
        ["<b>~45 min</b>", "2 demos · 3 testes · 4 flashcards", "formatador de printf"], body5, scripts=S)

# ---------------- CAP 6 ----------------
body6 = recap("Nos capítulos anteriores o ESP32 só mandou sinais (<code>OUTPUT</code>). Agora ele <b>lê</b>: um botão. É o primeiro passo de uma lição maior: sensor é entrada, atuador é saída, e a lógica decide a ponte entre eles.") + '''
<section class="sec" id="pullup">
  <h2><span class="sn">1</span>O botão e o INPUT_PULLUP</h2>
  <p class="gancho">Apertar dá LOW. Sim, ao contrário.</p>
  <p>Um botão simples liga ou desliga um caminho elétrico. Se ele for ligado entre o pino e o <b>GND</b>, apertá-lo puxa o pino para 0 V. Mas e quando está solto? O pino fica "no ar", e um pino sem ligação definida <b>flutua</b>, captando ruído. A solução é o <b>resistor de pull-up</b>, que mantém o pino em HIGH quando nada o puxa. O ESP32 já tem um interno: basta <code>pinMode(pino, INPUT_PULLUP)</code>.</p>
  <div class="demo" data-demo="botao"></div>
  <p>Resultado: <b>solto = HIGH, pressionado = LOW</b>. A lógica fica <b>invertida</b>, e é o ponto que mais derruba quem está começando. O botão não precisa de resistor externo; o LED, sim. <i>Complemento:</i> no ESP32, os GPIOs 34, 35, 36 e 39 (só entrada) <b>não têm pull-up interno</b>; para um botão neles, use um resistor externo.</p>
<pre><code><span class="k">#define</span> LED_PIN 26
<span class="k">#define</span> BTN_PIN 21

<span class="k">void</span> setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT_PULLUP);       <span class="c">// entrada com pull-up interno</span>
}

<span class="k">void</span> loop() {
  <span class="k">if</span> (digitalRead(BTN_PIN) == LOW) {    <span class="c">// LOW = botão pressionado</span>
    Serial.println("Botão pressionado!");
    digitalWrite(LED_PIN, HIGH);
  } <span class="k">else</span> {
    digitalWrite(LED_PIN, LOW);
  }
  delay(50);
}</code></pre>
  <p>Aqui as estruturas condicionais saem da teoria: o <code>if/else</code> decide a partir de uma <b>leitura do mundo real</b>.</p>
</section>

<section class="sec" id="delay">
  <h2><span class="sn">2</span>O preço do delay</h2>
  <p class="gancho">Quando o processador dorme, o mundo continua.</p>
  <p>Um código típico faz o LED piscar quando o botão é apertado, com <code>delay(1000)</code> duas vezes (aceso e apagado). Durante esses 2 segundos o ESP32 está <b>"surdo"</b>: não lê o botão. Quanto isso custa? A demo simula um botão apertado a cada 0,7 s por 10 s (cada toque dura 150 ms) e mostra quantos toques o programa percebe, conforme o intervalo entre leituras:</p>
  <div class="demo" data-demo="bloqueio"></div>
  <div class="nota lembra"><span class="lbl">Complemento: millis() e debounce</span>A saída é <b>não bloquear</b>: em vez de <code>delay</code>, guarde o instante da última ação e compare com <code>millis()</code> (milissegundos desde que a placa ligou):<pre><code>unsigned long ultimo = 0;
const unsigned long INTERVALO = 500;
bool ledLigado = false;

void loop() {
  unsigned long agora = millis();
  if (agora - ultimo &gt;= INTERVALO) {     <span class="c">// passou 500 ms?</span>
    ultimo = agora;
    ledLigado = !ledLigado;
    digitalWrite(LED_PIN, ledLigado);
  }
  <span class="c">// o loop segue livre: dá para ler o botão a cada volta</span>
}</code></pre>O LED pisca igual, mas o <code>loop()</code> continua rodando e lendo o botão. E um botão mecânico "quica" por alguns milissegundos ao ser apertado (<i>bounce</i>), o que pode gerar vários cliques de um só: o <i>debounce</i> ignora mudanças muito próximas no tempo.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">3</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Entrada</b>: <code>pinMode(pino, INPUT_PULLUP)</code> e <code>digitalRead(pino)</code>.",
    "Com pull-up: <b>solto = HIGH, apertado = LOW</b> (lógica invertida). Sem pull-up, o pino <b>flutua</b> e lê valores aleatórios.",
    "O botão não precisa de resistor externo com <code>INPUT_PULLUP</code>; o LED precisa do dele.",
    "<code>delay</code> deixa o ESP32 <b>surdo</b>: toques entre leituras se perdem. Solução: <code>millis()</code> (complemento), e debounce para o 'quique' do botão."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Com INPUT_PULLUP, qual o valor lido quando o botão está solto?", [("a","HIGH."),("b","LOW."),("c","Aleatório.")], "O resistor interno mantém o pino em HIGH; apertar liga ao GND e dá LOW.") + quiz(2, "c", "O que acontece se você usar INPUT puro, sem resistor externo, com o botão solto?", [("a","Lê sempre LOW."),("b","Lê sempre HIGH."),("c","O pino flutua e a leitura é imprevisível.")], "Sem referência, o pino capta ruído. Por isso o pull-up.") + quiz(3, "b", "Por que um delay(2000) no loop() faz o programa perder toques do botão?", [("a","Porque o botão tem defeito."),("b","Porque durante o delay o processador não lê o pino."),("c","Porque o delay desliga o pull-up.")], "O delay é bloqueante: nada mais roda enquanto ele espera.") + flash([
    ("Por que apertar o botão dá LOW?", "O botão liga o pino ao GND, e o pull-up interno mantém HIGH quando solto."),
    ("O que é um pino flutuando?", "Um pino sem nível definido, que capta ruído e lê valores aleatórios."),
    ("O que faz o millis()?", "Devolve os milissegundos desde que a placa ligou: serve para medir tempo sem bloquear."),
    ("O que é debounce?", "Ignorar mudanças muito próximas no tempo, causadas pelo 'quique' mecânico do botão.")]) + ponte("Do botão (liga/desliga) para o sensor de verdade, que mede números do ambiente.", "O DHT22.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
chapter(PASTA, 6, "botao", T, "Entradas: o botão, o pull-up e o delay que trava", "Capítulo 6 · Aula 6",
        "Ler um botão com INPUT_PULLUP, entender a lógica invertida e ver por que delay perde toques.",
        ["<b>~40 min</b>", "2 demos · 3 testes · 4 flashcards", "pull-up e toques perdidos"], body6, scripts=S)

# ---------------- CAP 7 ----------------
body7 = recap("O botão lê dois estados. O <b>DHT22</b> lê <b>números</b> do ambiente, com uma biblioteca externa, risco de falha e a necessidade de decidir a partir do valor. É a síntese do que veio antes: pinos, tipos, <code>printf</code>, <code>if</code> e <code>delay</code>.") + '''
<section class="sec" id="porque">
  <h2><span class="sn">1</span>Por que medir temperatura e umidade</h2>
  <p class="gancho">Um problema real: conservar coisas sensíveis.</p>
  <p>Acervos de livros antigos, remédios e alimentos estragam com <b>calor e umidade</b> fora da faixa. Um sistema IoT que mede e alerta é a solução óbvia: sensor, ESP32 e um alerta (LED, buzzer, mensagem). Os sensores mais comuns:</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>DHT11</th><th>DHT22</th><th>SHT40</th></tr>
    <tr><td><b>Precisão (temperatura)</b></td><td>±2 °C</td><td>±0,5 °C</td><td>±0,2 °C</td></tr>
    <tr><td><b>Faixa (temperatura)</b></td><td>0 a 50 °C</td><td>−40 a 80 °C</td><td>−40 a 125 °C</td></tr>
    <tr><td><b>Precisão (umidade)</b></td><td>±5 % UR</td><td>±2 a 5 % UR</td><td>±1,8 % UR</td></tr>
    <tr><td><b>Faixa (umidade)</b></td><td>20 a 80 %</td><td>0 a 100 %</td><td>0 a 100 %</td></tr>
    <tr><td><b>Intervalo entre leituras</b></td><td>1 s</td><td><b>2 s</b></td><td>várias por segundo</td></tr>
    <tr><td><b>Resumo</b></td><td>o mais barato</td><td>mais preciso</td><td>o mais preciso e o mais usado em produto</td></tr>
  </table></div>
  <p>O DHT22 liga com quatro pinos: <b>VCC</b> em 3,3 V, <b>GND</b> no GND, <b>DATA</b> em um GPIO e um pino <b>NC</b> (não conectado). UR é umidade relativa.</p>
</section>

<section class="sec" id="codigo">
  <h2><span class="sn">2</span>O código, peça por peça</h2>
  <p class="gancho">A primeira biblioteca externa do projeto.</p>
  <p>A biblioteca da Adafruit entra no <code>platformio.ini</code>, e o PlatformIO a baixa sozinho no primeiro build:</p>
<pre><code>lib_deps =
    adafruit/DHT sensor library @ ^1.4.6</code></pre>
<pre><code><span class="k">#include</span> &lt;Arduino.h&gt;
<span class="k">#include</span> &lt;DHT.h&gt;

<span class="k">#define</span> DHT_PIN 19
<span class="k">#define</span> DHT_MODEL DHT22

DHT sensor(DHT_PIN, DHT_MODEL);          <span class="c">// objeto: pino e modelo</span>

<span class="k">void</span> setup() {
  Serial.begin(115200);
  sensor.begin();                        <span class="c">// inicializa o sensor</span>
  delay(2000);                           <span class="c">// espera antes da 1ª medição</span>
}

<span class="k">void</span> loop() {
  float temp = sensor.readTemperature();
  float umid = sensor.readHumidity();

  <span class="k">if</span> (isnan(temp) || isnan(umid)) {      <span class="c">// leitura falhou?</span>
    Serial.println("Falha na leitura!!!");
    delay(2000);
    <span class="k">return</span>;                              <span class="c">// encerra ESTA volta e tenta de novo</span>
  }

  Serial.printf("Temperatura: %.2f  |  Umidade: %.2f\\r\\n", temp, umid);

  <span class="k">if</span> (temp &gt; 35) Serial.println("-- ALERTA -- Temperatura Alta!");
  <span class="k">if</span> (umid &gt; 65) Serial.println("-- ALERTA -- Umidade Alta!");

  delay(2000);                           <span class="c">// o DHT22 só lê a cada 2 s</span>
}</code></pre>
  <ul>
    <li><code>DHT sensor(DHT_PIN, DHT_MODEL);</code> cria um <b>objeto</b> da biblioteca. Daí em diante tudo é <code>sensor.alguma_coisa()</code>.</li>
    <li><code>isnan()</code> (<i>is not a number</i>): quando a leitura falha, o sensor devolve <code>NaN</code>. Testa-se <b>antes</b> de usar o valor.</li>
    <li><code>return</code> dentro do <code>loop()</code> <b>não para o programa</b>: só encerra esta volta; o framework chama o <code>loop()</code> de novo.</li>
    <li>O <code>delay(2000)</code> respeita o intervalo mínimo do DHT22. O <code>delay</code> dentro do bloco de erro evita tentar de novo antes de 2 s.</li>
    <li>Dois <code>if</code> <b>separados</b>, e não <code>if/else</code>: os dois alertas podem ocorrer juntos.</li>
  </ul>
  <p>No simulador, é possível ajustar a temperatura e a umidade do sensor virtual na mão, como no Wokwi. Faça o mesmo aqui:</p>
  <div class="demo" data-demo="dht"></div>
</section>

<section class="sec" id="calor">
  <h2><span class="sn">3</span>Índice de calor: o calor que se sente</h2>
  <p class="gancho">Temperatura e umidade juntas valem mais que cada uma.</p>
  <p>O <b>índice de calor</b> é a temperatura que o corpo <b>sente</b>: com o ar úmido, o suor evapora pior e o mesmo calor parece maior. A biblioteca já calcula:</p>
<pre><code>float ic = sensor.computeHeatIndex(temp, umid, false);   <span class="c">// false = em Celsius</span></code></pre>
  <div class="ex rv"><span class="t">Exemplo resolvido: duas leituras e um limite de 25</span>
    <div class="l"><div><b>24 °C e 40%</b>: o índice de calor é cerca de <b>23,5 °C</b>. Menor que 25, então o LED fica <b>apagado</b>.</div></div>
    <div class="l"><div><b>27 °C e 60%</b>: o índice sobe para cerca de <b>28,1 °C</b>, acima da temperatura real, por causa da umidade. Maior que 25: LED <b>aceso</b>.</div></div>
    <div class="l"><div>Para <b>32 °C e 70%</b> o índice chega a cerca de <b>40,4 °C</b>: a sensação é 8 °C acima do termômetro. (Valores calculados com a lógica da biblioteca da Adafruit: média de Steadman em valores baixos e regressão de Rothfusz acima de cerca de 80 °F. É complemento: a aula não detalhou a fórmula, e os decimais podem diferir da sua versão. A regressão de Rothfusz pura daria 25,3 para 24 °C e 40%, e não 23,5.)</div></div>
  </div>
  <div class="ex rv"><span class="t">Atividade para você: LED de alerta</span>
    <div class="l"><div>Monte ESP32 + LED + DHT22 (por exemplo, DHT no GPIO 26 e LED no 25). Leia temperatura e umidade e mostre no Monitor Serial. Se as leituras forem válidas, calcule o índice de calor (<code>ic</code>).</div></div>
    <div class="l"><div>Se <code>ic &gt; 25</code>, acenda o LED e mostre o aviso com o valor. Depois de 3 segundos, apague o LED e meça de novo. Teste com valores acima e abaixo do limite.</div></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado com o intervalo</span>Um <code>delay(2000)</code> faltando antes do <code>return</code> do caso de erro faz o <code>loop()</code> pedir outra leitura na hora, antes dos 2 s que o DHT22 precisa. O resultado são falhas em série.</div>
</section>

<section class="sec" id="dataset">
  <h2><span class="sn">4</span>De sensor a dataset</h2>
  <p class="gancho">Medir é o primeiro passo de ensinar uma máquina.</p>
  <p>Se cada leitura sair em <b>uma linha CSV</b>, o Monitor Serial vira uma fonte de dados: basta imprimir o cabeçalho uma vez e uma linha por leitura.</p>
<pre><code><span class="c">// globais, fora do setup() e do loop():</span>
int id = 0;
String classe = "normal";   <span class="c">// o rótulo da linha: você decide como defini-lo</span>
<span class="c">// no setup():</span>
Serial.println("id,temperatura,umidade,classe");
<span class="c">// no loop(), a cada leitura válida:</span>
Serial.printf("%d,%.2f,%.2f,%s\\r\\n", id++, temp, umid, classe.c_str());</code></pre>
  <p>Copiar a saída para um arquivo <code>.csv</code> e abri-lo com o Pandas leva ao mundo do machine learning, que usa o mesmo formato do conjunto Iris. A diferença é que aqui <b>você cria o próprio conjunto</b>, e a coluna de <b>classe</b> (o rótulo que diz o que cada linha representa) é sua responsabilidade: sem ela não existe classificação supervisionada. O valor de uma solução costuma estar em <b>modelo próprio com dados próprios</b>, e em saber explicar como os dados foram coletados.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo (e da apostila)</h2>
  ''' + resumo([
    "<b>DHT22</b>: ±0,5 °C, −40 a 80 °C, leitura a cada <b>2 s</b>. Pinos: VCC (3,3 V), GND, DATA (um GPIO), NC.",
    "Biblioteca externa em <code>lib_deps</code>; objeto <code>DHT sensor(pino, modelo)</code>; <code>sensor.begin()</code> no setup.",
    "<code>isnan()</code> antes de usar a leitura; <code>return</code> encerra só a volta do loop.",
    "Dois <code>if</code> separados para alertas independentes. Respeite o intervalo do sensor com <code>delay</code>.",
    "<b>Índice de calor</b> junta temperatura e umidade (<code>computeHeatIndex(t, u, false)</code>). Saída em CSV leva ao dataset e ao machine learning."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "O que isnan(temp) testa?", [("a","Se a temperatura é negativa."),("b","Se a leitura falhou e veio NaN, para não usar um valor inválido."),("c","Se a temperatura é maior que 35.")], "Se o sensor falha, o valor é 'not a number'. O teste vem antes de imprimir ou comparar.") + quiz(2, "c", "Qual o intervalo mínimo entre leituras do DHT22?", [("a","100 ms."),("b","1 s."),("c","2 s.")], "O DHT11 lê a cada 1 s; o DHT22, a cada 2 s.") + quiz(3, "a", "O que o 'false' em computeHeatIndex(temp, umid, false) faz?", [("a","Calcula o índice em graus Celsius."),("b","Desliga o sensor."),("c","Ignora a umidade.")], "O terceiro argumento indica se a temperatura está em Fahrenheit; false significa Celsius.") + flash([
    ("O que é o índice de calor?", "A temperatura que o corpo sente, combinando temperatura e umidade."),
    ("Por que dois if e não if/else nos alertas?", "Porque temperatura alta e umidade alta podem acontecer ao mesmo tempo."),
    ("O que o return faz dentro do loop()?", "Encerra só aquela volta. O loop() é chamado de novo logo em seguida."),
    ("O que é a coluna de classe de um dataset?", "O rótulo de cada linha, necessário para o aprendizado supervisionado.")]) + '''
  <div class="ponte rv"><div class="t">Fim da apostila</div><div class="q">Do LED ao sensor, de um pino a um dataset.</div><p>O passo seguinte é levar esses dados para a rede (servidor web no próprio ESP32 e nuvem). Tudo o que foi visto aqui, de pinos a Serial, é a base dessa conversa.</p></div>
</section>'''
chapter(PASTA, 7, "dht22", T, "O sensor DHT22 e o índice de calor", "Capítulo 7 · Aula 7",
        "Ler temperatura e umidade com uma biblioteca externa, tratar falhas, alertar e calcular o índice de calor.",
        ["<b>~50 min</b>", "1 demo · 3 testes · 4 flashcards", "DHT22 virtual com índice de calor"], body7, scripts=S)
print("emb caps 4-7 ok")
