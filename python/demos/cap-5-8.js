/* Demos dos capítulos 5 a 8 da apostila de Python */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- cap 5: adivinhação de 1 a 10 com 3 tentativas ---- */
  E.demos.guess = function (el) {
    var segredo, tent;
    el.innerHTML = '<h4>Adivinhe o número de 1 a 10 (3 tentativas)</h4><div class="ctrls"><input type="number" id="gn" min="1" max="10" placeholder="1 a 10" style="width:100px"><button class="btn sm pri" type="button" id="gb">Chutar</button><button class="btn sm" type="button" id="gr">Novo jogo</button></div><div class="read"></div>' +
      '<pre class="jq" style="margin:8px 0">segredo = random.randint(1, 10)\ntentativas = 0\nwhile tentativas &lt; 3:\n    palpite = int(input("Seu palpite: "))\n    tentativas += 1\n    if palpite == segredo:\n        print("Acertou!")\n        break\n    elif palpite &lt; segredo:\n        print("Maior")\n    else:\n        print("Menor")\nelse:\n    print("Acabaram as tentativas")</pre>';
    var rd = el.querySelector(".read"), gn = el.querySelector("#gn"), over = false;
    function reset() { segredo = 1 + Math.floor(Math.random() * 10); tent = 0; over = false; rd.innerHTML = "Pensei em um número. Você tem <b>3</b> tentativas. (O <code>while</code> repete enquanto <code>tentativas &lt; 3</code>.)"; gn.value = ""; }
    function chuta() {
      if (over) return; var p = parseInt(gn.value, 10); if (isNaN(p)) return; tent++;
      var msg;
      if (p === segredo) { msg = "<b style='color:var(--green)'>Acertou!</b> Em " + tent + " tentativa" + (tent > 1 ? "s" : "") + ". O <code>break</code> sai do laço."; over = true; }
      else { msg = "<b>" + (p < segredo ? "Maior" : "Menor") + "</b> do que " + p + ". Tentativa " + tent + " de 3."; if (tent >= 3) { msg += " <b style='color:var(--red)'>Acabaram as tentativas.</b> Era " + segredo + ": o <code>else</code> do <code>while</code> roda quando o laço termina <i>sem</i> break."; over = true; } }
      rd.innerHTML = msg; gn.value = ""; gn.focus();
    }
    el.querySelector("#gb").addEventListener("click", chuta); gn.addEventListener("keydown", function (e) { if (e.key === "Enter") chuta(); }); el.querySelector("#gr").addEventListener("click", reset); reset();
  };

  /* ---- cap 6: matriz ---- */
  E.demos.matriz = function (el) {
    var M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], sel = [1, 2], timer = 0;
    el.innerHTML = '<h4>Matriz[y][x]: primeiro a linha, depois a coluna</h4><div class="mx" style="display:grid;grid-template-columns:repeat(3,64px);gap:6px;margin:10px 0"></div>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" data-m="walk">▶ Percorrer com for aninhado</button><button class="btn sm" type="button" data-m="append">matriz.append([10, 11, 12])</button><button class="btn sm" type="button" data-m="reset">Reiniciar</button></div><pre class="jq" style="margin:8px 0"></pre><div class="read"></div>';
    var box = el.querySelector(".mx"), jq = el.querySelector(".jq"), rd = el.querySelector(".read");
    function draw(hl) {
      var cols = M[0].length; box.style.gridTemplateColumns = "repeat(" + cols + ",64px)";
      var h = ""; M.forEach(function (r, y) { r.forEach(function (v, x) { var on = hl ? (hl[0] === y && hl[1] === x) : (sel[0] === y && sel[1] === x); h += '<button type="button" data-y="' + y + '" data-x="' + x + '" style="padding:14px 0;border:2px solid var(--' + (on ? "c1" : "ink") + ');border-radius:10px;background:var(--' + (on ? "hl-y" : "card") + ');font:700 1.2rem var(--f-head);color:var(--ink);transition:.2s">' + v + '<br><small class="muted" style="font:400 .68rem var(--f-mono)">[' + y + '][' + x + ']</small></button>'; }); }); box.innerHTML = h;
    }
    function info() { jq.textContent = "matriz[" + sel[0] + "][" + sel[1] + "]   # -> " + M[sel[0]][sel[1]]; rd.innerHTML = "<code>y</code> = linha (" + sel[0] + "), <code>x</code> = coluna (" + sel[1] + "). Os dois índices <b>começam em 0</b>. Uma matriz é uma <b>lista de listas</b>: <code>matriz[" + sel[0] + "]</code> é a linha inteira (" + JSON.stringify(M[sel[0]]) + ") e <code>[" + sel[1] + "]</code> escolhe o elemento dela."; draw(); }
    el.addEventListener("click", function (e) {
      var c = e.target.closest("button[data-y]"); if (c) { clearInterval(timer); sel = [+c.getAttribute("data-y"), +c.getAttribute("data-x")]; info(); return; }
      var b = e.target.closest("button[data-m]"); if (!b) return; var m = b.getAttribute("data-m");
      if (m === "reset") { clearInterval(timer); M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]; sel = [1, 2]; info(); }
      if (m === "append") { if (M.length < 4) M.push([10, 11, 12]); sel = [Math.min(sel[0], M.length - 1), sel[1]]; info(); }
      if (m === "walk") {
        clearInterval(timer); var cells = []; for (var y = 0; y < M.length; y++) for (var x = 0; x < M[0].length; x++) cells.push([y, x]); var i = 0, out = [];
        timer = setInterval(function () { if (i >= cells.length) { clearInterval(timer); rd.innerHTML = "Fim do laço. Saída: <b>" + out.join(" ") + "</b>."; draw(); return; } var c2 = cells[i++]; out.push(M[c2[0]][c2[1]]); jq.textContent = "for y in range(" + M.length + "):\n    for x in range(" + M[0].length + "):\n        print(matriz[y][x])   # y=" + c2[0] + ", x=" + c2[1] + " -> " + M[c2[0]][c2[1]]; rd.innerHTML = "O <code>for</code> de fora escolhe a linha; o de dentro anda pelas colunas dela. Saída até agora: <b>" + out.join(" ") + "</b>"; draw(c2); }, E.reduce ? 10 : 600);
      }
    });
    info();
  };

  /* ---- cap 7: simulador de Git ---- */
  E.demos.gitsim = function (el) {
    var st; function init() { st = { work: { "README.md": "v1" }, edited: false, staged: false, local: [{ msg: "primeiro commit", id: "a1b2c3" }], remote: [{ msg: "primeiro commit", id: "a1b2c3" }], ver: 1, msg: "Você tem um repositório com 1 commit, já enviado ao GitHub." }; }
    init();
    el.innerHTML = '<h4>O caminho de uma mudança: do seu disco até o GitHub</h4><div class="grid2 gz" style="margin:8px 0"></div><div class="ctrls"><button class="btn sm" type="button" data-g="edit">✎ Editar README.md</button><button class="btn sm pri" type="button" data-g="add">git add .</button><button class="btn sm pri" type="button" data-g="commit">git commit -m "..."</button><button class="btn sm pri" type="button" data-g="push">git push</button><button class="btn sm" type="button" data-g="reset">Reiniciar</button></div><div class="read"></div>';
    var gz = el.querySelector(".gz"), rd = el.querySelector(".read");
    function zone(t, sub, body, hot) { return '<div class="card" style="margin:0;border:2px solid var(--' + (hot ? "c1" : "line") + ');transition:.3s"><b>' + t + '</b><br><small class="muted">' + sub + '</small><div style="margin-top:8px;font:.85rem var(--f-mono)">' + body + '</div></div>'; }
    function log(a) { return a.slice().reverse().map(function (c) { return "● " + c.id + " " + esc(c.msg); }).join("<br>"); }
    function draw() {
      gz.innerHTML =
        zone("1. Seu disco", "diretório de trabalho", "README.md (v" + st.ver + ")" + (st.edited ? ' <span style="color:var(--red)">● modificado</span>' : ""), st.edited && !st.staged) +
        zone("2. Staging", "área de preparação", st.staged ? "README.md (v" + st.ver + ") <span style=\"color:var(--green)\">pronto para o commit</span>" : '<span class="muted">vazio</span>', st.staged) +
        zone("3. Repositório local", "seus commits (histórico)", log(st.local), false) +
        zone("4. GitHub", "repositório remoto (nuvem)", log(st.remote), st.local.length !== st.remote.length);
      rd.innerHTML = st.msg;
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-g]"); if (!b) return; var a = b.getAttribute("data-g");
      if (a === "reset") { init(); }
      if (a === "edit") { st.ver++; st.edited = true; if (st.staged) st.dirty = true; st.msg = st.staged ? "Você alterou o arquivo <b>depois</b> do <code>git add</code>. A versão adicionada continua na staging, e a mudança nova está só na pasta: seria preciso um novo <code>git add</code> para incluí-la." : "Você alterou o arquivo. O Git percebeu, mas <b>ainda não guardou nada</b>."; }
      if (a === "add") { if (!st.edited) st.msg = "Nada para adicionar: não há mudanças. Edite o arquivo primeiro."; else { st.staged = true; st.dirty = false; st.msg = "<code>git add .</code> move a mudança para a <b>staging</b>: você escolhe o que entra no próximo commit."; } }
      if (a === "commit") { if (!st.staged) st.msg = "Nada na staging. <code>git commit</code> só registra o que passou pelo <code>git add</code>."; else { var id = Math.random().toString(16).slice(2, 8); st.local.push({ msg: "atualiza README (v" + st.ver + ")", id: id }); st.staged = false; st.edited = !!st.dirty; st.dirty = false; st.msg = "<code>git commit -m \"...\"</code> tira uma <b>foto</b> com a mensagem. Fica só no seu computador."; } }
      if (a === "push") { if (st.local.length === st.remote.length) st.msg = "Nada para enviar: o GitHub já tem todos os seus commits."; else { st.remote = st.local.slice(); st.msg = "<code>git push</code> envia os commits para o GitHub. Agora há backup e dá para compartilhar."; } }
      draw();
    });
    draw();
  };

  /* ---- cap 8: o cofre (bom / ótimo) ---- */
  function pistas(s, c) { var o = 0, cs = {}, cc = {}, i; for (i = 0; i < 4; i++) { if (s[i] === c[i]) o++; cs[s[i]] = (cs[s[i]] || 0) + 1; cc[c[i]] = (cc[c[i]] || 0) + 1; } var com = 0; Object.keys(cc).forEach(function (k) { if (cs[k]) com += Math.min(cs[k], cc[k]); }); return [o, com - o]; }
  var TODAS = []; (function () { for (var i = 0; i < 10000; i++) TODAS.push(("000" + i).slice(-4)); })();
  function filtra(c, chute, r) { return c.filter(function (x) { var p = pistas(x, chute); return p[0] === r[0] && p[1] === r[1]; }); }

  E.demos.cofrepistas = function (el) {
    el.innerHTML = '<h4>Como o cofre responde</h4><div class="ctrls"><label>senha <input type="text" id="cs" value="4071" maxlength="4" style="width:80px;font-family:var(--f-mono)"></label><label>chute <input type="text" id="cg" value="0111" maxlength="4" style="width:80px;font-family:var(--f-mono)"></label></div><div class="read"></div>';
    var cs = el.querySelector("#cs"), cg = el.querySelector("#cg"), rd = el.querySelector(".read");
    function go() { if (!/^\d{4}$/.test(cs.value) || !/^\d{4}$/.test(cg.value)) { rd.textContent = "Digite 4 dígitos nos dois campos."; return; } var p = pistas(cs.value, cg.value); rd.innerHTML = "Resposta: <b style='color:var(--green)'>" + p[0] + " ótimo(s)</b> (dígito certo na posição certa) e <b style='color:var(--c1)'>" + p[1] + " bom(ns)</b> (dígito existe, mas em outra posição). O cofre <b>não diz qual</b> dígito gerou cada pista."; }
    cs.addEventListener("input", go); cg.addEventListener("input", go); go();
  };

  E.demos.cofrejogo = function (el) {
    var seg, hist, cand;
    el.innerHTML = '<h4>Descubra a senha de 4 dígitos</h4><div class="ctrls"><input type="text" id="jg" maxlength="4" placeholder="4 dígitos" style="width:110px;font-family:var(--f-mono)"><button class="btn sm pri" type="button" id="jb">Chutar</button><button class="btn sm" type="button" id="jn">Nova senha</button><label><input type="checkbox" id="jh"> mostrar quantas senhas ainda são possíveis</label></div><div class="tablewrap"><table class="jt"></table></div><div class="read"></div>';
    var jg = el.querySelector("#jg"), jt = el.querySelector(".jt"), rd = el.querySelector(".read"), jh = el.querySelector("#jh");
    function novo() { seg = TODAS[Math.floor(Math.random() * 10000)]; hist = []; cand = TODAS; jg.value = ""; draw(); rd.innerHTML = "O cofre sorteou uma senha. Há <b>10.000</b> possibilidades (0000 a 9999)."; }
    function draw() { jt.innerHTML = hist.length ? '<tr><th>#</th><th>chute</th><th>ótimo</th><th>bom</th>' + (jh.checked ? '<th>ainda possíveis</th>' : '') + '</tr>' + hist.map(function (h, i) { return '<tr><td>' + (i + 1) + '</td><td><code>' + h.c + '</code></td><td>' + h.r[0] + '</td><td>' + h.r[1] + '</td>' + (jh.checked ? '<td>' + E.fmt(h.n) + '</td>' : '') + '</tr>'; }).join("") : ""; }
    function chuta() {
      var c = jg.value; if (!/^\d{4}$/.test(c)) { rd.textContent = "Digite exatamente 4 dígitos."; return; } if (hist.length && hist[hist.length - 1].r[0] === 4) return;
      var r = pistas(seg, c); cand = filtra(cand, c, r); hist.push({ c: c, r: r, n: cand.length }); jg.value = ""; draw();
      rd.innerHTML = r[0] === 4 ? "<b style='color:var(--green)'>Abriu!</b> A senha era " + seg + ", em " + hist.length + " tentativas. Um algoritmo que sempre chuta uma senha ainda possível resolve em média cerca de 9." : "Resposta: " + r[0] + " ótimo(s) e " + r[1] + " bom(ns). Anote o chute e a resposta: a próxima senha precisa ser compatível com <b>todas</b> as respostas até aqui.";
    }
    el.querySelector("#jb").addEventListener("click", chuta); jg.addEventListener("keydown", function (e) { if (e.key === "Enter") chuta(); }); el.querySelector("#jn").addEventListener("click", novo); jh.addEventListener("change", draw); novo();
  };

  E.demos.cofresolver = function (el) {
    el.innerHTML = '<h4>Deixe o algoritmo resolver</h4><div class="ctrls"><label>senha <input type="text" id="ss" value="4071" maxlength="4" style="width:80px;font-family:var(--f-mono)"></label><button class="btn sm pri" type="button" id="sb">▶ Resolver passo a passo</button></div><div class="tablewrap"><table class="st"></table></div><div class="read"></div>';
    var ss = el.querySelector("#ss"), tb = el.querySelector(".st"), rd = el.querySelector(".read"), timer = 0;
    el.querySelector("#sb").addEventListener("click", function () {
      clearInterval(timer); var s = ss.value; if (!/^\d{4}$/.test(s)) { rd.textContent = "Digite 4 dígitos."; return; }
      var cand = TODAS, rows = []; tb.innerHTML = '<tr><th>#</th><th>chute</th><th>ótimo</th><th>bom</th><th>possíveis antes do chute</th></tr>'; rd.innerHTML = "Regra: chutar sempre a <b>primeira</b> senha que ainda é possível, e descartar as que não dariam a mesma resposta.";
      timer = setInterval(function () {
        var ch = cand[0], r = pistas(s, ch), n = cand.length; rows.push(ch);
        tb.insertAdjacentHTML("beforeend", '<tr><td>' + rows.length + '</td><td><code>' + ch + '</code></td><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + E.fmt(n) + '</td></tr>');
        if (r[0] === 4) { clearInterval(timer); rd.innerHTML = "<b style='color:var(--green)'>Abriu em " + rows.length + " tentativas.</b> Cada resposta eliminou muitas hipóteses: de " + E.fmt(TODAS.length) + " para 1." + (s === "4071" ? " (Para 4071 o resultado conferido no Python também é 8 tentativas.)" : ""); return; }
        cand = filtra(cand, ch, r);
      }, E.reduce ? 10 : 700);
    });
  };
})();
