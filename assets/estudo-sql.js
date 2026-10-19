/* ==========================================================
   estudo-sql.js | SQL de verdade no navegador (SQLite via sql.js)
   Uso:
     Estudo.sqlDBs.alpha = "CREATE TABLE ...; INSERT ...;";        // registra uma base
     <div class="demo" data-demo="sql" data-db="alpha" data-expect="17" data-titulo="...">
        <pre class="q">SELECT * FROM Funcionario;</pre>
     </div>
   data-expect (opcional): número de linhas esperado no último SELECT; mostra um aviso quando bate.
   Observação: o navegador roda SQLite. Os comandos das aulas (SELECT, JOIN, GROUP BY, INSERT...) são os mesmos
   do MySQL; as diferenças estão marcadas no texto de cada capítulo.
   ========================================================== */
(function () {
  "use strict";
  var E = window.Estudo; if (!E) return;
  E.sqlDBs = E.sqlDBs || {};
  var CDN = "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/", loading = null;

  function loadSql() {
    if (loading) return loading;
    loading = new Promise(function (res, rej) {
      var s = document.createElement("script"); s.src = CDN + "sql-wasm.js";
      s.onload = function () { window.initSqlJs({ locateFile: function (f) { return CDN + f; } }).then(res, rej); };
      s.onerror = function () { rej(new Error("não consegui baixar o sql.js (sem internet?)")); };
      document.head.appendChild(s);
    });
    return loading;
  }
  E.loadSql = loadSql;
  function esc(t) { return String(t == null ? "NULL" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  E.demos.sql = function (el) {
    var qe = el.querySelector(".q"), q0 = (qe ? qe.textContent.replace(/copiar$/, "") : "SELECT 1;").trim(), dbName = el.getAttribute("data-db"),
        expect = el.getAttribute("data-expect"), titulo = el.getAttribute("data-titulo") || "Rode o SQL aqui";
    el.innerHTML = '<h4>' + esc(titulo) + '</h4><div class="sqlbox"><textarea spellcheck="false" aria-label="Comando SQL"></textarea></div>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" data-s="run">▶ Executar</button><button class="btn sm" type="button" data-s="reset">Reiniciar a base</button><button class="btn sm" type="button" data-s="orig">Voltar o comando original</button><span class="muted sqlst">carregando o SQL...</span></div>' +
      '<div class="sqlres" aria-live="polite"></div>';
    var ta = el.querySelector("textarea"), res = el.querySelector(".sqlres"), st = el.querySelector(".sqlst"), db = null, SQL = null;
    ta.value = q0;
    function open() {
      if (db) db.close();
      db = new SQL.Database(); db.run("PRAGMA foreign_keys = ON;"); db.run(E.sqlDBs[dbName] || "");
      st.textContent = "base \"" + dbName + "\" pronta";
    }
    function run() {
      if (!SQL) return; res.innerHTML = "";
      try {
        var out = db.exec(ta.value), msg = "";
        if (!out.length) { var ch = db.getRowsModified(); res.innerHTML = '<p class="sqlok">Comando executado com sucesso' + (ch ? " (" + ch + " linha" + (ch > 1 ? "s" : "") + " afetada" + (ch > 1 ? "s" : "") + ")" : "") + '.</p>'; return; }
        out.forEach(function (r) {
          res.insertAdjacentHTML("beforeend", '<table><tr>' + r.columns.map(function (c) { return '<th>' + esc(c) + '</th>'; }).join("") + '</tr>' +
            r.values.slice(0, 300).map(function (row) { return '<tr>' + row.map(function (v) { return '<td>' + esc(v) + '</td>'; }).join("") + '</tr>'; }).join("") + '</table><p class="muted" style="margin:4px 0 12px">' + r.values.length + ' linha' + (r.values.length === 1 ? "" : "s") + (r.values.length > 300 ? " (mostrando 300)" : "") + '</p>');
        });
        if (el.hasAttribute("data-bar")) {
          var r0 = out[0], nums = r0.values.map(function (r) { return Number(r[r.length - 1]); });
          if (r0.columns.length >= 2 && nums.every(function (v) { return !isNaN(v); })) {
            var mx = Math.max.apply(null, nums) || 1;
            res.insertAdjacentHTML("beforeend", '<div class="bars">' + r0.values.map(function (r, i) { return '<div class="bar"><div>' + esc(r.slice(0, -1).join(" · ")) + '</div><div class="tr"><div class="fl" style="width:' + (nums[i] / mx * 100).toFixed(1) + '%"></div></div><div class="v">' + esc(nums[i]) + '</div></div>'; }).join("") + '</div>');
          }
        }
        if (expect !== null && expect !== "") {
          var last = out[out.length - 1].values.length;
          if (String(last) === expect) res.insertAdjacentHTML("beforeend", '<p class="sqlok">✓ Bateu com o esperado: ' + expect + ' linha' + (expect === "1" ? "" : "s") + '.</p>');
        }
      } catch (e) { res.innerHTML = '<div class="sqlerr">' + esc(e.message) + '</div>'; }
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-s]"); if (!b || !SQL) return; var a = b.getAttribute("data-s");
      if (a === "run") run(); if (a === "reset") { open(); res.innerHTML = '<p class="sqlok">Base reiniciada.</p>'; } if (a === "orig") { ta.value = q0; }
    });
    ta.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); run(); }
      if (e.key === "Tab") { e.preventDefault(); var s = ta.selectionStart; ta.value = ta.value.slice(0, s) + "  " + ta.value.slice(ta.selectionEnd); ta.selectionStart = ta.selectionEnd = s + 2; }
    });
    loadSql().then(function (S) { SQL = S; open(); run(); }, function (err) { st.textContent = ""; res.innerHTML = '<div class="sqlerr">' + esc(err.message) + '</div>'; });
  };
})();
