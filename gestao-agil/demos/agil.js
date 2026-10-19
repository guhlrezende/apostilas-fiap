/* Demos da apostila de Gestão Ágil e Pitch */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function f(x, d) { if (!isFinite(x)) return "n/d"; d = d === undefined ? 1 : d; return x.toFixed(d).replace(".", ","); }
  function pct(x) { return isFinite(x) ? f(x * 100, 1) + "%" : "n/d"; }

  /* ---- cap 1: o caso dos 92% de acurácia ---- */
  E.demos.acuracia = function (el) {
    el.innerHTML = '<h4>1.000 solicitações de atendimento, 80 delas urgentes</h4><div class="ctrls"><button class="btn sm" type="button" data-p="10,10">O modelo do caso (92%)</button><button class="btn sm" type="button" data-p="0,0">Sempre diz "não urgente"</button><button class="btn sm" type="button" data-p="64,24">Um modelo útil</button></div><div class="ctrls"><label>urgentes que ele acertou (VP) <input type="range" id="ac-tp" min="0" max="80" step="1" value="10"><output id="ac-tpo"></output></label><label>não urgentes que ele marcou como urgentes (FP) <input type="range" id="ac-fp" min="0" max="120" step="1" value="10"><output id="ac-fpo"></output></label></div><div class="tablewrap"><table class="cm"></table></div><div class="sg"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, P = 80, T = 1000;
    function go() {
      var tp = +g("#ac-tp").value, fp = +g("#ac-fp").value, fn = P - tp, tn = T - P - fp;
      g("#ac-tpo").textContent = tp; g("#ac-fpo").textContent = fp;
      var acc = (tp + tn) / T, prec = tp + fp ? tp / (tp + fp) : NaN, rec = tp / P, f1 = prec + rec ? 2 * prec * rec / (prec + rec) : 0, base = (T - P) / T;
      g(".cm").innerHTML = '<tr><th></th><th>previu urgente</th><th>previu não urgente</th></tr><tr><td><b>era urgente</b> (80)</td><td class="dest">VP = ' + tp + '</td><td>FN = ' + fn + '</td></tr><tr><td><b>não era urgente</b> (920)</td><td>FP = ' + fp + '</td><td>VN = ' + tn + '</td></tr>';
      var it = [["acurácia", pct(acc)], ["precisão (urgentes)", pct(prec)], ["recall (urgentes)", pct(rec)], ["F1 (urgentes)", f(f1, 2)]];
      g(".sg").innerHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:10px 0">' + it.map(function (p) { return '<div class="card" style="margin:0;padding:8px 10px"><small class="muted">' + p[0] + '</small><div style="font:700 1.2rem var(--f-mono)">' + p[1] + '</div></div>'; }).join("") + '</div>';
      g(".read").innerHTML = "Um modelo que <b>sempre</b> responde \"não urgente\" já acerta <b>" + pct(base) + "</b> (920 de 1.000), sem olhar para nada. " + (acc <= base + 0.0001 ? "<b style='color:var(--red)'>A acurácia dessa configuração (" + pct(acc) + ") é igual ou pior que a do chute.</b> " : "A acurácia (" + pct(acc) + ") passa do chute, ") + "" + (rec < 0.5 ? "mas o que o projeto queria era achar as <b>urgentes</b>: o recall diz que ele encontra só <b>" + pct(rec) + "</b> delas. Acurácia alta, projeto falho." : "e o recall mostra que ele encontra <b>" + pct(rec) + "</b> das urgentes, que era o objetivo do projeto. Esse desempenho, sim, serve ao que o cliente pediu.");
    }
    el.addEventListener("input", go);
    el.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-p]"); if (!b) return; var p = b.dataset.p.split(","); g("#ac-tp").value = p[0]; g("#ac-fp").value = p[1]; go(); });
    go();
  };

  /* ---- cap 2: o ciclo da Sprint ---- */
  var EVT = [
    { k: "Sprint Planning", q: "O que vamos entregar nesta Sprint, e como?", quem: "todo o time Scrum", saida: "Meta da Sprint + Sprint Backlog", tempo: "até 8 h para uma Sprint de 1 mês (menos em Sprints menores)", txt: "O Product Owner traz os itens mais valiosos do Product Backlog, o time define uma <b>meta da Sprint</b> e escolhe o que cabe. Se uma tarefa não ajuda a meta, provavelmente não pertence a esta Sprint." },
    { k: "Sprint (com Daily)", q: "Estamos no caminho da meta?", quem: "Developers (SM facilita)", saida: "um Incremento utilizável", tempo: "Sprint de até 1 mês; Daily de 15 min", txt: "É o período de trabalho. A <b>Daily Scrum</b> é um encontro curto, todo dia, para inspecionar o progresso rumo à meta e ajustar o plano do dia. Impedimentos aparecem aqui." },
    { k: "Sprint Review", q: "O que ficou pronto, e o que o feedback muda?", quem: "time Scrum + partes interessadas", saida: "Product Backlog ajustado", tempo: "até 4 h para uma Sprint de 1 mês", txt: "O time <b>demonstra o Incremento</b> e recebe feedback de quem usa ou paga pelo produto. Não é um relatório: é inspeção do produto e adaptação do Backlog. Num curso com empresa parceira, costuma ser curta (por exemplo, 5 min de apresentação e 10 min de feedback)." },
    { k: "Sprint Retrospective", q: "Como melhorar a forma de trabalhar?", quem: "time Scrum", saida: "ações de melhoria do processo", tempo: "até 3 h para uma Sprint de 1 mês", txt: "Olha para o <b>processo</b>, e não para o produto: o que funcionou, o que travou, o que vamos mudar na próxima Sprint. Fecha o ciclo de inspeção e adaptação." }
  ];
  E.demos.ciclo = function (el) {
    el.innerHTML = '<h4>Os eventos do Scrum em ciclo</h4><div class="ctrls ev-tabs"></div><div class="card" style="margin:0"><div class="ev-body"></div></div><div class="ctrls"><button class="btn sm pri" type="button" id="ev-n">Próximo evento →</button></div>';
    var i = 0, tabs = el.querySelector(".ev-tabs"), body = el.querySelector(".ev-body");
    tabs.innerHTML = EVT.map(function (e, k) { return '<button class="btn sm" type="button" data-k="' + k + '">' + (k + 1) + '. ' + e.k + '</button>'; }).join("");
    function go() {
      var e = EVT[i]; tabs.querySelectorAll("button").forEach(function (b, k) { b.classList.toggle("pri", k === i); b.setAttribute("aria-pressed", k === i ? "true" : "false"); });
      body.innerHTML = '<div style="font:700 1.15rem var(--f-hand);color:var(--pen)">' + esc(e.q) + '</div><p style="margin:.4rem 0">' + e.txt + '</p><div class="tablewrap"><table><tr><th>quem participa</th><td>' + e.quem + '</td></tr><tr><th>o que sai dele</th><td>' + e.saida + '</td></tr><tr><th>duração máxima</th><td>' + e.tempo + '</td></tr></table></div>';
    }
    tabs.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-k]"); if (b) { i = +b.dataset.k; go(); } });
    el.querySelector("#ev-n").addEventListener("click", function () { i = (i + 1) % EVT.length; go(); });
    go();
  };

  /* ---- cap 3: montar uma user story ---- */
  E.demos.story = function (el) {
    el.innerHTML = '<h4>Monte uma história e seus critérios de aceite</h4><div class="grid2"><div><label>Como <input type="text" id="st-a" value="bibliotecária" style="width:100%"></label><label>quero <input type="text" id="st-b" value="ver os livros em atraso" style="width:100%"></label><label>para <input type="text" id="st-c" value="decidir quem avisar primeiro" style="width:100%"></label><label>critérios de aceite (um por linha) <textarea id="st-d" rows="4" style="width:100%">Mostra título, aluno e dias de atraso\nOrdena do maior para o menor atraso\nPermite filtrar por turma</textarea></label></div><div><div class="card" style="margin:0"><div class="prev"></div></div><div class="chk"></div></div></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function go() {
      var a = g("#st-a").value.trim(), b = g("#st-b").value.trim(), c = g("#st-c").value.trim(), crit = g("#st-d").value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean);
      g(".prev").innerHTML = '<div style="font:700 1.1rem var(--f-hand);color:var(--pen)">História</div><p><b>Como</b> ' + esc(a || "…") + ', <b>quero</b> ' + esc(b || "…") + ', <b>para</b> ' + esc(c || "…") + '.</p><div style="font:700 1.1rem var(--f-hand);color:var(--pen)">Critérios de aceite</div>' + (crit.length ? "<ul>" + crit.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" : "<p class='muted'>Nenhum ainda.</p>");
      var tests = [[!!(a && b && c), "tem papel, ação e benefício"], [crit.length >= 2, "tem pelo menos 2 critérios de aceite"], [crit.every(function (x) { return x.length >= 12; }) && crit.length > 0, "cada critério é específico (não é só uma palavra)"], [!/\b(rápido|fácil|bonito|amigável|bom|melhor)\b/i.test(b + " " + crit.join(" ")), "evita termos vagos (rápido, fácil, bonito...)"], [!/\b(banco de dados|api|python|tabela|botão|tela)\b/i.test(b), "descreve o valor, e não a solução técnica"]];
      g(".chk").innerHTML = '<ul style="list-style:none;padding:0;margin:.6rem 0">' + tests.map(function (t) { return "<li>" + (t[0] ? "✅" : "⚠️") + " " + t[1] + "</li>"; }).join("") + "</ul>";
      var ok = tests.filter(function (t) { return t[0]; }).length;
      g(".read").innerHTML = ok === tests.length ? "<b style='color:var(--green)'>História bem formada.</b> Lembre: a história diz <b>o valor</b>; os critérios dizem <b>como validar</b>; as tarefas técnicas (campos, cálculo, tela) vêm depois e saem dos critérios." : "A história ainda tem pontos a ajustar (" + ok + " de " + tests.length + "). Os testes acima são uma checagem didática, inspirada no checklist INVEST e em boas práticas, e não uma regra do Scrum.";
    }
    el.addEventListener("input", go); go();
  };

  /* ---- cap 4: limite de WIP ---- */
  function simWip(wip, tasks, devs, work) {
    var dt = 0.01, t = 0, backlog = tasks, act = [], done = [];
    while (done.length < tasks && t < 500) {
      while (act.length < wip && backlog > 0) { act.push(work); backlog--; }
      var rate = Math.min(1, devs / act.length), nxt = [];
      act.forEach(function (a) { var r = a - rate * dt; if (r <= 1e-9) done.push(t + dt); else nxt.push(r); });
      act = nxt; t += dt;
    }
    return done;
  }
  E.demos.wip = function (el) {
    el.innerHTML = '<h4>12 tarefas de 3 dias, 3 pessoas: qual o limite de WIP?</h4><div class="ctrls"><label>limite de trabalho em andamento (WIP) <input type="range" id="wp" min="1" max="12" step="1" value="12"><output id="wpo"></output></label><button class="btn sm" type="button" id="wp-a">WIP = 12 (começar tudo)</button><button class="btn sm pri" type="button" id="wp-b">WIP = 3 (terminar antes de começar)</button></div><canvas style="height:220px;cursor:default"></canvas><div class="sg"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, cv = el.querySelector("canvas"), D = [];
    var api = E.canvas(cv, function (ctx, w, h, c) {
      var pad = { l: 40, r: 12, t: 14, b: 34 }, X = function (d) { return pad.l + d / 36 * (w - pad.l - pad.r); }, Y = function (n) { return pad.t + (1 - n / 12) * (h - pad.t - pad.b); };
      ctx.save(); ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
      for (var d = 0; d <= 36; d += 6) { ctx.beginPath(); ctx.moveTo(X(d), pad.t); ctx.lineTo(X(d), h - pad.b); ctx.stroke(); ctx.fillText(d, X(d), h - pad.b + 14); }
      ctx.textAlign = "right"; for (var n = 0; n <= 12; n += 4) { ctx.beginPath(); ctx.moveTo(pad.l, Y(n)); ctx.lineTo(w - pad.r, Y(n)); ctx.stroke(); ctx.fillText(n, pad.l - 6, Y(n) + 4); }
      ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.textAlign = "center"; ctx.fillText("dias", (pad.l + w - pad.r) / 2, h - 4);
      ctx.beginPath(); ctx.moveTo(X(0), Y(0)); D.forEach(function (t, i) { ctx.lineTo(X(t), Y(i)); ctx.lineTo(X(t), Y(i + 1)); }); ctx.lineWidth = 3; ctx.strokeStyle = c.pen; ctx.stroke();
      ctx.fillStyle = c.muted; ctx.textAlign = "left"; ctx.fillText("tarefas entregues (acumulado)", pad.l + 6, pad.t + 12); ctx.restore();
    });
    function go() {
      var wip = +g("#wp").value; g("#wpo").textContent = wip; D = simWip(wip, 12, 3, 3);
      var med = D.reduce(function (a, b) { return a + b; }, 0) / D.length;
      var it = [["primeira entrega", f(D[0], 1) + " dias"], ["tempo médio até entregar", f(med, 2) + " dias"], ["tudo pronto em", f(D[D.length - 1], 1) + " dias"], ["pessoas ocupadas", Math.min(3, wip) + " de 3"]];
      g(".sg").innerHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px;margin:10px 0">' + it.map(function (p) { return '<div class="card" style="margin:0;padding:8px 10px"><small class="muted">' + p[0] + '</small><div style="font:700 1.15rem var(--f-mono)">' + p[1] + '</div></div>'; }).join("") + '</div>';
      g(".read").innerHTML = wip < 3 ? "<b>WIP baixo demais:</b> há gente sem tarefa, e a equipe entrega devagar." : wip === 3 ? "<b>WIP = número de pessoas:</b> cada um termina a sua tarefa antes de começar outra. Entregas aos 3, 6, 9 e 12 dias." : "<b>WIP alto:</b> todo mundo está \"ocupado\", mas cada tarefa recebe só " + f(3 / wip, 2) + " de dia de trabalho por dia, e tudo demora mais. " + (wip >= 12 ? "Com 12 em andamento, <b>nada</b> fica pronto antes do dia 12." : "") + " O trabalho total é o mesmo; o que muda é <b>quando</b> cada coisa fica pronta. (Modelo simplificado, sem o custo extra de trocar de contexto, que só pioraria o caso.)";
      api.paint();
    }
    el.addEventListener("input", go); g("#wp-a").addEventListener("click", function () { g("#wp").value = 12; go(); }); g("#wp-b").addEventListener("click", function () { g("#wp").value = 3; go(); });
    go();
  };

  /* ---- cap 5: o relógio do pitch ---- */
  E.demos.pitch = function (el) {
    var S = [["Abertura: a pessoa e o problema", 25, "t"], ["A situação do usuário", 30, "t"], ["Um dado sobre o problema", 28, "t"], ["A User Story", 30, "t"], ["Os critérios de aceite", 28, "t"], ["Imagem de apoio", 3, "i"], ["A solução em ação", 30, "t"], ["Evidências e testes feitos", 30, "t"], ["Imagem de apoio", 3, "i"], ["Diagrama da arquitetura", 30, "t"], ["Critérios de sucesso e valor", 28, "t"], ["Fechamento e próximo passo", 26, "t"]];
    el.innerHTML = '<h4>Planeje os 5 minutos: cada slide, seus segundos</h4><div class="tablewrap"><table class="pt"></table></div><div class="sg"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); };
    function render() {
      g(".pt").innerHTML = '<tr><th>#</th><th>slide</th><th>tipo</th><th>segundos</th></tr>' + S.map(function (s, i) { return '<tr><td>' + (i + 1) + '</td><td>' + s[0] + '</td><td><select data-i="' + i + '" data-f="2" aria-label="tipo do slide ' + (i + 1) + '"><option value="t"' + (s[2] === "t" ? " selected" : "") + '>tópicos ou gráfico</option><option value="i"' + (s[2] === "i" ? " selected" : "") + '>imagem de apoio</option></select></td><td><input type="number" min="1" max="120" value="' + s[1] + '" data-i="' + i + '" data-f="1" style="width:70px" aria-label="segundos do slide ' + (i + 1) + '"></td></tr>'; }).join("");
    }
    function go() {
      var tot = S.reduce(function (a, s) { return a + s[1]; }, 0), m = Math.floor(tot / 60), sec = tot % 60, avisos = [];
      S.forEach(function (s, i) { if (s[2] === "t" && s[1] > 30) avisos.push("O slide " + (i + 1) + " passa de 30 s com tópicos: divida em dois slides ou corte texto."); if (s[2] === "i" && s[1] > 3) avisos.push("O slide " + (i + 1) + " é só imagem de apoio: o certo é 2 a 3 s."); });
      var st = tot > 300 ? ["red", "Passou de 5 min: o pitch é cortado."] : tot < 270 ? ["red", "Abaixo de 4 min 30 s: faltou aproveitar o tempo."] : tot >= 285 && tot <= 295 ? ["green", "Zona ideal (cerca de 4 min 50 s)."] : ["amber", "Dentro da regra (4 min 30 s a 5 min), mas pouco folgado: o ideal é cerca de 4 min 50 s."];
      g(".sg").innerHTML = '<div class="card" style="margin:10px 0;padding:10px 14px"><small class="muted">tempo total</small><div style="font:700 1.5rem var(--f-mono);color:var(--' + (st[0] === "amber" ? "pen" : st[0]) + ')">' + m + " min " + (sec < 10 ? "0" : "") + sec + " s</div><div>" + st[1] + "</div></div>";
      g(".read").innerHTML = avisos.length ? "<ul>" + avisos.map(function (a) { return "<li>" + a + "</li>"; }).join("") + "</ul>" : "Nenhum slide fora das regras de densidade. Lembre: o relógio é uma <b>regra de ensaio</b>; o que prende a atenção é a história, e não a precisão do cronômetro.";
    }
    el.addEventListener("input", function (ev) { var t = ev.target; if (t.dataset.f === "1") { S[+t.dataset.i][1] = Math.max(0, +t.value || 0); go(); } });
    el.addEventListener("change", function (ev) { var t = ev.target; if (t.dataset.f === "2") { S[+t.dataset.i][2] = t.value; go(); } });
    render(); go();
  };

  /* ---- cap 6: diagrama de componentes interativo ---- */
  var COMP = {
    mot: { n: "Motorista", x: 20, y: 90, w: 90, h: 50, tipo: "ator", d: "Quem usa o sistema (ator). Fica fora das caixas: é o usuário, e não uma peça do software." },
    cam: { n: "Câmera + sensor no volante", x: 150, y: 20, w: 140, h: 50, tipo: "dev", d: "Captura imagem do rosto e a pressão nas mãos. Está ligado a um pino de entrada (GPIO) do microcontrolador." },
    mcu: { n: "Microcontrolador (ESP32)", x: 150, y: 120, w: 140, h: 56, tipo: "dev", d: "Tem CPU e memória (caixa 3D com estereótipo device). Roda o algoritmo em C++ e decide se dispara o alerta local." },
    buz: { n: "Buzzer", x: 150, y: 210, w: 140, h: 40, tipo: "dev", d: "Alerta sonoro para o motorista. Está ligado a um pino de saída (GPIO) do microcontrolador." },
    cloud: { n: "Cloud Server (EC2, Python)", x: 340, y: 100, w: 150, h: 70, tipo: "srv", d: "Back-end: recebe os dados, roda o modelo de IA de detecção de fadiga, gera alertas e guarda tudo." },
    db: { n: "Banco de dados", x: 340, y: 210, w: 150, h: 40, tipo: "bd", d: "Histórico de ocorrências, para relatórios simples. Fica ligado ao back-end." },
    dash: { n: "Dashboard (navegador)", x: 540, y: 100, w: 140, h: 70, tipo: "web", d: "Front-end: o gestor vê o estado em tempo real e os relatórios pelo celular ou computador." },
    ges: { n: "Gestor", x: 560, y: 8, w: 90, h: 44, tipo: "ator", d: "Segundo ator: recebe o alerta no painel e consulta o histórico." }
  };
  var LIG = [["mot", "cam", "olhar e dirigir", ""], ["cam", "mcu", "GPIO (leitura)", ""], ["mcu", "buz", "GPIO (alerta)", ""], ["mcu", "cloud", "MQTT ou WebSocket", ""], ["cloud", "db", "consulta e gravação", ""], ["cloud", "dash", "HTTPS", ""], ["ges", "dash", "navegador", ""]];
  E.demos.uml = function (el) {
    el.innerHTML = '<h4>Detector de fadiga: clique em um componente ou em uma ligação</h4><div class="uml-wrap" style="overflow-x:auto"><svg viewBox="0 0 700 270" role="group" aria-label="Diagrama de componentes do detector de fadiga" style="width:100%;min-width:560px;height:auto"></svg></div><div class="read">Clique em uma caixa para ver a responsabilidade dela.</div>';
    var svg = el.querySelector("svg"), rd = el.querySelector(".read"), NS = "http://www.w3.org/2000/svg";
    function mk(tag, at, txt) { var e = document.createElementNS(NS, tag); Object.keys(at).forEach(function (k) { e.setAttribute(k, at[k]); }); if (txt) e.textContent = txt; return e; }
    function cx(c) { return c.x + c.w / 2; } function cy(c) { return c.y + c.h / 2; }
    var grp = mk("rect", { x: 130, y: 6, width: 570, height: 258, rx: 8, fill: "none", stroke: "currentColor", "stroke-dasharray": "6 5", "stroke-width": 1.5, opacity: .5 }); svg.appendChild(grp);
    svg.appendChild(mk("text", { x: 692, y: 258, "font-size": 12, "text-anchor": "end", fill: "currentColor", opacity: .7 }, "User Story 1"));
    var rotulos = [];
    LIG.forEach(function (l) {
      var a = COMP[l[0]], b = COMP[l[1]], x1 = cx(a), y1 = cy(a), x2 = cx(b), y2 = cy(b), g = mk("g", { tabindex: 0, role: "button", "aria-label": "ligação: " + l[2], style: "cursor:pointer" });
      g.appendChild(mk("line", { x1: x1, y1: y1, x2: x2, y2: y2, stroke: "currentColor", "stroke-width": 2, opacity: .75 }));
      g.appendChild(mk("line", { x1: x1, y1: y1, x2: x2, y2: y2, stroke: "transparent", "stroke-width": 14 }));
      var tx = (x1 + x2) / 2, ty = (y1 + y2) / 2 - 4; rotulos.push(mk("text", { x: tx, y: ty, "font-size": 11, "text-anchor": "middle", fill: "currentColor", "pointer-events": "none", style: "paint-order:stroke;stroke:var(--card,#fff);stroke-width:4px" }, l[2]));
      function sel() { rd.innerHTML = "<b>Ligação: " + esc(l[2]) + "</b><br>" + esc(COMP[l[0]].n) + " → " + esc(COMP[l[1]].n) + ". " + (l[2].indexOf("HTTPS") >= 0 ? "Navegador falando com o servidor: HTTP seguro." : l[2].indexOf("MQTT") >= 0 ? "Protocolos leves, comuns em IoT: o microcontrolador publica as leituras para a nuvem." : l[2].indexOf("GPIO") >= 0 ? "Fio ou pino físico (General Purpose Input/Output): não é rede, é eletrônica." : "Comunicação entre as partes."); }
      g.addEventListener("click", sel); g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sel(); } });
      svg.appendChild(g);
    });
    Object.keys(COMP).forEach(function (k) {
      var c = COMP[k], g = mk("g", { tabindex: 0, role: "button", "aria-label": c.n, style: "cursor:pointer" });
      var fill = c.tipo === "ator" ? "none" : "var(--card,#fff)";
      if (c.tipo === "ator") { g.appendChild(mk("circle", { cx: cx(c), cy: c.y + 8, r: 7, fill: "none", stroke: "currentColor", "stroke-width": 2 })); g.appendChild(mk("path", { d: "M" + cx(c) + " " + (c.y + 15) + "v14M" + (cx(c) - 12) + " " + (c.y + 20) + "h24M" + cx(c) + " " + (c.y + 29) + "l-9 13M" + cx(c) + " " + (c.y + 29) + "l9 13", fill: "none", stroke: "currentColor", "stroke-width": 2 })); g.appendChild(mk("text", { x: cx(c), y: c.y + c.h + 12, "font-size": 12, "text-anchor": "middle", fill: "currentColor", "font-weight": 600 }, c.n)); g.appendChild(mk("rect", { x: c.x, y: c.y - 4, width: c.w, height: c.h + 20, fill: "transparent" })); }
      else {
        if (c.tipo === "bd") { g.appendChild(mk("rect", { x: c.x, y: c.y, width: c.w, height: c.h, rx: 14, fill: fill, stroke: "currentColor", "stroke-width": 2 })); }
        else if (c.tipo === "dev" || c.tipo === "srv") { g.appendChild(mk("rect", { x: c.x + 5, y: c.y - 5, width: c.w, height: c.h, fill: "none", stroke: "currentColor", "stroke-width": 1.5, opacity: .6 })); g.appendChild(mk("rect", { x: c.x, y: c.y, width: c.w, height: c.h, fill: fill, stroke: "currentColor", "stroke-width": 2 })); }
        else g.appendChild(mk("rect", { x: c.x, y: c.y, width: c.w, height: c.h, fill: fill, stroke: "currentColor", "stroke-width": 2 }));
        var words = c.n.split(" "), lines = [], cur = ""; words.forEach(function (w) { if ((cur + " " + w).trim().length > 20) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim(); }); lines.push(cur);
        lines.forEach(function (ln, i) { g.appendChild(mk("text", { x: cx(c), y: cy(c) + 4 + (i - (lines.length - 1) / 2) * 14, "font-size": 12, "text-anchor": "middle", fill: "currentColor", "font-weight": 600 }, ln)); });
      }
      function sel() { rd.innerHTML = "<b>" + esc(c.n) + "</b> · " + (c.tipo === "ator" ? "ator" : c.tipo === "bd" ? "banco de dados" : c.tipo === "web" ? "front-end" : c.tipo === "srv" ? "back-end (execução na nuvem)" : "hardware / dispositivo") + "<br>" + c.d; }
      g.addEventListener("click", sel); g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sel(); } });
      svg.appendChild(g);
    });
    rotulos.forEach(function (t) { svg.appendChild(t); });
  };
})();
