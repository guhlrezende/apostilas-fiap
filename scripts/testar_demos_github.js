/* Testa a lógica das demos da apostila github-uso (sem navegador).
   Uso:  node scripts/testar_demos_github.js   (sai com código 1 se algo falhar) */
global.window = {};
const GH = require("../github-uso/demos/gh-core.js");
let falhas = 0, total = 0;
function t(nome, cond) { total++; if (!cond) { falhas++; console.log("FALHOU:", nome); } }
function naoLanca(nome, f) { try { f(); total++; } catch (e) { total++; falhas++; console.log("LANCOU em", nome, e.message); } }

/* (a) merge: números que o texto do capítulo 5 cita (PR de 3 commits, main andou) */
let r = GH.merge({ n: 3, tipo: "merge", mainAvancou: true });
t("merge commit: 7 na main", r.totalMain === 7 && r.novosNaMain === 4 && r.temCommitDeMerge);
r = GH.merge({ n: 3, tipo: "squash", mainAvancou: true });
t("squash: 4 na main", r.totalMain === 4 && r.novosNaMain === 1 && !r.commitsDoPRNaMain);
r = GH.merge({ n: 3, tipo: "rebase", mainAvancou: true });
t("rebase: 6 na main", r.totalMain === 6 && r.novosNaMain === 3 && r.hashesNovos && !r.temCommitDeMerge);
t("rebase linear sem merge no grafo", r.linhas.every(l => l.indexOf("merge do PR") < 0));
r = GH.merge({ n: 3, tipo: "merge", mainAvancou: false });
t("merge sem main andar: 6", r.totalMain === 6);
t("limites do n", GH.merge({ n: 0 }).n === 1 && GH.merge({ n: 99 }).n === 8 && GH.merge({ n: "5" }).n === 5 && GH.merge({ n: "abc" }).n === 3 && GH.merge({ n: NaN }).n === 3 && GH.merge({ n: 2.9 }).n === 2);
t("tipo inválido", GH.merge({ n: 3, tipo: "xyz" }).ok === false);
naoLanca("merge entradas ruins", () => { GH.merge(); GH.merge(null); GH.merge("x"); GH.merge({ n: {}, tipo: 5, mainAvancou: [] }); });
t("indicado", GH.indicado("logico").tipo === "squash" && GH.indicado("historico").tipo === "merge" && GH.indicado("linear").tipo === "rebase" && GH.indicado("x") === null);

