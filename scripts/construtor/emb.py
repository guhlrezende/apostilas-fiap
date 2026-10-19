import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *

PASTA = "embarcados"
TITULO = "Sistemas Embarcados com ESP32"
T = TITULO
S = ["demos/emb.js"]
CAPS = [
 dict(n=1, file="cap-1-esp32.html", titulo="O ESP32 e o mundo embarcado", aula="Aula 1", tempo=35,
      resumo="Dispositivos robustos e restritos, Arduino x ESP8266 x ESP32, sensores, atuadores e o ciclo que toda placa repete.",
      pergunta="Já sei o que é a placa. Como se escreve um programa para ela, e onde os erros aparecem?"),
 dict(n=2, file="cap-2-programar.html", titulo="Programar o ESP32: C++, build e ambiente", aula="Aulas 1 e 2", tempo=40,
      resumo="C++ compilado, as três etapas do build, o ambiente VSCode + PlatformIO + Wokwi e os arquivos mínimos do projeto.",
      pergunta="O código compila, mas a placa é feita de pinos. Quais usar, e como ligar um LED sem queimá-lo?"),
 dict(n=3, file="cap-3-gpio-e-led.html", titulo="GPIO, LED e resistor", aula="Aulas 1, 2 e 6", tempo=40,
      resumo="Mapa dos pinos, o que pode e o que não pode, anodo e catodo, a conta do resistor e o primeiro pisca-pisca.",
      pergunta="O LED pisca, mas o programa que o controla ainda é uma caixa preta. Como o setup, o loop e o Serial funcionam?"),
 dict(n=4, file="cap-4-setup-loop-serial.html", titulo="setup, loop, Serial e a lógica", aula="Aulas 2, 4 e 6", tempo=45,
      resumo="O modelo de execução, o Monitor Serial, variável global x local, delay e as quatro estruturas da lógica de programação.",
      pergunta="Guardamos valores em variáveis. Que tipos existem, e como imprimir cada um do jeito certo?"),
 dict(n=5, file="cap-5-tipos-e-strings.html", titulo="Tipos, strings, operadores e printf", aula="Aula 5", tempo=45,
      resumo="int, float, char, String e bool, o terminador nulo, operadores, = x ==, printf, ternário e leitura pelo Serial.",
      pergunta="Até aqui o ESP32 só mandou sinais. Como ele passa a ler o mundo, começando por um botão?"),
 dict(n=6, file="cap-6-botao.html", titulo="Entradas: o botão, o pull-up e o delay que trava", aula="Aula 6", tempo=40,
      resumo="INPUT_PULLUP, lógica invertida, o botão controlando o LED, e por que delay perde toques.",
      pergunta="Do botão (liga/desliga) para o sensor de verdade, que mede números do ambiente."),
 dict(n=7, file="cap-7-dht22.html", titulo="O sensor DHT22 e o índice de calor", aula="Aula 7", tempo=50,
      resumo="Temperatura e umidade com biblioteca externa, checagem de falha, alertas, índice de calor e o caminho até um dataset.",
      pergunta=""),
]
manifest(PASTA, "embarcados", TITULO, CAPS)
hub(PASTA, TITULO, "Sistemas Embarcados e Sensores com ESP32", "Apostila de Sistemas Embarcados com ESP32",
    "Do LED que pisca ao sensor de temperatura, com C++ no ESP32, o Monitor Serial e circuitos para entender sem montar nada.",
    ["<b>7</b> capítulos", "<b>~4h55</b> de estudo ativo", "circuitos e Serial simulados"],
    '<p>A história é a de um <mark class="hl">computador minúsculo que fala com o mundo físico</mark>. Primeiro conhecemos a placa e o que a separa de um computador comum. Depois aprendemos a escrever e compilar o programa, escolher os pinos e acender um LED sem queimá-lo. Em seguida vem a lógica (setup, loop, variáveis, strings), a primeira entrada (um botão) e, por fim, o primeiro sensor de verdade, o DHT22. Cada capítulo termina com a pergunta que o próximo responde.</p>',
    'Os códigos seguem o estilo das aulas e foram revisados à mão, <b>sem compilar neste ambiente</b>: compile no seu PlatformIO antes de confiar. Os simuladores da página mostram o comportamento esperado, mas não substituem o Monitor Serial real. Material complementar (como <code>millis()</code> e debounce) vem marcado.')

# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo. Você não precisa de eletrônica: basta já ter programado um pouco. Ele apresenta a placa que acompanha o resto da apostila, o <b>ESP32</b>, e a ideia por trás de qualquer sistema embarcado.", "Ponto de partida") + '''
<section class="sec" id="dispositivos">
  <h2><span class="sn">1</span>Dois grupos de dispositivos</h2>
  <p class="gancho">Nem todo computador tem sistema operacional.</p>
  <p>Dispositivos que carregam "inteligência" se dividem em dois grandes grupos:</p>
  <div class="grid2">
    <div class="card rv"><b>Robustos</b><p>Exemplo: <b>Raspberry Pi 5</b>. Rodam um <b>sistema operacional de propósito geral</b> (Linux), têm de centenas de MB a vários GB de RAM, CPU de vários núcleos na casa de GHz, saída de vídeo, WiFi, Bluetooth e Ethernet. Exigem energia contínua ou uma bateria bem forte.</p></div>
    <div class="card rv"><b>Restritos</b><p>Exemplos: <b>Arduino, ESP32</b>. São <b>microcontroladores (MCU)</b> de 8, 16 ou 32 bits, com RAM e memória flash na casa de centenas de KB a poucos MB. <b>Não executam sistema operacional geral</b>, mas têm pinos para sensores e atuadores e consomem muito pouco: uma bateria pode durar dias, meses ou anos.</p></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Dentro dos restritos, qual placa escolher?</div><p>Depende do que ela precisa fazer.</p></div>
</section>

<section class="sec" id="placas">
  <h2><span class="sn">2</span>Arduino, ESP8266 e ESP32</h2>
  <p class="gancho">Uma linha do tempo de três placas.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>Arduino</th><th>ESP8266</th><th>ESP32</th></tr>
    <tr><td><b>Ano</b></td><td>2005 (ATmega8)</td><td>2014</td><td>2016</td></tr>
    <tr><td><b>Processador</b></td><td>8 bits</td><td>capacidade baixa</td><td><b>dual-core de 32 bits</b></td></tr>
    <tr><td><b>WiFi</b></td><td>não nativo (precisa de uma placa de expansão)</td><td>nativo</td><td>nativo</td></tr>
    <tr><td><b>Bluetooth</b></td><td>não</td><td>não</td><td>sim, incluindo BLE (baixo consumo)</td></tr>
    <tr><td><b>IoT e IA</b></td><td>pouco ou nenhum suporte</td><td>pouco suporte</td><td>suporte pleno, inclusive visão computacional</td></tr>
  </table></div>
  <div class="card sorter rv" data-demo="sorter" data-opts="ard:Arduino|e82:ESP8266|e32:ESP32">
    <div class="item" data-ans="e32"><p>Lançado em 2016, com CPU de 2 núcleos e 32 bits, WiFi e Bluetooth.</p><span class="why">Dual-core, 32 bits e Bluetooth são do ESP32.</span></div>
    <div class="item" data-ans="ard"><p>Surgiu em 2005 com um ATmega de 8 bits e, por si só, não tem WiFi.</p><span class="why">É a revolução eletrônica do Arduino: simples, de 8 bits, sem rede nativa.</span></div>
    <div class="item" data-ans="e82"><p>Trouxe WiFi nativo em 2014, mas com capacidade de processamento muito baixa.</p><span class="why">O ESP8266 popularizou o WiFi barato, mas é fraco para IA.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <p>O <b>ESP32</b> é o dispositivo usado no resto desta apostila: pequeno, barato, com WiFi e Bluetooth nativos e processamento suficiente para IA leve. Ele é o <b>cérebro</b>: o resto do circuito (LEDs, botões, sensores) é conectado a ele. Mas o chip sozinho é pequeno e delicado, por isso vem em uma <b>placa de desenvolvimento</b> (como a <b>NodeMCU</b>, uma plataforma aberta em que o chip é soldado em uma placa com conexão <b>USB</b>) e existem variantes, como a <b>ESP32-CAM</b>, com câmera.</p>
