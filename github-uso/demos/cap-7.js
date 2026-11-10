/* Demo do capítulo 7: este PR pode entrar na main? Lógica em gh-core.js (GH.regras). */
(function () {
  var E = window.Estudo, GH = E.gh, esc = GH.esc;
  E.demos.regrasMain = function (el) {
    GH.estilo();
    el.innerHTML = '<h4>Este PR pode entrar na main?</h4>' +
      '<p class="muted" style="margin:0 0 6px">Primeiro bloco: as regras da main. Segundo bloco: a situação do PR. É uma simulação do que a documentação descreve.</p>' +
      '<div class="ghform"><label>Aprovações exigidas (0 a 3)<input class="ma" type="number" min="0" max="3" value="1" inputmode="numeric"></label>' +
      '<label class="ck"><input type="checkbox" class="co" checked> Checks obrigatórios</label>' +
      '<label class="ck"><input type="checkbox" class="cv" checked> Conversas resolvidas obrigatórias</label>' +
      '<label class="ck"><input type="checkbox" class="ow"> Aprovação de code owner obrigatória</label>' +
      '<label class="ck"><input type="checkbox" class="de"> Aprovação antiga é descartada com novo commit</label>' +
      '<label class="ck"><input type="checkbox" class="sb"> Não permitir bypass (vale para admin)</label></div>' +
      '<div class="ghform"><label>Aprovações que o PR tem (0 a 5)<input class="ap" type="number" min="0" max="5" value="0" inputmode="numeric"></label>' +
      '<label>Checks<select class="ch"><option value="rodando">Rodando</option><option value="passou">Passaram</option><option value="falhou">Falharam</option></select></label>' +
      '<label>Conversas abertas (0 a 9)<input class="ab" type="number" min="0" max="9" value="1" inputmode="numeric"></label>' +
      '<label class="ck"><input type="checkbox" class="oa"> O code owner aprovou</label>' +
      '<label class="ck"><input type="checkbox" class="nc"> Houve novo commit depois da aprovação</label>' +
      '<label class="ck"><input type="checkbox" class="ad"> Quem faz o merge é administrador</label></div>' +
      '<div class="ghmsg v" aria-live="polite"></div>';
    var q = function (s) { return el.querySelector(s); };
    function atualiza() {
      var r = GH.regras({ minAprov: q(".ma").value, aprov: q(".ap").value, checks: q(".ch").value, conversasAbertas: q(".ab").value,
        checksObrig: q(".co").checked, conversasObrig: q(".cv").checked, ownersObrig: q(".ow").checked, ownerAprovou: q(".oa").checked,
        descartarAntigas: q(".de").checked, novoCommitDepois: q(".nc").checked, admin: q(".ad").checked, semBypass: q(".sb").checked });
      var v = q(".v");
      v.className = "ghmsg v " + (r.liberado ? "ok" : "no");
      v.innerHTML = '<b>' + (r.liberado ? (r.bypass ? 'Liberado, por bypass de administrador' : 'Liberado para merge') : 'Bloqueado') + '</b>' +
        (r.motivos.length ? '<ul style="margin:6px 0 0">' + r.motivos.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul>' : '<p style="margin:6px 0 0">Todas as regras ligadas foram cumpridas.</p>') +
        (r.nota ? '<p style="margin:6px 0 0">' + esc(r.nota) + '</p>' : '');
    }
    el.addEventListener("input", atualiza); el.addEventListener("change", atualiza); atualiza();
  };
})();
