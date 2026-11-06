/* Demo do capítulo 1: um terminal de brincadeira, com sistema de arquivos falso (nada do seu computador é tocado). */
(function () {
  var E = window.Estudo, TG = E.tg, esc = TG.esc;

  E.demos.terminalSim = function (el) {
    TG.estilo();
    var sh = new TG.Shell(), hist = [], hpos = 0;
    var SUGESTOES = ["pwd", "ls", "ls -la", "cat tarefas.txt", "cd projeto", "cd ..", "grep ERRO log.txt", "wc -l vendas.csv", "mkdir backup", "cp tarefas.txt backup", "ls backup", "echo oi > novo.txt", "cat novo.txt", "rm novo.txt", "ls nao_existe", "man ls"];
    el.innerHTML = '<h4>Um terminal de mentira (de verdade, só o aprendizado)</h4>' +
      '<p class="muted" style="margin:0 0 6px">Os arquivos são falsos e vivem só nesta página: pode errar e apagar à vontade. Digite um comando e aperte Enter, ou clique numa sugestão. As setas para cima e para baixo repetem comandos. Digite <code>help</code> para ver a lista do que o simulador conhece.</p>' +
      '<div class="tgchips"></div>' +
      '<div class="tgterm"><div class="tgout" aria-live="polite" tabindex="0"></div><div class="tgin"><span class="tgp"></span><input type="text" spellcheck="false" autocomplete="off" autocapitalize="off" aria-label="Linha de comando"></div></div>' +
      '<div class="ctrls"><button class="btn sm" type="button" data-a="reset">Recomeçar</button><button class="btn sm" type="button" data-a="clear">Limpar a tela</button></div>';
    var out = el.querySelector(".tgout"), inp = el.querySelector("input"), pr = el.querySelector(".tgp"), chips = el.querySelector(".tgchips");
    chips.innerHTML = SUGESTOES.map(function (s) { return '<button type="button" data-c="' + esc(s) + '">' + esc(s) + '</button>'; }).join("");
    function add(html) { out.insertAdjacentHTML("beforeend", html); out.scrollTop = out.scrollHeight; }
    function prompt() { pr.textContent = sh.prompt(); }
    function exec(l) {
      add('<span class="tgps">' + esc(sh.prompt()) + '</span> ' + esc(l) + '\n');
      if (l.trim()) { hist.push(l); hpos = hist.length; }
      var r = sh.run(l);
      if (r.clear) { out.innerHTML = ""; }
      if (r.out) add(esc(r.out));
      if (r.err) add('<span class="tgerr">' + esc(r.err) + '</span>');
      prompt();
    }
    function reset() { sh = new TG.Shell(); out.innerHTML = ""; add('<span class="tgok">Terminal simulado. Você começa na pasta estudo. Experimente: ls</span>\n'); prompt(); }
    inp.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { var l = inp.value; inp.value = ""; exec(l); }
      else if (e.key === "ArrowUp") { if (hpos > 0) { hpos--; inp.value = hist[hpos]; } e.preventDefault(); }
      else if (e.key === "ArrowDown") { if (hpos < hist.length - 1) { hpos++; inp.value = hist[hpos]; } else { hpos = hist.length; inp.value = ""; } e.preventDefault(); }
    });
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b || !el.contains(b)) return;
      if (b.hasAttribute("data-c")) { exec(b.getAttribute("data-c")); inp.focus({ preventScroll: true }); }
      else if (b.getAttribute("data-a") === "reset") reset();
      else if (b.getAttribute("data-a") === "clear") out.innerHTML = "";
    });
    reset();
  };
})();