</section>

<section class="sec" id="ciclo">
  <h2><span class="sn">3</span>O ciclo de três passos</h2>
  <p class="gancho">Sentir, pensar, agir. Para sempre.</p>
  <ol>
    <li>Um <b>sensor</b> capta uma medição do ambiente (temperatura, luz, um clique).</li>
    <li>O <b>dispositivo</b> (o ESP32) processa o dado.</li>
    <li>Ele <b>toma uma ação</b>: acende uma luz, liga um motor, mostra um alerta.</li>
  </ol>
  <p><b>Sensores</b> são entradas (<i>input</i>): pegam algo do ambiente e levam para dentro do dispositivo. <b>Atuadores</b> são saídas (<i>output</i>): levam algo do dispositivo para o ambiente. O <b>LED</b> é o componente mais usado de todos. Outros que aparecem ao longo do caminho:</p>
  <div class="tablewrap"><table>
    <tr><th>Componente</th><th>Função</th><th>Tipo</th></tr>
    <tr><td>LED</td><td>emite luz</td><td>saída</td></tr>
    <tr><td>Buzzer</td><td>emite som</td><td>saída</td></tr>
    <tr><td>Botão (push button)</td><td>liga/desliga um sinal</td><td>entrada</td></tr>
    <tr><td>DHT22</td><td>temperatura e umidade</td><td>entrada</td></tr>
    <tr><td>LDR</td><td>luminosidade</td><td>entrada</td></tr>
    <tr><td>HC-SR04</td><td>distância (ultrassom)</td><td>entrada</td></tr>
    <tr><td>PIR</td><td>presença</td><td>entrada</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Isso é só o começo</span>A aplicação de IoT vem depois: ligar esse ciclo à internet (WiFi) e a modelos de IA. Mas tudo começa em um ESP32 que sabe ler um pino, decidir e escrever em outro.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Robustos</b> (Raspberry Pi: SO geral, GB de RAM) x <b>restritos</b> (Arduino, ESP32: microcontrolador, sem SO, consumo mínimo).",
    "<b>Arduino</b> (2005, 8 bits, sem WiFi), <b>ESP8266</b> (2014, WiFi, fraco), <b>ESP32</b> (2016, dual-core 32 bits, WiFi + Bluetooth/BLE, IA).",
    "O ESP32 é o <b>cérebro</b>; vem numa <b>placa de desenvolvimento</b> (NodeMCU) com USB.",
    "Ciclo: <b>sensor → processa → age</b>. Sensor é entrada; atuador é saída."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual característica define um dispositivo 'restrito'?", [("a","Roda Linux."),("b","Precisa de energia ininterrupta."),("c","É um microcontrolador, sem sistema operacional de propósito geral e com consumo muito baixo.")], "Restritos (Arduino, ESP32) são MCUs de baixo consumo. Robustos (Raspberry Pi) rodam um SO geral.") + quiz(2, "a", "O que o ESP32 tem que o Arduino original não tinha?", [("a","WiFi e Bluetooth nativos e CPU de 32 bits com dois núcleos."),("b","Apenas mais pinos."),("c","Sistema operacional Linux.")], "É a combinação de conectividade e processamento que o torna adequado a IoT e IA leve.") + quiz(3, "b", "Um buzzer, que emite som, é...", [("a","Um sensor de entrada."),("b","Um atuador, ou seja, uma saída."),("c","Uma placa de desenvolvimento.")], "Saída leva algo do dispositivo para o ambiente; sensor traz do ambiente para o dispositivo.") + flash([
    ("O que é uma placa de desenvolvimento?", "O chip soldado numa placa com USB e pinos, para facilitar programar e prototipar (por exemplo, NodeMCU)."),
    ("Quais os três passos do ciclo embarcado?", "O sensor capta, o ESP32 processa, e ele toma uma ação."),
    ("O que significa BLE?", "Bluetooth Low Energy: Bluetooth de baixo consumo."),
    ("Sensor x atuador?", "Sensor é entrada (ambiente → dispositivo). Atuador é saída (dispositivo → ambiente).")]) + ponte("Já sei o que é a placa. Como se escreve um programa para ela, e onde os erros aparecem?", "Em C++, que é compilado.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "esp32", T, "O ESP32 e o mundo embarcado", "Capítulo 1 · Aula 1",
        "O que é um dispositivo restrito, como o ESP32 se compara ao Arduino e ao ESP8266 e o ciclo de qualquer sistema embarcado.",
        ["<b>~35 min</b>", "1 demo · 3 testes · 4 flashcards", "classifique as placas"], body1, scripts=S)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 você conheceu a placa. Agora o programa que roda nela: <b>C++</b>, uma linguagem <b>compilada</b>. Isso muda como os erros aparecem, e é o que este capítulo mostra, junto com as ferramentas do ambiente de desenvolvimento.") + '''
