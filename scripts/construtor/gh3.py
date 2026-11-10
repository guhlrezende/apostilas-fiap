from gh_base import *

S7 = ["demos/gh-core.js", "demos/cap-7.js"]
S9 = ["demos/gh-core.js", "demos/cap-9.js"]


def cap7():
    corpo = ""
    corpo += secao("por-que", 1, "Por que não commitar direto na main em equipe",
        "Se eu confio nas pessoas do time, por que trancar a main?",
        camada("Intuição", "A main é o que todo mundo usa e o que vai para o ar. Um erro nela vira problema de todos na hora, sem ninguém ter olhado. Trancar a porta não é desconfiar de ninguém: é garantir que <b>uma segunda pessoa e os testes</b> passem antes.") +
        camada("Definição", "Com proteção, a main só recebe mudança por PR aprovado e com checks passando. A página de branches protegidas diz que as regras podem <b>bloquear o merge</b> quando os requisitos não são atendidos. (GitHub Docs, lida em 10/11/2026.)") +
        ex("uma analogia local: um remoto que recusa push direto na main", [
            "Como eu não podia ligar a proteção do GitHub, montei <b>uma analogia</b>: um repositório bare com um hook <code>pre-receive</code> que recusa pushes na <code>main</code> depois do primeiro. Não é a mesma coisa que a proteção do GitHub, mas mostra a ideia de um servidor que diz não.",
            "O primeiro push da <code>main</code> passou (era a criação). O segundo, direto na main, foi <b>recusado</b> com <code>pre-receive hook declined</code>.",
            "O push de uma branch <code>feature/ok</code> passou normalmente: o caminho do trabalho é a branch, e a main só muda depois (pelo PR).",
        ]) +
        code('''
$ git push origin main                       # segundo push direto na main
remote: main protegida: abra um pull request
To ../prot.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to '../prot.git'
$ git switch -c feature/ok ; git push -u origin feature/ok     # a branch passa
 * [new branch]      feature/ok -> feature/ok
$ git branch -vv
* feature/ok 5eea15b [origin/feature/ok] c2
  main       5eea15b [origin/main: ahead 1] c2
''') +
        SAIDA_PROT +
        naotestado("A proteção de verdade do GitHub eu não testei. O hook acima é só uma analogia de um servidor que recusa o push, e a mensagem do GitHub é diferente.") +
        erro("Achar que proteção resolve tudo. Ela só <b>obriga o processo</b>: quem aprova ainda precisa olhar o código. E liberar sempre o bypass para administradores: anula a regra."),
        ponte("A ideia está clara. Que regras existem, exatamente, e quem as configura?", "Proteção de branch clássica e rulesets."))

    corpo += secao("regras", 2, "Proteção de branch e rulesets",
        "Quais as travas que posso ligar na main, e quais valem em qualquer plano?",
        camada("Intuição", "Cada regra é uma tranca separada: exigir PR, exigir uma aprovação, exigir testes verdes, exigir conversas resolvidas, impedir force push. Você liga as que fazem sentido para o time.") +
        camada("Definição", "A página de branches protegidas (lida em 10/11/2026) lista: exigir PR antes do merge, com número mínimo de aprovações (revisores com permissão de escrita ou code owners); <b>Request changes</b> bloqueia o merge até ser resolvido; descartar aprovações antigas quando novos commits mudam o diff; <b>status checks obrigatórios</b> (modo <i>strict</i> exige a branch atualizada com a base, o <i>loose</i> não exige); exigir aprovação de code owners; exigir conversas resolvidas; <b>force push</b> e <b>exclusão da branch</b> bloqueados por padrão. Por padrão, as regras <b>não valem para administradores</b>; existe a opção “Do not allow bypassing the above settings”. <b>Rulesets</b> são listas nomeadas de regras para branches e tags: vários podem valer ao mesmo tempo, dá para desativar sem apagar, quem tem leitura vê os ativos e, em conflito, vale a mais restritiva; também controlam mensagem de commit e e-mail do autor, e o limite citado é 75 rulesets por repositório e por organização.") +
        '<div class="nota cuidado"><span class="lbl">Disponibilidade por plano: confira</span>A página de rulesets diz que estão nos planos Team e Enterprise. A página de planos não os lista para conta pessoal Free ou Pro. A página de proteção que reli em 10/11/2026 só menciona plano para duas funções: <b>restringir quem pode dar push</b> (em repositórios públicos de uma organização Free e em todos os de organizações Team ou Enterprise Cloud) e <b>listas de bypass</b> (só em repositórios de organização). Ela <b>não diz</b> se a proteção clássica ou os rulesets funcionam num repositório pessoal gratuito, e eu não testei. Antes de contar com uma regra, olhe a tela de configuração do <b>seu</b> repositório e a página de planos.</div>' +
        '<div class="demo" data-demo="regrasMain"></div>' +
        ex("lendo a demo", [
            "Com as regras iniciais (1 aprovação, checks obrigatórios, conversas resolvidas) e o PR sem aprovação, o veredito é <b>bloqueado</b>, com a lista do que falta.",
            "Aprove, faça os checks passarem e resolva as conversas: o veredito vira <b>liberado</b>.",
            "Ligue “aprovação antiga é descartada com novo commit”, marque que houve um novo commit e a aprovação some: bloqueado de novo.",
            "Marque “sou administrador” com a regra “não permitir bypass” desligada: o merge é liberado mesmo sem cumprir as regras (a página diz que, por padrão, a regra não vale para admin). Ligue o “não permitir bypass” e ele volta a bloquear.",
        ]) +
        naotestado("A demo aplica as regras como a documentação as descreve. Eu não ativei proteção nem ruleset em nenhum repositório real, e o comportamento exato (por exemplo, se o autor pode aprovar o próprio PR) depende da configuração: <b>confira</b>.") +
        erro("Exigir um check com nome que não existe mais: o PR fica esperando para sempre. E exigir aprovação de uma só pessoa no time de uma pessoa: ninguém consegue fazer merge."),
        ponte("Quem deve revisar o quê? Dá para o GitHub pedir a revisão certa sozinho?", "Com o CODEOWNERS."))

    corpo += secao("codeowners", 3, "CODEOWNERS: quem é dono de cada pedaço",
        "O time tem uma pessoa que cuida do front e outra do banco. Como o GitHub pede revisão a quem entende?",
        camada("Intuição", "É uma tabela “pasta, dono” na porta do arquivo. Quando um PR mexe numa pasta, o GitHub chama quem aparece como dono dela.") +
        camada("Definição", "O arquivo <code>CODEOWNERS</code> fica em <code>.github/</code>, na raiz ou em <code>docs/</code> (usa o primeiro que achar) e <b>precisa estar na branch base do PR</b> para pedir revisão. Até 3 MB. A sintaxe parece a do <code>.gitignore</code>, mas <b>sem</b> <code>!</code>, sem intervalo <code>[ ]</code> e sem escapar <code>#</code>. Vários donos na mesma linha; <b>vence a última regra que casa</b> com o caminho, então as gerais (<code>*</code>) vão no começo e as específicas embaixo. Os donos precisam ter <b>permissão de escrita explícita</b> no repositório. Um PR em draft não pede revisão automática a code owners. (GitHub Docs, lido em 10/11/2026.)") +
        code('''
# .github/CODEOWNERS  (exemplo ilustrativo, NAO testado aqui)
*           @seu-usuario              # regra geral, no comeco
/docs/      @seu-usuario
*.yml       @seu-usuario              # a ultima regra que casa vence
''') +
        naotestado("O CODEOWNERS não foi testado: ele depende do site para pedir a revisão. O exemplo usa um nome de usuário de mentira.") +
        erro("Colocar no CODEOWNERS um usuário sem permissão de escrita: a regra não pega e ninguém é avisado. Ou pôr uma regra geral <b>no fim</b> do arquivo, que passa por cima de todas as específicas (a última que casa vence)."),
        ponte("A main está protegida e a revisão tem dono. E as tarefas repetitivas, quem faz?", "As Actions."))

    corpo += aviso_lab() + lab("cap7", "proteger a main do seu repositório de treino",
        "Primeira metade do exercício 8. Se o seu plano não oferecer a opção, a própria tela diz; anote o que viu (<b>confira</b>).",
        ["Nas configurações do <code>treino-github</code>, procure a proteção de branch ou os rulesets para a <code>main</code>. Anote se a opção está disponível no seu plano (não suponha).",
         "Se estiver, ative: exigir PR antes do merge, exigir conversas resolvidas e bloquear force push. Se houver revisor obrigatório, perceba o efeito num repositório de uma pessoa só.",
         "Tente dar um <b>push direto na main</b> de um commit de teste e leia a mensagem de recusa. Anote a frase exata.",
         "Crie um <code>.github/CODEOWNERS</code> com você como dona ou dono, em uma branch, e abra um PR: veja se a revisão é pedida a você (você precisa ter permissão de escrita). <b>Pode não acontecer</b>: a documentação que li não diz o que ocorre quando o PR é do próprio dono do arquivo; anote o que viu.",
         "Prova de que deu certo: o push direto foi <b>recusado</b>, o mesmo commit passou por branch + PR, e você sabe dizer, com a frase da tela, qual regra segurou o push."])

    fim = fechamento(4,
        ["Proteger a main = obrigar PR, revisão e checks antes do merge. É processo, não confiança.",
         "Regras clássicas: PR obrigatório, número de aprovações, descartar aprovação antiga, checks obrigatórios (strict ou loose), code owners, conversas resolvidas, sem force push, sem apagar a branch. <b>Admin escapa por padrão</b>.",
         "<b>Rulesets</b>: vários ao mesmo tempo, dá para desativar, vale a mais restritiva. <b>Disponibilidade por plano: confira</b> (a página lida não fecha o caso do repositório pessoal gratuito).",
         "<b>CODEOWNERS</b>: <code>.github/</code>, raiz ou <code>docs/</code>; na branch base; última regra que casa vence; donos com permissão de escrita.",
         "Hook <code>pre-receive</code> local: analogia de servidor que recusa push, não é o GitHub."],
        [quiz(1, "c", "No CODEOWNERS há <code>*.yml @a</code> e, depois, <code>*.yml @b</code>. Quem é o dono dos arquivos <code>.yml</code>?", [("a", "@a, a primeira."), ("b", "Os dois ao mesmo tempo."), ("c", "@b: vence a última regra que casa.")], "Segundo a página de code owners, em linhas separadas só a última vale. Para vários donos, ponha todos na mesma linha."),
         quiz(2, "b", "Um administrador consegue fazer merge sem cumprir as regras?", [("a", "Nunca."), ("b", "Por padrão, sim: as regras não valem para administradores, a menos que se ative a opção de não permitir bypass."), ("c", "Só em repositório privado.")], "É o que a página de branches protegidas diz. A demo do capítulo mostra os dois casos."),
         quiz(3, "a", "A frase certa sobre rulesets em repositório pessoal gratuito é…", [("a", "A documentação que li não fecha o caso, então confiro na tela e na página de planos."), ("b", "Sempre estão disponíveis."), ("c", "Nunca estão disponíveis.")], "A página de rulesets cita Team e Enterprise; a de planos não os lista para Free ou Pro. Por isso o texto diz confira."),
         quiz(4, "b", "No PR da demo, a regra de checks obrigatórios está ligada e os checks ainda estão rodando. O veredito?", [("a", "Liberado."), ("b", "Bloqueado: faltam os checks passarem."), ("c", "Depende da cor do botão.")], "Check obrigatório que não passou bloqueia o merge.")],
        [("Por que não commitar direto na main?", "Um erro vai para o código de todos sem revisão nem teste. A proteção obriga o processo."),
         ("Qual a diferença entre strict e loose nos checks?", "Strict exige a branch atualizada com a base; loose não exige."),
         ("O que o CODEOWNERS precisa para funcionar?", "Estar na branch base do PR, e os donos terem permissão de escrita."),
         ("Quem escapa da proteção por padrão?", "Administradores, a menos que se ative a opção de não permitir bypass.")],
        fontes("gh_protected", "gh_rulesets", "gh_owners", "gh_planos", "gh_reviews"),
        prox=(8, "Quem faz as tarefas repetitivas?", "GitHub Actions, Pages e releases."))
    publicar(7, "proteger-a-main", "Proteger a main: proteção de branch, rulesets e CODEOWNERS",
             "Por que trancar a main em equipe, quais travas existem e como saber, em cada caso, se um PR pode entrar.",
             "No capítulo 6 você contribuiu sem esbarrar em ninguém. A pergunta que ficou: <b>em equipe, o que impede alguém de quebrar a main?</b>",
             corpo + fim, 40, S7)


