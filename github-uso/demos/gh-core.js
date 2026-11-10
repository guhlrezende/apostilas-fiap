/* Núcleo das demos de GitHub: como usar do jeito certo. Sem DOM nas funções de lógica: dá para conferir em node.
   Tudo é simulado e com dados fictícios. Nada sai da página e nenhuma conta ou serviço do GitHub é chamado. */
(function () {
  var E = window.Estudo = window.Estudo || { demos: {} };
  E.demos = E.demos || {};
  var GH = E.gh = {};

  GH.esc = function (t) { return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };

  /* Converte para inteiro dentro de [min, max]; entrada inválida (texto, NaN, vazio) vira o padrão. */
  GH.inteiro = function (v, min, max, padrao) {
    if (typeof v === "string" && v.trim() === "") return padrao;
    if (v === null || v === undefined || typeof v === "boolean") return padrao;
    var n = Number(v);
    if (!isFinite(n)) return padrao;
    n = Math.floor(n);
    return Math.max(min, Math.min(max, n));
  };
  GH.bool = function (v) { return v === true || v === "1" || v === "true" || v === 1; };

  /* ====================== (a) tipos de merge ====================== */
  GH.TIPOS = { merge: "Merge commit", squash: "Squash and merge", rebase: "Rebase and merge" };
  GH.BASE = 2; /* a main começa com 2 commits: c1 e c2 */
  GH.SITUACOES = {
    logico: { rot: "O PR é uma única mudança lógica, com vários commits de ajuste", tipo: "squash", porque: "a página oficial indica squash quando o PR é uma única mudança lógica com muitos commits de ajuste: a main ganha um commit só." },
    historico: { rot: "O histórico completo importa e cada commit tem significado", tipo: "merge", porque: "a página oficial indica o merge commit quando o histórico completo importa: todos os commits do PR ficam, mais um commit de merge." },
    linear: { rot: "O time quer histórico linear e os commits já estão bem organizados", tipo: "rebase", porque: "a página oficial indica rebase and merge para histórico linear com commits já organizados: sem commit de merge, e o GitHub recria os commits com novos SHAs." }
  };

  GH.indicado = function (sit) {
    var s = GH.SITUACOES[sit];
    return s ? { tipo: s.tipo, porque: s.porque, rot: s.rot } : null;
  };

  /* opts: {n (1 a 8), tipo, mainAvancou}. Nunca lança erro. */
  GH.merge = function (opts) {
    opts = opts && typeof opts === "object" ? opts : {};
    var n = GH.inteiro(opts.n, 1, 8, 3);
    var tipo = typeof opts.tipo === "string" ? opts.tipo : "merge";
    if (!GH.TIPOS[tipo]) return { ok: false, erro: "Tipo de merge desconhecido: " + GH.esc(String(opts.tipo)) };
    var m1 = GH.bool(opts.mainAvancou);
    var i, linhas = [], novos, merge = false;
    var pr = []; for (i = 1; i <= n; i++) pr.push("p" + i);
    if (tipo === "merge") {
      novos = n + 1; merge = true;
      linhas.push("*   M   merge do PR (2 pais)");
      linhas.push("|\\");
      for (i = n; i >= 1; i--) linhas.push("| * p" + i + "  commit do PR");
      if (m1) { linhas.push("* | m1  main andou"); linhas.push("|/"); } else { linhas.push("|/"); }
    } else if (tipo === "squash") {
      novos = 1;
      linhas.push("* S   um commit com tudo (squash de p1 a p" + n + ")");
      if (m1) linhas.push("* m1  main andou");
    } else {
      novos = n;
      for (i = n; i >= 1; i--) linhas.push("* p" + i + "' (hash novo)");
      if (m1) linhas.push("* m1  main andou");
    }
    linhas.push("* c2  base"); linhas.push("* c1  base");
    var total = GH.BASE + (m1 ? 1 : 0) + novos;
    return {
      ok: true, n: n, tipo: tipo, nome: GH.TIPOS[tipo], mainAvancou: m1, linhas: linhas,
      novosNaMain: novos, totalMain: total, temCommitDeMerge: merge,
      commitsDoPRNaMain: tipo !== "squash", hashesNovos: tipo === "rebase"
    };
  };

  /* ====================== (b) vida de um PR ====================== */
  var FASES = { "nao-aberto": "ainda não aberto", draft: "rascunho (draft)", aberto: "aberto", revisao: "em revisão", mudancas: "mudanças pedidas", aprovado: "aprovado", mergeado: "mesclado" };
  GH.FASES = FASES;
  GH.pr = {};
  GH.pr.novo = function (regras) {
    regras = regras && typeof regras === "object" ? regras : {};
    return { fase: "nao-aberto", checks: "nenhum", conflito: false, aprovacoes: 0, branchApagada: false,
      regras: { aprovacao: regras.aprovacao === undefined ? true : GH.bool(regras.aprovacao), checks: regras.checks === undefined ? true : GH.bool(regras.checks), descartar: GH.bool(regras.descartar) } };
  };
  function clona(s) { return JSON.parse(JSON.stringify(s)); }

  /* motivos que impedem o merge agora (lista vazia = pode) */
  GH.pr.motivos = function (s) {
    var m = [];
    if (!s || typeof s !== "object") return ["Estado inválido."];
    if (s.fase === "nao-aberto") return ["O PR ainda não foi aberto."];
    if (s.fase === "mergeado") return ["O PR já foi mesclado."];
    if (s.fase === "draft") m.push("É um rascunho (draft): não pode ser mesclado até ser marcado como pronto.");
    if (s.conflito) m.push("Há conflito com a base: resolva antes.");
    /* Request changes só bloqueia o merge quando a regra de revisão exige (a página: "se a regra exigir"). */
    if (s.fase === "mudancas" && s.regras && s.regras.aprovacao) m.push("Há mudanças pedidas na revisão (Request changes) e a regra de revisão está ligada.");
    if (s.regras && s.regras.aprovacao && s.fase !== "aprovado" && s.fase !== "draft" && s.fase !== "mudancas") m.push("A regra exige aprovação e ainda não há.");
    if (s.regras && s.regras.aprovacao && s.fase === "draft") m.push("A regra exige aprovação (e o rascunho nem recebe revisão).");
    if (s.regras && s.regras.checks && s.checks !== "passou") m.push(s.checks === "falhou" ? "Um check obrigatório falhou." : "Os checks obrigatórios ainda não passaram (" + (s.checks === "nenhum" ? "não rodaram" : "rodando") + ").");
    return m;
  };

  /* agir(estado, acao): devolve {ok, msg, estado}. Transição inválida => ok:false e o estado volta igual. */
  GH.pr.ACOES = ["abrir_draft", "abrir", "pronto", "pedir_revisao", "aprovar", "pedir_mudancas", "novo_commit", "checks_passam", "checks_falham", "gerar_conflito", "resolver_conflito", "merge", "apagar_branch"];
  GH.pr.agir = function (estado, acao) {
    var s = estado && typeof estado === "object" && estado.fase ? clona(estado) : GH.pr.novo();
    function nao(msg) { return { ok: false, msg: msg, estado: s }; }
    function sim(msg) { return { ok: true, msg: msg, estado: s }; }
    var f = s.fase;
    var aberta = f === "draft" || f === "aberto" || f === "revisao" || f === "mudancas" || f === "aprovado";
    switch (acao) {
      case "abrir_draft":
        if (f !== "nao-aberto") return nao("O PR já está aberto.");
        s.fase = "draft"; s.checks = "rodando"; return sim("PR aberto como rascunho. Os checks começaram a rodar.");
      case "abrir":
        if (f !== "nao-aberto") return nao("O PR já está aberto.");
        s.fase = "aberto"; s.checks = "rodando"; return sim("PR aberto. Os checks começaram a rodar.");
      case "pronto":
        if (f !== "draft") return nao(f === "nao-aberto" ? "Abra o PR primeiro." : "Só um rascunho pode ser marcado como pronto.");
        s.fase = "aberto"; return sim("Marcado como pronto para revisão.");
      case "pedir_revisao":
        if (f === "draft") return nao("Rascunho não recebe pedido de revisão: marque como pronto antes.");
        if (f !== "aberto") return nao(f === "nao-aberto" ? "Abra o PR primeiro." : "A revisão só é pedida num PR aberto, ainda sem revisão.");
        s.fase = "revisao"; return sim("Revisão pedida.");
      case "aprovar":
        if (f !== "revisao") return nao(f === "draft" ? "Rascunho não pode ser aprovado." : "Só dá para aprovar um PR que está em revisão.");
        s.fase = "aprovado"; s.aprovacoes = 1; return sim("PR aprovado (1 aprovação).");
      case "pedir_mudancas":
        if (f !== "revisao") return nao("Só dá para pedir mudanças num PR que está em revisão.");
        s.fase = "mudancas"; s.aprovacoes = 0; return sim(s.regras && s.regras.aprovacao ? "Mudanças pedidas. Com a regra de revisão ligada, o merge fica bloqueado até a pessoa autora responder com novos commits." : "Mudanças pedidas. Com a regra de revisão desligada, isso não bloqueia o merge nesta simulação (a página diz que bloqueia 'se a regra exigir'); confira no seu repositório.");
      case "novo_commit":
        if (!aberta) return nao(f === "mergeado" ? "O PR já foi mesclado." : "Abra o PR primeiro.");
        s.checks = "rodando";
        if (f === "mudancas") { s.fase = "revisao"; return sim("Novo commit: o PR volta para a revisão e os checks recomeçam."); }
        if (f === "aprovado" && s.regras.descartar) { s.fase = "revisao"; s.aprovacoes = 0; return sim("Novo commit: a regra descarta aprovações antigas, então o PR volta para a revisão."); }
        return sim("Novo commit: o PR se atualiza sozinho e os checks recomeçam.");
      case "checks_passam":
        if (!aberta) return nao("Não há checks rodando: o PR não está aberto.");
        if (s.checks !== "rodando") return nao(s.checks === "passou" ? "Os checks já passaram." : "Não há checks rodando agora. Faça um novo commit para rodar de novo.");
        s.checks = "passou"; return sim("Checks passaram.");
      case "checks_falham":
        if (!aberta) return nao("Não há checks rodando: o PR não está aberto.");
        if (s.checks !== "rodando") return nao("Não há checks rodando agora. Faça um novo commit para rodar de novo.");
        s.checks = "falhou"; return sim("Um check falhou. Corrija e faça um novo commit.");
      case "gerar_conflito":
        if (!aberta) return nao("Não há PR aberto para ter conflito.");
        if (s.conflito) return nao("O conflito já existe.");
        s.conflito = true; return sim("A base mudou na mesma linha: o PR agora tem conflito.");
      case "resolver_conflito":
        if (!s.conflito) return nao("Não há conflito para resolver.");
        s.conflito = false; s.checks = "rodando";
        if (f === "aprovado" && s.regras.descartar) { s.fase = "revisao"; s.aprovacoes = 0; return sim("Conflito resolvido (merge ou rebase da base na sua branch). Isso gera commit novo: a regra descarta aprovações antigas, então o PR volta para a revisão, e os checks recomeçam."); }
        return sim("Conflito resolvido (merge ou rebase da base na sua branch). Os checks recomeçam.");
      case "merge": {
        var m = GH.pr.motivos(s);
        if (m.length) return { ok: false, msg: "Merge recusado: " + m.join(" "), estado: s };
        s.fase = "mergeado"; return sim("Merge feito. A branch ainda existe: o passo 6 do GitHub Flow é apagá-la.");
      }
      case "apagar_branch":
        if (f !== "mergeado") return nao("Só se apaga a branch depois do merge.");
        if (s.branchApagada) return nao("A branch já foi apagada (o histórico do PR continua e ela pode ser restaurada, segundo a documentação).");
        s.branchApagada = true; return sim("Branch apagada.");
      default:
        return nao("Ação desconhecida.");
    }
  };

  /* ====================== (e) regras da main: este PR pode entrar? ====================== */
  GH.regras = function (c) {
    c = c && typeof c === "object" ? c : {};
    var minAprov = GH.inteiro(c.minAprov, 0, 3, 1);
    var aprov = GH.inteiro(c.aprov, 0, 5, 0);
    var checks = ["passou", "falhou", "rodando"].indexOf(c.checks) >= 0 ? c.checks : "rodando";
    var abertas = GH.inteiro(c.conversasAbertas, 0, 9, 0);
    var descartou = GH.bool(c.descartarAntigas) && GH.bool(c.novoCommitDepois);
    var efetivas = descartou ? 0 : aprov;
    var ownerOk = GH.bool(c.ownerAprovou) && !descartou; /* a aprovação do code owner também é descartada */
    var m = [];
    if (efetivas < minAprov) m.push("Faltam aprovações: a regra pede " + minAprov + " e valem " + efetivas + (efetivas !== aprov ? " (as " + aprov + " antigas foram descartadas pelo novo commit)" : "") + ".");
    if (GH.bool(c.checksObrig) && checks !== "passou") m.push(checks === "falhou" ? "Um check obrigatório falhou." : "Os checks obrigatórios ainda estão rodando.");
    if (GH.bool(c.conversasObrig) && abertas > 0) m.push("Há " + abertas + " conversa" + (abertas > 1 ? "s" : "") + " não resolvida" + (abertas > 1 ? "s" : "") + ".");
    if (GH.bool(c.ownersObrig) && !ownerOk) m.push("Falta a aprovação de quem é dono (CODEOWNERS) dos arquivos alterados" + (GH.bool(c.ownerAprovou) && descartou ? " (a aprovação dele foi descartada pelo novo commit)" : "") + ".");
    var admin = GH.bool(c.admin), semBypass = GH.bool(c.semBypass);
    var bypass = m.length > 0 && admin && !semBypass;
    return { liberado: m.length === 0 || bypass, bypass: bypass, motivos: m, aprovEfetivas: efetivas, ownerEfetivo: ownerOk,
      nota: bypass ? "Liberado só porque administradores escapam da regra por padrão. Ligue 'não permitir bypass' para a regra valer para todos." : (m.length && admin && semBypass ? "Mesmo sendo administrador, a opção de não permitir bypass está ligada: a regra vale." : "") };
  };

  /* ====================== (d) fork e upstream ====================== */
  GH.fork = {};
  GH.fork.MAX = 9;
  GH.fork.novo = function () {
    return { forkFeito: false, clonado: false, upstreamRemoto: false, up: 3, origin: 0, local: 0, visto: null,
      branch: false, commitsBranch: 0, enviados: 0, pr: false };
  };
  GH.fork.atras = function (s) { return s && s.forkFeito ? Math.max(0, s.up - s.origin) : null; };
  GH.fork.ACOES = ["fork", "clonar", "add_upstream", "dono_publica", "fetch_upstream", "merge_upstream", "push_main", "criar_branch", "commit_branch", "enviar_branch", "abrir_pr"];
  GH.fork.agir = function (estado, acao) {
    var s = estado && typeof estado === "object" && typeof estado.up === "number" ? clona(estado) : GH.fork.novo();
    function nao(msg) { return { ok: false, msg: msg, estado: s }; }
    function sim(msg) { return { ok: true, msg: msg, estado: s }; }
    switch (acao) {
      case "fork":
        if (s.forkFeito) return nao("Você já fez o fork.");
        s.forkFeito = true; s.origin = s.up; return sim("Fork feito: uma cópia do original na sua conta, com " + s.up + " commits na main.");
      case "clonar":
        if (!s.forkFeito) return nao("Faça o fork antes: sem ele, você clonaria o original e não teria permissão de escrita.");
        if (s.clonado) return nao("Você já clonou.");
        s.clonado = true; s.local = s.origin; return sim("Clone do seu fork. O origin aponta para o seu fork.");
      case "add_upstream":
        if (!s.clonado) return nao("Clone o fork antes.");
        if (s.upstreamRemoto) return nao("O remoto upstream já existe.");
        s.upstreamRemoto = true; return sim("git remote add upstream: agora existe um segundo remoto, o original.");
      case "dono_publica":
        if (s.up >= GH.fork.MAX) return nao("O original já tem " + GH.fork.MAX + " commits nesta simulação.");
        s.up += 1; return sim("O dono do original publicou um commit. O original agora tem " + s.up + " commits." + (s.forkFeito ? " O seu fork ficou " + GH.fork.atras(s) + " atrás." : ""));
      case "fetch_upstream":
        if (!s.upstreamRemoto) return nao("Não existe o remoto upstream. Rode git remote add upstream primeiro.");
        s.visto = s.up; return sim("git fetch upstream: o seu computador agora sabe que o original tem " + s.up + " commits. Seus arquivos não mudaram.");
      case "merge_upstream":
        if (!s.upstreamRemoto) return nao("Não existe o remoto upstream.");
        if (s.visto === null) return nao("Faça git fetch upstream antes: o merge usa o que o fetch trouxe.");
        if (s.visto <= s.local) return nao("Nada para integrar: a sua main já tem tudo o que o upstream/main tem (faça um novo fetch se o dono publicou algo).");
        s.local = s.visto; return sim("git merge upstream/main: a sua main local foi para " + s.local + " commits.");
      case "push_main":
        if (!s.clonado) return nao("Clone o fork antes.");
        if (s.local <= s.origin) return nao("Nada para enviar: o seu fork já está igual ou à frente da sua main local.");
        s.origin = s.local; return sim("git push origin main: o seu fork foi para " + s.origin + " commits e agora está " + GH.fork.atras(s) + " atrás do original.");
      case "criar_branch":
        if (!s.clonado) return nao("Clone o fork antes.");
        if (s.branch) return nao("A branch de trabalho já existe.");
        s.branch = true; return sim("git switch -c fix/typo, a partir da sua main de " + s.local + " commits.");
      case "commit_branch":
        if (!s.branch) return nao("Crie a branch antes: commit direto na main do fork dificulta sincronizar depois.");
        if (s.commitsBranch >= 5) return nao("A simulação limita a branch a 5 commits.");
        s.commitsBranch += 1; return sim("Commit na branch (" + s.commitsBranch + " no total). Ainda só no seu computador.");
      case "enviar_branch":
        if (!s.branch) return nao("Crie a branch antes.");
        if (s.commitsBranch === 0) return nao("A branch ainda não tem commits para enviar.");
        if (s.enviados === s.commitsBranch) return nao("A branch já foi enviada, sem commits novos.");
        s.enviados = s.commitsBranch; return sim("git push -u origin fix/typo: a branch agora existe no seu fork com " + s.enviados + " commit(s).");
      case "abrir_pr":
        if (!s.branch || s.enviados === 0) return nao("O PR sai de uma branch que existe no seu fork. Envie a branch com git push antes.");
        if (s.pr) return nao("O PR já está aberto.");
        s.pr = true; return sim("PR aberto do seu fork (fix/typo) para a main do original." + (s.enviados < s.commitsBranch ? " Atenção: há commits locais que ainda não foram enviados e não aparecem no PR." : ""));
      default:
        return nao("Ação desconhecida.");
    }
  };

  /* ====================== (c) vazou um segredo ====================== */
  GH.vazou = {};
  GH.vazou.TIPOS = { token_gh: "Token de acesso do GitHub", chave_api: "Chave de API de outro serviço", senha: "Senha", ssh_privada: "Chave privada SSH", dado_pessoal: "Dado pessoal (CPF, dados de cliente, saúde...)" };
  var REVOGAR = {
    token_gh: "Revogue o token nas configurações da sua conta (a documentação diz que dá para revogar a qualquer momento) e gere outro com validade e permissões mínimas. Token enviado a repositório público é revogado automaticamente, mas troque mesmo assim.",
    chave_api: "Revogue ou rotacione a chave no painel do serviço que a emitiu e crie outra com o menor privilégio possível.",
    senha: "Troque a senha no serviço e em todo lugar onde ela se repetia, e ligue a verificação em duas etapas.",
    ssh_privada: "Remova a chave pública correspondente da sua conta e dos servidores onde ela entrava, e gere um par novo. A privada vazada nunca mais deve ser usada.",
    dado_pessoal: "Dado pessoal não se revoga. Remova as cópias que você controla, avise a pessoa responsável pelo projeto e quem foi afetado, e peça ao suporte do GitHub a remoção das cópias que o histórico limpo não alcança."
  };
  GH.vazou.plano = function (c) {
    c = c && typeof c === "object" ? c : {};
    if (!GH.vazou.TIPOS[c.tipo] || ["publico", "privado"].indexOf(c.visibilidade) < 0 || ["sim", "nao"].indexOf(c.enviado) < 0) return { pendente: true, passos: [], aviso: "Responda as três perguntas para ver o plano." };
    var passos = [], pub = c.visibilidade === "publico";
    if (c.enviado === "nao") {
      passos.push({ n: 1, t: "Tire o segredo do commit local, antes do push", d: "O valor ainda só existe no seu computador: ajuste o commit (por exemplo, <code>git commit --amend</code> ou <code>git reset --soft HEAD~1</code>) e ponha o arquivo no <code>.gitignore</code>. Minha recomendação: se houver qualquer dúvida de que o valor saiu da sua máquina (chat, print, outro push), trate como vazado e siga o plano de quem já enviou." });
      passos.push({ n: 2, t: "Guarde o valor fora do repositório", d: "Variável de ambiente ou cofre de senhas. No repositório, só um modelo sem valores." });
      return { pendente: false, passos: passos, aviso: "Como o commit nunca foi enviado, o caso é bem mais simples. Mesmo assim, não confie só na memória: confira com <code>git log -p</code> se o valor não ficou em outro commit local.", erroComum: "Fazer o push primeiro “para ver se passa” e só depois tentar remover." };
    }
    passos.push({ n: 1, t: "Revogar ou rotacionar agora", d: REVOGAR[c.tipo], obrig: true });
    passos.push({ n: 2, t: "Verificar se alguém usou", d: c.tipo === "dado_pessoal" ? "Veja quem teve acesso ao repositório e por quanto tempo esteve visível." : "Olhe o registro de acesso do serviço da credencial, se ele tiver." });
    passos.push({ n: 3, t: "Guardar a nova credencial fora do código", d: c.tipo === "dado_pessoal" ? "Dados pessoais não pertencem ao repositório: mantenha-os fora e ponha o caminho no <code>.gitignore</code>." : "Variável de ambiente ou cofre de senhas, nunca no repositório. O arquivo local vai para o <code>.gitignore</code>." });
    var pessoalPub = c.tipo === "dado_pessoal" && pub;
    passos.push({ n: 4, t: "Avisar quem tem clone antigo, antes de reescrever", d: "Um <code>git pull</code> seguido de <code>git push</code> pode reintroduzir o dado, e reescrever o histórico muda os hashes de todo mundo. Avise o time antes de limpar." });
    passos.push({ n: 5, t: pessoalPub ? "Limpar o histórico (neste caso não é opcional)" : "Se quiser, limpar o histórico (opcional)",
      d: (pessoalPub ? "Dado pessoal em repositório público: o dado não se revoga, então tirar do histórico faz parte da resposta (depois de remover as cópias que você controla e de avisar). " : "") +
        "Faça num <b>clone novo</b>, com um <b>backup</b> antes. Use <code>git filter-repo</code> (a documentação cita a versão 2.47 ou superior) e depois <code>git push --force --mirror origin</code>, que reescreve <b>todas as refs</b> (branches e tags) e tem riscos; não testei esses comandos. " +
        (pub ? "Em repositório público, limpar <b>não basta</b>: clones, forks, caches e PRs que citam o commit continuam com o dado, e remover de vez exige acionar o suporte do GitHub." : "Em repositório privado, menos gente vê, mas quem tem acesso já pode ter copiado, e limpar não alcança clones nem caches.") });
    return { pendente: false, passos: passos, aviso: pub ? "Repositório público: trate o valor como já copiado por alguém." : "Repositório privado: o risco é menor, mas o tratamento é o mesmo.", erroComum: "Apagar o arquivo ou o commit (ou rodar <code>git rm --cached</code>) e achar que resolveu: o valor continua no histórico e na cópia de quem já baixou. Só o passo 1 impede o uso." };
  };

  GH.vazou.ACOES = { apagar_commit: "Apagar o arquivo / o commit", rm_cached: "git rm --cached + .gitignore", revogar: "Revogar ou rotacionar a credencial", verificar_uso: "Verificar o log de acesso", guardar_novo: "Guardar a nova fora do código", limpar_historico: "Limpar o histórico (filter-repo)", avisar_time: "Avisar quem tem clone antigo" };
  /* feitas: lista de ações já feitas. Devolve {ok, nivel: bom|alerta|erro, msg}. */
  GH.vazou.avalia = function (acao, feitas) {
    if (!GH.vazou.ACOES[acao]) return { ok: false, nivel: "erro", msg: "Ação desconhecida." };
    feitas = Array.isArray(feitas) ? feitas : [];
    var rev = feitas.indexOf("revogar") >= 0;
    if (feitas.indexOf(acao) >= 0) return { ok: true, nivel: "alerta", msg: "Você já fez isto." };
    switch (acao) {
      case "revogar": return { ok: true, nivel: "bom", msg: "Certo. É o passo que impede o uso do segredo, e vem antes de qualquer limpeza." };
      case "apagar_commit": return rev ? { ok: true, nivel: "alerta", msg: "Como a credencial já foi revogada, apagar ajuda na higiene, mas o valor segue no histórico antigo e em quem já clonou." } : { ok: true, nivel: "erro", msg: "Este é o erro comum. Apagar o arquivo ou o commit não tira o valor do histórico nem de quem já baixou, e a credencial continua valendo. Revogue primeiro." };
      case "rm_cached": return rev ? { ok: true, nivel: "alerta", msg: "Evita um novo vazamento, mas o valor antigo segue no histórico. Como já revogou, o risco caiu." } : { ok: true, nivel: "erro", msg: "O <code>git rm --cached</code> só tira o arquivo dos próximos commits: o commit antigo mantém o valor (eu rodei e o <code>git show</code> o imprimiu). A credencial continua valendo: revogue primeiro." };
      case "limpar_historico": return rev ? { ok: true, nivel: "alerta", msg: "Arriscado: reescreve o histórico e exige push forçado. Faça num clone novo, com backup, depois de avisar o time. Não alcança clones, forks e caches." } : { ok: true, nivel: "erro", msg: "Limpar o histórico antes de revogar não impede ninguém de usar a credencial. Revogue primeiro." };
      case "verificar_uso": return rev ? { ok: true, nivel: "bom", msg: "Certo: depois de revogar, veja se houve uso no registro de acesso." } : { ok: true, nivel: "alerta", msg: "Vale verificar, mas enquanto a credencial não for revogada ela pode ser usada de novo. Revogue primeiro." };
      case "guardar_novo": return rev ? { ok: true, nivel: "bom", msg: "Certo: a nova fica em variável de ambiente ou cofre, nunca no repositório." } : { ok: true, nivel: "alerta", msg: "Ainda não existe credencial nova: revogue ou rotacione a antiga primeiro." };
      default: return rev ? { ok: true, nivel: "bom", msg: "Certo. Um clone antigo pode reintroduzir o dado com pull e push, por isso o aviso, de preferência antes de reescrever o histórico." } : { ok: true, nivel: "alerta", msg: "Avisar o time é bom, mas a credencial continua valendo: revogue ou rotacione primeiro, depois avise." };
    }
  };

  /* ====================== estilo ====================== */
  GH.estilo = function () {
    if (typeof document === "undefined" || document.getElementById("gh-estilo")) return;
    var st = document.createElement("style"); st.id = "gh-estilo";
    st.textContent =
      ".ghform{display:grid;gap:8px 12px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));margin:8px 0}" +
      ".ghform label{display:grid;gap:3px;font-size:.86rem;font-weight:600;min-width:0}" +
      ".ghform input,.ghform select{width:100%;box-sizing:border-box;font:.85rem var(--f-mono);padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}" +
      ".ghform label.ck{display:flex;gap:8px;align-items:center;font-weight:500}.ghform label.ck input{width:auto}" +
      ".ghbox{border:1px solid var(--line);border-radius:10px;background:var(--paper-2);padding:10px 12px;margin:8px 0;font:.82rem/1.5 var(--f-mono);white-space:pre;overflow-x:auto;min-height:60px}" +
      ".ghmsg{border:2px solid var(--line);border-radius:12px;background:var(--card);padding:8px 12px;margin:8px 0;font-size:.9rem;min-height:2.6em}" +
      ".ghmsg.ok{border-color:var(--green)}.ghmsg.no{border-color:var(--red);background:var(--red-soft)}" +
      ".ghfases{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}" +
      ".ghfases .f{flex:1 1 90px;min-width:0;border:2px solid var(--line);border-radius:10px;padding:5px 8px;font-size:.78rem;text-align:center;background:var(--card);opacity:.6}" +
      ".ghfases .f.on{opacity:1;border-color:var(--pen);font-weight:700}.ghfases .f.fim{border-color:var(--green)}" +
      ".ghnos{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}" +
      ".ghno{flex:1 1 150px;min-width:0;border:2px solid var(--line);border-radius:12px;padding:8px 10px;background:var(--card);font-size:.85rem}" +
      ".ghno b{display:block;margin-bottom:2px}.ghno .n{font:700 1.4rem var(--f-mono)}" +
      ".ghno.atras{border-color:var(--amber);background:var(--amber-soft)}.ghno.ok{border-color:var(--green)}" +
      ".ghpasso{border:2px solid var(--line);border-radius:12px;background:var(--card);padding:8px 12px;margin:6px 0;font-size:.88rem}" +
      ".ghpasso.obrig{border-color:var(--green)}.ghpasso .t{font-weight:700}" +
      ".ghlog{margin:6px 0;font-size:.88rem}.ghlog div{padding:4px 8px;border-left:4px solid var(--line);margin:3px 0}" +
      ".ghlog .bom{border-color:var(--green)}.ghlog .alerta{border-color:var(--amber)}.ghlog .erro{border-color:var(--red)}" +
      ".ghcmp{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin:8px 0;font-size:.85rem}" +
      ".ghcmp div{border:1px solid var(--line);border-radius:10px;padding:6px 10px;background:var(--card)}" +
      ".demo[data-demo=mergeSim]{min-height:460px}.demo[data-demo=prFluxo]{min-height:420px}.demo[data-demo=forkSim]{min-height:380px}.demo[data-demo=regrasMain]{min-height:420px}.demo[data-demo=vazouSegredo]{min-height:480px}";
    document.head.appendChild(st);
  };
  if (typeof module !== "undefined" && module.exports) module.exports = GH;
})();
