/* Demo do capítulo 1: simulador de requisição HTTP. O servidor é de mentira (dp-core.js); nada sai da página. */
(function () {
  var E = window.Estudo, DP = E.dp, esc = DP.esc;
  var PRE = [
    ["Página inicial", { metodo: "GET", caminho: "/", cab: "", corpo: "" }],
    ["Página que não existe", { metodo: "GET", caminho: "/nada.html", cab: "", corpo: "" }],
    ["Endereço antigo", { metodo: "GET", caminho: "/antigo", cab: "", corpo: "" }],
    ["Só os cabeçalhos (HEAD)", { metodo: "HEAD", caminho: "/", cab: "", corpo: "" }],
    ["Área restrita, sem token", { metodo: "GET", caminho: "/admin", cab: "", corpo: "" }],
    ["Área restrita, com token", { metodo: "GET", caminho: "/admin", cab: "Authorization: " + DP.TOKEN, corpo: "" }],
    ["Contato sem Content-Type", { metodo: "POST", caminho: "/contato", cab: "", corpo: '{"msg": "oi"}' }],
    ["Contato certo", { metodo: "POST", caminho: "/contato", cab: "Content-Type: application/json", corpo: '{"msg": "oi"}' }],
    ["POST na página inicial", { metodo: "POST", caminho: "/", cab: "", corpo: "" }],
    ["Rota com bug no servidor", { metodo: "GET", caminho: "/quebrado", cab: "", corpo: "" }]
  ];
  E.demos.httpSim = function (el) {
    DP.estilo();
    el.innerHTML = '<h4>Monte uma requisição e veja a resposta</h4>' +
      '<p class="muted" style="margin:0 0 6px">O servidor é de mentira e só atende o site <code>' + DP.HOST + '</code>. Escolha um exemplo ou monte o seu pedido. As rotas que existem: <code>/</code>, <code>/sobre.html</code>, <code>/antigo</code>, <code>/api/dados</code>, <code>/contato</code>, <code>/admin</code> e <code>/quebrado</code>.</p>' +
      '<div class="ctrls">' + PRE.map(function (p, i) { return '<button class="btn sm" type="button" data-p="' + i + '">' + esc(p[0]) + '</button>'; }).join("") + '</div>' +
      '<div class="dpform">' +
      '<label>Método<select class="m">' + DP.METODOS.map(function (m) { return '<option>' + m + '</option>'; }).join("") + '</select></label>' +
      '<label>Caminho<input class="c" type="text" value="/" spellcheck="false"></label>' +
      '<label>Host<input class="h" type="text" value="' + DP.HOST + '" spellcheck="false"></label></div>' +
      '<div class="dpform"><label>Cabeçalhos (um por linha, Nome: valor)<textarea class="cab" spellcheck="false"></textarea></label>' +
      '<label>Corpo (só faz sentido em POST)<textarea class="corpo" spellcheck="false"></textarea></label></div>' +
      '<div class="ctrls"><button class="btn pri" type="button" data-a="enviar">Enviar</button></div>' +
      '<div class="dpbox rq" aria-live="polite"></div><div class="read rs" aria-live="polite"></div>';
    var q = function (s) { return el.querySelector(s); };
    function enviar() {
      var req = { metodo: q(".m").value, caminho: q(".c").value, host: q(".h").value, cab: q(".cab").value, corpo: q(".corpo").value };
      var r = DP.http(req);
      var cabs = req.cab.trim() ? "\n" + req.cab.trim() : "";
      q(".rq").innerHTML = '<b>Requisição</b>\n' + esc(r.linhaReq) + '\nHost: ' + esc(req.host) + esc(cabs) + (req.corpo.trim() && req.metodo === "POST" ? '\n\n' + esc(req.corpo) : '');
      var cl = "s" + Math.floor(r.status / 100);
      q(".rs").innerHTML = '<span class="dpbadge ' + cl + '">' + r.status + ' ' + esc(r.texto) + '</span> <span class="muted">(' + DP.classe(r.status) + ')</span>' +
        '<div class="dpbox">' + r.cab.map(function (p) { return esc(p[0]) + ': ' + esc(p[1]); }).join("\n") + (r.corpo ? '\n\n' + esc(r.corpo) : '') + '</div>' +
        (r.dica ? '<p style="margin:4px 0 0"><b>Leitura:</b> ' + esc(r.dica) + '</p>' : '') +
        (r.ignoradas.length ? '<p class="muted" style="margin:4px 0 0">Linhas de cabeçalho ignoradas por não terem o formato Nome: valor: ' + esc(r.ignoradas.join(" | ")) + '</p>' : '');
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b || !el.contains(b)) return;
      if (b.hasAttribute("data-p")) {
        var p = PRE[+b.getAttribute("data-p")][1];
        q(".m").value = p.metodo; q(".c").value = p.caminho; q(".h").value = DP.HOST; q(".cab").value = p.cab; q(".corpo").value = p.corpo; enviar();
      } else if (b.getAttribute("data-a") === "enviar") enviar();
    });
    q(".c").addEventListener("keydown", function (e) { if (e.key === "Enter") enviar(); });
    enviar();
  };
})();
