/* Demos do capítulo 1: camadas da IA e classificador de cenários */
(function () {
  var E = window.Estudo;

  /* ---- camadas da IA (blocos aninhados clicáveis) ---- */
  var CAMADAS = [
    { id: "ia", nome: "IA", cor: "c0", natureza: "Conceito amplo", aprende: "Não é uma técnica, é o objetivo", entrega: "Habilitar raciocínio e ação",
      txt: "É o guarda-chuva. Inclui qualquer coisa que faça um sistema parecer inteligente, até sistemas feitos só de regras escritas à mão." },
    { id: "ml", nome: "Machine Learning", cor: "c1", natureza: "Modelagem estatística", aprende: "Padrões em dados", entrega: "Predições e insights",
      txt: "Em vez de escrever regras, você mostra exemplos e o algoritmo descobre o padrão. É onde esta apostila inteira vive." },
    { id: "dl", nome: "Deep Learning", cor: "c2", natureza: "Redes neurais profundas", aprende: "Representações complexas", entrega: "Compreensão e geração",
      txt: "ML com redes neurais de muitas camadas. Brilha em imagem, áudio e texto, onde o padrão é difícil de descrever com colunas simples." },
    { id: "gen", nome: "Gen AI", cor: "c0", natureza: "Modelagem probabilística sequencial", aprende: "Modelos probabilísticos", entrega: "Geração e compreensão",
      txt: "Gera texto, imagem ou código prevendo o que vem a seguir. É um uso específico de deep learning, com resultado novo em vez de só uma nota ou categoria." }
  ];
  E.demos.camadas = function (el) {
    var html = '<h4>Toque em uma camada</h4><div class="ctrls" role="group" aria-label="Escolha uma camada">';
    CAMADAS.forEach(function (c, i) { html += '<button type="button" class="btn sm" data-i="' + i + '">' + c.nome + '</button>'; });
    html += '</div><div class="cam" aria-hidden="true" style="display:grid;gap:0">';
    var inner = '';
    for (var i = CAMADAS.length - 1; i >= 0; i--) {
      var c = CAMADAS[i];
      inner = '<div class="camb" data-i="' + i + '" style="--cc:var(--' + c.cor + ')"><span class="camn">' + c.nome + '</span>' + inner + '</div>';
    }
    html += inner + '</div><div class="card cam-info" style="margin:12px 0 0" aria-live="polite"></div>';
    html += '<p class="muted" style="font-size:.88rem;margin:10px 0 0"><b>IA agêntica</b> não é uma camada de dentro: é uma arquitetura que usa modelos (inclusive os de cima) para planejar e agir sozinha, com ferramentas e APIs.</p>';
    el.innerHTML = html;
    var st = document.createElement("style");
    st.textContent = ".camb{display:block;width:100%;text-align:left;border:2.5px solid var(--cc);border-radius:18px;padding:10px 14px 14px;margin:0;background:color-mix(in srgb,var(--cc) 9%,var(--card));cursor:pointer;transition:transform .2s,background .2s,box-shadow .2s}" +
      ".camb .camn{display:block;font:700 1rem var(--f-head);color:var(--cc);margin-bottom:8px;pointer-events:none}" +
      ".camb .camb{margin-top:2px}.camb:hover{background:color-mix(in srgb,var(--cc) 16%,var(--card))}.camb.sel{box-shadow:0 0 0 4px color-mix(in srgb,var(--cc) 30%,transparent)}";
    el.appendChild(st);
    var info = el.querySelector(".cam-info");
    function show(i) {
      var c = CAMADAS[i];
      info.innerHTML = '<b style="font:700 1.2rem var(--f-head);color:var(--' + c.cor + ')">' + c.nome + '</b><p style="margin:.4em 0">' + c.txt + '</p>' +
        '<div class="tablewrap" style="margin:6px 0 0"><table><tr><th>Natureza</th><th>O que aprende</th><th>O que entrega</th></tr><tr><td>' + c.natureza + '</td><td>' + c.aprende + '</td><td>' + c.entrega + '</td></tr></table></div>';
      el.querySelectorAll(".camb").forEach(function (b) { b.classList.toggle("sel", +b.getAttribute("data-i") === i); });
      el.querySelectorAll("button[data-i]").forEach(function (b) { b.classList.toggle("pri", +b.getAttribute("data-i") === i); });
    }
    el.addEventListener("click", function (e) { var b = e.target.closest(".camb, button[data-i]"); if (!b) return; e.stopPropagation(); show(+b.getAttribute("data-i")); });
    show(1);
  };
})();
