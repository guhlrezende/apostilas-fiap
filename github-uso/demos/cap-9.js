/* Demo do capítulo 9: vazou um segredo, e agora? Lógica em gh-core.js (GH.vazou). */
(function () {
  var E = window.Estudo, GH = E.gh, esc = GH.esc;
  E.demos.vazouSegredo = function (el) {
    GH.estilo();
    var tipos = Object.keys(GH.vazou.TIPOS), acoes = Object.keys(GH.vazou.ACOES);
    el.innerHTML = '<h4>Vazou um segredo, e agora?</h4>' +
      '<p class="muted" style="margin:0 0 6px">Responda as três perguntas e veja a ordem certa. Depois teste o seu instinto: clique no que você faria primeiro. Tudo é simulado e nenhum valor real é usado.</p>' +
      '<div class="ghform"><label>O que vazou?<select class="t"><option value="">Escolha...</option>' + tipos.map(function (k) { return '<option value="' + k + '">' + esc(GH.vazou.TIPOS[k]) + '</option>'; }).join("") + '</select></label>' +
      '<label>O repositório é...<select class="v"><option value="">Escolha...</option><option value="publico">Público</option><option value="privado">Privado</option></select></label>' +
      '<label>O commit já foi enviado (push)?<select class="e"><option value="">Escolha...</option><option value="sim">Sim</option><option value="nao">Não, só local</option></select></label></div>' +
      '<div class="plano" aria-live="polite"></div>' +
      '<h4 style="margin-top:14px">O que você faz? (clique na ordem em que faria)</h4><div class="ctrls">' + acoes.map(function (a) { return '<button class="btn sm" type="button" data-a="' + a + '">' + esc(GH.vazou.ACOES[a]) + '</button>'; }).join("") + '<button class="btn sm" type="button" data-r="1">Limpar</button></div>' +
      '<div class="ghlog log" aria-live="polite"></div>';
    var q = function (s) { return el.querySelector(s); };
    var feitas = [];
    function plano() {
      var p = GH.vazou.plano({ tipo: q(".t").value, visibilidade: q(".v").value, enviado: q(".e").value });
      if (p.pendente) { q(".plano").innerHTML = '<div class="ghmsg">' + esc(p.aviso) + '</div>'; return; }
      q(".plano").innerHTML = '<div class="ghmsg">' + p.aviso + '</div>' + p.passos.map(function (s) { return '<div class="ghpasso' + (s.obrig ? ' obrig' : '') + '"><span class="t">' + s.n + '. ' + esc(s.t) + '</span><br>' + s.d + '</div>'; }).join("") +
        '<div class="nota erro"><span class="lbl">Erro comum</span>' + p.erroComum + '</div>';
    }
    el.addEventListener("change", plano);
    el.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("button") : null;
      if (!b || !el.contains(b)) return;
      if (b.getAttribute("data-r")) { feitas = []; q(".log").innerHTML = ""; return; }
      var a = b.getAttribute("data-a"); if (!a) return;
      var r = GH.vazou.avalia(a, feitas);
      if (feitas.indexOf(a) < 0 && r.ok) feitas.push(a);
      var d = document.createElement("div"); d.className = r.nivel; d.innerHTML = '<b>' + esc(GH.vazou.ACOES[a] || a) + ':</b> ' + r.msg;
      q(".log").appendChild(d);
    });
    plano();
  };
})();
