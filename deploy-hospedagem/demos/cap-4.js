/* Demo do capítulo 4: árvore de decisão "onde hospedar". A lógica fica em dp-core.js (DP.recomenda). */
(function () {
  var E = window.Estudo, DP = E.dp, esc = DP.esc;
  function sel(c, rot, ops) { return '<label>' + rot + '<select class="' + c + '">' + ops.map(function (o) { return '<option value="' + o[0] + '">' + o[1] + '</option>'; }).join("") + '</select></label>'; }
  E.demos.ondeHospedar = function (el) {
    DP.estilo();
    el.innerHTML = '<h4>Onde eu hospedo isto?</h4>' +
      '<p class="muted" style="margin:0 0 6px">Responda sobre o seu projeto. A recomendação é um ponto de partida e o raciocínio aparece junto. Preços e planos gratuitos mudam: a demo não cita números.</p>' +
      '<div class="dpform">' +
      sel("conteudo", "O que o site tem?", [["estatico", "Só arquivos (HTML, CSS, JS, imagens)"], ["codigo", "Código que roda no servidor"], ["banco", "Código e banco de dados"]]) +
      sel("orcamento", "Orçamento", [["zero", "Zero"], ["baixo", "Baixo"], ["folga", "Tenho folga"]]) +
      sel("controle", "Controle sobre o servidor", [["nenhum", "Não preciso"], ["total", "Quero controle total"]]) +
      sel("admin", "Sei administrar servidor Linux?", [["nao", "Não"], ["sim", "Sim"]]) +
      sel("picos", "Tem picos fortes de acesso?", [["nao", "Não"], ["sim", "Sim"]]) +
      '</div><div class="out" aria-live="polite"></div>';
    var out = el.querySelector(".out");
    function atualiza() {
      var v = function (c) { return el.querySelector("." + c).value; };
      var r = DP.recomenda({ conteudo: v("conteudo"), orcamento: v("orcamento"), controle: v("controle"), admin: v("admin"), picos: v("picos") });
      out.innerHTML = '<div class="dpchk ok"><span><b>' + esc(r.titulo) + '</b><br><span class="muted">Modelo: ' + esc(r.modelo) + '</span></span></div>' +
        '<div class="read"><b>Por quê</b><ul style="margin:4px 0">' + r.motivos.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul>' +
        (r.cuidados.length ? '<b>Cuidados</b><ul style="margin:4px 0">' + r.cuidados.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul>' : '') + '</div>';
    }
    el.addEventListener("change", atualiza); atualiza();
  };
})();
