/* Demos do capítulo 4: OneHot, scalers, vazamento (Insurance real) */
(function () {
  var E = window.Estudo, ML = window.ML, D = ML.D, INS = D.INS;

  /* ---- OneHotEncoder: 3 colunas viram 8 ---- */
  E.demos.onehot = function (el) {
    var cols = [["sex", ["female", "male"]], ["smoker", ["no", "yes"]], ["region", ["northeast", "northwest", "southeast", "southwest"]]];
    var h = '<h4>Monte uma pessoa e veja as 8 colunas acenderem</h4><div class="ctrls">';
    cols.forEach(function (c) { h += '<label>' + c[0] + ' <select data-c="' + c[0] + '">' + c[1].map(function (v) { return '<option>' + v + '</option>'; }).join("") + '</select></label>'; });
    h += '</div><div class="oh" style="display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin:10px 0"></div><div class="read"></div>';
    el.innerHTML = h;
    var box = el.querySelector(".oh"), rd = el.querySelector(".read"), sel = {};
    el.querySelectorAll("select").forEach(function (s) { sel[s.getAttribute("data-c")] = s; s.addEventListener("change", draw); });
    sel.smoker.value = "yes"; sel.region.value = "southwest"; sel.sex.value = "female";
    function draw() {
      var vec = [], html = "";
      cols.forEach(function (c) { c[1].forEach(function (v) { var on = sel[c[0]].value === v; vec.push(on ? 1 : 0); html += '<div style="padding:10px 2px;text-align:center;border-radius:10px;border:2px solid ' + (on ? "var(--green)" : "var(--line)") + ';background:' + (on ? "var(--green-soft)" : "var(--paper-2)") + ';transition:.3s;transform:' + (on ? "translateY(-4px)" : "none") + '"><small class="muted" style="display:block;font-size:.66rem;word-break:break-all">' + c[0] + '_' + v + '</small><b style="font:700 1.5rem var(--f-head)">' + (on ? 1 : 0) + '</b></div>'; }); });
      box.innerHTML = html;
      rd.innerHTML = "Vetor desta pessoa: <b style='font-family:var(--f-mono)'>[" + vec.join(", ") + "]</b>. As <b>3 colunas de texto</b> (2 + 2 + 4 categorias) viraram <b>8 colunas</b> de 0 e 1, e em cada grupo exatamente <b>uma</b> está ligada.";
    }
    draw();
  };

  /* ---- os três scalers ---- */
  function stats(arr) {
    var a = arr.slice().sort(function (x, y) { return x - y; }), n = a.length, mean = a.reduce(function (s, v) { return s + v; }, 0) / n;
    var sd = Math.sqrt(a.reduce(function (s, v) { return s + (v - mean) * (v - mean); }, 0) / n);
    function q(p) { var pos = (n - 1) * p, lo = Math.floor(pos), f = pos - lo; return a[lo] + (a[Math.min(n - 1, lo + 1)] - a[lo]) * f; }
    return { min: a[0], max: a[n - 1], mean: mean, sd: sd, med: q(.5), q1: q(.25), q3: q(.75), a: a };
  }
  E.demos.scalers = function (el) {
    var COLS = { age: { i: 0, lbl: "age (idade)", step: 1, dec: 0 }, bmi: { i: 1, lbl: "bmi (IMC)", step: .1, dec: 2 }, children: { i: 2, lbl: "children (filhos)", step: 1, dec: 0 } };
    var S = {}; Object.keys(COLS).forEach(function (k) { S[k] = stats(INS.map(function (r) { return r[COLS[k].i]; })); });
    el.innerHTML = '<h4>Um valor, três réguas (colunas reais do Insurance)</h4>' +
      '<div class="ctrls"><label>coluna <select id="sc">' + Object.keys(COLS).map(function (k) { return '<option value="' + k + '">' + COLS[k].lbl + '</option>'; }).join("") + '</select></label>' +
      '<label>valor <input type="range" id="sv"><output id="svo"></output></label></div><canvas style="height:150px;cursor:default"></canvas>' +
      '<div class="tablewrap"><table><tr><th>Scaler</th><th>Conta</th><th class="n">Resultado</th></tr><tr><td><b>MinMax</b></td><td class="c0"></td><td class="n r0"></td></tr><tr><td><b>Standard</b></td><td class="c1"></td><td class="n r1"></td></tr><tr><td><b>Robust</b></td><td class="c2"></td><td class="n r2"></td></tr></table></div>' +
      '<div class="read st"></div>';
    var sc = el.querySelector("#sc"), sv = el.querySelector("#sv"), svo = el.querySelector("#svo"), cv = el.querySelector("canvas");
    function cfg() { var k = sc.value, s = S[k], c = COLS[k]; sv.min = s.min; sv.max = s.max; sv.step = c.step; if (+sv.value < s.min || +sv.value > s.max || cv._k !== k) sv.value = k === "age" ? 19 : (k === "bmi" ? 30 : 2); cv._k = k; }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var k = sc.value, s = S[k], bins = k === "children" ? 6 : 24, lo = k === "children" ? -.5 : s.min, hi = k === "children" ? 5.5 : s.max + 1e-9, cnt = new Array(bins).fill(0);
      s.a.forEach(function (v) { var b = Math.min(bins - 1, Math.floor((v - lo) / (hi - lo) * bins)); cnt[b]++; });
      var mx = Math.max.apply(null, cnt), pl = 10, pr = 10, bw = (w - pl - pr) / bins;
      cnt.forEach(function (n, i) { var bh = n / mx * (h - 38); ctx.fillStyle = c.hlB; ctx.fillRect(pl + i * bw + 1, h - 22 - bh, bw - 2, bh); });
      var X = function (v) { return pl + (v - lo) / (hi - lo) * (w - pl - pr); };
      ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center"; ctx.fillText(E.fmt(s.min, COLS[k].dec), X(s.min + (k === "children" ? 0 : 0)) + (k === "children" ? bw / 2 : 4), h - 6); ctx.fillText(E.fmt(s.max, COLS[k].dec), X(s.max) - (k === "children" ? bw / 2 : 8), h - 6);
      var v = +sv.value, x = X(k === "children" ? v + .5 - .5 + .0 : v) + (k === "children" ? bw / 2 - bw / 2 : 0);
      ctx.strokeStyle = c.red; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, 6); ctx.lineTo(x, h - 22); ctx.stroke();
      ctx.fillStyle = c.red; ctx.beginPath(); ctx.arc(x, 8, 5, 0, 6.2832); ctx.fill();
      [["mediana", s.med], ["Q1", s.q1], ["Q3", s.q3]].forEach(function (m) { ctx.strokeStyle = c.muted; ctx.setLineDash([3, 3]); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(X(m[1]), 14); ctx.lineTo(X(m[1]), h - 22); ctx.stroke(); ctx.setLineDash([]); });
    });
    function calc() {
      var k = sc.value, s = S[k], c = COLS[k], v = +sv.value, d = c.dec;
      svo.textContent = E.fmt(v, d);
      var mm = (v - s.min) / (s.max - s.min), z = (v - s.mean) / s.sd, rb = (v - s.med) / (s.q3 - s.q1), f = function (x, n) { return E.fmt(x, n == null ? d : n); };
      el.querySelector(".c0").innerHTML = "(" + f(v) + " − " + f(s.min) + ") ÷ (" + f(s.max) + " − " + f(s.min) + ")";
      el.querySelector(".c1").innerHTML = "(" + f(v) + " − " + f(s.mean, 3) + ") ÷ " + f(s.sd, 3);
      el.querySelector(".c2").innerHTML = "(" + f(v) + " − " + f(s.med) + ") ÷ (" + f(s.q3) + " − " + f(s.q1) + ")";
      el.querySelector(".r0").innerHTML = "<b>" + E.fmt(mm, 4) + "</b>"; el.querySelector(".r1").innerHTML = "<b>" + E.fmt(z, 4) + "</b>"; el.querySelector(".r2").innerHTML = "<b>" + E.fmt(rb, 4) + "</b>";
      el.querySelector(".st").innerHTML = "Estatísticas reais da coluna: mín " + f(s.min) + ", máx " + f(s.max) + ", média " + f(s.mean, 3) + ", desvio (populacional) " + f(s.sd, 3) + ", mediana " + f(s.med) + ", Q1 " + f(s.q1) + ", Q3 " + f(s.q3) + "." + (k === "age" && +sv.value === 19 ? " <b>Para age = 19 você deve ver 0,0217 · −1,4388 · −0,8333.</b>" : "");
      api.paint();
    }
    sc.addEventListener("change", function () { cfg(); calc(); }); sv.addEventListener("input", calc); cfg(); calc();
  };

  /* ---- o que um outlier faz com cada scaler ---- */
  E.demos.outlier = function (el) {
    var base = [20, 22, 25, 27, 30, 32, 35, 38, 40, 42];
    el.innerHTML = '<h4>Adicione um valor extremo e veja os scalers reagirem</h4><div class="ctrls"><label>valor extra <input type="range" id="ov" min="45" max="400" value="150" step="5"><output id="ovo">150</output></label></div>' +
      '<p class="muted" style="margin:.2em 0">Base (10 valores): ' + base.join(", ") + '. O valor extra entra como 11º. Abaixo, o que acontece com o valor <b>30</b>.</p>' +
      '<div class="bars"><div class="bar" data-w="0"><div>MinMax (0 a 1)</div><div class="tr"><div class="fl" style="transition:width .3s"></div></div><div class="v">-</div></div><div class="bar" data-w="0"><div>Robust (mediana 0)</div><div class="tr"><div class="fl" style="transition:width .3s"></div></div><div class="v">-</div></div></div><div class="read"></div>';
    var ov = el.querySelector("#ov"), bars = el.querySelectorAll(".bar"), rd = el.querySelector(".read");
    function calc() {
      var x = +ov.value; el.querySelector("#ovo").textContent = x; var a = base.concat([x]), s = stats(a);
      var mm = (30 - s.min) / (s.max - s.min), rb = (30 - s.med) / (s.q3 - s.q1);
      var mm0 = (30 - 20) / (42 - 20);
      bars[0].querySelector(".fl").style.width = Math.max(1, mm * 100) + "%"; bars[0].querySelector(".v").textContent = E.fmt(mm, 3);
      var rn = Math.min(100, Math.abs(rb) * 100); bars[1].querySelector(".fl").style.width = Math.max(1, rn) + "%"; bars[1].querySelector(".v").textContent = E.fmt(rb, 3);
      rd.innerHTML = "Sem o valor extra, o 30 valia <b>" + E.fmt(mm0, 3) + "</b> no MinMax. Com " + x + ", vale <b>" + E.fmt(mm, 3) + "</b>: o MinMax <b>amassa</b> todo mundo perto de zero porque o máximo foi puxado. O Robust usa mediana e quartis, que quase não se mexem com um valor só: " + E.fmt(rb, 3) + ".";
    }
    ov.addEventListener("input", calc); calc();
  };

  /* ---- desvio amostral (Excel) x populacional (scikit-learn) ---- */
  E.demos.desvio = function (el) {
    el.innerHTML = '<h4>Por que o Excel e o scikit-learn discordam?</h4><p class="muted" style="margin:.2em 0">Dez rendas <i>ilustrativas</i> (edite à vontade, separadas por vírgula):</p>' +
      '<input type="text" id="dv" value="40000, 60000, 120000, 90000, 250000, 130000, 200000, 30000, 80000, 260000" style="width:100%;font-family:var(--f-mono)">' +
      '<div class="tablewrap"><table><tr><th></th><th class="n">Desvio</th><th class="n">Padronizado do 1º valor</th></tr><tr><td><b>Excel</b> (<code>STDEV.S</code>, divide por n − 1)</td><td class="n a"></td><td class="n b"></td></tr><tr><td><b>scikit-learn</b> (divide por n)</td><td class="n c"></td><td class="n d"></td></tr></table></div><div class="read"></div>';
    var inp = el.querySelector("#dv");
    function calc() {
      var v = inp.value.split(",").map(function (s) { return parseFloat(s.trim()); }).filter(function (x) { return !isNaN(x); }), n = v.length;
      if (n < 2) { el.querySelector(".read").textContent = "Digite pelo menos 2 números."; return; }
      var m = v.reduce(function (a, b) { return a + b; }, 0) / n, ss = v.reduce(function (a, b) { return a + (b - m) * (b - m); }, 0), s1 = Math.sqrt(ss / (n - 1)), s0 = Math.sqrt(ss / n);
      el.querySelector(".a").textContent = E.fmt(s1, 2); el.querySelector(".b").textContent = E.fmt((v[0] - m) / s1, 4); el.querySelector(".c").textContent = E.fmt(s0, 2); el.querySelector(".d").textContent = E.fmt((v[0] - m) / s0, 4);
      el.querySelector(".read").innerHTML = "Com <b>n = " + n + "</b> a diferença aparece (a razão entre os dois é √(n/(n−1)) = " + E.fmt(Math.sqrt(n / (n - 1)), 4) + "). Quanto mais linhas, menor ela fica. No Insurance (1.338 linhas), é desprezível.";
    }
    inp.addEventListener("input", calc); calc();
  };

  /* ---- balança: quanto pesa cada coluna na distância (após MinMax) ---- */
  E.demos.peso = function (el) {
    var A = stats(INS.map(function (r) { return r[0]; })), B = stats(INS.map(function (r) { return r[1]; })), C = stats(INS.map(function (r) { return r[2]; }));
    el.innerHTML = '<h4>Duas pessoas. O que as deixa mais "distantes" para o KNN?</h4>' +
      '<div class="ctrls"><label>diferença de idade <input type="range" id="pa" min="0" max="46" value="10"><output id="pao">10 anos</output></label>' +
      '<label>diferença de IMC <input type="range" id="pb" min="0" max="37" value="5"><output id="pbo">5</output></label>' +
      '<label>diferença de filhos <input type="range" id="pc" min="0" max="5" value="1"><output id="pco">1</output></label>' +
      '<label><input type="checkbox" id="pf"> um fuma e o outro não</label></div>' +
      '<div class="bars"><div class="bar" data-w="0"><div>idade</div><div class="tr"><div class="fl" style="transition:width .25s"></div></div><div class="v"></div></div><div class="bar" data-w="0"><div>IMC</div><div class="tr"><div class="fl" style="transition:width .25s"></div></div><div class="v"></div></div><div class="bar" data-w="0"><div>filhos</div><div class="tr"><div class="fl" style="transition:width .25s"></div></div><div class="v"></div></div><div class="bar" data-w="0"><div>fumante (coluna 0/1)</div><div class="tr"><div class="fl" style="transition:width .25s"></div></div><div class="v"></div></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, bars = el.querySelectorAll(".bar");
    function calc() {
      var da = +g("#pa").value, db = +g("#pb").value, dc = +g("#pc").value, f = g("#pf").checked ? 1 : 0;
      g("#pao").textContent = da + " anos"; g("#pbo").textContent = db; g("#pco").textContent = dc;
      var parts = [da / (A.max - A.min), db / (B.max - B.min), dc / (C.max - C.min), f]; // MinMax: cada diferença é fração da faixa
      var tot = Math.sqrt(parts.reduce(function (s, v) { return s + v * v; }, 0));
      parts.forEach(function (v, i) { bars[i].querySelector(".fl").style.width = Math.min(100, v * 100) + "%"; bars[i].querySelector(".v").textContent = E.fmt(v, 3); });
      g(".read").innerHTML = "Depois do <b>MinMax</b>, cada diferença vira uma <b>fração da faixa da coluna</b>. Distância euclidiana entre as duas: <b>" + E.fmt(tot, 3) + "</b>. " + (f ? "Repare: <b>só o fato de um fumar e o outro não</b> já vale 1,000, tanto quanto a diferença entre a pessoa mais nova e a mais velha do dataset (46 anos). Colunas 0/1 pesam <b>muito</b> numa distância com MinMax (a demo usa uma coluna só; com o one-hot de duas categorias, seriam duas colunas discordando)." : "Ligue a caixa do fumante e veja uma única coluna 0/1 dominar a conta.");
    }
    el.querySelectorAll("input").forEach(function (i) { i.addEventListener("input", calc); i.addEventListener("change", calc); }); calc();
  };

  /* ---- vazamento com números ---- */
  E.demos.vazamento = function (el) {
    var tr = [20, 25, 30, 35, 40, 45, 50, 55], te = [60, 64];
    el.innerHTML = '<h4>O scaler "viu" o teste? Compare as médias</h4>' +
      '<div class="grid2"><div class="card" style="margin:0"><b style="color:var(--c0)">Treino</b>: ' + tr.join(", ") + '</div><div class="card" style="margin:0"><b style="color:var(--c1)">Teste</b>: ' + te.join(", ") + '</div></div>' +
      '<div class="ctrls"><button class="btn sm" type="button" data-m="all">Errado: ajustar o scaler em todos os dados</button><button class="btn sm pri" type="button" data-m="tr">Certo: ajustar só no treino</button></div><div class="read"></div>';
    var rd = el.querySelector(".read");
    function show(m) {
      var base = m === "all" ? tr.concat(te) : tr, n = base.length, mean = base.reduce(function (a, b) { return a + b; }, 0) / n, sd = Math.sqrt(base.reduce(function (s, v) { return s + (v - mean) * (v - mean); }, 0) / n);
      var z = te.map(function (v) { return E.fmt((v - mean) / sd, 3); });
      rd.innerHTML = "<b>" + (m === "all" ? "Errado" : "Certo") + "</b>. O scaler calculou média <b>" + E.fmt(mean, 2) + "</b> e desvio <b>" + E.fmt(sd, 2) + "</b> usando " + (m === "all" ? "as <b>10</b> linhas, <b>inclusive as de teste</b>" : "só as <b>8</b> linhas de treino") + ". Os dois valores de teste (60 e 64) viram <b>" + z.join(" e ") + "</b>." +
        (m === "all" ? "<br><span style='color:var(--red)'>O teste influenciou a régua que vai medir o próprio teste. É vazamento: o resultado pode ficar otimista, e ninguém vê (com um scaler o efeito costuma ser pequeno, mas em outras etapas, como seleção de colunas, pode ser grande).</span>" : "<br><span style='color:var(--green)'>No mundo real, os dados novos chegam depois e não participam da régua. Aqui é igual: o teste só é <i>transformado</i> com os números do treino.</span>");
      el.querySelectorAll("button").forEach(function (b) { b.classList.toggle("pri", b.getAttribute("data-m") === m); });
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-m]"); if (b) show(b.getAttribute("data-m")); }); show("tr");
  };
})();
