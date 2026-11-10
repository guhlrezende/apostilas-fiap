from gh_base import *

S5 = ["demos/gh-core.js", "demos/cap-5.js"]
S6 = ["demos/gh-core.js", "demos/cap-6.js"]


def cap4():
    corpo = ""
    corpo += secao("issue", 1, "Issue, label, milestone e assignee",
        "Tenho dez coisas para fazer no projeto, anotadas em cinco lugares. Como junto tudo e ainda deixo claro quem faz o quê?",
        camada("Intuição", "A issue é uma ficha de tarefa afixada no mural do projeto: tem número, título, conversa e responsável. Cada ficha é uma coisa só (um bug, uma ideia, uma tarefa), e dá para pesquisar e fechar.") +
        camada("Definição", "<b>Issue</b>: item para registrar e discutir trabalho, com número (<code>#123</code>). <b>Label</b>: etiqueta colorida (<code>bug</code>, <code>documentação</code>). <b>Milestone</b>: marco com prazo que agrupa issues e PRs. <b>Assignee</b>: quem está responsável. A página oficial também cita <b>sub-issues</b> (hierarquia de tarefas dentro de uma issue maior). <b>Discussions</b> é outra coisa: conversa aberta, sem item de trabalho; serve para perguntas, anúncios e enquetes, e pode virar issue quando vira trabalho. O administrador precisa habilitar. (GitHub Docs, lido em 10/11/2026.)") +
        tabela(["Quando usar", "Issue", "Discussion"], [
            ["“Isso está quebrado, e dá para consertar”", "sim", "não"],
            ["“Qual a melhor forma de organizar as pastas?”", "não", "sim"],
            ["Uma pergunta que acabou virando tarefa", "abra a issue", "converta a discussão em issue"],
        ]) +
        '<p>Pelo terminal, o <code>gh issue create</code> aceita, segundo a ajuda real que li nesta máquina (sem criar nada):</p>' +
        code('''
$ gh issue create --help | grep -E "^\\s+-"
  -a, --assignee login       Assign people by their login. Use "@me" to self-assign.
  -b, --body string          Supply a body. Will prompt for one otherwise.
  -F, --body-file file       Read body text from file (use "-" to read from standard input)
  -l, --label name           Add labels by name
  -m, --milestone name       Add the issue to a milestone by name
      --parent number        Add the new issue as a sub-issue of the specified parent number
  -p, --project title        Add the issue to projects by title
  -T, --template name        Template name to use as starting body text
  -t, --title string         Supply a title. Will prompt for one otherwise.
      --type name            Set the issue type by name
  -w, --web                  Open the browser to create an issue
$ gh issue create --title "Corrige o calculo da media" --label bug --assignee @me      # NAO rodei: criaria uma issue
''') +
        naotestado("Não criei issue, label nem milestone. Só li a ajuda do comando e a documentação. As telas de criação de issue e de labels eu não vi.") +
        erro("Criar labels demais. Poucas e claras (por exemplo <code>bug</code>, <code>documentação</code>, <code>boa primeira issue</code>) valem mais que vinte que ninguém usa. Outro: usar issue para pergunta aberta que cabia numa Discussion, ou o contrário."),
        ponte("Tenho as fichas. Como ligo uma ficha ao código que a resolve?", "Com referências no texto do PR e do commit."))

    corpo += secao("referencias", 2, "#123, Closes #123 e a regra do branch padrão",
        "Escrevi “Closes #7” no PR e a issue não fechou. O que faltou?",
        camada("Intuição", "É uma etiqueta que o GitHub lê: “quando esta mudança entrar na pista principal, dê a ficha por resolvida”. Se a mudança entrar numa pista lateral, a etiqueta não dispara.") +
        camada("Definição", "Escrever <code>#123</code> em outra issue ou PR cria um <b>link</b> entre eles. As palavras que <b>fecham</b> a issue quando o PR entra são <code>close</code>, <code>closes</code>, <code>closed</code>, <code>fix</code>, <code>fixes</code>, <code>fixed</code>, <code>resolve</code>, <code>resolves</code> e <code>resolved</code>, como em <code>Closes #123</code> ou <code>Fixes dono/repo#100</code>. <b>A palavra só vale quando o PR tem como destino o branch padrão.</b> Em outro destino, nada acontece. Para desfazer o vínculo automático, edite a descrição do PR e tire a palavra. (GitHub Docs, lido em 10/11/2026.)") +
        ex("o Git guarda a frase, mas quem interpreta é o GitHub", [
            "Fiz um commit com a mensagem <code>docs: README, LICENSE, gitignore e templates (Closes #7)</code> num repositório local.",
            "O <code>git log</code> mostrou a frase inteira, como qualquer texto. <b>Localmente nada fecha nem liga</b>: não existe issue 7 no meu computador.",
            "No GitHub, a palavra-chave é lida na descrição do PR e (segundo a documentação) também nos commits, quando o PR vai para o branch padrão. Eu <b>não</b> testei isso no site.",
        ]) +
        code('''
$ git commit -qm "docs: README, LICENSE, gitignore e templates (Closes #7)"
$ git log -1 --format='%s'
docs: README, LICENSE, gitignore e templates (Closes #7)    # so texto: quem le e o GitHub
''') +
        SAIDA_LOCAL +
        naotestado("O fechamento automático da issue só acontece no GitHub. Para confirmar, no seu repositório de treino abra uma issue de teste, escreva <code>Closes #1</code> num PR para a main e veja a issue fechar quando o PR entrar (laboratório abaixo).") +
        erro("Abrir o PR para uma branch que não é a padrão (por exemplo <code>develop</code>) com <code>Closes #123</code> e esperar que a issue feche. Nesse destino, nada acontece. Outro: confundir <code>#123</code> de issue com <code>#123</code> de PR: os dois usam a mesma numeração no repositório."),
        ponte("As fichas e o código estão ligados. E para ver tudo isso de uma vez, com prazo e prioridade?", "Projects."))

    corpo += secao("projects", 3, "Projects: tabela, quadro e roadmap",
        "Tenho vinte issues abertas. Quais atacar primeiro, e quem está parado onde?",
        camada("Intuição", "Se a issue é a ficha, o Project é o quadro na parede onde você pendura as fichas em colunas (a fazer, fazendo, feito) ou as lista numa tabela com prazo e prioridade.") +
        camada("Definição", "<b>Projects</b> oferece visões de <b>tabela</b>, <b>quadro</b> (kanban) e <b>roadmap</b> sobre issues e PRs, com campos personalizados (a página lida cita até 50 por projeto). O quadro lê as issues; mover o cartão atualiza o campo de status. (GitHub Docs, lido em 10/11/2026.)") +
        erro("Montar um quadro bonito e nunca olhar. Quadro que ninguém atualiza é pior que nenhum: dá falsa sensação de organização. Comece com três colunas e só acrescente quando precisar."),
        ponte("Sei registrar e planejar. Agora, como a mudança chega à main com revisão?", "Com branch, pull request e merge."))

    corpo += aviso_lab() + lab("cap4", "uma issue de ponta a ponta",
        "Prepara o exercício 3 do capítulo 5: você precisa de uma issue de teste.",
        ["No <code>treino-github</code>, crie duas labels (por exemplo <code>bug</code> e <code>documentação</code>) e um milestone com uma data próxima. Anote o nome de cada.",
         "Abra uma issue de teste com título claro e uma frase de descrição, com a label e o milestone. Ela deve ter o número <code>#1</code> (se não tiver, anote o número que apareceu e use ele no capítulo 5).",
         "Atribua a issue a você mesmo (no terminal, <code>--assignee @me</code> na criação; no site, o campo de responsável).",
         "Crie um Project (tabela ou quadro) e adicione a issue. Mova o cartão de coluna e observe o campo de status.",
         "Prova de que deu certo: <code>gh issue list</code> mostra a issue com label e responsável, e o Project mostra o mesmo cartão. Se você usou o <code>gh</code>, nenhum token apareceu na tela."])

    fim = fechamento(4,
        ["<b>Issue</b> = ficha de trabalho com número. <b>Label</b> classifica, <b>milestone</b> agrupa com prazo, <b>assignee</b> é o responsável. <b>Discussion</b> é para conversa sem tarefa.",
         "<code>#123</code> cria link. <code>Closes #123</code> (ou fix, resolve) <b>fecha a issue</b>, mas só quando o PR vai para o branch padrão.",
         "O Git guarda a frase como texto; quem interpreta é o GitHub.",
         "<b>Projects</b>: tabela, quadro e roadmap sobre issues e PRs, com campos personalizados.",
         "Poucas labels, claras. Quadro só vale se alguém atualiza."],
        [quiz(1, "c", "Seu PR tem <code>Closes #5</code> mas o destino é a branch <code>develop</code>, que não é a padrão. O que acontece com a issue 5?", [("a", "Fecha mesmo assim."), ("b", "Fecha quando o PR é aberto."), ("c", "Nada: a palavra-chave só vale com destino no branch padrão.")], "Essa regra está na página oficial de vínculo de PR com issue."),
         quiz(2, "a", "Uma dúvida geral do tipo “qual a melhor estrutura de pastas?” cabe melhor em…", [("a", "Discussions."), ("b", "Uma issue com label bug."), ("c", "Um milestone.")], "Discussions é para conversa sem item de trabalho; se virar tarefa, converta em issue."),
         quiz(3, "b", "Você fez um commit local com “Closes #7” na mensagem. A issue 7 fecha?", [("a", "Sim, o Git fecha."), ("b", "Não: o Git só guarda o texto. Quem interpreta é o GitHub, quando o commit ou PR chega lá."), ("c", "Sim, quando você faz <code>git log</code>.")], "O Git local nem conhece a issue. Eu rodei e o <code>git log</code> só mostrou a frase.")],
        [("O que o milestone faz?", "Agrupa issues e PRs sob um marco com prazo."),
         ("Quais palavras fecham uma issue pelo PR?", "close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved, seguidas de #número."),
         ("Quando a palavra-chave <i>não</i> fecha a issue?", "Quando o PR tem como destino um branch que não é o padrão."),
         ("Projects serve para quê?", "Ver issues e PRs em tabela, quadro ou roadmap, com campos como status e prazo.")],
        fontes("gh_issues", "gh_link", "gh_projects", "gh_discussions", "osguide", "ghcli"),
        prox=(5, "Como a mudança chega à main?", "Branch, pull request, revisão e os tipos de merge."))
    publicar(4, "issues-e-projects", "Issues, labels, milestones, referências e Projects",
             "Como registrar, ligar e acompanhar o trabalho antes de escrever o código.",
             "No capítulo 3 você aprendeu a enviar código e a se autenticar. A pergunta que ficou: <b>como planejo o trabalho e registro quem faz o quê?</b>",
             corpo + fim, 35)