<section class="sec" id="compilado">
  <h2><span class="sn">1</span>Compilado x interpretado</h2>
  <p class="gancho">Em C++, o programa inteiro precisa estar certo antes de rodar.</p>
  <p>Em <b>Python</b> (interpretado), o código é executado <b>linha a linha</b>: se há um erro, o interpretador para e aponta a linha. Em <b>C/C++</b> (compilado), um <b>compilador</b> converte o programa <b>inteiro</b> em código de máquina (um <code>.exe</code> no Windows; um <code>.elf</code> ou <code>.bin</code> para um ESP32). <b>O código só é executado se compilar sem erros.</b> O arquivo de programa de uma placa ESP32 usa a extensão <code>.ino</code>.</p>
  <h3>As três etapas do build</h3>
  <ol>
    <li><b>Pré-processamento</b>: as diretivas <code>#include</code> e <code>#define</code> são resolvidas antes de qualquer compilação (por exemplo, trazem as bibliotecas).</li>
    <li><b>Compilação</b>: o código-fonte vira código-objeto.</li>
    <li><b>Linkagem</b>: as bibliotecas usadas são vinculadas ao seu código e gera-se o binário final.</li>
  </ol>
  <p>Escolha um erro e veja em que etapa ele aparece (ou se fica escondido):</p>
  <div class="demo" data-demo="compila"></div>
  <div class="nota cuidado"><span class="lbl">Sempre salve o arquivo</span>O compilador usa o arquivo <b>salvo em disco</b>, e não o que está na tela. Rodar sem salvar é rodar a versão anterior. É o erro mais bobo e um dos mais frequentes.</div>
</section>

<section class="sec" id="ambiente">
  <h2><span class="sn">2</span>O ambiente: VSCode, PlatformIO e Wokwi</h2>
  <p class="gancho">Três ferramentas, cada uma com um papel.</p>
  <div class="tablewrap"><table>
    <tr><th>Ferramenta</th><th>Papel</th></tr>
    <tr><td><b>VSCode</b></td><td>Editor de código. Vira um ambiente de desenvolvimento conforme as extensões instaladas.</td></tr>
    <tr><td><b>PlatformIO</b> (extensão)</td><td>O <i>toolchain</i>: baixa o compilador do ESP32 e o framework Arduino, resolve dependências e <b>gera o binário</b> (<code>firmware.elf</code> e <code>firmware.bin</code>).</td></tr>
    <tr><td><b>Wokwi</b> (extensão)</td><td>O <b>simulador</b>: pega o binário do PlatformIO e o executa em uma placa ESP32 virtual, com Monitor Serial e os componentes desenhados em um arquivo de circuito.</td></tr>
  </table></div>
  <p><b>PlatformIO compila, Wokwi simula.</b> Sem compilar antes, o simulador não tem o que executar. (O Wokwi também tem uma versão web, ótima para começar, mas a execução local evita limites de tempo e deixa o projeto em arquivos que você versiona.) O Wokwi pede uma licença gratuita para a extensão local. Alternativas: a Arduino IDE, mais simples, ou uma placa física, que exige o toolchain instalado.</p>
  <h3>Os arquivos mínimos de um projeto</h3>