/* (b) fluxo do PR */
let s = GH.pr.novo();
let a = GH.pr.agir(s, "merge"); t("merge antes de abrir recusado", !a.ok);
a = GH.pr.agir(s, "abrir_draft"); s = a.estado; t("abre draft", a.ok && s.fase === "draft");
a = GH.pr.agir(s, "merge"); t("draft não faz merge", !a.ok && /rascunho/i.test(a.msg));
a = GH.pr.agir(s, "pedir_revisao"); t("draft não pede revisão", !a.ok);
a = GH.pr.agir(s, "aprovar"); t("draft não aprova", !a.ok);
a = GH.pr.agir(s, "pronto"); s = a.estado; t("pronto", a.ok && s.fase === "aberto");
a = GH.pr.agir(s, "pedir_revisao"); s = a.estado; t("revisão", s.fase === "revisao");
a = GH.pr.agir(s, "pedir_mudancas"); s = a.estado; t("mudanças pedidas", s.fase === "mudancas");
a = GH.pr.agir(s, "merge"); t("mudanças pedidas bloqueiam", !a.ok);
a = GH.pr.agir(s, "novo_commit"); s = a.estado; t("novo commit volta à revisão", s.fase === "revisao" && s.checks === "rodando");
a = GH.pr.agir(s, "aprovar"); s = a.estado; t("aprovado", s.fase === "aprovado");
a = GH.pr.agir(s, "merge"); t("checks rodando bloqueiam", !a.ok && /check/i.test(a.msg));
a = GH.pr.agir(s, "checks_falham"); s = a.estado; a = GH.pr.agir(s, "merge"); t("check falho bloqueia", !a.ok);
a = GH.pr.agir(s, "checks_passam"); t("não passa check que não roda", !a.ok);
a = GH.pr.agir(s, "novo_commit"); s = a.estado; a = GH.pr.agir(s, "checks_passam"); s = a.estado; t("checks passam", a.ok && s.checks === "passou");
a = GH.pr.agir(s, "gerar_conflito"); s = a.estado; a = GH.pr.agir(s, "merge"); t("conflito bloqueia", !a.ok && /conflito/i.test(a.msg));
a = GH.pr.agir(s, "resolver_conflito"); s = a.estado; t("resolver conflito reinicia checks", s.checks === "rodando");
a = GH.pr.agir(s, "checks_passam"); s = a.estado;
a = GH.pr.agir(s, "merge"); s = a.estado; t("merge ok", a.ok && s.fase === "mergeado");
a = GH.pr.agir(s, "merge"); t("merge duplo recusado", !a.ok);
a = GH.pr.agir(s, "novo_commit"); t("commit depois do merge recusado", !a.ok);
a = GH.pr.agir(s, "apagar_branch"); s = a.estado; t("apaga branch", a.ok && s.branchApagada);
a = GH.pr.agir(s, "apagar_branch"); t("apagar branch duas vezes recusado", !a.ok);
/* sem regras: merge de PR aberto passa; draft continua bloqueando; "Request changes" só bloqueia se a regra de revisão estiver ligada */
s = GH.pr.novo({ aprovacao: false, checks: false });
s = GH.pr.agir(s, "abrir").estado; a = GH.pr.agir(s, "merge"); t("sem regras, aberto faz merge", a.ok);
s = GH.pr.novo({ aprovacao: false, checks: false }); s = GH.pr.agir(s, "abrir").estado; s = GH.pr.agir(s, "pedir_revisao").estado; s = GH.pr.agir(s, "pedir_mudancas").estado;
a = GH.pr.agir(s, "merge"); t("sem regra de revisão, Request changes não bloqueia", a.ok && !/Request changes/.test(GH.pr.motivos(s).join(" ")));
s.regras.aprovacao = true; t("com regra de revisão, Request changes bloqueia", GH.pr.motivos(s).some(x => /Request changes/.test(x)));
s = GH.pr.novo({ aprovacao: false }); s = GH.pr.agir(s, "abrir_draft").estado; t("draft bloqueia mesmo sem regras", GH.pr.agir(s, "merge").ok === false);
s = GH.pr.novo({ descartar: true }); s = GH.pr.agir(s, "abrir").estado; s = GH.pr.agir(s, "pedir_revisao").estado; s = GH.pr.agir(s, "aprovar").estado;
a = GH.pr.agir(s, "novo_commit"); t("descartar aprovação antiga", a.estado.fase === "revisao" && a.estado.aprovacoes === 0);
/* resolver conflito gera commit novo: com "descartar" ligado, a aprovação cai */
s = GH.pr.novo({ descartar: true, checks: false }); ["abrir", "pedir_revisao", "aprovar", "gerar_conflito"].forEach(x => { s = GH.pr.agir(s, x).estado; });
t("conflito não tira a aprovação por si", s.fase === "aprovado" && s.aprovacoes === 1);
a = GH.pr.agir(s, "resolver_conflito"); t("resolver conflito descarta aprovação com descartar ligado", a.estado.fase === "revisao" && a.estado.aprovacoes === 0);
s = GH.pr.novo({ descartar: false, checks: false }); ["abrir", "pedir_revisao", "aprovar", "gerar_conflito"].forEach(x => { s = GH.pr.agir(s, x).estado; });
a = GH.pr.agir(s, "resolver_conflito"); t("resolver conflito mantém a aprovação com descartar desligado", a.estado.fase === "aprovado" && a.estado.aprovacoes === 1);
naoLanca("pr entradas ruins", () => { GH.pr.agir(null, "abrir"); GH.pr.agir(undefined, undefined); GH.pr.agir({}, "merge"); GH.pr.agir("x", 5); GH.pr.novo(5); GH.pr.motivos(null); });
t("ação desconhecida", GH.pr.agir(GH.pr.novo(), "voar").ok === false);

