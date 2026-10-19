/* Demos da apostila de Redes Neurais, Deep Learning e Algoritmos Genéticos */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function gauss(r) { var u = 1 - r(), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  var ACT = { degrau: function (z) { return z >= 0 ? 1 : 0; }, relu: function (z) { return Math.max(0, z); }, sigmoide: function (z) { return 1 / (1 + Math.exp(-z)); }, tanh: function (z) { return Math.tanh(z); }, linear: function (z) { return z; } };

  /* helpers de gráfico simples */
  function plotter(w, h, x0, x1, y0, y1, pad) { pad = pad || { l: 46, r: 12, t: 12, b: 32 }; return { pad: pad, X: function (x) { return pad.l + (x - x0) / (x1 - x0) * (w - pad.l - pad.r); }, Y: function (y) { return pad.t + (1 - (y - y0) / (y1 - y0)) * (h - pad.t - pad.b); }, ix: function (px) { return x0 + (px - pad.l) / (w - pad.l - pad.r) * (x1 - x0); } }; }
  function axes(ctx, w, h, P, x0, x1, y0, y1, xs, ys, xl, yl, c) {
    ctx.save(); ctx.lineWidth = 1; ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
    for (var x = Math.ceil(x0 / xs) * xs; x <= x1 + 1e-9; x += xs) { ctx.beginPath(); ctx.moveTo(P.X(x), P.pad.t); ctx.lineTo(P.X(x), h - P.pad.b); ctx.stroke(); ctx.fillText(+x.toFixed(2), P.X(x), h - P.pad.b + 14); }
    ctx.textAlign = "right"; for (var y = Math.ceil(y0 / ys) * ys; y <= y1 + 1e-9; y += ys) { ctx.beginPath(); ctx.moveTo(P.pad.l, P.Y(y)); ctx.lineTo(w - P.pad.r, P.Y(y)); ctx.stroke(); ctx.fillText(+y.toFixed(2), P.pad.l - 6, P.Y(y) + 4); }
    ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.textAlign = "center"; ctx.fillText(xl, (P.pad.l + w - P.pad.r) / 2, h - 4); ctx.save(); ctx.translate(12, (P.pad.t + h - P.pad.b) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText(yl, 0, 0); ctx.restore(); ctx.restore();
  }

  /* ---- cap 1: um neurônio ---- */
  E.demos.neuronio = function (el) {
    el.innerHTML = '<h4>Um neurônio artificial: soma ponderada e ativação</h4><div class="grid2"><div>' +
      '<div class="ctrls"><label>x1 <input type="range" id="x1" min="-2" max="2" step="0.1" value="1"><output id="x1o"></output></label><label>peso w1 <input type="range" id="w1" min="-3" max="3" step="0.1" value="1.5"><output id="w1o"></output></label></div>' +
      '<div class="ctrls"><label>x2 <input type="range" id="x2" min="-2" max="2" step="0.1" value="-0.5"><output id="x2o"></output></label><label>peso w2 <input type="range" id="w2" min="-3" max="3" step="0.1" value="-1"><output id="w2o"></output></label></div>' +
      '<div class="ctrls"><label>bias b <input type="range" id="bb" min="-3" max="3" step="0.1" value="0.5"><output id="bbo"></output></label><label>ativação <select id="ac"><option value="degrau">degrau</option><option value="relu">ReLU</option><option value="sigmoide">sigmoide</option><option value="tanh">tanh</option><option value="linear">linear</option></select></label></div></div>' +
      '<div class="card" style="margin:0"><div class="nm"></div></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, nm = g(".nm"), rd = g(".read");
    function go() {
      var x1 = +g("#x1").value, x2 = +g("#x2").value, w1 = +g("#w1").value, w2 = +g("#w2").value, b = +g("#bb").value, a = g("#ac").value;
      ["x1", "w1", "x2", "w2", "bb"].forEach(function (k) { g("#" + k + "o").textContent = (+g("#" + k).value).toFixed(1); });
      var z = Math.round((x1 * w1 + x2 * w2 + b) * 1e6) / 1e6, y = ACT[a](z);
      nm.innerHTML = '<div style="font:.9rem var(--f-mono);line-height:1.9">z = x1·w1 + x2·w2 + b<br>z = ' + x1.toFixed(1) + '·' + w1.toFixed(1) + ' + ' + x2.toFixed(1) + '·' + w2.toFixed(1) + ' + ' + b.toFixed(1) + '<br><b>z = ' + z.toFixed(2) + '</b><br>saída = ' + a + '(z) = <b style="color:var(--pen);font-size:1.2rem">' + y.toFixed(3) + '</b></div>';
      rd.innerHTML = "O neurônio <b>multiplica cada entrada pelo seu peso, soma tudo (mais o bias)</b> e passa o resultado pela <b>função de ativação</b>. " + (a === "degrau" ? "O degrau só diz sim (1) ou não (0): é o neurônio do Perceptron." : a === "relu" ? "A ReLU zera o que é negativo e deixa o positivo passar." : a === "sigmoide" ? "A sigmoide comprime qualquer valor para o intervalo entre 0 e 1: serve como probabilidade." : a === "tanh" ? "A tanh comprime para o intervalo entre -1 e 1." : "A linear devolve z: sem ativação, a rede inteira vira uma conta linear.");
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  E.demos.ativacoes = function (el) {
    el.innerHTML = '<h4>Formato de cada função de ativação</h4><canvas style="height:260px;cursor:default"></canvas><div class="legend"></div><div class="read">Sem uma ativação <b>não linear</b> entre as camadas, empilhar camadas não adianta: a rede inteira se comporta como uma única conta linear. É a não linearidade que permite aprender curvas.</div>';
    var cv = el.querySelector("canvas"), lg = el.querySelector(".legend"), nomes = ["degrau", "relu", "sigmoide", "tanh"], cores = ["c0", "c1", "c2", "green"];
    lg.innerHTML = nomes.map(function (n, i) { return '<span><i style="background:var(--' + cores[i] + ')"></i>' + n + '</span>'; }).join("");
    E.canvas(cv, function (ctx, w, h, c) {
      var P = plotter(w, h, -4, 4, -1.5, 3, null); axes(ctx, w, h, P, -4, 4, -1, 3, 1, 1, "z (a soma ponderada)", "saída", c);
      nomes.forEach(function (n, k) { ctx.beginPath(); for (var i = 0; i <= 160; i++) { var x = -4 + i * 8 / 160, y = ACT[n](x); var X = P.X(x), Y = P.Y(y); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); } ctx.lineWidth = 3; ctx.strokeStyle = c[cores[k]] || c.green; ctx.stroke(); });
    });
  };

  /* ---- cap 2: gradiente descendente e taxa de aprendizado ---- */
  E.demos.gradiente = function (el) {
    el.innerHTML = '<h4>Descendo até o menor erro (L = (w − 3)² + 1)</h4><canvas style="height:260px;cursor:default"></canvas><div class="ctrls"><label>taxa de aprendizado <input type="range" id="gl" min="0.02" max="1.1" step="0.01" value="0.2"><output id="glo"></output></label><button class="btn sm pri" type="button" id="gr">▶ Treinar 15 passos</button><button class="btn sm" type="button" id="gz">Reiniciar</button></div><div class="read"></div>';
    var cv = el.querySelector("canvas"), gl = el.querySelector("#gl"), rd = el.querySelector(".read"), hist = [0.5], timer = 0;
    var L = function (w) { return (w - 3) * (w - 3) + 1; }, dL = function (w) { return 2 * (w - 3); };
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = plotter(w, h, -2, 8, 0, 40, null); axes(ctx, w, h, P, -2, 8, 0, 40, 2, 10, "peso w", "erro L", c);
      ctx.beginPath(); for (var i = 0; i <= 120; i++) { var x = -2 + i * 10 / 120, X = P.X(x), Y = P.Y(Math.min(40, L(x))); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); } ctx.lineWidth = 3; ctx.strokeStyle = c.ink; ctx.stroke();
      hist.forEach(function (v, i) { if (v < -2 || v > 8) return; var X = P.X(v), Y = P.Y(Math.min(40, L(v))); ctx.beginPath(); ctx.arc(X, Y, i === hist.length - 1 ? 7 : 4, 0, 6.2832); ctx.fillStyle = i === hist.length - 1 ? c.red : c.pen; ctx.globalAlpha = i === hist.length - 1 ? 1 : .5; ctx.fill(); ctx.globalAlpha = 1; });
    });
    function rep() {
      var lr = +gl.value, w = hist[hist.length - 1]; el.querySelector("#glo").textContent = lr.toFixed(2);
      rd.innerHTML = "Passo " + (hist.length - 1) + ": w = <b>" + (isFinite(w) ? w.toFixed(3) : "∞") + "</b>, erro = <b>" + (isFinite(L(w)) ? L(w).toFixed(3) : "explodiu") + "</b>. Regra: <code>w ← w − taxa × inclinação</code> (a inclinação é <code>2(w − 3)</code>). " + (lr > 1 ? "<b style='color:var(--red)'>Taxa alta demais: a cada passo o ponto pula para o outro lado e se afasta.</b>" : (lr < 0.06 ? "Taxa muito baixa: converge, mas devagar." : "Taxa moderada: desce e estabiliza perto de w = 3, o mínimo."));
    }
    function passo() { var w = hist[hist.length - 1]; hist.push(w - +gl.value * dL(w)); api.paint(); rep(); }
    el.querySelector("#gr").addEventListener("click", function () { clearInterval(timer); var n = 0; timer = setInterval(function () { if (n++ >= 15) { clearInterval(timer); return; } passo(); }, E.reduce ? 5 : 350); });
    el.querySelector("#gz").addEventListener("click", function () { clearInterval(timer); hist = [0.5]; api.paint(); rep(); });
    gl.addEventListener("input", rep); rep();
  };

  /* ---- cap 2: overfitting com polinômios ---- */
  E.demos.overfit = function (el) {
    var r = rng(5), pts = []; for (var i = 0; i < 24; i++) { var x = i / 23 * 6; pts.push({ x: x, y: Math.sin(x) + gauss(r) * 0.28, test: i % 3 === 1 }); }
    el.innerHTML = '<h4>Complexidade do modelo: do simples demais ao decorador</h4><canvas style="height:290px;cursor:default"></canvas><div class="ctrls"><label>grau do polinômio (complexidade) <input type="range" id="og" min="1" max="12" value="1"><output id="ogo">1</output></label></div><div class="legend"><span><i style="background:var(--c0)"></i>treino (16 pontos)</span><span><i style="background:var(--c1)"></i>teste (8 pontos, nunca vistos no ajuste)</span><span><i style="background:var(--red)"></i>modelo</span></div><div class="read"></div>';
    var cv = el.querySelector("canvas"), og = el.querySelector("#og"), rd = el.querySelector(".read");
    function fit(deg) { var tr = pts.filter(function (p) { return !p.test; }), n = deg + 1, A = [], b = []; for (var i = 0; i < n; i++) { A.push(new Array(n).fill(0)); b.push(0); } tr.forEach(function (p) { var pw = []; for (var i = 0; i < n; i++) pw.push(Math.pow(p.x / 6, i)); for (var i2 = 0; i2 < n; i2++) { b[i2] += pw[i2] * p.y; for (var j = 0; j < n; j++) A[i2][j] += pw[i2] * pw[j]; } }); for (var d = 0; d < n; d++) A[d][d] += 1e-9;
      for (var i3 = 0; i3 < n; i3++) { var m = i3; for (var j2 = i3 + 1; j2 < n; j2++) if (Math.abs(A[j2][i3]) > Math.abs(A[m][i3])) m = j2; var t = A[i3]; A[i3] = A[m]; A[m] = t; var tb = b[i3]; b[i3] = b[m]; b[m] = tb; for (var j3 = i3 + 1; j3 < n; j3++) { var f = A[j3][i3] / A[i3][i3]; for (var k = i3; k < n; k++) A[j3][k] -= f * A[i3][k]; b[j3] -= f * b[i3]; } }
      var co = new Array(n).fill(0); for (var i4 = n - 1; i4 >= 0; i4--) { var s = b[i4]; for (var j4 = i4 + 1; j4 < n; j4++) s -= A[i4][j4] * co[j4]; co[i4] = s / A[i4][i4]; } return function (x) { var y = 0; for (var i5 = 0; i5 < n; i5++) y += co[i5] * Math.pow(x / 6, i5); return y; }; }
    function rmse(f, test) { var s = pts.filter(function (p) { return p.test === test; }); return Math.sqrt(s.reduce(function (a, p) { var e = f(p.x) - p.y; return a + e * e; }, 0) / s.length); }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = plotter(w, h, 0, 6, -2, 2, null); axes(ctx, w, h, P, 0, 6, -2, 2, 1, 1, "x", "y", c); var f = fit(+og.value);
      ctx.beginPath(); for (var i = 0; i <= 200; i++) { var x = i / 200 * 6, y = Math.max(-2.3, Math.min(2.3, f(x))); var X = P.X(x), Y = P.Y(y); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); } ctx.lineWidth = 3; ctx.strokeStyle = c.red; ctx.stroke();
      pts.forEach(function (p) { ctx.beginPath(); ctx.arc(P.X(p.x), P.Y(p.y), 5, 0, 6.2832); ctx.fillStyle = p.test ? c.c1 : c.c0; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = c.paper; ctx.stroke(); });
    });
    function rep() { var d = +og.value, f = fit(d); el.querySelector("#ogo").textContent = d; var a = rmse(f, false), b = rmse(f, true);
      rd.innerHTML = "Grau <b>" + d + "</b>: erro no <b style='color:var(--c0)'>treino</b> = <b>" + a.toFixed(2) + "</b> · erro no <b style='color:var(--c1)'>teste</b> = <b>" + b.toFixed(2) + "</b>. " + (d <= 2 ? "<b>Underfitting</b>: simples demais, erra até no treino." : (b > a * 1.5 ? "<b>Overfitting</b>: o erro de treino caiu, mas o erro de <b>teste</b> ficou bem maior que o de treino. A curva se ajusta ao ruído dos pontos de treino." : "Complexidade razoável: treino e teste próximos.")); }
    og.addEventListener("input", function () { api.paint(); rep(); }); rep();
  };

  /* ---- cap 3: perceptron ---- */
  var GATES = { AND: [0, 0, 0, 1], OR: [0, 1, 1, 1], XOR: [0, 1, 1, 0] }, IN = [[0, 0], [0, 1], [1, 0], [1, 1]];
  E.demos.perceptron = function (el) {
    var st; function init() { st = { w: [0, 0], b: 0, ep: 0, log: [] }; }
    init();
    el.innerHTML = '<h4>Treine um Perceptron (taxa 0,1, ativação degrau com ≥ 0)</h4><div class="ctrls"><label>porta lógica <select id="pg"><option>AND</option><option>OR</option><option>XOR</option></select></label><button class="btn sm pri" type="button" data-a="1">Treinar 1 época</button><button class="btn sm" type="button" data-a="20">Treinar até 20 épocas</button><button class="btn sm" type="button" data-a="0">Reiniciar</button></div>' +
      '<div class="grid2"><canvas style="height:240px;cursor:default"></canvas><div class="tablewrap"><table class="pt"></table></div></div><div class="read"></div>';
    var cv = el.querySelector("canvas"), sel = el.querySelector("#pg"), pt = el.querySelector(".pt"), rd = el.querySelector(".read");
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = plotter(w, h, -0.4, 1.4, -0.4, 1.4, { l: 34, r: 10, t: 10, b: 28 }); axes(ctx, w, h, P, -0.4, 1.4, -0.4, 1.4, 1, 1, "x1", "x2", c);
      var y = GATES[sel.value];
      // região positiva
      if (st.w[1] !== 0 || st.w[0] !== 0) { ctx.save(); ctx.beginPath(); ctx.rect(P.pad.l, P.pad.t, w - P.pad.l - P.pad.r, h - P.pad.t - P.pad.b); ctx.clip(); ctx.beginPath(); var pts = []; for (var i = 0; i <= 1; i += 1) { var x1 = -0.4 + i * 1.8; if (st.w[1] !== 0) pts.push([x1, -(st.w[0] * x1 + st.b) / st.w[1]]); } if (pts.length === 2) { ctx.moveTo(P.X(pts[0][0]), P.Y(pts[0][1])); ctx.lineTo(P.X(pts[1][0]), P.Y(pts[1][1])); } else { var xv = -st.b / st.w[0]; ctx.moveTo(P.X(xv), P.pad.t); ctx.lineTo(P.X(xv), h - P.pad.b); } ctx.lineWidth = 3; ctx.strokeStyle = c.ink; ctx.stroke(); ctx.restore(); }
      IN.forEach(function (p, i) { ctx.beginPath(); ctx.arc(P.X(p[0]), P.Y(p[1]), 10, 0, 6.2832); ctx.fillStyle = y[i] ? c.c1 : c.c0; ctx.fill(); ctx.font = "700 12px Inter,sans-serif"; ctx.textAlign = "center"; ctx.lineWidth = 3; ctx.strokeStyle = "#10131c"; ctx.strokeText(y[i], P.X(p[0]), P.Y(p[1]) + 4); ctx.fillStyle = "#fff"; ctx.fillText(y[i], P.X(p[0]), P.Y(p[1]) + 4); });
    });
    function epoca() {
      var y = GATES[sel.value], erros = 0;
      IN.forEach(function (p, i) { var z = st.w[0] * p[0] + st.w[1] * p[1] + st.b, yh = z >= 0 ? 1 : 0, e = y[i] - yh; if (e !== 0) { erros++; st.w = [Math.round((st.w[0] + 0.1 * e * p[0]) * 100) / 100, Math.round((st.w[1] + 0.1 * e * p[1]) * 100) / 100]; st.b = Math.round((st.b + 0.1 * e) * 100) / 100; } });
      st.ep++; st.log.push({ ep: st.ep, w: st.w.slice(), b: st.b, e: erros }); return erros;
    }
    function draw() {
      pt.innerHTML = !st.log.length ? '<tr><td class="muted">Ainda sem treino.</td></tr>' : '<tr><th>época</th><th>w1</th><th>w2</th><th>bias</th><th>erros</th></tr>' + st.log.slice(-8).map(function (l) { return '<tr class="' + (l.e === 0 ? "dest" : "") + '"><td>' + l.ep + '</td><td>' + l.w[0] + '</td><td>' + l.w[1] + '</td><td>' + l.b + '</td><td>' + l.e + '</td></tr>'; }).join("");
      var last = st.log[st.log.length - 1];
      rd.innerHTML = !last ? "Pesos e bias começam em zero. Cada época passa pelos 4 exemplos e ajusta os pesos só quando erra: <code>w ← w + taxa · erro · x</code> e <code>b ← b + taxa · erro</code>." : (last.e === 0 ? "<b style='color:var(--green)'>Convergiu na época " + last.ep + ": zero erros.</b> A reta separa as classes." : (sel.value === "XOR" && st.ep >= 6 ? "<b style='color:var(--red)'>O XOR não converge.</b> Não existe uma reta que separe {(0,0),(1,1)} de {(0,1),(1,0)}: foi o limite que parou a área nos anos 1970 (Minsky e Papert, 1969)." : "Época " + last.ep + ": " + last.e + " erro(s). Continue treinando."));
      api.paint();
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-a]"); if (!b) return; var n = +b.getAttribute("data-a"); if (n === 0) init(); else for (var k = 0; k < n; k++) { if (epoca() === 0) break; } draw(); });
    sel.addEventListener("change", function () { init(); draw(); }); draw();
  };

  /* ---- cap 4: o bias numa decisão de negócio (AND) ---- */
  E.demos.bias = function (el) {
    el.innerHTML = '<h4>Liberar a oferta só se pagou em dia E tem alto engajamento</h4><div class="ctrls"><label>peso w1 <input type="range" id="b1" min="-1" max="2" step="0.1" value="1"><output id="b1o"></output></label><label>peso w2 <input type="range" id="b2" min="-1" max="2" step="0.1" value="1"><output id="b2o"></output></label><label>bias <input type="range" id="bb" min="-3" max="1" step="0.1" value="0"><output id="bbo"></output></label></div><div class="tablewrap"><table class="bt"></table></div><div class="read"></div>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" id="bt">Deixar o modelo aprender o bias (6 épocas)</button></div><div class="tablewrap"><table class="bl"></table></div>';
    var g = function (id) { return el.querySelector(id); };
    function go() {
      var w1 = +g("#b1").value, w2 = +g("#b2").value, b = +g("#bb").value; g("#b1o").textContent = w1.toFixed(1); g("#b2o").textContent = w2.toFixed(1); g("#bbo").textContent = b.toFixed(1);
      var Y = GATES.AND, ok = 0, rows = IN.map(function (p, i) { var z = Math.round((p[0] * w1 + p[1] * w2 + b) * 1e6) / 1e6, yh = z >= 0 ? 1 : 0, c = yh === Y[i]; if (c) ok++; return '<tr><td>[' + p + ']</td><td>' + z.toFixed(1) + '</td><td>' + yh + '</td><td>' + Y[i] + '</td><td>' + (c ? "✅" : "❌") + '</td></tr>'; }).join("");
      g(".bt").innerHTML = '<tr><th>entrada [pagou, engajado]</th><th>soma</th><th>previsto</th><th>esperado</th><th></th></tr>' + rows;
      g(".read").innerHTML = "Acertos: <b>" + ok + " de 4</b>. " + (b === 0 && w1 === 1 && w2 === 1 ? "Sem bias, o caso [0, 0] dá soma 0, e como o degrau é <code>≥ 0</code>, sai 1: <b>a fronteira é obrigada a passar pela origem</b>. Tente bias <b>−1,5</b>: só as duas condições juntas (soma 2) passam do corte." : (ok === 4 ? "<b style='color:var(--green)'>Acertou tudo.</b> O bias é a <i>nota de corte</i>: exige evidência suficiente antes de responder 1." : "Mexa no bias e nos pesos. Procure uma combinação que acerte as 4."));
    }
    el.querySelector("#bt").addEventListener("click", function () {
      var w = [0, 0], b = 0, Y = GATES.AND, rows = "";
      for (var ep = 1; ep <= 6; ep++) { var er = 0; IN.forEach(function (p, i) { var z = w[0] * p[0] + w[1] * p[1] + b, yh = z >= 0 ? 1 : 0, e = Y[i] - yh; if (e) { er++; w = [Math.round((w[0] + 0.1 * e * p[0]) * 100) / 100, Math.round((w[1] + 0.1 * e * p[1]) * 100) / 100]; b = Math.round((b + 0.1 * e) * 100) / 100; } }); rows += '<tr class="' + (er === 0 ? "dest" : "") + '"><td>' + ep + '</td><td>[' + w + ']</td><td>' + b + '</td><td>' + er + '</td></tr>'; }
      g(".bl").innerHTML = '<tr><th>época</th><th>pesos ao fim</th><th>bias ao fim</th><th>erros</th></tr>' + rows;
    });
    el.addEventListener("input", go); go();
  };

  /* ---- cap 5: MLP do consumo de energia (resultados reais do scikit-learn) ---- */
  E.demos.mlpenergia = function (el) {
    var D = window.RNDATA;
    el.innerHTML = '<h4>Consumo de energia x temperatura (365 dias gerados por computador)</h4><canvas style="height:300px;cursor:default"></canvas><div class="ctrls"><label><input type="checkbox" id="mr" checked> reta (regressão linear)</label><label><input type="checkbox" id="mm" checked> MLP (8 neurônios ReLU)</label></div><div class="legend"><span><i style="background:var(--muted)"></i>dias</span><span><i style="background:var(--c1)"></i>reta</span><span><i style="background:var(--green)"></i>MLP</span></div>' +
      '<div class="tablewrap"><table><tr><th>modelo</th><th class="n">RMSE no teste (kWh)</th></tr><tr><td>chutar sempre a média</td><td class="n">' + D.rmse.media.toFixed(2).replace(".", ",") + '</td></tr><tr><td>reta</td><td class="n">' + D.rmse.reta.toFixed(2).replace(".", ",") + '</td></tr><tr class="dest"><td>MLP (8 neurônios, ReLU, taxa 0,01)</td><td class="n">' + D.rmse.mlp.toFixed(2).replace(".", ",") + '</td></tr></table></div><div class="read">Uma reta quase não melhora o chute da média, porque o consumo faz um <b>U</b> (gasta mais no frio e no calor, menos no meio). A MLP desenha o U: cada neurônio ReLU contribui com uma "dobra".</div>';
    var cv = el.querySelector("canvas"), mr = el.querySelector("#mr"), mm = el.querySelector("#mm");
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = plotter(w, h, 8, 38, 12, 42, null); axes(ctx, w, h, P, 8, 38, 12, 42, 5, 5, "temperatura (°C)", "consumo (kWh)", c);
      ctx.globalAlpha = .45; D.pts.forEach(function (p) { ctx.beginPath(); ctx.arc(P.X(p[0]), P.Y(p[1]), 2.8, 0, 6.2832); ctx.fillStyle = c.muted; ctx.fill(); }); ctx.globalAlpha = 1;
      function line(a, col) { ctx.beginPath(); D.grid.forEach(function (x, i) { var X = P.X(x), Y = P.Y(a[i]); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }); ctx.lineWidth = 3.5; ctx.strokeStyle = col; ctx.stroke(); }
      if (mr.checked) line(D.reta, c.c1); if (mm.checked) line(D.mlp, c.green);
    });
    mr.addEventListener("change", api.paint); mm.addEventListener("change", api.paint);
  };

  E.demos.experimentos = function (el) {
    var D = window.RNDATA.exp, f = function (v) { return v.toFixed(2).replace(".", ","); };
    el.innerHTML = '<h4>Os experimentos A, B e C do notebook (valores reais)</h4><div class="grid3"><div><b>A: neurônios ocultos</b><div class="tablewrap"><table>' + Object.keys(D.A).map(function (k) { return '<tr class="' + (D.A[k] > 5 ? "" : "dest") + '"><td><code>(' + k + ',)</code></td><td class="n">' + f(D.A[k]) + '</td></tr>'; }).join("") + '</table></div></div>' +
      '<div><b>B: ativação</b><div class="tablewrap"><table>' + Object.keys(D.B).map(function (k) { return '<tr class="' + (D.B[k] > 5 ? "" : "dest") + '"><td><code>' + k + '</code></td><td class="n">' + f(D.B[k]) + '</td></tr>'; }).join("") + '</table></div></div>' +
      '<div><b>C: taxa de aprendizagem</b><div class="tablewrap"><table><tr><th>taxa</th><th class="n">RMSE</th><th class="n">épocas</th></tr>' + Object.keys(D.C).map(function (k) { return '<tr><td><code>' + k.replace(".", ",") + '</code></td><td class="n">' + f(D.C[k].rmse) + '</td><td class="n">' + D.C[k].epocas + '</td></tr>'; }).join("") + '</table></div></div></div>' +
      '<div class="read"><b>A:</b> com 1 ou 2 neurônios a rede não passa da reta (5,9); com 3 já desenha o U. Um U precisa de uma curva que desce e outra que sobe. <b>B:</b> com <code>identity</code> (sem ativação) a rede inteira é uma reta, por mais neurônios que tenha. <b>C:</b> taxa muito baixa (0,0001) nem converge em 2000 épocas; taxa muito alta (0,1) converge em poucas épocas, mas pode oscilar.</div>';
  };

  /* ---- cap 5: a rede mínima que resolve o XOR, treinada no navegador ---- */
  E.demos.xor = function (el) {
    el.innerHTML = '<h4>Uma rede 2-4-1 (tanh) aprendendo o XOR, que o Perceptron não aprende</h4><div class="grid2"><canvas style="height:260px;cursor:default"></canvas><div><canvas class="lc" style="height:260px;cursor:default"></canvas></div></div><div class="ctrls"><button class="btn sm pri" type="button" id="xt">▶ Treinar 1500 épocas</button><button class="btn sm" type="button" id="xz">Reiniciar pesos</button></div><div class="read"></div>';
    var cvs = el.querySelectorAll("canvas"), rd = el.querySelector(".read"), r, W1, b1, W2, b2, loss = [], epoca = 0, timer = 0;
    var X = IN, Y = GATES.XOR;
    function init() { r = rng(7); W1 = []; for (var i = 0; i < 4; i++) W1.push([(r() - .5) * 2, (r() - .5) * 2]); b1 = [0, 0, 0, 0]; W2 = [(r() - .5), (r() - .5), (r() - .5), (r() - .5)]; b2 = 0; loss = []; epoca = 0; }
    function fwd(x) { var h = []; for (var i = 0; i < 4; i++) h.push(Math.tanh(W1[i][0] * x[0] + W1[i][1] * x[1] + b1[i])); var z = b2; for (var j = 0; j < 4; j++) z += W2[j] * h[j]; return { h: h, y: 1 / (1 + Math.exp(-z)) }; }
    function treina(n) { var lr = 0.5; for (var e = 0; e < n; e++) { var L = 0; X.forEach(function (x, k) { var o = fwd(x), d = o.y - Y[k]; L += d * d; var gW2 = [], gb2 = d, gh = []; for (var j = 0; j < 4; j++) { gW2.push(d * o.h[j]); gh.push(d * W2[j] * (1 - o.h[j] * o.h[j])); } for (var j2 = 0; j2 < 4; j2++) { W2[j2] -= lr * gW2[j2]; W1[j2][0] -= lr * gh[j2] * x[0]; W1[j2][1] -= lr * gh[j2] * x[1]; b1[j2] -= lr * gh[j2]; } b2 -= lr * gb2; }); loss.push(L / 4); epoca++; } }
    init();
    var a1 = E.canvas(cvs[0], function (ctx, w, h, c) {
      var P = plotter(w, h, -0.3, 1.3, -0.3, 1.3, { l: 30, r: 8, t: 8, b: 26 }); var n = 28;
      for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) { var x = -0.3 + i / n * 1.6, y = -0.3 + j / n * 1.6, o = fwd([x, y]).y; ctx.fillStyle = o > .5 ? c.c1 : c.c0; ctx.globalAlpha = .12 + .38 * Math.abs(o - .5) * 2; ctx.fillRect(P.X(x), P.Y(y + 1.6 / n), (w - 38) / n + 1, (h - 34) / n + 1); } ctx.globalAlpha = 1;
      axes(ctx, w, h, P, -0.3, 1.3, -0.3, 1.3, 1, 1, "x1", "x2", c);
      X.forEach(function (p, k) { ctx.beginPath(); ctx.arc(P.X(p[0]), P.Y(p[1]), 10, 0, 6.2832); ctx.fillStyle = Y[k] ? c.c1 : c.c0; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = c.ink; ctx.stroke(); ctx.font = "700 12px Inter,sans-serif"; ctx.textAlign = "center"; ctx.lineWidth = 3; ctx.strokeStyle = "#10131c"; ctx.strokeText(Y[k], P.X(p[0]), P.Y(p[1]) + 4); ctx.fillStyle = "#fff"; ctx.fillText(Y[k], P.X(p[0]), P.Y(p[1]) + 4); });
    });
    var a2 = E.canvas(cvs[1], function (ctx, w, h, c) {
      var P = plotter(w, h, 0, 1500, 0, 0.35, { l: 40, r: 8, t: 8, b: 26 }); axes(ctx, w, h, P, 0, 1500, 0, 0.35, 500, 0.1, "época", "erro (perda)", c);
      ctx.beginPath(); loss.forEach(function (v, i) { var Xp = P.X(i), Yp = P.Y(Math.min(0.35, v)); if (i) ctx.lineTo(Xp, Yp); else ctx.moveTo(Xp, Yp); }); ctx.lineWidth = 2.5; ctx.strokeStyle = c.red; ctx.stroke();
    });
    function rep() { var ok = X.every(function (p, k) { return (fwd(p).y > .5 ? 1 : 0) === Y[k]; }); rd.innerHTML = "Época <b>" + epoca + "</b>. Saídas: " + X.map(function (p, k) { return "[" + p + "] → <b>" + fwd(p).y.toFixed(2) + "</b>"; }).join(" · ") + ". " + (epoca === 0 ? "Pesos aleatórios: a rede ainda não sabe o XOR." : (ok ? "<b style='color:var(--green)'>Acertou os 4 casos.</b> A <b>camada oculta</b> cria uma fronteira curva, que uma reta (um neurônio só) não consegue." : "Ainda aprendendo...")); a1.paint(); a2.paint(); }
    el.querySelector("#xt").addEventListener("click", function () { clearInterval(timer); if (epoca >= 1500) { init(); } var k = 0; timer = setInterval(function () { treina(E.reduce ? 1500 : 50); rep(); if (epoca >= 1500) clearInterval(timer); }, 30); });
    el.querySelector("#xz").addEventListener("click", function () { clearInterval(timer); init(); rep(); });
    rep();
  };

  /* ---- cap 7: convolução ---- */
  E.demos.conv = function (el) {
    var IMG = ["00000000", "00111100", "00111100", "00111100", "00111100", "00111100", "00111100", "00000000"].map(function (r) { return r.split("").map(Number); });
    var K = { "borda vertical": [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], "borda horizontal": [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], "desfocar": [[1, 1, 1], [1, 1, 1], [1, 1, 1]].map(function (r) { return r.map(function (v) { return v / 9; }); }) };
    el.innerHTML = '<h4>Um filtro 3x3 deslizando por uma imagem 8x8</h4><div class="ctrls"><label>filtro <select id="ck">' + Object.keys(K).map(function (k) { return '<option>' + k + '</option>'; }).join("") + '</select></label></div><div class="grid3" style="align-items:start"><div><b>Imagem</b><div class="cg i"></div></div><div><b>Filtro</b><div class="cg k"></div></div><div><b>Resultado (6x6)</b><div class="cg o"></div></div></div><div class="read">O filtro desliza pela imagem. Em cada posição, <b>multiplica</b> cada pixel pelo número do filtro e <b>soma</b>. Filtros de borda reagem onde o brilho muda; o resultado é um "mapa de onde há borda". Numa <b>rede convolucional</b> (CNN), esses números do filtro <b>são os pesos</b>, e <b>aprendidos</b>, em vez de escolhidos à mão.</div>';
    var ck = el.querySelector("#ck");
    function grid(sel, m, fmt, col) { el.querySelector(sel).innerHTML = '<div style="display:grid;grid-template-columns:repeat(' + m[0].length + ',1fr);gap:2px">' + m.map(function (r) { return r.map(function (v) { return '<div style="aspect-ratio:1;display:grid;place-items:center;font:.62rem var(--f-mono);background:' + col(v) + ';border-radius:3px">' + fmt(v) + '</div>'; }).join(""); }).join("") + '</div>'; }
    function go() {
      var k = K[ck.value], out = [];
      for (var y = 0; y < 6; y++) { var row = []; for (var x = 0; x < 6; x++) { var s = 0; for (var a = 0; a < 3; a++) for (var b = 0; b < 3; b++) s += IMG[y + a][x + b] * k[a][b]; row.push(s); } out.push(row); }
      grid(".i", IMG, function (v) { return v; }, function (v) { return v ? "var(--ink)" : "var(--paper-2)"; });
      grid(".k", k, function (v) { return Math.round(v * 100) / 100; }, function () { return "var(--pen-soft)"; });
      var mx = Math.max.apply(null, out.map(function (r) { return Math.max.apply(null, r.map(Math.abs)); })) || 1;
      grid(".o", out, function (v) { return Math.round(v * 10) / 10; }, function (v) { var t = Math.abs(v) / mx; return "color-mix(in srgb,var(--" + (v >= 0 ? "c1" : "c0") + ") " + Math.round(t * 90) + "%,var(--paper-2))"; });
    }
    ck.addEventListener("change", go); go();
  };

  /* ---- cap 8: algoritmo genético evoluindo uma frase ---- */
  E.demos.genetico = function (el) {
    var ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    el.innerHTML = '<h4>Evoluir uma frase a partir de letras aleatórias</h4><div class="ctrls"><label>alvo <input type="text" id="ga" value="OLA MUNDO" maxlength="16" style="width:170px;font-family:var(--f-mono)"></label><label>população <input type="range" id="gp" min="20" max="300" step="10" value="100"><output id="gpo">100</output></label><label>mutação <input type="range" id="gm" min="0" max="60" value="3"><output id="gmo">3%</output></label></div><div class="ctrls"><button class="btn sm pri" type="button" id="gg">▶ Evoluir</button><button class="btn sm" type="button" id="gs">Parar</button></div><div class="tablewrap"><table class="gt"></table></div><div class="read"></div>';
    var timer = 0, g = function (id) { return el.querySelector(id); };
    function evolve() {
      clearInterval(timer); var alvo = g("#ga").value.toUpperCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Z ]/g, ""); if (!alvo) { g(".read").textContent = "Digite um alvo com letras e espaços."; return; }
      var N = +g("#gp").value, mut = +g("#gm").value / 100, r = rng(Date.now() & 0xffff), L = alvo.length;
      var pop = []; for (var i = 0; i < N; i++) { var s = ""; for (var j = 0; j < L; j++) s += ALF[Math.floor(r() * 27)]; pop.push(s); }
      var fit = function (s) { var f = 0; for (var i = 0; i < L; i++) if (s[i] === alvo[i]) f++; return f; }, gen = 0, rows = [];
      function passo() {
        pop.sort(function (a, b) { return fit(b) - fit(a); }); var best = pop[0], f = fit(best);
        rows.push('<tr class="' + (f === L ? "dest" : "") + '"><td>' + gen + '</td><td><code>' + esc(best) + '</code></td><td>' + f + '/' + L + '</td></tr>'); if (rows.length > 8) rows.shift();
        g(".gt").innerHTML = '<tr><th>geração</th><th>melhor indivíduo</th><th>aptidão (fitness)</th></tr>' + rows.join("");
        if (f === L) { clearInterval(timer); g(".read").innerHTML = "<b style='color:var(--green)'>Chegou ao alvo na geração " + gen + ".</b> Ninguém programou a resposta: ela <b>emergiu</b> de seleção, cruzamento e mutação. Mude a população e a mutação: sem mutação a população costuma travar (sem novidade), e com mutação muito alta a busca vira quase aleatória. Com um alvo curto o efeito é pequeno: experimente um alvo de 16 letras e mutação acima de 30%."; return; }
        var pais = pop.slice(0, Math.max(2, Math.floor(N / 5))), novo = [best];
        while (novo.length < N) { var a = pais[Math.floor(r() * pais.length)], b = pais[Math.floor(r() * pais.length)], corte = Math.floor(r() * L), f2 = ""; for (var i = 0; i < L; i++) { var ch = i < corte ? a[i] : b[i]; if (r() < mut) ch = ALF[Math.floor(r() * 27)]; f2 += ch; } novo.push(f2); }
        pop = novo; gen++;
      }
      g(".read").innerHTML = "<b>Seleção</b>: só os 20% melhores da população viram pais. <b>Cruzamento</b>: o filho pega o começo de um pai e o fim do outro. <b>Mutação</b>: cada letra pode mudar ao acaso. O melhor sempre passa adiante (<i>elitismo</i>).";
      passo(); timer = setInterval(function () { passo(); if (gen > 600) { clearInterval(timer); g(".read").innerHTML += " <b>Parou em 600 gerações.</b> Tente outra mutação."; } }, E.reduce ? 5 : 90);
    }
    g("#gg").addEventListener("click", evolve); g("#gs").addEventListener("click", function () { clearInterval(timer); });
    el.addEventListener("input", function () { g("#gpo").textContent = g("#gp").value; g("#gmo").textContent = g("#gm").value + "%"; });
  };
})();