<pre><code>meu-projeto/
├── src/
│   └── meuProjeto.ino     <span class="c"># o código</span>
├── platformio.ini         <span class="c"># placa, plataforma e framework</span>
├── diagram.json           <span class="c"># o circuito virtual do Wokwi</span>
└── wokwi.toml             <span class="c"># aponta o Wokwi para o binário compilado</span></code></pre>
<pre><code><span class="c"># platformio.ini</span>
[env:esp32]
platform = espressif32     <span class="c"># a família de chips (toolchain da Espressif)</span>
framework = arduino        <span class="c"># usa a API Arduino: setup(), loop(), Serial, pinMode...</span>
board = esp32dev           <span class="c"># placa genérica ESP32 DevKit</span>

<span class="c"># wokwi.toml: a ponte entre as duas extensões</span>
[wokwi]
version = 1
elf = ".pio/build/esp32/firmware.elf"
firmware = ".pio/build/esp32/firmware.bin"</code></pre>
  <p>No <code>diagram.json</code> ficam as peças e as ligações. Para o Monitor Serial aparecer, o circuito precisa ligar <code>esp:TX</code> a <code>$serialMonitor:RX</code> e <code>esp:RX</code> a <code>$serialMonitor:TX</code>. Sem essas duas ligações, o <code>Serial.println()</code> roda, mas você não vê nada.</p>
</section>

