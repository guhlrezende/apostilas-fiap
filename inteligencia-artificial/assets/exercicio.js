/* Célula de exercício: editor + Rodar + Enviar + dicas + solução, com Python (Pyodide) num Web Worker local.
   Contrato HTML de cada <section class="experimento" data-ex="ID" [data-limite="5"]>:
     <script type="text/plain" class="py-inicial">...</script>   código que o leitor vê
     <script type="text/plain" class="py-preparo">...</script>   (opcional) roda antes, invisível
     <script type="text/plain" class="py-teste">...</script>     usa verificar(cond, "mensagem") e a variável saida
     <script type="text/plain" class="py-solucao">...</script>   (opcional)
     <template class="dica">texto em HTML</template>             (zero ou mais, mostradas uma por vez)
   Estados: pass, fail, error, timeout, setup_error, test_error (mais "ok" quando só roda sem teste). */
(function () {
  "use strict";
  var BASE = document.currentScript ? document.currentScript.src : location.href;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var NS = "http://www.w3.org/2000/svg";
  var CHAVE_FEITOS = "ia:exercicios";
  function lerLS(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }
  function gravarLS(k, v) { try { localStorage.setItem(k, v); } catch (e) { } }
  function feitos() { try { var a = JSON.parse(lerLS(CHAVE_FEITOS, "[]")); return Array.isArray(a) ? a : []; } catch (e) { return []; } }

  /* ---------- Motor: um Worker compartilhado pela página ---------- */
  var Motor = {
    w: null, estado: "parado", pronto: null, fila: Promise.resolve(), proximoId: 1, pend: {}, pendPac: {}, carregados: {}, onProgresso: null, textoProgresso: "",
    garantir: function () {
      var M = this;
      if (M.estado === "pronto") return Promise.resolve();
      if (M.pronto) return M.pronto;
      M.estado = "carregando";
      M.pronto = new Promise(function (ok, falha) {
        var w;
        try { w = new Worker(new URL("runner-worker.js", BASE).href, { type: "module" }); }
        catch (e) { M.estado = "parado"; M.pronto = null; return falha(new Error("Este navegador não conseguiu iniciar o Python (Web Worker).")); }
        M.w = w;
        var limite = setTimeout(function () { M.reiniciar(); falha(new Error("O Python demorou demais para carregar.")); }, 90000);
        w.onmessage = function (ev) {
          var m = ev.data;
          if (m.tipo === "progresso") { M.textoProgresso = m.texto; M.onProgresso && M.onProgresso(m.texto); }
          else if (m.tipo === "pronto") { clearTimeout(limite); M.estado = "pronto"; ok(); }
          else if (m.tipo === "falha-carga") { clearTimeout(limite); M.reiniciar(); falha(new Error(m.erro)); }
          else if (m.tipo === "resultado") { var p = M.pend[m.id]; if (p) { delete M.pend[m.id]; clearTimeout(p.t); p.ok(m); } }
          else if (m.tipo === "pacotes-ok" || m.tipo === "pacotes-falha") {
            var q = M.pendPac[m.id]; if (q) { delete M.pendPac[m.id]; clearTimeout(q.t); if (m.tipo === "pacotes-ok") q.ok(); else q.falha(new Error("Não consegui carregar os pacotes: " + m.erro)); }
          }
        };
        w.onerror = function (e) { clearTimeout(limite); M.reiniciar(); falha(new Error("Falha ao carregar os arquivos do Python.")); };
      });
      return M.pronto;
    },
    reiniciar: function () {
      if (this.w) { try { this.w.terminate(); } catch (e) { } }
      this.w = null; this.estado = "parado"; this.pronto = null; this.carregados = {};
      var pend = this.pend; this.pend = {};
      Object.keys(pend).forEach(function (k) { clearTimeout(pend[k].t); });
      var pp = this.pendPac; this.pendPac = {};
      Object.keys(pp).forEach(function (k) { clearTimeout(pp[k].t); pp[k].falha(new Error("O Python foi reiniciado.")); });
    },
    /* Carrega pacotes locais (assets/pyodide/*.whl) que ainda faltam neste Worker. Não tem o limite do exercício. */
    carregarPacotes: function (lista) {
      var M = this, falt = (lista || []).filter(function (n) { return !M.carregados[n]; });
      if (!falt.length) return Promise.resolve();
      return new Promise(function (ok, falha) {
        var id = M.proximoId++;
        var t = setTimeout(function () { delete M.pendPac[id]; M.reiniciar(); falha(new Error("Os pacotes demoraram demais para carregar.")); }, 120000);
        M.pendPac[id] = { ok: function () { falt.forEach(function (n) { M.carregados[n] = true; }); ok(); }, falha: falha, t: t };
        M.onProgresso && M.onProgresso("Carregando " + falt.join(", ") + " (só na primeira vez)...");
        M.w.postMessage({ tipo: "pacotes", id: id, lista: falt });
      });
    },
    /* Executa; o tempo-limite só conta depois do Python e dos pacotes prontos. Passou do limite: mata e reinicia o Worker. */
    rodar: function (carga, limiteS) {
      var M = this;
      var tarefa = M.fila.then(function () {
        return M.garantir().then(function () { return M.carregarPacotes(carga.pacotes); }).then(function () {
          return new Promise(function (ok) {
            var id = M.proximoId++;
            var t = setTimeout(function () {
              delete M.pend[id]; M.reiniciar();
              ok({ estado: "timeout", saida: "", mensagem: "", linha: null, limite: limiteS });
            }, limiteS * 1000);
            M.pend[id] = { ok: ok, t: t };
            M.w.postMessage({ tipo: "rodar", id: id, setup: carga.setup, codigo: carga.codigo, teste: carga.teste });
          });
        });
      });
      M.fila = tarefa.catch(function () { });
      return tarefa;
    }
  };
  window.IAPython = Motor;

  /* ---------- Textos e ícones dos estados ---------- */
  var ICONES = {
    pass: "M5 12.5l4.5 4.5L19 7.5",
    ok: "M5 12.5l4.5 4.5L19 7.5",
    fail: "M6 6l12 12M18 6L6 18",
    error: "M12 8v5M12 16.5v.5M10.3 3.9L2.5 17.5A2 2 0 0 0 4.2 20.5h15.6a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z",
    timeout: "M12 7v5l3 2M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z",
    problema: "M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5z",
    carregando: "M12 3v4M12 17v4M3 12h4M17 12h4"
  };
  var TITULOS = {
    pass: "Passou", ok: "Rodou sem erro", fail: "Ainda não passou no teste", error: "Erro no seu código",
    timeout: "Tempo esgotado", setup_error: "Problema no exercício", test_error: "Problema no exercício"
  };
  var CLASSE = { pass: "pass", ok: "info", fail: "fail", error: "error", timeout: "fail", setup_error: "problema", test_error: "problema", carregando: "info" };
  var ICONE_DE = { pass: "pass", ok: "ok", fail: "fail", error: "error", timeout: "timeout", setup_error: "problema", test_error: "problema", carregando: "carregando" };

  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function icone(nome) {
    var s = document.createElementNS(NS, "svg"); s.setAttribute("viewBox", "0 0 24 24"); s.setAttribute("aria-hidden", "true");
    var p = document.createElementNS(NS, "path"); p.setAttribute("d", ICONES[nome]); s.appendChild(p); return s;
  }
  function texto(sec, cls) { var s = $("script." + cls, sec); return s ? s.textContent.replace(/^\n/, "").replace(/\s+$/, "") : ""; }

  /* ---------- Um exercício ---------- */
  function montar(sec) {
    var id = sec.getAttribute("data-ex") || ("ex" + Math.random().toString(36).slice(2, 7));
    var limite = parseFloat(sec.getAttribute("data-limite")) || 5;
    var pacotes = (sec.getAttribute("data-pacotes") || "").split(",").map(function (x) { return x.trim(); }).filter(Boolean);
    var inicial = texto(sec, "py-inicial"), preparo = texto(sec, "py-preparo"), teste = texto(sec, "py-teste"), solucao = texto(sec, "py-solucao");
    var dicas = [].slice.call(sec.querySelectorAll("template.dica")).map(function (t) { return t.innerHTML; });
    var chaveCod = "ia:cod:" + id;
    var tentativas = [], tentativa = 0, dicasVistas = 0, ocupado = false;

    var titulo = $("header h3", sec), rotulo = titulo ? (titulo.textContent) : id;

    /* Editor */
    var wrap = el("div", "editor-wrap");
    var ta = el("textarea", "editor");
    ta.value = lerLS(chaveCod, inicial);
    ta.spellcheck = false; ta.setAttribute("autocapitalize", "off"); ta.setAttribute("autocomplete", "off"); ta.setAttribute("autocorrect", "off");
    ta.setAttribute("aria-label", "Código Python do experimento: " + rotulo);
    ta.setAttribute("aria-describedby", id + "-dica-editor");
    function ajustar() { var n = ta.value.split("\n").length; ta.rows = Math.max(4, Math.min(24, n + 1)); }
    ajustar();
    var dicaEd = el("p", "editor-dica", "Dentro do editor, Tab indenta. Para sair com o teclado: Esc e depois Tab. Ctrl+Enter roda.");
    dicaEd.id = id + "-dica-editor";
    wrap.appendChild(ta); wrap.appendChild(dicaEd);

    /* Barra */
    var barra = el("div", "barra");
    function botao(txt, cls) { var b = el("button", "btn" + (cls ? " " + cls : ""), txt); b.type = "button"; return b; }
    var bRodar = botao("Rodar"), bEnviar = botao("Enviar", "primario"), bDica = botao(dicas.length ? "Dica" : "Dica", ""), bSol = botao("Ver solução"), bRest = botao("Restaurar o código inicial", "discreto");
    barra.appendChild(bRodar); if (teste) barra.appendChild(bEnviar);
    if (dicas.length) barra.appendChild(bDica);
    if (solucao) barra.appendChild(bSol);
    barra.appendChild(bRest);
    function rotDica() { var rest = dicas.length - dicasVistas; bDica.textContent = rest > 0 ? "Dica (" + rest + (rest === 1 ? " restante)" : " restantes)") : "Sem mais dicas"; bDica.setAttribute("aria-disabled", rest > 0 ? "false" : "true"); }
    rotDica();

    var areaDicas = el("div", "dicas"); areaDicas.setAttribute("aria-live", "polite");
    var areaSol = el("div", "solucao-area"); areaSol.hidden = true;
    var saida = el("div", "saida"); saida.hidden = true; saida.setAttribute("aria-label", "Saída do seu código");
    var res = el("div", "resultado vazio"); res.setAttribute("role", "status"); res.setAttribute("aria-live", "polite");

    var contador = el("span", "tentativas"); contador.setAttribute("aria-live", "off");

    /* Feito */
    var rot = $("header .rotulo", sec);
    var selo = el("span", "selo-feito", "Concluído"); selo.hidden = true;
    if (rot) rot.appendChild(selo);
    function marcarFeito() {
      var f = feitos(); if (f.indexOf(id) < 0) { f.push(id); gravarLS(CHAVE_FEITOS, JSON.stringify(f)); }
      selo.hidden = false;
    }
    if (feitos().indexOf(id) >= 0) selo.hidden = false;

    sec.appendChild(wrap); sec.appendChild(barra); sec.appendChild(areaDicas); sec.appendChild(areaSol); sec.appendChild(saida); sec.appendChild(res);
    barra.appendChild(contador);

    /* Resultado */
    function mostrar(estado, titulo, corpo, extra) {
      res.className = "resultado " + CLASSE[estado]; res.textContent = "";
      res.appendChild(icone(ICONE_DE[estado]));
      var d = el("div"); var t = el("span", "estado", titulo); d.appendChild(t);
      if (corpo) { var p = el("span", "msg", corpo); d.appendChild(p); }
      if (extra) { var x = el("span", "msg pequeno", extra); d.appendChild(x); }
      res.appendChild(d);
    }
    function mostrarSaida(s) { if (s && s.trim() !== "") { saida.hidden = false; saida.textContent = s; } else { saida.hidden = true; saida.textContent = ""; } }

    function carga(comTeste) { return { setup: preparo, codigo: ta.value, teste: comTeste ? teste : "", pacotes: pacotes }; }

    var dicaCarga = "Na primeira vez são cerca de 13 MB do Python" + (pacotes.length ? " mais os pacotes (" + pacotes.join(", ") + ")" : "") + "; depois fica guardado no navegador.";

    function ocupar(sim) { ocupado = sim; [bRodar, bEnviar].forEach(function (b) { b.setAttribute("aria-disabled", sim ? "true" : "false"); }); sec.setAttribute("aria-busy", sim ? "true" : "false"); }

    function executar(comTeste) {
      if (ocupado) return;
      ocupar(true);
      var nova = false;
      if (comTeste) {
        var cod = ta.value;
        nova = cod !== inicial && tentativas.indexOf(cod) < 0;
        if (nova) { tentativas.push(cod); tentativa++; contador.textContent = "Tentativa " + tentativa; }
      }
      mostrar("carregando", Motor.estado === "pronto" ? "Rodando..." : (Motor.textoProgresso || "Preparando o Python..."), "", Motor.estado === "pronto" ? "" : dicaCarga);
      Motor.onProgresso = function (tx) { mostrar("carregando", tx, "", dicaCarga); };
      Motor.rodar(carga(comTeste), limite).then(function (r) {
        Motor.onProgresso = null; mostrarSaida(r.saida);
        if (r.estado === "pass") { if (comTeste) { mostrar("pass", "Passou", "O teste conferiu. Bom trabalho."); marcarFeito(); } else mostrar("ok", "Rodou sem erro", "Ainda não conferi com o teste. Use Enviar para testar."); }
        else if (r.estado === "fail") mostrar("fail", TITULOS.fail, r.mensagem || "A resposta não bate com o esperado.", comTeste && !nova ? "Mesmo código de antes: não contou como nova tentativa." : "");
        else if (r.estado === "error") mostrar("error", TITULOS.error, (r.linha ? "Linha " + r.linha + ": " : "") + r.mensagem);
        else if (r.estado === "timeout") mostrar("timeout", TITULOS.timeout, "O código passou de " + r.limite + " segundos e foi interrompido, talvez por um laço que nunca termina.", "O Python foi reiniciado, então variáveis de antes foram perdidas.");
        else mostrar(r.estado, TITULOS[r.estado] || "Problema no exercício", r.mensagem, "O erro é do exercício, não do seu código. Avise quem mantém a apostila.");
      }).catch(function (e) {
        Motor.onProgresso = null;
        mostrar("error", "Não consegui carregar o que o exercício precisa", String(e.message || e), "Confira se os arquivos em assets/pyodide existem e se o navegador aceita Web Workers. Rodar de novo tenta outra vez.");
      }).then(function () { ocupar(false); });
    }

    bRodar.addEventListener("click", function () { executar(false); });
    bEnviar.addEventListener("click", function () { executar(true); });
    bDica.addEventListener("click", function () {
      if (dicasVistas >= dicas.length) return;
      var d = el("div", "dica-item"); var n = el("span", "rotulo", "Dica " + (dicasVistas + 1) + " de " + dicas.length); d.appendChild(n);
      var c = el("div"); c.innerHTML = dicas[dicasVistas]; d.appendChild(c); areaDicas.appendChild(d); dicasVistas++; rotDica();
    });
    bSol.addEventListener("click", function () {
      var liberada = tentativa >= 2 || (dicas.length > 0 && dicasVistas >= dicas.length);
      if (!areaSol.hidden) { areaSol.hidden = true; bSol.textContent = "Ver solução"; return; }
      if (!liberada) { mostrar("ok", "Calma, tente mais um pouco", "A solução libera depois de 2 tentativas diferentes" + (dicas.length ? " ou de ver todas as dicas." : "."), "Aprender é errar um pouco antes de olhar a resposta."); return; }
      areaSol.textContent = ""; areaSol.appendChild(el("span", "rotulo", "Uma solução possível"));
      var pre = el("pre", "codigo"); pre.tabIndex = 0; pre.textContent = solucao; areaSol.appendChild(pre);
      areaSol.hidden = false; bSol.textContent = "Esconder solução";
    });
    bRest.addEventListener("click", function () { ta.value = inicial; ajustar(); gravarLS(chaveCod, inicial); ta.focus(); });

    /* Editor: Tab indenta, Esc libera o Tab, Ctrl+Enter roda, rascunho salvo */
    var livre = false, salvar = null;
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { livre = true; return; }
      if (e.key === "Tab" && !livre && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        var s = ta.selectionStart, f = ta.selectionEnd;
        if (e.shiftKey) {
          var ini = ta.value.lastIndexOf("\n", s - 1) + 1;
          if (ta.value.substr(ini, 4) === "    ") { ta.value = ta.value.slice(0, ini) + ta.value.slice(ini + 4); ta.selectionStart = Math.max(ini, s - 4); ta.selectionEnd = Math.max(ini, f - 4); }
        } else { ta.value = ta.value.slice(0, s) + "    " + ta.value.slice(f); ta.selectionStart = ta.selectionEnd = s + 4; }
        ta.dispatchEvent(new Event("input"));
      } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); executar(false); }
      else if (e.key !== "Tab") livre = false;
    });
    ta.addEventListener("blur", function () { livre = false; });
    ta.addEventListener("input", function () { ajustar(); clearTimeout(salvar); salvar = setTimeout(function () { gravarLS(chaveCod, ta.value); }, 400); });
  }

  [].slice.call(document.querySelectorAll(".experimento[data-ex]")).forEach(montar);
})();
