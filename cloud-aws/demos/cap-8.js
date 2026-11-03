/* Demos do capítulo 8: balanceador, alarme do CloudWatch e Auto Scaling.
   As contas ficam em Estudo.calc8 (funções puras) para poderem ser conferidas fora do navegador. */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---------------- contas (sem DOM) ---------------- */
  var CALC = E.calc8 = {};

  /* Rodízio: distribui n pedidos entre as instâncias vivas, continuando de onde o ponteiro parou.
     Sem balanceador, todo pedido vai para a instância 0. */
  CALC.distribuir = function (n, vivas, ponteiro, comBalanceador) {
    var k = vivas.length, cont = vivas.map(function () { return 0; }), falhas = 0, p = ponteiro || 0;
    var qtd = vivas.filter(Boolean).length;
    for (var i = 0; i < n; i++) {
      if (!comBalanceador) { if (vivas[0]) cont[0]++; else falhas++; continue; }
      if (!qtd) { falhas++; continue; }
      while (!vivas[p % k]) p++;
      cont[p % k]++; p++;
    }
    return { cont: cont, falhas: falhas, ponteiro: p % k };
  };

  /* Alarme: ALARM se os últimos `seguidos` pontos estão todos acima do limite. */
  CALC.CPU = [30, 35, 42, 55, 72, 81, 88, 91, 86, 70, 52, 41];
  CALC.alarme = function (serie, limite, seguidos) {
    return serie.map(function (_, i) {
      if (i + 1 < seguidos) return "OK";
      for (var j = i - seguidos + 1; j <= i; j++) if (!(serie[j] > limite)) return "OK";
      return "ALARM";
    });
  };

  /* Auto Scaling simplificado: mede a carga com `atraso` minutos de defasagem e pede
     instâncias para manter a utilização no alvo, entre mínimo e máximo. */
  CALC.CARGA = [120, 130, 150, 200, 350, 600, 850, 900, 900, 880, 700, 500, 350, 250, 200, 160, 140, 130, 120, 120];
  CALC.CAP = 100;
  CALC.escala = function (minimo, maximo, alvo, atraso) {
    return CALC.CARGA.map(function (l, t) {
      var ref = CALC.CARGA[Math.max(0, t - atraso)];
      var n = Math.min(maximo, Math.max(minimo, Math.ceil(ref / (CALC.CAP * alvo / 100))));
      var cap = n * CALC.CAP;
      return { t: t, carga: l, n: n, cap: cap, perdido: Math.max(0, l - cap) };
    });
  };
  CALC.fixa = function (n) {
    return CALC.CARGA.map(function (l, t) { return { t: t, carga: l, n: n, cap: n * CALC.CAP, perdido: Math.max(0, l - n * CALC.CAP) }; });
  };
  CALC.resumo = function (o) {
    var tot = 0, perd = 0, im = 0, pico = 0;
    o.forEach(function (x) { tot += x.carga; perd += x.perdido; im += x.n; pico = Math.max(pico, x.n); });
    return { total: tot, perdidos: perd, pct: Math.round(1000 * perd / tot) / 10, instMin: im, pico: pico };
  };
  function pt(x) { return String(x).replace(".", ","); }

  /* ---------------- demo 1: balanceador ---------------- */
  E.demos.balanceador = function (el) {
    var NOMES = ["A", "B", "C"], vivas = [true, true, true], tot = [0, 0, 0], falhas = 0, ponteiro = 0, ultimo = "";
    el.innerHTML = '<h4>Mande tráfego e derrube instâncias</h4>' +
      '<div class="ctrls"><label><input type="checkbox" class="bl" checked> usar o balanceador</label>' +
      '<button class="btn sm pri" type="button" data-a="env">Enviar 12 pedidos</button><button class="btn sm" type="button" data-a="zera">Zerar contagem</button></div>' +
      '<div class="lbg" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:10px 0"></div>' +
      '<div class="read" aria-live="polite"></div>';
    var grid = el.querySelector(".lbg"), rd = el.querySelector(".read"), cb = el.querySelector(".bl");
    function draw() {
      var mx = Math.max(1, Math.max.apply(null, tot));
      grid.innerHTML = NOMES.map(function (n, i) {
        var v = vivas[i];
        return '<div style="border:2px solid var(--' + (v ? "green" : "red") + ');border-radius:12px;padding:8px 8px 10px;background:var(--card);text-align:center;min-width:0">' +
          '<b>Instância ' + n + '</b><div style="font-size:.78rem;font-weight:700;color:var(--' + (v ? "green" : "red") + ')">' + (v ? "saudável" : "fora do ar") + '</div>' +
          '<div style="font:700 1.6rem var(--f-head);margin:4px 0">' + tot[i] + '</div>' +
          '<div style="height:8px;border-radius:5px;background:var(--paper-2);border:1px solid var(--line);overflow:hidden"><div style="height:100%;width:' + (tot[i] / mx * 100) + '%;background:var(--pen);transition:width .4s"></div></div>' +
          '<button class="btn sm" type="button" data-i="' + i + '" style="margin-top:8px">' + (v ? "Derrubar" : "Subir") + '</button></div>';
      }).join("");
    }
    function leitura() {
      var com = cb.checked, vivasN = vivas.filter(Boolean).length, soma = tot.reduce(function (a, b) { return a + b; }, 0);
      var t = ultimo ? ultimo + " " : "";
      if (!com) t += "<b>Sem balanceador</b>, todos os pedidos vão para a instância A. " + (vivas[0] ? "Ela atende tudo sozinha: se o pico passar da capacidade dela, o site trava." : "Ela caiu, então <b>o site inteiro fica fora do ar</b>, mesmo com B e C saudáveis e ociosas.");
      else if (!vivasN) t += "Com o balanceador, mas sem nenhuma instância saudável: o balanceador responde erro 503 (serviço indisponível).";
      else t += "<b>Com balanceador</b>, o tráfego é repartido entre as " + vivasN + " instância(s) saudável(is). Se uma cai, as outras seguem atendendo: é a <b>tolerância a falhas</b>.";
      t += " <span class='muted'>Total atendido: " + soma + ". Pedidos que falharam: " + falhas + ".</span>";
      rd.innerHTML = t;
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b || !el.contains(b)) return;
      if (b.hasAttribute("data-i")) { var i = +b.getAttribute("data-i"); vivas[i] = !vivas[i]; ultimo = "Instância " + NOMES[i] + (vivas[i] ? " voltou." : " caiu."); }
      else if (b.getAttribute("data-a") === "env") {
        var r = CALC.distribuir(12, vivas, ponteiro, cb.checked); ponteiro = r.ponteiro; falhas += r.falhas;
        r.cont.forEach(function (c, i) { tot[i] += c; });
        ultimo = "Rodada de 12 pedidos: " + r.cont.map(function (c, i) { return NOMES[i] + " recebeu " + c; }).join(", ") + (r.falhas ? "; " + r.falhas + " falharam" : "") + ".";
      } else if (b.getAttribute("data-a") === "zera") { tot = [0, 0, 0]; falhas = 0; ultimo = "Contagem zerada."; }
      else return;
      draw(); leitura();
    });
    cb.addEventListener("change", leitura);
    draw(); leitura();
  };

  /* ---------------- demo 2: alarme do CloudWatch ---------------- */
  E.demos.alarme = function (el) {
    el.innerHTML = '<h4>Quando o alarme dispara?</h4>' +
      '<div class="ctrls"><label>limite de CPU <input type="range" class="al" min="50" max="95" step="5" value="70"><output class="alo">70%</output></label>' +
      '<label>pontos seguidos acima do limite <input type="range" class="as" min="1" max="5" step="1" value="3"><output class="aso">3</output></label>' +
      '<label>ação <select class="aa"><option value="sns">notificar por SNS</option><option value="asg">executar o Auto Scaling</option></select></label></div>' +
      '<div class="alg" style="position:relative;display:flex;gap:3px;align-items:flex-end;height:150px;margin:14px 0 4px;border-bottom:2px solid var(--line)"></div>' +
      '<div class="als" style="display:flex;gap:3px;margin-bottom:8px"></div>' +
      '<div class="read" aria-live="polite"></div>';
    var L = el.querySelector(".al"), S = el.querySelector(".as"), A = el.querySelector(".aa"), g = el.querySelector(".alg"), st = el.querySelector(".als"), rd = el.querySelector(".read");
    function go() {
      var lim = +L.value, seg = +S.value, cpu = CALC.CPU, est = CALC.alarme(cpu, lim, seg);
      el.querySelector(".alo").textContent = lim + "%"; el.querySelector(".aso").textContent = seg;
      g.innerHTML = cpu.map(function (v, i) {
        return '<div title="ponto ' + (i + 1) + ': ' + v + '%" style="flex:1;min-width:0;height:' + v + '%;background:var(--' + (v > lim ? "red" : "pen") + ');border-radius:4px 4px 0 0;opacity:.9"></div>';
      }).join("") + '<div style="position:absolute;left:0;right:0;bottom:' + lim + '%;border-top:2px dashed var(--amber)"></div>';
      st.innerHTML = est.map(function (s) {
        return '<div style="flex:1;min-width:0;text-align:center;font:700 .6rem var(--f-body);padding:2px 0;border-radius:4px;background:var(--' + (s === "ALARM" ? "red-soft" : "green-soft") + ');color:var(--' + (s === "ALARM" ? "red" : "green") + ')">' + (s === "ALARM" ? "ALM" : "OK") + '</div>';
      }).join("");
      var ini = est.indexOf("ALARM"), acao = A.value === "sns" ? "uma notificação por e-mail ou mensagem (SNS)" : "uma ação do Auto Scaling (criar instâncias)";
      if (ini < 0) rd.innerHTML = "Com limite de <b>" + lim + "%</b> e <b>" + seg + "</b> ponto(s) seguido(s), o alarme <b>nunca dispara</b> nesta série. Ou o limite está alto demais, ou a exigência de pontos seguidos é rígida demais.";
      else {
        var fim = ini; while (fim + 1 < est.length && est[fim + 1] === "ALARM") fim++;
        var acima = cpu.filter(function (v) { return v > lim; }).length;
        rd.innerHTML = "O alarme entra em <b>ALARM no ponto " + (ini + 1) + "</b> e dispara " + acao + ". Volta a OK no ponto " + (fim + 2 <= est.length ? (fim + 2) : "-") + ". Pontos acima do limite na série: <b>" + acima + "</b> de " + cpu.length + ". " + (seg === 1 ? "Com 1 ponto basta um pico passageiro para disparar." : "Exigir mais pontos seguidos filtra picos curtos, mas atrasa a reação.");
      }
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---------------- demo 3: Auto Scaling na Black Friday ---------------- */
  E.demos.escalaAsg = function (el) {
    var YMAX = 1200;
    el.innerHTML = '<h4>Simule a Black Friday: frota fixa x Auto Scaling</h4>' +
      '<p class="muted" style="margin:0 0 6px;font-size:.88rem">Modelo simplificado e <b>meu</b> (complemento, não foi dado em aula): cada instância atende 100 pedidos por minuto, e o grupo mede a carga com alguns minutos de atraso.</p>' +
      '<div class="ctrls"><label>mínimo <input type="range" class="e-min" min="1" max="4" value="2"><output class="o-min">2</output></label>' +
      '<label>máximo <input type="range" class="e-max" min="2" max="12" value="10"><output class="o-max">10</output></label>' +
      '<label>meta de uso <input type="range" class="e-alvo" min="30" max="80" step="10" value="60"><output class="o-alvo">60%</output></label>' +
      '<label>atraso para ficar pronta <input type="range" class="e-atr" min="0" max="5" value="2"><output class="o-atr">2 min</output></label>' +
      '<label>frota fixa de comparação <input type="range" class="e-fix" min="1" max="12" value="2"><output class="o-fix">2</output></label></div>' +
      '<div class="eg" style="position:relative;display:flex;gap:2px;align-items:flex-end;height:170px;margin:14px 0 2px;border-bottom:2px solid var(--line)"></div>' +
      '<div style="display:flex;justify-content:space-between;font-size:.72rem;color:var(--muted)"><span>minuto 0</span><span>minuto 19</span></div>' +
      '<p class="muted" style="font-size:.8rem;margin:6px 0">Azul: pedidos atendidos. Vermelho: pedidos perdidos. Linha verde: capacidade do grupo em cada minuto. Linha tracejada: frota fixa.</p>' +
      '<div class="tablewrap"><table class="et"></table></div><div class="read" aria-live="polite"></div>';
    var q = function (c) { return el.querySelector(c); }, g = q(".eg"), tb = q(".et"), rd = q(".read");
    function go() {
      var mn = +q(".e-min").value, mx = +q(".e-max").value, alvo = +q(".e-alvo").value, atr = +q(".e-atr").value, fx = +q(".e-fix").value;
      if (mx < mn) { mx = mn; q(".e-max").value = mx; }
      q(".o-min").textContent = mn; q(".o-max").textContent = mx; q(".o-alvo").textContent = alvo + "%"; q(".o-atr").textContent = atr + " min"; q(".o-fix").textContent = fx;
      var A = CALC.escala(mn, mx, alvo, atr), F = CALC.fixa(fx), P = CALC.fixa(Math.ceil(Math.max.apply(null, CALC.CARGA) / CALC.CAP));
      g.innerHTML = A.map(function (x) {
        var serv = Math.min(x.carga, x.cap);
        return '<div title="minuto ' + x.t + ': carga ' + x.carga + ', ' + x.n + ' instância(s), perdidos ' + x.perdido + '" style="flex:1;min-width:0;position:relative;height:100%">' +
          '<div style="position:absolute;left:0;right:0;bottom:0;height:' + serv / YMAX * 100 + '%;background:var(--pen)"></div>' +
          '<div style="position:absolute;left:0;right:0;bottom:' + serv / YMAX * 100 + '%;height:' + x.perdido / YMAX * 100 + '%;background:var(--red)"></div>' +
          '<div style="position:absolute;left:-1px;right:-1px;bottom:calc(' + x.cap / YMAX * 100 + '% - 1px);height:3px;background:var(--green)"></div></div>';
      }).join("") + '<div style="position:absolute;left:0;right:0;bottom:' + fx * CALC.CAP / YMAX * 100 + '%;border-top:2px dashed var(--amber);pointer-events:none"></div>';
      var ra = CALC.resumo(A), rf = CALC.resumo(F), rp = CALC.resumo(P);
      function lin(nome, r, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : "") + '><td>' + nome + '</td><td>' + r.perdidos + '</td><td>' + pt(r.pct) + '%</td><td>' + r.instMin + '</td></tr>'; }
      tb.innerHTML = '<tr><th>Estratégia</th><th>Pedidos perdidos</th><th>% perdido</th><th>Minutos de instância</th></tr>' +
        lin("Frota fixa de " + fx, rf) + lin("Frota fixa para o pico (" + rp.pico + ")", rp) + lin("Auto Scaling (" + mn + " a " + mx + ")", ra, "dest");
      var economia = Math.round(100 * (rp.instMin - ra.instMin) / rp.instMin);
      rd.innerHTML = "Foram <b>" + ra.total + "</b> pedidos em 20 minutos. O Auto Scaling perdeu <b>" + ra.perdidos + "</b> (" + pt(ra.pct) + "%) e usou <b>" + ra.instMin + "</b> minutos de instância; a frota fixa dimensionada para o pico usa <b>" + rp.instMin + "</b>, ou seja, " + (economia >= 0 ? "o grupo gastou <b>" + economia + "%</b> menos" : "o grupo gastou mais") + ". " +
        (ra.perdidos ? "As perdas aparecem na <b>subida</b>, antes de as instâncias novas ficarem prontas; tente diminuir o atraso ou subir o mínimo." : "Sem perda nenhuma: o grupo antecipou o pico.");
    }
    el.addEventListener("input", go); go();
  };
})();