/* (e) regras da main */
r = GH.regras({ minAprov: 1, aprov: 0, checks: "rodando", conversasAbertas: 1, checksObrig: true, conversasObrig: true });
t("regras: bloqueado com 3 motivos", !r.liberado && r.motivos.length === 3);
r = GH.regras({ minAprov: 1, aprov: 1, checks: "passou", conversasAbertas: 0, checksObrig: true, conversasObrig: true });
t("regras: liberado", r.liberado && !r.bypass && r.motivos.length === 0);
r = GH.regras({ minAprov: 1, aprov: 1, checks: "passou", descartarAntigas: true, novoCommitDepois: true });
t("regras: aprovação descartada", !r.liberado && r.aprovEfetivas === 0);
r = GH.regras({ minAprov: 2, aprov: 0, admin: true });
t("regras: bypass de admin", r.liberado && r.bypass);
r = GH.regras({ minAprov: 2, aprov: 0, admin: true, semBypass: true });
t("regras: admin sem bypass bloqueia", !r.liberado);
r = GH.regras({ ownersObrig: true, minAprov: 0, ownerAprovou: false });
t("regras: code owner", !r.liberado);
r = GH.regras({ ownersObrig: true, minAprov: 0, ownerAprovou: true });
t("regras: code owner aprovou", r.liberado && r.ownerEfetivo);
r = GH.regras({ ownersObrig: true, minAprov: 0, ownerAprovou: true, descartarAntigas: true, novoCommitDepois: true });
t("regras: aprovação do code owner também é descartada por novo commit", !r.liberado && !r.ownerEfetivo && /descartada/.test(r.motivos.join(" ")));
r = GH.regras({ ownersObrig: true, minAprov: 0, ownerAprovou: true, descartarAntigas: false, novoCommitDepois: true });
t("regras: sem descartar, a do owner continua valendo", r.liberado);
t("regras: limites", GH.regras({ minAprov: 99, aprov: -4 }).aprovEfetivas === 0 && GH.regras({ minAprov: "x" }).motivos.length === 1);
naoLanca("regras entradas ruins", () => { GH.regras(); GH.regras(null); GH.regras("x"); GH.regras({ minAprov: {}, aprov: [], checks: 9 }); });

/* (d) fork */
let f = GH.fork.novo();
a = GH.fork.agir(f, "clonar"); t("clonar sem fork recusado", !a.ok);
a = GH.fork.agir(f, "fetch_upstream"); t("fetch sem upstream recusado", !a.ok);
a = GH.fork.agir(f, "abrir_pr"); t("PR sem branch enviada recusado", !a.ok);
f = GH.fork.agir(f, "fork").estado; t("fork copia o original", f.origin === 3 && GH.fork.atras(f) === 0);
f = GH.fork.agir(f, "clonar").estado; t("clone", f.local === 3);
a = GH.fork.agir(f, "merge_upstream"); t("merge sem upstream recusado", !a.ok);
f = GH.fork.agir(f, "add_upstream").estado;
a = GH.fork.agir(f, "merge_upstream"); t("merge sem fetch recusado", !a.ok && /fetch/.test(a.msg));
f = GH.fork.agir(f, "dono_publica").estado; t("fork fica atrás", GH.fork.atras(f) === 1);
a = GH.fork.agir(f, "push_main"); t("push sem nada novo recusado", !a.ok);
f = GH.fork.agir(f, "fetch_upstream").estado;
f = GH.fork.agir(f, "merge_upstream").estado; t("merge integra", f.local === 4);
a = GH.fork.agir(f, "merge_upstream"); t("merge repetido recusado", !a.ok);
f = GH.fork.agir(f, "push_main").estado; t("fork em dia", GH.fork.atras(f) === 0 && f.origin === 4);
a = GH.fork.agir(f, "commit_branch"); t("commit sem branch recusado", !a.ok);
f = GH.fork.agir(f, "criar_branch").estado;
a = GH.fork.agir(f, "enviar_branch"); t("enviar branch vazia recusado", !a.ok);
f = GH.fork.agir(f, "commit_branch").estado;
a = GH.fork.agir(f, "abrir_pr"); t("PR antes de enviar recusado", !a.ok);
f = GH.fork.agir(f, "enviar_branch").estado;
a = GH.fork.agir(f, "abrir_pr"); f = a.estado; t("PR aberto", a.ok && f.pr);
a = GH.fork.agir(f, "abrir_pr"); t("PR duplicado recusado", !a.ok);
for (let i = 0; i < 20; i++) f = GH.fork.agir(f, "dono_publica").estado; t("limite de commits do dono", f.up === GH.fork.MAX);
naoLanca("fork entradas ruins", () => { GH.fork.agir(null, "fork"); GH.fork.agir({}, 7); GH.fork.agir("x"); GH.fork.atras(null); });

