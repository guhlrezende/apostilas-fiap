/* Componentes de leitura: quiz de cenário, lacunas e glossário em tooltip. Sem dependências.
   Quiz:     <fieldset class="quiz" data-quiz="ID"><legend>...</legend>
               <label class="opcao" [data-certa]><input type="radio" name="ID"> <span>texto</span><template class="fb">explicação</template></label> ...
               <button class="btn" type="button">Conferir</button><div class="feedback"></div></fieldset>
   Lacuna:   <div class="lacuna" data-lacuna="ID"><p>Texto <input data-resp="resposta|alternativa"> texto</p><button class="btn">Conferir</button><div class="feedback"></div></div>
   Termo:    <button type="button" class="termo" data-def="definição curta">palavra</button>
   Progresso em localStorage (try/catch). */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  function lerLS(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function gravarLS(k, v) { try { localStorage.setItem(k, v); } catch (e) { } }
  function marcar(chave, id) {
    var a; try { a = JSON.parse(lerLS(chave) || "[]"); } catch (e) { a = []; } if (!Array.isArray(a)) a = [];
    if (a.indexOf(id) < 0) { a.push(id); gravarLS(chave, JSON.stringify(a)); }
  }
  function feito(chave, id) { try { var a = JSON.parse(lerLS(chave) || "[]"); return Array.isArray(a) && a.indexOf(id) >= 0; } catch (e) { return false; } }
  function norm(s) { return String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/\s+/g, " ").trim(); }
  function msg(box, cls, titulo, corpo) {
    box.className = "feedback " + cls; box.textContent = "";
    var t = document.createElement("span"); t.className = "estado"; t.textContent = titulo; box.appendChild(t);
    if (corpo != null) { var d = document.createElement("div"); if (typeof corpo === "string") d.textContent = corpo; else d.appendChild(corpo); box.appendChild(d); }
  }

  /* ---------- Quiz ---------- */
  $$("[data-quiz]").forEach(function (q) {
    var id = q.getAttribute("data-quiz"), box = $(".feedback", q), btn = $(".btn", q), erros = 0, travado = false;
    box.setAttribute("role", "status"); box.setAttribute("aria-live", "polite");
    function conferir() {
      if (travado) return;
      var marcada = $("input:checked", q);
      if (!marcada) { msg(box, "info", "Escolha uma opção", "Marque uma resposta e confira de novo."); return; }
      var lab = marcada.closest(".opcao"), certa = lab.hasAttribute("data-certa"), fb = $("template.fb", lab);
      var corpo = document.createElement("div"); if (fb) corpo.innerHTML = fb.innerHTML;
      $$(".opcao", q).forEach(function (o) { o.classList.remove("acertou", "errou"); });
      if (certa) {
        lab.classList.add("acertou"); msg(box, "ok", "Certo", corpo); travado = true; btn.setAttribute("aria-disabled", "true");
        $$("input", q).forEach(function (i) { i.disabled = true; }); marcar("ia:quiz", id);
      } else {
        erros++; lab.classList.add("errou");
        msg(box, "no", "Ainda não", corpo);
        if (erros >= 2) { var c = $(".opcao[data-certa]", q); c.classList.add("dica-certa"); var ex = document.createElement("div"); ex.className = "msg pequeno"; ex.textContent = "Depois de duas tentativas, destaquei a resposta certa com um contorno. Leia a explicação dela."; box.appendChild(ex); }
      }
    }
    btn.addEventListener("click", conferir);
    if (feito("ia:quiz", id)) { var c = $(".opcao[data-certa]", q); if (c) { $("input", c).checked = true; conferir(); } }
  });

  /* ---------- Lacunas ---------- */
  $$("[data-lacuna]").forEach(function (L) {
    var id = L.getAttribute("data-lacuna"), box = $(".feedback", L), btn = $(".btn", L), campos = $$("input[data-resp]", L), mostrou = false;
    box.setAttribute("role", "status"); box.setAttribute("aria-live", "polite");
    campos.forEach(function (c, i) {
      if (!c.getAttribute("aria-label")) c.setAttribute("aria-label", "Lacuna " + (i + 1) + " de " + campos.length);
      c.setAttribute("autocomplete", "off"); c.setAttribute("autocapitalize", "off"); c.spellcheck = false;
      if (!c.size || c.size < 4) c.size = Math.max(6, c.getAttribute("data-resp").split("|")[0].length + 2);
      c.addEventListener("input", function () { c.classList.remove("ok", "no"); c.removeAttribute("aria-invalid"); });
    });
    function conferir() {
      var certas = 0, vazias = 0;
      campos.forEach(function (c) {
        var v = norm(c.value), alts = c.getAttribute("data-resp").split("|").map(norm);
        c.classList.remove("ok", "no"); c.removeAttribute("aria-invalid");
        if (!v) { vazias++; c.classList.add("no"); c.setAttribute("aria-invalid", "true"); return; }
        if (alts.indexOf(v) >= 0) { certas++; c.classList.add("ok"); } else { c.classList.add("no"); c.setAttribute("aria-invalid", "true"); }
      });
      if (certas === campos.length) { msg(box, "ok", "Tudo certo", "Todas as " + campos.length + " lacunas conferem."); marcar("ia:lacunas", id); }
      else {
        msg(box, "no", certas + " de " + campos.length + " certas", vazias ? "Preencha todas as lacunas e confira de novo." : "As lacunas marcadas ainda não batem. Releia a frase e tente de novo.");
        if (!mostrou) { mostrou = true; var b = document.createElement("button"); b.type = "button"; b.className = "btn discreto"; b.textContent = "Mostrar as respostas";
          b.addEventListener("click", function () { campos.forEach(function (c) { c.value = c.getAttribute("data-resp").split("|")[0]; c.classList.remove("no"); c.classList.add("ok"); c.removeAttribute("aria-invalid"); }); msg(box, "info", "Respostas mostradas", "Preenchi com as respostas esperadas. Tente explicar por que cada uma serve."); });
          btn.parentNode.insertBefore(b, btn.nextSibling); }
      }
    }
    btn.addEventListener("click", conferir);
    L.addEventListener("keydown", function (e) { if (e.key === "Enter" && e.target.tagName === "INPUT") { e.preventDefault(); conferir(); } });
  });

  /* ---------- Glossário em tooltip ---------- */
  var tip = null, atual = null, pinado = false, timer = null, contador = 0;
  function criarTip() {
    tip = document.createElement("div"); tip.className = "tooltip"; tip.setAttribute("role", "tooltip"); tip.id = "ia-tooltip"; tip.hidden = true;
    document.body.appendChild(tip);
  }
  function mostrarTip(el) {
    if (!tip) criarTip();
    clearTimeout(timer); atual = el;
    tip.textContent = el.getAttribute("data-def"); tip.hidden = false; tip.style.visibility = "hidden";
    el.setAttribute("aria-describedby", "ia-tooltip");
    var r = el.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight, vw = document.documentElement.clientWidth, vh = window.innerHeight;
    var x = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), vw - tw - 8);
    var y = r.top - th - 10; if (y < 8) y = Math.min(r.bottom + 10, vh - th - 8);
    tip.style.left = x + "px"; tip.style.top = y + "px"; tip.style.visibility = "visible";
  }
  function esconderTip() { if (!tip || tip.hidden) return; tip.hidden = true; if (atual) atual.removeAttribute("aria-describedby"); atual = null; pinado = false; }
  $$(".termo").forEach(function (t) {
    t.setAttribute("aria-expanded", "false");
    t.addEventListener("mouseenter", function () { if (!pinado) mostrarTip(t); });
    t.addEventListener("mouseleave", function () { if (!pinado) timer = setTimeout(esconderTip, 120); });
    t.addEventListener("focus", function () { if (!pinado) mostrarTip(t); });
    t.addEventListener("blur", function () { if (!pinado) esconderTip(); });
    t.addEventListener("click", function (e) {
      e.preventDefault();
      if (pinado && atual === t) { esconderTip(); t.setAttribute("aria-expanded", "false"); return; }
      mostrarTip(t); pinado = true; t.setAttribute("aria-expanded", "true");
    });
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && tip && !tip.hidden) { var a = atual; esconderTip(); if (a) a.setAttribute("aria-expanded", "false"); } });
  document.addEventListener("click", function (e) { if (pinado && !e.target.closest(".termo")) { var a = atual; esconderTip(); if (a) a.setAttribute("aria-expanded", "false"); } });
  window.addEventListener("scroll", function () { if (tip && !tip.hidden && atual) mostrarTip(atual); }, { passive: true });
  window.addEventListener("resize", function () { if (tip && !tip.hidden && atual) mostrarTip(atual); });
})();
