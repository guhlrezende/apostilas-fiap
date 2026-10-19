/* Demos do capítulo 5: regressão linear (Insurance real) */
(function () {
  var E = window.Estudo, ML = window.ML, D = ML.D, INS = D.INS;

  /* ---- a planilha: custo = b0 + b1 * IMC ---- */
  E.demos.planilha = function (el) {
    el.innerHTML = '<h4>A planilha da aula: custo = b0 + b1 × IMC</h4>' +
      '<div class="ctrls"><label>b0 (intercepto) <input type="range" id="p0" min="0" max="10000" step="100" value="5000"><output id="p0o"></output></label>' +
      '<label>b1 (coef. angular) <input type="range" id="p1" min="0" max="500" step="10" value="200"><output id="p1o"></output></label></div><canvas style="height:240px;cursor:default"></canvas>' +
      '<div class="tablewrap"><table class="tb"></table></div><div class="read"></div>';
    var p0 = el.querySelector("#p0"), p1 = el.querySelector("#p1"), cv = el.querySelector("canvas");
    var xs = [0, 15, 17, 19, 21, 23, 25, 27, 29, 31];
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var b0 = +p0.value, b1 = +p1.value, P = ML.plot(w, h, 0, 32, 0, 20000, { l: 56, r: 14, t: 12, b: 36 });
      ML.axes(ctx, w, h, P, 0, 32, 0, 20000, 4, 5000, "IMC", "custo previsto (US$)", c);
      ctx.beginPath(); ctx.moveTo(P.X(0), P.Y(b0)); ctx.lineTo(P.X(32), P.Y(b0 + b1 * 32)); ctx.lineWidth = 3.5; ctx.strokeStyle = c.pen; ctx.stroke();
      ctx.beginPath(); ctx.arc(P.X(0), P.Y(b0), 7, 0, 6.2832); ctx.fillStyle = c.red; ctx.fill();
      ctx.fillStyle = c.red; ctx.font = "700 12px Inter,system-ui,sans-serif"; ctx.textAlign = "left"; ctx.fillText("b0 = onde a reta cruza o eixo", P.X(0) + 12, P.Y(b0) - 8);
      xs.forEach(function (x) { ctx.beginPath(); ctx.arc(P.X(x), P.Y(b0 + b1 * x), 4, 0, 6.2832); ctx.fillStyle = c.pen; ctx.fill(); });
    });
    function calc() {
      var b0 = +p0.value, b1 = +p1.value; el.querySelector("#p0o").textContent = E.fmt(b0); el.querySelector("#p1o").textContent = E.fmt(b1);
      el.querySelector(".tb").innerHTML = "<tr><th>IMC</th>" + xs.map(function (x) { return "<th class='n'>" + x + "</th>"; }).join("") + "</tr><tr><td><b>custo</b></td>" + xs.map(function (x) { return "<td class='n'>" + E.fmt(b0 + b1 * x) + "</td>"; }).join("") + "</tr>";
      el.querySelector(".read").innerHTML = "<b>b0 = " + E.fmt(b0) + "</b> é o custo quando IMC = 0 (o ponto de partida). <b>b1 = " + E.fmt(b1) + "</b> é quanto o custo sobe a cada ponto de IMC: de um IMC para o seguinte a coluna soma sempre o mesmo valor. Com os valores da aula (5.000 e 200), IMC 15 dá 8.000 e IMC 17 dá 8.400.";
      api.paint();
    }
    p0.addEventListener("input", calc); p1.addEventListener("input", calc); calc();
  };

  /* ---- arraste a reta e veja o erro (Insurance real: IMC x custo em milhares) ---- */
  E.demos.reta = function (el) {
    var all = INS.map(function (r) { return { x: r[1], y: r[6] / 1000, s: r[3] }; });
    var idx = ML.shuffle(all.map(function (_, i) { return i; }), ML.rng(11)).slice(0, 25), small = idx.map(function (i) { return all[i]; });
    el.innerHTML = '<h4>Arraste as bolinhas da reta (ou use os botões) e veja o erro cair</h4><canvas></canvas>' +
      '<div class="ctrls"><label>dados <select id="rm"><option value="s">25 pontos (para enxergar os resíduos)</option><option value="a">os 1.338 pontos</option></select></label>' +
      '<label><input type="checkbox" id="rc"> colorir por fumante</label></div>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" data-a="best">Melhor reta</button><button class="btn sm" type="button" data-a="mean">Só a média (b1 = 0)</button><button class="btn sm" type="button" data-a="slide">Reta da aula (1,19 e 0,39)</button><button class="btn sm" type="button" data-a="rand">Reta aleatória</button></div>' +
      '<div class="kp grid2" style="gap:8px"></div><div class="read"></div>' +
      '<p class="muted" style="font-size:.85rem;margin:8px 0 0">Custo em <b>milhares</b> de dólares (<code>charges/1000</code>), como no slide da aula. As linhas vermelhas são os <b>resíduos</b>: a distância de cada ponto até a reta. Erro e R² são calculados nos pontos mostrados, sem separar treino e teste.</p>';
    var cv = el.querySelector("canvas"), rm = el.querySelector("#rm"), rc = el.querySelector("#rc"), b0 = 2, b1 = 0, X1 = 16, X2 = 54;
    function set() { return rm.value === "s" ? small : all; }
    function ls(s) { var n = s.length, mx = 0, my = 0; s.forEach(function (p) { mx += p.x; my += p.y; }); mx /= n; my /= n; var sxy = 0, sxx = 0; s.forEach(function (p) { sxy += (p.x - mx) * (p.y - my); sxx += (p.x - mx) * (p.x - mx); }); var b = sxy / sxx; return { b0: my - b * mx, b1: b }; }
    function met(s) { var n = s.length, my = 0, sse = 0, sst = 0; s.forEach(function (p) { my += p.y; }); my /= n; s.forEach(function (p) { var e = p.y - (b0 + b1 * p.x); sse += e * e; sst += (p.y - my) * (p.y - my); }); return { mse: sse / n, r2: 1 - sse / sst }; }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = ML.plot(w, h, 14, 56, -5, 66, { l: 48, r: 14, t: 12, b: 36 }); cv._P = P;
      ML.axes(ctx, w, h, P, 14, 56, -5, 66, 5, 10, "IMC (bmi)", "custo (mil US$)", c);
      var s = set(), sm = rm.value === "s";
      if (sm) { ctx.strokeStyle = c.red; ctx.globalAlpha = .8; ctx.lineWidth = 1.6; s.forEach(function (p) { ctx.beginPath(); ctx.moveTo(P.X(p.x), P.Y(p.y)); ctx.lineTo(P.X(p.x), P.Y(b0 + b1 * p.x)); ctx.stroke(); }); ctx.globalAlpha = 1; }
      ctx.globalAlpha = sm ? .95 : .4; s.forEach(function (p) { ctx.beginPath(); ctx.arc(P.X(p.x), P.Y(p.y), sm ? 5 : 2.8, 0, 6.2832); ctx.fillStyle = rc.checked ? (p.s ? c.c1 : c.c0) : c.pen; ctx.fill(); }); ctx.globalAlpha = 1;
      ctx.beginPath(); ctx.moveTo(P.X(X1), P.Y(b0 + b1 * X1)); ctx.lineTo(P.X(X2), P.Y(b0 + b1 * X2)); ctx.lineWidth = 3.5; ctx.strokeStyle = c.ink; ctx.stroke();
      [X1, X2].forEach(function (x) { ctx.beginPath(); ctx.arc(P.X(x), P.Y(b0 + b1 * x), 9, 0, 6.2832); ctx.fillStyle = c.red; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = c.paper; ctx.stroke(); });
    });
    function report() {
      var s = set(), m = met(s), best = ls(s), mb = (function () { var s0 = b0, s1 = b1; b0 = best.b0; b1 = best.b1; var r = met(s); b0 = s0; b1 = s1; return r; })();
      el.querySelector(".kp").innerHTML = [["Reta", "y = " + E.fmt(b0, 2) + " + " + E.fmt(b1, 3) + " · IMC"], ["MSE", E.fmt(m.mse, 2)], ["RMSE", E.fmt(Math.sqrt(m.mse), 2) + " mil"], ["R²", E.fmt(m.r2, 3)]].map(function (k) { return '<div class="card" style="margin:0;padding:8px 14px"><small class="muted">' + k[0] + '</small><br><b style="font:700 1.25rem var(--f-head)">' + k[1] + '</b></div>'; }).join("");
      var gap = m.mse - mb.mse;
      el.querySelector(".read").innerHTML = gap < 0.02 * Math.max(1, mb.mse) ? "<b style='color:var(--green)'>Você chegou na melhor reta!</b> Nenhuma outra reta tem MSE menor para estes pontos: é o que os <b>mínimos quadrados</b> garantem." : "A melhor reta para estes pontos tem MSE <b>" + E.fmt(mb.mse, 2) + "</b> (y = " + E.fmt(best.b0, 2) + " + " + E.fmt(best.b1, 3) + "·IMC). A sua está <b>" + E.fmt(gap, 2) + "</b> acima. Continue arrastando ou clique em <b>Melhor reta</b>.";
    }
    function paint() { api.paint(); report(); }
    var drag = 0;
    E.pointer(cv, function (x, y) { var P = cv._P; if (!P) return; var d1 = Math.abs(P.X(X1) - x) + Math.abs(P.Y(b0 + b1 * X1) - y), d2 = Math.abs(P.X(X2) - x) + Math.abs(P.Y(b0 + b1 * X2) - y); drag = d1 <= d2 ? 1 : 2; move(y); }, function (x, y) { move(y); });
    function move(py) { var P = cv._P, v = Math.max(-5, Math.min(66, P.iy(py))); var y1 = b0 + b1 * X1, y2 = b0 + b1 * X2; if (drag === 1) y1 = v; else y2 = v; b1 = (y2 - y1) / (X2 - X1); b0 = y1 - b1 * X1; paint(); }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-a]"); if (!b) return; var a = b.getAttribute("data-a"), s = set();
      if (a === "best") { var r = ls(s); b0 = r.b0; b1 = r.b1; } if (a === "mean") { var my = s.reduce(function (t, p) { return t + p.y; }, 0) / s.length; b0 = my; b1 = 0; }
      if (a === "slide") { b0 = 1.1929; b1 = 0.3939; } if (a === "rand") { b0 = -5 + Math.random() * 30; b1 = -0.4 + Math.random() * 1.2; }
      paint();
    });
    rm.addEventListener("change", paint); rc.addEventListener("change", paint); paint();
  };

  /* ---- duas retas paralelas: IMC + fumante ---- */
  E.demos.plano = function (el) {
    var rows = INS.map(function (r) { return { x: r[1], s: r[3], y: r[6] / 1000 }; });
    function solve(A, b) { var n = b.length, i, j, k; for (i = 0; i < n; i++) { var m = i; for (j = i + 1; j < n; j++) if (Math.abs(A[j][i]) > Math.abs(A[m][i])) m = j; var t = A[i]; A[i] = A[m]; A[m] = t; var tb = b[i]; b[i] = b[m]; b[m] = tb; for (j = i + 1; j < n; j++) { var f = A[j][i] / A[i][i]; for (k = i; k < n; k++) A[j][k] -= f * A[i][k]; b[j] -= f * b[i]; } } var x = new Array(n).fill(0); for (i = n - 1; i >= 0; i--) { var s = b[i]; for (j = i + 1; j < n; j++) s -= A[i][j] * x[j]; x[i] = s / A[i][i]; } return x; }
    function fit(cols) { var p = cols.length, A = [], b = []; for (var i = 0; i < p; i++) { A.push(new Array(p).fill(0)); b.push(0); } rows.forEach(function (r) { var v = cols.map(function (f) { return f(r); }); for (var i = 0; i < p; i++) { b[i] += v[i] * r.y; for (var j = 0; j < p; j++) A[i][j] += v[i] * v[j]; } }); return solve(A, b); }
    function r2(pred) { var my = rows.reduce(function (t, r) { return t + r.y; }, 0) / rows.length, sse = 0, sst = 0; rows.forEach(function (r) { var e = r.y - pred(r); sse += e * e; sst += (r.y - my) * (r.y - my); }); return 1 - sse / sst; }
    var f1 = fit([function () { return 1; }, function (r) { return r.x; }]), f2 = fit([function () { return 1; }, function (r) { return r.x; }, function (r) { return r.s; }]);
    var R1 = r2(function (r) { return f1[0] + f1[1] * r.x; }), R2 = r2(function (r) { return f2[0] + f2[1] * r.x + f2[2] * r.s; });
    el.innerHTML = '<h4>Uma reta, ou duas retas paralelas?</h4><canvas></canvas><div class="ctrls"><button class="btn sm pri" type="button" data-m="1">Só IMC</button><button class="btn sm" type="button" data-m="2">IMC + fumante</button></div><div class="read"></div>';
    var cv = el.querySelector("canvas"), mode = 1;
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = ML.plot(w, h, 14, 56, -5, 66, { l: 48, r: 14, t: 12, b: 36 });
      ML.axes(ctx, w, h, P, 14, 56, -5, 66, 5, 10, "IMC (bmi)", "custo (mil US$)", c);
      ctx.globalAlpha = .4; rows.forEach(function (r) { ctx.beginPath(); ctx.arc(P.X(r.x), P.Y(r.y), 2.8, 0, 6.2832); ctx.fillStyle = r.s ? c.c1 : c.c0; ctx.fill(); }); ctx.globalAlpha = 1;
      function line(a, b, col) { ctx.beginPath(); ctx.moveTo(P.X(15), P.Y(a + b * 15)); ctx.lineTo(P.X(55), P.Y(a + b * 55)); ctx.lineWidth = 3.5; ctx.strokeStyle = col; ctx.stroke(); }
      if (mode === 1) line(f1[0], f1[1], c.ink); else { line(f2[0], f2[1], c.c0); line(f2[0] + f2[2], f2[1], c.c1); }
    });
    function report() {
      el.querySelector(".read").innerHTML = mode === 1 ?
        "<b>Só IMC:</b> custo = " + E.fmt(f1[0], 2) + " + " + E.fmt(f1[1], 3) + " · IMC. <b>R² = " + E.fmt(R1, 3) + "</b>: a reta explica uns <b>4%</b> da variação do custo. A nuvem é muito mais espalhada do que a reta." :
        "<b>IMC + fumante:</b> custo = " + E.fmt(f2[0], 2) + " + " + E.fmt(f2[1], 3) + " · IMC + " + E.fmt(f2[2], 2) + " · fumante. Duas retas <b>paralelas</b>: a de cima é a dos fumantes (+" + E.fmt(f2[2], 1) + " mil). <b>R² = " + E.fmt(R2, 3) + "</b>. Uma única coluna extra, e o modelo passou de 4% para cerca de 66%.";
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-m]"); if (!b) return; mode = +b.getAttribute("data-m"); el.querySelectorAll("button").forEach(function (x) { x.classList.toggle("pri", x === b); }); api.paint(); report(); }); report();
  };

  /* ---- quem pesa mais no custo (coeficientes reais do notebook) ---- */
  E.demos.coef = function (el) {
    var L = D.LIN, rows = L.cols.map(function (c, i) { return { c: c, v: L.coef[i] }; }).sort(function (a, b) { return Math.abs(b.v) - Math.abs(a.v); }), mx = Math.abs(rows[0].v);
    el.innerHTML = '<h4>Coeficientes do modelo com todas as variáveis (já padronizadas)</h4><div class="bars">' + rows.map(function (r) {
      return '<div class="bar ' + (r.v < 0 ? "bad" : "") + '"><div><code>' + r.c + '</code></div><div class="tr"><div class="fl" style="width:0"></div></div><div class="v">' + (r.v > 0 ? "+" : "") + E.fmt(r.v, 0) + '</div></div>'; }).join("") +
      '</div><div class="ctrls"><button class="btn sm" type="button" id="cr">Animar de novo ↺</button></div><div class="read">Cada coeficiente é <b>quanto o custo previsto muda, em US$, quando a variável sobe 1 desvio-padrão</b>, com as outras fixas. <b>Fumar</b> pesa mais que qualquer outra coisa, depois a <b>idade</b> e o <b>IMC</b>. <code>sex_male</code> é praticamente zero.</div>';
    var bars = el.querySelectorAll(".bar");
    function run() { bars.forEach(function (b) { b.querySelector(".fl").style.width = "0%"; }); setTimeout(function () { bars.forEach(function (b, i) { setTimeout(function () { b.querySelector(".fl").style.width = Math.max(1, Math.abs(rows[i].v) / mx * 100) + "%"; }, i * 90); }); }, 60); }
    el.querySelector("#cr").addEventListener("click", run); run();
  };

  /* ---- calculadora de previsão com a reta da aula ---- */
  E.demos.prever = function (el) {
    el.innerHTML = '<h4>Usando a reta da aula: custo = 1,1929 + 0,3939 × IMC</h4><div class="ctrls"><label>IMC <input type="range" id="pi" min="15" max="50" step="0.5" value="20"><output id="pio">20</output></label></div><div class="read"></div>';
    var pi = el.querySelector("#pi"), rd = el.querySelector(".read");
    function calc() { var x = +pi.value; el.querySelector("#pio").textContent = E.fmt(x, 1); var m = 1.1929372 + 0.3938730 * x; rd.innerHTML = "IMC <b>" + E.fmt(x, 1) + "</b>: 1,1929 + 0,3939 × " + E.fmt(x, 1) + " = <b>" + E.fmt(m, 4) + " mil</b>, ou cerca de <b>US$ " + E.fmt(m * 1000, 0) + "</b> (por isso o <code>×1000</code>: o custo está em milhares). Em IMC 20, são os 9.070 do slide; em 15, 22, 28 e 33 saem 7,10, 9,86, 12,22 e 14,19 mil."; }
    pi.addEventListener("input", calc); calc();
  };

  /* ---- placar com a referência extra ---- */
  E.demos.placar3 = function (el) {
    var R = D.REF, L = D.LIN, f = function (v, n) { return E.fmt(v, n); };
    el.innerHTML = '<div class="tablewrap"><table><tr><th>Modelo (mesma divisão 80/20, seed 42)</th><th class="n">MAE</th><th class="n">RMSE</th><th class="n">R²</th></tr>' +
      '<tr><td>KNN baseline (k=5)</td><td class="n">' + f(R.baseline.MAE, 2) + '</td><td class="n">' + f(R.baseline.RMSE, 2) + '</td><td class="n">' + f(R.baseline.R2, 4) + '</td></tr>' +
      '<tr><td>KNN tunado (GridSearchCV)</td><td class="n">' + f(R.tunado.MAE, 2) + '</td><td class="n">' + f(R.tunado.RMSE, 2) + '</td><td class="n">' + f(R.tunado.R2, 4) + '</td></tr>' +
      '<tr class="dest"><td>Regressão linear (todas as variáveis)</td><td class="n">' + f(L.MAE, 2) + '</td><td class="n">' + f(L.RMSE, 2) + '</td><td class="n">' + f(L.R2, 4) + '</td></tr></table></div>';
  };
})();
