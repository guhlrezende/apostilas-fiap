/* Demos da apostila do Claude */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- cap 4: quanto custa uma chamada. Preços da página oficial de modelos, conferidos em 29/10/2026 (US$ por milhão de tokens). ---- */
  var PRECOS = { "Claude Fable 5.1": [10, 50], "Claude Opus 5.5": [4, 20], "Claude Sonnet 5.5": [2, 10], "Claude Haiku 5.5 (preço mínimo)": [0.10, 0.50] };
  E.demos.custoApi = function (el) {
    var ks = Object.keys(PRECOS);
    el.innerHTML = '<h4>Calculadora de custo da API</h4><div class="ctrls">' +
      '<label>Modelo <select data-k="m">' + ks.map(function (k, i) { return '<option' + (i === 2 ? " selected" : "") + '>' + k + '</option>'; }).join("") + '</select></label>' +
      '<label>Tokens de entrada <input type="range" data-k="i" min="500" max="50000" step="500" value="3000"><output></output></label>' +
      '<label>Tokens de saída <input type="range" data-k="o" min="100" max="8000" step="100" value="500"><output></output></label>' +
      '<label>Chamadas por mês <input type="range" data-k="n" min="100" max="20000" step="100" value="1000"><output></output></label>' +
      '<label><input type="checkbox" data-k="b"> Batch API (50% off)</label></div><div class="read"></div>';
    var q = function (k) { return el.querySelector('[data-k="' + k + '"]'); }, rd = el.querySelector(".read");
    function fmt(x) { return "US$ " + x.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 4 }); }
    function go() {
      ["i", "o", "n"].forEach(function (k) { q(k).nextElementSibling.textContent = (+q(k).value).toLocaleString("pt-BR"); });
      var p = PRECOS[q("m").value], i = +q("i").value, o = +q("o").value, n = +q("n").value, f = q("b").checked ? 0.5 : 1;
      var ci = i / 1e6 * p[0] * f, co = o / 1e6 * p[1] * f, um = ci + co;
      rd.innerHTML = 'Uma chamada: entrada ' + fmt(ci) + ' + saída ' + fmt(co) + ' = <b>' + fmt(um) + '</b><br>No mês (' + n.toLocaleString("pt-BR") + ' chamadas): <b>' + fmt(um * n) + '</b><br>' +
        '<span class="muted">Repare: o token de saída custa 5 vezes o de entrada em todos os modelos da tabela. Respostas longas pesam mais que prompts longos.</span>';
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---- cap 3: do pedido vago ao prompt estruturado ---- */
  E.demos.prompt = function (el) {
    var partes = [
      { k: "papel", t: "Papel (system)", v: "Você é assistente de um escritório de advocacia e escreve para clientes leigos." },
      { k: "contexto", t: "Contexto e porquê", v: "O cliente recebeu uma intimação e está ansioso. A mensagem vai por WhatsApp, então precisa ser curta e sem juridiquês." },
      { k: "documento", t: "Documento", v: "Intimação para audiência de conciliação em 12/11/2026, às 14h, no fórum central." },
      { k: "instrucoes", t: "Instruções", v: "1. Explique o que é a audiência em uma frase.\n2. Diga data, hora e local.\n3. Diga o que o cliente precisa levar." },
      { k: "formato", t: "Formato de saída", v: "Até 5 linhas, em prosa, sem listas. Responda dentro de <mensagem></mensagem>." }
    ];
    el.innerHTML = '<h4>Ligue e desligue as partes do prompt</h4><div class="ctrls">' + partes.map(function (p) { return '<label><input type="checkbox" data-k="' + p.k + '" checked> ' + p.t + '</label>'; }).join("") + '</div><pre class="pp" style="white-space:pre-wrap"></pre><div class="read"></div>';
    var pre = el.querySelector(".pp"), rd = el.querySelector(".read");
    function go() {
      var on = partes.filter(function (p) { return el.querySelector('[data-k="' + p.k + '"]').checked; });
      if (!on.length) { pre.textContent = "Escreva uma mensagem para o cliente sobre a intimação."; rd.innerHTML = "Este é o pedido vago. O Claude vai ter de adivinhar público, tom, tamanho e até o conteúdo da intimação."; return; }
      pre.textContent = on.map(function (p) { return p.k === "papel" ? "[system] " + p.v : "<" + p.k + ">\n" + p.v + "\n</" + p.k + ">"; }).join("\n\n");
      var falta = partes.filter(function (p) { return on.indexOf(p) < 0; }).map(function (p) { return p.t.toLowerCase(); });
      rd.innerHTML = falta.length ? "Faltando: <b>" + esc(falta.join(", ")) + "</b>. Cada parte que some vira um palpite do modelo." : "Completo: cada tipo de conteúdo está na sua tag, o porquê está explicado e o formato de saída é verificável pelo seu código (a tag <code>&lt;mensagem&gt;</code>).";
    }
    el.addEventListener("change", go); go();
  };
})();
