/* Demo do capítulo 8 (banco de dados): injeção de SQL de verdade, sobre a base alpha */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t == null ? "NULL" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  E.demos.inject = function (el) {
    el.innerHTML = '<h4>Uma tela de busca por nome (e um atacante)</h4>' +
      '<div class="ctrls"><label>nome <input type="text" id="in" value="Ana" style="min-width:220px;font-family:var(--f-mono)"></label>' +
      '<label><input type="checkbox" id="pp"> consulta parametrizada (segura)</label></div>' +
      '<div class="ctrls"><span class="muted">Tente:</span><button class="btn sm" type="button" data-v="Ana">um nome normal</button><button class="btn sm" type="button" data-v="\' OR \'1\'=\'1">\' OR \'1\'=\'1</button><button class="btn sm" type="button" data-v="Ana\'; DROP TABLE Funcionario; --">DROP TABLE</button></div>' +
      '<pre class="jq" style="margin:8px 0"></pre><div class="sqlres"></div><div class="read"></div>';
    var inp = el.querySelector("#in"), pp = el.querySelector("#pp"), jq = el.querySelector(".jq"), res = el.querySelector(".sqlres"), rd = el.querySelector(".read"), SQL = null;
    function newDb() { var d = new SQL.Database(); d.run(E.sqlDBs.alpha); return d; }
    function go() {
      if (!SQL) return; var db = newDb(), v = inp.value, rows = null, err = null, q;
      try {
        if (pp.checked) { q = "SELECT idFuncionario, nome FROM Funcionario WHERE nome = ?   -- valor entregue à parte: " + JSON.stringify(v); var st = db.prepare("SELECT idFuncionario, nome FROM Funcionario WHERE nome = ?"); st.bind([v]); rows = []; while (st.step()) rows.push(st.get()); st.free(); }
        else { q = "SELECT idFuncionario, nome FROM Funcionario WHERE nome = '" + v + "'"; var out = db.exec(q); rows = out.length ? out[0].values : []; }
      } catch (e) { err = e.message; }
      jq.textContent = (pp.checked ? "-- o SQL é fixo; o texto digitado vira só um valor\n" : "-- o texto digitado foi colado dentro do SQL\n") + q;
      var count = "";
      try { count = db.exec("SELECT COUNT(*) FROM Funcionario")[0].values[0][0]; } catch (e) { count = "a tabela não existe mais"; } var dropped = (typeof count === "string"); db.close();
      res.innerHTML = err ? '<div class="sqlerr">' + esc(err) + '</div>' : '<table><tr><th>idFuncionario</th><th>nome</th></tr>' + rows.slice(0, 8).map(function (r) { return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td></tr>'; }).join("") + '</table><p class="muted" style="margin:4px 0">' + rows.length + ' linha' + (rows.length === 1 ? "" : "s") + (rows.length > 8 ? " (mostrando 8)" : "") + '</p>';
      var ruim = !pp.checked && rows && rows.length > 1;
      rd.innerHTML = (dropped && !pp.checked) ? "<b style='color:var(--red)'>Destruiu:</b> o texto digitado carregava um segundo comando, <code>DROP TABLE</code>, e o banco o executou: <b>a tabela Funcionario não existe mais</b>. Marque a consulta parametrizada para ver o ataque falhar." : pp.checked ? "<b>Parametrizada:</b> o banco trata o texto inteiro como <i>um nome</i>. Nenhum funcionário se chama assim, então volta " + rows.length + " linha(s). Funcionários na tabela: <b>" + count + "</b>." :
        (ruim ? "<b style='color:var(--red)'>Vazou:</b> a condição <code>'1'='1'</code> é sempre verdadeira, e a busca devolveu <b>" + rows.length + "</b> funcionários em vez de um." : "Busca normal: devolveu " + rows.length + " linha(s).") + " Funcionários na tabela: <b>" + count + "</b>.";
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-v]"); if (b) { inp.value = b.getAttribute("data-v"); go(); } });
    inp.addEventListener("input", go); pp.addEventListener("change", go);
    E.loadSql().then(function (S) { SQL = S; go(); }, function (err) { res.innerHTML = '<div class="sqlerr">' + esc(err.message) + '</div>'; });
  };
})();
