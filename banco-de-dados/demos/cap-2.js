/* Demos do capítulo 2 (banco de dados): cardinalidade e tabela associativa */
(function () {
  var E = window.Estudo;

  var CARD = {
    "1:1": { esq: "Funcionário", dir: "Departamento que chefia", a: ["Ana", "Carlos", "Mariana"], b: ["Dep. Dados", "Dep. Cloud", "Dep. Segurança"], lig: [[0, 0], [1, 1], [2, 2]], nota: "Cada funcionário chefia no máximo um departamento, e cada departamento tem um chefe. Notação típica: (0,1) de um lado e (1,1) do outro." },
    "1:N": { esq: "Departamento", dir: "Funcionários", a: ["Dep. Dados", "Dep. Cloud"], b: ["Ana", "Carlos", "Mariana", "Pedro"], lig: [[0, 0], [0, 1], [1, 2], [1, 3]], nota: "Um departamento tem muitos funcionários, mas cada funcionário trabalha em um único departamento. A chave do lado 1 vira FK no lado N." },
    "N:N": { esq: "Funcionário", dir: "Projeto", a: ["Ana", "Carlos", "Mariana"], b: ["Omega", "AlphaBI", "NeuralNet"], lig: [[0, 0], [1, 0], [1, 2], [2, 1], [2, 2]], nota: "Carlos está em dois projetos, e o NeuralNet tem duas pessoas. Não cabe numa tabela só: exige uma tabela associativa." }
  };

  E.demos.cardinal = function (el) {
    var keys = Object.keys(CARD), cur = "1:N";
    el.innerHTML = '<h4>Escolha o tipo de relacionamento</h4><div class="ctrls">' + keys.map(function (k) { return '<button type="button" class="btn sm' + (k === cur ? " pri" : "") + '" data-k="' + k + '">' + k + '</button>'; }).join("") + '</div>' +
      '<canvas style="height:230px;cursor:default"></canvas><div class="read"></div>';
    var cv = el.querySelector("canvas"), rd = el.querySelector(".read");
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var d = CARD[cur], xl = 110, xr = w - 110, rows = Math.max(d.a.length, d.b.length), top = 50, gap = (h - top - 20) / Math.max(rows - 1, 1);
      function yOf(arr, i) { var span = gap * (arr.length - 1), off = ((rows - 1) * gap - span) / 2; return top + off + i * gap; }
      ctx.font = "700 12px Inter,system-ui,sans-serif"; ctx.fillStyle = c.muted; ctx.textAlign = "center";
      ctx.fillText(d.esq, xl, 22); ctx.fillText(d.dir, xr, 22);
      ctx.lineWidth = 2.5; ctx.strokeStyle = c.pen;
      d.lig.forEach(function (l) { ctx.beginPath(); ctx.moveTo(xl + 52, yOf(d.a, l[0])); ctx.bezierCurveTo(w / 2, yOf(d.a, l[0]), w / 2, yOf(d.b, l[1]), xr - 52, yOf(d.b, l[1])); ctx.stroke(); });
      function box(arr, x, col) { arr.forEach(function (t, i) { var y = yOf(arr, i); ctx.fillStyle = c.card; ctx.strokeStyle = col; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x - 52, y - 16, 104, 32, 9) : ctx.rect(x - 52, y - 16, 104, 32); ctx.fill(); ctx.stroke(); ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.fillText(t, x, y + 4); }); }
      box(d.a, xl, c.c0); box(d.b, xr, c.c1);
    });
    function show(k) { cur = k; el.querySelectorAll("button[data-k]").forEach(function (b) { b.classList.toggle("pri", b.getAttribute("data-k") === k); }); rd.innerHTML = "<b>" + k + "</b>. " + CARD[k].nota; api.paint(); }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-k]"); if (b) show(b.getAttribute("data-k")); });
    show(cur);
  };

  /* tabela associativa com linhas reais da base alpha */
  E.demos.ponte = function (el) {
    var F = [[1, "Ana Silva"], [2, "Carlos Souza"], [3, "Mariana Oliveira"], [5, "Juliana Rocha"]];
    var P = [[1, "Omega"], [2, "AlphaBI"], [3, "NeuralNet"]];
    var PF = [[1, 1, 8], [2, 1, 6], [2, 3, 5], [3, 2, 8], [5, 3, 8]];
    el.innerHTML = '<h4>Clique em um funcionário e veja a tabela do meio</h4><div class="grid3" style="align-items:start"><div><b>Funcionario</b><div class="tablewrap"><table class="tf"></table></div></div><div><b>ProjetoFuncionario</b> <span class="muted">(associativa)</span><div class="tablewrap"><table class="tpf"></table></div></div><div><b>Projeto</b><div class="tablewrap"><table class="tp"></table></div></div></div><div class="read"></div>';
    var sel = 2;
    function draw() {
      el.querySelector(".tf").innerHTML = "<tr><th>idFuncionario</th><th>nome</th></tr>" + F.map(function (r) { return '<tr data-f="' + r[0] + '" class="' + (r[0] === sel ? "dest" : "") + '" style="cursor:pointer"><td>' + r[0] + "</td><td>" + r[1] + "</td></tr>"; }).join("");
      el.querySelector(".tpf").innerHTML = "<tr><th>idFuncionario</th><th>idProjeto</th><th>horas</th></tr>" + PF.map(function (r) { return '<tr class="' + (r[0] === sel ? "dest" : "") + '"><td>' + r[0] + "</td><td>" + r[1] + "</td><td>" + r[2] + "</td></tr>"; }).join("");
      var ids = PF.filter(function (r) { return r[0] === sel; }).map(function (r) { return r[1]; });
      el.querySelector(".tp").innerHTML = "<tr><th>idProjeto</th><th>nome</th></tr>" + P.map(function (r) { return '<tr class="' + (ids.indexOf(r[0]) > -1 ? "dest" : "") + '"><td>' + r[0] + "</td><td>" + r[1] + "</td></tr>"; }).join("");
      var nome = F.filter(function (r) { return r[0] === sel; })[0][1], pj = P.filter(function (r) { return ids.indexOf(r[0]) > -1; }).map(function (r) { return r[1]; });
      el.querySelector(".read").innerHTML = "<b>" + nome + "</b> aparece em <b>" + ids.length + "</b> linha" + (ids.length > 1 ? "s" : "") + " da tabela do meio, e por isso está em " + (pj.length ? pj.join(" e ") : "nenhum projeto") + ". A PK composta (idFuncionario, idProjeto) impede repetir o mesmo par, e a coluna <code>horas</code> pertence ao <i>relacionamento</i>, não a um dos lados.";
    }
    el.addEventListener("click", function (e) { var tr = e.target.closest("tr[data-f]"); if (tr) { sel = +tr.getAttribute("data-f"); draw(); } });
    draw();
  };
})();
