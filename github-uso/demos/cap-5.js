/* Demos do capítulo 5: simulador de tipos de merge e vida de um pull request. Lógica em gh-core.js (GH.merge, GH.pr). */
(function () {
  var E = window.Estudo, GH = E.gh, esc = GH.esc;

  E.demos.mergeSim = function (el) {
    GH.estilo();
    el.innerHTML = '<h4>Que história o merge deixa na main?</h4>' +
      '<p class="muted" style="margin:0 0 6px">A main começa com 2 commits (c1, c2). Escolha quantos commits tem o PR, se a main andou enquanto isso e o tipo de merge. É uma simulação das regras da documentação: nenhum repositório real é usado.</p>' +
      '<div class="ghform">' +
      '<label>Commits no PR (1 a 8)<input class="n" type="number" min="1" max="8" value="3" inputmode="numeric"></label>' +
      '<label>A main andou depois que a branch nasceu?<select class="m"><option value="1">Sim (apareceu o commit m1)</option><option value="0">Não</option></select></label>' +
      '<label>Tipo de merge<select class="t"><option value="merge">Merge commit</option><option value="squash">Squash and merge</option><option value="rebase">Rebase and merge</option></select></label>' +
      '<label>Situação do time<select class="s"><option value="logico">Uma mudança lógica com vários commits de ajuste</option><option value="historico">O histórico completo importa</option><option value="linear">Histórico linear, commits já organizados</option></select></label></div>' +
      '<div class="ghbox gr" aria-live="polite"></div><div class="ghcmp rs"></div><div class="ghmsg ind" aria-live="polite"></div>';
    var q = function (s) { return el.querySelector(s); };
    function atualiza() {
      var r = GH.merge({ n: q(".n").value, tipo: q(".t").value, mainAvancou: q(".m").value });
      if (!r.ok) { q(".gr").textContent = ""; q(".rs").innerHTML = ""; q(".ind").className = "ghmsg no ind"; q(".ind").innerHTML = r.erro; return; }
      q(".gr").textContent = r.linhas.join("\n");
      q(".rs").innerHTML = '<div><b>' + r.totalMain + '</b> commits na main depois do merge</div>' +
        '<div><b>' + r.novosNaMain + '</b> commit' + (r.novosNaMain > 1 ? 's' : '') + ' novo' + (r.novosNaMain > 1 ? 's' : '') + ' na main</div>' +
        '<div>Commit de merge: <b>' + (r.temCommitDeMerge ? 'sim' : 'não') + '</b></div>' +
        '<div>Commits do PR na main: <b>' + (r.commitsDoPRNaMain ? 'sim' : 'não') + (r.hashesNovos ? ' (cópias, hashes novos)' : '') + '</b></div>';
      var i = GH.indicado(q(".s").value), el2 = q(".ind");
      if (i.tipo === r.tipo) { el2.className = "ghmsg ok ind"; el2.innerHTML = '<b>Combina com a situação.</b> ' + esc(i.porque); }
      else { el2.className = "ghmsg ind"; el2.innerHTML = 'Para a situação “' + esc(i.rot) + '”, a documentação indica <b>' + esc(GH.TIPOS[i.tipo]) + '</b>: ' + esc(i.porque) + ' Você escolheu <b>' + esc(r.nome) + '</b>, que também funciona, mas deixa outra história.'; }
    }
    /* ao sair do campo de número, devolve o valor já corrigido (limite de 1 a 8) */
    el.addEventListener("change", function (e) {
      if (e.target === q(".n")) q(".n").value = GH.merge({ n: q(".n").value }).n;
      atualiza();
    });
    el.addEventListener("input", atualiza); atualiza();
  };

  var BOTOES = [
    ["abrir_draft", "Abrir como draft"], ["abrir", "Abrir como PR normal"], ["pronto", "Marcar como pronto"], ["pedir_revisao", "Pedir revisão"],
    ["aprovar", "Aprovar"], ["pedir_mudancas", "Pedir mudanças"], ["novo_commit", "Novo commit"], ["checks_passam", "Checks passam"], ["checks_falham", "Checks falham"],
    ["gerar_conflito", "Gerar conflito"], ["resolver_conflito", "Resolver conflito"], ["merge", "Fazer merge"], ["apagar_branch", "Apagar a branch"]
  ];
  E.demos.prFluxo = function (el) {
    GH.estilo();
    el.innerHTML = '<h4>Leve um PR do começo ao fim</h4>' +
      '<p class="muted" style="margin:0 0 6px">Clique nas ações. A simulação recusa o que não faz sentido e explica por quê. As regras ligadas abaixo são as da proteção da main (capítulo 7).</p>' +
      '<div class="ghform"><label class="ck"><input type="checkbox" class="ra" checked> Exigir aprovação</label><label class="ck"><input type="checkbox" class="rc" checked> Exigir checks</label><label class="ck"><input type="checkbox" class="rd"> Descartar aprovação antiga com novo commit</label></div>' +
      '<div class="ctrls">' + BOTOES.map(function (b) { return '<button class="btn sm" type="button" data-a="' + b[0] + '">' + b[1] + '</button>'; }).join("") + '<button class="btn sm" type="button" data-r="1">Recomeçar</button></div>' +
      '<div class="ghfases"></div><div class="ghmsg msg" aria-live="polite"></div><div class="ghcmp info"></div>';
    var q = function (s) { return el.querySelector(s); };
    var estado = null;
    function regras() { return { aprovacao: q(".ra").checked, checks: q(".rc").checked, descartar: q(".rd").checked }; }
    function novo() { estado = GH.pr.novo(regras()); msg("Escolha uma ação para começar: abra o PR.", ""); desenha(); }
    function msg(t, cl) { var m = q(".msg"); m.className = "ghmsg msg " + cl; m.textContent = t; }
    function desenha() {
      var ordem = ["draft", "aberto", "revisao", "mudancas", "aprovado", "mergeado"];
      q(".ghfases").innerHTML = ordem.map(function (f) { return '<div class="f' + (estado.fase === f ? ' on' : '') + (f === "mergeado" && estado.fase === f ? ' fim' : '') + '">' + esc(GH.FASES[f]) + '</div>'; }).join("");
      var ch = { nenhum: "não rodaram", rodando: "rodando", passou: "passaram", falhou: "falharam" }[estado.checks];
      q(".info").innerHTML = '<div>Fase: <b>' + esc(GH.FASES[estado.fase]) + '</b></div><div>Checks: <b>' + ch + '</b></div><div>Conflito: <b>' + (estado.conflito ? 'sim' : 'não') + '</b></div><div>Aprovações: <b>' + estado.aprovacoes + '</b></div><div>Branch: <b>' + (estado.fase === "mergeado" ? (estado.branchApagada ? 'apagada' : 'ainda existe') : 'em uso') + '</b></div>';
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("button") : null;
      if (!b || !el.contains(b)) return;
      if (b.getAttribute("data-r")) { novo(); return; }
      var a = b.getAttribute("data-a"); if (!a) return;
      estado.regras = regras(); /* as regras podem ser mudadas a qualquer momento */
      var r = GH.pr.agir(estado, a);
      estado = r.estado; msg((r.ok ? "" : "Recusado: ") + r.msg, r.ok ? "ok" : "no"); desenha();
    });
    el.addEventListener("change", function (e) {
      var c = e.target.classList;
      if (c && (c.contains("ra") || c.contains("rc") || c.contains("rd"))) { estado.regras = regras(); msg("Regras atualizadas.", ""); }
    });
    novo();
  };
})();
