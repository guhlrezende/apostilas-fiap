/* Demos do capítulo 10 da apostila de Python: herança.
   O modelo (classes Sensor e filhas) reproduz o código do capítulo e fica em Estudo.heranca,
   para poder ser comparado com a saída real do Python. */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- números como o Python os escreve: 6.0 continua 6.0, 7 continua 7 ---- */
  function num(s) {
    s = String(s).trim().replace(",", ".");
    if (!/^-?\d{1,6}(\.\d{1,4})?$/.test(s)) return null;
    return { f: /\./.test(s), v: parseFloat(s) };
  }
  function rep(n) {
    if (!n.f) return String(n.v === 0 ? 0 : n.v);
    if (Object.is(n.v, -0)) return "-0.0";
    return Number.isInteger(n.v) ? n.v.toFixed(1) : String(n.v);
  }
  function I(v) { return { f: false, v: v }; }
  function F(v) { return { f: true, v: v }; }
  function vrep(v) {
    if (typeof v === "string") return "'" + v + "'";
    if (Array.isArray(v)) return "[" + v.map(vrep).join(", ") + "]";
    return rep(v);
  }

  /* ---- as quatro classes (o mesmo código do capítulo) ---- */
  var K = {
    Sensor: {
      pai: null,
      m: {
        __init__: function (x, o, k, a) { set(o, "nome", a[0]); set(o, "unidade", a[1]); set(o, "leituras", []); },
        registrar: function (x, o, k, a) { get(o, "leituras").push(a[0]); return null; },
        media: function (x, o) { var L = get(o, "leituras"), s = 0; L.forEach(function (n) { s += n.v; }); return F(Math.round(s / L.length * 100) / 100); },
        alerta: function () { return false; }
      }
    },
    SensorTemperatura: {
      pai: "Sensor",
      m: {
        __init__: function (x, o, k, a) { sup(x, o, k, "__init__", [a[0], "°C"]); set(o, "limite_max", a[1]); },
        alerta: function (x, o, k, a) { return a[0].v > get(o, "limite_max").v; }
      }
    },
    SensorUmidade: {
      pai: "Sensor",
      m: {
        __init__: function (x, o, k, a) { sup(x, o, k, "__init__", [a[0], "%"]); set(o, "minimo", a[1]); set(o, "maximo", a[2]); },
        alerta: function (x, o, k, a) { return !(get(o, "minimo").v <= a[0].v && a[0].v <= get(o, "maximo").v); }
      }
    },
    SensorGeladeira: {
      pai: "SensorTemperatura",
      m: {
        __init__: function (x, o, k, a) { sup(x, o, k, "__init__", [a[0], a[2]]); set(o, "limite_min", a[1]); },
        alerta: function (x, o, k, a) { return sup(x, o, k, "alerta", [a[0]]) || a[0].v < get(o, "limite_min").v; }
      }
    }
  };
  var ORDEM = ["Sensor", "SensorTemperatura", "SensorUmidade", "SensorGeladeira"];
  var VAR = { Sensor: "s", SensorTemperatura: "t", SensorUmidade: "u", SensorGeladeira: "g" };
  var CTOR = {
    Sensor: ['"base"', '"un"'],
    SensorTemperatura: ['"T1"', "8"],
    SensorUmidade: ['"U1"', "30", "70"],
    SensorGeladeira: ['"G1"', "2", "8"]
  };
  var CARGS = {
    Sensor: ["base", "un"],
    SensorTemperatura: ["T1", I(8)],
    SensorUmidade: ["U1", I(30), I(70)],
    SensorGeladeira: ["G1", I(2), I(8)]
  };
  function set(o, k, v) { for (var i = 0; i < o.attrs.length; i++) if (o.attrs[i][0] === k) { o.attrs[i][1] = v; return; } o.attrs.push([k, v]); }
  function get(o, k) { for (var i = 0; i < o.attrs.length; i++) if (o.attrs[i][0] === k) return o.attrs[i][1]; }
  function call(x, o, cls, nome, a) {
    var k = cls; while (k && !K[k].m[nome]) k = K[k].pai;
    x.log.push({ d: x.d, c: k, m: nome }); x.d++;
    var r = K[k].m[nome](x, o, k, a); x.d--; return r;
  }
  function sup(x, o, k, nome, a) { return call(x, o, K[k].pai, nome, a); }
  function mro(c) { var r = []; while (c) { r.push(c); c = K[c].pai; } r.push("object"); return r; }
  function novo(cn, x) { var o = { cls: cn, attrs: [] }; call(x, o, cn, "__init__", CARGS[cn]); return o; }
  function dicio(o) { return "{" + o.attrs.map(function (p) { return "'" + p[0] + "': " + vrep(p[1]); }).join(", ") + "}"; }

  /* roda um método de verdade no modelo e devolve a cadeia de chamadas e o resultado */
  function run(cn, metodo, arg) {
    var x = { log: [], d: 0 }, o, res;
    if (metodo === "__init__") { o = novo(cn, x); return { log: x.log, res: dicio(o) }; }
    var tmp = { log: [], d: 0 }; o = novo(cn, tmp);
    [F(4.5), F(6.0), F(9.2)].forEach(function (n) { call(tmp, o, cn, "registrar", [n]); });
    if (metodo === "media") res = rep(call(x, o, cn, "media", []));
    else {
      var n = num(arg); if (!n) return null;
      if (metodo === "registrar") { var r = call(x, o, cn, "registrar", [n]); res = (r === null ? "None" : r) + " | " + vrep(get(o, "leituras")); }
      else res = call(x, o, cn, "alerta", [n]) ? "True" : "False";
    }
    return { log: x.log, res: res };
  }
  E.heranca = { run: run, mro: mro, ordem: ORDEM };

  var CSS_CHIP = "display:inline-block;padding:6px 12px;border-radius:10px;font:600 .88rem var(--f-mono);border:2px solid ";
  function chip(estado, nome, legenda) {
    var st = estado === "roda" ? "var(--green);background:var(--green-soft)" : estado === "passa" ? "var(--amber);background:var(--amber-soft)" : "var(--line);background:var(--card);opacity:.55;border-style:dashed";
    return '<span style="display:inline-flex;flex-direction:column;align-items:center;gap:3px;text-align:center"><span style="' + CSS_CHIP + st + '">' + esc(nome) + '</span><small class="muted" style="font-size:.72rem;max-width:11em">' + legenda + '</small></span>';
  }
  var SETA = '<span class="muted" style="align-self:flex-start;padding-top:6px" aria-hidden="true">→</span>';

  /* ---- demo: quem responde quando eu chamo o método? ---- */
  E.demos.hierlab = function (el) {
    el.innerHTML = '<h4>Quem responde quando você chama o método?</h4>' +
      '<p class="muted" style="margin:2px 0 0">Escolha o objeto e o método. O Python procura o método na ordem da <code>__mro__</code> e roda o primeiro que achar.</p>' +
      '<div class="ctrls"><label>objeto <select class="hl-o">' + ORDEM.map(function (c) { return '<option value="' + c + '"' + (c === "SensorGeladeira" ? " selected" : "") + '>' + c + '</option>'; }).join("") + '</select></label>' +
      '<label>método <select class="hl-m"><option value="alerta" selected>alerta(valor)</option><option value="media">media()</option><option value="registrar">registrar(valor)</option><option value="__init__">criar o objeto (__init__)</option></select></label>' +
      '<label class="hl-a-w">valor <input class="hl-a" type="text" inputmode="decimal" value="1.5" size="6" style="width:5.5em;font-family:var(--f-mono)"></label>' +
      '<span class="hl-q"><button class="btn sm" type="button" data-v="1.5">1.5</button> <button class="btn sm" type="button" data-v="5">5</button> <button class="btn sm" type="button" data-v="9.2">9.2</button> <button class="btn sm" type="button" data-v="72.5">72.5</button></span></div>' +
      '<pre class="hl-cod" style="margin:6px 0"></pre>' +
      '<b>1. Ordem de busca (<code>__mro__</code>)</b><div class="hl-mro" style="display:flex;flex-wrap:wrap;gap:8px 6px;margin:8px 0 14px"></div>' +
      '<b>2. Quem rodou, e quem chamou quem</b><pre class="hl-ch" style="margin:6px 0 12px;white-space:pre-wrap"></pre>' +
      '<b>3. O que o Python devolve</b><div class="read hl-out"></div>';
    var so = el.querySelector(".hl-o"), sm = el.querySelector(".hl-m"), ia = el.querySelector(".hl-a"), aw = el.querySelector(".hl-a-w"), q = el.querySelector(".hl-q");
    var cod = el.querySelector(".hl-cod"), mr = el.querySelector(".hl-mro"), ch = el.querySelector(".hl-ch"), out = el.querySelector(".hl-out");
    function draw() {
      var cn = so.value, m = sm.value, v = VAR[cn], precisa = m === "alerta" || m === "registrar";
      aw.style.display = precisa ? "" : "none"; q.style.display = precisa ? "" : "none";
      var r = run(cn, m, ia.value);
      var setup = v + " = " + cn + "(" + CTOR[cn].join(", ") + ")";
      if (!r) { cod.textContent = setup; mr.innerHTML = ""; ch.textContent = ""; out.innerHTML = "Digite um número, como 9.2 ou 5 (até 6 dígitos)."; return; }
      var chamada = m === "__init__" ? "vars(" + v + ")" : m === "media" ? "round(" + v + ".media(), 2)" : v + "." + m + "(" + rep(num(ia.value)) + ")";
      cod.textContent = setup + (m === "__init__" ? "" : "\nfor n in (4.5, 6.0, 9.2):\n    " + v + ".registrar(n)") + "\n" + chamada;
      var ran = {}; r.log.forEach(function (e) { ran[e.c] = (ran[e.c] || 0) + 1; });
      var primeiro = null; r.log.forEach(function (e) { if (primeiro === null) primeiro = e.c; });
      var ordem = mro(cn), achou = false, h = [];
      ordem.forEach(function (c, i) {
        var est, leg;
        if (ran[c]) { est = "roda"; achou = true; leg = c === primeiro ? "define " + (m === "__init__" ? "__init__" : m) + ": roda" : "roda via super()"; }
        else if (!achou) { est = "passa"; leg = c === "object" ? "não tem" : "não define: o Python segue"; }
        else { est = "nao"; leg = "nem foi preciso olhar"; }
        if (i) h.push(SETA);
        h.push(chip(est, c, leg));
      });
      mr.innerHTML = h.join("");
      ch.textContent = r.log.map(function (e) {
        var pad = new Array(e.d + 1).join("    ");
        return e.d ? pad + "↳ via super(): " + e.c + "." + e.m : e.c + "." + e.m;
      }).join("\n");
      var primeiroCls = r.log[0].c, ult = r.log[r.log.length - 1].c;
      var txt = "<code>" + esc(chamada) + "</code> devolve <b>" + esc(r.res) + "</b>.";
      if (m === "registrar") txt = "<code>" + esc(chamada) + "</code> devolve <b>None</b> (o método só guarda) e a lista do objeto fica <b>" + esc(r.res.split(" | ")[1]) + "</b>.";
      if (primeiroCls !== cn) txt += " Quem respondeu foi a classe <b>" + primeiroCls + "</b>: <code>" + cn + "</code> herdou esse método sem escrevê-lo.";
      else if (r.log.length > 1) txt += " A própria <code>" + cn + "</code> definiu o método e, no meio dele, chamou a mãe com <code>super()</code>.";
      else txt += " A própria <code>" + cn + "</code> definiu o método (sobrescrita ou método só dela).";
      out.innerHTML = txt;
    }
    [so, sm].forEach(function (s) { s.addEventListener("change", draw); });
    ia.addEventListener("input", draw);
    q.addEventListener("click", function (e) { var b = e.target.closest("button[data-v]"); if (!b) return; ia.value = b.getAttribute("data-v"); draw(); });
    draw();
  };

  /* ---- demo: isinstance, type e issubclass ---- */
  E.demos.tipolab = function (el) {
    var NOMES = ORDEM.concat(["object"]);
    function opcoes(lista, sel) { return lista.map(function (c) { return '<option value="' + c + '"' + (c === sel ? " selected" : "") + '>' + c + '</option>'; }).join(""); }
    el.innerHTML = '<h4>isinstance, type e issubclass</h4>' +
      '<div class="ctrls"><label>objeto <select class="tl-o">' + opcoes(ORDEM, "SensorGeladeira") + '</select></label></div>' +
      '<div class="tablewrap"><table class="tl-t"></table></div><div class="read tl-r"></div>' +
      '<div class="ctrls" style="margin-top:14px"><code>issubclass(</code><select class="tl-a" aria-label="classe A">' + opcoes(NOMES, "SensorGeladeira") + '</select><code>,</code><select class="tl-b" aria-label="classe B">' + opcoes(NOMES, "Sensor") + '</select><code>)</code><b class="tl-s" style="font-family:var(--f-mono)"></b></div>';
    var so = el.querySelector(".tl-o"), tb = el.querySelector(".tl-t"), rd = el.querySelector(".tl-r"), sa = el.querySelector(".tl-a"), sb = el.querySelector(".tl-b"), rs = el.querySelector(".tl-s");
    function tf(b) { return '<b style="color:var(--' + (b ? "green" : "red") + ')">' + (b ? "True" : "False") + '</b>'; }
    function draw() {
      var cn = so.value, m = mro(cn), v = VAR[cn];
      tb.innerHTML = '<tr><th>classe C</th><th><code>isinstance(' + v + ', C)</code></th><th><code>type(' + v + ') == C</code></th></tr>' +
        NOMES.map(function (c) { return '<tr' + (c === cn ? ' class="dest"' : "") + '><td><code>' + c + '</code></td><td>' + tf(m.indexOf(c) >= 0) + '</td><td>' + tf(c === cn) + '</td></tr>'; }).join("");
      rd.innerHTML = "<code>" + cn + ".__mro__</code> = <b>" + m.join(" → ") + "</b>. O <code>isinstance</code> é <b>True</b> para a classe do objeto e para todas as mães dela; o <code>type(...) ==</code> só aceita a classe exata.";
      var ok = mro(sa.value === "object" ? "Sensor" : sa.value);
      var eh = sa.value === "object" ? sb.value === "object" : ok.indexOf(sb.value) >= 0;
      rs.innerHTML = "→ " + tf(eh);
    }
    [so, sa, sb].forEach(function (s) { s.addEventListener("change", draw); });
    draw();
  };
})();
