/* Demo do capítulo 2: visualizador de pipes, estágio por estágio. Usa o mesmo mini shell do capítulo 1. */
(function () {
  var E = window.Estudo, TG = E.tg, esc = TG.esc;

  var PRESETS = [
    ["Quantas linhas de erro?", "cat log.txt | grep ERRO | wc -l"],
    ["Qual erro é o mais comum?", "grep ERRO log.txt | cut -d' ' -f3- | sort | uniq -c | sort -rn"],
    ["Vendas por produto (contagem)", "grep -v produto vendas.csv | cut -d, -f1 | sort | uniq -c"],
    ["Total vendido (awk)", "awk -F, 'NR>1 {s+=$2*$3} END {print s}' vendas.csv"],
    ["Armadilha: o erro não passa pelo pipe", "ls nao_existe | grep nao"],
    ["Consertando com 2>&1", "ls nao_existe 2>&1 | grep -c nao"]
  ];

  function nl(s) { return TG.linhas(s).length; }
  function mostra(s) {
    var ls = TG.linhas(s);
    if (!ls.length) return "(vazio)";
    var topo = ls.slice(0, 8).join("\n");
    return topo + (ls.length > 8 ? "\n... mais " + (ls.length - 8) + " linhas" : "");
  }

  E.demos.pipeViz = function (el) {
    TG.estilo();
    var cur = 0, res = null;
    el.innerHTML = '<h4>Siga os dados pelo pipe</h4>' +
      '<p class="muted" style="margin:0 0 6px">Cada estágio recebe o que o anterior mandou. Escolha um exemplo (ou digite o seu, usando os arquivos <code>log.txt</code> e <code>vendas.csv</code>) e avance um estágio por vez.</p>' +
      '<div class="ctrls"><label>exemplo <select class="pv-sel">' + PRESETS.map(function (p, i) { return '<option value="' + i + '">' + esc(p[0]) + '</option>'; }).join("") + '</select></label></div>' +
      '<div class="tgterm"><div class="tgin"><span>$</span><input class="pv-in" type="text" spellcheck="false" autocomplete="off" aria-label="Linha de comando com pipes"></div></div>' +
      '<div class="ctrls"><button class="btn sm" type="button" data-a="run">Executar</button><button class="btn sm" type="button" data-a="prev">Voltar um estágio</button><button class="btn sm pri" type="button" data-a="next">Próximo estágio</button><button class="btn sm" type="button" data-a="all">Mostrar tudo</button></div>' +
      '<div class="tgst"></div><div class="read" aria-live="polite"></div>';
    var sel = el.querySelector(".pv-sel"), inp = el.querySelector(".pv-in"), box = el.querySelector(".tgst"), rd = el.querySelector(".read"), upto = 0;

    function desenha() {
      if (!res) { box.innerHTML = ""; return; }
      var st = res.stages;
      box.innerHTML = st.map(function (s, i) {
        var on = i < upto;
        var cab = '<b>Estágio ' + (i + 1) + '</b> <code>' + esc(s.cmd) + '</code>';
        var ent = i === 0 ? "lê direto do arquivo (ou do teclado)" : nl(st[i - 1].out) + " linha(s) de entrada";
        var corpo = '<pre><code>' + esc(mostra(s.out)) + '</code></pre>';
        var er = s.err ? '<div class="tgerr" style="color:var(--red);font-size:.85rem;margin-top:4px">erro (vai direto para a tela, não entra no pipe): ' + esc(s.err.trim()) + '</div>' : "";
        return '<div class="tgcard' + (on ? " on" : "") + '">' + cab + '<br><small>' + ent + ' → ' + nl(s.out) + ' linha(s) de saída</small>' + (on ? corpo + er : "") + '</div>';
      }).join("");
      var ult = st[st.length - 1];
      if (upto >= st.length) {
        var perdidoNoPipe = st.some(function (s) { return s.err; });
        rd.innerHTML = 'Resultado final: <b>' + esc(mostra(ult.out).replace(/\n/g, " | ")) + '</b>.' + (perdidoNoPipe ? ' Repare: a mensagem de erro apareceu na tela, mas <b>não entrou</b> no <code>grep</code>. É por isso que o pipe seguinte ficou vazio.' : '');
      } else rd.innerHTML = upto === 0 ? 'Clique em <b>Próximo estágio</b> para ver o primeiro comando rodar.' : 'Estágio ' + upto + ' de ' + st.length + ' mostrado. O próximo comando vai receber exatamente estas ' + nl(st[upto - 1].out) + ' linha(s).';
    }
    function rodar() {
      var sh = new TG.Shell(); res = sh.run(inp.value); upto = 0;
      if (!res.stages.length) { rd.innerHTML = '<span style="color:var(--red)">' + esc(res.err || "Digite um comando.") + '</span>'; box.innerHTML = ""; res = null; return; }
      desenha();
    }
    function usar(i) { cur = i; inp.value = PRESETS[i][1]; rodar(); }
    sel.addEventListener("change", function () { usar(+sel.value); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") rodar(); });
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-a]"); if (!b || !res && b.getAttribute("data-a") !== "run") return;
      var a = b.getAttribute("data-a");
      if (a === "run") rodar();
      else if (a === "next") { upto = Math.min(res.stages.length, upto + 1); desenha(); }
      else if (a === "prev") { upto = Math.max(0, upto - 1); desenha(); }
      else if (a === "all") { upto = res.stages.length; desenha(); }
    });
    usar(cur);
  };
})();
