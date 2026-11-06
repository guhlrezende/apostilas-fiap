/* Demo do capítulo 3: calculadora de permissões (rwx <-> número octal). As contas ficam em Estudo.tgperm, sem DOM. */
(function () {
  var E = window.Estudo, TG = E.tg, esc = TG.esc;
  var P = E.tgperm = {};

  /* bits: [[r,w,x] dono, [r,w,x] grupo, [r,w,x] outros] com 0/1 */
  P.octal = function (bits) {
    return bits.map(function (t) { return t[0] * 4 + t[1] * 2 + t[2]; }).join("");
  };
  P.simbolico = function (bits) {
    return bits.map(function (t) { return (t[0] ? "r" : "-") + (t[1] ? "w" : "-") + (t[2] ? "x" : "-"); }).join("");
  };
  P.deOctal = function (txt) {
    if (!/^[0-7]{3}$/.test(txt)) return null;
    return txt.split("").map(function (d) { d = +d; return [(d >> 2) & 1, (d >> 1) & 1, d & 1]; });
  };

  var PRE = [["644", "arquivo comum"], ["755", "script ou pasta"], ["600", "só você"], ["777", "perigoso"]];

  E.demos.chmodCalc = function (el) {
    TG.estilo();
    var bits = P.deOctal("644"), QUEM = ["dono", "grupo", "outros"], LET = ["r (ler)", "w (escrever)", "x (executar)"];
    var html = '<h4>Marque as caixas e veja o número</h4><div class="tgbits"><span></span>' + LET.map(function (l) { return '<b style="text-align:center;font-size:.85rem">' + l + '</b>'; }).join("");
    QUEM.forEach(function (q, i) {
      html += '<b>' + q + '</b>';
      for (var j = 0; j < 3; j++) html += '<label><input type="checkbox" data-i="' + i + '" data-j="' + j + '" aria-label="' + q + ' ' + LET[j] + '"></label>';
    });
    html += '</div><div class="ctrls">' + PRE.map(function (p) { return '<button class="btn sm" type="button" data-p="' + p[0] + '">' + p[0] + ' (' + p[1] + ')</button>'; }).join("") +
      '<label>ou digite o número <input class="pm-n" type="text" inputmode="numeric" maxlength="3" size="4" aria-label="Número octal" style="font:700 1rem var(--f-mono)"></label></div>' +
      '<div class="read" aria-live="polite"></div>';
    el.innerHTML = html;
    var cbs = el.querySelectorAll("input[type=checkbox]"), rd = el.querySelector(".read"), num = el.querySelector(".pm-n");
    function desenha(origem) {
      cbs.forEach(function (c) { c.checked = !!bits[+c.getAttribute("data-i")][+c.getAttribute("data-j")]; });
      var o = P.octal(bits), s = P.simbolico(bits);
      if (origem !== "digitou") num.value = o;
      var linhas = bits.map(function (t, i) {
        var d = t[0] * 4 + t[1] * 2 + t[2], p = [];
        if (t[0]) p.push("ler"); if (t[1]) p.push("escrever"); if (t[2]) p.push("executar");
        return '<b>' + QUEM[i] + '</b>: ' + (t[0] ? "4" : "0") + '+' + (t[1] ? "2" : "0") + '+' + (t[2] ? "1" : "0") + ' = <b>' + d + '</b> (' + (p.length ? p.join(", ") : "nada") + ')';
      }).join("<br>");
      rd.innerHTML = '<code>chmod ' + o + ' arquivo</code> deixa a listagem como <code>-' + s + '</code>.<br>' + linhas +
        (o === "777" ? '<br><span style="color:var(--red)"><b>Atenção:</b> qualquer usuário pode escrever e executar. Evite; dê só o mínimo necessário.</span>' : "") +
        (bits[0][2] === 0 && bits[1][2] === 0 && bits[2][2] === 0 ? "" : '<br><span class="muted">Há bit x ligado: o arquivo pode ser executado por quem tem esse x.</span>');
    }
    el.addEventListener("change", function (e) {
      var c = e.target.closest("input[type=checkbox]");
      if (c) { bits[+c.getAttribute("data-i")][+c.getAttribute("data-j")] = c.checked ? 1 : 0; desenha(); }
    });
    num.addEventListener("input", function () { var b = P.deOctal(num.value); if (b) { bits = b; desenha("digitou"); } else rd.innerHTML = '<span class="muted">Use três dígitos de 0 a 7, como 644.</span>'; });
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-p]"); if (!b) return;
      bits = P.deOctal(b.getAttribute("data-p")); desenha();
    });
    desenha();
  };
})();
