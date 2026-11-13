/* Hub: monta a lista de partes e capítulos a partir de trilha.js e do progresso salvo (try/catch). */
(function () {
  "use strict";
  var T = window.IA_TRILHA, host = document.getElementById("trilha");
  if (!T || !host) return;
  var feitos = [];
  try { var v = JSON.parse(localStorage.getItem("ia:feitos") || "[]"); if (Array.isArray(v)) feitos = v; } catch (e) { }
  var porN = {}; T.caps.forEach(function (c) { porN[c.n] = c; });
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var pub = T.caps.filter(function (c) { return c.file; }).length;
  var cont = document.getElementById("conta-pub");
  if (cont) cont.textContent = pub + " de " + T.caps.length + " capítulos publicados";
  host.innerHTML = T.partes.map(function (p) {
    return '<section class="parte-card p' + p.n + '" aria-labelledby="hp' + p.n + '"><h3 id="hp' + p.n + '"><span class="rotulo">Parte ' + p.n + '</span>' + esc(p.nome) + '</h3><ol>' +
      p.caps.map(function (n) {
        var c = porN[n], f = feitos.indexOf(n) >= 0, nome = (n < 10 ? "0" + n : n) + " " + esc(c.titulo);
        var estado = c.file ? (f ? "concluído" : "disponível") : "em breve";
        return '<li class="' + (c.file ? "" : "sem") + '">' + (c.file ? '<a href="' + esc(c.file) + '">' + nome + "</a>" : "<span>" + nome + "</span>") + '<span class="estado-cap">' + estado + "</span></li>";
      }).join("") + "</ol></section>";
  }).join("");
})();
