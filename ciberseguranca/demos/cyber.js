/* Demos da apostila de Cibersegurança */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- cap 1: encapsulamento pelas camadas OSI ---- */
  E.demos.osi = function (el) {
    var L = [
      ["7 Aplicação", "HTTP", "GET /index.html", "var(--c0)"], ["6 Apresentação", "TLS", "dados cifrados", "var(--c2)"], ["5 Sessão", "Sessão", "id da sessão", "var(--c0)"],
      ["4 Transporte", "TCP", "porta 51234 → 443", "var(--c1)"], ["3 Rede", "IP", "192.168.0.10 → 203.0.113.7", "var(--green)"], ["2 Enlace", "Ethernet", "MAC origem → MAC destino", "var(--amber)"], ["1 Física", "Bits", "sinais elétricos, ópticos ou de rádio", "var(--red)"]];
    el.innerHTML = '<h4>Mande uma mensagem e veja cada camada acrescentar a sua parte</h4>' +
      '<div class="ctrls"><label>mensagem <input type="text" id="om" value="Olá, servidor!" style="min-width:220px"></label><button class="btn sm pri" type="button" id="os">▶ Enviar (de cima para baixo)</button><button class="btn sm" type="button" id="or">◀ Receber (de baixo para cima)</button></div>' +
      '<div class="osi" style="display:grid;gap:6px;margin:8px 0"></div><div class="read"></div>';
    var box = el.querySelector(".osi"), rd = el.querySelector(".read"), timer = 0, msg = el.querySelector("#om");
    function draw(n, dir) {
      var h = ""; L.forEach(function (l, i) {
        var on = dir === "down" ? i <= n : i >= n && n >= 0;
        var cur = i === n;
        var inner = on ? L.slice(0, i + 1).reverse().map(function (x) { return '<span style="padding:2px 8px;border-radius:6px;background:color-mix(in srgb,' + x[3] + ' 22%,var(--card));border:1.5px solid ' + x[3] + ';font-size:.78rem;font-weight:700">' + x[1] + '</span>'; }).join("") + ' <span style="padding:2px 8px;border-radius:6px;background:var(--paper-2);font-size:.78rem">' + esc(msg.value || "...") + '</span>' : "";
        h += '<div style="display:grid;grid-template-columns:130px 1fr;gap:8px;align-items:center;padding:6px 10px;border:2px solid ' + (cur ? "var(--ink)" : "var(--line)") + ';border-radius:10px;background:' + (cur ? "var(--hl-y)" : "var(--card)") + ';transition:.3s"><b style="font-size:.85rem">' + l[0] + '</b><div style="display:flex;gap:4px;flex-wrap:wrap;min-height:26px">' + inner + '</div></div>';
      }); box.innerHTML = h;
    }
    function run(dir) {
      clearInterval(timer); var i = dir === "down" ? 0 : L.length - 1; draw(i, dir);
      var step = function () {
        var l = L[i]; rd.innerHTML = dir === "down" ? "<b>" + l[0] + "</b>: acrescenta o cabeçalho <b>" + l[1] + "</b> (" + l[2] + "). A mensagem <b>cresce</b> ao descer." : "<b>" + l[0] + "</b>: lê e <b>retira</b> o cabeçalho " + l[1] + " e entrega o resto à camada de cima.";
        draw(i, dir); i += dir === "down" ? 1 : -1; if (i < 0 || i >= L.length) { clearInterval(timer); setTimeout(function () { rd.innerHTML += dir === "down" ? " Chegou à camada física: vira sinal no cabo ou no ar." : " Na aplicação, o servidor lê a mensagem original."; }, 50); }
      };
      step(); timer = setInterval(step, E.reduce ? 10 : 900);
    }
    el.querySelector("#os").addEventListener("click", function () { run("down"); }); el.querySelector("#or").addEventListener("click", function () { run("up"); });
    draw(-1, "down"); rd.innerHTML = "Cada camada <b>embrulha</b> o que recebe de cima com o seu cabeçalho. É o <i>encapsulamento</i>. No destino, o caminho é o inverso.";
  };

  /* ---- cap 2: calculadora de IP e máscara (CIDR) ---- */
  function ip2n(s) { var p = s.split("."); if (p.length !== 4) return null; var n = 0; for (var i = 0; i < 4; i++) { var v = +p[i]; if (p[i] === "" || isNaN(v) || v < 0 || v > 255) return null; n = n * 256 + v; } return n; }
  function n2ip(n) { return [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join("."); }
  function bin(n) { return [24, 16, 8, 0].map(function (s) { return ("00000000" + ((n >>> s) & 255).toString(2)).slice(-8); }).join("."); }
  E.demos.ipcalc = function (el) {
    el.innerHTML = '<h4>Endereço IPv4 em binário e a divisão em redes</h4><div class="ctrls"><label>IP <input type="text" id="ci" value="192.168.10.77" style="width:150px;font-family:var(--f-mono)"></label><label>prefixo /<input type="number" id="cp" value="24" min="0" max="32" style="width:70px"></label></div><div class="tablewrap"><table class="ct"></table></div><div class="read"></div>';
    var ci = el.querySelector("#ci"), cp = el.querySelector("#cp"), ct = el.querySelector(".ct"), rd = el.querySelector(".read");
    function go() {
      var ip = ip2n(ci.value.trim()), p = Math.max(0, Math.min(32, parseInt(cp.value, 10) || 0));
      if (ip === null) { ct.innerHTML = ""; rd.textContent = "Digite um IPv4 válido, como 192.168.10.77."; return; }
      var mask = p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0, net = (ip & mask) >>> 0, bc = (net | (~mask >>> 0)) >>> 0, hosts = p >= 31 ? (p === 32 ? 1 : 2) : Math.pow(2, 32 - p) - 2;
      var b = bin(ip); var parte = b.replace(/\./g, ""); var colorido = ""; var cnt = 0; for (var i = 0; i < parte.length; i++) { if (i && i % 8 === 0) colorido += "."; colorido += '<span style="color:var(--' + (i < p ? "c0" : "c1") + ')">' + parte[i] + '</span>'; cnt++; }
      ct.innerHTML = '<tr><th>IP</th><td><code>' + n2ip(ip) + '</code></td></tr><tr><th>Em binário</th><td><code>' + colorido + '</code><br><small class="muted"><span style="color:var(--c0)">azul</span>: parte da rede (' + p + ' bits) · <span style="color:var(--c1)">laranja</span>: parte do dispositivo (' + (32 - p) + ' bits)</small></td></tr>' +
        '<tr><th>Máscara</th><td><code>' + n2ip(mask) + '</code></td></tr><tr><th>Endereço da rede</th><td><code>' + n2ip(net) + '/' + p + '</code></td></tr><tr><th>Broadcast</th><td><code>' + n2ip(bc) + '</code></td></tr><tr><th>Dispositivos possíveis</th><td><b>' + E.fmt(hosts) + '</b></td></tr>';
      var priv = (ip >>> 24 === 10) || ((ip >>> 20) === 0xAC1) || ((ip >>> 16) === 0xC0A8);
      rd.innerHTML = "Os <b>" + p + "</b> primeiros bits identificam a rede, e os outros " + (32 - p) + " identificam cada dispositivo nela. " + (p <= 30 ? "Dois endereços são reservados (o da rede e o de broadcast), por isso " + E.fmt(Math.pow(2, 32 - p)) + " − 2 = " + E.fmt(hosts) + ". " : "") + (priv ? "Este IP está numa faixa <b>privada</b> (10.0.0.0/8, 172.16.0.0/12 ou 192.168.0.0/16): não é roteado na internet pública." : "Este IP está numa faixa pública (ou especial).");
    }
    ci.addEventListener("input", go); cp.addEventListener("input", go); go();
  };

  /* ---- cap 3: consulta DNS de verdade (DNS público do Google, via HTTPS) ---- */
  E.demos.dnsquery = function (el) {
    el.innerHTML = '<h4>Pergunte a um servidor DNS de verdade</h4><div class="ctrls"><label>domínio <input type="text" id="dn" value="example.com" style="width:200px;font-family:var(--f-mono)"></label><label>tipo <select id="dt"><option>A</option><option>AAAA</option><option>MX</option><option>NS</option><option>TXT</option><option>CNAME</option></select></label><button class="btn sm pri" type="button" id="db">Consultar</button></div><div class="sqlres"></div><div class="read">A consulta sai do <b>seu navegador</b> para o DNS público do Google (<code>dns.google</code>), por HTTPS. É o mesmo que <code>nslookup</code> ou <code>dig</code> fariam.</div>';
    var res = el.querySelector(".sqlres"), rd = el.querySelector(".read");
    function go() {
      var n = el.querySelector("#dn").value.trim(), t = el.querySelector("#dt").value; if (!/^[a-z0-9.-]+$/i.test(n)) { rd.textContent = "Digite só o nome do domínio (sem http://)."; return; }
      rd.textContent = "Consultando..."; res.innerHTML = "";
      fetch("https://dns.google/resolve?name=" + encodeURIComponent(n) + "&type=" + t).then(function (r) { return r.json(); }).then(function (j) {
        var tipos = { 1: "A", 28: "AAAA", 15: "MX", 2: "NS", 16: "TXT", 5: "CNAME" };
        if (!j.Answer) { rd.innerHTML = "Sem resposta do tipo <b>" + t + "</b> para <b>" + esc(n) + "</b> (código " + j.Status + (j.Status === 3 ? ": o domínio não existe (NXDOMAIN)" : "") + ")."; return; }
        res.innerHTML = '<table><tr><th>nome</th><th>tipo</th><th>TTL (s)</th><th>dado</th></tr>' + j.Answer.map(function (a) { return '<tr><td>' + esc(a.name) + '</td><td>' + (tipos[a.type] || a.type) + '</td><td>' + a.TTL + '</td><td><code>' + esc(a.data) + '</code></td></tr>'; }).join("") + '</table>';
        rd.innerHTML = "O <b>TTL</b> diz por quantos segundos esta resposta pode ficar no <b>cache</b> antes de precisar ser perguntada de novo.";
      }).catch(function () { rd.innerHTML = '<span style="color:var(--red)">Não consegui consultar (sem internet, ou o navegador bloqueou). Rode <code>nslookup ' + esc(n) + '</code> no terminal para ver o mesmo resultado.</span>'; });
    }
    el.querySelector("#db").addEventListener("click", go); el.querySelector("#dn").addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
  };

  /* ---- cap 4: DNS tunneling (didático): dados viram nomes de subdomínio ---- */
  function b32(bytes) { var A = "abcdefghijklmnopqrstuvwxyz234567", out = "", bits = 0, val = 0; for (var i = 0; i < bytes.length; i++) { val = (val << 8) | bytes[i]; bits += 8; while (bits >= 5) { out += A[(val >>> (bits - 5)) & 31]; bits -= 5; } } if (bits > 0) out += A[(val << (5 - bits)) & 31]; return out; }
  E.demos.tunel = function (el) {
    el.innerHTML = '<h4>Como dados "viram" consultas DNS (modelo didático)</h4><div class="ctrls"><label>dado "roubado" <input type="text" id="td" value="senha=1234; cartao=0000" style="min-width:260px"></label></div><pre class="jq" style="margin:8px 0;white-space:pre-wrap"></pre><div class="read"></div>';
    var td = el.querySelector("#td"), jq = el.querySelector(".jq"), rd = el.querySelector(".read");
    function go() {
      var bytes = Array.prototype.slice.call(new TextEncoder().encode(td.value)), code = b32(bytes), parts = []; for (var i = 0; i < code.length; i += 20) parts.push(code.slice(i, i + 20));
      jq.textContent = parts.map(function (p, i) { return p + "." + (i + 1) + ".t.dominio-do-atacante.test   (consulta " + (i + 1) + ")"; }).join("\n") || "(digite algo)";
      rd.innerHTML = "O dado foi codificado em <b>base32</b> e quebrado em pedaços de 20 caracteres, cada um virando um <b>subdomínio</b>. Seriam <b>" + parts.length + "</b> consulta(s) DNS aparentemente comuns, que o resolvedor local encaminha até o servidor autoritativo do atacante, que remonta o dado. O domínio é fictício (<code>.test</code> é reservado e nunca resolve).<br><b>Como detectar:</b> subdomínios longos e de aparência aleatória, <b>volume anormal</b> de consultas para um único domínio, muitas respostas do tipo TXT, e domínios recém-registrados.";
    }
    td.addEventListener("input", go); go();
  };

  /* ---- cap 5: força bruta: quanto tempo leva ---- */
  E.demos.senha = function (el) {
    el.innerHTML = '<h4>Quanto tempo uma força bruta leva?</h4><div class="ctrls"><label>tamanho <input type="range" id="sl" min="4" max="20" value="8"><output id="slo">8</output></label><label>alfabeto <select id="sa"><option value="10">só dígitos (10)</option><option value="26">letras minúsculas (26)</option><option value="52">maiúsculas e minúsculas (52)</option><option value="62">letras e dígitos (62)</option><option value="94" selected>todos os símbolos do teclado (94)</option></select></label><label>tentativas por segundo <select id="sr"><option value="100">100 (login online com limite)</option><option value="1000000">1 milhão (servidor fraco)</option><option value="10000000000" selected>10 bilhões (hash rápido roubado)</option></select></label></div><div class="read"></div>' +
      '<p class="muted" style="font-size:.85rem;margin:8px 0 0">As velocidades são <b>ilustrativas</b>: servem para comparar ordens de grandeza, não para prever um ataque real.</p>';
    var sl = el.querySelector("#sl"), sa = el.querySelector("#sa"), sr = el.querySelector("#sr"), rd = el.querySelector(".read");
    function human(s) { var U = [["milênios", 3.15e10], ["séculos", 3.15e9], ["anos", 3.15e7], ["dias", 86400], ["horas", 3600], ["minutos", 60], ["segundos", 1]]; if (s < 1) return "menos de 1 segundo"; for (var i = 0; i < U.length; i++) if (s >= U[i][1]) { var v = s / U[i][1]; return (v >= 1e6 ? v.toExponential(1).replace("e+", " × 10^") : E.fmt(v, v < 10 ? 1 : 0)) + " " + U[i][0]; } return "?"; }
    function go() {
      var L = +sl.value, A = +sa.value, R = +sr.value; el.querySelector("#slo").textContent = L;
      var comb = Math.pow(A, L), bits = L * Math.log2(A), t = comb / R / 2; // em média, metade do espaço
      rd.innerHTML = "Combinações possíveis: <b>" + (comb >= 1e15 ? comb.toExponential(2).replace("e+", " × 10^") : E.fmt(comb)) + "</b> (cerca de <b>" + E.fmt(bits, 0) + " bits</b> de entropia, se escolhida ao acaso). Tempo médio para acertar: <b>" + human(t) + "</b>." +
        "<br><span class='muted'>Cada caractere a mais multiplica o tempo por " + A + ". Por isso o <b>tamanho</b> pesa mais do que a variedade. E uma senha <i>previsível</i> (nome, data, 'senha123') cai em segundos por <b>dicionário</b>, qualquer que seja o tamanho.</span>";
    }
    sl.addEventListener("input", go); sa.addEventListener("change", go); sr.addEventListener("change", go); go();
  };

  /* ---- cap 5: XSS (mostra a diferença entre tratar entrada como HTML ou como texto) ---- */
  E.demos.xss = function (el) {
    el.innerHTML = '<h4>Um comentário num site: texto ou código?</h4><div class="ctrls"><label>comentário <input type="text" id="xc" value="<b>Ótimo post!</b> <script>roubaSessao()</script>" style="min-width:320px;font-family:var(--f-mono)"></label></div><div class="grid2"><div class="card" style="margin:0"><b style="color:var(--red)">Vulnerável: colado como HTML</b><p class="muted" style="font-size:.85rem;margin:.3em 0">O navegador trataria o texto como marcação. Aqui mostramos o que ele <i>enxergaria</i>:</p><pre class="xv" style="margin:6px 0;white-space:pre-wrap"></pre><div class="xr read"></div></div><div class="card" style="margin:0"><b style="color:var(--green)">Seguro: escapado</b><p class="muted" style="font-size:.85rem;margin:.3em 0">Os caracteres especiais viram texto inofensivo, que aparece na tela e nada mais:</p><pre class="xs" style="margin:6px 0;white-space:pre-wrap"></pre></div></div>';
    var xc = el.querySelector("#xc");
    function go() {
      var v = xc.value, perigoso = /<\s*script|on\w+\s*=|javascript:/i.test(v);
      el.querySelector(".xv").textContent = v; el.querySelector(".xs").textContent = v.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
      el.querySelector(".xr").innerHTML = perigoso ? "<b style='color:var(--red)'>Há código executável.</b> Num site vulnerável, o <code>&lt;script&gt;</code> rodaria no navegador de <b>quem abrir a página</b>, com acesso ao que aquela página acessa (a sessão, por exemplo)." : "Sem código executável neste texto. Tente incluir <code>&lt;script&gt;...&lt;/script&gt;</code>.";
    }
    xc.addEventListener("input", go); go();
  };

  /* ---- cap 6: hash de verdade (SHA-256 do navegador) ---- */
  E.demos.hash = function (el) {
    el.innerHTML = '<h4>Uma mudança de um caractere muda tudo</h4><div class="ctrls"><label>texto <input type="text" id="ht" value="senha123" style="min-width:240px;font-family:var(--f-mono)"></label></div><div class="tablewrap"><table class="ht"></table></div><div class="read"></div>';
    var ht = el.querySelector("#ht"), tb = el.querySelector(".ht"), rd = el.querySelector(".read");
    function sha(t) { return crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)).then(function (b) { return Array.prototype.map.call(new Uint8Array(b), function (x) { return ("0" + x.toString(16)).slice(-2); }).join(""); }); }
    function go() {
      if (!window.crypto || !crypto.subtle) { rd.textContent = "Este navegador não oferece crypto.subtle (precisa de HTTPS ou localhost)."; return; }
      var a = ht.value, b = a + "!"; Promise.all([sha(a), sha(b)]).then(function (h) {
        var diff = 0; for (var i = 0; i < 64; i++) if (h[0][i] !== h[1][i]) diff++;
        tb.innerHTML = '<tr><th>texto</th><th>SHA-256</th></tr><tr><td><code>' + esc(a) + '</code></td><td><code style="word-break:break-all">' + h[0] + '</code></td></tr><tr><td><code>' + esc(b) + '</code></td><td><code style="word-break:break-all">' + h[1] + '</code></td></tr>';
        rd.innerHTML = "Acrescentar só um <code>!</code> mudou <b>" + diff + " de 64</b> caracteres do resultado (o <i>efeito avalanche</i>). O hash tem sempre o mesmo tamanho (256 bits) e <b>não tem volta</b>: dá para conferir uma senha comparando hashes, mas não para recuperar a senha a partir do hash (só por tentativa e erro).";
      });
    }
    ht.addEventListener("input", go); go();
  };
  /* ---- cap 6: cifra de César (didática) ---- */
  E.demos.cesar = function (el) {
    el.innerHTML = '<h4>A cifra de César: a criptografia mais simples (e fraca)</h4><div class="ctrls"><label>texto <input type="text" id="ct" value="ATAQUE AO AMANHECER" style="min-width:240px"></label><label>chave (deslocamento) <input type="range" id="ck" min="1" max="25" value="3"><output id="cko">3</output></label></div><div class="tablewrap"><table class="cc"></table></div><div class="read"></div>';
    var ct = el.querySelector("#ct"), ck = el.querySelector("#ck"), tb = el.querySelector(".cc"), rd = el.querySelector(".read");
    function rot(t, k) { return t.replace(/[a-z]/gi, function (c) { var b = c <= "Z" ? 65 : 97; return String.fromCharCode((c.charCodeAt(0) - b + k + 26) % 26 + b); }); }
    function go() {
      var k = +ck.value; el.querySelector("#cko").textContent = k; var c = rot(ct.value, k);
      tb.innerHTML = '<tr><th>claro</th><td><code>' + esc(ct.value) + '</code></td></tr><tr><th>cifrado</th><td><code>' + esc(c) + '</code></td></tr><tr><th>decifrado</th><td><code>' + esc(rot(c, -k)) + '</code></td></tr>';
      rd.innerHTML = "Cada letra anda <b>" + k + "</b> posições no alfabeto. Quem tem a <b>chave</b> desfaz. O problema: só existem <b>25</b> chaves possíveis, então um atacante testa todas em segundos (força bruta), e a frequência das letras entrega a mensagem. Cifras modernas (AES) são desenhadas para que testar todas as chaves seja inviável.";
    }
    ct.addEventListener("input", go); ck.addEventListener("input", go); go();
  };
})();