<section class="sec" id="checklist">
  <h2><span class="sn">3</span>Checklist de depuração do ambiente</h2>
  <p class="gancho">Quando "não funciona", comece por aqui.</p>
  <div class="tablewrap"><table>
    <tr><th>Sintoma</th><th>Causa provável</th></tr>
    <tr><td>Monitor Serial mudo</td><td><code>Serial.begin()</code> esquecido, velocidade diferente de 115200 no monitor, ou faltam as ligações TX/RX no <code>diagram.json</code></td></tr>
    <tr><td>"firmware not found" no Wokwi</td><td>não compilou antes, ou o VSCode foi aberto na pasta errada (o <code>wokwi.toml</code> precisa estar na raiz)</td></tr>
    <tr><td>Simulador não inicia</td><td>licença do Wokwi não ativada</td></tr>
    <tr><td>A mudança não aparece</td><td>arquivo não salvo, ou salvou e não recompilou</td></tr>
    <tr><td>Erro que parece estranho depois de reaproveitar um projeto</td><td>faça um <b>Clean</b> e depois um <b>Build</b> no PlatformIO</td></tr>
  </table></div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>C++ é compilado</b>: o programa inteiro precisa compilar antes de rodar. Python é interpretado, linha a linha.",
    "<b>Build em 3 etapas</b>: pré-processamento, compilação, linkagem. Erros de lógica e esquecimentos só aparecem na execução.",
    "<b>VSCode</b> edita, <b>PlatformIO</b> compila, <b>Wokwi</b> simula. Arquivos: <code>.ino</code>, <code>platformio.ini</code>, <code>diagram.json</code>, <code>wokwi.toml</code>.",
    "Sempre <b>salvar</b> antes de compilar. Em dúvida, <b>Clean</b> e <b>Build</b>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Em que etapa aparece o erro 'DHT.h: No such file or directory'?", [("a","Na execução, no ESP32."),("b","No pré-processamento: o #include não encontra a biblioteca."),("c","Na linkagem.")], "É o #include que falha, e ele é resolvido na primeira etapa do build.") + quiz(2, "c", "Qual a função do PlatformIO neste ambiente?", [("a","Simular o circuito."),("b","Escrever o código."),("c","Compilar o programa e gerar o binário.")], "O Wokwi simula; o PlatformIO compila. Sem compilar, o simulador não acha o firmware.") + quiz(3, "a", "Você esqueceu o pinMode(pino, OUTPUT). O que acontece?", [("a","Compila normalmente, mas o LED não acende: é um erro silencioso."),("b","O compilador mostra um erro na linha."),("c","O ESP32 reinicia.")], "O compilador só pega erros de escrita. Esquecimentos aparecem no comportamento da placa.") + flash([
    ("Qual a diferença entre compilar e interpretar?", "Compilar converte o programa inteiro em binário antes de rodar. Interpretar executa linha a linha."),
    ("O que faz o wokwi.toml?", "Aponta o Wokwi para o binário gerado pelo PlatformIO."),
    ("Por que sempre salvar o arquivo?", "O compilador usa a versão salva em disco, e não a que aparece na tela."),
    ("O que é um 'erro silencioso'?", "Um erro que compila sem avisos mas faz a placa se comportar errado, como esquecer o pinMode.")]) + ponte("O código compila, mas a placa é feita de pinos. Quais usar, e como ligar um LED sem queimá-lo?", "Conhecendo os GPIOs e fazendo a conta do resistor.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "programar", T, "Programar o ESP32: C++, build e ambiente", "Capítulo 2 · Aulas 1 e 2",
        "Por que C++ compilado muda a forma de errar, e como montar o ambiente de desenvolvimento.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "em que etapa cada erro aparece"], body2, scripts=S)

# ---------------- CAP 3 ----------------
body3 = recap("Com o ambiente pronto, falta ligar algo ao ESP32. Este capítulo trata dos <b>pinos (GPIO)</b>, de como acender um <b>LED</b> sem queimá-lo e do primeiro programa de saída digital.") + '''
<section class="sec" id="gpio">
  <h2><span class="sn">1</span>GPIO: os pinos de uso geral</h2>
  <p class="gancho">Nem todo pino serve para tudo.</p>
  <p><b>GPIO</b> significa <i>General Purpose Input/Output</i>: pinos que o programa pode configurar como <b>entrada</b> (ler um sinal) ou <b>saída</b> (emitir um sinal). A placa usada na disciplina tem <b>30 pinos</b>, divididos nos dois lados, mas há restrições. Clique nos pinos e teste uma combinação:</p>
  <div class="demo" data-demo="gpio"></div>
  <ul>
    <li><b>Somente entrada</b>: GPIO <b>34, 35, 36 e 39</b>. São entradas analógicas (ADC1), usadas para medir sensores.</li>
    <li><b>Reservados, não use</b>: GPIO <b>6 a 11</b>. Ligados à memória flash.</li>
    <li><b>Serial do console</b>: GPIO <b>1 (TX)</b> e <b>3 (RX)</b>. Usá-los para outra função atrapalha o Monitor Serial.</li>
    <li><b>GPIO 2</b>: ligado ao LED embutido da placa.</li>
    <li><b>PWM no boot</b>: GPIO <b>0, 5, 13 e 14</b>. Cuidado com o que estiver ligado neles ao ligar a placa.</li>
    <li>Todos os demais são livres, como entrada ou saída.</li>
  </ul>
</section>

<section class="sec" id="led">
  <h2><span class="sn">2</span>O LED: polaridade e resistor</h2>
  <p class="gancho">Um LED é um diodo: tem lado certo, e não aguenta corrente livre.</p>
  <p>O LED tem <b>anodo (+)</b>, a perna longa, e <b>catodo (−)</b>, a perna curta (lado chanfrado). Ele só conduz do anodo para o catodo. Ligado ao contrário, <b>não acende e não dá erro nenhum</b>, o que o torna um dos bugs mais chatos de achar. O lado positivo vem do pino do ESP32 (que "liga e desliga"); o negativo vai ao <b>GND</b>, um fio comum a todo o circuito, como um barramento.</p>
  <p>O <b>resistor em série</b> é obrigatório: ele limita a corrente. Pela lei de Ohm, <code>R = (V_pino − V_LED) / I</code>. Com um LED vermelho (queda de cerca de 2,0 V) em um pino de 3,3 V e um resistor de 220 Ω, a corrente é <code>(3,3 − 2,0) / 220 ≈ 5,9 mA</code>: segura para o pino e suficiente para o brilho. Calcule o seu:</p>
  <div class="demo" data-demo="ohm"></div>
</section>

<section class="sec" id="pisca">
  <h2><span class="sn">3</span>O primeiro programa: pisca-pisca</h2>
  <p class="gancho">Três passos que valem para qualquer saída.</p>
  <ol>
    <li><b>Definir o pino</b> do atuador, antes do <code>setup()</code>.</li>
    <li><b>Configurar o pino</b> no <code>setup()</code>: <code>OUTPUT</code> para um atuador, <code>INPUT</code> para um sensor.</li>
    <li><b>Usar o pino</b> no <code>loop()</code>.</li>
  </ol>
<pre><code><span class="k">#define</span> LED 22              <span class="c">// o pré-processador troca LED por 22 antes de compilar</span>

<span class="k">void</span> setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);       <span class="c">// sem esta linha, o LED não acende</span>
  Serial.println("Sistema de controle de LED");
}

<span class="k">void</span> loop() {
  digitalWrite(LED, HIGH);    <span class="c">// HIGH = 3,3 V no pino: acende</span>
  delay(500);                 <span class="c">// espera 500 ms</span>
  digitalWrite(LED, LOW);     <span class="c">// LOW = 0 V: apaga</span>
  delay(500);
}</code></pre>
  <p>O período completo é 500 ms aceso + 500 ms apagado = <b>1 s</b>, ou seja, <b>1 Hz</b>. <code>digitalWrite</code> só escreve dois estados, HIGH e LOW (para brilho intermediário seria PWM). O <code>#define</code> <b>não cria uma variável</b>: troca o texto antes de compilar e não ocupa RAM. Sem o <code>delay</code>, o ESP32 (240 MHz) alternaria o LED rápido demais para o olho perceber.</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: o delay não é "a velocidade da simulação"</span>É uma <b>pausa que trava o processador</b> pelo tempo indicado. Enquanto ele espera, o ESP32 não faz mais nada. O Capítulo 6 mostra o que isso custa.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>GPIO</b>: pinos de entrada ou saída. <b>34, 35, 36, 39</b> só entrada; <b>6 a 11</b> reservados (flash); <b>1 e 3</b> são o serial; <b>2</b> é o LED embutido.",
    "LED: <b>anodo (+)</b> perna longa, <b>catodo (−)</b> perna curta ao GND. Invertido não acende e não avisa.",
    "Resistor: <code>R = (V_pino − V_LED)/I</code>. Vermelho + 220 Ω + 3,3 V ≈ 5,9 mA.",
    "Saída digital: <code>pinMode(pino, OUTPUT)</code> e <code>digitalWrite(pino, HIGH/LOW)</code>. <code>#define</code> troca texto, sem RAM.",
    "<code>delay</code> <b>bloqueia</b> o processador."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "Você quer usar o GPIO 34 como saída para acender um LED. Funciona?", [("a","Não: o GPIO 34 é somente entrada."),("b","Sim, qualquer GPIO serve."),("c","Sim, mas só com um resistor maior.")], "Os GPIOs 34, 35, 36 e 39 são só entrada (ADC1).") + quiz(2, "c", "Qual a corrente de um LED vermelho (2,0 V) em 3,3 V com resistor de 220 Ω?", [("a","Cerca de 15 mA."),("b","Cerca de 60 mA."),("c","Cerca de 5,9 mA: (3,3 − 2,0) / 220.")], "Lei de Ohm: 1,3 V sobre 220 Ω dá 5,9 mA.") + quiz(3, "b", "O que faz o #define LED 22?", [("a","Cria uma variável do tipo int que ocupa RAM."),("b","Faz o pré-processador trocar o texto LED por 22 antes de compilar."),("c","Liga o LED.")], "É substituição de texto, sem variável nem RAM.") + flash([
    ("O que é o GND?", "O fio comum de referência (0 V) a que o negativo de todos os componentes se liga."),
    ("Por que o LED precisa de resistor?", "Para limitar a corrente. Sem ele, o LED e o pino podem queimar."),
    ("HIGH e LOW?", "HIGH = 3,3 V no pino; LOW = 0 V."),
    ("O que acontece se o LED for ligado ao contrário?", "Não acende, e não aparece nenhum erro.")]) + ponte("O LED pisca, mas o programa que o controla ainda é uma caixa preta. Como o setup, o loop e o Serial funcionam?", "Vamos abrir o modelo de execução.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "gpio-e-led", T, "GPIO, LED e resistor", "Capítulo 3 · Aulas 1, 2 e 6",
        "Que pinos usar, como ligar um LED com o resistor certo e o primeiro programa de saída digital.",
        ["<b>~40 min</b>", "2 demos · 3 testes · 4 flashcards", "mapa de pinos e calculadora de resistor"], body3, scripts=S)
print("emb caps 1-3 ok")
