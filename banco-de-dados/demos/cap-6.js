/* Demo do capítulo 6 (banco de dados): tipos de JOIN com as tabelas da papelaria */
(function () {
  var E = window.Estudo;
  var CLI = [[1, "Júlia"], [2, "Amanda"], [3, "Roberto"], [4, "Mariana"], [5, "Miguel"]];
  var PED = [[1, 1], [2, 2], [3, 1], [4, 2]]; // [idPedido, idCliente]

  function esc(t) { return t == null ? '<span class="nul">NULL</span>' : String(t); }

  E.demos.joins = function (el) {
    var tipo = "INNER", inv = false;
    el.innerHTML = '<h4>Escolha o JOIN e veja quais linhas sobrevivem</h4>' +
      '<div class="ctrls"><label>tipo <select id="jt"><option>INNER</option><option>LEFT</option><option>RIGHT</option><option>FULL</option></select></label>' +
      '<label><input type="checkbox" id="ji"> inverter: <code>pedido</code> à esquerda</label></div>' +
      '<div class="grid2"><div><b id="la"></b><div class="tablewrap"><table class="ta"></table></div></div><div><b id="lb"></b><div class="tablewrap"><table class="tb"></table></div></div></div>' +
      '<pre class="jq" style="margin:10px 0"></pre><div class="tablewrap"><table class="tr"></table></div><div class="read"></div>';
    var st = document.createElement("style"); st.textContent = ".nul{color:var(--red);font-style:italic;font-weight:600}"; el.appendChild(st);
    var sel = el.querySelector("#jt"), ck = el.querySelector("#ji");
    function calc() {
      tipo = sel.value; inv = ck.checked;
      // esquerda = cliente (ou pedido se invertido)
      var L = inv ? PED.map(function (p) { return { k: p[1], v: [p[0], p[1]] }; }) : CLI.map(function (c) { return { k: c[0], v: [c[0], c[1]] }; });
      var R = inv ? CLI.map(function (c) { return { k: c[0], v: [c[0], c[1]] }; }) : PED.map(function (p) { return { k: p[1], v: [p[0], p[1]] }; });
      var nl = inv ? "pedido" : "cliente", nr = inv ? "cliente" : "pedido";
      var hl = inv ? ["idPedido", "idCliente"] : ["idCliente", "Nome"], hr = inv ? ["idCliente", "Nome"] : ["idPedido", "idCliente"];
      el.querySelector("#la").textContent = "Esquerda: " + nl; el.querySelector("#lb").textContent = "Direita: " + nr;
      function tab(h, rows) { return "<tr>" + h.map(function (x) { return "<th>" + x + "</th>"; }).join("") + "</tr>" + rows.map(function (r) { return "<tr>" + r.v.map(function (x) { return "<td>" + x + "</td>"; }).join("") + "</tr>"; }).join(""); }
      el.querySelector(".ta").innerHTML = tab(hl, L); el.querySelector(".tb").innerHTML = tab(hr, R);
      var res = [], usedR = {};
      L.forEach(function (l) {
        var m = R.filter(function (r, i) { return r.k === l.k; });
        m.forEach(function (r) { res.push({ l: l.v, r: r.v }); usedR[R.indexOf(r)] = 1; });
        if (!m.length && (tipo === "LEFT" || tipo === "FULL")) res.push({ l: l.v, r: [null, null] });
      });
      if (tipo === "RIGHT" || tipo === "FULL") R.forEach(function (r, i) { if (!usedR[i]) res.push({ l: [null, null], r: r.v }); });
      // as chaves iguais são a coluna idCliente: o 1º do pedido (inv) ou do cliente
      el.querySelector(".jq").textContent = "SELECT * FROM " + nl + " A\n" + (tipo === "FULL" ? "FULL OUTER" : tipo) + " JOIN " + nr + " B ON A.idCliente = B.idCliente;" + (tipo === "FULL" ? "\n-- no MySQL não existe FULL JOIN: simule com LEFT JOIN + UNION + RIGHT JOIN" : "");
      el.querySelector(".tr").innerHTML = "<tr>" + hl.map(function (x) { return "<th>A." + x + "</th>"; }).join("") + hr.map(function (x) { return "<th>B." + x + "</th>"; }).join("") + "</tr>" +
        res.map(function (r) { return "<tr>" + r.l.concat(r.r).map(function (x) { return "<td>" + esc(x) + "</td>"; }).join("") + "</tr>"; }).join("");
      var texto = { INNER: "só as linhas que têm par dos dois lados.", LEFT: "todas as linhas da esquerda; quem não tem par na direita vem com NULL.", RIGHT: "todas as linhas da direita; quem não tem par na esquerda vem com NULL.", FULL: "todas as linhas dos dois lados; o que não tem par vem com NULL." }[tipo];
      el.querySelector(".read").innerHTML = "<b>" + tipo + " JOIN</b>: " + texto + " Resultado: <b>" + res.length + " linha" + (res.length === 1 ? "" : "s") + "</b>." + (tipo === "INNER" ? " Roberto, Mariana e Miguel nunca fizeram pedido, então somem." : "");
    }
    sel.addEventListener("change", calc); ck.addEventListener("change", calc); calc();
  };
})();
