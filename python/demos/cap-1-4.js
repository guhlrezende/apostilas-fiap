/* Demos dos capítulos 1 a 4 da apostila de Python */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- cap 2: formatação de f-string ---- */
  function pyFormat(v, spec) {
    var m = /^(?:(.)?([<>^=]))?([+\- ])?(0)?(\d+)?(,)?(?:\.(\d+))?([dfeEsg%])?$/.exec(spec);
    if (!m) return null;
    var fill = m[1], align = m[2], sign = m[3] || "", zero = m[4], width = m[5] ? +m[5] : 0, comma = m[6], prec = m[7] !== undefined ? +m[7] : null, type = m[8] || "";
    var s, num = typeof v === "number";
    if (type === "s" || (!num && !type)) { s = String(v); if (prec !== null) s = s.slice(0, prec); }
    else if (!num) return null;
    else {
      var neg = v < 0, a = Math.abs(v);
      if (!type && prec !== null && num) return null;
      if (type === "g") return null;
      if (type === "f") s = a.toFixed(prec === null ? 6 : prec);
      else if (type === "%") s = (a * 100).toFixed(prec === null ? 6 : prec) + "%";
      else if (type === "e" || type === "E") { s = a.toExponential(prec === null ? 6 : prec).replace(/e([+-])(\d)$/, "e$10$2"); if (type === "E") s = s.toUpperCase(); }
      else if (type === "d") { if (a % 1) return null; s = String(a); }
      else s = String(a);
      if (comma) { var p = s.split("."); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ","); s = p.join("."); }
      s = (neg ? "-" : (sign === "+" ? "+" : (sign === " " ? " " : ""))) + s;
    }
    if (s.length < width) {
      var padc = zero && !align ? "0" : (fill || " "), pad = width - s.length, al = align || (zero ? "=" : (num ? ">" : "<"));
      if (al === "<") s = s + new Array(pad + 1).join(padc);
      else if (al === "^") { var l = Math.floor(pad / 2); s = new Array(l + 1).join(padc) + s + new Array(pad - l + 1).join(padc); }
      else if (al === "=" && /^[+\- ]/.test(s)) s = s[0] + new Array(pad + 1).join(padc) + s.slice(1);
      else s = new Array(pad + 1).join(padc) + s;
    }
    return s;
  }
  E.demos.fmt = function (el) {
    el.innerHTML = '<h4>Mude o valor e a formatação e veja o que o print mostra</h4>' +
      '<div class="ctrls"><label>valor <input type="text" id="fv" value="34.611111111111114" style="width:210px;font-family:var(--f-mono)"></label>' +
      '<label>formato <input type="text" id="fs" value=".2f" style="width:110px;font-family:var(--f-mono)"></label></div>' +
      '<div class="ctrls"><span class="muted">Exemplos:</span>' + [".2f", ".4f", ".0f", ",.2f", ".1%", "e", "10.2f", "<10", ">10", "^10", "010.2f", "+.1f"].map(function (f) { return '<button class="btn sm" type="button" data-f="' + f + '">' + f + '</button>'; }).join("") + '</div>' +
      '<pre class="jq" style="margin:8px 0"></pre><div class="read"></div>';
    var iv = el.querySelector("#fv"), is = el.querySelector("#fs"), jq = el.querySelector(".jq"), rd = el.querySelector(".read");
    function go() {
      var raw = iv.value.trim(), num = raw !== "" && !isNaN(Number(raw)), v = num ? Number(raw) : iv.value, spec = is.value;
      jq.textContent = 'valor = ' + (num ? raw : JSON.stringify(raw)) + '\nprint(f"[{valor:' + spec + '}]")';
      var r = pyFormat(v, spec);
      rd.innerHTML = r === null ? "Este formato não é aceito para este tipo de valor ou não está coberto pela demo (ela cobre <code>d</code>, <code>f</code>, <code>e</code>, <code>%</code>, <code>s</code>, largura, alinhamento, sinal e vírgula). Em Python, alguns destes casos dão <code>ValueError</code> e outros têm saída própria." : "Saída: <b style='font-family:var(--f-mono)'>[" + esc(r) + "]</b>. O formato só muda o que <b>aparece</b>: a variável continua guardando o valor completo. (Detalhe: a demo arredonda como o JavaScript; em empates exatos, como <code>2.5</code> com <code>.0f</code>, o Python arredonda para o par e dá 2.)";
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-f]"); if (b) { is.value = b.getAttribute("data-f"); go(); } });
    iv.addEventListener("input", go); is.addEventListener("input", go); go();
  };

  /* ---- cap 3: condições com and / or / not ---- */
  E.demos.cond = function (el) {
    el.innerHTML = '<h4>Quem passa na condição?</h4><div class="ctrls"><label>idade <input type="range" id="ci" min="10" max="30" value="20"><output id="cio">20</output></label>' +
      '<label><input type="checkbox" id="cc" checked> tem_carteira</label></div>' +
      '<pre class="jq" style="margin:8px 0">if idade &gt;= 18 and tem_carteira:\n    print("Pode dirigir")\nif idade &lt; 18 or not tem_carteira:\n    print("Não pode dirigir")</pre><div class="tablewrap"><table class="ct"></table></div><div class="read"></div>';
    var ci = el.querySelector("#ci"), cc = el.querySelector("#cc");
    function go() {
      var i = +ci.value, c = cc.checked; el.querySelector("#cio").textContent = i;
      var a = i >= 18, b = c, r1 = a && b, a2 = i < 18, b2 = !c, r2 = a2 || b2;
      function tf(x) { return '<b style="color:var(--' + (x ? "green" : "red") + ')">' + (x ? "True" : "False") + '</b>'; }
      el.querySelector(".ct").innerHTML = '<tr><th>Expressão</th><th>Parte 1</th><th>Parte 2</th><th>Resultado</th></tr>' +
        '<tr><td><code>idade &gt;= 18 and tem_carteira</code></td><td>' + tf(a) + '</td><td>' + tf(b) + '</td><td>' + tf(r1) + '</td></tr>' +
        '<tr><td><code>idade &lt; 18 or not tem_carteira</code></td><td>' + tf(a2) + '</td><td>' + tf(b2) + '</td><td>' + tf(r2) + '</td></tr>';
      el.querySelector(".read").innerHTML = "Imprime: <b>" + (r1 ? "Pode dirigir" : "") + (r1 && r2 ? " e " : "") + (r2 ? "Não pode dirigir" : "") + "</b>. " + "O <code>and</code> exige as duas partes verdadeiras; o <code>or</code> basta uma; o <code>not</code> inverte. Repare que as duas condições são <b>complementares</b>: exatamente uma é verdadeira.";
    }
    ci.addEventListener("input", go); cc.addEventListener("change", go); go();
  };

  /* ---- cap 4: caixas da lista ---- */
  E.demos.listbox = function (el) {
    var L0 = [3, 1, 4, 1, 5], L = L0.slice(), code = "minha_lista = [3, 1, 4, 1, 5]", extra = null;
    el.innerHTML = '<h4>Uma lista é uma fila de caixas numeradas</h4><div class="lb" style="display:flex;gap:6px;flex-wrap:wrap;margin:10px 0"></div>' +
      '<div class="ctrls">' + [["append(9)", "append"], ["insert(0, 7)", "insert"], ["pop()", "pop"], ["pop(0)", "pop0"], ["remove(1)", "remove"], ["sort()", "sort"], ["reverse()", "reverse"], ["extend([8, 8])", "extend"], ["Reiniciar", "reset"]].map(function (b) { return '<button class="btn sm' + (b[1] === "reset" ? "" : " pri") + '" type="button" data-o="' + b[1] + '">' + (b[1] === "reset" ? "" : "minha_lista.") + b[0] + '</button>'; }).join("") + '</div>' +
      '<div class="ctrls"><label>fatia [ <input type="number" id="fa" value="1" style="width:60px"> : <input type="number" id="fb" value="3" style="width:60px"> ]</label></div><pre class="jq" style="margin:8px 0"></pre><div class="read"></div>';
    var box = el.querySelector(".lb"), jq = el.querySelector(".jq"), rd = el.querySelector(".read"), fa = el.querySelector("#fa"), fb = el.querySelector("#fb");
    function slice(l, a, b) { var n = l.length; a = a < 0 ? Math.max(0, n + a) : Math.min(a, n); b = b < 0 ? Math.max(0, n + b) : Math.min(b, n); return [a, Math.max(a, b)]; }
    function draw(msg) {
      var n = L.length, sl = slice(L, fa.value === "" ? 0 : +fa.value, fb.value === "" ? L.length : +fb.value);
      box.innerHTML = L.map(function (v, i) { var inS = i >= sl[0] && i < sl[1]; return '<div style="text-align:center;min-width:54px"><div style="padding:12px 0;border:2px solid var(--' + (inS ? "pen" : "ink") + ');border-radius:10px;background:var(--' + (inS ? "pen-soft" : "card") + ');font:700 1.2rem var(--f-head);transition:.25s">' + v + '</div><small class="muted">' + i + ' / ' + (i - n) + '</small></div>'; }).join("") || '<span class="muted">(lista vazia)</span>';
      jq.textContent = code + "\n# resultado: minha_lista = [" + L.join(", ") + "]\nminha_lista[" + fa.value + ":" + fb.value + "]  # -> [" + L.slice(sl[0], sl[1]).join(", ") + "]";
      rd.innerHTML = (msg || "Clique numa operação. Embaixo de cada caixa: o índice (da esquerda) e o índice negativo (da direita). A fatia destacada vai do primeiro índice (incluso) ao segundo (<b>excluso</b>).") + " Tamanho: <b>" + n + "</b>.";
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-o]"); if (!b) return; var o = b.getAttribute("data-o"), msg = "";
      if (o === "reset") { L = L0.slice(); code = "minha_lista = [3, 1, 4, 1, 5]"; }
      else if (o === "append") { L.push(9); code = "minha_lista.append(9)"; msg = "<code>append</code> põe no <b>final</b>."; }
      else if (o === "insert") { L.unshift(7); code = "minha_lista.insert(0, 7)"; msg = "<code>insert(i, x)</code> põe na posição i e <b>empurra</b> o resto para frente."; }
      else if (o === "pop") { var x = L.pop(); code = "minha_lista.pop()"; msg = "<code>pop()</code> remove <b>e devolve</b> o último (" + x + ")."; }
      else if (o === "pop0") { var y = L.shift(); code = "minha_lista.pop(0)"; msg = "<code>pop(0)</code> remove e devolve o do índice 0 (" + y + ")."; }
      else if (o === "remove") { var k = L.indexOf(1); if (k < 0) msg = "O valor 1 não está mais na lista: <code>remove(1)</code> daria <b>ValueError</b>."; else { L.splice(k, 1); msg = "<code>remove(x)</code> tira a <b>primeira</b> ocorrência do <b>valor</b> x (não o índice)."; } code = "minha_lista.remove(1)"; }
      else if (o === "sort") { L.sort(function (a, b) { return a - b; }); code = "minha_lista.sort()"; msg = "<code>sort()</code> ordena <b>no lugar</b> e devolve <code>None</code>. Para uma cópia, use <code>sorted(minha_lista)</code>."; }
      else if (o === "reverse") { L.reverse(); code = "minha_lista.reverse()"; msg = "<code>reverse()</code> inverte no lugar."; }
      else if (o === "extend") { L = L.concat([8, 8]); code = "minha_lista.extend([8, 8])"; msg = "<code>extend</code> junta os <b>elementos</b>. Já <code>append([8, 8])</code> poria a lista inteira como <b>um</b> elemento."; }
      draw(msg);
    });
    fa.addEventListener("input", function () { draw(); }); fb.addEventListener("input", function () { draw(); }); draw();
  };
})();
