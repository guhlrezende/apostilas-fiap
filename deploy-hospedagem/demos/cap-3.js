/* Demo do capítulo 3: o navegador confere o certificado (nome, validade, autoridade). Casos prontos e modo livre. */
(function () {
  var E = window.Estudo, DP = E.dp, esc = DP.esc;
  var CASOS = [
    ["Certificado em ordem", { host: "www.exemplo.test", sans: "exemplo.test, *.exemplo.test", de: "2026-09-01", ate: "2026-12-01", hoje: "2026-11-06", confiavel: true }],
    ["Expirado", { host: "www.exemplo.test", sans: "exemplo.test, *.exemplo.test", de: "2025-01-01", ate: "2025-04-01", hoje: "2026-11-06", confiavel: true }],
    ["Nome errado", { host: "loja.exemplo.test", sans: "outro.test", de: "2026-09-01", ate: "2026-12-01", hoje: "2026-11-06", confiavel: true }],
    ["Autoassinado", { host: "www.exemplo.test", sans: "www.exemplo.test", de: "2026-09-01", ate: "2026-12-01", hoje: "2026-11-06", confiavel: false }],
    ["Curinga não cobre dois níveis", { host: "a.b.exemplo.test", sans: "*.exemplo.test", de: "2026-09-01", ate: "2026-12-01", hoje: "2026-11-06", confiavel: true }]
  ];
  E.demos.certCheck = function (el) {
    DP.estilo();
    el.innerHTML = '<h4>O navegador confere o certificado</h4>' +
      '<p class="muted" style="margin:0 0 6px">Escolha um caso ou mude os campos. O navegador faz três perguntas: o nome bate, está na validade e a autoridade é conhecida. Um "não" em qualquer uma derruba o cadeado. Os nomes (<code>exemplo.test</code>) são inventados.</p>' +
      '<div class="ctrls">' + CASOS.map(function (c, i) { return '<button class="btn sm" type="button" data-p="' + i + '">' + esc(c[0]) + '</button>'; }).join("") + '</div>' +
      '<div class="dpform"><label>Endereço aberto<input class="host" type="text" spellcheck="false"></label>' +
      '<label>Nomes no certificado (separe por vírgula)<input class="sans" type="text" spellcheck="false"></label>' +
      '<label>Válido de<input class="de" type="date"></label><label>Válido até<input class="ate" type="date"></label>' +
      '<label>Hoje<input class="hoje" type="date"></label>' +
      '<label>Autoridade conhecida?<select class="conf"><option value="1">Sim</option><option value="0">Não</option></select></label></div>' +
      '<div class="out" aria-live="polite"></div>';
    var q = function (s) { return el.querySelector(s); };
    function atualiza() {
      var r = DP.certVeredito({ host: q(".host").value, sans: q(".sans").value, de: q(".de").value, ate: q(".ate").value, hoje: q(".hoje").value, confiavel: q(".conf").value === "1" });
      if (r.erro) { q(".out").innerHTML = '<div class="dpchk no">' + esc(r.erro) + '</div>'; return; }
      q(".out").innerHTML = r.testes.map(function (t) { return '<div class="dpchk ' + (t.ok ? 'ok' : 'no') + '"><b>' + (t.ok ? 'OK' : 'FALHOU') + '</b><span><b>' + esc(t.nome) + '</b> ' + esc(t.txt) + '</span></div>'; }).join("") +
        '<div class="read">' + (r.ok ? 'Três de três: o navegador mostra o cadeado e segue em frente.' : '<b>' + r.falhas + ' de 3 falharam</b>: o navegador mostra um aviso de segurança antes de abrir a página.') + '</div>';
    }
    function carrega(i) { var c = CASOS[i][1]; q(".host").value = c.host; q(".sans").value = c.sans; q(".de").value = c.de; q(".ate").value = c.ate; q(".hoje").value = c.hoje; q(".conf").value = c.confiavel ? "1" : "0"; atualiza(); }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-p]"); if (b) carrega(+b.getAttribute("data-p")); });
    el.addEventListener("input", atualiza); el.addEventListener("change", atualiza);
    carrega(0);
  };
})();
