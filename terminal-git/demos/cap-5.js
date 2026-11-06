/* Demo do capítulo 5: grafo de commits e branches que reage a comandos git.
   Simplificações: os identificadores são c1, c2... (no Git de verdade são hashes de 40 caracteres) e não há conflito nem arquivos.
   A lógica fica em Estudo.tggit (sem DOM) para poder ser conferida fora do navegador. */
(function () {
  var E = window.Estudo, TG = E.tg || {}, G = E.tggit = {};
  function esc(t) { return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  G.novo = function () {
    return { commits: [{ id: "c1", msg: "primeiro commit", pais: [], faixa: 0 }], branches: { main: "c1" }, head: "main" };
  };
  function acha(r, id) { for (var i = 0; i < r.commits.length; i++) if (r.commits[i].id === id) return r.commits[i]; return null; }
  /* conjunto de ancestrais (incluindo o próprio commit) */
  G.ancestrais = function (r, id) {
    var vistos = {}, pilha = [id];
    while (pilha.length) { var x = pilha.pop(); if (vistos[x]) continue; vistos[x] = 1; acha(r, x).pais.forEach(function (p) { pilha.push(p); }); }
    return vistos;
  };
  /* guarda no próprio commit a faixa em que ele foi desenhado ao nascer: se a branch for apagada depois, o commit não cai na faixa 0 */
  function marca(r, id) { acha(r, id).faixa = G.faixas(r)[id]; }
  function tokens(l) {
    var out = [], re = /"([^"]*)"|'([^']*)'|(\S+)/g, m;
    while ((m = re.exec(l))) out.push(m[1] !== undefined ? m[1] : m[2] !== undefined ? m[2] : m[3]);
    return out;
  }
  /* Executa um comando git sobre o repositório r. Devolve o texto que o git mostraria. */
  G.exec = function (r, linha) {
    var t = tokens(linha.trim());
    if (!t.length) return { ok: true, txt: "" };
    if (t[0] !== "git") return { ok: false, txt: "Aqui só vale comando git. Exemplo: git commit -m \"mensagem\"" };
    var cmd = t[1], tip = r.branches[r.head];
    if (cmd === "commit") {
      var i = t.indexOf("-m"), im = i < 0 ? t.indexOf("-am") : i;
      if (im < 0 || !t[im + 1]) return { ok: false, txt: "Falta a mensagem: git commit -m \"o que mudou\"" };
      var id = "c" + (r.commits.length + 1);
      r.commits.push({ id: id, msg: t[im + 1], pais: [tip] }); r.branches[r.head] = id; marca(r, id);
      return { ok: true, txt: "[" + r.head + " " + id + "] " + t[im + 1] };
    }
    if (cmd === "branch") {
      if (t.length === 2) return { ok: true, txt: Object.keys(r.branches).sort().map(function (b) { return (b === r.head ? "* " : "  ") + b; }).join("\n") };
      var flag = t[2].charAt(0) === "-" ? t[2] : null;
      if (flag === "-d" || flag === "-D") {
        var nome = t[3];
        if (!nome) return { ok: false, txt: "fatal: branch name required" };
        if (!r.branches[nome]) return { ok: false, txt: "error: branch '" + nome + "' not found" };
        if (nome === r.head) return { ok: false, txt: "error: cannot delete branch '" + nome + "' used by worktree (você está nela)" };
        if (flag === "-d" && !G.ancestrais(r, tip)[r.branches[nome]]) return { ok: false, txt: "error: the branch '" + nome + "' is not fully merged (se tiver certeza, use -D)" };
        var onde = r.branches[nome]; delete r.branches[nome];
        return { ok: true, txt: "Deleted branch " + nome + " (was " + onde + ")." };
      }
      if (flag) return { ok: false, txt: "error: unknown switch '" + flag + "' (o simulador só entende -d e -D)" };
      if (r.branches[t[2]]) return { ok: false, txt: "fatal: a branch named '" + t[2] + "' already exists" };
      r.branches[t[2]] = tip; return { ok: true, txt: "" };
    }
    if (cmd === "switch" || cmd === "checkout") {
      var criar = t[2] === "-c" || t[2] === "-b", alvo = criar ? t[3] : t[2];
      if (!alvo) return { ok: false, txt: "Diga para qual branch: git switch nome" };
      if (alvo.charAt(0) === "-") return { ok: false, txt: "error: unknown switch '" + alvo + "' (o simulador só entende -c)" };
      if (criar) {
        if (r.branches[alvo]) return { ok: false, txt: "fatal: a branch named '" + alvo + "' already exists" };
        r.branches[alvo] = tip; r.head = alvo; return { ok: true, txt: "Switched to a new branch '" + alvo + "'" };
      }
      if (!r.branches[alvo]) return { ok: false, txt: "fatal: invalid reference: " + alvo };
      r.head = alvo; return { ok: true, txt: "Switched to branch '" + alvo + "'" };
    }
    if (cmd === "merge") {
      var outra = t[2];
      if (!outra || !r.branches[outra]) return { ok: false, txt: "merge: " + outra + " - not something we can merge" };
      var alvoId = r.branches[outra];
      if (G.ancestrais(r, tip)[alvoId]) return { ok: true, txt: "Already up to date." };
      if (G.ancestrais(r, alvoId)[tip]) { r.branches[r.head] = alvoId; return { ok: true, txt: "Fast-forward (nenhum commit novo: " + r.head + " só andou até " + alvoId + ")" }; }
      var nid = "c" + (r.commits.length + 1);
      r.commits.push({ id: nid, msg: "Merge branch '" + outra + "'", pais: [tip, alvoId] }); r.branches[r.head] = nid; marca(r, nid);
      return { ok: true, txt: "Merge made by the 'ort' strategy. (novo commit " + nid + " com 2 pais: " + tip + " e " + alvoId + ")" };
    }
    if (cmd === "log") {
      var vis = G.ancestrais(r, tip);
      return { ok: true, txt: r.commits.filter(function (c) { return vis[c.id]; }).reverse().map(function (c) { return c.id + " " + c.msg; }).join("\n") };
    }
    if (cmd === "status") return { ok: true, txt: "On branch " + r.head };
    return { ok: false, txt: "O simulador conhece: commit -m, branch [nome | -d nome | -D nome], switch [-c] nome, merge nome, log e status." };
  };

  /* faixas (linhas) do desenho: a cadeia do primeiro pai de main fica na faixa 0; as demais branches ocupam as faixas seguintes */
  G.faixas = function (r) {
    var faixa = {}, prox = 1, nomes = Object.keys(r.branches).sort(function (a, b) { return a === "main" ? -1 : b === "main" ? 1 : a < b ? -1 : 1; });
    nomes.forEach(function (n) {
      var id = r.branches[n], lane = n === "main" ? 0 : null;
      if (faixa[id] !== undefined) return;
      if (lane === null) lane = prox++;
      while (id && faixa[id] === undefined) { faixa[id] = lane; var c = acha(r, id); id = c.pais[0]; }
    });
    r.commits.forEach(function (c) { if (faixa[c.id] === undefined) faixa[c.id] = c.faixa || 0; });
    return faixa;
  };

  var CORES = ["--c0", "--c1", "--c2", "--green"];
  G.desenho = function (r) {
    var faixa = G.faixas(r), nL = 0, W = 70, H = 64, X0 = 50, Y0 = 62;
    r.commits.forEach(function (c) { nL = Math.max(nL, faixa[c.id]); });
    var largura = X0 * 2 + (r.commits.length - 1) * W + 40, altura = Y0 + nL * H + 56, pos = {};
    r.commits.forEach(function (c, i) { pos[c.id] = { x: X0 + i * W, y: Y0 + faixa[c.id] * H }; });
    var s = '<svg width="' + largura + '" height="' + altura + '" viewBox="0 0 ' + largura + ' ' + altura + '" role="img" aria-label="Grafo de commits e branches">';
    r.commits.forEach(function (c) {
      c.pais.forEach(function (p, k) {
        var a = pos[p], b = pos[c.id], cor = CORES[Math.max(faixa[c.id], faixa[p]) % 4];
        var d = a.y === b.y ? "M" + a.x + " " + a.y + " L" + b.x + " " + b.y : "M" + a.x + " " + a.y + " C" + (a.x + 30) + " " + a.y + " " + (b.x - 30) + " " + b.y + " " + b.x + " " + b.y;
        s += '<path d="' + d + '" fill="none" style="stroke:var(' + cor + ')" stroke-width="3" ' + (k ? 'stroke-dasharray="6 4"' : "") + '/>';
      });
    });
    r.commits.forEach(function (c) {
      var p = pos[c.id], cor = CORES[faixa[c.id] % 4], merge = c.pais.length > 1;
      s += '<circle cx="' + p.x + '" cy="' + p.y + '" r="' + (merge ? 15 : 13) + '" style="fill:var(--card);stroke:var(' + cor + ')" stroke-width="' + (merge ? 4 : 3) + '"/>';
      s += '<text x="' + p.x + '" y="' + (p.y + 4) + '" text-anchor="middle" style="fill:var(--ink)" font-size="11" font-weight="700" font-family="monospace">' + c.id + '</text>';
      s += '<text x="' + p.x + '" y="' + (p.y + 30) + '" text-anchor="middle" style="fill:var(--muted)" font-size="9">' + esc(c.msg.length > 12 ? c.msg.slice(0, 11) + "…" : c.msg) + '</text>';
    });
    var porCommit = {};
    Object.keys(r.branches).forEach(function (n) { (porCommit[r.branches[n]] = porCommit[r.branches[n]] || []).push(n); });
    Object.keys(porCommit).forEach(function (id) {
      var p = pos[id];
      porCommit[id].sort().forEach(function (n, k) {
        var txt = (n === r.head ? "HEAD → " : "") + n, w = txt.length * 6.4 + 14, y = p.y - 24 - k * 20, cor = n === r.head ? "--pen" : "--muted";
        s += '<rect x="' + (p.x - w / 2) + '" y="' + (y - 13) + '" width="' + w + '" height="17" rx="8" style="fill:' + (n === r.head ? "var(--pen)" : "var(--paper-2)") + ';stroke:var(' + cor + ')"/>';
        s += '<text x="' + p.x + '" y="' + (y - 1) + '" text-anchor="middle" font-size="10" font-weight="700" style="fill:' + (n === r.head ? "#fff" : "var(--ink)") + '">' + esc(txt) + '</text>';
      });
    });
    return s + "</svg>";
  };

  var CENARIOS = {
    a: { nome: "Cenário A: fast-forward", passos: ["git switch -c feature", "git commit -m \"apostila\"", "git commit -m \"exercicio\"", "git switch main", "git merge feature"] },
    b: { nome: "Cenário B: merge com dois pais", passos: ["git switch -c feature", "git commit -m \"apostila\"", "git commit -m \"exercicio\"", "git switch main", "git commit -m \"so na main\"", "git merge feature"] }
  };
  G.cenarios = CENARIOS;

  E.demos.gitGrafo = function (el) {
    if (TG.estilo) TG.estilo();
    var rep = G.novo(), cen = null, pos = 0;
    el.innerHTML = '<h4>Dê comandos e veja o grafo mudar</h4>' +
      '<p class="muted" style="margin:0 0 6px">Você começa com um commit (<code>c1</code>) na branch main. Digite comandos como <code>git commit -m "algo"</code> ou use um cenário pronto e avance um passo por vez. Os ids aqui são c1, c2... só para ler fácil.</p>' +
      '<div class="ctrls"><button class="btn sm" type="button" data-c="a">Cenário A: fast-forward</button><button class="btn sm" type="button" data-c="b">Cenário B: merge com dois pais</button><button class="btn sm pri" type="button" data-a="passo" disabled>Próximo passo do cenário</button><button class="btn sm" type="button" data-a="zera">Zerar</button></div>' +
      '<div class="tggit"></div>' +
      '<div class="tgterm"><div class="tgout" style="min-height:90px;max-height:170px" aria-live="polite"></div><div class="tgin"><span>$</span><input type="text" spellcheck="false" autocomplete="off" autocapitalize="off" aria-label="Comando git"></div></div>' +
      '<div class="read" aria-live="polite"></div>';
    var graf = el.querySelector(".tggit"), out = el.querySelector(".tgout"), inp = el.querySelector("input"), rd = el.querySelector(".read"), bp = el.querySelector("[data-a=passo]");
    function leitura(extra) {
      var n = rep.commits.length, bs = Object.keys(rep.branches).sort().map(function (b) { return b + " em " + rep.branches[b]; }).join(", ");
      var merges = rep.commits.filter(function (c) { return c.pais.length > 1; }).length;
      rd.innerHTML = '<b>' + n + '</b> commit(s)' + (merges ? ', sendo <b>' + merges + '</b> de merge (com 2 pais)' : '') + '. Branches: ' + esc(bs) + '. Você está em <b>' + esc(rep.head) + '</b>.' + (extra ? ' ' + extra : '');
    }
    function desenha(extra) { graf.innerHTML = G.desenho(rep); leitura(extra); }
    function roda(l) {
      var r = G.exec(rep, l);
      out.insertAdjacentHTML("beforeend", '<span class="tgps">$</span> ' + esc(l) + '\n' + (r.txt ? (r.ok ? esc(r.txt) : '<span class="tgerr">' + esc(r.txt) + '</span>') + '\n' : ""));
      out.scrollTop = out.scrollHeight; desenha();
    }
    function zera() { rep = G.novo(); cen = null; pos = 0; out.innerHTML = ""; bp.disabled = true; bp.textContent = "Próximo passo do cenário"; desenha(); }
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter" && inp.value.trim()) { roda(inp.value); inp.value = ""; } });
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b || !el.contains(b)) return;
      if (b.hasAttribute("data-c")) { zera(); cen = CENARIOS[b.getAttribute("data-c")]; bp.disabled = false; bp.textContent = "Próximo passo (1 de " + cen.passos.length + ")"; leitura(cen.nome + ". Clique em Próximo passo."); }
      else if (b.getAttribute("data-a") === "zera") zera();
      else if (b.getAttribute("data-a") === "passo" && cen && pos < cen.passos.length) {
        roda(cen.passos[pos++]);
        if (pos >= cen.passos.length) { bp.disabled = true; bp.textContent = "Cenário terminado"; } else bp.textContent = "Próximo passo (" + (pos + 1) + " de " + cen.passos.length + ")";
      }
    });
    zera();
  };
})();