def cap8():
    corpo = ""
    corpo += secao("actions", 1, "Actions: um workflow em YAML",
        "Todo PR eu rodo os testes à mão. Dá para o GitHub fazer isso sozinho, sempre igual?",
        camada("Intuição", "É um robô de plantão. Você escreve uma receita (“quando alguém fizer push, rode isto numa máquina limpa”) e o GitHub executa toda vez, igual, e mostra se passou.") +
        camada("Definição", "Um <b>workflow</b> é um arquivo YAML em <code>.github/workflows/</code> (extensão <code>.yml</code> ou <code>.yaml</code>). Ele diz <b>quando</b> rodar (<code>on</code>), em <b>qual máquina</b> (<code>runs-on</code>) e quais <b>passos</b> (<code>steps</code>). Roda na infraestrutura do GitHub. Gatilhos comuns: <code>push</code> (commits enviados, com filtro por branch, tag ou caminho), <code>pull_request</code> (atividade em PR, com filtros) e <code>workflow_dispatch</code> (disparo manual). O <code>schedule</code> (cron) aparece na minha referência geral, mas eu não li a página dele: <b>confira</b>. (GitHub Docs, lidos em 10/11/2026.)") +
        '<p>Um workflow mínimo, com <b>permissão mínima</b>. Conferi com um parser que o YAML é válido (1 job, 3 passos); <b>não rodei</b> no GitHub:</p>' +
        yaml_code('''
name: ci
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read          # o GITHUB_TOKEN so le o repositorio; eleve so o job que precisar
jobs:
  testar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6        # tag so por ser didatico; confira a versao atual
      - name: Ver os arquivos
        run: ls
      - name: Teste de exemplo
        run: echo "tudo certo"           # troque por npm test, pytest etc.
''') +
        naotestado("Não rodei nenhum workflow. Só validei que o YAML é um YAML válido. A versão <code>@v6</code> do <code>checkout</code> vem do exemplo oficial que li e eu <b>não</b> conferi se é a atual. O exemplo usa <b>tag</b> por ser didático, mas a lista da seção seguinte recomenda o SHA completo para actions de terceiros: confira a versão e fixe o SHA no uso real.") +
        '<p>Para ver o resultado depois, o <code>gh run</code> (flags lidas na ajuda real, não rodei contra o GitHub): <code>gh run list --branch main</code>, <code>gh run view ID --log-failed</code>, <code>gh run watch ID</code> e <code>gh run rerun ID</code>. Para ver a falha, faça um passo falhar de propósito, por exemplo <code>run: exit 1</code>, e leia o log.</p>' +
        erro("Colar um workflow da internet sem ler o que ele faz, ou subir a indentação errada do YAML. Valide sempre (o editor ajuda). E esquecer o <code>permissions</code>: aí o acesso do token depende do padrão do repositório ou da organização, que varia conforme a configuração (<b>confira</b>; a página de GITHUB_TOKEN que li não informa o padrão). Declare <code>permissions</code> para não depender dele."),
        ponte("O workflow roda. E quando ele precisa de uma senha, onde ela mora?", "Em secrets, nunca no YAML."))

    corpo += secao("secrets", 2, "Secrets, GITHUB_TOKEN e o que não fazer",
        "O deploy precisa de uma chave. Coloco no YAML, só para testar?",
        camada("Intuição", "O YAML vai para o repositório, e o repositório pode ser público. A chave fica no cofre do GitHub, e o workflow a pede por nome na hora de rodar, sem nunca aparecer no arquivo.") +
        camada("Definição", "<b>Secrets</b> são cadastrados nas configurações do repositório, em “Secrets and variables” e depois “Actions”, e nunca no YAML. Quem tem escrita no repositório consegue usá-los: use credencial de <b>menor privilégio</b>. Não use JSON, XML ou YAML como valor de um secret (a ocultação nos logs depende de texto exato): um secret por valor. Se um secret aparecer sem ocultação num log, apague o log e <b>rotacione</b> o secret. <i>Environments</i> com revisores obrigatórios protegem secrets de produção. O <b>GITHUB_TOKEN</b> é um token temporário do próprio workflow: dê só o que o job precisa com <code>permissions</code>, no workflow ou no job. E um ponto importante da página de gatilhos: <b>eventos criados com o GITHUB_TOKEN geralmente não iniciam novos workflows</b> (para evitar laços infinitos), com exceção de <code>workflow_dispatch</code> e <code>repository_dispatch</code>. (GitHub Docs, lidos em 10/11/2026.)") +
        yaml_code('''
jobs:
  publicar:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Usar o segredo sem imprimir
        env:
          CHAVE_DE_DEPLOY: ${{ secrets.CHAVE_DE_DEPLOY }}   # vem do cofre; nunca do repositorio
        run: ./publicar.sh                                    # o script le a variavel; ninguem faz echo dela
''') +
        '<h3>O que a página de segurança manda evitar</h3><ul>' +
        '<li><code>pull_request_target</code> ou <code>workflow_run</code> com checkout de <b>código de fork não confiável</b>: esses gatilhos rodam com privilégios e acesso a secrets, e a página diz que isso pode levar à tomada do repositório.</li>' +
        '<li>Usar <code>${{ github.event.pull_request.title }}</code> direto dentro de um <code>run:</code>: o texto vem de fora e pode ser um comando. Passe por variável de ambiente e use aspas.</li>' +
        '<li>Runner self-hosted em repositório público: qualquer pessoa pode abrir um PR.</li>' +
        '<li><code>issue_comment</code>: um workflow nesse gatilho também processa texto escrito por gente de fora (o comentário). Isso é uma ressalva minha, <b>não lida na página</b> de segurança: confira antes de usar texto do comentário num <code>run:</code> ou de dar permissão ao token.</li>' +
        '<li>Fixar uma action só pela tag, se você não confia no autor: prefira o SHA completo de 40 caracteres.</li></ul>' +
        naotestado("Não criei secrets nem rodei workflow. Eu não descrevo as telas de cadastro: siga a página oficial.") +
        erro("Imprimir o secret num <code>echo</code> para “conferir”. Pode vazar no log. E dar a um token mais permissão do que o job usa: se a ação for comprometida, o estrago cresce."),
        ponte("Automatizei os testes. E publicar uma página e marcar versões?", "Pages, tags e releases."))

    corpo += secao("pages-releases", 3, "Pages, tags, releases e versionamento",
        "Quero colocar um site no ar de graça e marcar a versão 1.0 do meu projeto. Como?",
        camada("Intuição", "Pages é uma vitrine automática: o GitHub pega os arquivos do site do seu repositório e os serve. A tag é uma etiqueta em um commit (“esta é a versão 1.0”). A release embrulha essa etiqueta com notas e arquivos para baixar.") +
        camada("Definição", "<b>Pages</b> hospeda site estático (HTML, CSS, JS) a partir de um repositório, podendo passar por um build. Há site de usuário ou organização (repositório <code>&lt;usuario&gt;.github.io</code>, um por conta) e site de projeto (um por repositório); o endereço padrão é <code>https://&lt;usuario&gt;.github.io</code> ou <code>https://&lt;usuario&gt;.github.io/&lt;repositorio&gt;</code>. A fonte de publicação pode ser <b>“Deploy from a branch”</b> (<b>uma</b> branch que você escolhe, publicando a raiz <code>/</code> ou a pasta <code>/docs</code>) ou <b>GitHub Actions</b> com um workflow seu. A página diz que o IP do visitante é registrado por segurança. <b>Tag</b> é um ponteiro com nome para um commit; <b>release</b> é o pacote que usa uma tag, com notas, arquivos e os zips automáticos. Toda release se baseia numa tag; a página cita até 1000 arquivos por release, cada um com menos de 2 GiB. (GitHub Docs, lidos em 10/11/2026.)") +
        '<h3>Versionamento semântico (SemVer 2.0.0)</h3>' +
        tabela(["Parte", "Quando sobe", "Exemplo de commit (Conventional Commits)"], [
            ["MAJOR", "muda a API de forma incompatível", "<code>feat!: remove o parametro antigo</code> ou rodapé <code>BREAKING CHANGE:</code>"],
            ["MINOR", "adiciona função compatível", "<code>feat: adiciona exportar em CSV</code>"],
            ["PATCH", "corrige bug de forma compatível", "<code>fix: corrige a media com nota zero</code>"],
        ]) +
        '<p>Versões <code>0.y.z</code> são a fase inicial (qualquer coisa pode mudar); <code>1.0.0</code> declara a API pública. Tipos como <code>docs</code>, <code>chore</code>, <code>refactor</code> e <code>test</code> são aceitos sem efeito na versão. O <i>Keep a Changelog</i> sugere um <code>CHANGELOG.md</code> com seções por versão (a mais recente primeiro) e as categorias Added, Changed, Deprecated, Removed, Fixed e Security, com uma seção “Não publicado” no topo.</p>' +
        ex("uma tag anotada, rodada de verdade", [
            "Num repositório de teste criei a tag anotada <code>v0.1.0</code> e fiz push dela para o remoto bare. O <code>git tag -n1</code> mostrou a mensagem e o <code>git ls-remote --tags origin</code> listou a tag no remoto.",
            "Depois de um commit novo, o <code>git describe --tags</code> respondeu <code>v0.1.0-1-gda5b4a8</code>: “1 commit depois da tag v0.1.0”. É uma forma de saber em que versão você está.",
            "A <b>release</b> pelo <code>gh release create</code> eu <b>não</b> criei: li só a ajuda (<code>--title</code>, <code>--notes</code>, <code>--notes-file</code>, <code>--generate-notes</code>, <code>--draft</code>, <code>--prerelease</code>, <code>--target</code>).",
        ]) +
        code('''
$ git tag -a v0.1.0 -m "Primeira versao demo"
$ git push -q origin v0.1.0
$ git tag -n1
v0.1.0          Primeira versao demo
$ git ls-remote --tags origin | cut -c42-
refs/tags/v0.1.0
refs/tags/v0.1.0^{}
$ git commit -qam "fix: corrige texto" ; git describe --tags
v0.1.0-1-gda5b4a8
$ gh release create v0.1.0 --title "v0.1.0" --notes-file CHANGELOG-trecho.md   # NAO rodei: criaria uma release
''') +
        SAIDA_TAGS +
        naotestado("Pages publicando e a criação de release (pelo site ou pelo <code>gh</code>) não foram testados. A fonte de publicação “branch ou Actions” vem da documentação; eu não vi a tela.") +
        erro("Apagar ou mover uma tag já publicada: quem usa aquela versão fica com algo diferente do que baixou. Publique uma versão nova (PATCH) em vez de trocar a velha. Outro: pôr nome de tag fora do SemVer e perder a ordem das versões."),
        ponte("Tenho automação, site e versões. E o maior risco de tudo isso: um segredo ou um erro irreversível. Como me proteger e me recuperar?", "Segurança e recuperação."))

    corpo += aviso_lab() + lab("cap8", "tag, release e Actions com permissão mínima",
        "Exercícios 6 e 7 da lista. Nada aqui pede segredo real.",
        ["<b>Tag e release.</b> Crie a tag anotada <code>v0.1.0</code> (<code>git tag -a v0.1.0 -m \"primeira versao\"</code>) e envie (<code>git push origin v0.1.0</code>). Escreva um trecho de notas no formato Keep a Changelog (<code>## [0.1.0]</code>, <code>### Added</code>).",
         "Publique a release com <code>gh release create v0.1.0 --title \"v0.1.0\" --notes-file notas.md</code>. Prova: a release aparece na lista de releases do repositório com as suas notas.",
         "Faça um commit <code>fix:</code> pequeno, crie a tag <code>v0.1.1</code> (um PATCH) e publique a release. Prova: <code>git tag -l \"v*\"</code> lista as duas.",
         "<b>Actions.</b> Crie <code>.github/workflows/ci.yml</code> com <code>permissions: contents: read</code> e um job com um <code>run: echo</code> (ou <code>npm test</code>, se tiver projeto). Valide o YAML no editor antes de enviar.",
         "Faça push e veja a execução: <code>gh run list</code> e <code>gh run view --log</code>. Prova: o job aparece como passou.",
         "Troque um passo por <code>run: exit 1</code>, envie de novo e leia o erro com <code>gh run view --log-failed</code>. Depois volte ao passo certo. Prova: você achou a linha do log em que o passo falhou."])

    fim = fechamento(4,
        ["Workflow = YAML em <code>.github/workflows/</code>: <code>on</code> (quando), <code>runs-on</code> (onde), <code>steps</code> (o quê). Gatilhos: <code>push</code>, <code>pull_request</code>, <code>workflow_dispatch</code>.",
         "<code>permissions: contents: read</code> como padrão; eleve só o job que precisa. <b>Secrets</b> nunca no YAML, nunca no <code>echo</code>.",
         "Eventos criados com o <b>GITHUB_TOKEN</b> geralmente <b>não disparam</b> novos workflows (exceto <code>workflow_dispatch</code> e <code>repository_dispatch</code>).",
         "Evite <code>pull_request_target</code> com código de fork, título de PR direto num <code>run:</code> e runner self-hosted em repositório público. Prefira SHA completo para actions de terceiros.",
         "<b>Pages</b>: site estático; fonte pode ser uma branch (raiz ou <code>/docs</code>) ou Actions. <b>Release</b> usa uma <b>tag</b>.",
         "<b>SemVer</b>: MAJOR (incompatível), MINOR (nova função compatível), PATCH (correção). <code>feat</code> ~ MINOR, <code>fix</code> ~ PATCH, <code>!</code> ou <code>BREAKING CHANGE</code> ~ MAJOR."],
        [quiz(1, "c", "Um workflow, usando o <code>GITHUB_TOKEN</code>, faz um push. Esse push dispara outro workflow?", [("a", "Sempre."), ("b", "Nunca, nem com <code>workflow_dispatch</code>."), ("c", "Geralmente não, para evitar laços; as exceções são <code>workflow_dispatch</code> e <code>repository_dispatch</code>.")], "É o que a página de gatilhos descreve."),
         quiz(2, "b", "Qual a versão seguinte a <code>1.4.2</code> se você só corrigiu um bug compatível?", [("a", "2.0.0"), ("b", "1.4.3"), ("c", "1.5.0")], "Correção compatível é PATCH. Função nova compatível seria 1.5.0; mudança incompatível, 2.0.0."),
         quiz(3, "a", "Onde o valor de um secret deve ficar?", [("a", "No cofre de secrets do repositório, e o YAML só cita o nome."), ("b", "No YAML, em comentário."), ("c", "No README.")], "O YAML vai para o repositório. O valor fica fora dele."),
         quiz(4, "c", "Por que não usar <code>${{ github.event.pull_request.title }}</code> direto dentro de um <code>run:</code>?", [("a", "Porque o título é muito grande."), ("b", "Porque o GitHub bloqueia."), ("c", "Porque o texto vem de fora e pode injetar comando; passe por variável de ambiente e use aspas.")], "É um dos itens da página de segurança de Actions.")],
        [("Para que serve o <code>permissions</code>?", "Limitar o que o GITHUB_TOKEN pode fazer. Comece em <code>contents: read</code>."),
         ("Tag x release?", "Tag é um ponteiro com nome para um commit; release é o pacote com notas e arquivos que usa uma tag."),
         ("O que o <code>git describe --tags</code> mostra?", "A tag mais próxima e quantos commits depois dela você está, como <code>v0.1.0-1-gda5b4a8</code>."),
         ("De onde o Pages publica?", "De uma branch (raiz ou <code>/docs</code>) ou de um workflow de Actions.")],
        fontes("gh_actions", "gh_trigger", "gh_actions_seg", "gh_gtoken", "gh_pages", "gh_pages_fonte", "gh_releases", "semver", "convcommits", "changelog"),
        prox=(9, "Como me protejo e me recupero?", "Segurança, gh, erros comuns e portfólio."))
    publicar(8, "actions-pages-releases", "Actions, Pages, releases e versionamento",
             "Automatizar testes, publicar um site e marcar versões sem expor segredo e sem acesso demais.",
             "No capítulo 7 você trancou a main. A pergunta que ficou: <b>as tarefas repetitivas (testar, publicar, versionar), quem faz?</b>",
             corpo + fim, 50)


