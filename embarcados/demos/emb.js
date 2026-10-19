/* Demos da apostila de Sistemas Embarcados com ESP32 */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function f(x, d) { if (!isFinite(x)) return "nan"; d = d === undefined ? 2 : d; return x.toFixed(d); }
  function fb(x, d) { return f(x, d).replace(".", ","); }

  /* ---- cap 1: onde o erro aparece: build em 3 etapas ---- */
  var BUGS = [
    { k: "Código correto", fase: 4, msg: "Compilou e roda. O Monitor Serial mostra a saída esperada.", code: 'void setup() {\n  Serial.begin(115200);\n  pinMode(2, OUTPUT);\n}\nvoid loop() {\n  digitalWrite(2, HIGH);\n  delay(500);\n}' },
    { k: "Faltou o ponto e vírgula", fase: 2, msg: "error: expected ';' before 'delay'", code: 'void loop() {\n  digitalWrite(2, HIGH)   // <- falta ;\n  delay(500);\n}' },
    { k: "Variável não declarada", fase: 2, msg: "error: 'led' was not declared in this scope", code: 'void setup() {\n  pinMode(led, OUTPUT);   // led nunca foi declarada\n}' },
    { k: "Biblioteca não instalada", fase: 1, msg: "fatal error: DHT.h: No such file or directory", code: '#include <DHT.h>   // a biblioteca não está em lib_deps\nvoid setup() { }' },
    { k: "Função declarada, mas nunca escrita", fase: 3, msg: "undefined reference to `lerSensor()'", code: 'float lerSensor();    // só a declaração\nvoid loop() {\n  float x = lerSensor();\n}' },
    { k: "Esqueceu o pinMode(OUTPUT)", fase: 4, msg: "Compila sem erro. O LED simplesmente não acende: o pino continua como entrada. Erro silencioso.", code: 'void setup() {\n  Serial.begin(115200);\n  // pinMode(2, OUTPUT);   <- esquecido\n}\nvoid loop() {\n  digitalWrite(2, HIGH);\n}', silencioso: true },
    { k: "Esqueceu o Serial.begin", fase: 4, msg: "Compila e roda, mas o Monitor Serial fica mudo.", code: 'void setup() {\n  // Serial.begin(115200);  <- esquecido\n}\nvoid loop() {\n  Serial.println("oi");\n}', silencioso: true },
    { k: "Não salvou o arquivo", fase: 4, msg: "Compila e roda a versão ANTERIOR: o compilador usa o arquivo salvo em disco, e não o que está na tela.", code: '// Você mudou o código na tela,\n// mas esqueceu de salvar (Ctrl+S).', silencioso: true }
  ];
  E.demos.compila = function (el) {
    el.innerHTML = '<h4>Em que etapa cada erro aparece?</h4><div class="ctrls"><label>erro <select id="cp-s">' + BUGS.map(function (b, i) { return '<option value="' + i + '">' + b.k + '</option>'; }).join("") + '</select></label></div><div class="grid2"><div><b>Código</b><pre class="raw cp-code"></pre></div><div><div class="cp-steps"></div></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, NOMES = ["1. Pré-processamento (#include, #define)", "2. Compilação (código vira objeto)", "3. Linkagem (junta bibliotecas)", "4. Execução no ESP32"];
    function go() {
      var b = BUGS[+g("#cp-s").value]; g(".cp-code").textContent = b.code;
      g(".cp-steps").innerHTML = NOMES.map(function (n, i) { var num = i + 1, st = num < b.fase ? "ok" : num === b.fase && b.fase < 4 ? "falha" : num === b.fase ? (b.silencioso ? "silencioso" : "ok") : "nao"; var cor = st === "ok" ? "var(--green)" : st === "falha" ? "var(--red)" : st === "silencioso" ? "var(--pen)" : "var(--muted)"; return '<div class="card" style="margin:0 0 8px;padding:8px 12px;border-left:6px solid ' + cor + '"><b>' + n + '</b><br><span class="muted">' + (st === "ok" ? "passou" : st === "falha" ? "FALHOU aqui" : st === "silencioso" ? "roda, mas se comporta errado" : "não chegou aqui") + '</span></div>'; }).join("");
      g(".read").innerHTML = "<pre class='raw'>" + esc(b.msg) + "</pre>" + (b.silencioso ? "<b>Os piores erros são os que compilam.</b> O compilador só reclama de erro de escrita; erros de lógica ou de esquecimento aparecem no comportamento da placa. É por isso que se imprime no Monitor Serial e se testa passo a passo." : b.fase < 4 ? "<b>O código só roda se compilar sem erros.</b> Quando o erro é de escrita, o build para e aponta a linha." : "");
    }
    el.addEventListener("change", go); go();
  };

  /* ---- cap 2: mapa de GPIO ---- */
  var GP = {};
  [34, 35, 36, 39].forEach(function (p) { GP[p] = { c: "ent", t: "Só entrada. É uma entrada analógica do ADC1, usada para medir sensores. Não pode ser saída." }; });
  [6, 7, 8, 9, 10, 11].forEach(function (p) { GP[p] = { c: "res", t: "Reservado: ligado à memória flash (SPI). Não use." }; });
  GP[1] = { c: "ser", t: "TX do console serial (UART). Usá-lo para outra coisa atrapalha o Monitor Serial. É saída de depuração no boot." };
  GP[3] = { c: "ser", t: "RX do console serial (UART). Fica em HIGH no boot. Evite para outras funções." };
  GP[2] = { c: "led", t: "Ligado ao LED embutido da placa. Pode ser usado, mas influencia o boot em algumas placas." };
  [0, 5, 13, 14].forEach(function (p) { GP[p] = { c: "boot", t: "Emite sinal PWM no boot: cuidado com o que estiver ligado nele quando a placa liga." }; });
  [4, 12, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33].forEach(function (p) { GP[p] = { c: "livre", t: p === 12 || p === 15 ? "Entrada ou saída livre, mas é um pino de 'strapping' (afeta o boot se estiver em nível errado no momento de ligar). Evite se puder." : "Livre: pode ser configurado como entrada ou saída." }; });
  [20, 24, 28, 29, 30, 31, 37, 38].forEach(function (p) { GP[p] = { c: "nao", t: "Não aparece na placa de 30 pinos usada na disciplina." }; });
  var COR = { ent: "var(--c2)", res: "var(--red)", ser: "var(--pen)", led: "var(--c1)", boot: "var(--c0)", livre: "var(--green)", nao: "var(--muted)" };
  var LEG = { ent: "só entrada", res: "reservado (flash)", ser: "serial (TX/RX)", led: "LED embutido", boot: "PWM no boot", livre: "livre", nao: "indisponível" };
  E.demos.gpio = function (el) {
    el.innerHTML = '<h4>Mapa dos GPIOs do ESP32 (placa de 30 pinos)</h4><div class="legend"></div><div class="gpg" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(54px,1fr));gap:6px;margin:10px 0"></div><div class="ctrls"><label>quero usar o GPIO <input type="number" id="gp-n" min="0" max="39" value="34" style="width:70px"></label><label>como <select id="gp-m"><option value="OUTPUT">saída (OUTPUT)</option><option value="INPUT">entrada (INPUT)</option></select></label></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    g(".legend").innerHTML = Object.keys(LEG).map(function (k) { return '<span><i style="background:' + COR[k] + '"></i>' + LEG[k] + '</span>'; }).join("");
    var grid = g(".gpg");
    for (var p = 0; p <= 39; p++) { var b = document.createElement("button"); b.type = "button"; b.className = "btn sm"; b.dataset.p = p; b.textContent = p; b.style.cssText = "border-left:8px solid " + COR[GP[p].c] + ";"; b.setAttribute("aria-label", "GPIO " + p + ": " + LEG[GP[p].c]); grid.appendChild(b); }
    function verdict() {
      var p = +g("#gp-n").value, m = g("#gp-m").value, info = GP[p]; if (!info) { g(".read").textContent = "Digite um número de 0 a 39."; return; }
      var ok = info.c === "livre" || info.c === "led" || info.c === "boot" ? true : info.c === "ent" ? m === "INPUT" : false;
      g(".read").innerHTML = "<b>GPIO " + p + "</b> como <code>" + m + "</code>: " + (ok ? "<b style='color:var(--green)'>pode</b>" + (info.c === "livre" ? "." : ", com ressalvas.") : "<b style='color:var(--red)'>não é boa ideia / não funciona</b>.") + "<br>" + info.t + "<br><span class='muted'>Tabela da aula. Confira também o datasheet da placa que você usa, porque o mapeamento varia de modelo para modelo.</span>";
    }
    grid.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-p]"); if (b) { g("#gp-n").value = b.dataset.p; verdict(); } });
    el.addEventListener("input", verdict); el.addEventListener("change", verdict); verdict();
  };

  /* ---- cap 2: resistor do LED ---- */
  var E12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820, 1000, 1200, 1500, 1800, 2200];
  E.demos.ohm = function (el) {
    el.innerHTML = '<h4>Que resistor usar com o LED?</h4><div class="ctrls"><label>cor do LED <select id="oh-c"><option value="2.0">vermelho (≈ 2,0 V)</option><option value="2.1">amarelo (≈ 2,1 V)</option><option value="2.2">verde (≈ 2,2 V)</option><option value="3.0">azul ou branco (≈ 3,0 V)</option></select></label><label>corrente desejada <input type="range" id="oh-i" min="2" max="20" step="1" value="10"><output id="oh-io"></output></label></div><div class="sg"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function go() {
      var vf = +g("#oh-c").value, i = +g("#oh-i").value / 1000, vr = 3.3 - vf; g("#oh-io").textContent = (i * 1000) + " mA";
      var r = vr / i, pad = E12.filter(function (x) { return x >= r; })[0] || E12[E12.length - 1], ireal = vr / pad;
      var it = [["tensão sobre o resistor", fb(vr, 2) + " V"], ["R calculado", fb(r, 0) + " Ω"], ["valor comercial (série E12) ≥", pad + " Ω"], ["corrente real", fb(ireal * 1000, 1) + " mA"]];
      g(".sg").innerHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px;margin:10px 0">' + it.map(function (p) { return '<div class="card" style="margin:0;padding:8px 10px"><small class="muted">' + p[0] + '</small><div style="font:700 1.15rem var(--f-mono)">' + p[1] + '</div></div>'; }).join("") + '</div>';
      g(".read").innerHTML = "<code>R = (V_pino − V_LED) / I = (3,3 − " + fb(vf, 1) + ") / " + fb(i, 3) + " = " + fb(r, 0) + " Ω</code>. Escolhe-se o valor comercial <b>igual ou maior</b>, para a corrente ficar igual ou menor que a desejada. " + (vf >= 3 ? "<b>Atenção:</b> LEDs azuis e brancos precisam de cerca de 3 V; com 3,3 V sobra pouca margem e a corrente é muito sensível a pequenas variações." : "") + (ireal > 0.012 ? " <b>Corrente alta para um pino de microcontrolador.</b> Prefira valores menores." : "") + " Sem resistor, o LED ficaria limitado só pela própria resistência interna e queimaria.";
    }
    el.addEventListener("input", go); go();
  };

  /* ---- cap 3: setup, loop e variável global ---- */
  E.demos.serial = function (el) {
    el.innerHTML = '<h4>Simule o Monitor Serial</h4><div class="ctrls"><label>variável <code>id</code> <select id="sr-v"><option value="g">global (fora do loop)</option><option value="l">local (dentro do loop)</option></select></label><label>impressão <select id="sr-p"><option value="ln">println (quebra linha)</option><option value="pr">print (sem quebra)</option></select></label><label>delay(ms) <input type="range" id="sr-d" min="100" max="3000" step="100" value="2000"><output id="sr-do"></output></label></div><div class="grid2"><div><b>Código</b><pre class="raw sr-code"></pre></div><div><b>Monitor Serial</b><pre class="raw sr-out" style="min-height:130px"></pre></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function go() {
      var glob = g("#sr-v").value === "g", ln = g("#sr-p").value === "ln", d = +g("#sr-d").value; g("#sr-do").textContent = d;
      var pr = ln ? "println" : "print";
      g(".sr-code").textContent = (glob ? "int id = 0;\n\n" : "") + "void setup() {\n  Serial.begin(115200);\n}\n\nvoid loop() {\n" + (glob ? "" : "  int id = 0;\n") + "  id = id + 1;\n  Serial." + pr + "(\"Contagem: \");\n  Serial." + pr + "(id);\n  delay(" + d + ");\n}";
      var out = "", id = 0, linhas = [];
      for (var k = 0; k < 5; k++) { id = glob ? id + 1 : 1; var t = k * d; linhas.push("[t = " + t + " ms]  " + (ln ? "Contagem: \n" + id : "Contagem: " + id)); }
      g(".sr-out").textContent = ln ? linhas.map(function (l) { return l.replace("\n", "\n              "); }).join("\n") : linhas.map(function (l) { return l.replace(/\[t = \d+ ms\]\s+/, ""); }).join("") + "...";
      g(".read").innerHTML = (glob ? "Com <code>id</code> <b>global</b>, o valor sobrevive entre as voltas do <code>loop()</code>: 1, 2, 3, 4, 5." : "Com <code>id</code> <b>local</b>, a variável é recriada em 0 a cada volta: imprime <b>1 para sempre</b>.") + (ln ? "" : " Com <code>print</code> (sem <code>ln</code>) tudo sai <b>grudado</b>, na mesma linha.") + " O <code>setup()</code> roda <b>uma vez</b>; o <code>loop()</code> repete a cada " + d + " ms (o <code>delay</code> é uma pausa que trava o processador).";
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---- cap 4: printf e divisão inteira ---- */
  E.demos.formato = function (el) {
    el.innerHTML = '<h4>Formatando a saída e cuidado com a divisão</h4><div class="grid2"><div><div class="ctrls"><label>valor <input type="number" id="fm-v" value="27.456" step="any" style="width:110px"></label><label>formato <select id="fm-f"><option value="%d">%d (inteiro)</option><option value="%.2f">%.2f (2 casas)</option><option value="%.7f">%.7f (7 casas)</option><option value="%c">%c (caractere)</option><option value="%5d">%5d (largura 5)</option><option value="%x">%x (hexadecimal)</option></select></label></div><pre class="raw fm-o"></pre></div><div><div class="ctrls"><label>a <input type="number" id="fm-a" value="10" style="width:70px"></label><label>b <input type="number" id="fm-b" value="4" style="width:70px"></label></div><pre class="raw fm-d"></pre></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function go() {
      var v = +g("#fm-v").value, fm = g("#fm-f").value, s;
      if (fm === "%d") s = String(Math.trunc(v)); else if (fm === "%c") s = String.fromCharCode(Math.trunc(v)); else if (fm === "%5d") s = String(Math.trunc(v)).padStart(5, " "); else if (fm === "%x") s = Math.trunc(v).toString(16); else s = v.toFixed(+fm.slice(2, 3));
      var inteiro = /[dcx]$/.test(fm); g(".fm-o").textContent = "float x = " + v + ";\nSerial.printf(\"Valor: " + fm + "\r\n\", " + (inteiro ? "(int)x" : "x") + ");\n→ Valor: " + s + (fm === "%.7f" ? "\n(a demo usa precisão de double; num float de 32 bits do ESP32 os últimos dígitos podem diferir)" : "");
      var a = Math.trunc(+g("#fm-a").value), b = Math.trunc(+g("#fm-b").value);
      g(".fm-d").textContent = b === 0 ? "b = 0: divisão por zero! Em inteiros o programa pode travar." : "int   a / b  = " + Math.trunc(a / b) + "\nint   a % b  = " + (a % b) + "\nfloat a / b  = " + (a / b).toFixed(2) + "   (se um dos dois for float)";
      g(".read").innerHTML = "O <code>%</code> escolhe como o número vira texto: <code>%d</code> exige um <b>int</b> (passar um float direto é comportamento indefinido e imprime lixo; converta com <code>(int)x</code>, que descarta a parte decimal: " + Math.trunc(v) + "), <code>%.2f</code> decimal com 2 casas, <code>%c</code> um caractere, <code>%s</code> texto. Já a divisão entre <b>dois inteiros</b> também é inteira: <code>10 / 4</code> dá <b>2</b>, e não 2,5. Para ter decimais, ao menos um dos lados precisa ser <code>float</code> (<code>10.0 / 4</code>).";
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---- cap 5: o botão e o pull-up ---- */
  E.demos.botao = function (el) {
    el.innerHTML = '<h4>Por que apertar o botão dá LOW?</h4><div class="ctrls"><label>modo <select id="bt-m"><option value="PU">INPUT_PULLUP</option><option value="IN">INPUT (sem resistor externo)</option></select></label><button class="btn sm pri" type="button" id="bt-b" aria-pressed="false">Botão: solto (clique para apertar)</button></div><div class="grid2"><div class="card" style="margin:0"><div class="bt-v"></div></div><div><pre class="raw bt-c"></pre></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, press = false, timer = 0;
    function level() { var m = g("#bt-m").value; if (m === "PU") return press ? 0 : 1; return press ? 0 : (Math.random() < .5 ? 0 : 1); }
    function paint() {
      var m = g("#bt-m").value, lv = level(), flut = m === "IN" && !press;
      g(".bt-v").innerHTML = '<div style="font:.95rem var(--f-mono);line-height:1.8">pino BTN_PIN em ' + (m === "PU" ? "<b>INPUT_PULLUP</b>" : "<b>INPUT</b>") + '<br>botão: <b>' + (press ? "apertado (liga o pino ao GND)" : "solto") + '</b><br>digitalRead(BTN_PIN) = <b style="font-size:1.4rem;color:var(--pen)">' + (lv ? "HIGH (1)" : "LOW (0)") + '</b>' + (flut ? '<br><span style="color:var(--red)">pino flutuando: valor aleatório</span>' : "") + "</div>";
      g(".bt-c").textContent = "pinMode(BTN_PIN, " + (m === "PU" ? "INPUT_PULLUP" : "INPUT") + ");\n\nif (digitalRead(BTN_PIN) == LOW) {\n  // 'botão pressionado' → " + (lv === 0 ? "ENTRA aqui" : "não entra") + "\n}";
      g(".read").innerHTML = m === "PU" ? "Com <code>INPUT_PULLUP</code> o ESP32 liga um resistor interno que mantém o pino em <b>HIGH</b> quando o botão está solto. Apertar liga o pino ao GND: <b>LOW</b>. A lógica é <b>invertida</b>: pressionado = LOW. Não precisa de resistor externo no botão." : "Com <code>INPUT</code> puro e sem resistor externo, o pino solto <b>flutua</b>: capta ruído e <code>digitalRead</code> devolve valores aleatórios. O LED pode piscar sozinho. Por isso o botão pede <code>INPUT_PULLUP</code> (ou um resistor externo).";
    }
    function tick() { if (g("#bt-m").value === "IN" && !press) paint(); }
    g("#bt-b").addEventListener("click", function () { press = !press; this.textContent = press ? "Botão: apertado (clique para soltar)" : "Botão: solto (clique para apertar)"; this.setAttribute("aria-pressed", press ? "true" : "false"); paint(); });
    el.addEventListener("change", paint);
    timer = setInterval(function () { if (!document.body.contains(el)) { clearInterval(timer); return; } tick(); }, E.reduce ? 3000 : 600);
    paint();
  };

  /* ---- cap 5: o delay bloqueante perde toques ---- */
  E.demos.bloqueio = function (el) {
    el.innerHTML = '<h4>Um botão apertado a cada 0,7 s durante 10 s</h4><div class="ctrls"><label>o programa lê o botão a cada <input type="range" id="bl-p" min="10" max="2000" step="10" value="2000"><output id="bl-po"></output> ms</label></div><canvas style="height:140px;cursor:default"></canvas><div class="sg"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, cv = el.querySelector("canvas"), P = 2000, T = 10000, DUR = 150, STEP = 700;
    function taps() { var a = []; for (var k = 0; k * STEP < T; k++) a.push(k * STEP); return a; }
    function det(p) { var d = 0, reads = []; for (var t = 0; t <= T; t += p) reads.push(t); taps().forEach(function (s) { if (reads.some(function (r) { return r >= s && r < s + DUR; })) d++; }); return d; }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var pad = 16, X = function (ms) { return pad + ms / T * (w - 2 * pad); }; ctx.save();
      ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
      for (var s = 0; s <= 10; s += 2) { ctx.beginPath(); ctx.moveTo(X(s * 1000), 10); ctx.lineTo(X(s * 1000), h - 24); ctx.stroke(); ctx.fillText(s + " s", X(s * 1000), h - 8); }
      taps().forEach(function (t) { ctx.fillStyle = c.pen; ctx.fillRect(X(t), 30, Math.max(3, X(t + DUR) - X(t)), 30); });
      var reads = []; for (var t2 = 0; t2 <= T; t2 += P) reads.push(t2);
      ctx.fillStyle = c.red; reads.forEach(function (r) { if (P >= 100 || r % 100 === 0) { ctx.fillRect(X(r) - 1, 76, 2, 26); } });
      ctx.fillStyle = c.ink; ctx.textAlign = "left"; ctx.font = "600 11px Inter,system-ui,sans-serif"; ctx.fillText("toques do usuário (azul)", pad, 24); ctx.fillText("leituras do programa (vermelho)", pad, 70); ctx.restore();
    });
    function go() {
      P = +g("#bl-p").value; g("#bl-po").textContent = P; var n = taps().length, d = det(P);
      g(".sg").innerHTML = '<div class="card" style="margin:8px 0;padding:8px 12px"><small class="muted">toques percebidos</small><div style="font:700 1.4rem var(--f-mono)">' + d + " de " + n + " (" + Math.round(d / n * 100) + "%)</div></div>";
      g(".read").innerHTML = "Cada toque dura " + DUR + " ms. O programa só enxerga o botão no instante em que <code>digitalRead</code> roda. " + (P >= 1000 ? "Com <code>delay</code>s de segundos no <code>loop()</code>, <b>quase todos os toques se perdem</b>: o ESP32 está 'surdo' enquanto espera." : P > 150 ? "Com intervalo maior que a duração do toque, alguns toques caem entre duas leituras." : "Lendo com frequência (intervalo menor que o toque), nenhum toque se perde.") + " A solução profissional é <b>não bloquear</b>: usar <code>millis()</code> para medir o tempo e deixar o <code>loop()</code> girar livre (complemento).";
      api.paint();
    }
    el.addEventListener("input", go); go();
  };

  /* ---- cap 6: DHT22 simulado e índice de calor ---- */
  function heatIndexC(tc, rh) {
    var t = tc * 9 / 5 + 32, hi = 0.5 * (t + 61.0 + ((t - 68.0) * 1.2) + (rh * 0.094));
    if (hi > 79) {
      hi = -42.379 + 2.04901523 * t + 10.14333127 * rh - 0.22475541 * t * rh - 0.00683783 * t * t - 0.05481717 * rh * rh + 0.00122874 * t * t * rh + 0.00085282 * t * rh * rh - 0.00000199 * t * t * rh * rh;
      if (rh < 13 && t >= 80 && t <= 112) hi -= ((13 - rh) * 0.25) * Math.sqrt((17 - Math.abs(t - 95)) * 0.05882);
      else if (rh > 85 && t >= 80 && t <= 87) hi += ((rh - 85) * 0.1) * ((87 - t) * 0.2);
    }
    return (hi - 32) * 5 / 9;
  }
  E.demos.dht = function (el) {
    el.innerHTML = '<h4>Um DHT22 virtual: ajuste como no simulador</h4><div class="ctrls"><label>temperatura (°C) <input type="range" id="dh-t" min="-10" max="50" step="0.5" value="24"><output id="dh-to"></output></label><label>umidade (%) <input type="range" id="dh-u" min="0" max="100" step="1" value="40"><output id="dh-uo"></output></label><label><input type="checkbox" id="dh-f"> sensor desconectado (leitura falha)</label></div><div class="grid2"><div><b>Monitor Serial</b><pre class="raw dh-o" style="min-height:120px"></pre></div><div class="card" style="margin:0"><div class="dh-s"></div></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function go() {
      var t = +g("#dh-t").value, u = +g("#dh-u").value, falha = g("#dh-f").checked; g("#dh-to").textContent = fb(t, 1) + " °C"; g("#dh-uo").textContent = u + "%";
      if (falha) { g(".dh-o").textContent = "Falha na leitura!!!"; g(".dh-s").innerHTML = "<div style='font:.95rem var(--f-mono)'>readTemperature() = <b>nan</b><br>readHumidity() = <b>nan</b><br>isnan(...) → <b>true</b> → return</div>"; g(".read").innerHTML = "Quando a leitura falha, a biblioteca devolve <code>NaN</code> (<i>not a number</i>). O código testa <code>isnan()</code> <b>antes</b> de usar o valor, imprime o erro e dá <code>return</code>: o <code>loop()</code> recomeça na volta seguinte. Sem esse teste, o programa imprimiria e compararia lixo."; return; }
      var ic = heatIndexC(t, u), linhas = ["Temperatura: " + f(t, 2) + "  |  Umidade: " + f(u, 2)];
      if (t > 35) linhas.push("-- ALERTA -- Temperatura Alta!"); if (u > 65) linhas.push("-- ALERTA -- Umidade Alta!");
      linhas.push("Índice de calor: " + f(ic, 2) + (ic > 25 ? "  → ALTO! LED aceso" : "  → normal, LED apagado"));
      g(".dh-o").textContent = linhas.join("\n");
      g(".dh-s").innerHTML = "<div style='font:.95rem var(--f-mono);line-height:1.8'>temp &gt; 35 ? <b>" + (t > 35) + "</b><br>umid &gt; 65 ? <b>" + (u > 65) + "</b><br>índice de calor = <b>" + f(ic, 1) + " °C</b><br>ic &gt; 25 ? <b style='color:var(--pen)'>" + (ic > 25) + "</b> (LED " + (ic > 25 ? "HIGH" : "LOW") + ")</div>";
      g(".read").innerHTML = "Os dois alertas são <code>if</code> <b>separados</b> (não <code>if/else</code>), porque temperatura e umidade podem estar altas ao mesmo tempo. O <b>índice de calor</b> junta as duas: com o ar úmido o suor evapora pior e o calor <i>parece</i> maior. Neste simulador o cálculo segue a lógica usada pela biblioteca da Adafruit (uma média simples, de Steadman, para valores baixos, e a regressão de Rothfusz, com ajustes, acima de cerca de 80 °F). Complemento: a aula não detalhou a fórmula, e os decimais podem diferir um pouco da sua versão da biblioteca.";
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };
})();
