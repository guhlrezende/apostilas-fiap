/* Demo do capítulo 6: fork e upstream. Lógica em gh-core.js (GH.fork). */
(function () {
  var E = window.Estudo, GH = E.gh, esc = GH.esc;
  var BOTOES = [
    ["fork", "1. Fazer o fork"], ["clonar", "2. git clone do fork"], ["add_upstream", "3. git remote add upstream"], ["dono_publica", "O dono publica uma novidade"],
    ["fetch_upstream", "4. git fetch upstream"], ["merge_upstream", "5. git merge upstream/main"], ["push_main", "6. git push origin main"],
    ["criar_branch", "7. Criar branch"], ["commit_branch", "8. Commit na branch"], ["enviar_branch", "9. git push da branch"], ["abrir_pr", "10. Abrir PR"]
  ];
  E.demos.forkSim = function (el) {
    GH.estilo();
    el.innerHTML = '<h4>Upstream, origin e a sua máquina</h4>' +
      '<p class="muted" style="margin:0 0 6px">Cada caixa mostra quantos commits tem a <code>main</code> naquele lugar. Clique nos passos, em qualquer ordem: a simulação recusa o que depende de outro passo.</p>' +
      '<div class="ctrls">' + BOTOES.map(function (b) { return '<button class="btn sm" type="button" data-a="' + b[0] + '">' + esc(b[1]) + '</button>'; }).join("") + '<button class="btn sm" type="button" data-r="1">Recomeçar</button></div>' +
      '<div class="ghnos nos"></div><div class="ghmsg msg" aria-live="polite"></div>';
    var q = function (s) { return el.querySelector(s); };
    var s;
    function msg(t, cl) { var m = q(".msg"); m.className = "ghmsg msg " + cl; m.textContent = t; }
    function desenha() {
      var atras = GH.fork.atras(s);
      var visto = s.visto === null ? "ainda não buscou" : s.visto + " commits";
      q(".nos").innerHTML =
        '<div class="ghno"><b>upstream (o original)</b><span class="n">' + s.up + '</span> commits na main</div>' +
        '<div class="ghno ' + (atras > 0 ? 'atras' : (s.forkFeito ? 'ok' : '')) + '"><b>origin (o seu fork)</b>' + (s.forkFeito ? '<span class="n">' + s.origin + '</span> commits na main<br>' + (atras > 0 ? 'atrás do original: <b>' + atras + '</b>' : 'em dia com o original') + (s.enviados ? '<br>branch fix/typo: ' + s.enviados + ' commit(s)' : '') : 'não existe ainda') + '</div>' +
        '<div class="ghno"><b>local (o seu computador)</b>' + (s.clonado ? '<span class="n">' + s.local + '</span> commits na main<br>upstream/main visto: ' + visto + (s.branch ? '<br>branch: ' + s.commitsBranch + ' commit(s)' : '') : 'ainda não clonou') + '</div>' +
        '<div class="ghno ' + (s.pr ? 'ok' : '') + '"><b>pull request</b>' + (s.pr ? 'aberto: fix/typo do seu fork para o original' : 'não aberto') + '</div>';
    }
    function novo() { s = GH.fork.novo(); msg("Comece pelo fork: sem ele, você não tem onde escrever.", ""); desenha(); }
    el.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("button") : null;
      if (!b || !el.contains(b)) return;
      if (b.getAttribute("data-r")) { novo(); return; }
      var a = b.getAttribute("data-a"); if (!a) return;
      var r = GH.fork.agir(s, a); s = r.estado; msg((r.ok ? "" : "Recusado: ") + r.msg, r.ok ? "ok" : "no"); desenha();
    });
    novo();
  };
})();
