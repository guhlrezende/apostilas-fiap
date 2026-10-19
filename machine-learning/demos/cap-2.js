/* Demos do capítulo 2: Mitchell, pombos, treino/teste e KNN no Iris */
(function () {
  var E = window.Estudo, ML = window.ML, D = ML.D;

  /* ---- Mitchell: E, T e P ---- */
  var EX = {
    iris: { nome: "Iris + KNN", E: "As 150 flores já medidas e com a espécie anotada (as de treino).", T: "Dizer a espécie de uma flor nova a partir das medidas das pétalas e sépalas.", P: "Acurácia: a porcentagem de flores novas em que a espécie prevista está certa.", m: "Se a acurácia sobe quando damos mais flores de exemplo, o programa está aprendendo." },
    spam: { nome: "Filtro de spam", E: "Milhares de e-mails que já foram marcados como spam ou não spam.", T: "Classificar um e-mail novo.", P: "Taxa de e-mails classificados corretamente (e, na prática, quantos bons foram parar no lixo).", m: "Se o filtro erra menos conforme vê mais e-mails marcados, ele aprende." },
    seguro: { nome: "Custo do seguro", E: "As 1.338 pessoas com os dados e o custo real de cada uma.", T: "Prever o custo de uma pessoa nova.", P: "Erro médio (MAE e RMSE) e R², medidos em pessoas que o modelo não viu no treino.", m: "Se o erro cai quando melhoramos os dados e o modelo, houve aprendizado de verdade." }
  };
  E.demos.mitchell = function (el) {
    var h = '<h4>Escolha um problema e preencha E, T e P</h4><div class="ctrls">';
    Object.keys(EX).forEach(function (k, i) { h += '<button type="button" class="btn sm' + (i === 0 ? ' pri' : '') + '" data-k="' + k + '">' + EX[k].nome + '</button>'; });
    h += '</div><div class="grid3 mit"></div><div class="read mitm"></div>';
    el.innerHTML = h;
    function show(k) {
      var x = EX[k];
      el.querySelector(".mit").innerHTML =
        '<div class="card" style="margin:0"><b style="color:var(--c0)">E · experiência</b><p>' + x.E + '</p></div>' +
        '<div class="card" style="margin:0"><b style="color:var(--c1)">T · tarefa</b><p>' + x.T + '</p></div>' +
        '<div class="card" style="margin:0"><b style="color:var(--c2)">P · desempenho</b><p>' + x.P + '</p></div>';
      el.querySelector(".mitm").innerHTML = "<b>Aprendeu?</b> " + x.m;
      el.querySelectorAll("button[data-k]").forEach(function (b) { b.classList.toggle("pri", b.getAttribute("data-k") === k); });
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-k]"); if (b) show(b.getAttribute("data-k")); });
    show("iris");
  };

  /* ---- pombos ---- */
  E.demos.pombos = function (el) {
    el.innerHTML = '<h4>Os pombos e as pinturas</h4><p class="muted" style="margin:.2em 0 .8em">Acerto dos pombos ao diferenciar os dois artistas (números do slide da aula). A barra vermelha é um memorizador <i>hipotético</i>, só para comparar.</p>' +
      '<div class="bars">' +
      '<div class="bar" data-w="95"><div>Pinturas já vistas (treino)</div><div class="tr"><div class="fl"></div></div><div class="v">95%</div></div>' +
      '<div class="bar best" data-w="85"><div>Pinturas novas (teste)</div><div class="tr"><div class="fl"></div></div><div class="v">85%</div></div>' +
      '<div class="bar bad" data-w="50"><div>Memorizador no teste (chute)</div><div class="tr"><div class="fl"></div></div><div class="v">~50%</div></div>' +
      '</div><div class="read" id="pomMsg">Clique em "Reproduzir" e compare as barras.</div>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" id="pomBtn">Reproduzir ↺</button></div>';
    var bars = el.querySelectorAll(".bar");
    function run() {
      bars.forEach(function (b) { b.querySelector(".fl").style.width = "0%"; });
      setTimeout(function () { bars.forEach(function (b, i) { setTimeout(function () { b.querySelector(".fl").style.width = b.getAttribute("data-w") + "%"; }, i * 500); }); }, 60);
      el.querySelector("#pomMsg").innerHTML = "Cair de <b>95%</b> para <b>85%</b> é normal: é a distância entre o que você estudou e a prova. O que importa é ainda acertar a maioria no que <b>nunca viu</b>. Um memorizador cairia para o chute (com 2 artistas, cerca de 50%).";
    }
    el.querySelector("#pomBtn").addEventListener("click", run);
    E.onView(el, run, .3);
  };

  /* ---- divisão treino/teste ---- */
  E.demos.split = function (el) {
    var N = 150, nTest = 45, nTrain = 105;
    el.innerHTML = '<h4>150 flores, uma bolinha cada</h4><canvas style="height:300px;cursor:default"></canvas>' +
      '<div class="ctrls"><button class="btn sm" type="button" data-m="seq">Separar 70/30 sem embaralhar</button><button class="btn sm pri" type="button" data-m="emb">Embaralhar e separar</button><button class="btn sm" type="button" data-m="ini">Voltar</button></div>' +
      '<div class="legend"><span><i style="background:var(--c0)"></i>setosa</span><span><i style="background:var(--c1)"></i>versicolor</span><span><i style="background:var(--c2)"></i>virginica</span></div>' +
      '<div class="read"></div>';
    var cv = el.querySelector("canvas"), rd = el.querySelector(".read");
    var pos = [], tgt = [], cls = D.IRIS.map(function (r) { return r[4]; }), isTest = new Array(N).fill(false), mode = "ini", raf = 0, rseed = 3;
    var W = 0, H = 0;
    function grid(ids, x0, y0, w, h) {
      var n = ids.length, cols = Math.max(1, Math.round(Math.sqrt(n * w / h))), rows = Math.ceil(n / cols), dx = w / cols, dy = h / rows;
      ids.forEach(function (id, j) { tgt[id] = { x: x0 + dx * (j % cols) + dx / 2, y: y0 + dy * Math.floor(j / cols) + dy / 2 }; });
    }
    function layout() {
      if (!W) return;
      var all = []; for (var i = 0; i < N; i++) all.push(i);
      if (mode === "ini") { grid(all, 20, 36, W - 40, H - 60); return; }
      var tr = all.filter(function (i) { return !isTest[i]; }), te = all.filter(function (i) { return isTest[i]; });
      var cut = Math.round(W * 0.66);
      grid(tr, 16, 46, cut - 28, H - 70); grid(te, cut + 12, 46, W - cut - 28, H - 70);
    }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      if (w !== W || h !== H) { W = w; H = h; layout(); pos = tgt.map(function (t) { return { x: t.x, y: t.y }; }); }
      ctx.font = "700 12px Inter,system-ui,sans-serif"; ctx.textAlign = "left";
      if (mode === "ini") { ctx.fillStyle = c.ink; ctx.fillText("Dados na ordem do arquivo: 50 setosa, depois 50 versicolor, depois 50 virginica", 16, 22); }
      else {
        var cut = Math.round(w * 0.66);
        ctx.fillStyle = c.pen; ctx.fillText("TREINO (105 flores, 70%)", 16, 24); ctx.fillStyle = c.red; ctx.fillText("TESTE (45 flores, 30%)", cut + 12, 24);
        ctx.strokeStyle = c.line; ctx.setLineDash([5, 5]); ctx.beginPath(); ctx.moveTo(cut, 8); ctx.lineTo(cut, h - 8); ctx.stroke(); ctx.setLineDash([]);
      }
      for (var i = 0; i < N; i++) {
        var p = pos[i]; if (!p) continue;
        ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, 6.2832); ctx.fillStyle = ML.classCol(c, cls[i]); ctx.fill();
        if (mode !== "ini" && isTest[i]) { ctx.lineWidth = 2; ctx.strokeStyle = c.ink; ctx.stroke(); }
      }
    });
    function step() {
      var moving = false;
      for (var i = 0; i < N; i++) { var p = pos[i], t = tgt[i]; if (!p || !t) continue; var dx = t.x - p.x, dy = t.y - p.y; if (Math.abs(dx) + Math.abs(dy) > .4) { p.x += dx * .16; p.y += dy * .16; moving = true; } else { p.x = t.x; p.y = t.y; } }
      api.paint(); if (moving) raf = requestAnimationFrame(step);
    }
    function go() { layout(); cancelAnimationFrame(raf); if (E.reduce) { pos = tgt.map(function (t) { return { x: t.x, y: t.y }; }); api.paint(); } else step(); }
    function count(test) { var c = [0, 0, 0]; for (var i = 0; i < N; i++) if (isTest[i] === test) c[cls[i]]++; return c; }
    function report() {
      if (mode === "ini") { rd.innerHTML = "Escolha como separar. Repare que as flores estão <b>ordenadas por espécie</b>."; return; }
      var a = count(false), b = count(true);
      rd.innerHTML = "<b>Treino</b>: " + a[0] + " setosa, " + a[1] + " versicolor, " + a[2] + " virginica. <b>Teste</b>: " + b[0] + " setosa, " + b[1] + " versicolor, " + b[2] + " virginica." +
        (mode === "seq" ? "<br><b style='color:var(--red)'>Problema:</b> o teste só tem virginica, e o treino quase não vê essa espécie (só 5 de 105). O modelo nunca seria cobrado sobre setosa e versicolor, e a nota não significaria nada." : "<br><b style='color:var(--green)'>Melhor:</b> as três espécies aparecem nos dois lados. É isso que o <code>train_test_split</code> faz ao embaralhar antes de separar.");
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-m]"); if (!b) return; mode = b.getAttribute("data-m");
      isTest.fill(false);
      if (mode === "seq") { for (var i = N - nTest; i < N; i++) isTest[i] = true; }
      if (mode === "emb") { var ids = ML.shuffle(Array.apply(null, { length: N }).map(function (_, i) { return i; }), ML.rng(rseed++)); for (var j = 0; j < nTest; j++) isTest[ids[j]] = true; }
      go(); report();
    });
    report();
  };

  /* ---- KNN classificando flores (Iris real, 2 medidas) ---- */
  E.demos.knnIris = function (el) {
    el.innerHTML = '<h4>Coloque uma flor nova e veja os vizinhos votarem</h4><canvas></canvas>' +
      '<div class="ctrls"><label>k = <input type="range" min="1" max="25" value="5" id="kk"><output id="kko">5</output></label>' +
      '<label><input type="checkbox" id="reg" checked> mostrar o mapa de decisão</label></div>' +
      '<div class="legend"><span><i style="background:var(--c0)"></i>setosa</span><span><i style="background:var(--c1)"></i>versicolor</span><span><i style="background:var(--c2)"></i>virginica</span><span>▲ = flor nova</span></div>' +
      '<div class="read">Clique ou arraste no gráfico para colocar uma flor nova.</div>' +
      '<p class="muted" style="font-size:.85rem;margin:8px 0 0">Aqui uso só <b>comprimento e largura da pétala</b>, para caber num plano. O notebook usa as 4 medidas. Em caso de empate, esta demo escolhe a classe do vizinho mais próximo.</p>';
    var cv = el.querySelector("canvas"), rd = el.querySelector(".read"), kk = el.querySelector("#kk"), reg = el.querySelector("#reg");
    var pts = D.IRIS.map(function (r) { return { x: [r[0], r[1]], y: r[4] }; });
    var q = null, X0 = 0.8, X1 = 7.2, Y0 = 0, Y1 = 2.7, cache = null, cacheKey = "";
    function classify(x, y, k) { var n = ML.vizinhos(pts, [x, y], k); var v = ML.votar(n, 3); var mx = Math.max.apply(null, v.votos), tie = v.votos.filter(function (a) { return a === mx; }).length > 1; return { n: n, v: v, cls: tie ? n[0].y : v.classe, tie: tie }; }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var P = ML.plot(w, h, X0, X1, Y0, Y1);
      var k = +kk.value;
      if (reg.checked) {
        var key = [w, h, k].join("|");
        if (key !== cacheKey) { cacheKey = key; cache = []; var st = 7; for (var px = P.pad.l; px < w - P.pad.r; px += st) for (var py = P.pad.t; py < h - P.pad.b; py += st) cache.push([px, py, classify(P.ix(px + st / 2), P.iy(py + st / 2), k).cls]); }
        ctx.globalAlpha = .16; cache.forEach(function (r) { ctx.fillStyle = ML.classCol(c, r[2]); ctx.fillRect(r[0], r[1], 7, 7); }); ctx.globalAlpha = 1;
      }
      ML.axes(ctx, w, h, P, X0, X1, Y0, Y1, 1, .5, "comprimento da pétala (cm)", "largura da pétala (cm)", c);
      pts.forEach(function (p, i) { ctx.beginPath(); ctx.arc(P.X(p.x[0]) + (i % 3 - 1) * .8, P.Y(p.x[1]), 4.6, 0, 6.2832); ctx.fillStyle = ML.classCol(c, p.y); ctx.globalAlpha = .85; ctx.fill(); ctx.globalAlpha = 1; ctx.lineWidth = 1; ctx.strokeStyle = c.paper; ctx.stroke(); });
      if (q) {
        var r = classify(q.x, q.y, k);
        ctx.strokeStyle = c.ink; ctx.lineWidth = 1.2; ctx.setLineDash([3, 3]);
        r.n.forEach(function (n) { ctx.beginPath(); ctx.moveTo(P.X(q.x), P.Y(q.y)); ctx.lineTo(P.X(pts[n.i].x[0]), P.Y(pts[n.i].x[1])); ctx.stroke(); });
        ctx.setLineDash([]);
        r.n.forEach(function (n) { ctx.beginPath(); ctx.arc(P.X(pts[n.i].x[0]), P.Y(pts[n.i].x[1]), 8, 0, 6.2832); ctx.lineWidth = 2.5; ctx.strokeStyle = c.ink; ctx.stroke(); });
        var X = P.X(q.x), Y = P.Y(q.y); ctx.beginPath(); ctx.moveTo(X, Y - 11); ctx.lineTo(X + 10, Y + 8); ctx.lineTo(X - 10, Y + 8); ctx.closePath();
        ctx.fillStyle = ML.classCol(c, r.cls); ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = c.ink; ctx.stroke();
      }
      cv._P = P;
    });
    function report() {
      el.querySelector("#kko").textContent = kk.value;
      if (!q) return;
      var k = +kk.value, r = classify(q.x, q.y, k), v = r.v.votos;
      rd.innerHTML = "Flor nova: pétala <b>" + q.x.toFixed(1) + " × " + q.y.toFixed(1) + " cm</b>. Votos dos " + k + " vizinhos: " +
        '<b style="color:var(--c0)">setosa ' + v[0] + '</b> · <b style="color:var(--c1)">versicolor ' + v[1] + '</b> · <b style="color:var(--c2)">virginica ' + v[2] + '</b>. ' +
        "Previsão: <b>" + ML.NOMES[r.cls] + "</b>" + (r.tie ? " (empate, decidiu o vizinho mais próximo)" : "") + ". Vizinho mais próximo a " + r.n[0].d.toFixed(2) + " cm.";
    }
    E.pointer(cv, function (x, y) { place(x, y); }, function (x, y) { place(x, y); });
    function place(px, py) { var P = cv._P; if (!P) return; q = { x: Math.min(X1, Math.max(X0, P.ix(px))), y: Math.min(Y1, Math.max(Y0, P.iy(py))) }; api.paint(); report(); }
    kk.addEventListener("input", function () { api.paint(); report(); }); reg.addEventListener("change", function () { api.paint(); });
  };
})();
