/* Núcleo das demos de Deploy e Hospedagem. Sem DOM nas funções de lógica: dá para conferir em node.
   Tudo é simulado e com dados fictícios (domínio meusite.example, faixas de IP reservadas para documentação). Nada sai da página. */
(function () {
  var E = window.Estudo = window.Estudo || { demos: {} };
  E.demos = E.demos || {};
  var DP = E.dp = {};

  DP.esc = function (t) { return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };

  /* ====================== HTTP ====================== */
  var STATUS = { 200: "OK", 201: "Created", 204: "No Content", 301: "Moved Permanently", 304: "Not Modified", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable", 415: "Unsupported Media Type", 500: "Internal Server Error", 502: "Bad Gateway" };
  DP.STATUS = STATUS;
  DP.METODOS = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"];
  DP.HOST = "meusite.example";
  var TOKEN_DE_TESTE = "Bearer teste123"; /* valor inventado para a demo */

  /* tamanho em bytes UTF-8 (é o que o Content-Length conta; acento ocupa 2 bytes) */
  DP.bytes = function (t) {
    t = String(t == null ? "" : t); var n = 0;
    for (var i = 0; i < t.length; i++) {
      var c = t.charCodeAt(i);
      if (c < 0x80) n += 1; else if (c < 0x800) n += 2;
      else if (c >= 0xD800 && c <= 0xDBFF) { n += 4; i++; } else n += 3;
    }
    return n;
  };

  /* Host: sem diferença de maiúscula, com porta opcional (meusite.example:8080) */
  DP.normHost = function (h) {
    h = String(h == null ? "" : h).trim().toLowerCase().replace(/\.$/, "");
    return h.replace(/:\d{1,5}$/, "");
  };

  DP.parseCab = function (txt) {
    var mapa = {}, ignoradas = [];
    String(txt == null ? "" : txt).split(/\r?\n/).forEach(function (l) {
      if (!l.trim()) return;
      var i = l.indexOf(":");
      if (i < 1 || /\s/.test(l.slice(0, i).trim())) { ignoradas.push(l.trim()); return; }
      mapa[l.slice(0, i).trim().toLowerCase()] = l.slice(i + 1).trim();
    });
    return { mapa: mapa, ignoradas: ignoradas };
  };

  /* Rotas do site de mentira: [metodos permitidos, função que responde] */
  var ROTAS = {
    "/": { m: ["GET", "HEAD"], f: function () { return { s: 200, tipo: "text/html; charset=utf-8", corpo: "<h1>Meu site</h1>" }; } },
    "/sobre.html": { m: ["GET", "HEAD"], f: function () { return { s: 200, tipo: "text/html; charset=utf-8", corpo: "<h1>Sobre</h1>" }; } },
    "/antigo": { m: ["GET", "HEAD"], f: function () { return { s: 301, extra: [["Location", "/sobre.html"]], corpo: "" }; } },
    "/api/dados": { m: ["GET", "HEAD"], f: function (c) {
      var ac = c.mapa["accept"];
      if (ac && !/json|\*\/\*/.test(ac)) return { s: 406, tipo: "text/plain", corpo: "Esta rota só entrega JSON (Accept: application/json)." };
      return { s: 200, tipo: "application/json", corpo: '{"visitas": 42}' };
    } },
    "/contato": { m: ["POST", "OPTIONS"], f: function (c, corpo) {
      if (!/application\/json/.test(c.mapa["content-type"] || "")) return { s: 415, tipo: "text/plain", corpo: "Envie Content-Type: application/json." };
      if (!String(corpo || "").trim()) return { s: 400, tipo: "text/plain", corpo: "Corpo vazio." };
      try { JSON.parse(corpo); } catch (e) { return { s: 400, tipo: "text/plain", corpo: "JSON inválido." }; }
      return { s: 201, tipo: "application/json", extra: [["Location", "/contato/7"]], corpo: '{"id": 7}' };
    } },
    "/admin": { m: ["GET", "HEAD"], f: function (c) {
      var a = c.mapa["authorization"];
      if (!a) return { s: 401, extra: [["WWW-Authenticate", "Bearer"]], tipo: "text/plain", corpo: "Faça login." };
      if (a !== TOKEN_DE_TESTE) return { s: 403, tipo: "text/plain", corpo: "Token sem permissão." };
      return { s: 200, tipo: "text/html; charset=utf-8", corpo: "<h1>Painel</h1>" };
    } },
    "/quebrado": { m: ["GET", "HEAD"], f: function () { return { s: 500, tipo: "text/plain", corpo: "Erro no código do servidor." }; } }
  };
  DP.TOKEN = TOKEN_DE_TESTE;

  /* req: {metodo, caminho, host, cab (texto), corpo}. Nunca lança erro: entrada ruim vira resposta 400. */
  DP.http = function (req) {
    req = req && typeof req === "object" ? req : {};
    var metodo = typeof req.metodo === "string" ? req.metodo.trim().toUpperCase() : "";
    var caminho = typeof req.caminho === "string" ? req.caminho.trim() : "";
    var host = typeof req.host === "string" ? req.host.trim() : "";
    var corpoReq = typeof req.corpo === "string" ? req.corpo : "";
    var c = DP.parseCab(req.cab);
    var data = "Fri, 06 Nov 2026 12:00:00 GMT";
    function resp(s, tipo, extra, corpo, len, dica) {
      var cab = [["Date", data], ["Server", "servidor-de-mentira"]];
      if (tipo) cab.push(["Content-Type", tipo]);
      cab.push(["Content-Length", String(len == null ? DP.bytes(corpo || "") : len)]);
      (extra || []).forEach(function (p) { cab.push(p); });
      return { status: s, texto: STATUS[s] || "", cab: cab, corpo: corpo || "", dica: dica || "", ignoradas: c.ignoradas, linhaReq: (metodo || "?") + " " + (caminho || "/") + " HTTP/1.1" };
    }
    if (!host) return resp(400, "text/plain", [], "Falta o cabeçalho Host.", null, "HTTP/1.1 exige o cabeçalho Host: um mesmo servidor pode atender vários sites, e é o Host que diz qual.");
    if (DP.normHost(host) !== DP.HOST) return resp(404, "text/plain", [], "Site desconhecido.", null, "O servidor de mentira só atende o Host " + DP.HOST + ". Num servidor real com vários sites, o Host errado cai no site padrão ou dá erro.");
    if (DP.METODOS.indexOf(metodo) < 0) return resp(400, "text/plain", [], "Método inválido.", null, "Escolha um método da lista: " + DP.METODOS.join(", ") + ".");
    if (!caminho) caminho = "/";
    if (caminho.charAt(0) !== "/") caminho = "/" + caminho;
    var semQuery = caminho.split("?")[0];
    var rota = ROTAS[semQuery];
    if (!rota) return resp(404, "text/plain", [], "Não achei " + semQuery, null, "Nenhum arquivo ou rota com esse caminho. Em servidor Linux, maiúscula e minúscula contam como nomes diferentes.");
    if (metodo === "OPTIONS") return resp(204, null, [["Allow", rota.m.join(", ")]], "", 0, "OPTIONS pergunta o que a rota aceita. Resposta sem corpo.");
    if (rota.m.indexOf(metodo) < 0) return resp(405, "text/plain", [["Allow", rota.m.join(", ")]], "Método não permitido.", null, "A rota existe, mas não aceita " + metodo + ". O cabeçalho Allow lista o que ela aceita.");
    var r = rota.f(c, corpoReq);
    var corpo = metodo === "HEAD" ? "" : r.corpo;
    var dicas = { 200: "Deu certo e o corpo veio junto.", 201: "Algo foi criado. O Location diz onde.", 301: "O recurso mudou de lugar. O navegador segue o Location sozinho.", 400: "O servidor não entendeu o pedido.", 406: "A rota não tem uma versão no formato que o Accept pediu.", 401: "Falta identificação (login ou token).", 403: "Você se identificou, mas não tem permissão.", 415: "O corpo veio num formato que a rota não aceita.", 500: "O erro é do servidor (código ou configuração), não do pedido." };
    return resp(r.s, r.tipo, r.extra, corpo, r.len != null ? r.len : DP.bytes(r.corpo), (metodo === "HEAD" ? "HEAD devolve só os cabeçalhos. " : "") + (dicas[r.s] || ""));
  };
  DP.classe = function (s) { return s >= 500 ? "erro do servidor" : s >= 400 ? "erro do cliente" : s >= 300 ? "redirecionamento" : s >= 200 ? "sucesso" : "informação"; };

  /* ====================== DNS ====================== */
  /* Zonas fictícias. IPs da faixa de documentação (RFC 5737). */
  var ZONAS = {
    "meusite.example": { servidor: "ns1.meusite.example", regs: {
      "meusite.example": { t: "A", v: "203.0.113.10", ttl: 300 },
      "www.meusite.example": { t: "CNAME", v: "meusite.example", ttl: 3600 },
      "blog.meusite.example": { t: "CNAME", v: "meusite-blog.hospedagem.example", ttl: 3600 }
    } },
    "hospedagem.example": { servidor: "ns1.hospedagem.example", regs: {
      "meusite-blog.hospedagem.example": { t: "A", v: "198.51.100.7", ttl: 60 }
    } }
  };
  DP.NOMES_DNS = ["meusite.example", "www.meusite.example", "blog.meusite.example", "loja.meusite.example", "outro.invalido"];

  DP.validaNome = function (n) {
    if (typeof n !== "string") return "Digite um nome.";
    n = n.trim().replace(/\.$/, "").toLowerCase();
    if (!n) return "Digite um nome.";
    if (n.length > 253) return "Nome longo demais (o limite é 253 caracteres).";
    var ls = n.split(".");
    if (ls.length < 2) return "Um nome de site precisa de pelo menos dois pedaços, como meusite.example.";
    for (var i = 0; i < ls.length; i++) {
      if (!ls[i]) return "Tem dois pontos seguidos ou um ponto no começo.";
      if (ls[i].length > 63) return "Cada pedaço do nome tem no máximo 63 caracteres.";
      if (!/^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/.test(ls[i])) return "Use só letras sem acento, números e hífen (sem hífen no começo ou no fim de um pedaço).";
    }
    return "";
  };

  function achaZona(nome) {
    var best = null;
    Object.keys(ZONAS).forEach(function (z) { if (nome === z || nome.slice(-(z.length + 1)) === "." + z) { if (!best || z.length > best.length) best = z; } });
    return best;
  }

  /* cache: objeto {nome: segundoEmQueExpira}. agora: segundos desde o início da demo.
     Devolve {erro?, passos:[{de,para,pergunta,resposta}], respostaFinal, ttl, doCache, cache} */
  DP.resolve = function (nome, agora, cache) {
    var erro = DP.validaNome(nome);
    cache = cache && typeof cache === "object" ? cache : {};
    agora = isFinite(agora) ? +agora : 0;
    if (erro) return { erro: erro, passos: [], cache: cache };
    nome = nome.trim().replace(/\.$/, "").toLowerCase();
    var passos = [];
    if (cache[nome] && cache[nome].expira > agora) {
      var c = cache[nome];
      passos.push({ de: "Navegador", para: "Resolvedor", pergunta: "Qual o IP de " + nome + "?", resposta: "" });
      passos.push({ de: "Resolvedor", para: "Navegador", pergunta: "", resposta: "Tenho na memória: " + c.ip + " (ainda vale por " + Math.round(c.expira - agora) + " s). Não precisei perguntar a ninguém." });
      return { passos: passos, respostaFinal: c.ip, ttl: c.ttl, doCache: true, cache: cache, restante: Math.round(c.expira - agora) };
    }
    passos.push({ de: "Navegador", para: "Resolvedor", pergunta: "Qual o IP de " + nome + "?", resposta: "" });
    var tld = nome.split(".").pop();
    passos.push({ de: "Resolvedor", para: "Servidor raiz", pergunta: "Quem cuida de ." + tld + "?", resposta: tld === "example" ? "Pergunte aos servidores de .example." : "Não existe o domínio de topo ." + tld + " (NXDOMAIN)." });
    if (tld !== "example") return { erro: "NXDOMAIN: o servidor raiz não conhece ." + tld + ".", passos: passos, cache: cache, nx: true };
    var zona = achaZona(nome);
    passos.push({ de: "Resolvedor", para: "Servidor do TLD .example", pergunta: "Quem cuida de " + (zona || nome.split(".").slice(-2).join(".")) + "?", resposta: zona ? "Pergunte a " + ZONAS[zona].servidor + "." : "Esse domínio não está registrado (NXDOMAIN)." });
    if (!zona) return { erro: "NXDOMAIN: o domínio não está registrado no .example.", passos: passos, cache: cache, nx: true };
    var atual = nome, ttlMin = Infinity, saltos = 0, ip = "";
    var zonaAtual = zona;
    for (;;) {
      var reg = ZONAS[zonaAtual].regs[atual];
      passos.push({ de: "Resolvedor", para: ZONAS[zonaAtual].servidor + " (autoritativo)", pergunta: "Qual o registro de " + atual + "?", resposta: reg ? (reg.t + " " + reg.v + " (TTL " + reg.ttl + " s)") : "Esse nome não existe nesta zona (NXDOMAIN)." });
      if (!reg) return { erro: "NXDOMAIN: o servidor autoritativo diz que " + atual + " não existe.", passos: passos, cache: cache, nx: true };
      ttlMin = Math.min(ttlMin, reg.ttl);
      if (reg.t === "A") { ip = reg.v; break; }
      if (++saltos > 5) return { erro: "Cadeia de CNAME longa demais.", passos: passos, cache: cache };
      atual = reg.v;
      var z2 = achaZona(atual);
      if (!z2) return { erro: "O CNAME aponta para um nome que não existe.", passos: passos, cache: cache };
      if (z2 !== zonaAtual) {
        passos.push({ de: "Resolvedor", para: "Servidor do TLD .example", pergunta: "Quem cuida de " + z2 + "?", resposta: "Pergunte a " + ZONAS[z2].servidor + "." });
        zonaAtual = z2;
      }
    }
    passos.push({ de: "Resolvedor", para: "Navegador", pergunta: "", resposta: nome + " = " + ip + ". Guardei por " + ttlMin + " s." });
    var novo = {}; Object.keys(cache).forEach(function (k) { novo[k] = cache[k]; });
    novo[nome] = { ip: ip, ttl: ttlMin, expira: agora + ttlMin };
    return { passos: passos, respostaFinal: ip, ttl: ttlMin, doCache: false, cache: novo };
  };

  /* ====================== Certificado ====================== */
  DP.nomeCasa = function (host, san) {
    host = String(host || "").trim().toLowerCase().replace(/\.$/, ""); san = String(san || "").trim().toLowerCase().replace(/\.$/, "");
    if (!host || !san || host.indexOf("*") >= 0) return false;
    if (san === host) return true;
    if (san.indexOf("*.") === 0) {
      var resto = san.slice(2), i = host.indexOf(".");
      if (resto.indexOf("*") >= 0 || resto.split(".").length < 2 || resto.split(".").some(function (x) { return !x; })) return false; /* curinga de TLD (*.com, *.test) não vale */
      return i > 0 && host.slice(i + 1) === resto; /* o curinga cobre UM nível só */
    }
    return false;
  };
  /* valida o "endereço aberto": só o nome do site, sem https://, porta, caminho ou * */
  DP.validaHost = function (h) {
    h = String(h == null ? "" : h).trim();
    if (!h) return "Digite o endereço que você abriu no navegador.";
    if (/^[a-z][a-z0-9+.-]*:\/\//i.test(h)) return "Digite só o nome do site, sem https:// (ex.: www.exemplo.test).";
    if (/[\/:?#]/.test(h)) return "Digite só o nome do site, sem porta (:443) nem caminho.";
    if (h.indexOf("*") >= 0) return "O endereço aberto é um nome de verdade; o * só vale dentro do certificado.";
    return DP.validaNome(h);
  };
  function dataOk(s) { return typeof s === "string" && /^\d{4}-\d{2}-\d{2}$/.test(s) && !isNaN(Date.parse(s + "T00:00:00Z")); }
  /* c: {host, sans:[...], de, ate, hoje (AAAA-MM-DD), confiavel:boolean} */
  DP.certVeredito = function (c) {
    c = c && typeof c === "object" ? c : {};
    var sans = Array.isArray(c.sans) ? c.sans : String(c.sans || "").split(/[,\s]+/).filter(Boolean);
    var eh = DP.validaHost(c.host);
    if (eh) return { erro: eh };
    if (!sans.length) return { erro: "Informe pelo menos um nome que o certificado cobre." };
    if (!dataOk(c.de) || !dataOk(c.ate) || !dataOk(c.hoje)) return { erro: "Use datas completas (AAAA-MM-DD) nos três campos." };
    if (c.ate < c.de) return { erro: "A data de fim vem antes da de início." };
    var nome = sans.some(function (s) { return DP.nomeCasa(c.host, s); });
    var valido = c.hoje >= c.de && c.hoje <= c.ate;
    var conf = !!c.confiavel;
    var testes = [
      { nome: "O nome bate?", ok: nome, txt: nome ? "O endereço " + c.host + " está coberto pelo certificado." : "O certificado não cobre " + c.host + ". Cadeado indevido: o navegador avisa." },
      { nome: "Está dentro da validade?", ok: valido, txt: valido ? "Hoje está entre " + c.de + " e " + c.ate + "." : (c.hoje < c.de ? "Ainda não começou a valer." : "Expirou em " + c.ate + ".") },
      { nome: "A autoridade é confiável?", ok: conf, txt: conf ? "A cadeia chega a uma autoridade que o navegador já conhece." : "A cadeia não chega a uma autoridade conhecida (por exemplo, certificado autoassinado)." }
    ];
    var falhas = testes.filter(function (t) { return !t.ok; }).length;
    return { testes: testes, ok: falhas === 0, falhas: falhas };
  };

  /* ====================== Onde hospedar ====================== */
  /* r: {conteudo: estatico|codigo|banco, orcamento: zero|baixo|folga, controle: nenhum|total, admin: sim|nao, picos: nao|sim} */
  DP.recomenda = function (r) {
    r = r && typeof r === "object" ? r : {};
    var v = function (k, ok, def) { return ok.indexOf(r[k]) >= 0 ? r[k] : def; };
    var conteudo = v("conteudo", ["estatico", "codigo", "banco"], "estatico");
    var orc = v("orcamento", ["zero", "baixo", "folga"], "zero");
    var ctrl = v("controle", ["nenhum", "total"], "nenhum");
    var admin = v("admin", ["sim", "nao"], "nao");
    var picos = v("picos", ["nao", "sim"], "nao");
    var out = { titulo: "", modelo: "", motivos: [], cuidados: [] };
    if (conteudo === "estatico") {
      if (ctrl === "total" && admin === "sim") {
        out.titulo = "VPS com nginx (ou hospedagem estática, se o controle não for mesmo necessário)";
        out.modelo = "IaaS (você administra o sistema)";
        out.motivos.push("Site estático é só arquivo: qualquer servidor web entrega.", "Você pediu controle total e sabe administrar, então o VPS faz sentido, principalmente para aprender.");
        out.cuidados.push("Você passa a cuidar de atualizações, firewall e certificado.");
      } else {
        out.titulo = "Hospedagem estática (GitHub Pages, Cloudflare Pages, Netlify ou Vercel)";
        out.modelo = "PaaS/SaaS (a plataforma cuida do servidor)";
        out.motivos.push("Site que é só HTML, CSS, JS e imagens não precisa de servidor seu.", "A plataforma entrega os arquivos e costuma cuidar do HTTPS.");
        if (ctrl === "total") out.cuidados.push("Você quer controle total, mas disse que não sabe administrar servidor. Comece pela estática; VPS fica para depois de aprender.");
      }
      if (picos === "sim") {
        if (/VPS/.test(out.titulo)) out.cuidados.push("Picos de acesso: um servidor único não absorve sozinho. Ponha um CDN na frente (arquivo estático se presta a isso) ou use mais de uma máquina com balanceador de carga.");
        else out.motivos.push("Picos de acesso em arquivo estático são o caso mais fácil: a plataforma e o CDN absorvem.");
      }
    } else if (ctrl === "total" && admin === "sim") {
      out.titulo = "VPS (ou IaaS) com nginx como proxy reverso e a aplicação num container";
      out.modelo = "IaaS (você administra o sistema)";
      out.motivos.push("Você quer controle e sabe administrar: dá para instalar o que precisar.");
      if (conteudo === "banco") out.motivos.push("O banco pode rodar no mesmo VPS (mais barato, mais trabalho) ou num serviço de banco gerenciado.");
      out.cuidados.push("Backup, atualização de segurança e monitoramento passam a ser seus.");
      if (picos === "sim") out.cuidados.push("Picos de acesso: uma máquina só não escala sozinha. Planeje mais de uma máquina com balanceador de carga, ou mande a parte que oscila para funções serverless ou PaaS com escala automática.");
    } else {
      if (picos === "sim") {
        out.titulo = "Funções serverless ou PaaS com escala automática" + (conteudo === "banco" ? " + banco gerenciado" : "");
        out.modelo = "PaaS / serverless";
        out.motivos.push("Com picos de uso, pagar só pelo que executa ou escalar sozinho evita servidor parado.");
        out.cuidados.push("Serverless tem partida a frio e prende você ao fornecedor.");
      } else {
        out.titulo = "PaaS (a plataforma roda o seu código)" + (conteudo === "banco" ? " + banco gerenciado" : "");
        out.modelo = "PaaS";
        out.motivos.push("Você manda o código e a plataforma cuida do sistema e do servidor.");
      }
      if (conteudo === "banco") out.motivos.push("Banco de dados precisa de backup e de persistência; um serviço gerenciado tira esse peso de você.");
      if (ctrl === "total") out.cuidados.push("Você pediu controle total mas não sabe administrar servidor: VPS sem gerenciamento é arriscado (atualizações e segurança ficam com você). O PaaS é o caminho mais seguro para começar.");
    }
    if (orc === "zero") out.cuidados.push("Com orçamento zero, procure se a plataforma tem plano gratuito e leia os limites na página oficial (eles mudam). " + (/VPS/.test(out.titulo) ? "VPS costuma ser pago." : ""));
    if (orc === "folga" && conteudo !== "estatico") out.motivos.push("Com folga no orçamento, vale um plano pago com suporte e backup automático.");
    out.cuidados = out.cuidados.filter(Boolean);
    return out;
  };

  /* ====================== Pipeline ====================== */
  /* o: {modo: ci|entrega|implantacao, testes: boolean, segredo: boolean, aprovado: boolean} */
  DP.pipeline = function (o) {
    o = o && typeof o === "object" ? o : {};
    var modo = ["ci", "entrega", "implantacao"].indexOf(o.modo) >= 0 ? o.modo : "ci";
    var testes = o.testes !== false, segredo = !!o.segredo, aprovado = !!o.aprovado;
    var et = [
      { n: "Baixar o código", s: "ok", t: "O runner baixa a versão do commit." },
      { n: "Instalar dependências", s: "ok", t: "Instala o que o projeto declara." },
      { n: "Rodar os testes", s: testes ? "ok" : "falhou", t: testes ? "Todos os testes passaram." : "Um teste falhou: a esteira para aqui." },
      { n: "Gerar o build", s: "?", t: "" },
      { n: "Publicar (deploy)", s: "?", t: "" }
    ];
    function pula(i, motivo) { et[i].s = "pulado"; et[i].t = motivo; }
    if (!testes) { pula(3, "Não roda porque a etapa anterior falhou."); pula(4, "Não roda porque a etapa anterior falhou."); return { modo: modo, etapas: et, publicou: false }; }
    et[3].s = "ok"; et[3].t = "Gera a pasta que será publicada.";
    if (modo === "ci") { pula(4, "No modo só de integração contínua não existe etapa de publicar: o resultado é o aviso de que está tudo certo."); return { modo: modo, etapas: et, publicou: false }; }
    if (modo === "entrega" && !aprovado) { et[4].s = "aguardando"; et[4].t = "O código está pronto para subir, mas uma pessoa precisa aprovar."; return { modo: modo, etapas: et, publicou: false }; }
    if (!segredo) { et[4].s = "falhou"; et[4].t = "A credencial de publicação (cadastrada como segredo do projeto) não está configurada, então o deploy não autentica."; return { modo: modo, etapas: et, publicou: false }; }
    et[4].s = "ok"; et[4].t = modo === "entrega" ? "Publicado depois da aprovação." : "Publicado sozinho, sem aprovação humana.";
    return { modo: modo, etapas: et, publicou: true };
  };

  /* ====================== estilo ====================== */
  DP.estilo = function () {
    if (typeof document === "undefined" || document.getElementById("dp-estilo")) return;
    var st = document.createElement("style"); st.id = "dp-estilo";
    st.textContent =
      ".dpform{display:grid;gap:8px 12px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));margin:8px 0}" +
      ".dpform label{display:grid;gap:3px;font-size:.86rem;font-weight:600;min-width:0}" +
      ".dpform input,.dpform select,.dpform textarea{width:100%;box-sizing:border-box;font:.85rem var(--f-mono);padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}" +
      ".dpform textarea{min-height:64px;resize:vertical}" +
      ".dpbox{border:1px solid var(--line);border-radius:10px;background:var(--paper-2);padding:10px 12px;margin:8px 0;font:.82rem/1.5 var(--f-mono);white-space:pre-wrap;word-break:break-word}" +
      ".dpbox b{color:var(--pen)}" +
      ".dpbadge{display:inline-block;padding:2px 10px;border-radius:99px;font:700 .85rem var(--f-mono);color:#fff}" +
      ".dpbadge.s2{background:var(--green)}.dpbadge.s3{background:var(--amber)}.dpbadge.s4,.dpbadge.s5{background:var(--red)}" +
      ".dpstep{border:2px solid var(--line);border-radius:12px;background:var(--card);padding:8px 12px;margin:6px 0;font-size:.88rem}" +
      ".dpstep .who{font:700 .8rem var(--f-mono);color:var(--pen)}" +
      ".dpstep.ans{border-color:var(--green)}.dpstep.bad{border-color:var(--red)}" +
      ".dpchk{display:flex;gap:8px;align-items:flex-start;border:2px solid var(--line);border-radius:12px;padding:8px 12px;margin:6px 0;background:var(--card);font-size:.9rem}" +
      ".dpchk.ok{border-color:var(--green)}.dpchk.no{border-color:var(--red)}" +
      ".dppipe{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}" +
      ".dppipe .et{flex:1 1 140px;min-width:0;border:2px solid var(--line);border-radius:12px;padding:8px 10px;background:var(--card);font-size:.84rem}" +
      ".dppipe .et b{display:block;margin-bottom:2px}" +
      ".dppipe .et.ok{border-color:var(--green)}.dppipe .et.falhou{border-color:var(--red);background:var(--red-soft)}" +
      ".dppipe .et.pulado{opacity:.5;border-style:dashed}.dppipe .et.aguardando{border-color:var(--amber);background:var(--amber-soft)}";
    document.head.appendChild(st);
  };
})();
