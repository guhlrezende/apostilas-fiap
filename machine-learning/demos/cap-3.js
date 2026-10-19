/* Demos do capítulo 3: KNN para números (Insurance real) */
(function () {
  var E = window.Estudo, ML = window.ML, D = ML.D, INS = D.INS;
  var money = function (v) { return "$" + E.fmt(v, 0); };

  /* ---- olhar os dados: idade ou IMC x custo, colorido por fumante ---- */
  E.demos.insScatter = function (el) {
    el.innerHTML = '<h4>1.338 pessoas do seguro, uma bolinha cada</h4><canvas></canvas>' +
      '<div class="ctrls"><label>eixo x <select id="ix"><option value="0">idade</option><option value="1">IMC</option></select></label>' +
      '<label>mostrar <select id="ig"><option value="all">todos</option><option value="0">só não fumantes</option><option value="1">só fumantes</option></select></label></div>' +
      '<div class="legend"><span><i style="background:var(--c0)"></i>não fuma</span><span><i style="background:var(--c1)"></i>fuma</span></div><div class="read"></div>';
    var cv = el.querySelector("canvas"), rd = el.querySelector(".read"), ix = el.querySelector("#ix"), ig = el.querySelector("#ig");
    var mean = function (s) { var a = INS.filter(function (r) { return r[3] === s; }); return a.reduce(function (t, r) { return t + r[6]; }, 0) / a.length; };
    var m0 = mean(0), m1 = mean(1);
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var xi = +ix.value, x0 = xi ? 15 : 17, x1 = xi ? 54 : 65, P = ML.plot(w, h, x0, x1, 0, 65000, { l: 56, r: 12, t: 12, b: 36 });
      ML.axes(ctx, w, h, P, x0, x1, 0, 65000, xi ? 5 : 10, 10000, xi ? "IMC (bmi)" : "idade (age)", "custo (charges)", c, function (v) { return v / 1000 + " mil"; });
      var sel = ig.value;
      ctx.globalAlpha = .55;
      INS.forEach(function (r) { if (sel !== "all" && +sel !== r[3]) return; ctx.beginPath(); ctx.arc(P.X(r[xi]), P.Y(r[6]), 3, 0, 6.2832); ctx.fillStyle = r[3] ? c.c1 : c.c0; ctx.fill(); });
      ctx.globalAlpha = 1;
    });
    rd.innerHTML = "Custo médio: <b>não fumantes " + money(m0) + "</b> · <b>fumantes " + money(m1) + "</b> (" + (m1 / m0).toFixed(1).replace(".", ",") + " vezes mais). Troque o eixo para IMC e veja o grupo de fumantes se partir em dois.";
    ix.addEventListener("change", api.paint); ig.addEventListener("change", api.paint);
  };

  /* ---- KNN regressão em 1 dimensão (não fumantes, idade -> custo) ---- */
  E.demos.knnReg1d = function (el) {
    el.innerHTML = '<h4>A média dos vizinhos desenha uma curva</h4><canvas></canvas>' +
      '<div class="ctrls"><label>k = <input type="range" min="1" max="150" value="40" id="k1"><output id="k1o">40</output></label></div>' +
      '<div class="legend"><span><i style="background:var(--c0)"></i>não fumantes (1.064 pessoas reais)</span><span><i style="background:var(--red)"></i>previsão do KNN</span></div>' +
      '<div class="read">Clique no gráfico para escolher uma idade e ver os vizinhos.</div>';
    var cv = el.querySelector("canvas"), rd = el.querySelector(".read"), kEl = el.querySelector("#k1"), ko = el.querySelector("#k1o");
    var pts = INS.filter(function (r) { return r[3] === 0; }).map(function (r) { return { a: r[0], y: r[6] }; });
    var xs = []; for (var a = 18; a <= 64.001; a += 0.5) xs.push(a);
    var order = xs.map(function (x) { var idx = pts.map(function (_, i) { return i; }); idx.sort(function (i, j) { return Math.abs(pts[i].a - x) - Math.abs(pts[j].a - x) || i - j; }); return idx; });
    function predAt(oi, k) { var s = 0; for (var j = 0; j < k; j++) s += pts[order[oi][j]].y; return s / k; }
    var qx = null;
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = ML.plot(w, h, 17, 65, 0, 30000, { l: 56, r: 12, t: 12, b: 36 }); cv._P = P;
      ML.axes(ctx, w, h, P, 17, 65, 0, 30000, 10, 5000, "idade", "custo", c, function (v) { return v / 1000 + " mil"; });
      ctx.globalAlpha = .35; pts.forEach(function (p) { if (p.y > 30000) return; ctx.beginPath(); ctx.arc(P.X(p.a), P.Y(p.y), 2.6, 0, 6.2832); ctx.fillStyle = c.c0; ctx.fill(); }); ctx.globalAlpha = 1;
      var k = +kEl.value;
      if (qx !== null) {
        var oi = Math.round((qx - 18) / 0.5), ids = order[oi].slice(0, k), ys = ids.map(function (i) { return pts[i].y; });
        ctx.fillStyle = c.hlY; var lo = Math.min.apply(null, ids.map(function (i) { return pts[i].a; })), hi = Math.max.apply(null, ids.map(function (i) { return pts[i].a; }));
        ctx.fillRect(P.X(lo) - 3, P.pad.t, P.X(hi) - P.X(lo) + 6, h - P.pad.t - P.pad.b);
        ctx.globalAlpha = .9; ids.forEach(function (i) { if (pts[i].y > 30000) return; ctx.beginPath(); ctx.arc(P.X(pts[i].a), P.Y(pts[i].y), 3.6, 0, 6.2832); ctx.fillStyle = c.ink; ctx.fill(); }); ctx.globalAlpha = 1;
      }
      ctx.beginPath(); xs.forEach(function (x, i) { var X = P.X(x), Y = P.Y(Math.min(30000, predAt(i, k))); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); });
      ctx.lineWidth = 3; ctx.strokeStyle = c.red; ctx.stroke();
      if (qx !== null) { var oq = Math.round((qx - 18) / 0.5), pv = predAt(oq, k); ctx.beginPath(); ctx.arc(P.X(qx), P.Y(Math.min(30000, pv)), 6, 0, 6.2832); ctx.fillStyle = c.red; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = c.paper; ctx.stroke(); }
    });
    function report() {
      ko.textContent = kEl.value; if (qx === null) return;
      var k = +kEl.value, oi = Math.round((qx - 18) / 0.5), ids = order[oi].slice(0, k);
      var ages = ids.map(function (i) { return pts[i].a; });
      var lo = Math.min.apply(null, ages), hi = Math.max.apply(null, ages);
      rd.innerHTML = "Pessoa de <b>" + Math.round(qx) + " anos</b>. Os <b>" + k + "</b> vizinhos " + (lo === hi ? "têm todos <b>" + lo + "</b> anos" : "têm entre <b>" + lo + "</b> e <b>" + hi + "</b> anos") + ". Previsão (média dos custos deles): <b>" + money(predAt(oi, k)) + "</b>." + (k <= 5 ? " Com poucos vizinhos, a previsão depende muito de quem calhou de ser sorteado entre pessoas da mesma idade." : "");
    }
    E.pointer(cv, function (x) { qx = Math.max(18, Math.min(64, cv._P.ix(x))); api.paint(); report(); }, function (x) { qx = Math.max(18, Math.min(64, cv._P.ix(x))); api.paint(); report(); });
    kEl.addEventListener("input", function () { api.paint(); report(); });
  };

  /* ---- por que a escala importa ---- */
  var PESSOAS = [[25, 40000], [30, 60000], [41, 120000], [52, 90000], [23, 250000], [60, 130000], [35, 200000], [70, 30000], [18, 80000], [45, 260000]];
  E.demos.escala = function (el) {
    el.innerHTML = '<h4>Quem é o vizinho mais próximo?</h4>' +
      '<div class="ctrls"><label>idade <input type="range" id="ea" min="18" max="70" value="45"><output id="eao">45</output></label>' +
      '<label>renda (R$) <input type="range" id="er" min="30000" max="260000" step="5000" value="150000"><output id="ero">150.000</output></label></div>' +
      '<div class="grid2"><div><b>Sem escala</b><div class="tablewrap"><table class="t0"></table></div></div><div><b>Com MinMax (0 a 1)</b><div class="tablewrap"><table class="t1"></table></div></div></div><div class="read"></div>';
    var ea = el.querySelector("#ea"), er = el.querySelector("#er"), rd = el.querySelector(".read");
    function calc() {
      var a = +ea.value, r = +er.value;
      el.querySelector("#eao").textContent = a; el.querySelector("#ero").textContent = E.fmt(r);
      var raw = PESSOAS.map(function (p, i) { return { i: i, d: Math.sqrt(Math.pow(p[0] - a, 2) + Math.pow(p[1] - r, 2)) }; });
      var sc = PESSOAS.map(function (p, i) { return { i: i, d: Math.sqrt(Math.pow((p[0] - a) / 52, 2) + Math.pow((p[1] - r) / 230000, 2)) }; });
      function tbl(arr, fmt, cls) {
        var best = arr.reduce(function (m, x) { return x.d < m.d ? x : m; }, arr[0]);
        return '<tr><th>pessoa</th><th class="n">distância</th></tr>' + arr.slice().sort(function (x, y) { return x.d - y.d; }).slice(0, 4).map(function (x) {
          return '<tr class="' + (x.i === best.i ? "dest" : "") + '"><td>' + PESSOAS[x.i][0] + ' anos, R$ ' + E.fmt(PESSOAS[x.i][1]) + '</td><td class="n">' + fmt(x.d) + '</td></tr>'; }).join("");
      }
      el.querySelector(".t0").innerHTML = tbl(raw, function (d) { return E.fmt(d, 0); });
      el.querySelector(".t1").innerHTML = tbl(sc, function (d) { return E.fmt(d, 3); });
      var br = raw.reduce(function (m, x) { return x.d < m.d ? x : m; }), bs = sc.reduce(function (m, x) { return x.d < m.d ? x : m; });
      var pr = PESSOAS[br.i], ps = PESSOAS[bs.i];
      rd.innerHTML = br.i === bs.i ? "Neste ponto os dois métodos escolhem a <b>mesma</b> pessoa (" + pr[0] + " anos). Mexa nos controles até as colunas discordarem." :
        "<b>Sem escala</b> o vizinho é a pessoa de <b>" + pr[0] + " anos</b>; <b>com escala</b> é a de <b>" + ps[0] + " anos</b>. A renda, em milhares, esmagou a idade, em dezenas. Não é que a renda seja mais importante: os números é que são maiores.";
    }
    ea.addEventListener("input", calc); er.addEventListener("input", calc); calc();
  };

  /* ---- calculadora de métricas ---- */
  E.demos.metricas = function (el) {
    var real = [10, 20, 30, 40], prev = [12, 18, 36, 38];
    var h = '<h4>Edite os números e veja as quatro métricas reagirem</h4><div class="tablewrap"><table><tr><th>#</th><th>Real</th><th>Previsto</th><th class="n">Erro</th><th class="n">|Erro|</th><th class="n">Erro²</th></tr>';
    for (var i = 0; i < 4; i++) h += '<tr><td>' + (i + 1) + '</td><td><input type="number" data-r="' + i + '" value="' + real[i] + '" style="width:80px"></td><td><input type="number" data-p="' + i + '" value="' + prev[i] + '" style="width:80px"></td><td class="n e"></td><td class="n a"></td><td class="n q"></td></tr>';
    h += '</table></div><div class="ctrls"><button class="btn sm" type="button" id="mBig">Aumentar um erro</button><button class="btn sm" type="button" id="mRes">Voltar ao exemplo</button></div><div class="kp grid2" style="gap:8px"></div><div class="read"></div>';
    el.innerHTML = h;
    var ins = [].slice.call(el.querySelectorAll("input"));
    function calc() {
      var r = [], p = [];
      ins.forEach(function (x) { var v = parseFloat(x.value); if (x.hasAttribute("data-r")) r[+x.getAttribute("data-r")] = isNaN(v) ? 0 : v; else p[+x.getAttribute("data-p")] = isNaN(v) ? 0 : v; });
      var rows = el.querySelectorAll("tbody tr"), mae = 0, mse = 0, mean = r.reduce(function (a, b) { return a + b; }, 0) / 4, sst = 0;
      for (var i = 0; i < 4; i++) { var e = p[i] - r[i]; mae += Math.abs(e); mse += e * e; sst += Math.pow(r[i] - mean, 2); var tr = rows[i + 1]; tr.querySelector(".e").textContent = E.fmt(e, 1); tr.querySelector(".a").textContent = E.fmt(Math.abs(e), 1); tr.querySelector(".q").textContent = E.fmt(e * e, 1); }
      mae /= 4; mse /= 4; var rmse = Math.sqrt(mse), r2 = sst === 0 ? NaN : 1 - (mse * 4) / sst;
      el.querySelector(".kp").innerHTML = [["MAE", mae, "média dos |erros|"], ["MSE", mse, "média dos erros ao quadrado"], ["RMSE", rmse, "raiz do MSE (volta à unidade original)"], ["R²", r2, "1 = perfeito · 0 = chutar a média"]].map(function (m) {
        return '<div class="card" style="margin:0;padding:10px 14px"><small class="muted">' + m[0] + ' · ' + m[2] + '</small><br><b style="font:700 1.5rem var(--f-head)">' + (isNaN(m[1]) ? "-" : E.fmt(m[1], m[0] === "R²" ? 3 : 2)) + '</b></div>'; }).join("");
      el.querySelector(".read").innerHTML = rmse > mae * 1.25 ? "Repare: o <b>RMSE (" + E.fmt(rmse, 2) + ") ficou bem acima do MAE (" + E.fmt(mae, 2) + ")</b>. Isso acontece quando existe um erro grande e isolado, porque elevar ao quadrado pune muito mais o erro grande." : "RMSE e MAE parecidos: os erros têm tamanhos parecidos entre si. Tente <b>Aumentar um erro</b>.";
    }
    ins.forEach(function (x) { x.addEventListener("input", calc); });
    el.querySelector("#mBig").addEventListener("click", function () { ins[7].value = 10; calc(); });
    el.querySelector("#mRes").addEventListener("click", function () { for (var i = 0; i < 4; i++) { ins[2 * i].value = real[i]; ins[2 * i + 1].value = prev[i]; } calc(); });
    calc();
  };

  /* ---- curva do k (valores reais do scikit-learn) ---- */
  E.demos.kcurve = function (el) {
    var K = D.KCURVE;
    el.innerHTML = '<h4>Erro de treino e de teste conforme o k (valores reais)</h4><canvas></canvas>' +
      '<div class="ctrls"><label>k = <input type="range" min="1" max="40" value="5" id="kc"><output id="kco">5</output></label></div>' +
      '<div class="legend"><span><i style="background:var(--c0)"></i>RMSE no treino</span><span><i style="background:var(--red)"></i>RMSE no teste</span><span><i style="background:var(--green)"></i>RMSE na validação cruzada (treino)</span></div><div class="read"></div>' +
      '<p class="muted" style="font-size:.85rem;margin:8px 0 0">Calculado com o mesmo pipeline do notebook da aula (k de 1 a 40): Insurance, divisão 80/20 com <code>random_state=42</code>, KNN com escala e one-hot, <code>euclidean</code> e <code>uniform</code>.</p>';
    var cv = el.querySelector("canvas"), kEl = el.querySelector("#kc"), rd = el.querySelector(".read");
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = ML.plot(w, h, 1, 40, 0, 8000, { l: 52, r: 12, t: 12, b: 36 });
      ML.axes(ctx, w, h, P, 1, 40, 0, 8000, 5, 2000, "k (número de vizinhos)", "RMSE", c);
      function line(a, col) { ctx.beginPath(); a.forEach(function (v, i) { var X = P.X(i + 1), Y = P.Y(v); if (i) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }); ctx.lineWidth = 3; ctx.strokeStyle = col; ctx.stroke(); }
      line(K.train, c.c0); line(K.test, c.red); line(K.cv, c.green);
      var k = +kEl.value; ctx.strokeStyle = c.ink; ctx.setLineDash([4, 4]); ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(P.X(k), P.pad.t); ctx.lineTo(P.X(k), h - P.pad.b); ctx.stroke(); ctx.setLineDash([]);
      [[K.train, c.c0], [K.test, c.red], [K.cv, c.green]].forEach(function (s) { ctx.beginPath(); ctx.arc(P.X(k), P.Y(s[0][k - 1]), 5.5, 0, 6.2832); ctx.fillStyle = s[1]; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = c.paper; ctx.stroke(); });
    });
    function report() {
      var k = +kEl.value; el.querySelector("#kco").textContent = k;
      var msg = k <= 2 ? "<b>Overfitting.</b> O modelo praticamente decora: erro de treino baixíssimo, e o de teste muito maior. " : (k >= 25 ? "<b>Underfitting.</b> Suave demais: o erro sobe também no treino. " : "Na região do meio, treino e teste ficam mais próximos. ");
      rd.innerHTML = "k = <b>" + k + "</b>: treino <b>" + E.fmt(K.train[k - 1], 0) + "</b> · teste <b>" + E.fmt(K.test[k - 1], 0) + "</b> · validação cruzada <b>" + E.fmt(K.cv[k - 1], 0) + "</b>. " + msg;
    }
    kEl.addEventListener("input", function () { api.paint(); report(); }); report();
  };

  /* ---- holdout x validação cruzada (60 sorteios reais) ---- */
  E.demos.holdout = function (el) {
    el.innerHTML = '<h4>A mesma pergunta, vários sorteios</h4><canvas style="height:220px;cursor:default"></canvas>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" id="h1">Sortear 1</button><button class="btn sm" type="button" id="h10">Sortear 10</button><button class="btn sm" type="button" id="h60">Sortear todos</button><button class="btn sm" type="button" id="h0">Limpar</button></div>' +
      '<div class="legend"><span><i style="background:var(--red)"></i>holdout 80/20 (um corte só)</span><span><i style="background:var(--green)"></i>validação cruzada 5-fold</span></div><div class="read">Cada bolinha é um sorteio diferente (<code>random_state</code> de 0 a 59) para o mesmo KNN com k=5. Sorteie e compare o espalhamento.</div><p class="muted" style="font-size:.85rem;margin:8px 0 0">Como foi calculado: o holdout é <b>um</b> corte de 268 pessoas. A validação cruzada usa as 1.338 pessoas em 5 cortes de 268 e tira a média. Cada ponto de validação cruzada, portanto, já é uma média de 5 provas.</p>';
    var cv = el.querySelector("canvas"), rd = el.querySelector(".read"), n = 0;
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = ML.plot(w, h, 4600, 7200, 0, 1, { l: 150, r: 14, t: 10, b: 36 });
      ctx.save(); ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
      for (var x = 5000; x <= 7000; x += 500) { ctx.beginPath(); ctx.moveTo(P.X(x), 8); ctx.lineTo(P.X(x), h - 32); ctx.stroke(); ctx.fillText(x, P.X(x), h - 18); }
      ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.fillText("RMSE", (P.pad.l + w - P.pad.r) / 2, h - 3); ctx.textAlign = "right";
      ctx.fillText("Holdout", P.pad.l - 10, h * .30); ctx.fillText("Validação cruzada", P.pad.l - 10, h * .66); ctx.restore();
      function row(arr, y, col) { for (var i = 0; i < n; i++) { ctx.beginPath(); ctx.arc(P.X(arr[i]), y + ((i * 37) % 21 - 10) * 1.3, 6, 0, 6.2832); ctx.globalAlpha = .75; ctx.fillStyle = col; ctx.fill(); ctx.globalAlpha = 1; } }
      row(D.HOLD, h * .28, c.red); row(D.CVS, h * .64, c.green);
    });
    function range(a) { var s = a.slice(0, n); return [Math.min.apply(null, s), Math.max.apply(null, s)]; }
    function report() {
      if (!n) { rd.innerHTML = "Cada bolinha é um sorteio diferente (<code>random_state</code> de 0 a 59) para o mesmo KNN com k=5. Sorteie e compare o espalhamento."; return; }
      var a = range(D.HOLD), b = range(D.CVS);
      rd.innerHTML = "Com <b>" + n + "</b> sorteios: o holdout foi de <b>" + E.fmt(a[0], 0) + "</b> a <b>" + E.fmt(a[1], 0) + "</b> (amplitude " + E.fmt(a[1] - a[0], 0) + "). A validação cruzada foi de <b>" + E.fmt(b[0], 0) + "</b> a <b>" + E.fmt(b[1], 0) + "</b> (amplitude " + E.fmt(b[1] - b[0], 0) + ")." + (n >= 30 ? " <b>O mesmo modelo parece muito melhor ou muito pior dependendo da sorte do corte. A média de 5 cortes balança bem menos.</b>" : "");
    }
    function add(m) { n = Math.min(60, n + m); api.paint(); report(); }
    el.querySelector("#h1").addEventListener("click", function () { add(1); }); el.querySelector("#h10").addEventListener("click", function () { add(10); });
    el.querySelector("#h60").addEventListener("click", function () { add(60); }); el.querySelector("#h0").addEventListener("click", function () { n = 0; api.paint(); report(); });
  };

  /* ---- as 5 rodadas da validação cruzada ---- */
  E.demos.folds = function (el) {
    var vals = [5.6, 6.4, 5.9, 6.1, 5.7];
    el.innerHTML = '<h4>Cinco rodadas, cada pedaço valida uma vez</h4><div class="ctrls" id="fb"></div><div class="folds2" style="display:flex;gap:6px;margin:8px 0"></div><div class="read"></div>';
    var box = el.querySelector(".folds2"), rd = el.querySelector(".read"), fb = el.querySelector("#fb"), cur = 0, seen = [true, false, false, false, false];
    for (var i = 0; i < 5; i++) { var b = document.createElement("button"); b.className = "btn sm" + (i ? "" : " pri"); b.type = "button"; b.textContent = "Rodada " + (i + 1); b.setAttribute("data-i", i); fb.appendChild(b); }
    function draw() {
      box.innerHTML = vals.map(function (_, i) { var v = i === cur; return '<div style="flex:1;text-align:center;padding:16px 0;border-radius:10px;border:2px solid ' + (v ? "var(--amber)" : "var(--line)") + ';background:' + (v ? "var(--amber-soft)" : "var(--paper-2)") + ';font-weight:' + (v ? 700 : 500) + ';transition:.3s;font-size:.85rem">' + (v ? "VALIDA" : "treina") + '<br><small class="muted">pedaço ' + (i + 1) + '</small></div>'; }).join("");
      seen[cur] = true;
      var done = vals.map(function (v, i) { return seen[i] ? v : null; }).filter(function (v) { return v !== null; }), n = done.length, m = done.reduce(function (x, y) { return x + y; }, 0) / n;
      rd.innerHTML = "Rodada <b>" + (cur + 1) + "</b>: o pedaço " + (cur + 1) + " fica de fora, o modelo treina nos outros 4 e é medido nele. RMSE das rodadas que você já viu (valores <i>ilustrativos</i>): " + done.map(function (v) { return E.fmt(v * 1000, 0); }).join(" · ") + ". " + (n === 5 ? "<b>Média das 5: " + E.fmt(m * 1000, 0) + "</b>. Esse é o RMSE da validação cruzada." : "Passe pelas outras rodadas (faltam " + (5 - n) + ") para fechar a média.");
      fb.querySelectorAll("button").forEach(function (b, i) { b.classList.toggle("pri", i === cur); });
    }
    fb.addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; cur = +b.getAttribute("data-i"); draw(); }); draw();
  };

  /* ---- GridSearchCV: 80 combinações com RMSE reais ---- */
  E.demos.grid = function (el) {
    var G = D.GRID, keys = ["euclidean|uniform", "euclidean|distance", "manhattan|uniform", "manhattan|distance"], names = ["euclidean · uniform", "euclidean · distance", "manhattan · uniform", "manhattan · distance"];
    var all = []; keys.forEach(function (k) { G[k].forEach(function (v) { all.push(v); }); });
    var mn = Math.min.apply(null, all), mx = Math.max.apply(null, all), best = { r: 0, k: 0 };
    keys.forEach(function (k, r) { G[k].forEach(function (v, i) { if (v === mn) best = { r: r, k: i }; }); });
    var h = '<h4>As 80 combinações da aula, com o RMSE real de cada uma</h4><div class="ctrls"><button class="btn sm pri" type="button" id="gRun">Rodar a busca ▶</button><span class="muted" id="gCnt">0 de 400 treinos</span></div>';
    h += '<div style="overflow-x:auto"><div style="min-width:560px">';
    keys.forEach(function (k, r) { h += '<div style="display:grid;grid-template-columns:150px 1fr;gap:8px;align-items:center;margin:4px 0"><span style="font-size:.8rem" class="muted">' + names[r] + '</span><div class="hm" style="grid-template-columns:repeat(20,1fr)" data-r="' + r + '"></div></div>'; });
    h += '<div style="display:grid;grid-template-columns:150px 1fr;gap:8px"><span></span><div style="display:grid;grid-template-columns:repeat(20,1fr);gap:3px;font-size:.62rem;text-align:center" class="muted">';
    for (var i = 1; i <= 20; i++) h += '<span>' + i + '</span>'; h += '</div></div></div></div>';
    h += '<p class="muted" style="font-size:.82rem;margin:4px 0 0">Colunas: k de 1 a 20. Cada quadrado é uma combinação, treinada 5 vezes (<code>cv=5</code>). Verde = RMSE menor.</p><div class="read">Passe o mouse (ou toque) em um quadrado, ou clique em "Rodar a busca".</div>';
    el.innerHTML = h;
    var cells = [], rd = el.querySelector(".read"), cnt = el.querySelector("#gCnt");
    el.querySelectorAll(".hm").forEach(function (row, r) {
      G[keys[r]].forEach(function (v, i) {
        var c = document.createElement("div"); c.className = "cell"; c.tabIndex = 0; var t = (v - mn) / (mx - mn);
        c.style.background = "color-mix(in srgb, var(--green) " + Math.round((1 - t) * 100) + "%, var(--red))"; c.style.opacity = "1"; c.setAttribute("data-r", r); c.setAttribute("data-i", i);
        c.title = names[r] + ", k=" + (i + 1) + ": RMSE " + E.fmt(v, 1); row.appendChild(c); cells.push(c);
      });
    });
    function info(c) { var r = +c.getAttribute("data-r"), i = +c.getAttribute("data-i"); rd.innerHTML = "<b>" + names[r] + ", k = " + (i + 1) + "</b>: RMSE médio na validação cruzada = <b>" + E.fmt(G[keys[r]][i], 1) + "</b>" + (r === best.r && i === best.k ? " <b style='color:var(--green)'>← a melhor das 80</b>" : ""); }
    el.addEventListener("mouseover", function (e) { var c = e.target.closest(".cell"); if (c) info(c); });
    el.addEventListener("focusin", function (e) { var c = e.target.closest(".cell"); if (c) info(c); });
    el.addEventListener("click", function (e) { var c = e.target.closest(".cell"); if (c) info(c); });
    var gTok = 0;
    el.querySelector("#gRun").addEventListener("click", function () {
      var tok = ++gTok;
      cells.forEach(function (c) { c.style.opacity = ".12"; c.classList.remove("best"); }); cnt.textContent = "0 de 400 treinos";
      var n = 0, order = cells.slice();
      (function tick() {
        if (tok !== gTok) return;
        if (n >= order.length) { cells[best.r * 20 + best.k].classList.add("best"); cnt.innerHTML = "<b>400 de 400 treinos</b>"; rd.innerHTML = "Fim da busca. Melhor combinação: <b>manhattan, distance, k = " + (best.k + 1) + "</b>, com RMSE médio de <b>" + E.fmt(mn, 1) + "</b> na validação cruzada. É exatamente o que o <code>GridSearchCV</code> da aula devolveu."; return; }
        var batch = E.reduce ? 80 : 2; for (var b = 0; b < batch && n < order.length; b++, n++) order[n].style.opacity = "1";
        cnt.textContent = (n * 5) + " de 400 treinos"; setTimeout(tick, E.reduce ? 0 : 55);
      })();
    });
  };

  /* ---- placar final ---- */
  E.demos.placar = function (el) {
    var R = D.REF;
    el.innerHTML = '<div class="tablewrap"><table><tr><th>Modelo</th><th class="n">MAE</th><th class="n">MSE</th><th class="n">RMSE</th><th class="n">R²</th></tr>' +
      '<tr><td>Baseline (k=5, uniform, euclidean)</td><td class="n">' + E.fmt(R.baseline.MAE, 2) + '</td><td class="n">' + (R.baseline.MSE / 1e7).toFixed(3).replace(".", ",") + 'e7</td><td class="n">' + E.fmt(R.baseline.RMSE, 2) + '</td><td class="n">' + E.fmt(R.baseline.R2, 4) + '</td></tr>' +
      '<tr class="dest"><td>KNN tunado (manhattan, k=7, distance)</td><td class="n">' + E.fmt(R.tunado.MAE, 2) + '</td><td class="n">' + (R.tunado.MSE / 1e7).toFixed(3).replace(".", ",") + 'e7</td><td class="n">' + E.fmt(R.tunado.RMSE, 2) + '</td><td class="n">' + E.fmt(R.tunado.R2, 4) + '</td></tr></table></div>';
  };
})();
