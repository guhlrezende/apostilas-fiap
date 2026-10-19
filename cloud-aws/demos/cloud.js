/* Demos da apostila de Cloud e AWS */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t == null ? "NULL" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ---- cap 1: quem cuida de quê em cada modelo ---- */
  var CAMADAS = ["Aplicações", "Dados", "Runtime e middleware", "Sistema operacional", "Virtualização", "Servidores e armazenamento", "Rede e data center"];
  var MODELOS = { "Local (on-premises)": [1, 1, 1, 1, 1, 1, 1], "IaaS (ex.: EC2)": [1, 1, 1, 1, 0, 0, 0], "PaaS (ex.: Elastic Beanstalk)": [1, 1, 0, 0, 0, 0, 0], "SaaS (ex.: Google Drive, Office 365)": [0, 0, 0, 0, 0, 0, 0] };
  E.demos.pilha = function (el) {
    var ks = Object.keys(MODELOS), cur = ks[1];
    el.innerHTML = '<h4>Quem cuida de cada camada?</h4><div class="ctrls">' + ks.map(function (k) { return '<button type="button" class="btn sm' + (k === cur ? " pri" : "") + '" data-k="' + esc(k) + '">' + esc(k) + '</button>'; }).join("") + '</div><div class="pl" style="display:grid;gap:5px;margin:10px 0"></div><div class="read"></div>';
    var box = el.querySelector(".pl"), rd = el.querySelector(".read");
    function draw() {
      var m = MODELOS[cur];
      box.innerHTML = CAMADAS.map(function (c, i) { var voce = m[i]; return '<div style="display:flex;justify-content:space-between;gap:10px;padding:9px 14px;border-radius:10px;border:2px solid var(--' + (voce ? "c1" : "c0") + ');background:color-mix(in srgb,var(--' + (voce ? "c1" : "c0") + ') 12%,var(--card));transition:.3s"><b>' + c + '</b><span style="font-weight:700;color:var(--' + (voce ? "c1" : "c0") + ')">' + (voce ? "você" : "o provedor") + '</span></div>'; }).join("");
      var n = m.reduce(function (a, b) { return a + b; }, 0);
      rd.innerHTML = "<b>" + esc(cur) + "</b>: você cuida de <b>" + n + "</b> das 7 camadas. " + ({ 0: "No SaaS você só <b>usa</b> o software: nenhum controle sobre o servidor, e menos trabalho de TI.", 2: "No PaaS o foco é <b>implementar e gerir a aplicação</b>; a nuvem gerencia o sistema operacional.", 4: "No IaaS você controla o sistema operacional e tudo acima: mais controle, <b>mais responsabilidade</b>.", 7: "No modelo local, <b>tudo é seu</b>: do prédio ao software." }[n] || "");
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-k]"); if (!b) return; cur = b.getAttribute("data-k"); el.querySelectorAll("button[data-k]").forEach(function (x) { x.classList.toggle("pri", x === b); }); draw(); });
    draw();
  };

  /* ---- cap 1: servidor fixo x pagar pelo uso (ilustrativo) ---- */
  E.demos.custo = function (el) {
    el.innerHTML = '<h4>Quando pagar pelo uso compensa?</h4><div class="ctrls"><label>uso médio do servidor <input type="range" id="cu" min="5" max="100" value="25"><output id="cuo">25%</output></label><label>preço da nuvem por hora de uso, relativo ao servidor próprio <input type="range" id="cf" min="100" max="400" value="200" step="10"><output id="cfo">2,0x</output></label></div>' +
      '<div class="bars"><div class="bar"><div>Servidor próprio (custo fixo)</div><div class="tr"><div class="fl" style="transition:width .3s"></div></div><div class="v"></div></div><div class="bar"><div>Nuvem (paga o que usa)</div><div class="tr"><div class="fl" style="transition:width .3s"></div></div><div class="v"></div></div></div><div class="read"></div>' +
      '<p class="muted" style="font-size:.85rem;margin:8px 0 0">Modelo <b>ilustrativo</b>, em unidades relativas: o servidor próprio custa 100 por mês independente do uso (compra, energia, espaço, pessoal diluídos). Não são preços reais; servem para mostrar a lógica do TCO.</p>';
    var cu = el.querySelector("#cu"), cf = el.querySelector("#cf"), bars = el.querySelectorAll(".bar"), rd = el.querySelector(".read");
    function go() {
      var u = +cu.value / 100, f = +cf.value / 100; el.querySelector("#cuo").textContent = Math.round(u * 100) + "%"; el.querySelector("#cfo").textContent = f.toFixed(1).replace(".", ",") + "x";
      var local = 100, nuvem = 100 * u * f, max = Math.max(local, nuvem, 100);
      bars[0].querySelector(".fl").style.width = local / max * 100 + "%"; bars[0].querySelector(".v").textContent = Math.round(local);
      bars[1].querySelector(".fl").style.width = Math.min(100, nuvem / max * 100) + "%"; bars[1].querySelector(".v").textContent = Math.round(nuvem);
      var eq = 100 / f;
      rd.innerHTML = nuvem < local ? "Com <b>" + Math.round(u * 100) + "%</b> de uso, a nuvem sai mais barata (<b>" + Math.round(nuvem) + "</b> contra 100): você não paga pela capacidade ociosa." : "Com uso alto e constante, o servidor próprio pode sair mais barato (a nuvem custaria <b>" + Math.round(nuvem) + "</b>). O ponto de equilíbrio está perto de <b>" + Math.round(eq) + "%</b> de uso com esse preço relativo.";
      rd.innerHTML += " A nuvem vale mais pela <b>flexibilidade</b> (escalar para cima e para baixo em minutos) e pelo <b>tempo de lançamento</b> do que por ser sempre mais barata.";
    }
    cu.addEventListener("input", go); cf.addEventListener("input", go); go();
  };

  /* ---- cap 2: avaliador de políticas IAM ---- */
  var POLS = {
    ec2ro: { nome: "EC2ReadOnly (grupo Suporte)", st: [{ e: "Allow", a: ["ec2:Describe*"], r: "*" }] },
    s3ro: { nome: "S3ReadOnly (grupo Suporte)", st: [{ e: "Allow", a: ["s3:GetObject", "s3:ListBucket"], r: "*" }] },
    ec2adm: { nome: "EC2Admin (grupo Admin)", st: [{ e: "Allow", a: ["ec2:*"], r: "*" }] },
    nodel: { nome: "NegaTerminar (Deny explícito)", st: [{ e: "Deny", a: ["ec2:TerminateInstances"], r: "*" }] }
  };
  function casa(pad, act) { var re = new RegExp("^" + pad.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*") + "$"); return re.test(act); }
  E.demos.iam = function (el) {
    var acts = ["ec2:DescribeInstances", "ec2:StartInstances", "ec2:TerminateInstances", "s3:GetObject", "s3:DeleteObject", "rds:DeleteDBInstance"];
    el.innerHTML = '<h4>Esta pessoa pode fazer isto?</h4><div class="ctrls"><span class="muted">Políticas anexadas:</span>' + Object.keys(POLS).map(function (k) { return '<label><input type="checkbox" data-p="' + k + '"' + (k === "ec2ro" ? " checked" : "") + '> ' + POLS[k].nome + '</label>'; }).join("") + '</div>' +
      '<div class="ctrls"><label>ação <select id="ia">' + acts.map(function (a) { return '<option>' + a + '</option>'; }).join("") + '</select></label></div><div class="tablewrap"><table class="it"></table></div><div class="read"></div>';
    var sel = el.querySelector("#ia"), it = el.querySelector(".it"), rd = el.querySelector(".read");
    function go() {
      var act = sel.value, on = [].slice.call(el.querySelectorAll("input[data-p]")).filter(function (c) { return c.checked; }).map(function (c) { return c.getAttribute("data-p"); });
      var allow = false, deny = false, rows = "";
      on.forEach(function (k) { POLS[k].st.forEach(function (s) { var m = s.a.some(function (p) { return casa(p, act); }); if (m && s.e === "Allow") allow = true; if (m && s.e === "Deny") deny = true; rows += '<tr><td>' + esc(POLS[k].nome) + '</td><td><code>' + s.e + '</code></td><td><code>' + esc(s.a.join(", ")) + '</code></td><td>' + (m ? "<b>casa</b>" : '<span class="muted">não casa</span>') + '</td></tr>'; }); });
      it.innerHTML = '<tr><th>Política</th><th>Efeito</th><th>Ação</th><th>Casa com <code>' + esc(act) + '</code>?</th></tr>' + (rows || '<tr><td colspan="4" class="muted">Nenhuma política anexada.</td></tr>');
      var r = deny ? ["NEGADO", "red", "Há um <b>Deny explícito</b> que casa. O Deny <b>sempre vence</b> qualquer Allow."] : allow ? ["PERMITIDO", "green", "Pelo menos um <b>Allow</b> casa, e nenhum Deny."] : ["NEGADO", "red", "Nada permite a ação: é o <b>Deny implícito</b>. Toda conta nasce sem permissão nenhuma (privilégio mínimo)."];
      rd.innerHTML = '<b style="color:var(--' + r[1] + ');font-size:1.1rem">' + r[0] + "</b>. " + r[2];
    }
    el.addEventListener("change", go); go();
  };

  /* ---- cap 3: decodificador de nome de instância ---- */
  E.demos.instancia = function (el) {
    var FAM = { t: "propósito geral, 'burstable' (desempenho que estoura quando precisa, custo-base menor)", m: "propósito geral (cerca de 4 GB de RAM por vCPU)", c: "otimizada para processamento (mais vCPU por GB de memória)", r: "otimizada para memória", x: "otimizada para memória (muito grande)", i: "otimizada para armazenamento (E/S de disco alta)", d: "otimizada para armazenamento (muito denso)", p: "computação acelerada (GPU, para ML)", g: "computação acelerada (GPU, gráficos e ML)" };
    var ATR = { g: "processador Graviton (ARM, da própria AWS)", a: "processador AMD", i: "processador Intel", d: "disco local NVMe SSD", n: "rede aprimorada (mais banda)", e: "mais memória ou armazenamento extra", b: "otimizada para EBS" };
    var TAM = { nano: 1, micro: 1, small: 1, medium: 2, large: 2, xlarge: 4, "2xlarge": 8, "4xlarge": 16, "8xlarge": 32 };
    el.innerHTML = '<h4>Leia o nome de uma instância</h4><div class="ctrls"><label>tipo <input type="text" id="in" value="c6gd.large" style="width:170px;font-family:var(--f-mono)"></label>' + ["t2.micro", "m5.xlarge", "c6gd.8xlarge", "r5.large", "p3.2xlarge"].map(function (x) { return '<button class="btn sm" type="button" data-x="' + x + '">' + x + '</button>'; }).join("") + '</div><div class="tablewrap"><table class="itab"></table></div><div class="read"></div>';
    var inp = el.querySelector("#in"), tb = el.querySelector(".itab"), rd = el.querySelector(".read");
    function go() {
      var m = /^([a-z]+)(\d+)([a-z]*)\.([a-z0-9]+)$/.exec(inp.value.trim().toLowerCase());
      if (!m) { tb.innerHTML = ""; rd.textContent = "Use o padrão família + geração + atributos, ponto, tamanho (por exemplo, m5.large)."; return; }
      var fam = m[1], ger = m[2], atr = m[3], tam = m[4];
      tb.innerHTML = '<tr><th>Parte</th><th>Valor</th><th>Significa</th></tr><tr><td>Família</td><td><code>' + fam + '</code></td><td>' + (fam.length === 1 && FAM[fam] ? FAM[fam] : "família não listada aqui (consulte a documentação de tipos de instância)") + '</td></tr><tr><td>Geração</td><td><code>' + ger + '</code></td><td>quanto maior, mais novo o hardware</td></tr>' +
        '<tr><td>Atributos</td><td><code>' + (atr || "-") + '</code></td><td>' + (atr ? atr.split("").map(function (c) { return (ATR[c] || c); }).join("; ") : "nenhum extra") + '</td></tr><tr><td>Tamanho</td><td><code>' + tam + '</code></td><td>' + (TAM[tam] ? "cerca de " + TAM[tam] + " vCPU" + (TAM[tam] > 1 ? "s" : "") + " (varia por família)" : "tamanho personalizado") + '</td></tr>';
      rd.innerHTML = "<code>t2.micro</code> tem 1 vCPU e 1 GB de memória é um tipo pequeno que costuma aparecer em laboratórios (o tipo aceito no nível gratuito muda: confira o vigente). <b>vCPU</b> é um núcleo de processamento <i>virtual</i>, e não necessariamente um núcleo físico dedicado.";
    }
    el.addEventListener("click", function (e) { var b = e.target.closest("button[data-x]"); if (b) { inp.value = b.getAttribute("data-x"); go(); } });
    inp.addEventListener("input", go); go();
  };

  /* ---- cap 4: S3, duas camadas ---- */
  E.demos.s3acesso = function (el) {
    el.innerHTML = '<h4>Por que o site dá "AccessDenied"?</h4><div class="grid2"><div class="card" style="margin:0"><b>Camada 1: Block Public Access</b><br><label><input type="checkbox" id="bp" checked> bloqueio ativado (padrão)</label></div><div class="card" style="margin:0"><b>Camada 2: política do bucket</b><br><label><input type="checkbox" id="pb"> política com <code>s3:GetObject</code> para <code>"*"</code></label></div></div><div class="read" style="margin-top:10px"></div><pre class="jq" style="margin:8px 0;white-space:pre-wrap"></pre>';
    var bp = el.querySelector("#bp"), pb = el.querySelector("#pb"), rd = el.querySelector(".read"), jq = el.querySelector(".jq");
    function go() {
      var ok = !bp.checked && pb.checked;
      rd.innerHTML = ok ? '<b style="color:var(--green)">200 OK</b>: o site abre. As duas camadas estão certas: a trava foi removida <b>e</b> a política autoriza a leitura pública.' : '<b style="color:var(--red)">403 AccessDenied</b>. ' + (bp.checked && pb.checked ? "A política existe, mas o <b>bloqueio de acesso público</b> a neutraliza. Desmarque a camada 1." : (!bp.checked && !pb.checked ? "Você destravou a porta, mas ninguém <b>autorizou</b> a leitura: falta a política do bucket. <i>Desbloquear não concede acesso.</i>" : "A trava continua ativa e não há política: tudo privado, como deve ser por padrão."));
      jq.textContent = "GET https://meu-bucket.s3.us-east-1.amazonaws.com/index.html\n-> " + (ok ? "200 OK" : "403 Forbidden (AccessDenied)");
    }
    el.addEventListener("change", go); go();
  };

  /* ---- cap 5: RDS, duas camadas ---- */
  E.demos.rdsacesso = function (el) {
    el.innerHTML = '<h4>Consigo conectar no banco?</h4><div class="ctrls"><label><input type="checkbox" id="rp"> acesso público: Sim</label><label>regra de entrada na porta 3306 <select id="rs"><option value="none">nenhuma</option><option value="any">qualquer lugar (0.0.0.0/0)</option><option value="me">só o meu IP</option></select></label></div><div class="read"></div><pre class="jq" style="margin:8px 0;white-space:pre-wrap"></pre>';
    var rp = el.querySelector("#rp"), rs = el.querySelector("#rs"), rd = el.querySelector(".read"), jq = el.querySelector(".jq");
    function go() {
      var pub = rp.checked, r = rs.value, ok = pub && r !== "none";
      var msg = ok ? '<b style="color:var(--green)">Conectou.</b> O banco tem endereço alcançável (acesso público) <b>e</b> o Security Group deixou a porta passar.' : (!pub ? '<b style="color:var(--red)">Não conecta.</b> Sem acesso público, o banco só é alcançável de dentro da VPC: do seu computador não há caminho.' : '<b style="color:var(--red)">Timeout.</b> O endereço existe, mas o Security Group (o firewall) não tem regra de entrada na 3306: o pacote é descartado em silêncio.');
      if (ok && r === "any") msg += ' <b style="color:var(--amber)">Atenção:</b> <code>0.0.0.0/0</code> expõe o banco à internet inteira. Qualquer robô pode tentar adivinhar a senha. Serve só para laboratório.';
      if (ok && r === "me") msg += " Esta é a prática melhor: só o seu IP entra.";
      rd.innerHTML = msg; jq.textContent = "mysql -h db-instancia-xx.region.rds.amazonaws.com -P 3306 -u admin -p\n-> " + (ok ? "Welcome to the MySQL monitor" : (!pub ? "ERROR 2003: Can't connect (sem rota)" : "ERROR 2003: Can't connect (timeout)"));
    }
    el.addEventListener("change", go); go();
  };

  /* ---- cap 6: S3 -> Lambda -> RDS, com um MySQL (SQLite) de verdade ---- */
  E.demos.lambdalab = function (el) {
    el.innerHTML = '<h4>Suba o CSV e veja a função inserir as linhas</h4><textarea id="lc" spellcheck="false" style="width:100%;min-height:120px;font:.85rem var(--f-mono);background:#161b27;color:#dfe6f7;border:1px solid #2a3350;border-radius:10px;padding:12px">idProjeto;idFuncionario;horas\n1;1;20\n2;1;20\n2;2;30\n2;3;40\n3;4;40</textarea>' +
      '<div class="ctrls"><button class="btn sm pri" type="button" id="lu">⬆ Subir o CSV no bucket</button><button class="btn sm" type="button" id="lr">Limpar a tabela</button></div><div class="pipe" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0"></div><pre class="jq" style="margin:6px 0;white-space:pre-wrap;min-height:5em"></pre><div class="sqlres"></div><div class="read"></div>';
    var lc = el.querySelector("#lc"), pipe = el.querySelector(".pipe"), jq = el.querySelector(".jq"), res = el.querySelector(".sqlres"), rd = el.querySelector(".read"), db = null, SQL = null, busy = false;
    function mk() { db = new SQL.Database(); db.run("CREATE TABLE projetoFuncionario (idProjeto INT NOT NULL, idFuncionario INT NOT NULL, horas INT, PRIMARY KEY (idProjeto, idFuncionario));"); }
    function stage(n, erro) { var N = ["S3", "gatilho", "Lambda", "RDS"]; pipe.innerHTML = N.map(function (x, i) { return '<span style="padding:6px 14px;border-radius:10px;border:2px solid var(--' + (i === n ? (erro ? "red" : "green") : "line") + ');background:' + (i === n ? "var(--hl-y)" : "var(--card)") + ';font-weight:700;transition:.3s">' + x + '</span>' + (i < 3 ? "<span>→</span>" : ""); }).join(""); }
    function tabela() { var r = db.exec("SELECT * FROM projetoFuncionario ORDER BY idProjeto, idFuncionario"); res.innerHTML = r.length ? '<table><tr>' + r[0].columns.map(function (c) { return '<th>' + c + '</th>'; }).join("") + '</tr>' + r[0].values.map(function (v) { return '<tr>' + v.map(function (x) { return '<td>' + esc(x) + '</td>'; }).join("") + '</tr>'; }).join("") + '</table><p class="muted" style="margin:4px 0">' + r[0].values.length + ' linhas na tabela</p>' : '<p class="muted">A tabela está vazia.</p>'; }
    function sobe() {
      if (!SQL || busy) return; busy = true; var linhas = lc.value.split("\n"), log = ["START RequestId..."], falhou = null;
      stage(0); log.push("S3: objeto horasalocadas.csv criado -> evento ObjectCreated");
      setTimeout(function () { stage(1); log.push("Gatilho: aciona fn-inserir-horas-alocadas"); jq.textContent = log.join("\n");
        setTimeout(function () { stage(2); log.push("Lambda: lê o CSV, " + (linhas.length - 1) + " linha(s) de dados (pula o cabeçalho)"); jq.textContent = log.join("\n");
          setTimeout(function () {
            try { db.run("BEGIN"); linhas.slice(1).forEach(function (l) { if (!l.trim()) return; var p = l.split(";"); db.run("INSERT INTO projetoFuncionario (idProjeto, idFuncionario, horas) VALUES (?, ?, ?)", [p[0], p[1], p[2]]); }); db.run("COMMIT"); log.push("commit", "Inclusão realizada com sucesso!"); stage(3); }
            catch (e) { falhou = e.message; try { db.run("ROLLBACK"); } catch (x) { } log.push("ERRO: " + falhou, "rollback (nenhuma linha desta execução ficou)"); stage(3, true); }
            var n = db.exec("SELECT COUNT(*) FROM projetoFuncionario")[0].values[0][0]; log.push("Total de linhas no banco: " + n, "END RequestId..."); jq.textContent = log.join("\n");
            rd.innerHTML = falhou ? "<b style='color:var(--red)'>Falhou:</b> " + (/UNIQUE|PRIMARY/i.test(falhou) ? "as linhas repetidas violam a <b>chave primária</b> (idProjeto, idFuncionario)." : "<code>" + falhou.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</code>.") + " O <code>rollback</code> desfez a execução inteira, e o erro apareceria no <b>CloudWatch</b>. Era a pegadinha de subir o mesmo CSV duas vezes." : "A função rodou sem erro. Suba o <b>mesmo</b> CSV de novo para ver a chave primária barrar.";
            tabela(); busy = false;
          }, E.reduce ? 10 : 700); }, E.reduce ? 10 : 700); }, E.reduce ? 10 : 600);
    }
    el.querySelector("#lu").addEventListener("click", sobe); el.querySelector("#lr").addEventListener("click", function () { if (!SQL) return; mk(); tabela(); jq.textContent = ""; stage(-1); rd.textContent = "Tabela limpa."; });
    stage(-1); rd.textContent = "Carregando o banco do navegador...";
    E.loadSql().then(function (S) { SQL = S; mk(); tabela(); rd.textContent = "Pronto. Clique em subir o CSV."; }, function (err) { rd.textContent = err.message; });
  };
})();
