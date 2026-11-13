/* Casca da apostila "Inteligência Artificial": tema (claro, escuro, sistema) e barra de progresso.
   Sem dependências. localStorage sempre com try/catch. O mapa da trilha entra na tarefa seguinte. */
(function () {
  "use strict";
  var CHAVE = "ia:tema";
  var raiz = document.documentElement;

  function ler() { try { return localStorage.getItem(CHAVE); } catch (e) { return null; } }
  function gravar(v) { try { if (v) localStorage.setItem(CHAVE, v); else localStorage.removeItem(CHAVE); } catch (e) { } }
  function sistemaEscuro() { return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches; }
  function escuroAgora() { var t = raiz.getAttribute("data-theme"); return t ? t === "dark" : sistemaEscuro(); }

  function aplicar(t) {
    if (t === "dark" || t === "light") raiz.setAttribute("data-theme", t); else raiz.removeAttribute("data-theme");
  }

  var btn = document.getElementById("btnTema");
  function rotular() {
    if (!btn) return;
    var escuro = escuroAgora();
    btn.setAttribute("aria-label", escuro ? "Mudar para o tema claro" : "Mudar para o tema escuro");
    btn.setAttribute("aria-pressed", escuro ? "true" : "false");
    btn.querySelector(".ico-lua").style.display = escuro ? "none" : "";
    btn.querySelector(".ico-sol").style.display = escuro ? "" : "none";
  }
  if (btn) btn.addEventListener("click", function () {
    var novo = escuroAgora() ? "light" : "dark";
    gravar(novo); aplicar(novo); rotular();
  });
  if (window.matchMedia) {
    var mq = matchMedia("(prefers-color-scheme: dark)");
    var onMq = function () { if (!ler()) rotular(); };
    if (mq.addEventListener) mq.addEventListener("change", onMq); else if (mq.addListener) mq.addListener(onMq);
  }
  rotular();

  var barra = document.querySelector(".progresso i");
  if (barra) {
    var pend = false;
    var atualizar = function () {
      pend = false;
      var d = document.documentElement, max = d.scrollHeight - d.clientHeight;
      barra.style.width = (max > 0 ? Math.min(100, (d.scrollTop / max) * 100) : 0) + "%";
    };
    window.addEventListener("scroll", function () { if (!pend) { pend = true; requestAnimationFrame(atualizar); } }, { passive: true });
    window.addEventListener("resize", atualizar);
    atualizar();
  }
})();