def cap5():
    corpo = ""
    corpo += secao("flow", 1, "GitHub Flow: branch curta, PR, revisão, merge",
        "Num projeto com mais de uma pessoa, qual é o caminho de uma mudança até a main?",
        camada("Intuição", "A main é a versão “oficial” do livro. Você não rabisca nela: tira uma cópia (branch), escreve na cópia, mostra o rascunho para alguém ler (pull request) e só quando aprovado a mudança entra no original.") +
        camada("Definição", "A página oficial do GitHub Flow lista seis passos: (1) criar uma branch com nome curto e descritivo; (2) fazer a alteração, em commits com mensagem descritiva e, de preferência, uma mudança isolada e completa, e dar push; (3) abrir o PR com resumo, problema resolvido e issues ligadas (pode ser <b>draft</b> se você quer feedback antes); (4) responder aos comentários com novos commits (o PR se atualiza sozinho); (5) fazer o merge depois da aprovação, sem conflitos e respeitando as regras de proteção; (6) apagar a branch depois do merge. A página não diz qual é o nome do branch padrão; aqui assumo <code>main</code>. (GitHub Docs, lido em 10/11/2026.)") +
        code('''
$ git switch main
$ git pull --ff-only                       # so avanca; falha se divergiu
$ git switch -c feature/titulo-curto
# ... edita, testa ...
$ git add arquivo.ext
$ git commit -m "feat: descreve a mudanca"
$ git push -u origin feature/titulo-curto
$ gh pr create --draft --fill              # NAO rodei contra o GitHub: abriria um PR
# quando estiver pronto:
$ gh pr ready
$ gh pr checks
$ gh pr merge --squash --delete-branch
''') +
        naotestado("Os comandos <code>gh pr</code> acima não foram rodados contra o GitHub. As flags eu li na ajuda real: <code>gh pr create</code> aceita <code>--draft</code>, <code>--fill</code>, <code>--base</code>, <code>--title</code>, <code>--body</code>, <code>--reviewer</code>, <code>--label</code>, <code>--milestone</code>, <code>--template</code> e <code>--dry-run</code>. O <code>gh pr merge</code> aceita <code>--merge</code>, <code>--squash</code>, <code>--rebase</code>, <code>--delete-branch</code>, <code>--auto</code> e <code>--admin</code>.") +
        '<h3>Um bom PR</h3><p><b>Título</b>: o que muda, em uma frase, no imperativo (<code>Corrige o cálculo da média com nota zero</code>). <b>Descrição</b> (esta lista é sugestão minha, não está em página oficial): o que mudou e por quê, como testar, a issue com <code>Closes #123</code>, capturas de tela se houver mudança visual e o que ficou de fora de propósito. O guia de open source recomenda PRs pequenos e focados, que expliquem o motivo e não só o que foi feito.</p>' +
        erro("Trabalhar direto na <code>main</code> local e depois não conseguir separar o que é seu. Crie a branch <b>antes</b> de editar (veja o capítulo 9 para recuperar). E abrir PR de branch antiga, desatualizada: traga a base antes com merge ou rebase."),
        ponte("O PR está aberto. O que acontece com ele até virar merge?", "Estados: draft, revisão, mudanças pedidas, checks. Vamos mexer num."))

    corpo += secao("pr-estados", 2, "A vida de um PR: revisão, checks e conflito",
        "Pedi revisão e o colega pediu mudanças. Eu já posso fazer o merge? E o que muda quando o PR é draft?",
        camada("Intuição", "O PR é um processo com portões: cada portão só abre depois do anterior. Um rascunho não pede revisão nem entra. Uma revisão que pede mudanças tranca o merge até você responder. Os checks são a catraca automática: se falham, não passa.") +
        camada("Definição", "Segundo a página de revisões (lida em 10/11/2026): <b>Comment</b> comenta sem aprovar nem reprovar; <b>Approve</b> aprova; <b>Request changes</b> pede ajuste e bloqueia o merge enquanto não for resolvido, se a regra exigir; <b>Suggested changes</b> propõe um trecho exato que o autor aceita com um clique. Cada comentário em linha pode ser marcado como <b>resolvido</b>. A aba “Files changed” mostra o diff e “Conversation” a discussão. Um PR em <b>draft</b> não pode ser mesclado e não dispara pedido automático de revisão a CODEOWNERS. Um PR com <b>conflito</b> não pode ser mesclado até o conflito ser resolvido. A página não diz se o autor pode aprovar o próprio PR: isso depende da regra de proteção (<b>confira</b>).") +
        '<div class="demo" data-demo="prFluxo"></div>' +
        ex("lendo a demo", [
            "Comece clicando em <b>Abrir como draft</b>. Em seguida tente <b>Fazer merge</b>: a demo recusa, porque um rascunho não pode ser mesclado.",
            "<b>Marcar como pronto</b>, <b>Pedir revisão</b> e <b>Pedir mudanças</b>. Com mudanças pedidas e a regra de aprovação ligada, o merge é recusado (a página diz que bloqueia “se a regra exigir”: desligue a regra e a demo deixa passar). Um <b>novo commit</b> devolve o PR para a revisão e os checks recomeçam.",
            "Com as regras da demo ligadas (aprovação e checks obrigatórios), o merge só é aceito depois de <b>Aprovar</b> e de os <b>checks passarem</b>. Depois do merge, <b>Apagar a branch</b> só funciona uma vez.",
            "Desligue a regra de aprovação: num repositório seu, sem proteção, o merge é permitido sem aprovação. Se isso vale ou não no seu repositório depende da configuração: confira na tela.",
        ]) +
        '<p>Revisar pelo terminal (flags confirmadas na ajuda de <code>gh pr review</code>: <code>--approve</code>, <code>--comment</code>, <code>--request-changes</code>, <code>--body</code>):</p>' +
        code('''
$ gh pr review 123 --approve                                             # NAO testado aqui
$ gh pr review 123 --request-changes --body "Falta teste para o caso X"  # NAO testado aqui
$ gh pr review 123 --comment --body "Duvida sobre Y"                     # NAO testado aqui
''') +
        naotestado("A demo é uma simulação das regras descritas na documentação. Eu não abri PR, não vi a tela de revisão e não testei o comportamento real de aprovação do próprio autor.") +
        '<h3>Conflito</h3><p>Dois lados mexeram na mesma linha. O Git não decide por você. Resolva atualizando a sua branch com a base (<code>git merge main</code> ou <code>git rebase main</code>), editando o arquivo, <code>git add</code> e <code>git commit</code>, e enviando de novo. O GitHub também tem um editor para conflitos simples (não testado aqui). Saída real de um conflito de conteúdo:</p>' +
        code('''
$ git merge feature/conflito
Auto-merging titulo.txt
CONFLICT (content): Merge conflict in titulo.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status -s
UU titulo.txt
$ cat titulo.txt
<<<<<<< HEAD
titulo: C
=======
titulo: B
>>>>>>> feature/conflito
# resolver: deixe so o texto final no arquivo, depois: git add titulo.txt ; git commit
''') +
        SAIDA_LOCAL +
        erro("Deixar os marcadores <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code> no arquivo e dar commit. O texto com os marcadores vira parte do código. Abra o arquivo, escolha o texto final, apague as três linhas de marcação e só então <code>git add</code>."),
        ponte("O PR passou. Na hora de fazer o merge, o GitHub oferece três botões. Qual escolher?", "Merge commit, squash ou rebase: cada um deixa a história de um jeito."))

    corpo += secao("tipos-merge", 3, "Merge commit, squash e rebase: o que cada um faz na main",
        "O PR tem três commits de ajuste. Como eles vão aparecer na main depois do merge?",
        camada("Intuição", "Três jeitos de colar as páginas do rascunho no livro. <b>Merge commit</b>: cola as três páginas e põe um marcador no ponto de junção. <b>Squash</b>: resume as três numa só página. <b>Rebase</b>: recopia as três páginas, uma depois da outra, sem marcador.") +
        camada("Definição", "Segundo a página oficial de merges (lida em 10/11/2026): <b>merge commit</b> mantém todos os commits do PR e cria um commit de merge na base, indicado quando o histórico completo importa; <b>squash and merge</b> junta todos os commits do PR em um só, indicado quando o PR é uma única mudança lógica com muitos commits de ajuste; <b>rebase and merge</b> adiciona cada commit à base sem commit de merge e o GitHub <b>recria os commits com novos SHAs</b>, indicado quando o time quer histórico linear e os commits já estão bem organizados.") +
        '<div class="demo" data-demo="mergeSim"></div>' +
        ex("o mesmo PR, três resultados (rodado de verdade, e igual ao da demo)", [
            "Cenário: a main tinha 2 commits (<code>c1</code>, <code>c2</code>), eu abri uma branch com <b>3 commits</b> (<code>p1</code>, <code>p2</code>, <code>p3</code>) e, enquanto isso, a main ganhou 1 commit (<code>m1</code>).",
            "<b>Merge commit</b>: a main fica com <b>7</b> commits (2 + m1 + 3 do PR + o commit de merge). O grafo tem dois ramos e um commit de dois pais.",
            "<b>Squash</b>: a main fica com <b>4</b> commits (2 + m1 + 1 commit só com tudo). Os commits <code>p1</code> a <code>p3</code> <b>não estão</b> na main: o <code>git branch --contains</code> do <code>p3</code> listou só a branch do PR.",
            "<b>Rebase</b>: a main fica com <b>6</b> commits (2 + m1 + 3 copiados), em linha reta, sem commit de merge, e os três ganharam <b>hashes novos</b> (por exemplo, <code>p3</code> era <code>cdb9065</code> e virou <code>d6ba3ab</code>).",
        ]) +
        '<p><b>Merge commit</b> (<code>git log --oneline --graph</code>):</p>' +
        code('''
*   f2587a3 Merge branch 'feature/x'
|\\
| * da4d84c p3: ajuste 3
| * 9b15b44 p2: ajuste 2
| * 3b167e4 p1: ajuste 1
* | 5a0b2c9 m1: main andou
|/
* 84df076 c2: base
* ce63c94 c1: base
# 7 commits na main
''') +
        '<p><b>Squash</b>:</p>' +
        code('''
* 5836bb8 feat: ajustes (squash)
* 1f4ec53 m1: main andou
* d985e4d c2: base
* 2b0fa5e c1: base
# 4 commits na main
''') +
        '<p><b>Rebase</b> (note os hashes novos):</p>' +
        code('''
* d6ba3ab p3: ajuste 3
* 4698264 p2: ajuste 2
* 9366cda p1: ajuste 1
* 21bc125 m1: main andou
* 287b408 c2: base
* 0e3009e c1: base
# 6 commits na main
''') +
        '<p>Como reproduzi no terminal (o botão do GitHub faz o equivalente):</p>' +
        code('''
$ git merge --no-ff --no-edit feature/x        # merge commit
$ git merge --squash feature/x                 # squash: prepara tudo, e voce faz o commit
$ git commit -qm "feat: ajustes (squash)"
$ git switch feature/x ; git rebase main       # rebase: recopia os commits sobre a main
Successfully rebased and updated refs/heads/feature/x.
$ git switch main ; git merge --ff-only feature/x
''') +
        SAIDA_LOCAL +
        '<p class="muted" style="font-size:.85rem">Um detalhe que testei: com a <b>main parada</b> (sem commit novo desde que a branch nasceu), o <code>git rebase main</code> local respondeu <code>Current branch f is up to date.</code> e o hash <b>não mudou</b>. A página do GitHub diz que o “rebase and merge” recria os commits com novos SHAs; a demo mostra o resultado como a página descreve e eu <b>não testei o botão</b>.</p>' +
        naotestado("Os três botões de merge do GitHub não foram testados: reproduzi o efeito descrito na documentação com comandos locais. As opções de quais tipos de merge ficam habilitados em cada repositório são configurações do site (confira).") +
        '<h3>Desfazer um merge</h3>' +
        code('''
$ git revert --no-edit HEAD                    # HEAD e um commit de merge
error: commit fa218401631f516792442aa35d1823580ef4344b is a merge but no -m option was given.
fatal: revert failed
$ git revert --no-edit -m 1 HEAD               # -m 1 = manter o primeiro pai (a main)
[main e388493] Revert "Merge branch 'feature/x'"
 Date: Tue Nov 10 12:46:50 2026 -0300
 3 files changed, 3 deletions(-)
 delete mode 100644 p1
 delete mode 100644 p2
 delete mode 100644 p3
$ ls
a
b
m.txt                                          # sumiram so os 3 arquivos do PR (p1, p2, p3); o m1 ficou
''') +
        SAIDA_LOCAL +
        erro("Dar <code>git revert</code> num commit de merge sem <code>-m 1</code>. O Git não sabe qual dos dois pais é a “linha principal” e recusa. O <code>-m 1</code> diz: mantenha o primeiro pai (a main). Outro erro: usar rebase em branch que outras pessoas já baixaram, e dar <code>--force</code>."),
        ponte("Sei levar uma mudança minha até a main. E se o projeto não for meu?", "Aí não tenho nem permissão de escrita: é o caso do fork."))

    corpo += aviso_lab() + lab("cap5", "um PR de verdade, conflito e três merges",
        "Exercícios 3, 4 e 5 da lista, todos no seu <code>treino-github</code>. No repositório só seu não há outro revisor: registre a revisão com <code>--comment</code> e confira na tela se o merge é permitido sem aprovação.",
        ["<b>PR de treino.</b> Abra um PR de <code>feature/teste-1</code> para <code>main</code> <b>em draft</b>, com <code>Closes #1</code> na descrição (a issue do capítulo 4). Confirme que o botão de merge fica bloqueado enquanto é draft.",
         "Marque como pronto (<code>gh pr ready</code> ou no site), registre um comentário de revisão (<code>gh pr review --comment --body \"ok\"</code>) e faça o merge com <b>squash</b>, apagando a branch. Prova: a issue <code>#1</code> foi fechada sozinha, e <code>git log --oneline</code> na main mostra <b>um</b> commit novo.",
         "<b>Conflito real.</b> Edite a <b>mesma linha</b> de um arquivo pela interface web numa branch e, localmente, em outra. Abra o PR, veja o aviso de conflito e resolva localmente com <code>git merge main</code> (ou <code>rebase</code>). Prova: o PR deixa de mostrar conflito e não restou nenhum <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code> no arquivo (<code>grep -rn \"&lt;&lt;&lt;&lt;&lt;&lt;&lt;\" .</code> não acha nada).",
         "<b>Três tipos de merge.</b> Em três branches, faça três commits cada e abra três PRs. Faça um com <b>merge commit</b>, um com <b>squash</b> e um com <b>rebase</b>. Depois de cada um, rode <code>git pull</code> e <code>git log --oneline --graph</code> na main.",
         "Compare os três grafos com a demo do capítulo (mesmo número de commits do PR). Anote: quantos commits cada tipo adicionou à main e em qual deles apareceu um commit de merge.",
         "Num merge commit de teste, desfaça com <code>git revert -m 1 &lt;hash-do-merge&gt;</code> numa branch <b>descartável</b> e confirme que os arquivos do PR sumiram e o histórico foi preservado."])

    fim = fechamento(4,
        ["<b>GitHub Flow</b>: branch curta, commits descritivos, PR (draft se quer feedback), responder com novos commits, merge depois da aprovação, apagar a branch.",
         "<b>Draft</b> não faz merge. <b>Request changes</b> bloqueia (se a regra exigir). <b>Conflito</b> bloqueia. <b>Checks</b> falhando bloqueiam se forem obrigatórios.",
         "<b>Merge commit</b>: mantém tudo e cria commit de merge. <b>Squash</b>: um commit só. <b>Rebase</b>: commits copiados (hashes novos), história linear, sem merge commit.",
         "No cenário de 3 commits e main que andou 1: merge commit adiciona <b>4</b> (3 + merge), squash <b>1</b>, rebase <b>3</b>.",
         "<code>git revert</code> de merge exige <code>-m 1</code>. <code>git pull --ff-only</code> falha com histórico divergente.",
         "Sem forçar push em branch que outras pessoas usam."],
        [quiz(1, "b", "Um PR tem 3 commits de ajuste e o time quer a main com <b>um</b> commit por mudança. Qual tipo de merge?", [("a", "Merge commit."), ("b", "Squash."), ("c", "Nenhum: é impossível.")], "O squash junta todos os commits do PR em um só na base."),
         quiz(2, "c", "Você tenta <code>git revert</code> num commit de merge e recebe “is a merge but no -m option was given”. O que fazer?", [("a", "Apagar o repositório."), ("b", "Usar <code>git reset --hard</code> e <code>push --force</code>."), ("c", "Usar <code>git revert -m 1 &lt;hash&gt;</code>.")], "O <code>-m 1</code> diz ao Git para manter o primeiro pai, a linha da main."),
         quiz(3, "a", "Um PR em <b>draft</b>, com checks passando e aprovado. Dá para fazer o merge?", [("a", "Não: draft não pode ser mesclado até ser marcado como pronto."), ("b", "Sim, aprovado basta."), ("c", "Sim, mas só com squash.")], "A página de revisões diz que o draft não pode ser mesclado."),
         quiz(4, "b", "O que acontece, segundo a página oficial, com os commits quando você usa “rebase and merge”?", [("a", "São apagados."), ("b", "São adicionados à base sem commit de merge, e o GitHub recria os commits com novos SHAs."), ("c", "Viram um commit só.")], "É o que a página de merges descreve. Por isso o histórico fica linear, mas os hashes mudam.")],
        [("Quando usar squash?", "Quando o PR é uma única mudança lógica com vários commits de ajuste."),
         ("O que é <code>--ff-only</code>?", "Só aceita avançar a branch. Se divergiu, falha, e você escolhe merge ou rebase."),
         ("Por que <code>revert -m 1</code>?", "Um merge tem dois pais; o <code>-m 1</code> escolhe o primeiro (a main) como linha a manter."),
         ("Como resolver conflito antes do merge?", "Atualize a sua branch com a base (merge ou rebase), edite, <code>git add</code>, commit e envie.")],
        fontes("gh_flow", "gh_pr", "gh_reviews", "gh_merges", "gh_link", "osguide", "ghcli"),
        prox=(6, "E num projeto que não é meu?", "Fork, upstream e a etiqueta de quem contribui."))
    publicar(5, "branch-pr-e-merge", "Branches, GitHub Flow, pull request e tipos de merge",
             "O caminho completo de uma mudança até a main, com revisão, checks, conflito e as três formas de integrar.",
             "No capítulo 4 você ligou issues ao código. A pergunta que ficou: <b>como transformo uma issue em código revisado e entregue?</b> Este é o centro da apostila: o pull request e o que cada tipo de merge faz com a sua história. O PR simples você já viu no <a href='" + TG6 + "'>capítulo 6 de Terminal e Git</a>; aqui ele vem completo.",
             corpo + fim, 60, S5)


