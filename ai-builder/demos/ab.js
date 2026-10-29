/* Demos da apostila de Ferramentas de AI Builder */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- cap 1: requisição HTTP contra a API de triagem (mesmas respostas dos testes de exemplos/test_api.py) ---- */
  E.demos.http = function (el) {
    el.innerHTML = '<h4>Monte a requisição e veja a resposta</h4>' +
      '<div class="ctrls"><label>Método <select data-k="m"><option>GET</option><option selected>POST</option></select></label>' +
      '<label>Rota <select data-k="r"><option>/saude</option><option selected>/triagem</option></select></label>' +
      '<label>Cabeçalho x-api-key <select data-k="h"><option value="ok" selected>chave certa</option><option value="no">sem chave</option></select></label>' +
      '<label>Corpo (JSON) <select data-k="b"><option value="grande" selected>{"cliente":"Ana","valor":1500}</option><option value="pequeno">{"cliente":"Bia","valor":80}</option><option value="falta">{"cliente":"Davi"}</option></select></label></div>' +
      '<pre class="req"></pre><div class="read"></div>';
    var q = function (k) { return el.querySelector('[data-k="' + k + '"]'); }, pre = el.querySelector(".req"), rd = el.querySelector(".read");
    function run() {
      var m = q("m").value, r = q("r").value, h = q("h").value, b = q("b").value;
      var corpo = { grande: '{"cliente":"Ana","valor":1500}', pequeno: '{"cliente":"Bia","valor":80}', falta: '{"cliente":"Davi"}' }[b];
      pre.textContent = m + " " + r + " HTTP/1.1\nHost: 127.0.0.1:8000" + (h === "ok" ? "\nx-api-key: chave-de-teste" : "") + (m === "POST" ? "\ncontent-type: application/json\n\n" + corpo : "");
      var code, body, why;
      if (r === "/saude" && m === "GET") { code = 200; body = '{"status":"ok"}'; why = "A rota de saúde não pede chave nem corpo: só diz que a API está de pé."; }
      else if (r === "/saude") { code = 405; body = '{"detail":"Method Not Allowed"}'; why = "A rota existe, mas só aceita GET. 405 é o servidor dizendo: o endereço está certo, o verbo está errado."; }
      else if (m === "GET") { code = 405; body = '{"detail":"Method Not Allowed"}'; why = "/triagem só aceita POST, porque recebe dados para processar."; }
      else if (b === "falta") { code = 422; body = '{"detail":[{"type":"missing","loc":["body","valor"],...}]}'; why = "422: o JSON chegou, mas falta o campo obrigatório <code>valor</code>. A validação do corpo acontece antes da sua função rodar, por isso vem 422 mesmo sem chave."; }
      else if (h === "no") { code = 401; body = '{"detail":"chave inválida"}'; why = "401: o corpo é válido, mas sem a chave a função recusa. É o que impede um estranho de usar a sua API."; }
      else { var f = b === "grande" ? "prioridade" : "normal"; code = 200; body = '{"cliente":"' + (b === "grande" ? "Ana" : "Bia") + '","fila":"' + f + '"}'; why = "200: deu certo. Valor " + (b === "grande" ? "1500 é maior ou igual a 1000" : "80 é menor que 1000") + ", então a fila é <b>" + f + "</b>."; }
      var cor = code < 300 ? "var(--green)" : code < 500 ? "var(--red)" : "var(--amber)";
      rd.innerHTML = '<b style="color:' + cor + '">HTTP ' + code + '</b> <code>' + esc(body) + '</code><br>' + why;
    }
    el.addEventListener("change", run); run();
  };

  /* ---- cap 2: expressões do n8n ({{ $json... }}) sobre um item de exemplo ---- */
  var ITEM = { cliente: { nome: "Ana Souza", email: "ana@exemplo.com" }, pedido: { valor: 1500, itens: ["teclado", "mouse"] }, urgente: false };
  function caminho(expr) {
    var s = expr.trim();
    if (s.indexOf("$json") !== 0) throw new Error("comece com $json");
    var resto = s.slice(5), v = ITEM, re = /^\.([A-Za-z_]\w*)|^\[(\d+)\]|^\.(toUpperCase|toLowerCase)\(\)/, m;
    while (resto.length) {
      m = resto.match(re);
      if (!m) throw new Error("não entendi: " + resto);
      if (m[1] !== undefined) { if (v == null) throw new Error("Cannot read properties of undefined"); v = v[m[1]]; }
      else if (m[2] !== undefined) { if (v == null) throw new Error("Cannot read properties of undefined"); v = v[+m[2]]; }
      else { if (typeof v !== "string") throw new Error(m[3] + " só funciona em texto"); v = v[m[3]](); }
      resto = resto.slice(m[0].length);
    }
    return v;
  }
  function render(t) {
    return t.replace(/\{\{([^}]*)\}\}/g, function (_, ex) {
      var v = caminho(ex);
      if (v === undefined) return "[undefined]";
      return typeof v === "object" ? JSON.stringify(v) : String(v);
    });
  }
  E.demos.expr = function (el) {
    var exs = ["Olá, {{ $json.cliente.nome }}!", "Valor: R$ {{ $json.pedido.valor }}", "Primeiro item: {{ $json.pedido.itens[0] }}", "{{ $json.cliente.nome.toUpperCase() }}", "{{ $json.cliente.telefone }}", "{{ $json.endereco.cidade }}"];
    el.innerHTML = '<h4>Teste expressões do n8n neste item</h4><pre class="it"></pre>' +
      '<div class="ctrls">' + exs.map(function (x, i) { return '<button type="button" class="btn sm" data-i="' + i + '">' + esc(x) + '</button>'; }).join("") + '</div>' +
      '<label style="display:block;margin:6px 0">Campo do nó (texto com expressão):<br><input type="text" class="ex-in" style="width:100%;font:.9rem var(--f-mono);padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--paper-2);color:var(--ink)"></label><div class="read"></div>';
    el.querySelector(".it").textContent = JSON.stringify(ITEM, null, 2);
    var inp = el.querySelector(".ex-in"), rd = el.querySelector(".read");
    function go() {
      try {
        var out = render(inp.value);
        var aviso = out.indexOf("[undefined]") >= 0 ? '<br><span class="muted">O campo não existe neste item. No n8n isso aparece vazio e passa despercebido: confira o nome na aba de entrada do nó.</span>' : "";
        rd.innerHTML = 'Resultado: <b>' + esc(out) + '</b>' + aviso;
      } catch (e) { rd.innerHTML = '<span style="color:var(--red)">Erro: ' + esc(e.message) + '</span><br><span class="muted">Ler um campo de algo que não existe quebra a expressão inteira. É o erro mais comum quando o formato do dado de entrada muda.</span>'; }
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-i]"); if (!b) return; inp.value = exs[+b.getAttribute("data-i")]; go(); });
    inp.addEventListener("input", go); inp.value = exs[0]; go();
  };

  /* ---- cap 4: portas e volumes do Docker ---- */
  E.demos.porta = function (el) {
    el.innerHTML = '<h4>docker run -p PORTA_DO_PC:PORTA_DO_CONTAINER</h4>' +
      '<div class="ctrls"><label>Porta no seu PC <select data-k="h"><option>5678</option><option>8080</option></select></label>' +
      '<label>Porta no container <select data-k="c"><option>5678</option><option>80</option></select></label>' +
      '<label>Você abre <select data-k="u"><option>http://localhost:5678</option><option>http://localhost:8080</option></select></label>' +
      '<label><input type="checkbox" data-k="v" checked> volume n8n_data</label></div><div class="read"></div>' +
      '<div class="ctrls"><button type="button" class="btn sm pri" data-a="rec">docker compose down e depois up</button></div><div class="read rec"></div>';
    var q = function (k) { return el.querySelector('[data-k="' + k + '"]'); }, rd = el.querySelector(".read"), rec = el.querySelector(".rec");
    function go() {
      var h = q("h").value, c = q("c").value, u = q("u").value.split(":")[2];
      var cmd = "docker run -p " + h + ":" + c + (q("v").checked ? " -v n8n_data:/home/node/.n8n" : "") + " n8nio/n8n";
      var ok = u === h && c === "5678";
      var why = u !== h ? "Você abriu a porta " + u + ", mas o túnel foi aberto na " + h + " do seu PC. Nada escuta ali." :
        c !== "5678" ? "O túnel chega na porta " + c + " do container, mas o n8n escuta na 5678 lá dentro. Conexão recusada." :
        "O pedido entra pela " + h + " do seu PC e é entregue na 5678 do container, onde o n8n escuta.";
      rd.innerHTML = '<code>' + esc(cmd) + '</code><br><b style="color:var(--' + (ok ? "green" : "red") + ')">' + (ok ? "Abre o n8n" : "Não abre") + '</b>. ' + why;
      rec.innerHTML = "&nbsp;";
    }
    el.addEventListener("change", go);
    el.querySelector('[data-a="rec"]').addEventListener("click", function () {
      rec.innerHTML = q("v").checked ? "O container foi apagado e recriado, mas os fluxos e credenciais estavam no <b>volume</b>, que fica fora dele. Tudo continua lá." : '<b style="color:var(--red)">Sem volume, os dados viviam dentro do container.</b> Ele foi apagado no <code>down</code>, e os seus fluxos foram junto.';
    });
    go();
  };
})();