def cap9():
    corpo = ""
    corpo += secao("scanning", 1, "Secret scanning, push protection e Dependabot",
        "O GitHub avisa sozinho quando eu subo uma chave por engano?",
        camada("Intuição", "É um vigia com lista de padrões: ele conhece o jeito de uma chave de API ou de um token e grita quando vê um igual num commit. O Dependabot é outro vigia, que olha as bibliotecas que o seu projeto usa e avisa quando alguma tem falha conhecida.") +
        camada("Definição", "<b>Secret scanning</b> procura credenciais (chaves de API, tokens, senhas) no histórico completo de todas as branches e também em issues, PRs, discussões, wikis e gists secretos. Em repositório <b>público</b>, roda automaticamente e de graça; em privado exige o GitHub Secret Protection (planos Team ou Enterprise Cloud, segundo a página). <b>Push protection</b> bloqueia o push de uma credencial detectada, vem ativado por padrão em repositório público, e se alguém contorna o bloqueio, gera um alerta. Credenciais de provedores parceiros são avisadas ao provedor quando o vazamento é público. <b>Dependabot</b>: alertas de vulnerabilidade em dependências, <i>security updates</i> (PR com a correção) e <i>version updates</i> (PR para manter dependências atualizadas, com um <code>.github/dependabot.yml</code> criado ao ativar). A página de segurança que li diz que esses três estão em todos os planos. (GitHub Docs, lido em 10/11/2026.) A página do guia rápido do Dependabot <b>não traz</b> o exemplo mínimo do arquivo (ela só diz que o GitHub cria um <code>dependabot.yml</code> em <code>/.github</code>), então o exemplo abaixo é <b>ilustrativo</b>: confira as opções na página de referência do Dependabot.") +
        yaml_code('''
# .github/dependabot.yml  (exemplo ILUSTRATIVO; confira a pagina de opcoes do Dependabot)
version: 2
updates:
  - package-ecosystem: "github-actions"   # mantem as actions do workflow atualizadas
    directory: "/"
    schedule:
      interval: "weekly"
''') +
        naotestado("Secret scanning, push protection e Dependabot não foram testados: dependem do site e de um repositório real. Não tente disparar um alerta com uma credencial verdadeira nem com o token de teste de um serviço: o sistema reconhece padrões reais.") +
        erro("Confiar só no scanner. Ele pega padrões conhecidos, e pega <b>depois</b> que o dado já foi enviado. A defesa é não pôr segredo no repositório em primeiro lugar."),
        ponte("Se mesmo assim o segredo foi para o repositório, qual é a ordem das coisas?", "Revogar primeiro. Vamos treinar a árvore de decisão."))

    corpo += secao("vazou", 2, "Vazou um segredo: a ordem certa",
        "Commitei uma chave. Apago o commit e acabou?",
        camada("Intuição", "É uma carta com a senha que você já postou. Rasgar o rascunho em casa não a tira da caixa do correio, e quem pegou a carta continua com a senha. O que fecha a porta é <b>trocar a fechadura</b> (revogar a chave), não esconder a carta.") +
        camada("Definição", "A ordem, segundo a página oficial de remoção de dados sensíveis e a de expiração de tokens (lidas em 10/11/2026): <b>1. revogar ou rotacionar</b> a credencial agora (é a única ação que impede o uso do segredo); <b>2.</b> verificar se alguém usou, nos logs do serviço; <b>3.</b> <b>avisar</b> quem tem clone antigo, antes de reescrever nada, porque um <code>git pull</code> seguido de <code>git push</code> pode reintroduzir o dado; <b>4.</b> só depois, se preciso, <b>limpar o histórico</b> com <code>git filter-repo</code> (a página cita versão mínima 2.47; exemplo da página: <code>git filter-repo --invert-paths --path ARQUIVO</code> e depois <code>git push --force --mirror origin</code>). Pré-condições (são minhas e de bom senso, <b>não testei</b> esses comandos): faça num <b>clone novo</b>, com um <b>backup</b> antes, e avise o time antes, porque o <code>--mirror</code> reescreve <b>todas as refs</b> (branches e tags) e muda os hashes de todo mundo; <b>5.</b> saber que limpar o histórico <b>não basta</b>: clones, forks, caches e PRs que citam o commit continuam com o dado, e remover de vez exige acionar o GitHub Support. Se o que vazou é <b>dado pessoal em repositório público</b>, a limpeza deixa de ser opcional (o dado não se revoga): a ordem é remover as cópias que você controla, avisar, limpar e acionar o suporte. A página de expiração diz que um token enviado a repositório público é revogado automaticamente, e mesmo assim você troca a credencial.") +
        '<div class="demo" data-demo="vazouSegredo"></div>' +
        ex("o segredo continua no histórico (rodado, com valor falso)", [
            "Criei um arquivo com o valor falso <code>CHAVE_FALSA_123</code>, fiz o commit “sem querer”, depois pus o arquivo no <code>.gitignore</code>, rodei <code>git rm --cached</code> e fiz um segundo commit. O <code>git status</code> ficou limpo e o <code>git ls-files</code> só lista o <code>.gitignore</code>: parece resolvido.",
            "O <code>git log --all --oneline -S CHAVE_FALSA_123</code> listou <b>2 commits</b> que mexeram nessa string, e o <code>git show HEAD~1:segredo.txt</code> imprimiu a chave. O valor segue legível no commit anterior.",
            "Moral: <code>git rm --cached</code> e <code>.gitignore</code> impedem o <b>próximo</b> vazamento. Só <b>revogar</b> impede o uso do que já vazou.",
        ]) +
        code('''
$ echo "CHAVE_FALSA_123" > segredo.txt ; git add . ; git commit -qm "sem querer"
$ printf 'segredo.txt
' > .gitignore ; git rm -q --cached segredo.txt     # Git Bash
$ git add .gitignore ; git commit -qm "tira do rastreio"
$ git status --short                       # vazio: parece que acabou
$ git ls-files
.gitignore
$ git log --all --oneline -S CHAVE_FALSA_123
386bd13 tira do rastreio
7433788 sem querer
$ git show HEAD~1:segredo.txt
CHAVE_FALSA_123                            # continua ali, no commit anterior
''') +
        SAIDA_LOCAL +
        '<p class="muted" style="font-size:.85rem">Os comandos acima são de <b>Git Bash</b>. No PowerShell 5.1, o <code>&gt;</code> pode gravar o <code>.gitignore</code> em UTF-16 e o segredo continuaria aparecendo no <code>git status</code> (vi isso numa rodada e o <a href="' + TG5 + '">capítulo 5 de Terminal e Git</a> (seção do <code>.gitignore</code>) mostra): lá, use <code>Set-Content -Encoding ascii</code>.</p>' +
        naotestado("Não rodei <code>git filter-repo</code>, nem <code>git push --force</code>, nem pedi nada ao GitHub Support. O que digo sobre limpar o histórico vem da página oficial; o que eu rodei foi a prova de que o histórico guarda o valor.") +
        erro("Rodar <code>git rm --cached</code>, ou apagar o commit, e considerar resolvido sem revogar. Quem clonou antes, um robô que varre repositórios públicos ou um fork continuam com a chave. <b>Sem o passo 1, a chave segue valendo.</b> E reescrever o histórico sem avisar o time pode atrapalhar todo mundo."),
        ponte("Sei lidar com o pior caso. E o dia a dia: como faço mais rápido, sem sair do terminal?", "Com o gh."))

    corpo += secao("gh", 3, "O gh no terminal",
        "Abrir o navegador para cada PR e cada issue cansa. Dá para fazer pelo terminal?",
        camada("Intuição", "O <code>gh</code> é o controle remoto do GitHub no seu terminal. Você faz ali o que faria nos botões do site.") +
        camada("Definição", "O <code>gh</code> é o GitHub CLI (<code>gh --version</code> na minha máquina: 2.101.0). Grupos principais do manual: <code>gh auth</code>, <code>gh repo</code>, <code>gh pr</code>, <code>gh issue</code>, <code>gh run</code>, <code>gh release</code> e <code>gh api</code>. A ajuda abaixo é <b>real</b>, rodada nesta máquina, sem chamar a API. O <code>gh auth status</code> mostra a conta e os escopos: não cole a saída em chat. E o <code>gh api</code> com <code>-X POST</code>, <code>PUT</code> ou <code>DELETE</code> <b>altera</b> o GitHub: não use sem saber o que vai mudar.") +
        tabela(["Grupo", "Subcomandos úteis (da ajuda real e do manual)"], [
            ["<code>gh pr</code>", "<code>create</code>, <code>list</code>, <code>status</code>, <code>checkout</code>, <code>checks</code>, <code>comment</code>, <code>diff</code>, <code>edit</code>, <code>merge</code>, <code>ready</code>, <code>review</code>, <code>view</code>"],
            ["<code>gh issue</code>", "<code>create</code>, <code>list</code>, <code>view</code>, <code>comment</code>, <code>close</code>"],
            ["<code>gh repo</code>", "<code>create</code>, <code>clone</code>, <code>fork</code>, <code>sync</code>, <code>view</code>, <code>edit</code>, <code>archive</code>, <code>delete</code>, <code>rename</code>"],
            ["<code>gh run</code>", "<code>list</code>, <code>view</code>, <code>watch</code>, <code>rerun</code>, <code>cancel</code>, <code>download</code>"],
            ["<code>gh release</code>", "<code>create</code>, <code>list</code>, <code>upload</code>, <code>download</code>, <code>view</code>"],
        ]) +
        code('''
$ gh pr merge --help | grep -E "^\\s+(-m|-s|-r|-d|--auto|--admin)"
      --admin                   Use administrator privileges to merge a pull request that does not meet requirements
      --auto                    Automatically merge only after necessary requirements are met
  -d, --delete-branch           Delete the local and remote branch after merge
  -m, --merge                   Merge the commits with the base branch
  -r, --rebase                  Rebase the commits onto the base branch
  -s, --squash                  Squash the commits into one commit and merge it into the base branch
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 10/11/2026. O <code>--admin</code> usa privilégio de administrador para mesclar sem cumprir requisitos: é a mesma ideia de bypass do capítulo 7, e deve ser exceção.</p>' +
        erro("Rodar <code>gh api</code> com POST, PUT ou DELETE copiado de um tutorial. Isso muda o seu GitHub de verdade. Rode primeiro um GET e leia o que vai mudar."),
        ponte("Sei o terminal. E quando eu errar, como me recupero?", "Uma tabela de erros comuns, todos rodados."))

    corpo += secao("erros", 4, "Erros comuns e como se recuperar",
        "Fiz besteira no Git. Perdi trabalho?",
        camada("Intuição", "O Git quase nunca perde nada de verdade: guarda um diário (o <code>reflog</code>) de onde a sua branch esteve. O que dá medo é a rapidez com que dá para errar; a recuperação costuma ser curta.") +
        camada("Definição", "Os erros abaixo eu reproduzi num repositório de teste, com saída real. As correções que reescrevem histórico ou descartam trabalho (<code>reset --hard</code>) <b>só</b> use quando tiver certeza de que nada se perde.") +
        tabela(["Erro", "Sintoma real", "Como me recuperei (rodado)"], [
            ["Commit direto na main", "<code>git status -sb</code>: <code>## main...origin/main [ahead 1]</code>", "<code>git branch feature/oops</code> guarda o commit; depois, só se tiver certeza, <code>git reset --hard origin/main</code> na main (<b>destrutivo</b>)"],
            ["Push rejeitado", "<code>error: failed to push some refs</code> e <code>Updates were rejected because the remote contains work that you do not have locally</code>", "<code>git fetch</code>, <code>git pull --no-rebase</code> (ou rebase) e push de novo"],
            ["Fast-forward impossível", "<code>fatal: Not possible to fast-forward, aborting.</code>", "escolher <code>git pull --no-rebase</code> (merge) ou <code>--rebase</code>; sem <code>--force</code>"],
            ["Apaguei uma branch sem merge", "<code>git branch -d</code> recusou: <code>is not fully merged</code>; com <code>-D</code> apagou", "<code>git reflog</code> mostra o último commit; <code>git branch recuperada &lt;hash&gt;</code>"],
            ["Revert de merge falha", "<code>is a merge but no -m option was given</code>", "<code>git revert -m 1 &lt;hash&gt;</code>"],
            ["Token ou chave no repositório", "o valor aparece no histórico", "revogar primeiro; depois a seção anterior"],
            ["Remoto apontando para o lugar errado", "<code>git remote -v</code> mostra o original", "<code>git remote set-url origin URL</code>"],
            ["<code>Permission denied (publickey)</code>", "ao dar push por SSH", "chave pública não cadastrada ou chave certa não carregada no <code>ssh-agent</code> (<code>ssh -T</code> com o GitHub: não testado aqui)"],
        ]) +
        code('''
$ git branch -d temp                           # branch nao mesclada: o Git recusa
error: the branch 'temp' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D temp'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
$ git branch -D temp
Deleted branch temp (was e3b370b).
$ git reflog | head -2 | cut -c1-60
3b8f833 HEAD@{0}: checkout: moving from temp to main
e3b370b HEAD@{1}: commit: feat: trabalho em temp
$ git branch recuperada e3b370b
$ git log --oneline recuperada | head -1
e3b370b feat: trabalho em temp                # o trabalho voltou
''') +
        SAIDA_ERROS +
        erro("Dar <code>git push --force</code> para “limpar” um push recusado. Isso apaga o trabalho de quem enviou antes. Use <code>--force</code> só em branch sua e que ninguém mais usa, e mesmo assim prefira <code>--force-with-lease</code> (que eu <b>não</b> testei aqui)."),
        ponte("Aprendi a me proteger e a me recuperar. O que mostrar para quem olha o meu perfil?", "Um perfil honesto."))

    corpo += secao("portfolio", 5, "Portfólio: perfil, README e o que mostrar",
        "Quero que o meu perfil mostre o que sei fazer. O que vale pôr ali?",
        camada("Intuição", "O perfil é a sua vitrine, e o que está nela é público. Uma vitrine com poucas peças bem cuidadas diz mais que uma cheia de caixas vazias.") +
        camada("Definição", "O <b>README de perfil</b> é um repositório <b>público</b> com o <b>mesmo nome do seu usuário</b>, com um <code>README.md</code> na raiz: o GitHub o mostra no seu perfil. Repositórios criados antes de julho de 2020 não aparecem sozinhos (use “Share to profile”, segundo a página). A página <b>não</b> diz quantos repositórios podem ser fixados (<i>pins</i>): <b>confira</b>. Não há fonte oficial lida que diga o que recrutadores olham, e <b>nada garante vaga</b> por causa de commits ou PRs. O que dá para afirmar é que o perfil mostra repositórios públicos, o README de perfil e a atividade pública. Minhas sugestões (não são de fonte oficial): projetos reais com README que ensina a rodar, commits com mensagem clara, PRs em projetos de terceiros <i>com a resposta às revisões</i>, licença e <code>.gitignore</code> corretos, e nada de segredo, dado pessoal ou cópia de projeto de outra pessoa sem autorização.") +
        code('''
<!-- README.md do repositorio com o MESMO nome do seu usuario (exemplo, nao testado aqui) -->
# Oi, eu sou a Pessoa Exemplo
Estudo desenvolvimento e estou praticando Git e GitHub.
- Projeto em andamento: um organizador de tarefas em Python (link do repositorio)
- Aprendendo agora: GitHub Actions e testes automatizados
''') +
        naotestado("Não criei repositório de perfil nem fixei repositórios. O exemplo acima usa um nome de mentira. Escreva com as suas palavras e só com o que é verdade sobre você.") +
        erro("Perfil cheio de repositórios vazios ou só com “teste” no nome, e commits “ajuste” em série sem explicação. E prometer no README o que você ainda não sabe: escreva só o que é verdade."),
        ponte("Fechei a apostila. O que levo daqui?", "O resumo e o laboratório final."))

    corpo += aviso_lab() + lab("cap9", "secret scanning, vazamento simulado e gh",
        "Segunda metade do exercício 8, mais um treino de vazamento <b>local</b>. Em nenhum passo use credencial real ou de teste de um serviço.",
        ["No <code>treino-github</code>, confira nas configurações de segurança o que está ligado (secret scanning, push protection, Dependabot alerts). Anote o que viu e o que <b>depende do plano</b> (confira, sem supor).",
         "Crie um arquivo <code>teste-segredo.txt</code> com o texto <code>valor falso, nao e credencial</code> (algo que <b>não</b> imite nenhum formato de token) e dê push. Prova: o push <b>não</b> é bloqueado, porque não casa com nenhum padrão de credencial. Não tente simular um token.",
         "<b>Vazamento local.</b> Numa pasta temporária, repita o experimento do capítulo: commit de um arquivo com <code>CHAVE_FALSA_123</code>, depois <code>git rm --cached</code> e novo commit. Prova: <code>git log --all --oneline -S CHAVE_FALSA_123</code> lista <b>dois</b> commits.",
         "Abra a demo “vazou um segredo” e percorra os cinco tipos de segredo. Anote, para cada um, qual é o passo 1.",
         "<b>gh.</b> Rode <code>gh pr create --help</code> e <code>gh run list --help</code> e liste, no seu caderno, três flags que você usaria. Não rode <code>gh api</code> com POST, PUT ou DELETE.",
         "Monte o README de perfil (repositório com o seu usuário) com <b>só</b> o que é verdade. Prova: aberto numa janela anônima, o perfil mostra o README e nenhum dado pessoal que você não quis publicar."])

    fim = fechamento(6,
        ["<b>Secret scanning</b> (de graça em repositório público) e <b>push protection</b> (bloqueia push de credencial detectada) ajudam, mas agem depois ou só em padrões conhecidos. <b>Dependabot</b>: alertas, security updates e version updates.",
         "<b>Vazou?</b> 1. revogar ou rotacionar; 2. ver se foi usada; 3. avisar o time; 4. limpar o histórico com <code>git filter-repo</code> (opcional, exceto dado pessoal em repositório público), num clone novo e com backup; 5. limpar <b>não basta</b> (clones, forks, caches). <b>Apagar o commit não é o passo 1.</b>",
         "<code>git rm --cached</code> e <code>.gitignore</code> não removem o segredo do histórico: o <code>git log -S</code> o acha.",
         "<code>gh</code>: <code>pr</code>, <code>issue</code>, <code>repo</code>, <code>run</code>, <code>release</code>, <code>auth</code>, <code>api</code>. <code>gh api</code> com POST, PUT ou DELETE altera o GitHub de verdade. <code>--admin</code> no merge é bypass.",
         "Recuperação: <code>git reflog</code> acha o commit; <code>git branch nome hash</code> o devolve; <code>git revert -m 1</code> desfaz um merge; <code>pull --ff-only</code> falha com divergência.",
         "Perfil: README com o mesmo nome do usuário; nenhuma promessa de emprego; nada de segredo nem dado pessoal."],
        [quiz(1, "c", "Você enviou uma chave de API por engano para um repositório público. Qual é o <b>primeiro</b> passo?", [("a", "Apagar o commit."), ("b", "Rodar <code>git rm --cached</code>."), ("c", "Revogar ou rotacionar a chave no serviço que a emitiu.")], "É a única ação que impede o uso do segredo. O resto reduz o rastro, mas não desfaz o que já foi copiado."),
         quiz(2, "b", "Depois de <code>git rm --cached segredo.txt</code> e de um novo commit, o <code>git log --all --oneline -S VALOR</code> ainda lista commits. O que isso mostra?", [("a", "Um erro do Git."), ("b", "Que o valor continua no histórico, no commit antigo."), ("c", "Que o arquivo voltou.")], "Na execução que fiz, o <code>git show HEAD~1:segredo.txt</code> imprimiu a chave falsa."),
         quiz(3, "a", "Você apagou com <code>git branch -D</code> uma branch que tinha trabalho. Como recuperar?", [("a", "<code>git reflog</code> para achar o último commit e <code>git branch recuperada &lt;hash&gt;</code>."), ("b", "Não tem como."), ("c", "Clonar de novo e perder tudo.")], "O reflog guarda onde a sua HEAD esteve. Rodei e o trabalho voltou."),
         quiz(4, "b", "Qual a afirmação <b>correta</b> sobre portfólio no GitHub?", [("a", "Mais commits garantem uma vaga."), ("b", "O perfil mostra repositórios públicos, o README de perfil e a atividade pública, e não há garantia de vaga por causa deles."), ("c", "Repositório vazio impressiona.")], "A documentação não afirma o que recrutadores olham; o que vale é mostrar projetos reais, com README e honestidade.")],
        [("Qual a ordem quando um segredo vaza?", "Revogar, ver se foi usado, avisar o time, (opcional) limpar o histórico num clone novo e com backup, e saber que limpar não basta."),
         ("O que o reflog faz?", "Guarda onde sua HEAD esteve; serve para achar commit de uma branch apagada."),
         ("Quando o <code>gh api</code> é perigoso?", "Com POST, PUT ou DELETE: altera o GitHub de verdade."),
         ("Como ter um README de perfil?", "Repositório público com o mesmo nome do seu usuário e um <code>README.md</code> na raiz.")],
        fontes("gh_secret", "gh_seguranca", "gh_dependabot", "gh_remover", "gh_tokens", "ghcli", "gh_profile"),
        prox=None)
    publicar(9, "seguranca-gh-e-portfolio", "Segurança, gh, recuperação de erros e portfólio",
             "O que o GitHub vigia sozinho, a ordem certa quando algo vaza, o gh no terminal, como se recuperar de erros e como montar um perfil honesto.",
             "No capítulo 8 você automatizou testes, publicou e versionou. A pergunta que ficou: <b>se um segredo vazar ou eu errar feio, como me protejo e me recupero?</b> Este último capítulo, <b>complemento</b> como os outros, fecha a apostila.",
             corpo + fim, 55, S9)