def cap6():
    corpo = ""
    corpo += secao("quando-fork", 1, "Fork ou branch: quando usar cada um",
        "Quero corrigir um erro de digitação no repositório de outra pessoa. Faço uma branch nele?",
        camada("Intuição", "Se a casa é sua ou você tem a chave, você trabalha dentro dela (branch). Se a casa é de outra pessoa, você tira uma cópia da planta para a sua casa (fork), mexe lá e manda a proposta de volta por correio (PR).") +
        camada("Definição", "Sem permissão de escrita no repositório: <b>fork</b>. Com permissão de escrita no repositório do time: <b>branch</b> no próprio repositório, sem fork, que é o padrão de equipe. O fluxo de fork da página oficial (lida em 10/11/2026): fazer o fork, clonar o <i>seu</i> fork, criar uma branch, commitar, enviar para o seu fork e abrir o PR para o original. A página de visibilidade diz que o fork compartilha o código e as configurações de visibilidade com o original. A regra fina de fork de repositório privado não está na página que li (<b>confira</b>).") +
        tabela(["Situação", "O que fazer"], [
            ["O repositório é seu", "branch + PR para a sua main"],
            ["É do seu time e você tem permissão de escrita", "branch no repositório original + PR (sem fork)"],
            ["É de outra pessoa ou projeto aberto, sem permissão de escrita", "fork, branch no fork, PR para o original"],
        ]) +
        erro("Clonar o original, fazer commits e só então descobrir que o push é recusado. O clone aponta para o original: faltou o fork. Confira <code>git remote -v</code> antes de investir tempo."),
        ponte("Fiz o fork. O original continua andando. Como mantenho a minha cópia em dia?", "Com um segundo remoto, o upstream."))

    corpo += secao("upstream", 2, "origin, upstream e manter o fork em dia",
        "Meu fork é de semana passada e o original já recebeu dez commits. Como alcanço?",
        camada("Intuição", "Seu fork é uma foto do original no dia em que você tirou. O <code>upstream</code> é um segundo contato na sua agenda, o do original. Você busca as novidades por ele, mistura na sua cópia e devolve ao seu fork.") +
        camada("Definição", "Num fork há <b>dois remotos</b>: <code>origin</code> (o seu fork, onde você tem permissão) e <code>upstream</code> (o original, que você só lê). A sequência da página oficial de sincronização: <code>git remote add upstream URL</code>, <code>git fetch upstream</code>, <code>git switch main</code>, <code>git merge upstream/main</code> e <code>git push origin main</code>. O <code>gh repo sync</code> também faz isso, com <code>--branch</code>, <code>--source</code> e <code>--force</code>; a página avisa que o <code>--force</code> <b>apaga a branch do fork</b> para igualar ao original, descartando commits locais dela.") +
        ex("um fork simulado, rodado de verdade", [
            "Criei <code>original.git</code> (o dono) com um commit, e um <code>fork.git</code> como cópia dele (um <code>git clone --bare</code>, só para simular, porque eu não criei fork no GitHub). Clonei o fork em <code>meu</code> e adicionei o <code>upstream</code>.",
            "O dono enviou um commit novo. Rodei <code>git fetch upstream</code>. O <code>git rev-list --left-right --count main...upstream/main</code> deu <b>0 1</b>: zero commits meus à frente, um atrás do original.",
            "O <code>git merge --ff-only upstream/main</code> avançou a <code>main</code> e o <code>git push origin main</code> levou isso para o <b>meu fork</b> (<code>f629c8c..64436cb</code>). Só então criei a branch <code>fix/typo</code> a partir da main atualizada e a enviei com <code>-u</code> para o meu fork.",
        ]) +
        code('''
$ git remote -v                          # logo depois de clonar o meu fork
origin	.../fork.git (fetch)
origin	.../fork.git (push)
$ git remote add upstream ../original.git
$ git fetch upstream
 * [new branch]      main       -> upstream/main
$ git rev-list --left-right --count main...upstream/main
0	1                                    # 0 a frente, 1 atras do original
$ git switch main ; git merge --ff-only upstream/main
Updating f629c8c..64436cb
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
$ git push origin main
   f629c8c..64436cb  main -> main        # agora o meu fork esta em dia
$ git switch -c fix/typo ; git push -u origin fix/typo
$ git branch -vv
* fix/typo e3cd4cd [origin/fix/typo] docs: corrige typo
  main     64436cb [origin/main] feat: novidade do dono
$ git rev-list --left-right --count main...upstream/main
0	0                                    # em dia: nenhum commit de diferenca
''') +
        SAIDA_FORK +
        naotestado("Fork, <code>gh repo fork</code>, <code>gh repo sync</code> e o botão “Contribute”/“Open a pull request” não foram testados: usei dois repositórios bare locais para simular o fork. A simulação mostra os remotos e os commits, não o comportamento do site.") +
        erro("Fazer as suas alterações direto na <code>main</code> do fork e depois não conseguir sincronizar sem conflito. Deixe a <code>main</code> do fork espelhando o upstream e trabalhe em branches. Outro erro: usar <code>gh repo sync --force</code> sem saber que ele descarta commits locais da branch."),
        ponte("Sei manter o fork em dia. Como fica o desenho inteiro, com o PR?", "Num diagrama que você mexe."))

    corpo += secao("diagrama", 3, "O desenho completo: upstream, origin e a sua máquina",
        "Em que ordem acontecem as coisas, e o que está impedido enquanto outra etapa não for feita?",
        camada("Intuição", "Três caixas: o original (upstream), o seu fork no GitHub (origin) e o seu computador (local). As setas entre elas são os comandos. O PR é a seta que sai do seu fork e chega no original.") +
        camada("Definição", "O diagrama abaixo simula: fazer o fork, clonar, adicionar o remoto <code>upstream</code>, <code>fetch upstream</code>, <code>merge upstream/main</code>, <code>push origin main</code>, criar a branch, enviar a branch e abrir o PR. Quando o dono do original publica algo, o seu fork <b>fica atrás</b> até você sincronizar. A simulação recusa passos fora de ordem e explica por quê.") +
        '<div class="demo" data-demo="forkSim"></div>' +
        ex("um caminho completo na demo", [
            "<b>Fazer o fork</b>, <b>clonar o fork</b> e <b>git remote add upstream</b>.",
            "Clique em <b>O dono publica uma novidade</b>: o contador “atrás do original” sobe para 1.",
            "<b>git fetch upstream</b>, <b>git merge upstream/main</b> e <b>git push origin main</b>: o contador volta para 0 e o fork fica em dia.",
            "<b>Criar branch</b>, <b>Commit na branch</b>, <b>Enviar a branch</b> e <b>Abrir PR</b>. Tente abrir o PR sem enviar a branch: a demo recusa.",
        ]) +
        '<h3>Etiqueta de quem contribui</h3><p>Do guia de open source e da página de contribuição (lidos em 10/11/2026), resumidos com as minhas palavras:</p><ul>' +
        '<li>Antes de qualquer coisa, leia o README, o CONTRIBUTING e o código de conduta, e veja se o projeto tem commits e respostas recentes.</li>' +
        '<li>Procure uma issue existente antes de abrir outra. Se for trabalhar nela, avise.</li>' +
        '<li>Mudança grande: combine na issue <b>antes</b> de escrever o código.</li>' +
        '<li>PR pequeno e focado, com teste, e no estilo do projeto.</li>' +
        '<li>Responda à revisão com rapidez. Sem resposta por mais de uma semana, faça um lembrete educado no <b>próprio tópico</b>, não em mensagem privada.</li>' +
        '<li>Se recusarem a contribuição, agradeça e respeite. Você sempre pode manter o seu fork.</li>' +
        '<li>Se usou ferramentas de IA, revise o que for enviar: você continua responsável pelo conteúdo.</li></ul>' +
        erro("Abrir um PR enorme, sem avisar, num projeto que você acabou de conhecer. O mantenedor não tem como revisar e não sabe se a mudança cabe no projeto. Combine na issue e mande pedaços pequenos."),
        ponte("Sei contribuir sem esbarrar em ninguém. Em equipe, o que impede alguém de quebrar a main?", "A proteção da branch."))

    corpo += aviso_lab() + lab("cap6", "fork simulado no seu computador",
        "Fazer fork do seu próprio repositório na mesma conta não é o caso de uso (<b>confira</b> na tela: não li essa regra na documentação), e contribuir com um projeto de terceiros exige respeitar as regras dele. Por isso este laboratório é <b>local</b>: ele reproduz a mecânica com repositórios bare, e eu rodei exatamente estes comandos.",
        ["Numa pasta nova, crie o “original” e o “fork”: <code>git init -q --bare -b main original.git</code>. Clone-o para <code>dono</code>, faça um commit com README e <code>git push origin main</code>. Depois <code>git clone -q --bare original.git fork.git</code>.",
         "Clone o fork: <code>git clone -q fork.git meu</code>. Em <code>meu</code>, rode <code>git remote -v</code> e anote para onde o <code>origin</code> aponta. Configure nome e e-mail de teste só nesse clone (<code>git config user.name</code> e <code>user.email</code>).",
         "Adicione o <code>upstream</code> (<code>git remote add upstream ../original.git</code>). Em <code>dono</code>, faça outro commit e envie. Em <code>meu</code>, rode <code>git fetch upstream</code> e <code>git rev-list --left-right --count main...upstream/main</code>.",
         "Sincronize: <code>git merge --ff-only upstream/main</code> e <code>git push origin main</code>. Crie <code>fix/typo</code>, faça um commit e envie com <code>-u</code> para o fork.",
         "Prova de que deu certo: <code>git branch -vv</code> mostra <code>[origin/fix/typo]</code> e o contador do passo 3 vira <b>0 0</b> depois do sincronismo. Opcional, no site: veja como fica a tela “Contribute” do seu próprio fork (não testado aqui)."])

    fim = fechamento(4,
        ["Sem permissão de escrita: <b>fork</b>. Com permissão no repositório do time: <b>branch</b> nele, sem fork.",
         "Num fork: <code>origin</code> = o seu fork; <code>upstream</code> = o original. <code>git fetch upstream</code>, <code>git merge upstream/main</code>, <code>git push origin main</code>.",
         "<code>git rev-list --left-right --count main...upstream/main</code> diz quantos commits você tem à frente e atrás.",
         "<code>gh repo sync --force</code> <b>descarta</b> commits locais da branch do fork.",
         "Etiqueta: ler CONTRIBUTING, procurar issue existente, combinar mudança grande, PR pequeno com teste, lembrete educado no próprio tópico."],
        [quiz(1, "a", "Você não tem permissão de escrita num projeto e quer propor uma correção. Qual o caminho?", [("a", "Fork, branch no fork e PR para o original."), ("b", "Clonar o original e dar push na main."), ("c", "Pedir a senha do dono.")], "Sem permissão de escrita, a contribuição passa pelo seu fork."),
         quiz(2, "c", "O que o resultado <code>0 3</code> de <code>git rev-list --left-right --count main...upstream/main</code> diz?", [("a", "Que você está 3 commits à frente do original."), ("b", "Que o fork foi apagado."), ("c", "Que você tem 0 commits à frente e está 3 atrás do upstream.")], "O primeiro número conta o que só a sua <code>main</code> tem; o segundo, o que só a <code>upstream/main</code> tem."),
         quiz(3, "b", "Na demo, você tenta abrir o PR sem ter enviado a branch para o fork. O que acontece?", [("a", "O PR abre normalmente."), ("b", "A demo recusa: o PR sai de uma branch que existe no fork, então ela precisa ter sido enviada."), ("c", "O fork é apagado.")], "O PR compara uma branch do seu fork com a do original; sem push, a branch só existe no seu computador.")],
        [("Qual a diferença entre <code>origin</code> e <code>upstream</code> num fork?", "<code>origin</code> é o seu fork (você escreve); <code>upstream</code> é o original (você só lê)."),
         ("Como atualizar o fork pelo terminal?", "<code>git fetch upstream</code>, <code>git merge upstream/main</code> na main e <code>git push origin main</code>."),
         ("O que fazer antes de uma mudança grande num projeto de terceiros?", "Combinar na issue, antes de escrever o código."),
         ("Quando esperar mais de uma semana por revisão?", "Faça um lembrete educado no próprio tópico, não em mensagem privada.")],
        fontes("gh_contribuir", "gh_syncfork", "gh_repos", "osguide", "progit_dist", "ghcli"),
        prox=(7, "O que impede alguém de quebrar a main?", "Proteção de branch, rulesets e CODEOWNERS."))
    publicar(6, "fork-e-contribuicao", "Fork, upstream e contribuição em projeto de terceiros",
             "Quando usar fork, como manter a sua cópia em dia e como contribuir sem atrapalhar ninguém.",
             "No capítulo 5 você levou uma mudança até a main do <b>seu</b> repositório. A pergunta que ficou: <b>e num projeto que não é meu, onde eu nem posso escrever?</b>",
             corpo + fim, 45, S6)