/* (c) vazou segredo */
t("plano pendente", GH.vazou.plano({}).pendente && GH.vazou.plano().pendente && GH.vazou.plano({ tipo: "x", visibilidade: "publico", enviado: "sim" }).pendente);
let p = GH.vazou.plano({ tipo: "chave_api", visibilidade: "publico", enviado: "sim" });
t("plano: revogar é o passo 1 e há 5 passos", !p.pendente && p.passos.length === 5 && p.passos[0].n === 1 && /Revogar/.test(p.passos[0].t));
p = GH.vazou.plano({ tipo: "token_gh", visibilidade: "privado", enviado: "sim" });
t("plano privado", /privado/i.test(p.aviso) && p.passos[0].obrig);
p = GH.vazou.plano({ tipo: "dado_pessoal", visibilidade: "publico", enviado: "sim" });
t("dado pessoal não se revoga", /não se revoga/i.test(p.passos[0].d));
p = GH.vazou.plano({ tipo: "senha", visibilidade: "publico", enviado: "nao" });
t("só local: plano curto", p.passos.length === 2);
p = GH.vazou.plano({ tipo: "dado_pessoal", visibilidade: "publico", enviado: "sim" });
t("dado pessoal público: limpeza não é opcional, vem depois de avisar", /não é opcional/i.test(p.passos[4].t) && /Avisar/.test(p.passos[3].t) && /Limpar/.test(p.passos[4].t));
t("limpeza cita clone novo, backup e --mirror em todas as refs", /clone novo/.test(p.passos[4].d) && /backup/.test(p.passos[4].d) && /todas as refs/.test(p.passos[4].d));
p = GH.vazou.plano({ tipo: "chave_api", visibilidade: "publico", enviado: "sim" });
t("chave de API: limpeza segue opcional", /opcional/i.test(p.passos[4].t));
for (const k of Object.keys(GH.vazou.TIPOS)) t("plano " + k, GH.vazou.plano({ tipo: k, visibilidade: "publico", enviado: "sim" }).passos.length === 5);
t("apagar commit antes de revogar é erro", GH.vazou.avalia("apagar_commit", []).nivel === "erro");
t("rm_cached antes de revogar é erro", GH.vazou.avalia("rm_cached", []).nivel === "erro");
t("limpar histórico antes de revogar é erro", GH.vazou.avalia("limpar_historico", []).nivel === "erro");
t("avisar o time antes de revogar é alerta", GH.vazou.avalia("avisar_time", []).nivel === "alerta" && /revogue/i.test(GH.vazou.avalia("avisar_time", []).msg));
t("avisar o time depois de revogar é bom", GH.vazou.avalia("avisar_time", ["revogar"]).nivel === "bom");
t("revogar é bom", GH.vazou.avalia("revogar", []).nivel === "bom");
t("apagar depois de revogar é só alerta", GH.vazou.avalia("apagar_commit", ["revogar"]).nivel === "alerta");
t("repetir ação é alerta", GH.vazou.avalia("revogar", ["revogar"]).nivel === "alerta");
t("ação desconhecida", GH.vazou.avalia("x", []).ok === false && GH.vazou.avalia(undefined, null).ok === false);
naoLanca("vazou entradas ruins", () => { GH.vazou.avalia("revogar", "x"); GH.vazou.plano(5); });

t("inteiro", GH.inteiro(" ", 1, 5, 3) === 3 && GH.inteiro(true, 1, 5, 3) === 3 && GH.inteiro("7", 1, 5, 3) === 5 && GH.inteiro(Infinity, 1, 5, 3) === 3);
console.log(falhas ? falhas + " falha(s) de " + total : "Tudo certo: " + total + " verificações");
process.exit(falhas ? 1 : 0);
