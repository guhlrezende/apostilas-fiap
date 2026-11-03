/* Demos dos capítulos 8 e 9 da apostila de Sistemas Embarcados: botão que espera (if x while) e millis().
   As funções de simulação são puras e ficam em Estudo.embSim, para poderem ser conferidas fora do navegador. */
(function () {
  var E = window.Estudo;
  function f(x, d) { if (!isFinite(x)) return "nan"; d = d === undefined ? 2 : d; return x.toFixed(d); }
  function fb(x, d) { return f(x, d).replace(".", ","); }
  function seg(ms) { return fb(ms / 1000, 1); }
  function cards(items) {
    return '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:10px 0">' + items.map(function (p) {
      return '<div class="card" style="margin:0;padding:8px 10px"><small class="muted">' + p[0] + '</small><div style="font:700 1.15rem var(--f-mono)">' + p[1] + '</div></div>';
    }).join("") + '</div>';
  }

  /* ---------------------------------------------------------------
     Simulações (sem DOM)
     --------------------------------------------------------------- */
  /* Primeiro instante r >= t em que o botão está apertado (taps = [{s,e}], LOW em [s, e)). null se nunca mais. */
  function firstRead(taps, t) {
    var best = null;
    taps.forEach(function (k) {
      if (k.e > t) { var r = Math.max(t, k.s); if (r < k.e && (best === null || r < best)) best = r; }
    });
    return best;
  }
  /* App 1: if (LOW) { LED 1 s aceso, 1 s apagado }. Livre, o loop lê o botão o tempo todo. */
  function app1(taps, H) {
    var t = 0, out = { ciclos: [], led: [], deaf: [], serial: [] };
    while (t < H) {
      var r = firstRead(taps, t); if (r === null || r >= H) break;
      out.ciclos.push(r); out.led.push([r, r + 1000]); out.deaf.push([r, r + 2000]);
      out.serial.push([r, "Botão pressionado! LED - pisca"]);
      t = r + 2000;
    }
    return out;
  }
  /* App 2: while (HIGH) {} e depois for com 5 piscadas de 2 s (10 s). */
  function app2(taps, H) {
    var t = 0, out = { ciclos: [], led: [], deaf: [], serial: [] };
    out.serial.push([0, "Pressione o botão para piscar o LED 5 vezes"]);
    while (t < H) {
      var r = firstRead(taps, t); if (r === null || r >= H) break;
      out.ciclos.push(r);
      out.serial.push([r, "Botão pressionado! LED - pisca"]);
      for (var k = 0; k < 5; k++) out.led.push([r + 2000 * k, r + 2000 * k + 1000]);
      out.deaf.push([r, r + 10000]);
      t = r + 10000;
      if (t < H) out.serial.push([t, "Pressione o botão para piscar o LED 5 vezes"]);
    }
    return out;
  }
  function percebido(taps, ciclos) {
    return taps.map(function (k) { return ciclos.some(function (r) { return r >= k.s && r < k.e; }); });
  }
  function soma(ints, H) { return ints.reduce(function (a, p) { return a + Math.max(0, Math.min(p[1], H) - Math.min(p[0], H)); }, 0); }

  /* Toques de 150 ms a cada "cada" ms, o primeiro em 600 ms. */
  function toquesRegulares(cada, H) { var a = []; for (var s = 600; s < H; s += cada) a.push({ s: s, e: s + 150 }); return a; }
  /* Versão com delay: lê o botão e coleta em 0, I, 2I... e fica surda entre uma coisa e outra. */
  function laneDelay(I, H, taps) {
    var reads = []; for (var t = 0; t < H; t += I) reads.push(t);
    return { leituras: reads, coletas: reads.slice(), percebidos: taps.map(function (k) { return reads.some(function (r) { return r >= k.s && r < k.e; }); }) };
  }
  /* Versão com millis: lê a cada volta (microssegundos) e coleta quando passam I ms desde a última coleta. */
  function laneMillis(I, H, taps) {
    var coletas = []; for (var t = I; t < H; t += I) coletas.push(t);
    return { coletas: coletas, percebidos: taps.map(function (k) { return k.e - k.s >= 1; }) };
  }
  /* Loop da aula 9 com o botão apertado desde o início. Volta de espera: D ms (imprime o AVISO). Volta de coleta termina com delay(extra). */
  function voltasAula(I, D, extra, quantas) {
    var t = 0, ant = 0, fires = [], avisos = [], av = 0;
    while (fires.length < quantas && t < 600000) {
      if (t - ant >= I) { fires.push(t); avisos.push(av); av = 0; ant = t; t += extra; }
      else { av++; t += D; }
    }
    return { coletas: fires, avisos: avisos };
  }
  /* Estouro do millis(): tempoAnterior fica X ms antes do fim do contador de 32 bits; passam "dec" ms. */
  var M32 = 4294967296n, M64 = 18446744073709551616n;
  function mod(a, m) { return ((a % m) + m) % m; }
  function estouro(X, dec, I) {
    var ant = mod(M32 - BigInt(X), M32), agora = mod(ant + BigInt(dec), M32), big = BigInt(I);
    var dif32 = mod(agora - ant, M32), limite = mod(ant + big, M32), dif64 = mod(agora - ant, M64);
    var deveria = dec >= I;
    return {
      ant: ant, agora: agora, estourou: agora < ant, deveria: deveria,
      a: { valor: dif32, dispara: dif32 >= big }, b: { valor: limite, dispara: agora >= limite }, c: { valor: dif64, dispara: dif64 >= big }
    };
  }
  E.embSim = { firstRead: firstRead, app1: app1, app2: app2, percebido: percebido, soma: soma, toquesRegulares: toquesRegulares, laneDelay: laneDelay, laneMillis: laneMillis, voltasAula: voltasAula, estouro: estouro };

  /* ---------------------------------------------------------------
     Cap 8: o botão com if e com while
     --------------------------------------------------------------- */
  E.demos.botaoFluxo = function (el) {
    el.innerHTML = '<h4>Dois toques no botão: o que cada app percebe?</h4>' +
      '<div class="ctrls"><label>app <select id="bf-a"><option value="1">App 1: if (pisca enquanto aperta)</option><option value="2">App 2: while + pisca 5 vezes</option></select></label></div>' +
      '<div class="ctrls"><label>toque 1 começa em <input type="range" id="bf-s1" min="0" max="6000" step="100" value="500"><output id="bf-s1o"></output></label><label>dura <input type="range" id="bf-d1" min="50" max="3000" step="50" value="300"><output id="bf-d1o"></output></label></div>' +
      '<div class="ctrls"><label>toque 2 começa em <input type="range" id="bf-s2" min="0" max="10000" step="100" value="1500"><output id="bf-s2o"></output></label><label>dura <input type="range" id="bf-d2" min="50" max="3000" step="50" value="300"><output id="bf-d2o"></output></label></div>' +
      '<canvas style="height:196px;cursor:default"></canvas><div class="sg"></div><div class="grid2"><div><b>Monitor Serial</b><pre class="raw bf-o" style="min-height:90px"></pre></div><div class="read"></div></div>';
    var g = function (id) { return el.querySelector(id); }, cv = el.querySelector("canvas"), H = 12000, S = null;
    function ler() {
      var taps = [{ s: +g("#bf-s1").value, e: +g("#bf-s1").value + +g("#bf-d1").value }, { s: +g("#bf-s2").value, e: +g("#bf-s2").value + +g("#bf-d2").value }];
      var app = g("#bf-a").value === "1" ? 1 : 2, r = app === 1 ? app1(taps, H) : app2(taps, H);
      return { taps: taps, app: app, r: r, ok: percebido(taps, r.ciclos) };
    }
    var api = E.canvas(cv, function (ctx, w, h, c) {
      if (!S) return;
      var padL = 12, padR = 12, X = function (ms) { return padL + Math.min(ms, H) / H * (w - padL - padR); };
      var lanes = [{ y: 34, t: "botão (apertado = LOW)" }, { y: 88, t: "o que o programa está fazendo" }, { y: 142, t: "LED" }], bh = 26;
      ctx.save(); ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "left";
      ctx.strokeStyle = c.line; ctx.fillStyle = c.muted;
      for (var s = 0; s <= 12; s += 2) { ctx.beginPath(); ctx.moveTo(X(s * 1000), 14); ctx.lineTo(X(s * 1000), h - 20); ctx.stroke(); ctx.textAlign = "center"; ctx.fillText(s + " s", X(s * 1000), h - 6); }
      ctx.textAlign = "left"; ctx.fillStyle = c.ink; ctx.font = "600 11px Inter,system-ui,sans-serif";
      lanes.forEach(function (l) { ctx.fillText(l.t, padL, l.y - 6); });
      /* programa: lendo (verde) e surdo (vermelho) */
      ctx.fillStyle = c.green; ctx.globalAlpha = .55; ctx.fillRect(X(0), lanes[1].y, X(H) - X(0), bh); ctx.globalAlpha = 1;
      ctx.fillStyle = c.red; S.r.deaf.forEach(function (p) { ctx.fillRect(X(p[0]), lanes[1].y, Math.max(2, X(p[1]) - X(p[0])), bh); });
      ctx.fillStyle = c.ink; ctx.font = "10px Inter,system-ui,sans-serif"; ctx.textAlign = "left";
      S.r.deaf.forEach(function (p) { if (X(p[1]) - X(p[0]) > 70) { ctx.fillStyle = "#fff"; ctx.fillText("surdo (delay)", X(p[0]) + 5, lanes[1].y + 17); } });
      ctx.fillStyle = c.ink; ctx.fillText(S.app === 1 ? "verde: lendo o botão a cada volta" : "verde: preso no while, só lendo o botão", padL, lanes[1].y + bh + 12);
      /* toques */
      S.taps.forEach(function (k, i) {
        var ok = S.ok[i]; ctx.fillStyle = ok ? c.pen : c.muted; ctx.globalAlpha = ok ? 1 : .85;
        ctx.fillRect(X(k.s), lanes[0].y, Math.max(4, X(k.e) - X(k.s)), bh); ctx.globalAlpha = 1;
        ctx.fillStyle = ok ? c.pen : c.red; ctx.font = "700 11px Inter,system-ui,sans-serif"; ctx.textAlign = "left";
        var tx = Math.min(X(k.s) + 2, w - 90); ctx.fillText((i + 1) + (ok ? ": percebido" : ": IGNORADO"), tx, lanes[0].y + bh + 12);
      });
      /* LED */
      ctx.fillStyle = c.c1; S.r.led.forEach(function (p) { if (p[0] < H) ctx.fillRect(X(p[0]), lanes[2].y, Math.max(2, X(p[1]) - X(p[0])), bh); });
      ctx.restore();
    });
    function go() {
      ["s1", "d1", "s2", "d2"].forEach(function (k) { g("#bf-" + k + "o").textContent = seg(+g("#bf-" + k).value) + " s"; });
      S = ler();
      var nOk = S.ok.filter(Boolean).length, led = soma(S.r.led, H), surdo = soma(S.r.deaf, H);
      g(".sg").innerHTML = cards([["toques percebidos", nOk + " de 2"], ["LED aceso (nos 12 s)", fb(led / 1000, 1) + " s"], ["programa surdo (nos 12 s)", fb(surdo / 1000, 1) + " s"]]);
      g(".bf-o").textContent = S.r.serial.filter(function (p) { return p[0] <= H; }).map(function (p) { return "[t = " + seg(p[0]) + " s]  " + p[1]; }).join("\n") || "(nada impresso)";
      var msg = S.taps.map(function (k, i) {
        if (S.ok[i]) return "Toque " + (i + 1) + ": percebido, porque o programa estava lendo o botão quando ele ficou apertado.";
        var cai = S.r.deaf.some(function (p) { return k.s >= p[0] && k.s < p[1]; });
        return "Toque " + (i + 1) + ": <b>ignorado</b>" + (cai ? ", caiu em cima de um <code>delay</code> e acabou antes de o programa olhar de novo." : ", terminou antes de o programa voltar a ler o botão.");
      }).join("<br>");
      g(".read").innerHTML = msg + "<br><span class='muted'>Modelo simplificado: lendo o botão, o loop reage na hora (volta de microssegundos, suposição); os <code>delay</code> são exatos e o resto do código custa 0 ms.</span>";
      api.paint();
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---------------------------------------------------------------
     Cap 9: delay x millis lado a lado
     --------------------------------------------------------------- */
  E.demos.delayMillis = function (el) {
    el.innerHTML = '<h4>12 segundos com delay e com millis</h4>' +
      '<div class="ctrls"><label>INTERVALO_COLETA <input type="range" id="dm-i" min="500" max="3000" step="100" value="2100"><output id="dm-io"></output></label><label>um toque a cada <input type="range" id="dm-t" min="400" max="2000" step="100" value="1000"><output id="dm-to"></output></label></div>' +
      '<canvas style="height:206px;cursor:default"></canvas><div class="sg"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, cv = el.querySelector("canvas"), H = 12000, S = null;
    var api = E.canvas(cv, function (ctx, w, h, c) {
      if (!S) return;
      var padL = 12, padR = 12, X = function (ms) { return padL + ms / H * (w - padL - padR); }, bh = 26;
      var ys = [34, 90, 146];
      ctx.save(); ctx.font = "11px Inter,system-ui,sans-serif"; ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.textAlign = "center";
      for (var s = 0; s <= 12; s += 2) { ctx.beginPath(); ctx.moveTo(X(s * 1000), 14); ctx.lineTo(X(s * 1000), h - 20); ctx.stroke(); ctx.fillText(s + " s", X(s * 1000), h - 6); }
      ctx.textAlign = "left"; ctx.fillStyle = c.ink; ctx.font = "600 11px Inter,system-ui,sans-serif";
      ctx.fillText("toques no botão (150 ms cada)", padL, ys[0] - 6); ctx.fillText("com delay(INTERVALO)", padL, ys[1] - 6); ctx.fillText("com millis()", padL, ys[2] - 6);
      S.taps.forEach(function (k, i) { ctx.fillStyle = S.d.percebidos[i] ? c.pen : c.red; ctx.fillRect(X(k.s), ys[0], Math.max(3, X(k.e) - X(k.s)), bh); });
      /* delay: vermelho (surdo) com leituras em verde */
      ctx.fillStyle = c.red; ctx.globalAlpha = .6; ctx.fillRect(X(0), ys[1], X(H) - X(0), bh); ctx.globalAlpha = 1;
      ctx.fillStyle = c.green; S.d.leituras.forEach(function (r) { ctx.fillRect(X(r) - 1.5, ys[1], 3, bh); });
      /* millis: tudo verde */
      ctx.fillStyle = c.green; ctx.globalAlpha = .6; ctx.fillRect(X(0), ys[2], X(H) - X(0), bh); ctx.globalAlpha = 1;
      ctx.fillStyle = c.c1; S.d.coletas.forEach(function (r) { ctx.beginPath(); ctx.arc(X(r), ys[1] + bh / 2, 6, 0, 6.2832); ctx.fill(); });
      S.m.coletas.forEach(function (r) { ctx.beginPath(); ctx.arc(X(r), ys[2] + bh / 2, 6, 0, 6.2832); ctx.fill(); });
      ctx.fillStyle = c.muted; ctx.font = "10px Inter,system-ui,sans-serif"; ctx.fillText("vermelho: surdo · verde: lendo o botão · laranja: coleta do DHT22", padL, h - 22 + 0);
      ctx.restore();
    });
    function go() {
      var I = +g("#dm-i").value, T = +g("#dm-t").value; g("#dm-io").textContent = I + " ms"; g("#dm-to").textContent = T + " ms";
      var taps = toquesRegulares(T, H); S = { taps: taps, d: laneDelay(I, H, taps), m: laneMillis(I, H, taps) };
      var nd = S.d.percebidos.filter(Boolean).length, nm = S.m.percebidos.filter(Boolean).length;
      g(".sg").innerHTML = cards([["toques no total", String(taps.length)], ["percebidos com delay", nd + " de " + taps.length], ["percebidos com millis", nm + " de " + taps.length], ["coletas com delay", String(S.d.coletas.length)], ["coletas com millis", String(S.m.coletas.length)]]);
      g(".read").innerHTML = "Com <code>delay(" + I + ")</code> o programa só olha o botão nos instantes " + S.d.leituras.map(function (r) { return r / 1000; }).join(", ").replace(/\./g, ",") + " s, e cada toque dura só 150 ms: " + (nd === 0 ? "<b>nenhum toque</b> cai numa leitura." : "só " + nd + " caiu numa leitura" + (nd === 1 ? " (por coincidência, o toque começou justo no instante da leitura)." : ".")) + " Com <code>millis()</code> as coletas continuam a cada " + I + " ms (a primeira só em " + I + " ms, porque <code>tempoAnterior</code> começa em 0), e o botão é lido a cada volta: <b>" + nm + " de " + taps.length + "</b>." + "<br><span class='muted'>Programa de exemplo para comparar, não é o código da aula. Supõe que uma volta sem coleta dura microssegundos e que a coleta custa 0 ms.</span>";
      api.paint();
    }
    el.addEventListener("input", go); go();
  };

  /* ---------------------------------------------------------------
     Cap 9: o padrão guardar e comparar, volta a volta
     --------------------------------------------------------------- */
  var AV = "AVISO: DHT22 requer espera de 2 segundos para coleta";
  E.demos.voltasMillis = function (el) {
    el.innerHTML = '<h4>Quando cada coleta dispara no código da aula</h4>' +
      '<div class="ctrls"><label>INTERVALO_COLETA <input type="range" id="vm-i" min="500" max="3000" step="100" value="2100"><output id="vm-io"></output></label><label>uma volta de espera dura <input type="range" id="vm-d" min="1" max="700" step="1" value="5"><output id="vm-do"></output></label><label>botão <select id="vm-b"><option value="1">apertado desde o início</option><option value="0">solto</option></select></label></div>' +
      '<div class="vm-t"></div><div class="grid2"><div><b>Monitor Serial (resumido)</b><pre class="raw vm-o" style="min-height:120px"></pre></div><div class="read"></div></div>';
    var g = function (id) { return el.querySelector(id); }, EXTRA = 100;
    function go() {
      var I = +g("#vm-i").value, D = +g("#vm-d").value, ap = g("#vm-b").value === "1"; g("#vm-io").textContent = I + " ms"; g("#vm-do").textContent = D + " ms";
      if (!ap) {
        g(".vm-t").innerHTML = ""; g(".vm-o").textContent = "(nada: o programa está preso no while,\nsem coletar e sem imprimir o AVISO)";
        g(".read").innerHTML = "Com o botão solto, <code>while (digitalRead(BTN_PIN) == HIGH)</code> nunca termina. O <code>millis()</code> nem chega a ser consultado. É o limite que a nota da aula aponta no próprio código.";
        return;
      }
      var R = voltasAula(I, D, EXTRA, 6), rows = R.coletas.map(function (t, k) {
        return "<tr><td>" + (k + 1) + "</td><td>" + t + " ms</td><td>" + (k ? (t - R.coletas[k - 1]) + " ms" : "desde a partida") + "</td><td>" + R.avisos[k] + "</td></tr>";
      }).join("");
      g(".vm-t").innerHTML = '<div class="tablewrap"><table><tr><th>coleta</th><th>dispara em</th><th>intervalo desde a anterior</th><th>linhas de AVISO antes dela</th></tr>' + rows + "</table></div>";
      var o = [], t0 = R.coletas[0];
      function aviso(t) { return "[t = " + t + " ms]  " + AV; }
      o.push(aviso(0)); if (R.avisos[0] > 1) o.push(aviso(D));
      if (R.avisos[0] > 2) o.push("   ... mais " + (R.avisos[0] - 2) + " linhas de AVISO");
      o.push("[t = " + t0 + " ms]  coleta 1: temperatura, umidade, índice de calor");
      if (R.coletas.length > 1) {
        o.push(aviso(t0 + EXTRA)); if (R.avisos[1] > 1) o.push("   ... mais " + (R.avisos[1] - 1) + " linhas de AVISO");
        o.push("[t = " + R.coletas[1] + " ms]  coleta 2: temperatura, umidade, índice de calor");
      }
      g(".vm-o").textContent = o.join("\n");
      var dur = R.coletas[1] - R.coletas[0], exato = dur === I;
      g(".read").innerHTML = "A primeira coleta só acontece em <b>" + t0 + " ms</b>: <code>tempoAnterior</code> começa em 0 e a diferença só chega a " + I + " na primeira volta que passa de " + I + " ms. Depois, o intervalo entre coletas é <b>" + dur + " ms</b>" + (exato ? ", igual ao INTERVALO." : ", e não " + I + ": o <code>delay(100)</code> do fim da volta de coleta e o tamanho da volta de espera ( " + D + " ms ) empurram a próxima coleta. O intervalo é um <b>mínimo</b>.") + " Entre duas coletas o código imprime <b>" + R.avisos[1] + "</b> linhas de AVISO." + "<br><span class='muted'>Modelo: o botão fica apertado, cada volta de espera custa " + D + " ms (imprimir o AVISO), a volta de coleta termina com <code>delay(100)</code> e a leitura do DHT22 e os prints da coleta custam 0 ms.</span>";
    }
    el.addEventListener("input", go); el.addEventListener("change", go); go();
  };

  /* ---------------------------------------------------------------
     Cap 9 (complemento): o millis() estoura
     --------------------------------------------------------------- */
  function big(b) { return b.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  E.demos.estouroMillis = function (el) {
    el.innerHTML = '<h4>A coleta que cai na emenda do contador</h4>' +
      '<div class="ctrls"><label>a última coleta foi X ms antes do fim do contador, X = <input type="range" id="eo-x" min="100" max="5000" step="100" value="1000"><output id="eo-xo"></output></label><label>desde então passaram <input type="range" id="eo-d" min="100" max="4000" step="100" value="500"><output id="eo-do"></output></label></div>' +
      '<div class="eo-s"></div><div class="tablewrap eo-t"></div><div class="read"></div>';
    var g = function (id) { return el.querySelector(id); }, I = 2100;
    function go() {
      var X = +g("#eo-x").value, d = +g("#eo-d").value; g("#eo-xo").textContent = X + " ms"; g("#eo-do").textContent = d + " ms";
      var R = estouro(X, d, I);
      g(".eo-s").innerHTML = cards([["tempoAnterior (guardado)", big(R.ant)], ["millis() agora", big(R.agora)], ["o contador estourou?", R.estourou ? "sim, voltou a 0" : "não"], ["tempo real decorrido", d + " ms"]]);
      function veredito(disp) { var ok = disp === R.deveria; return '<b style="color:var(--' + (ok ? "green" : "red") + ')">' + (disp ? "coleta" : "não coleta") + (ok ? ": certo" : ": ERRADO") + "</b>"; }
      g(".eo-t").innerHTML = "<table><tr><th>como a condição é escrita</th><th>valor da conta</th><th>contra " + I + "</th></tr>" +
        "<tr><td><code>millis() - tempoAnterior &gt;= 2100</code><br><small class='muted'>unsigned long, 32 bits</small></td><td>" + big(R.a.valor) + "</td><td>" + veredito(R.a.dispara) + "</td></tr>" +
        "<tr><td><code>millis() &gt;= tempoAnterior + 2100</code><br><small class='muted'>32 bits, soma antes de comparar</small></td><td>limite = " + big(R.b.valor) + "</td><td>" + veredito(R.b.dispara) + "</td></tr>" +
        "<tr><td><code>millis() - tempoAnterior &gt;= 2100</code><br><small class='muted'>com tempoAnterior uint64_t (código da aula)</small></td><td>" + big(R.c.valor) + "</td><td>" + veredito(R.c.dispara) + "</td></tr></table>";
      g(".read").innerHTML = "Deveria coletar? <b>" + (R.deveria ? "sim" : "não") + "</b> (passaram " + d + " ms, o intervalo é " + I + "). A subtração em 32 bits sem sinal dá o tempo real mesmo depois do estouro. Somar antes de comparar quebra quando a soma passa de 2<sup>32</sup>. Com <code>uint64_t</code> a conta é feita em 64 bits, e <code>100 - 4294966296</code> deixa de dar 1100 e vira um número gigante: coleta cedo, uma única vez.<br><span class='muted'>Contas feitas com BigInt, seguindo as regras de conversão do C++ (código não compilado aqui).</span>";
    }
    el.addEventListener("input", go); go();
  };
})();
