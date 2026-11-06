/* Núcleo das demos de terminal: um sistema de arquivos falso e um mini shell.
   Sem DOM: dá para conferir as saídas fora do navegador (node). As demos terminalSim e pipeViz usam este arquivo.
   Cobre só o que a apostila ensina: pwd, ls, cd, cat, head, tail, wc, grep, sort, uniq, cut, echo, mkdir, touch, cp, mv, rm,
   awk e sed em formas simples, pipes (|) e redirecionamentos (>, >>, 2>, 2>&1). */
(function () {
  var E = window.Estudo = window.Estudo || { demos: {} };
  var TG = E.tg = {};

  /* ---------------- sistema de arquivos falso ---------------- */
  function dir() { return { t: "d", c: {} }; }
  function arq(s) { return { t: "f", s: s }; }
  var HOME = "/c/Users/voce";
  TG.HOME = HOME;
  TG.novoFs = function () {
    var raiz = dir(), estudo = dir(), c = raiz;
    ["c", "Users", "voce"].forEach(function (n) { var d = dir(); c.c[n] = d; c = d; });
    c.c.estudo = estudo;
    estudo.c["tarefas.txt"] = arq("estudar git\nler a apostila\nfazer exercicio\n");
    estudo.c["vendas.csv"] = arq("produto,qtd,preco\ncaneta,10,2\ncaderno,3,15\nlapis,25,1\ncaneta,5,2\ncaderno,2,15\n");
    estudo.c["log.txt"] = arq("10:01 INFO login ana\n10:03 ERRO disco cheio\n10:05 INFO login bia\n10:07 ERRO timeout\n10:09 INFO logout ana\n10:12 ERRO timeout\n");
    estudo.c.projeto = dir();
    return raiz;
  };

  function partes(cwd, p, home) {
    if (p === "~" || p.indexOf("~/") === 0) p = home + p.slice(1);
    var base = p.charAt(0) === "/" ? [] : cwd.split("/").filter(Boolean), out = base;
    p.split("/").forEach(function (s) {
      if (!s || s === ".") return;
      if (s === "..") out.pop(); else out.push(s);
    });
    return out;
  }
  function achar(raiz, ps) {
    var n = raiz;
    for (var i = 0; i < ps.length; i++) { if (!n || n.t !== "d" || !n.c.hasOwnProperty(ps[i])) return null; n = n.c[ps[i]]; }
    return n;
  }

  /* ---------------- tokenizador ---------------- */
  function tokens(linha) {
    var out = [], i = 0, w = "", tem = false, q = false;
    function fim() { if (tem) out.push({ w: w, q: q }); w = ""; tem = false; q = false; }
    while (i < linha.length) {
      var ch = linha.charAt(i);
      if (ch === " " || ch === "\t") { fim(); i++; continue; }
      if (ch === "'" || ch === '"') {
        var j = linha.indexOf(ch, i + 1);
        if (j < 0) throw new Error("aspas sem fechar");
        w += linha.slice(i + 1, j); tem = true; q = true; i = j + 1; continue;
      }
      if (ch === "|") { fim(); out.push({ op: "|" }); i++; continue; }
      if (linha.substr(i, 4) === "2>&1" && !tem) { out.push({ op: "2>&1" }); i += 4; continue; }
      if (linha.substr(i, 2) === "2>" && !tem) { fim(); out.push({ op: "2>" }); i += 2; continue; }
      if (ch === ">") { fim(); if (linha.charAt(i + 1) === ">") { out.push({ op: ">>" }); i += 2; } else { out.push({ op: ">" }); i++; } continue; }
      w += ch; tem = true; i++;
    }
    fim();
    return out;
  }
  function linhas(s) { if (!s) return []; var a = s.split("\n"); if (a[a.length - 1] === "") a.pop(); return a; }
  function juntar(a) { return a.length ? a.join("\n") + "\n" : ""; }
  TG.linhas = linhas;

  /* ---------------- o shell ---------------- */
  function Shell(raiz) { this.raiz = raiz || TG.novoFs(); this.cwd = HOME + "/estudo"; this.ultimo = 0; }
  TG.Shell = Shell;
  Shell.prototype.prompt = function () {
    var c = this.cwd;
    if (c === HOME) c = "~"; else if (c.indexOf(HOME + "/") === 0) c = "~" + c.slice(HOME.length);
    return c + " $";
  };
  Shell.prototype.no = function (p) { return achar(this.raiz, partes(this.cwd, p, HOME)); };
  Shell.prototype.pai = function (p) {
    var ps = partes(this.cwd, p, HOME), nome = ps.pop();
    return { dir: achar(this.raiz, ps), nome: nome, ps: ps };
  };
  /* expande * em palavras sem aspas */
  Shell.prototype.glob = function (t) {
    if (t.q || t.w.indexOf("*") < 0) return [t.w];
    var pos = t.w.lastIndexOf("/"), d = pos >= 0 ? t.w.slice(0, pos + 1) : "", pad = t.w.slice(pos + 1);
    var base = this.no(d || ".");
    if (!base || base.t !== "d") return [t.w];
    var re = new RegExp("^" + pad.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*") + "$");
    var achados = Object.keys(base.c).filter(function (n) { return re.test(n) && n.charAt(0) !== "."; }).sort();
    return achados.length ? achados.map(function (n) { return d + n; }) : [t.w];
  };

  /* Executa uma linha. Devolve { out, err, code, clear, stages:[{cmd, entrada, out, err, code}] }. */
  Shell.prototype.run = function (linha) {
    var self = this, tk;
    try { tk = tokens(linha); } catch (e) { return { out: "", err: "bash: " + e.message + "\n", code: 2, stages: [] }; }
    if (!tk.length) return { out: "", err: "", code: this.ultimo, stages: [] };
    var estagios = [[]];
    tk.forEach(function (t) { if (t.op === "|") estagios.push([]); else estagios[estagios.length - 1].push(t); });
    var stdin = "", errTotal = "", code = 0, stages = [], saida = "", clear = false;
    for (var k = 0; k < estagios.length; k++) {
      var st = estagios[k], argv = [], red = { out: null, err: null };
      /* os redirecionamentos valem na ordem em que aparecem, como no bash:
         "> arq 2>&1" manda saida e erro para o arquivo; "2>&1 > arq" copia o erro para onde a saida ESTÁ AGORA (a tela ou o pipe) e só depois manda a saida ao arquivo */
      for (var i = 0; i < st.length; i++) {
        var t = st[i];
        if (t.op === ">" || t.op === ">>" || t.op === "2>") {
          var alvo = st[i + 1];
          if (!alvo || alvo.op) return { out: "", err: "bash: erro de sintaxe perto de '" + t.op + "'\n", code: 2, stages: [] };
          var r = { p: alvo.w, add: t.op === ">>" };
          if (t.op === "2>") red.err = { arq: r, junto: false }; else red.out = r;
          i++;
        } else if (t.op === "2>&1") red.err = red.out ? { arq: red.out, junto: true } : { tela: true };
        else if (t.op) return { out: "", err: "bash: erro de sintaxe\n", code: 2, stages: [] };
        else argv = argv.concat(self.glob(t));
      }
      if (!argv.length) return { out: "", err: "bash: erro de sintaxe: comando vazio\n", code: 2, stages: [] };
      var entrada = stdin;
      var ultimoEst = k === estagios.length - 1;
      var res = self.exec(argv, stdin, ultimoEst && !red.out);
      var o = res.out || "", e = res.err || "", fluxo = "";
      if (red.err && red.err.tela) { fluxo = e; e = ""; }
      else if (red.err && red.err.junto) { o += e; e = ""; }
      if (red.out) { var m = self.escreve(red.out.p, o, red.out.add); if (m) e += m; } else fluxo = o + fluxo;
      if (red.err && red.err.arq && !red.err.junto) { var m2 = self.escreve(red.err.arq.p, e, red.err.arq.add); e = m2 || ""; }
      o = fluxo;
      if (res.clear) clear = true;
      stages.push({ cmd: argv.join(" "), entrada: entrada, out: o, err: e, code: res.code });
      errTotal += e; code = res.code; stdin = o; saida = o;
    }
    this.ultimo = code;
    return { out: saida, err: errTotal, code: code, clear: clear, stages: stages };
  };
  Shell.prototype.escreve = function (p, texto, add) {
    var pa = this.pai(p);
    if (!pa.dir || pa.dir.t !== "d") return "bash: " + p + ": No such file or directory\n";
    var ex = pa.dir.c[pa.nome];
    if (ex && ex.t === "d") return "bash: " + p + ": Is a directory\n";
    if (ex && add) ex.s += texto; else pa.dir.c[pa.nome] = arq(texto);
    return "";
  };

  /* ---------------- comandos ---------------- */
  var CMD = {};
  function leArquivos(sh, nome, args, stdin, usaStdin) {
    /* devolve { textos:[{nome,s}], err, code } */
    var textos = [], err = "", code = 0;
    if (!args.length) { return { textos: [{ nome: "", s: stdin }], err: "", code: 0 }; }
    args.forEach(function (a) {
      var n = sh.no(a);
      if (!n) { err += nome + ": " + a + ": No such file or directory\n"; code = 1; }
      else if (n.t === "d") { err += nome + ": " + a + ": Is a directory\n"; code = 1; }
      else textos.push({ nome: a, s: n.s });
    });
    return { textos: textos, err: err, code: code };
  }
  function opcoes(args, comValor) {
    /* separa -x flags e argumentos. comValor: letras que levam valor (-n 3). Aceita -n3 e -n 3. */
    var o = {}, resto = [];
    for (var i = 0; i < args.length; i++) {
      var a = args[i];
      if (a.length > 1 && a.charAt(0) === "-" && !/^-\d+$/.test(a) && a !== "-") {
        var letras = a.slice(1);
        for (var j = 0; j < letras.length; j++) {
          var l = letras.charAt(j);
          if (comValor.indexOf(l) >= 0) {
            var v = letras.slice(j + 1);
            if (!v) { v = args[++i]; }
            o[l] = v; break;
          } else o[l] = true;
        }
      } else if (/^-\d+$/.test(a) && comValor.indexOf("n") >= 0) o.n = a.slice(1);
      else resto.push(a);
    }
    return { o: o, a: resto };
  }
  Shell.prototype.exec = function (argv, stdin, tty) {
    var nome = argv[0], f = CMD[nome];
    if (!f) return { out: "", err: "bash: " + nome + ": command not found\n", code: 127 };
    try { return f(this, argv.slice(1), stdin, tty); }
    catch (e) { return { out: "", err: "bash: " + nome + ": o simulador não conseguiu executar isto\n", code: 1 }; }
  };

  CMD.pwd = function (sh) { return { out: sh.cwd + "\n", err: "", code: 0 }; };
  CMD.whoami = function () { return { out: "voce\n", err: "", code: 0 }; };
  CMD.clear = function () { return { out: "", err: "", code: 0, clear: true }; };
  CMD.echo = function (sh, args) {
    var nl = true; if (args[0] === "-n") { nl = false; args = args.slice(1); }
    return { out: args.join(" ") + (nl ? "\n" : ""), err: "", code: 0 };
  };
  CMD.cd = function (sh, args) {
    var alvo = args[0] || "~", ps = partes(sh.cwd, alvo, HOME), n = achar(sh.raiz, ps);
    if (!n) return { out: "", err: "bash: cd: " + alvo + ": No such file or directory\n", code: 1 };
    if (n.t !== "d") return { out: "", err: "bash: cd: " + alvo + ": Not a directory\n", code: 1 };
    sh.cwd = "/" + ps.join("/"); return { out: "", err: "", code: 0 };
  };
  function perms(n) { return n.t === "d" ? "drwxr-xr-x" : "-rw-r--r--"; }
  function tam(n) { return n.t === "d" ? 0 : unescape(encodeURIComponent(n.s)).length; }
  CMD.ls = function (sh, args, stdin, tty) {
    var op = opcoes(args, ""), longo = !!op.o.l, todos = !!op.o.a, alvos = op.a.length ? op.a : ["."], out = "", err = "", code = 0, multi = alvos.length > 1, soltos = [];
    alvos.forEach(function (a, idx) {
      var n = sh.no(a);
      if (!n) { err += "ls: cannot access '" + a + "': No such file or directory\n"; code = 2; return; }
      var itens;
      if (n.t === "f") itens = [[a, n]];
      else {
        var nomes = Object.keys(n.c).sort(function (x, y) { x = x.toLowerCase(); y = y.toLowerCase(); return x < y ? -1 : x > y ? 1 : 0; });
        if (!todos) nomes = nomes.filter(function (x) { return x.charAt(0) !== "."; });
        itens = nomes.map(function (x) { return [x, n.c[x]]; });
        if (todos) itens = [[".", n], ["..", n]].concat(itens);
      }
      if (multi && n.t === "d") out += (idx ? "\n" : "") + a + ":\n";
      if (longo) {
        var tot = 0; itens.forEach(function (p) { if (p[1].t === "f") tot += Math.ceil(tam(p[1]) / 1024); });
        if (n.t === "d") out += "total " + tot + "\n";
        var larg = 1; itens.forEach(function (p) { larg = Math.max(larg, String(tam(p[1])).length); });
        itens.forEach(function (p) { var sz = String(tam(p[1])); while (sz.length < larg) sz = " " + sz; out += perms(p[1]) + " 1 voce 197609 " + sz + " Nov  6 13:49 " + p[0] + "\n"; });
      } else {
        var nm = itens.map(function (p) { return p[0]; });
        if (n.t === "f") soltos.push(nm[0]);
        else out += nm.length ? (tty ? nm.join("  ") : nm.join("\n")) + "\n" : "";
      }
    });
    if (soltos.length) out = (tty ? soltos.join("  ") : soltos.join("\n")) + "\n" + out;
    return { out: out, err: err, code: code };
  };
  CMD.cat = function (sh, args, stdin) {
    var r = leArquivos(sh, "cat", args, stdin), out = "";
    r.textos.forEach(function (t) { out += t.s; });
    return { out: out, err: r.err, code: r.code };
  };
  function cabecaCauda(ehHead) {
    return function (sh, args, stdin) {
      var op = opcoes(args, "n"), nTxt = op.o.n === undefined ? "10" : String(op.o.n), r = leArquivos(sh, ehHead ? "head" : "tail", op.a, stdin), out = "";
      r.textos.forEach(function (t, i) {
        var ls = linhas(t.s), res;
        if (!ehHead && nTxt.charAt(0) === "+") res = ls.slice(parseInt(nTxt.slice(1), 10) - 1);
        else { var n = parseInt(nTxt, 10); res = ehHead ? ls.slice(0, n) : ls.slice(Math.max(0, ls.length - n)); }
        if (r.textos.length > 1) out += (i ? "\n" : "") + "==> " + t.nome + " <==\n";
        out += juntar(res);
      });
      return { out: out, err: r.err, code: r.code };
    };
  }
  CMD.head = cabecaCauda(true); CMD.tail = cabecaCauda(false);
  CMD.wc = function (sh, args, stdin) {
    var op = opcoes(args, ""), r = leArquivos(sh, "wc", op.a, stdin), out = "";
    var flags = ["l", "w", "c"].filter(function (x) { return op.o[x]; });
    var linhasWc = r.textos.map(function (t) {
      var l = (t.s.match(/\n/g) || []).length, w = (t.s.trim() ? t.s.trim().split(/\s+/).length : 0), c = tam({ t: "f", s: t.s });
      return { nome: t.nome, v: { l: l, w: w, c: c } };
    });
    var larg = 1; if (!flags.length || flags.length > 1) linhasWc.forEach(function (x) { larg = Math.max(larg, String(x.v.c).length); });
    linhasWc.forEach(function (x) {
      var usar = flags.length ? flags : ["l", "w", "c"];
      out += usar.map(function (f) { var s = String(x.v[f]); while (s.length < (flags.length === 1 ? 1 : larg)) s = " " + s; return s; }).join(" ") + (x.nome ? " " + x.nome : "") + "\n";
    });
    return { out: out, err: r.err, code: r.code };
  };
  CMD.grep = function (sh, args, stdin) {
    var op = opcoes(args, ""), pad = op.a[0], arquivos = op.a.slice(1);
    if (pad === undefined) return { out: "", err: "Usage: grep [OPTION]... PATTERNS [FILE]...\n", code: 2 };
    var re; try { re = new RegExp(pad, op.o.i ? "i" : ""); } catch (e) { return { out: "", err: "grep: padrão inválido\n", code: 2 }; }
    var r = leArquivos(sh, "grep", arquivos, stdin), out = "", achou = 0, multi = r.textos.length > 1;
    r.textos.forEach(function (t) {
      var cont = 0;
      linhas(t.s).forEach(function (l, i) {
        var casa = re.test(l); if (op.o.v) casa = !casa;
        if (!casa) return;
        cont++; if (op.o.c) return;
        out += (multi ? t.nome + ":" : "") + (op.o.n ? (i + 1) + ":" : "") + l + "\n";
      });
      achou += cont;
      if (op.o.c) out += (multi ? t.nome + ":" : "") + cont + "\n";
    });
    return { out: out, err: r.err, code: r.err ? 2 : (achou ? 0 : 1) };
  };
  CMD.sort = function (sh, args, stdin) {
    var op = opcoes(args, ""), r = leArquivos(sh, "sort", op.a, stdin), ls = [];
    r.textos.forEach(function (t) { ls = ls.concat(linhas(t.s)); });
    function cmpTxt(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
    function num(s) { var m = /^\s*(-?\d+(\.\d+)?)/.exec(s); return m ? parseFloat(m[1]) : 0; }
    ls.sort(function (a, b) {
      var c = op.o.n ? num(a) - num(b) : 0;
      if (c === 0) c = cmpTxt(a, b);
      return op.o.r ? -c : c;
    });
    if (op.o.u) ls = ls.filter(function (l, i) { return i === 0 || l !== ls[i - 1]; });
    return { out: juntar(ls), err: r.err, code: r.code };
  };
  CMD.uniq = function (sh, args, stdin) {
    var op = opcoes(args, ""), r = leArquivos(sh, "uniq", op.a, stdin), ls = linhas(r.textos.length ? r.textos[0].s : ""), out = [], i = 0;
    while (i < ls.length) {
      var j = i; while (j < ls.length && ls[j] === ls[i]) j++;
      var n = j - i, pre = op.o.c ? ("       " + n).slice(-7) + " " : "";
      out.push(pre + ls[i]); i = j;
    }
    return { out: juntar(out), err: r.err, code: r.code };
  };
  CMD.cut = function (sh, args, stdin) {
    var op = opcoes(args, "df"), r = leArquivos(sh, "cut", op.a, stdin), d = op.o.d === undefined ? "\t" : op.o.d, f = op.o.f;
    if (f === undefined || f === true) return { out: "", err: "cut: você deve informar uma lista de campos (-f)\n", code: 1 };
    var sel = []; String(f).split(",").forEach(function (p) {
      var m = /^(\d*)-(\d*)$/.exec(p);
      if (m) sel.push([m[1] ? +m[1] : 1, m[2] ? +m[2] : 1e9]); else sel.push([+p, +p]);
    });
    var out = [];
    r.textos.forEach(function (t) {
      linhas(t.s).forEach(function (l) {
        var cs = l.split(d), pegos = [];
        if (cs.length === 1) { out.push(l); return; }
        cs.forEach(function (c, i) { sel.forEach(function (s) { if (i + 1 >= s[0] && i + 1 <= s[1] && pegos.indexOf(i) < 0) pegos.push(i); }); });
        pegos.sort(function (a, b) { return a - b; });
        out.push(pegos.map(function (i) { return cs[i]; }).join(d));
      });
    });
    return { out: juntar(out), err: r.err, code: r.code };
  };
  CMD.mkdir = function (sh, args) {
    var op = opcoes(args, ""), err = "", code = 0;
    op.a.forEach(function (a) {
      var ps = partes(sh.cwd, a, HOME), n = sh.raiz;
      for (var i = 0; i < ps.length; i++) {
        var ultimo = i === ps.length - 1;
        if (n.t !== "d") { err += "mkdir: cannot create directory '" + (op.o.p ? ps[i - 1] : a) + "': Not a directory\n"; code = 1; return; }
        if (!n.c[ps[i]]) { if (!ultimo && !op.o.p) { err += "mkdir: cannot create directory '" + a + "': No such file or directory\n"; code = 1; return; } n.c[ps[i]] = dir(); }
        else if (ultimo && (!op.o.p || n.c[ps[i]].t !== "d")) { err += "mkdir: cannot create directory '" + a + "': File exists\n"; code = 1; return; }
        n = n.c[ps[i]];
      }
    });
    return { out: "", err: err, code: code };
  };
  CMD.touch = function (sh, args) {
    var err = "", code = 0;
    args.forEach(function (a) {
      var p = sh.pai(a);
      if (!p.dir || p.dir.t !== "d") { err += "touch: cannot touch '" + a + "': No such file or directory\n"; code = 1; return; }
      if (!p.dir.c[p.nome]) p.dir.c[p.nome] = arq("");
    });
    return { out: "", err: err, code: code };
  };
  function copia(n) { return n.t === "f" ? arq(n.s) : (function () { var d = dir(); Object.keys(n.c).forEach(function (k) { d.c[k] = copia(n.c[k]); }); return d; })(); }
  CMD.cp = function (sh, args) {
    var op = opcoes(args, ""), a = op.a;
    if (a.length < 2) return { out: "", err: "cp: missing file operand\n", code: 1 };
    var orig = sh.no(a[0]); if (!orig) return { out: "", err: "cp: cannot stat '" + a[0] + "': No such file or directory\n", code: 1 };
    if (orig.t === "d" && !op.o.r) return { out: "", err: "cp: -r not specified; omitting directory '" + a[0] + "'\n", code: 1 };
    var dest = sh.no(a[1]), p = sh.pai(a[1]);
    if (dest && dest.t === "d") dest.c[partes(sh.cwd, a[0], HOME).pop()] = copia(orig);
    else if (p.dir && p.dir.t === "d") p.dir.c[p.nome] = copia(orig);
    else return { out: "", err: "cp: cannot create regular file '" + a[1] + "': No such file or directory\n", code: 1 };
    return { out: "", err: "", code: 0 };
  };
  function contem(n, alvo) { if (n === alvo) return true; return n.t === "d" && Object.keys(n.c).some(function (k) { return contem(n.c[k], alvo); }); }
  CMD.mv = function (sh, args) {
    if (args.length < 2) return { out: "", err: "mv: missing file operand\n", code: 1 };
    var orig = sh.no(args[0]); if (!orig) return { out: "", err: "mv: cannot stat '" + args[0] + "': No such file or directory\n", code: 1 };
    var po = sh.pai(args[0]), dest = sh.no(args[1]), pd = sh.pai(args[1]), dDir, dNome, mostra;
    if (!po.dir || orig === sh.raiz) return { out: "", err: "mv: cannot move '" + args[0] + "': Device or resource busy\n", code: 1 };
    if (dest && dest.t === "d") { dDir = dest; dNome = po.nome; mostra = args[1].replace(/\/+$/, "") + "/" + po.nome; }
    else if (pd.dir && pd.dir.t === "d") { dDir = pd.dir; dNome = pd.nome; mostra = args[1]; }
    else return { out: "", err: "mv: cannot move '" + args[0] + "' to '" + args[1] + "': No such file or directory\n", code: 1 };
    /* o destino final é o próprio arquivo: o bash recusa e não mexe em nada */
    if (dDir === po.dir && dNome === po.nome) return { out: "", err: "mv: '" + args[0] + "' and '" + mostra + "' are the same file\n", code: 1 };
    if (orig.t === "d" && contem(orig, dDir)) return { out: "", err: "mv: cannot move '" + args[0] + "' to a subdirectory of itself, '" + mostra + "'\n", code: 1 };
    dDir.c[dNome] = orig; delete po.dir.c[po.nome];
    return { out: "", err: "", code: 0 };
  };
  CMD.rm = function (sh, args) {
    var op = opcoes(args, ""), err = "", code = 0;
    op.a.forEach(function (a) {
      var n = sh.no(a), p = sh.pai(a);
      if (!n) { if (!op.o.f) { err += "rm: cannot remove '" + a + "': No such file or directory\n"; code = 1; } return; }
      if (n.t === "d" && !op.o.r) { err += "rm: cannot remove '" + a + "': Is a directory\n"; code = 1; return; }
      if (n === sh.raiz || a === "/" ) { err += "rm: it is dangerous to operate recursively on '/'\n"; code = 1; return; }
      delete p.dir.c[p.nome];
    });
    return { out: "", err: err, code: code };
  };

  /* sed: s/a/b/ (com g), -n 'Np' e -n 'N,Mp' */
  CMD.sed = function (sh, args, stdin) {
    var op = opcoes(args, ""), prog = op.a[0], r = leArquivos(sh, "sed", op.a.slice(1), stdin), out = [];
    if (prog === undefined) return { out: "", err: "sed: faltou o programa\n", code: 1 };
    var ms = /^s\/(.*?)\/(.*?)\/(g?)$/.exec(prog), mp = /^(\d+)(?:,(\d+))?p$/.exec(prog);
    if (!ms && !mp) return { out: "", err: "sed: o simulador só entende s/antigo/novo/ (com g) e -n 'Np' ou -n 'N,Mp'\n", code: 1 };
    r.textos.forEach(function (t) {
      linhas(t.s).forEach(function (l, i) {
        if (ms) out.push(op.o.n ? null : l.replace(new RegExp(ms[1], ms[3]), ms[2]));
        else if (op.o.n) { var a = +mp[1], b = mp[2] ? +mp[2] : a; if (i + 1 >= a && i + 1 <= b) out.push(l); }
        else { out.push(l); var a2 = +mp[1], b2 = mp[2] ? +mp[2] : a2; if (i + 1 >= a2 && i + 1 <= b2) out.push(l); }
      });
    });
    return { out: juntar(out.filter(function (x) { return x !== null; })), err: r.err, code: r.code };
  };

  /* awk: -F, filtro opcional (NR>N, NR==N, /re/), corpo { print $1, $3 } ou { s+=$2*$3 }, e END { print s } */
  CMD.awk = function (sh, args, stdin) {
    var op = opcoes(args, "F"), prog = op.a[0], r = leArquivos(sh, "awk", op.a.slice(1), stdin);
    var NAO = { out: "", err: "awk: o simulador só entende '{print $1, $3}', 'NR>1 {s+=$2*$3} END {print s}' e filtros /texto/ ou NR>N\n", code: 1 };
    if (prog === undefined) return NAO;
    var m = /^\s*(NR\s*(?:>=|>|==|<=|<)\s*\d+|\/[^\/]*\/)?\s*(?:\{([^}]*)\})?\s*(?:END\s*\{([^}]*)\})?\s*$/.exec(prog);
    if (!m || (!m[2] && !m[3])) return NAO;
    var sep = op.o.F ? String(op.o.F) : null, vars = {}, out = [];
    function campo(cs, linha, tx) { tx = tx.trim(); if (tx === "$0") return linha; var mm = /^\$(\d+)$/.exec(tx); if (mm) return cs[+mm[1] - 1] === undefined ? "" : cs[+mm[1] - 1]; return null; }
    function expr(cs, linha, tx) {
      var fat = tx.split("*").map(function (p) { p = p.trim(); var v = campo(cs, linha, p); if (v !== null) return parseFloat(v) || 0; if (/^-?\d+(\.\d+)?$/.test(p)) return parseFloat(p); return vars.hasOwnProperty(p) ? vars[p] : 0; });
      return fat.reduce(function (a, b) { return a * b; }, 1);
    }
    function fmt(v) { return typeof v === "number" ? String(Math.round(v * 1e6) / 1e6) : String(v); }
    function execStm(txt, cs, linha) {
      txt.split(";").forEach(function (s) {
        s = s.trim(); if (!s) return;
        var pr = /^print\s*(.*)$/.exec(s);
        if (pr) { out.push(pr[1].trim() ? pr[1].split(",").map(function (x) { x = x.trim(); var v = campo(cs, linha, x); if (v !== null) return v; return vars.hasOwnProperty(x) ? fmt(vars[x]) : x; }).join(" ") : linha); return; }
        var at = /^(\w+)\s*\+=\s*(.+)$/.exec(s); if (at) { vars[at[1]] = (vars[at[1]] || 0) + expr(cs, linha, at[2]); return; }
        throw new Error("x");
      });
    }
    try {
      var nr = 0;
      r.textos.forEach(function (t) {
        linhas(t.s).forEach(function (l) {
          nr++;
          var cs = sep ? l.split(sep) : l.trim().split(/\s+/), ok = true;
          if (m[1]) {
            if (m[1].charAt(0) === "/") ok = new RegExp(m[1].slice(1, -1)).test(l);
            else { var q = /NR\s*(>=|>|==|<=|<)\s*(\d+)/.exec(m[1]), v = +q[2]; ok = { ">": nr > v, ">=": nr >= v, "==": nr === v, "<=": nr <= v, "<": nr < v }[q[1]]; }
          }
          if (ok && m[2] !== undefined) execStm(m[2], cs, l);
          else if (ok && m[1] && m[2] === undefined) out.push(l);
        });
      });
      if (m[3]) execStm(m[3], [], "");
    } catch (e) { return NAO; }
    return { out: juntar(out), err: r.err, code: r.code };
  };

  CMD.help = function () {
    return { out: "Comandos do simulador: pwd, ls [-l -a], cd, cat, head, tail, wc, grep [-i -v -c -n], sort [-r -n], uniq [-c], cut -d -f, echo, mkdir [-p], touch, cp, mv, rm [-r], awk, sed, clear.\nVocê também pode usar | (pipe), > (sobrescreve), >> (acrescenta), 2> (só o erro) e 2>&1 (erro junto da saída).\n", err: "", code: 0 };
  };
  TG.comandos = Object.keys(CMD);

  /* estilo comum das demos (injetado uma vez). As cores do terminal seguem as dos blocos de código da apostila. */
  TG.estilo = function () {
    if (typeof document === "undefined" || document.getElementById("tg-estilo")) return;
    var st = document.createElement("style"); st.id = "tg-estilo";
    st.textContent =
      ".tgterm{background:#161b27;color:#dfe6f7;border:1px solid #2a3350;border-radius:12px;font:.85rem/1.55 var(--f-mono);overflow:hidden;margin:10px 0}" +
      ".tgterm .tgout{max-height:300px;min-height:150px;overflow:auto;padding:12px 14px;white-space:pre-wrap;word-break:break-word}" +
      ".tgterm .tgerr{color:#ff8d84}.tgterm .tgps{color:#8fc1ff}.tgterm .tgok{color:#a5e88d}" +
      ".tgterm .tgin{display:flex;gap:8px;align-items:center;padding:8px 14px;border-top:1px solid #2a3350;background:#10141e}" +
      ".tgterm .tgin span{color:#8fc1ff;white-space:nowrap}" +
      ".tgterm input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:#dfe6f7;font:inherit}" +
      ".tgchips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}" +
      ".tgchips button{border:1px solid var(--line);background:var(--paper-2);color:var(--ink);border-radius:99px;padding:3px 11px;font:.78rem var(--f-mono);cursor:pointer}" +
      ".tgchips button:hover{border-color:var(--pen);color:var(--pen)}" +
      ".tgst{display:grid;gap:8px;margin:10px 0}" +
      ".tgst .tgcard{border:2px solid var(--line);border-radius:12px;background:var(--card);padding:8px 12px;opacity:.35;transition:opacity .25s,border-color .25s}" +
      ".tgst .tgcard.on{opacity:1;border-color:var(--pen)}" +
      ".tgst .tgcard code{font-weight:700}" +
      ".tgst .tgcard pre{margin:6px 0 0;padding:8px 10px;font-size:.78rem;max-height:150px}" +
      ".tgst .tgcard small{color:var(--muted)}" +
      ".tgbits{display:grid;grid-template-columns:auto repeat(3,minmax(0,1fr));gap:6px 10px;align-items:center;max-width:430px;margin:10px 0}" +
      ".tgbits label{display:flex;gap:6px;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:8px;padding:5px;background:var(--paper-2)}" +
      ".tggit{width:100%;overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--paper)}" +
      ".tggit svg{display:block;min-width:100%}";
    document.head.appendChild(st);
  };
  TG.esc = function (t) { return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
})();
