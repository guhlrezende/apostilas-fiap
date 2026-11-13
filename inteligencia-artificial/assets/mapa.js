/* Mapa da trilha: sidebar no desktop, gaveta no celular. Progresso em localStorage (try/catch).
   Precisa de trilha.js antes. A página define o capítulo atual com <body data-cap="N">. */
(function () {
  "use strict";
  var T = window.IA_TRILHA, host = document.getElementById("mapa");
  if (!T || !host) return;

  var CHAVE = "ia:feitos";
  function lerFeitos() { try { var v = JSON.parse(localStorage.getItem(CHAVE) || "[]"); return Array.isArray(v) ? v : []; } catch (e) { return []; } }
  function gravarFeitos(v) { try { localStorage.setItem(CHAVE, JSON.stringify(v)); } catch (e) { } }
  var feitos = lerFeitos();
  var atual = parseInt(document.body.getAttribute("data-cap"), 10) || 0;
  var porN = {}; T.caps.forEach(function (c) { porN[c.n] = c; });

  var SVG_OK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function estado(n) { return feitos.indexOf(n) >= 0 ? "feito" : (n === atual ? "atual" : "aberto"); }

  function render() {
    var total = T.caps.length, nFeitos = feitos.filter(function (n) { return porN[n]; }).length;
    var h = '<div class="mapa-cab"><span class="rotulo">Trilha</span>' +
      '<span class="mapa-conta" aria-live="polite">' + nFeitos + ' de ' + total + ' concluídos</span>' +
      '<div class="mapa-barra" role="progressbar" aria-label="Capítulos concluídos" aria-valuemin="0" aria-valuemax="' + total + '" aria-valuenow="' + nFeitos + '"><i style="width:' + (nFeitos / total * 100) + '%"></i></div></div>';
    T.partes.forEach(function (p) {
      h += '<section class="parte p' + p.n + '" aria-labelledby="mp' + p.n + '"><h2 class="parte-nome" id="mp' + p.n + '"><span>Parte ' + p.n + '</span>' + esc(p.nome) + '</h2><ol>';
      p.caps.forEach(function (n) {
        var c = porN[n], e = estado(n), tem = !!c.file;
        var marca = '<span class="marca-cap ' + e + '">' + (e === "feito" ? SVG_OK : "") + '</span>';
        var rot = '<span class="num-cap">' + (n < 10 ? "0" + n : n) + '</span><span class="tit-cap">' + esc(c.titulo) + '</span>';
        var sr = (e === "feito" ? '<span class="sr-only"> (concluído)</span>' : "") + (!tem ? '<span class="breve">em breve</span>' : "");
        var cur = n === atual ? ' aria-current="page"' : "";
        h += '<li class="cap ' + e + (tem ? "" : " sem") + '">' +
          (tem ? '<a href="' + esc(c.file) + '"' + cur + '>' : '<span class="cap-link"' + cur + '>') +
          marca + '<span class="cap-txt">' + rot + sr + '</span>' + (tem ? "</a>" : "</span>") + "</li>";
      });
      h += "</ol></section>";
    });
    host.innerHTML = h;
  }
  render();

  /* Gaveta (celular) */
  var btn = document.getElementById("btnMapa"), fundo = document.getElementById("mapaFundo");
  function aberta() { return document.body.classList.contains("mapa-aberto"); }
  function abrir() {
    document.body.classList.add("mapa-aberto"); btn && btn.setAttribute("aria-expanded", "true");
    var alvo = host.querySelector('[aria-current="page"]') || host.querySelector("a");
    setTimeout(function () { if (alvo) { if (!alvo.hasAttribute("href") && !alvo.hasAttribute("tabindex")) alvo.setAttribute("tabindex", "-1"); alvo.focus({ preventScroll: true }); } }, 30);
  }
  function fechar(voltar) {
    document.body.classList.remove("mapa-aberto"); btn && btn.setAttribute("aria-expanded", "false");
    if (voltar && btn) btn.focus();
  }
  if (btn) btn.addEventListener("click", function () { aberta() ? fechar(true) : abrir(); });
  if (fundo) fundo.addEventListener("click", function () { fechar(true); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && aberta()) fechar(true); });
  window.addEventListener("resize", function () { if (window.innerWidth >= 1024 && aberta()) fechar(false); });

  var ativo = host.querySelector('[aria-current="page"]');
  if (ativo) { /* só rola se o capítulo atual ficar fora da vista */
    var ra = ativo.getBoundingClientRect(), rh = host.getBoundingClientRect();
    if (ra.bottom > rh.bottom - 40) host.scrollTop += ra.top - rh.top - rh.height / 3;
  }

  /* Concluir o capítulo atual (botão no rodapé da página) */
  var bc = document.getElementById("btnConcluir");
  if (bc && atual) {
    function rotularBc() {
      var f = feitos.indexOf(atual) >= 0;
      bc.setAttribute("aria-pressed", f ? "true" : "false");
      bc.querySelector(".txt").textContent = f ? "Capítulo concluído" : "Marcar capítulo como concluído";
    }
    rotularBc();
    bc.addEventListener("click", function () {
      var i = feitos.indexOf(atual);
      if (i >= 0) feitos.splice(i, 1); else feitos.push(atual);
      gravarFeitos(feitos); rotularBc(); render();
    });
  }
})();
