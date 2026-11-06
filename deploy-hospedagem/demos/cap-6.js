/* Demo do capítulo 6: linha do tempo de um pipeline de CI/CD. Lógica em dp-core.js (DP.pipeline). */
(function () {
  var E = window.Estudo, DP = E.dp, esc = DP.esc;
  E.demos.pipelineSim = function (el) {
    DP.estilo();
    el.innerHTML = '<h4>Rode uma esteira de CI/CD</h4>' +
      '<p class="muted" style="margin:0 0 6px">Cada push dispara as etapas, em ordem. Mexa nas opções e veja onde a esteira para. É uma simulação: nenhum serviço real é chamado.</p>' +
      '<div class="dpform"><label>Modo<select class="modo"><option value="ci">Só integração contínua (CI)</option><option value="entrega">Entrega contínua (alguém aprova)</option><option value="implantacao">Implantação contínua (sobe sozinho)</option></select></label>' +
      '<label>Os testes passam?<select class="testes"><option value="1">Sim</option><option value="0">Não</option></select></label>' +
      '<label>Segredo de deploy cadastrado?<select class="segredo"><option value="1">Sim</option><option value="0">Não</option></select></label>' +
      '<label>Alguém aprovou?<select class="aprovado"><option value="0">Não</option><option value="1">Sim</option></select></label></div>' +
      '<div class="out" aria-live="polite"></div>';
    var out = el.querySelector(".out");
    function atualiza() {
      var v = function (c) { return el.querySelector("." + c).value; };
      var p = DP.pipeline({ modo: v("modo"), testes: v("testes") === "1", segredo: v("segredo") === "1", aprovado: v("aprovado") === "1" });
      var rot = { ok: "passou", falhou: "FALHOU", pulado: "não rodou", aguardando: "aguardando" };
      out.innerHTML = '<div class="dppipe">' + p.etapas.map(function (e, i) { return '<div class="et ' + e.s + '"><b>' + (i + 1) + '. ' + esc(e.n) + '</b>' + rot[e.s] + '<br><span class="muted">' + esc(e.t) + '</span></div>'; }).join("") + '</div>' +
        '<div class="read">' + (p.publicou ? '<b>O site novo foi para o ar.</b>' : '<b>Nada foi publicado.</b> O site que está no ar continua sendo a versão anterior.') + '</div>';
    }
    el.addEventListener("change", atualiza); atualiza();
  };
})();
