/* ==========================================================
   estudo.js  |  componentes compartilhados das apostilas
   Sem dependências. Cada apostila declara window.APOSTILA em capitulos.js.
   ========================================================== */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  };

  /* ---------- utilidades públicas ---------- */
  var Estudo = window.Estudo = {
    $: $, $$: $$, store: store, reduce: reduce,
    fmt: function (n, d) { return Number(n).toLocaleString("pt-BR", { minimumFractionDigits: d || 0, maximumFractionDigits: d == null ? 0 : d }); },
    colors: function () {
      var cs = getComputedStyle(document.documentElement), g = function (n) { return cs.getPropertyValue(n).trim(); };
      return { ink: g("--ink"), muted: g("--muted"), paper: g("--paper"), card: g("--card"), line: g("--line"), pen: g("--pen"),
        red: g("--red"), green: g("--green"), amber: g("--amber"), c0: g("--c0"), c1: g("--c1"), c2: g("--c2"),
        hlY: g("--hl-y"), hlB: g("--hl-b"), hlG: g("--hl-g"), hlP: g("--hl-p"), paper2: g("--paper-2") };
    },
    /* canvas com DPR, resize e repintura ao trocar de tema */
    canvas: function (cv, draw) {
      var ctx = cv.getContext("2d"), w = 0, h = 0, api = {};
      if (!cv.getAttribute("role")) { var hd = cv.closest(".demo") && cv.closest(".demo").querySelector("h4"); cv.setAttribute("role", "img"); cv.setAttribute("aria-label", (hd ? hd.textContent : "Gráfico") + ". O texto abaixo do gráfico descreve o resultado."); }
      function fit() {
        var r = cv.getBoundingClientRect(), d = window.devicePixelRatio || 1;
        w = r.width; h = r.height; cv.width = Math.max(1, Math.round(w * d)); cv.height = Math.max(1, Math.round(h * d));
        ctx.setTransform(d, 0, 0, d, 0, 0);
      }
      api.paint = function () { if (!w) fit(); ctx.clearRect(0, 0, w, h); draw(ctx, w, h, Estudo.colors()); };
      if (window.ResizeObserver) new ResizeObserver(function () { fit(); api.paint(); }).observe(cv);
      else { window.addEventListener("resize", function () { fit(); api.paint(); }); }
      document.addEventListener("themechange", api.paint);
      if (window.matchMedia) { try { matchMedia("(prefers-color-scheme: dark)").addEventListener("change", api.paint); } catch (e) { } }
      Object.defineProperty(api, "w", { get: function () { return w; } });
      Object.defineProperty(api, "h", { get: function () { return h; } });
      fit(); api.paint();
      return api;
    },
    /* arrastar/clicar em coordenadas CSS do canvas */
    pointer: function (cv, onDown, onMove, onUp) {
      var down = false; cv.style.touchAction = "none";
      function pos(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
      cv.addEventListener("pointerdown", function (e) { down = true; try { cv.setPointerCapture(e.pointerId); } catch (x) { } var p = pos(e); onDown && onDown(p.x, p.y, e); });
      cv.addEventListener("pointermove", function (e) { if (!down) return; var p = pos(e); onMove && onMove(p.x, p.y, e); });
      function up(e) { if (!down) return; down = false; var p = pos(e); onUp && onUp(p.x, p.y, e); }
      cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
    },
    /* executa fn uma vez, quando el entra na tela */
    onView: function (el, fn, th) {
      if (!("IntersectionObserver" in window)) { fn(); return; }
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); fn(); } }); }, { threshold: th || .25 });
      io.observe(el);
    },
    count: function (el, to, dec, ms) {
      if (reduce) { el.textContent = Estudo.fmt(to, dec); return; }
      var t0 = null; ms = ms || 1100;
      function f(t) { if (t0 === null) t0 = t; var p = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - p, 3); el.textContent = Estudo.fmt(to * e, dec); if (p < 1) requestAnimationFrame(f); }
      requestAnimationFrame(f);
    },
    demos: {},             // registro: Estudo.demos.nome = function(el){...}
    caps: function () { return window.APOSTILA ? window.APOSTILA.caps : []; }
  };

  /* ---------- tema ---------- */
  function applyTheme(t) {
    if (t) document.documentElement.setAttribute("data-theme", t); else document.documentElement.removeAttribute("data-theme");
    document.dispatchEvent(new Event("themechange"));
  }
  var savedTheme = store.get("estudo:tema", null);
  if (savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);
  function isDark() {
    var t = document.documentElement.getAttribute("data-theme");
    return t ? t === "dark" : (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches);
  }

  /* ---------- casca: topo, sidebar, folha ---------- */
  function buildShell() {
    var art = $("article.paper");
    if (!art) return;
    var A = window.APOSTILA, cap = parseInt(document.body.getAttribute("data-cap") || "0", 10);
    var base = document.body.getAttribute("data-root") || "../";
    var doneKey = A ? "estudo:" + A.id + ":done" : "estudo:x:done";
    var done = store.get(doneKey, []);

    var prog = document.createElement("div"); prog.id = "prog"; document.body.insertBefore(prog, document.body.firstChild);

    var top = document.createElement("header"); top.className = "topbar";
    var cur = A && cap ? A.caps.filter(function (c) { return c.n === cap; })[0] : null;
    top.innerHTML = '<button class="ibtn" id="menuBtn" aria-label="Abrir menu">☰</button>' +
      '<div class="brand">' + (A ? A.titulo : "Apostilas") + '<small>' + (cur ? "Cap. " + cur.n + " · " + cur.aula : "") + '</small></div>' +
      '<button class="ibtn" id="themeBtn" aria-label="Alternar tema claro e escuro" title="Claro / escuro"></button>';
    document.body.insertBefore(top, prog.nextSibling);
    var tb = $("#themeBtn"); function icon() { tb.textContent = isDark() ? "☀️" : "🌙"; } icon();
    tb.addEventListener("click", function () { var t = isDark() ? "light" : "dark"; store.set("estudo:tema", t); applyTheme(t); icon(); });
    $("#menuBtn").addEventListener("click", function () { document.body.classList.toggle("menu"); });

    var shell = document.createElement("div"); shell.className = "shell";
    var side = document.createElement("aside"); side.className = "side"; side.setAttribute("aria-label", "Navegação");
    var main = document.createElement("main"); main.className = "page";
    art.parentNode.insertBefore(shell, art); shell.appendChild(side); shell.appendChild(main); main.appendChild(art);

    var h = '<h4>Apostilas</h4><a href="' + base + 'index.html"><span class="n">⌂</span>Todas as apostilas</a>';
    if (A) {
      h += '<h4 style="margin-top:16px">' + A.titulo + '</h4><a href="' + (document.body.hasAttribute("data-hub") ? "#" : "index.html") + '" class="' + (cap ? "" : "cur") + '"><span class="n">★</span>Visão geral</a>';
      A.caps.forEach(function (c) {
        var isCur = c.n === cap, isDone = done.indexOf(c.n) > -1;
        h += '<a href="' + (c.file || "#") + '" class="' + (isCur ? "cur " : "") + (isDone ? "done" : "") + '"><span class="n">' + c.n + '</span><span style="flex:1">' + c.titulo + '</span><span class="ck">✓</span></a>';
        if (isCur) h += '<div class="subs" id="subs"></div>';
      });
      var pct = Math.round(100 * done.length / A.caps.length);
      h += '<div class="meter"><i style="width:' + pct + '%"></i></div><div class="meterlbl">' + done.length + " de " + A.caps.length + " capítulos concluídos</div>";
    }
    side.innerHTML = h;
    document.addEventListener("click", function (e) { if (document.body.classList.contains("menu") && !e.target.closest(".side") && !e.target.closest("#menuBtn")) document.body.classList.remove("menu"); });

    /* sub-índice das seções */
    var subs = $("#subs");
    if (subs) {
      $$(".sec", art).forEach(function (s, i) {
        if (!s.id) s.id = "s" + (i + 1);
        var h2 = $("h2", s); if (!h2) return;
        var a = document.createElement("a"); a.href = "#" + s.id; a.textContent = (h2.getAttribute("data-short") || h2.textContent.replace(/^\s*\d+\s*/, "").trim());
        a.setAttribute("data-t", s.id); subs.appendChild(a);
      });
    }

    /* anterior / próximo */
    if (A && cap && !$(".pn", art)) {
      var prev = A.caps.filter(function (c) { return c.n === cap - 1; })[0], next = A.caps.filter(function (c) { return c.n === cap + 1; })[0];
      var pn = document.createElement("nav"); pn.className = "pn";
      pn.innerHTML = (prev ? '<a class="prev" href="' + prev.file + '"><small>← Capítulo anterior</small><b>' + prev.titulo + '</b></a>' : '<span></span>') +
        (next ? '<a class="next" href="' + next.file + '"><small>Próximo capítulo →</small><b>' + next.titulo + '</b></a>' : '');
      art.appendChild(pn);
    }
    /* sentinela de conclusão */
    var fim = document.createElement("div"); fim.className = "fim"; fim.style.height = "1px"; art.appendChild(fim);
    if (A && cap) Estudo.onView(fim, function () {
      var d = store.get(doneKey, []); if (d.indexOf(cap) < 0) { d.push(cap); store.set(doneKey, d); }
      var a = $('.side a.cur'); if (a) a.classList.add("done");
    }, .6);

    /* barra de leitura */
    function onScroll() {
      var d = document.documentElement, p = d.scrollTop / Math.max(1, d.scrollHeight - d.clientHeight);
      prog.style.width = Math.min(100, p * 100) + "%";
    }
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

    /* scrollspy */
    if (subs && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { $$("a", subs).forEach(function (a) { a.classList.toggle("act", a.getAttribute("data-t") === e.target.id); }); } });
      }, { rootMargin: "-20% 0px -70% 0px" });
      $$(".sec", art).forEach(function (s) { io.observe(s); });
    }
  }

  /* ---------- hub: cartões dos capítulos ---------- */
  function buildHub() {
    var host = $("#caps"), A = window.APOSTILA; if (!host || !A) return;
    var done = store.get("estudo:" + A.id + ":done", []);
    host.innerHTML = A.caps.map(function (c) {
      var d = done.indexOf(c.n) > -1, soon = !c.file;
      return '<a class="cap-card rv ' + (d ? "done " : "") + (soon ? "soon" : "") + '" href="' + (c.file || "#") + '">' +
        '<span class="st">✓ lido</span><div class="no">' + c.n + '</div><h3>' + c.titulo + '</h3><p>' + c.resumo + '</p>' +
        '<p class="muted" style="font-size:.8rem;margin-top:8px">' + c.aula + (c.tempo ? " · ~" + c.tempo + " min" : "") + '</p></a>';
    }).join("");
  }
  function buildRoot() {
    var host = $("#apostilas"); if (!host || !window.APOSTILAS) return;
    host.innerHTML = window.APOSTILAS.map(function (a) {
      var done = store.get("estudo:" + a.id + ":done", []);
      return '<a class="cap-card rv ' + (a.pronta ? "" : "soon") + '" href="' + (a.pronta ? a.path : "#") + '"><div class="no">' + a.emoji + '</div><h3>' + a.titulo + '</h3><p>' + a.desc + '</p>' +
        '<p class="muted" style="font-size:.8rem;margin-top:8px">' + (a.pronta ? a.caps + " capítulos · " + done.length + " lidos" : "em breve") + '</p></a>';
    }).join("");
  }

  /* ---------- componentes ---------- */
  function initReveal() {
    var els = $$(".rv, .sec, mark.hl, .bar");
    if (!("IntersectionObserver" in window) || reduce) { els.forEach(function (e) { e.classList.add("in", "on"); if (e.classList.contains("bar")) setBar(e); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target; t.classList.add("in"); if (t.matches("mark.hl")) t.classList.add("on");
        if (t.classList.contains("bar")) setBar(t);
        io.unobserve(t);
      });
    }, { threshold: .15, rootMargin: "0px 0px -6% 0px" });
    els.forEach(function (e) { io.observe(e); });
    $$("[data-count]").forEach(function (el) {
      var to = parseFloat(el.getAttribute("data-count")), dec = parseInt(el.getAttribute("data-dec") || "0", 10);
      Estudo.onView(el, function () { Estudo.count(el, to, dec); }, .5);
    });
  }
  function setBar(b) { var f = $(".fl", b); if (f) f.style.width = (b.getAttribute("data-w") || 0) + "%"; }

  function initQuiz() {
    $$(".quiz").forEach(function (q, qi) {
      var ans = q.getAttribute("data-ans"), btns = $$(".opts button", q);
      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          if (q.classList.contains("done")) return;
          var ok = b.getAttribute("data-k") === ans;
          btns.forEach(function (x) { x.disabled = true; if (x.getAttribute("data-k") === ans) x.classList.add("ok"); });
          if (!ok) b.classList.add("no");
          q.classList.add("done");
          var fb = $(".fb", q); if (fb) fb.insertAdjacentHTML("afterbegin", ok ? "<b>Isso! </b>" : "<b>Quase. </b>");
        });
      });
    });
  }
  function initFlash() { $$(".fc").forEach(function (c) { c.addEventListener("click", function () { c.classList.toggle("flip"); }); }); }
  function initStepper() {
    $$(".stepper").forEach(function (s) {
      var steps = $$(".st", s), dots = $(".dots", s), i = 0, prev = $("[data-prev]", s), next = $("[data-next]", s);
      steps.forEach(function (_, k) { var d = document.createElement("i"); d.addEventListener("click", function () { go(k); }); dots.appendChild(d); });
      function go(n) {
        i = Math.max(0, Math.min(steps.length - 1, n));
        steps.forEach(function (x, k) { x.classList.toggle("on", k === i); });
        $$("i", dots).forEach(function (d, k) { d.className = k === i ? "on" : (k < i ? "past" : ""); });
        prev.disabled = i === 0; next.textContent = i === steps.length - 1 ? "Recomeçar ↺" : "Próximo →";
        s.dispatchEvent(new CustomEvent("step", { detail: i }));
      }
      prev.addEventListener("click", function () { go(i - 1); });
      next.addEventListener("click", function () { go(i === steps.length - 1 ? 0 : i + 1); });
      go(0);
    });
  }
  function initGlossary() { $$("abbr.gl").forEach(function (a) { a.tabIndex = 0; a.addEventListener("click", function () { a.classList.toggle("open"); }); a.addEventListener("blur", function () { a.classList.remove("open"); }); }); }
  function initCode() {
    $$("pre").forEach(function (p) {
      var b = document.createElement("button"); b.className = "copy"; b.type = "button"; b.textContent = "copiar";
      b.addEventListener("click", function () {
        var t = p.innerText.replace(/copiar$|copiado!$/, "").trimEnd();
        (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { b.textContent = "copiado!"; }, function () { b.textContent = "selecione e copie"; });
        setTimeout(function () { b.textContent = "copiar"; }, 1500);
      });
      p.appendChild(b);
    });
  }
  function initTransitions() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a"); if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target) return;
      var h = a.getAttribute("href"); if (!h || h.charAt(0) === "#" || /^(https?:|mailto:)/.test(h)) return;
      if (reduce) return;
      e.preventDefault(); document.body.classList.add("leaving"); setTimeout(function () { location.href = a.href; }, 170);
    });
    window.addEventListener("pageshow", function () { document.body.classList.remove("leaving"); });
  }
  function initDemos() {
    $$("[data-demo]").forEach(function (el) {
      var f = Estudo.demos[el.getAttribute("data-demo")];
      if (el.getAttribute("data-ready")) return; el.setAttribute("data-ready", "1");
      if (!f) { el.insertAdjacentHTML("beforeend", '<p class="muted">(demo "' + el.getAttribute("data-demo") + '" não encontrada)</p>'); return; }
      Estudo.onView(el, function () { try { f(el); } catch (err) { console.error(err); el.insertAdjacentHTML("beforeend", '<p class="muted">Erro ao carregar a demo.</p>'); } }, .05);
    });
  }

  /* ---- classificador de cenários (componente genérico: .sorter[data-demo=sorter][data-opts]) ---- */
  Estudo.demos.sorter = function (el) {
    var opts = (el.getAttribute("data-opts") || "").split("|").map(function (s) { var p = s.split(":"); return { k: p[0], t: p[1] }; });
    var score = 0, total = 0, items = el.querySelectorAll(".item");
    var out = el.querySelector(".sc");
    items.forEach(function (it) {
      var ans = it.getAttribute("data-ans"), box = document.createElement("div");
      box.style.cssText = "display:flex;gap:6px;flex-wrap:wrap";
      opts.forEach(function (o) {
        var b = document.createElement("button"); b.type = "button"; b.textContent = o.t; b.setAttribute("data-k", o.k);
        b.addEventListener("click", function () {
          if (it.classList.contains("done")) return;
          it.classList.add("done"); total++;
          box.querySelectorAll("button").forEach(function (x) { x.disabled = true; if (x.getAttribute("data-k") === ans) x.classList.add("ok"); });
          if (o.k === ans) score++; else b.classList.add("no");
          if (out) out.textContent = score + " de " + total + " certas" + (total === items.length ? (score === total ? ". Mandou bem!" : ". Releia os porquês abaixo de cada cenário.") : "");
        });
        box.appendChild(b);
      });
      it.insertBefore(box, it.querySelector(".why"));
    });
  };

  /* ---- lista de verificação que lembra o que você marcou (data-demo=checks) ---- */
  Estudo.demos.checks = function (el) {
    var key = "estudo:checks:" + location.pathname + ":" + (el.getAttribute("data-key") || "x"), saved = store.get(key, {}), boxes = $$("input[type=checkbox]", el), out = $(".chk-n", el);
    function upd() { var n = boxes.filter(function (b) { return b.checked; }).length; if (out) out.textContent = n + " de " + boxes.length; }
    boxes.forEach(function (b, i) { b.checked = !!saved[i]; b.addEventListener("change", function () { saved[i] = b.checked; store.set(key, saved); upd(); }); });
    upd();
  };

  document.addEventListener("DOMContentLoaded", function () {
    buildShell(); buildHub(); buildRoot();
    initCode(); initQuiz(); initFlash(); initStepper(); initGlossary(); initTransitions(); initReveal();
    document.dispatchEvent(new Event("estudo:ready"));
    initDemos();
  });
})();
