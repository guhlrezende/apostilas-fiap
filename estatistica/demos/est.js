/* Demos da apostila de Estatística com R e Python */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function gauss(r) { var u = 1 - r(), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  /* número no formato brasileiro */
  function f(x, d) { if (!isFinite(x)) return "n/d"; d = d === undefined ? 2 : d; return x.toFixed(d).replace(".", ","); }
  function plotter(w, h, x0, x1, y0, y1, pad) { pad = pad || { l: 46, r: 12, t: 12, b: 32 }; return { pad: pad, X: function (x) { return pad.l + (x - x0) / (x1 - x0) * (w - pad.l - pad.r); }, Y: function (y) { return pad.t + (1 - (y - y0) / (y1 - y0)) * (h - pad.t - pad.b); } }; }
  function axes(ctx, w, h, P, x0, x1, y0, y1, xs, ys, xl, yl, c) {
    ctx.save(); ctx.lineWidth = 1; ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
    for (var x = Math.ceil(x0 / xs) * xs; x <= x1 + 1e-9; x += xs) { ctx.beginPath(); ctx.moveTo(P.X(x), P.pad.t); ctx.lineTo(P.X(x), h - P.pad.b); ctx.stroke(); ctx.fillText(+x.toFixed(2), P.X(x), h - P.pad.b + 14); }
    if (ys) { ctx.textAlign = "right"; for (var y = Math.ceil(y0 / ys) * ys; y <= y1 + 1e-9; y += ys) { ctx.beginPath(); ctx.moveTo(P.pad.l, P.Y(y)); ctx.lineTo(w - P.pad.r, P.Y(y)); ctx.stroke(); ctx.fillText(+y.toFixed(2), P.pad.l - 6, P.Y(y) + 4); } }
    ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.textAlign = "center"; ctx.fillText(xl, (P.pad.l + w - P.pad.r) / 2, h - 4);
    if (yl) { ctx.save(); ctx.translate(12, (P.pad.t + h - P.pad.b) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText(yl, 0, 0); ctx.restore(); } ctx.restore();
  }

  function nice(x) { var p = Math.pow(10, Math.floor(Math.log10(x))), m = x / p; return (m > 5 ? 10 : m > 2 ? 5 : m > 1 ? 2 : 1) * p; }

  /* ---------- estatísticas ---------- */
  function quant(s, q) { var p = (s.length - 1) * q, i = Math.floor(p), fr = p - i; return i + 1 < s.length ? s[i] * (1 - fr) + s[i + 1] * fr : s[i]; }
  function resumo(v) {
    var n = v.length, s = v.slice().sort(function (a, b) { return a - b; }), soma = 0; v.forEach(function (x) { soma += x; });
    var m = soma / n, ss = 0; v.forEach(function (x) { ss += (x - m) * (x - m); });
    var var1 = n > 1 ? ss / (n - 1) : NaN, sd = Math.sqrt(var1), q1 = quant(s, .25), q2 = quant(s, .5), q3 = quant(s, .75), iqr = q3 - q1;
    var cont = {}, mx = 0; v.forEach(function (x) { cont[x] = (cont[x] || 0) + 1; if (cont[x] > mx) mx = cont[x]; });
    var moda = mx > 1 ? Object.keys(cont).filter(function (k) { return cont[k] === mx; }).map(Number).sort(function (a, b) { return a - b; }) : [];
    var lo = q1 - 1.5 * iqr, hi = q3 + 1.5 * iqr, fora = s.filter(function (x) { return x < lo || x > hi; });
    var dentro = s.filter(function (x) { return x >= lo && x <= hi; });
    return { n: n, s: s, media: m, mediana: q2, q1: q1, q3: q3, iqr: iqr, min: s[0], max: s[n - 1], var1: var1, sd: sd, cv: sd / m * 100, moda: moda, mx: mx, lo: lo, hi: hi, fora: fora, wlo: dentro[0], whi: dentro[dentro.length - 1] };
  }

  /* ---- cap 2: tamanho da amostra ---- */
  E.demos.amostra = function (el) {
    el.innerHTML = '<h4>Quantas pessoas preciso entrevistar?</h4><div class="ctrls"><label>confiança <select id="am-c"><option value="1.645">90%</option><option value="1.96" selected>95%</option><option value="2.576">99%</option></select></label><label>margem de erro <input type="range" id="am-e" min="1" max="10" step="0.5" value="5"><output id="am-eo"></output></label><label>proporção esperada p <input type="range" id="am-p" min="10" max="90" step="5" value="50"><output id="am-po"></output></label><label>população <select id="am-n"><option value="0">indefinida (grande)</option><option value="200">200</option><option value="500">500</option><option value="1000">1.000</option><option value="5000">5.000</option><option value="20000">20.000</option></select></label></div><canvas style="height:230px;cursor:default"></canvas><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, cv = el.querySelector("canvas"), Z = 1.96, p = 0.5, e = 0.05, N = 0, curN = 385;
    function n0(ee) { return Z * Z * p * (1 - p) / (ee * ee); }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var top = Math.min(12000, Math.ceil(n0(0.01) / 1000) * 1000), P = plotter(w, h, 1, 10, 0, top, { l: 52, r: 12, t: 12, b: 32 });
      axes(ctx, w, h, P, 1, 10, 0, top, 1, top / 4, "margem de erro (%)", "amostra n", c);
      ctx.beginPath(); for (var i = 0; i <= 90; i++) { var x = 1 + i * 0.1, y = Math.min(top, n0(x / 100)); if (i) ctx.lineTo(P.X(x), P.Y(y)); else ctx.moveTo(P.X(x), P.Y(y)); } ctx.lineWidth = 3; ctx.strokeStyle = c.pen; ctx.stroke();
      var cur = Math.min(top, curN); ctx.beginPath(); ctx.arc(P.X(e * 100), P.Y(cur), 7, 0, 6.2832); ctx.fillStyle = c.red; ctx.fill();
    });
    function go() {
      Z = +g("#am-c").value; e = +g("#am-e").value / 100; p = +g("#am-p").value / 100; N = +g("#am-n").value;
      g("#am-eo").textContent = f(e * 100, 1) + "%"; g("#am-po").textContent = f(p * 100, 0) + "%";
      var a = n0(e), aj = N ? a / (1 + (a - 1) / N) : a, fim = Math.ceil(aj); curN = aj;
      g(".read").innerHTML = "<code>n = Z² · p · q / e² = " + f(Z, 3) + "² · " + f(p, 2) + " · " + f(1 - p, 2) + " / " + f(e, 3) + "² = " + f(a, 2) + "</code>" + (N ? "<br>Com população finita de " + N.toLocaleString("pt-BR") + ": <code>n / (1 + (n − 1)/N) = " + f(aj, 2) + "</code>" : "") + "<br>Amostra mínima: <b style='font-size:1.3em;color:var(--pen)'>" + fim.toLocaleString("pt-BR") + " pessoas</b>. " + (p === 0.5 ? "Com p = 50% (cenário mais conservador) a conta dá o maior n possível." : "Quando p se afasta de 50%, o n necessário cai.") + " Repare na curva: <b>cortar a margem de erro pela metade multiplica a amostra por 4</b>.";
      api.paint();
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---- cap 3: tabela de frequência (ordinal) ---- */
  E.demos.freq = function (el) {
    var cats = ["Muito insatisfeito", "Insatisfeito", "Neutro", "Satisfeito", "Muito satisfeito"], cont = [2, 5, 9, 16, 8], orig = cont.slice();
    el.innerHTML = '<h4>Satisfação com o atendimento (escala Likert de 5 pontos)</h4><div class="ctrls"><button class="btn sm" type="button" id="fq-r">Restaurar as 40 respostas</button><span class="muted">Use + e − para mudar as respostas e veja a tabela reagir.</span></div><div class="tablewrap"><table class="ft"></table></div><canvas style="height:200px;cursor:default"></canvas><div class="read"></div>';
    var tb = el.querySelector(".ft"), cv = el.querySelector("canvas"), rd = el.querySelector(".read");
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var n = cont.reduce(function (a, b) { return a + b; }, 0) || 1, mx = Math.max.apply(null, cont) || 1, P = plotter(w, h, 0, 5, 0, mx * 1.15, { l: 36, r: 10, t: 14, b: 40 }), bw = (w - 46) / 5 * .66;
      ctx.save(); ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
      cats.forEach(function (k, i) { var x = P.X(i + .5), y = P.Y(cont[i]), y0 = P.Y(0); ctx.fillStyle = c.pen; ctx.globalAlpha = .85; ctx.fillRect(x - bw / 2, y, bw, y0 - y); ctx.globalAlpha = 1; ctx.fillStyle = c.ink; ctx.fillText(f(cont[i] / n * 100, 1) + "%", x, y - 4); ctx.fillStyle = c.muted; ctx.fillText(k.replace("Muito ", "M. "), x, h - 22); });
      ctx.restore();
    });
    function go() {
      var n = cont.reduce(function (a, b) { return a + b; }, 0), acc = 0, med = "n/d", mxc = Math.max.apply(null, cont), moda = n ? cats.filter(function (k, i) { return cont[i] === mxc; }).join(" e ") : "n/d";
      var rows = cats.map(function (k, i) { acc += cont[i]; if (med === "n/d" && n && acc >= n / 2) med = k; return '<tr><td>' + k + '</td><td><button class="btn sm" type="button" data-i="' + i + '" data-d="-1" aria-label="menos um em ' + k + '">−</button> <b>' + cont[i] + '</b> <button class="btn sm" type="button" data-i="' + i + '" data-d="1" aria-label="mais um em ' + k + '">+</button></td><td>' + f(n ? cont[i] / n * 100 : 0, 1) + '%</td><td>' + acc + '</td><td>' + f(n ? acc / n * 100 : 0, 1) + '%</td></tr>'; }).join("");
      tb.innerHTML = '<tr><th>resposta</th><th>fi (frequência absoluta)</th><th>fr (relativa)</th><th>Fi (acumulada)</th><th>Fr acumulada</th></tr>' + rows + '<tr class="dest"><td><b>Total</b></td><td><b>' + n + '</b></td><td>' + (n ? "100,0%" : "n/d") + '</td><td></td><td></td></tr>';
      var sat = cont[3] + cont[4];
      rd.innerHTML = "Moda: <b>" + moda + "</b>. Categoria da mediana (onde a frequência acumulada atinge ou passa de 50%): <b>" + med + "</b>. Satisfeitos + muito satisfeitos: <b>" + sat + " de " + n + " (" + f(n ? sat / n * 100 : 0, 1) + "%)</b>. Em variável <b>ordinal</b> a média numérica não faz sentido; use moda, mediana e a distribuição.";
      api.paint();
    }
    el.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-i]"); if (b) { var i = +b.dataset.i; cont[i] = Math.max(0, cont[i] + +b.dataset.d); go(); } });
    el.querySelector("#fq-r").addEventListener("click", function () { cont = orig.slice(); go(); });
    go();
  };

  /* ---- cap 3: histograma e número de classes ---- */
  var IDADES = [19, 21, 22, 22, 23, 23, 24, 24, 24, 25, 25, 26, 26, 26, 27, 27, 28, 28, 29, 30, 30, 31, 31, 32, 33, 34, 34, 35, 36, 38, 19, 20, 21, 23, 25, 27, 29, 41, 45, 52];
  E.demos.histograma = function (el) {
    el.innerHTML = '<h4>Idade de 40 respondentes: quantas classes usar?</h4><div class="ctrls"><label>número de classes <input type="range" id="hs-k" min="2" max="20" step="1" value="6"><output id="hs-ko"></output></label></div><canvas style="height:230px;cursor:default"></canvas><div class="tablewrap"><table class="ht"></table></div><div class="read"></div>';
    var cv = el.querySelector("canvas"), tb = el.querySelector(".ht"), rd = el.querySelector(".read"), mn = Math.min.apply(null, IDADES), mx = Math.max.apply(null, IDADES), amp = mx - mn, st;
    function calc(k) { var w = Math.floor(amp / k) + 1, c = []; for (var i = 0; i < k; i++) c.push(0); IDADES.forEach(function (x) { c[Math.floor((x - mn) / w)]++; }); return { w: w, c: c }; }
    st = calc(6);
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var k = st.c.length, top = Math.max.apply(null, st.c) + 2, P = plotter(w, h, 0, k, 0, top, { l: 36, r: 10, t: 12, b: 34 }), bw = (w - 46) / k;
      ctx.save(); ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
      st.c.forEach(function (n, i) { var x = P.X(i), y = P.Y(n); ctx.fillStyle = c.pen; ctx.globalAlpha = .85; ctx.fillRect(x + 1, y, bw - 2, P.Y(0) - y); ctx.globalAlpha = 1; if (k <= 12) { ctx.fillStyle = c.ink; ctx.fillText(n, x + bw / 2, y - 4); } if (k <= 10) { ctx.fillStyle = c.muted; ctx.fillText(mn + i * st.w, x + bw / 2, h - 20); } });
      ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.fillText("idade (início de cada classe)", w / 2, h - 4); ctx.restore();
    });
    function go() {
      var k = +el.querySelector("#hs-k").value; el.querySelector("#hs-ko").textContent = k; st = calc(k);
      var acc = 0; tb.innerHTML = '<tr><th>classe (idade)</th><th>fi</th><th>fr</th><th>Fi</th></tr>' + st.c.map(function (n, i) { acc += n; return '<tr class="' + (k === 6 && i === 1 ? "dest" : "") + '"><td>' + (mn + i * st.w) + ' a ' + (mn + (i + 1) * st.w - 1) + '</td><td>' + n + '</td><td>' + f(n / IDADES.length * 100, 1) + '%</td><td>' + acc + '</td></tr>'; }).join("");
      var sturges = 1 + 3.322 * Math.log10(IDADES.length);
      rd.innerHTML = "Regra de Sturges para n = 40: <code>k = 1 + 3,322·log₁₀(40) = " + f(sturges, 2) + "</code>, ou seja, cerca de <b>6 classes</b>. " + (k <= 3 ? "<b>Poucas classes</b> escondem a forma: tudo parece um bloco só." : k >= 14 ? "<b>Classes demais</b> viram ruído: barras de 0, 1 ou 2 pessoas, sem forma clara." : "Aqui já aparece a forma: muitos jovens, poucos acima de 40 (<b>assimetria à direita</b>).") + " Mesmos dados, desenhos diferentes: a escolha das classes é decisão de quem analisa.";
      api.paint();
    }
    el.addEventListener("input", go); go();
  };

  /* ---- cap 4: ler CSV: separador e decimal ---- */
  E.demos.csv = function (el) {
    var A = ["Nome;Idade;Salario", "Ana;42;5200", "Bruno;29;2500", "Clara;51;5000", "Diego;29;3000"], B = ["Nome;Idade;Salario", "Ana;42;5200,50", "Bruno;29;2500,00", "Clara;51;5000,75", "Diego;29;3000,00"];
    el.innerHTML = '<h4>O mesmo arquivo, lido de formas diferentes</h4><div class="ctrls"><label>arquivo <select id="cs-d"><option value="A">salários inteiros</option><option value="B">salários com centavos (vírgula)</option></select></label><label>sep <select id="cs-s"><option value=",">","</option><option value=";" selected>";"</option><option value=" ">" " (espaço)</option></select></label><label>decimal <select id="cs-c"><option value=".">"."</option><option value="," >","</option></select></label></div><div class="grid2"><div><b>DadosAula.csv (texto cru)</b><pre class="raw"></pre></div><div><b>O que o pandas entrega</b><div class="out"></div></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function num(s, dec) { var t = String(s).trim(); if (!t) return NaN; var re = dec === "," ? /^-?\d+(,\d+)?$/ : /^-?\d+(\.\d+)?$/; return re.test(t) ? +t.replace(",", ".") : NaN; }
    function go() {
      var L = g("#cs-d").value === "A" ? A : B, sep = g("#cs-s").value, dec = g("#cs-c").value;
      g(".raw").textContent = L.join("\n");
      var rows = L.map(function (l) { return l.split(sep); }), head = rows[0], erro = "";
      for (var i = 1; i < rows.length; i++) if (rows[i].length > head.length) { erro = "ParserError: Error tokenizing data. C error: Expected " + head.length + " fields in line " + (i + 1) + ", saw " + rows[i].length; break; }
      var code = 'df = pd.read_csv("DadosAula.csv", sep="' + sep + '"' + (dec === "," ? ', decimal=","' : "") + ")", out;
      if (erro) { out = "<pre class='raw'>" + esc(code) + "\n\n" + esc(erro) + "</pre>"; g(".read").innerHTML = "<b>Deu erro.</b> Com <code>sep=\",\"</code> o pandas acha que cada linha tem 1 coluna no cabeçalho, mas encontra mais campos nas linhas de dados (a vírgula decimal virou separador). Combine <code>sep=\";\"</code> com <code>decimal=\",\"</code>."; }
      else {
        var cols = head.map(function (nome, j) { var col = rows.slice(1).map(function (r) { return r[j]; }), vals = col.map(function (x) { return num(x, dec); }), ok = vals.every(function (v) { return !isNaN(v); }), tipo = !ok ? "object (texto)" : vals.every(function (v) { return Number.isInteger(v) && String(col[0]).indexOf(",") < 0 && !/[.,]/.test(col.join("")); }) ? "int64" : "float64"; return { nome: nome, tipo: tipo }; });
        out = "<pre class='raw'>" + esc(code) + "\ndf.shape → (" + (rows.length - 1) + ", " + head.length + ")\n\n" + cols.map(function (c) { return esc((c.nome.length > 22 ? c.nome.slice(0, 22) + "…" : c.nome)).padEnd(24) + c.tipo; }).join("\n") + "</pre>";
        var um = head.length === 1;
        g(".read").innerHTML = um ? "<b>Tudo numa coluna só</b>, chamada <code>'" + esc(head[0]) + "'</code>: o separador do arquivo é <code>;</code>, e não o que você pediu. Sinal clássico de <code>sep</code> errado." : (cols.some(function (c) { return c.tipo.indexOf("object") === 0 && c.nome === "Salario"; }) ? "<b>Salario virou texto</b> (<code>object</code>): o arquivo usa vírgula decimal e você pediu ponto. Não dá para calcular média de texto. Use <code>decimal=\",\"</code>." : "<b>Leitura correta</b>: 3 colunas, tipos numéricos onde deveriam ser. Confira sempre <code>df.shape</code> e <code>df.dtypes</code> logo depois de ler.");
      }
      g(".out").innerHTML = out;
    }
    el.addEventListener("change", go); go();
  };

  /* ---- cap 5: estatística descritiva ao vivo ---- */
  var SAL = [3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5];
  E.demos.descritiva = function (el) {
    el.innerHTML = '<h4>Salários de uma equipe (R$ mil): edite os valores</h4><div class="ctrls"><label style="flex:1;min-width:220px">valores (separe por espaço ou ponto e vírgula) <input type="text" id="ds-v" style="width:100%;font-family:var(--f-mono)"></label></div><div class="ctrls"><button class="btn sm" type="button" id="ds-o">+ Adicionar um valor extremo (40)</button><button class="btn sm" type="button" id="ds-r">Restaurar</button></div><div class="sg"></div><canvas style="height:150px;cursor:default"></canvas><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, inp = g("#ds-v"), cv = el.querySelector("canvas"), S = null;
    function parse() { return inp.value.replace(/,/g, ".").split(/[\s;]+/).map(parseFloat).filter(function (x) { return isFinite(x); }).slice(0, 60); }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      if (!S || S.n < 2) return;
      var pad = (S.max - S.min) * .08 || 1, a = S.min - pad, b = S.max + pad, P = plotter(w, h, a, b, 0, 1, { l: 16, r: 16, t: 10, b: 30 }), yb = 52;
      axes(ctx, w, h, P, a, b, 0, 0, nice((b - a) / 5), 0, "valor", "", c);
      ctx.save(); ctx.lineWidth = 2; ctx.strokeStyle = c.ink; ctx.fillStyle = c.pen; ctx.globalAlpha = .35;
      ctx.fillRect(P.X(S.q1), yb - 20, P.X(S.q3) - P.X(S.q1), 40); ctx.globalAlpha = 1; ctx.strokeRect(P.X(S.q1), yb - 20, P.X(S.q3) - P.X(S.q1), 40);
      ctx.beginPath(); ctx.moveTo(P.X(S.mediana), yb - 20); ctx.lineTo(P.X(S.mediana), yb + 20); ctx.lineWidth = 4; ctx.stroke(); ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(P.X(S.wlo), yb); ctx.lineTo(P.X(S.q1), yb); ctx.moveTo(P.X(S.q3), yb); ctx.lineTo(P.X(S.whi), yb); ctx.moveTo(P.X(S.wlo), yb - 8); ctx.lineTo(P.X(S.wlo), yb + 8); ctx.moveTo(P.X(S.whi), yb - 8); ctx.lineTo(P.X(S.whi), yb + 8); ctx.stroke();
      S.fora.forEach(function (x) { ctx.beginPath(); ctx.arc(P.X(x), yb, 6, 0, 6.2832); ctx.fillStyle = c.red; ctx.fill(); ctx.stroke(); });
      var mx = P.X(S.media); ctx.beginPath(); ctx.moveTo(mx, yb - 14); ctx.lineTo(mx + 9, yb); ctx.lineTo(mx, yb + 14); ctx.lineTo(mx - 9, yb); ctx.closePath(); ctx.fillStyle = c.c1; ctx.fill(); ctx.stroke();
      ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "left"; ctx.fillText("caixa = Q1 a Q3 · traço = mediana · losango = média · vermelho = outliers", 8, 16); ctx.restore();
    });
    function go() {
      var v = parse(); if (v.length < 2) { g(".sg").innerHTML = '<p class="muted">Digite pelo menos 2 números.</p>'; S = null; api.paint(); return; }
      S = resumo(v);
      var it = [["n", S.n], ["média", f(S.media)], ["mediana", f(S.mediana)], ["moda", S.moda.length ? S.moda.map(function (x) { return f(x, 1); }).join(", ") : "sem moda"], ["mínimo", f(S.min)], ["máximo", f(S.max)], ["amplitude", f(S.max - S.min)], ["Q1", f(S.q1, 3)], ["Q3", f(S.q3, 3)], ["IQR", f(S.iqr, 3)], ["variância (n−1)", f(S.var1, 3)], ["desvio padrão", f(S.sd, 3)], ["coef. de variação", f(S.cv, 1) + "%"], ["outliers", S.fora.length ? S.fora.map(function (x) { return f(x, 1); }).join(", ") : "nenhum"]];
      g(".sg").innerHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin:10px 0">' + it.map(function (p) { return '<div class="card" style="margin:0;padding:8px 10px"><small class="muted">' + p[0] + '</small><div style="font:700 1.1rem var(--f-mono)">' + p[1] + '</div></div>'; }).join("") + '</div>';
      var dif = S.media - S.mediana;
      g(".read").innerHTML = (S.fora.length || Math.abs(dif) > S.iqr * .5 ? "<b>Média (" + f(S.media) + ") e mediana (" + f(S.mediana) + ") se separaram.</b> Isso é sinal de assimetria ou de valor extremo: a média é puxada por ele, a mediana não. " : "Média e mediana próximas: distribuição razoavelmente simétrica. ") + "Regra do boxplot: é outlier o que passa de <code>Q3 + 1,5·IQR = " + f(S.hi, 3) + "</code> ou fica abaixo de <code>Q1 − 1,5·IQR = " + f(S.lo, 3) + "</code>. Quartis calculados por interpolação linear (o padrão de <code>numpy</code>, <code>pandas</code> e do R); o Excel (QUARTIL.EXC) e livros podem dar valores um pouco diferentes.";
      api.paint();
    }
    function set(a) { inp.value = a.join(" ").replace(/\./g, ","); go(); }
    inp.addEventListener("input", go);
    g("#ds-o").addEventListener("click", function () { var v = parse(); v.push(40); set(v); });
    g("#ds-r").addEventListener("click", function () { set(SAL); });
    set(SAL);
  };

  /* ---- cap 6: correlação, regressão e o quarteto de Anscombe ---- */
  var ANS = { I: [[10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]], II: [[10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]], III: [[10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]], IV: [[8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]] };
  E.demos.correlacao = function (el) {
    el.innerHTML = '<h4>Mesma correlação, histórias diferentes</h4><div class="ctrls"><label>dados <select id="cr-d"><option value="G">gerados: reta + ruído</option><option value="I">Anscombe I</option><option value="II">Anscombe II</option><option value="III">Anscombe III</option><option value="IV">Anscombe IV</option></select></label><label id="cr-nl">ruído <input type="range" id="cr-n" min="0" max="6" step="0.25" value="2"><output id="cr-no"></output></label></div><canvas style="height:280px;cursor:default"></canvas><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, cv = el.querySelector("canvas"), D = null, R = null;
    function reg(x, y) { var n = x.length, mx = 0, my = 0; for (var i = 0; i < n; i++) { mx += x[i]; my += y[i]; } mx /= n; my /= n; var sxy = 0, sxx = 0, syy = 0; for (var j = 0; j < n; j++) { sxy += (x[j] - mx) * (y[j] - my); sxx += (x[j] - mx) * (x[j] - mx); syy += (y[j] - my) * (y[j] - my); } var b = sxy / sxx, a = my - b * mx, r = sxy / Math.sqrt(sxx * syy); return { a: a, b: b, r: r, r2: r * r, mx: mx, my: my }; }
    function data() { var k = g("#cr-d").value; if (k !== "G") return ANS[k]; var r = rng(11), s = +g("#cr-n").value, x = [], y = []; for (var i = 0; i < 30; i++) { var xi = 1 + r() * 9; x.push(xi); y.push(2 + 1.5 * xi + s * gauss(r)); } return [x, y]; }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      if (!D) return; var x = D[0], y = D[1], x0 = 0, x1 = 20, y0 = Math.min(0, Math.floor(Math.min.apply(null, y))), y1 = Math.max(14, Math.ceil(Math.max.apply(null, y) + 1)), P = plotter(w, h, x0, x1, y0, y1, { l: 40, r: 12, t: 12, b: 32 });
      if (g("#cr-d").value === "G") { x1 = 10; y1 = Math.max(18, Math.ceil(Math.max.apply(null, y) + 1)); P = plotter(w, h, 0, 10, y0, y1, { l: 40, r: 12, t: 12, b: 32 }); }
      axes(ctx, w, h, P, x0, x1, y0, y1, g("#cr-d").value === "G" ? 2 : 4, 4, "x", "y", c);
      ctx.beginPath(); ctx.moveTo(P.X(x0), P.Y(R.a + R.b * x0)); ctx.lineTo(P.X(x1), P.Y(R.a + R.b * x1)); ctx.lineWidth = 3; ctx.strokeStyle = c.red; ctx.stroke();
      x.forEach(function (xi, i) { ctx.beginPath(); ctx.arc(P.X(xi), P.Y(y[i]), 6, 0, 6.2832); ctx.fillStyle = c.pen; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = c.ink; ctx.stroke(); });
    });
    function go() {
      var k = g("#cr-d").value; g("#cr-nl").style.display = k === "G" ? "" : "none"; g("#cr-no").textContent = f(+g("#cr-n").value, 2);
      D = data(); R = reg(D[0], D[1]);
      var txt = "<code>r = " + f(R.r, 3) + "</code> · reta <code>ŷ = " + f(R.a, 2) + " + " + f(R.b, 3) + "·x</code> · <code>R² = " + f(R.r2, 3) + "</code> · média de y = " + f(R.my, 2) + ". ";
      if (k === "G") txt += R.r2 > .95 ? "Quase todos os pontos sobre a reta: o x explica quase toda a variação de y." : "Com mais ruído, o <b>r</b> cai e o <b>R²</b> (a fatia da variação de y explicada pela reta) também. A reta continua sendo desenhada, mas explica menos.";
      else txt += { I: "<b>I</b>: o caso 'bem comportado', nuvem linear com ruído. A reta faz sentido.", II: "<b>II</b>: é uma <b>curva</b>. O mesmo r, mas uma reta é o modelo errado.", III: "<b>III</b>: uma reta quase perfeita estragada por <b>um outlier</b> que puxa a inclinação.", IV: "<b>IV</b>: todos com o mesmo x, menos <b>um ponto</b> isolado. O r inteiro depende dele." }[k] + " Os quatro conjuntos têm praticamente os mesmos números (r ≈ 0,816, mesma reta, média de y = 7,5) e desenhos completamente diferentes: <b>sempre olhe o gráfico</b>.";
      g(".read").innerHTML = txt; api.paint();
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };
})();
