/* Demo do capítulo 2: uma consulta DNS passo a passo, com cache e TTL. Zonas fictícias (dp-core.js). */
(function () {
  var E = window.Estudo, DP = E.dp, esc = DP.esc;
  E.demos.dnsSim = function (el) {
    DP.estilo();
    var cache = {}, agora = 0;
    el.innerHTML = '<h4>Siga uma consulta DNS passo a passo</h4>' +
      '<p class="muted" style="margin:0 0 6px">Os nomes e os IPs são inventados (domínio <code>.example</code>, faixas de IP reservadas para exemplos). Faça a mesma consulta duas vezes e depois avance o relógio para ver o cache expirar.</p>' +
      '<div class="dpform"><label>Nome a consultar<input class="n" type="text" list="dp-nomes" value="meusite.example" spellcheck="false" autocomplete="off"></label></div>' +
      '<datalist id="dp-nomes">' + DP.NOMES_DNS.map(function (n) { return '<option value="' + n + '">'; }).join("") + '</datalist>' +
      '<div class="ctrls"><button class="btn pri" type="button" data-a="consultar">Consultar</button>' +
      '<button class="btn sm" type="button" data-a="t60">Avançar 60 s</button><button class="btn sm" type="button" data-a="t300">Avançar 300 s</button>' +
      '<button class="btn sm" type="button" data-a="limpar">Limpar o cache</button>' +
      '<span class="muted">Relógio da demo: <b class="rel">0</b> s</span></div>' +
      '<div class="out" aria-live="polite"></div><p class="muted cacheinfo" style="margin:6px 0 0"></p>';
    var out = el.querySelector(".out"), rel = el.querySelector(".rel"), ci = el.querySelector(".cacheinfo");
    function info() {
      var ks = Object.keys(cache).filter(function (k) { return cache[k].expira > agora; });
      rel.textContent = agora;
      ci.textContent = ks.length ? "No cache do resolvedor: " + ks.map(function (k) { return k + " (resta " + Math.round(cache[k].expira - agora) + " s)"; }).join("; ") + "." : "Cache do resolvedor vazio (ou tudo já expirou).";
    }
    function consultar() {
      var nome = el.querySelector(".n").value;
      var r = DP.resolve(nome, agora, cache);
      if (r.erro && !r.passos.length) { out.innerHTML = '<div class="dpstep bad">' + esc(r.erro) + '</div>'; info(); return; }
      cache = r.cache;
      var h = r.passos.map(function (p, i) {
        var ult = i === r.passos.length - 1;
        return '<div class="dpstep' + (ult && !r.erro ? ' ans' : '') + (ult && r.erro ? ' bad' : '') + '"><span class="who">' + (i + 1) + '. ' + esc(p.de) + ' → ' + esc(p.para) + '</span><br>' +
          (p.pergunta ? esc(p.pergunta) : '') + (p.pergunta && p.resposta ? '<br>' : '') + (p.resposta ? '<b>' + esc(p.resposta) + '</b>' : '') + '</div>';
      }).join("");
      var resumo = r.erro ? '<b>' + esc(r.erro) + '</b>' : (r.doCache ? 'Resposta do <b>cache</b> em ' + r.passos.length + ' passos.' : 'Consulta completa em <b>' + r.passos.length + '</b> passos. IP final: <b>' + esc(r.respostaFinal) + '</b>, guardado por <b>' + r.ttl + ' s</b> (o menor TTL da cadeia).');
      out.innerHTML = h + '<div class="read">' + resumo + '</div>';
      info();
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-a]"); if (!b) return;
      var a = b.getAttribute("data-a");
      if (a === "consultar") consultar();
      else if (a === "t60") { agora += 60; info(); }
      else if (a === "t300") { agora += 300; info(); }
      else if (a === "limpar") { cache = {}; info(); out.innerHTML = ""; }
    });
    el.querySelector(".n").addEventListener("keydown", function (e) { if (e.key === "Enter") consultar(); });
    info(); consultar();
  };
})();
