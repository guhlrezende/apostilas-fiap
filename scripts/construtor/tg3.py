from tg_base import *
S5 = ["demos/tg-core.js", "demos/cap-5.js"]

IDENT = ('<p class="muted">Nos exemplos, o Git sabia quem era o autor porque passei a identidade por variáveis de ambiente (nome fictício, e-mail de exemplo). No seu computador isso se configura uma vez com <code>git config --global user.name</code> e <code>git config --global user.email</code>; <mark class="hl p">não rodei esses dois no seu computador</mark>. '
         'No PowerShell os comandos <code>git</code> são exatamente os mesmos, porque o <code>git</code> é um programa e não um comando de shell.</p>')


def cap5():
    corpo = ""
    corpo += secao("tres-lugares", 1, "Os três lugares e o commit",
        "Por que o Git pede <code>add</code> e <code>commit</code> separados? Não bastava salvar?",
        camada("Intuição", "Pense numa foto de grupo. Primeiro você <b>arruma quem vai aparecer</b> (o <code>add</code>), depois <b>aperta o botão</b> (o <code>commit</code>). O resultado é uma foto do projeto naquele momento, que fica guardada e dá para rever depois. Se você mudou 5 arquivos mas só 2 contam a mesma história, tira uma foto com 2 e outra com 3.") +
        camada("Definição", "Um repositório Git tem <b>três lugares</b>: a <b>pasta de trabalho</b> (os arquivos que você edita), a <b>área de preparação</b> (staging: o que vai entrar na próxima foto) e o <b>repositório</b> (a pasta escondida <code>.git</code>, onde as fotos ficam). Um <b>commit</b> é um registro de um estado do projeto, com identificador (hash), autor, mensagem e um ponteiro para o commit anterior (IBM Developer, tutorial de 2021).") +
        ex("do arquivo novo ao primeiro commit", [
            "Crio <code>notas.txt</code>. O <code>git status</code> o lista em <b>Untracked files</b>: o Git vê, mas ainda não acompanha.",
            "<code>git add notas.txt</code> põe o arquivo na área de preparação. O <code>git status -s</code> (versão curta) mostra <code>A  notas.txt</code>: A de <i>added</i>.",
            "<code>git commit -m \"primeiro commit\"</code> responde <code>1 file changed, 1 insertion(+)</code>: <b>1</b> arquivo, <b>1</b> linha nova. O <code>git log --oneline</code> mostra <b>1</b> commit, com hash curto de 7 caracteres.",
        ]) +
        code('''
$ git init -b main                  # cria o repositório (a pasta .git); main é o nome da branch
Initialized empty Git repository in C:/Users/voce/estudo/projeto-git/.git/
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notas.txt

nothing added to commit but untracked files present (use "git add" to track)
$ git add notas.txt                 # arruma a foto
warning: in the working copy of 'notas.txt', LF will be replaced by CRLF the next time Git touches it
$ git status -s
A  notas.txt
$ git commit -m "primeiro commit"   # aperta o botão
[main (root-commit) 8727806] primeiro commit
 1 file changed, 1 insertion(+)
 create mode 100644 notas.txt
$ git log --oneline
8727806 primeiro commit
''') + IDENT +
        ex("ver a diferença antes de registrar", [
            "Acrescento a linha <code>nova</code> a um arquivo de 3 linhas. O <code>git diff</code> mostra a mudança: linhas com <code>+</code> entraram, com <code>-</code> saíram. Aqui apareceu <b>1</b> linha com <code>+nova</code>.",
            "<code>git restore notas.txt</code> desfaz a edição e volta ao último commit. O <code>git status -s</code> fica vazio.",
        ]) +
        code('''
$ git diff
diff --git a/notas.txt b/notas.txt
index e2e365a..a7ce375 100644
--- a/notas.txt
+++ b/notas.txt
@@ -1,3 +1,4 @@
 a
 l2
 l3
+nova
$ git restore notas.txt     # CUIDADO: descarta a edição que não foi commitada
''') +
        erro("Dois tropeços. (1) Ver <code>warning: LF will be replaced by CRLF</code> e achar que quebrou tudo. Não é erro fatal: é o Git do Windows avisando que vai converter o fim de linha (configuração <code>core.autocrlf</code>). Não ignore sem entender se o seu time usa a mesma regra. (2) <b>Rodar <code>git restore</code> sem pensar</b>: ele descarta mudanças que não foram commitadas, e não há como recuperar."),
        ponte("Já tiro fotos do projeto. E se eu quiser testar uma ideia sem estragar a versão que funciona?", "Com branches e merge."))

    corpo += secao("branches", 2, "Branches, HEAD e merge",
        "Quero testar uma ideia sem arriscar a versão que funciona. Preciso copiar a pasta inteira?",
        camada("Intuição", "Não precisa copiar nada. Uma <b>branch</b> é só uma <b>etiqueta</b> colada num commit. Criar outra etiqueta é instantâneo. Quando você faz um commit novo, a etiqueta em que você está anda para a frente; as outras ficam onde estavam. O <b>HEAD</b> é o 'você está aqui': aponta para a branch atual.") +
        camada("Definição", "<code>git branch nome</code> cria a etiqueta; <code>git switch nome</code> muda para ela (<code>git switch -c nome</code> cria e muda). <code>git merge nome</code> junta o trabalho de <code>nome</code> na branch em que você está. Há dois resultados: <b>fast-forward</b> (a branch atual não andou, então o merge só move a etiqueta e <b>não cria commit</b>) ou <b>merge commit</b> (as duas andaram, então nasce um commit novo com <b>dois pais</b>). (IBM Developer, tutorial de 2021.)") +
        ex("os dois tipos de merge, com número", [
            "<b>Cenário A, fast-forward.</b> Parto de 1 commit (<code>c1</code>). Crio <code>feature</code> e faço 2 commits nela (<code>c2</code>, <code>c3</code>). Volto para a main, que não andou, e faço <code>git merge feature</code>: a resposta é <code>Fast-forward</code>. Total: <b>3</b> commits, em linha reta, e <b>nenhum commit de merge</b>.",
            "<b>Cenário B, dois pais.</b> Mesmo começo, mas depois de voltar para a main eu faço o commit <code>c4</code> nela. Agora as duas branches andaram. O <code>git merge feature</code> cria o commit <code>c5</code> com <b>2 pais</b> (<code>c4</code> e <code>c3</code>). Total: <b>5</b> commits.",
            "Na saída real do cenário B, o <code>git log --graph</code> desenha o losango: a linha da feature sai de <code>c1</code> e volta no commit de merge.",
        ]) +
        code('''
# Cenário A: fast-forward
$ git merge feature
Updating f4a794f..00d811c
Fast-forward
 notas.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git log --oneline --graph --all
* 00d811c (HEAD -> main, feature) c3: exercicio
* bfc05a0 c2
* f4a794f primeiro commit

# Cenário B: as duas andaram, então nasce um commit de merge
$ git merge feature -m "c5: junta feature"
Merge made by the 'ort' strategy.
 notas.txt | 2 ++
 1 file changed, 2 insertions(+)
$ git log --oneline --graph --all
*   2e19467 (HEAD -> main) c5: junta feature
|\\
| * 84a1923 (feature) c3: exercicio
| * cb32ac7 c2
* | 93b03f0 c4: so na main
|/
* bd48c22 primeiro commit
''') +
        '<p class="muted">Nas saídas reais acima, os hashes (como <code>2e19467</code>) vêm da minha execução e seriam outros no seu computador. Os nomes entre parênteses (<code>HEAD -&gt; main</code>, <code>feature</code>) o Git mostra quando a saída vai para um terminal; para reproduzir isso eu rodei com <code>--decorate</code>. Também encurtei as saídas: tirei os avisos de CRLF do Windows e as linhas de progresso que o Git imprime no terminal. Na demo, para ficar legível, os commits se chamam <code>c1</code>, <code>c2</code> e assim por diante. A mensagem do merge também é diferente: na demo, o Git de mentira escreve <code>Merge branch \'feature\'</code>. Use um cenário pronto ou digite os seus comandos.</p>' +
        '<div class="demo" data-demo="gitGrafo"></div>' +
        '<h3>Quando o merge não consegue sozinho: conflito</h3>' +
        '<p>Se as duas branches mudaram a <b>mesma linha</b> do mesmo arquivo, o Git não sabe qual vale, e para. Ele escreve os dois lados no arquivo, entre marcadores, e espera você decidir. Rodei isso de verdade:</p>' +
        code('''
$ git merge ajuste
Auto-merging leia.txt
CONFLICT (content): Merge conflict in leia.txt
Automatic merge failed; fix conflicts and then commit the result.
$ git status -s
UU leia.txt                          # UU: os dois lados mudaram
$ cat leia.txt
<<<<<<< HEAD
titulo: Guia de Git                  # o que está na sua branch (main)
=======
titulo: Git na pratica               # o que veio da outra branch (ajuste)
>>>>>>> ajuste
# edite o arquivo, deixe a versão final sem os marcadores, e então:
$ git add leia.txt
$ git commit -m "resolve conflito"   # fecha o merge, com 2 pais como o cenário B
''') +
        erro("Resolver o conflito às cegas com <code>git checkout --theirs</code> ou <code>--ours</code>, ou apagar os marcadores sem ler. Abra o arquivo, ache os <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code>, decida o texto final com a cabeça e só então faça o <code>git add</code> e o commit. Esquecer um marcador dentro do arquivo é um erro que costuma ir parar no repositório.") +
        '<details class="cola"><summary>Complemento do complemento: rebase e revert (rodei um caso simples)</summary><div class="in-body"><p>O <b>rebase</b> reaplica os commits de uma branch em cima da ponta de outra, criando commits <i>novos</i> e deixando o histórico em linha reta. Num teste simples (a <code>main</code> com <code>m1</code> e <code>m2</code>, e uma branch <code>rb</code> que saiu de <code>m1</code> com o commit <code>r1</code>), o <code>git rebase main</code> respondeu <code>Successfully rebased and updated refs/heads/rb.</code> O <code>r1</code> trocou de hash (era <code>cee1e6c</code> e virou <code>f90b08b</code>, ou seja, é um commit novo) e o <code>git log --graph</code> ficou reto, com 3 commits e sem losango. A IBM alerta: <b>não reescreva commits que já foram enviados a outras pessoas</b>, porque o rebase troca os hashes. O <code>git revert --no-edit HEAD</code> faz o contrário de apagar: cria um commit novo que desfaz o anterior (rodei: saiu <code>[main bb731b5] Revert "r1"</code>, com <code>1 file changed, 1 deletion(-)</code>, e o commit original continua no log, logo abaixo). Não testei <code>cherry-pick</code>.</p></div></details>',
        ponte("O Git guarda tudo que está na pasta. Mas e arquivos que nunca devem entrar, como senhas e chaves?", "Com o .gitignore."))

    corpo += secao("gitignore", 3, ".gitignore: o que nunca entra",
        "Quase todo projeto tem um arquivo com senha ou chave, tipo um <code>.env</code>. Como garantir que ele nunca vá parar no GitHub?",
        camada("Intuição", "O <code>.gitignore</code> é uma lista de 'não quero que você nem olhe para isso'. O Git passa a fingir que esses arquivos não existem: eles não aparecem no <code>git status</code> e não entram no <code>git add</code> comum.") +
        camada("Definição", "É um arquivo de texto na raiz do repositório com um padrão por linha (<code>.env</code>, <code>logs/</code>, <code>*.log</code>). Vale só para arquivos que <b>ainda não estão sendo acompanhados</b>. Um arquivo já commitado continua acompanhado até você mandar o Git parar de acompanhá-lo. (Documentação oficial do Git.)") +
        ex("ignorar antes, e o que fazer se for tarde", [
            "Com <code>.env</code> e <code>logs/a.log</code> na pasta e um <code>.gitignore</code> com as linhas <code>.env</code> e <code>logs/</code>, o <code>git status -s</code> lista só <code>.gitignore</code> e <code>app.txt</code>: <b>2</b> arquivos. Os outros 2 ficaram invisíveis.",
            "<code>git check-ignore -v .env</code> mostra a regra responsável (<code>.gitignore:1:.env</code>). É a forma de tirar a dúvida 'por que o Git está ignorando isto?'.",
            "O caso difícil: um arquivo <code>.env2</code> <b>já foi commitado</b>. Adiciono <code>.env2</code> ao <code>.gitignore</code> e edito o arquivo. O <code>git status -s</code> ainda mostra <code> M .env2</code> (modificado): continua acompanhado. Só <code>git rm --cached .env2</code> faz o Git parar de acompanhá-lo: ele imprime <code>rm '.env2'</code>, o status passa a <code>D  .env2</code> e o arquivo <b>continua na sua pasta</b>. Mas isso vale <b>daqui para a frente</b>: o conteúdo antigo continua nos commits que já existem (o <code>git show HEAD~1:.env2</code> do bloco abaixo mostra isso).",
        ]) +
        code('''
$ cat .gitignore
.env
logs/
$ git status -s
?? .gitignore
?? app.txt
$ git check-ignore -v .env logs/a.log
.gitignore:1:.env	.env
.gitignore:2:logs/	logs/a.log

# o caso difícil: o arquivo já foi commitado
$ echo ".env2" >> .gitignore
$ echo mudou >> .env2
$ git status -s
 M .env2                  # ainda acompanhado, apesar do .gitignore
?? .gitignore
?? app.txt
$ git rm --cached .env2   # [[--cached|tira do Git, mas não apaga o arquivo da pasta]]
rm '.env2'
$ git status -s
D  .env2
?? .gitignore
?? app.txt
$ git commit -m "para de acompanhar o .env2"    # saída do commit omitida
$ git show HEAD~1:.env2   # [[HEAD~1|o commit anterior ao da remoção]]: o conteúdo antigo continua no histórico
env2
''') +
        erro("Achar que o <code>.gitignore</code> resolve um segredo que já foi commitado. <b>Não resolve</b>: o arquivo continua no histórico e em quem já baixou o repositório. Se uma senha ou chave de API foi parar num commit, trate como <b>vazada</b>: o passo obrigatório é <b>revogar ou trocar a credencial</b> (gerar outra e invalidar a antiga no serviço). O <code>git rm --cached</code> só tira o arquivo dos commits <i>futuros</i>: a chave continua no histórico e, se você já fez push, no remoto e em quem clonou (rodei: depois do <code>rm --cached</code> e do commit, o <code>git show</code> do commit anterior ainda mostrou o conteúdo). Apagar do histórico exige reescrevê-lo com <code>git filter-repo</code> ou com o BFG Repo-Cleaner e dar um <code>push --force</code>, o que reescreve o histórico de todo mundo que usa o repositório: <mark class=\"hl p\">não testado aqui</mark>. Mesmo assim, troque a credencial, porque cópias antigas podem existir. (A parte de orientação é boa prática geral; o que eu medi foi o <code>git show</code>.)") +
        '<p class="muted"><b>Cuidado ao criar o <code>.gitignore</code> pelo PowerShell 5.1.</b> Rodei (com um arquivo de teste no lugar do <code>.env</code>): <code>&quot;.env&quot; &gt; .gitignore</code> grava o arquivo em <b>UTF-16 LE</b> (bytes <code>255 254 46 0 101 0 ...</code>) e o Git <b>não o lê</b>: o <code>.env</code> continuou aparecendo como <code>??</code> e o <code>git check-ignore -v .env</code> não imprimiu nada. O <code>Out-File</code> sem opção faz o mesmo. É um risco real de commitar um segredo achando que ele estava ignorado. O que funcionou nos meus testes: <code>Set-Content .gitignore -Value &quot;.env&quot; -Encoding ascii</code> (também o <code>-Encoding utf8</code>, que no 5.1 grava com BOM e o Git aceitou), ou criar o arquivo pelo Git Bash com <code>echo .env &gt; .gitignore</code>. Depois de criar, <b>sempre</b> rode <code>git check-ignore -v .env</code> para confirmar. Fonte do <code>.gitignore</code>: documentação oficial do Git (não é da IBM; a IBM não tem tutorial de .gitignore nas páginas que li).</p>',
        ponte("Meu repositório está só no meu computador. Como levo isso para o GitHub e trabalho com outras pessoas?", "Com remotos, push e pull request, no capítulo 6."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "Três lugares: <b>pasta de trabalho</b> → (<code>git add</code>) → <b>staging</b> → (<code>git commit</code>) → <b>repositório</b>. Use <code>git status</code> antes e depois de cada passo.",
        "<b>Commit</b> = registro com hash, autor, mensagem e ponteiro para o anterior. <code>git log --oneline</code> lista; <code>git diff</code> mostra o que mudou.",
        "<b>Branch</b> é uma etiqueta num commit, não uma cópia. <b>HEAD</b> é onde você está. <code>git switch -c nome</code> cria e entra.",
        "<b>Merge</b>: fast-forward (sem commit novo, a atual não andou) ou merge commit (dois pais, as duas andaram). Cenário A = 3 commits; cenário B = 5 commits.",
        "Conflito: os dois lados mudaram a mesma linha. Edite, <code>git add</code>, <code>git commit</code>.",
        "<code>.gitignore</code> só vale para o que ainda não é acompanhado. Se já foi commitado: <code>git rm --cached</code> tira só dos commits futuros; se era segredo, <b>revogue ou troque a credencial</b>, porque ele continua no histórico."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "A <code>main</code> não recebeu nenhum commit desde que a <code>feature</code> saiu dela. O que faz <code>git merge feature</code> na main?", [("a", "Cria sempre um commit de merge com dois pais."), ("b", "Fast-forward: só move a etiqueta da main, sem commit novo."), ("c", "Apaga a branch feature.")], "Se a atual não andou, o histórico da feature é continuação direta dela. O Git só avança a etiqueta (fast-forward). O commit de merge com dois pais só nasce quando as duas andaram.") + \
        quiz(2, "c", "Você adicionou <code>.env</code> ao <code>.gitignore</code>, mas ele já tinha sido commitado e continua aparecendo como modificado. O que resolve?", [("a", "Nada: o .gitignore vale para qualquer arquivo."), ("b", "Reiniciar o computador."), ("c", "<code>git rm --cached .env</code> (vale daqui para a frente; se era segredo, troque-o também).")], "O .gitignore só vale para arquivos que ainda não são acompanhados. O <code>--cached</code> tira o arquivo do Git sem apagá-lo da pasta, mas o conteúdo antigo continua no histórico.") + \
        quiz(3, "a", "Criar uma branch copia todos os arquivos do projeto?", [("a", "Não: cria uma etiqueta apontando para um commit, o que é quase instantâneo."), ("b", "Sim, por isso branches grandes demoram."), ("c", "Só copia os arquivos que você modificou.")], "A branch é um ponteiro. Os arquivos só mudam de verdade quando você troca de branch e os commits são diferentes.") + \
        flash([
            ("Quais são os três lugares do Git?", "Pasta de trabalho, área de preparação (staging) e repositório (.git). O add leva ao staging, o commit leva ao repositório."),
            ("O que é uma branch?", "Uma etiqueta que aponta para um commit. Criar outra é instantâneo, não é uma cópia da pasta."),
            ("Fast-forward x merge commit?", "Fast-forward: a branch atual não andou, o Git só move a etiqueta. Merge commit: as duas andaram, nasce um commit com dois pais."),
            ("Como parar de acompanhar um arquivo já commitado?", "Colocar no .gitignore E rodar git rm --cached arquivo. Só o .gitignore não basta. Isso vale daqui para a frente: o histórico antigo continua com o arquivo.")]) + \
        fontes("ibm_git", "git_ignore") + \
        ponte("Meu histórico está só no meu computador. Como levo isso para o GitHub e trabalho com outras pessoas?", "Com remotos, push e pull request.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
    body = recap("O capítulo 4 fechou o bloco do terminal. Falta o assunto que o terminal mais serve hoje: guardar o histórico dos arquivos e voltar atrás quando algo dá errado. Este capítulo, <b>complemento</b> como o resto, trata do Git local: commit, branch, merge e .gitignore.") + AVISO_COMP + corpo
    chapter(PASTA, 5, "git-commit-branch-merge", TITULO, "Git: commit, branch, merge e .gitignore", "Capítulo 5 · Complemento",
            "O histórico do projeto como uma linha de fotos, com branches para testar ideias e merge para juntar.",
            chips(body, 45), body, scripts=S5)


def cap6():
    corpo = ""
    corpo += secao("remoto", 1, "Remotos: push, pull e clone",
        "Meu histórico está só no meu computador. Como levo isso para o GitHub, e como outra pessoa pega?",
        camada("Intuição", "Pense numa pasta compartilhada na nuvem que entende de histórico. O GitHub guarda uma cópia do seu repositório. Cada pessoa trabalha na sua cópia local e eles se <b>sincronizam</b>: você <b>envia</b> (push) o que fez e <b>traz</b> (pull) o que os outros fizeram.") +
        camada("Definição", "Um <b>remoto</b> é um repositório em outro lugar, com um apelido; o padrão é <code>origin</code>. <code>git remote add origin URL</code> registra o apelido. <code>git push -u origin main</code> envia a branch (o <code>-u</code> lembra o destino para os próximos). <code>git clone URL</code> baixa uma cópia completa. <code>git fetch</code> só atualiza o que você sabe do remoto; <code>git pull</code> faz isso e traz as mudanças para a sua branch.") +
        ex("duas pessoas, um remoto", [
            "Para testar sem GitHub, criei uma pasta que faz o papel de remoto (<code>git init --bare -b main</code>; sem o <code>-b main</code>, dependendo da sua configuração o remoto nasce apontando para <code>master</code> e o primeiro <code>git clone</code> avisa <code>remote HEAD refers to nonexistent ref</code>, como aconteceu comigo) e dois repositórios que conversam com ela. É o mesmo mecanismo do GitHub; muda a URL.",
            "No <b>meu</b> repositório: 1 commit, <code>git remote add origin ../nuvem/projeto.git</code> e <code>git push -u origin main</code>. A resposta: <code>[new branch] main -&gt; main</code>.",
            "A <b>colega</b> faz <code>git clone</code>, cria a branch <code>ajuste-titulo</code>, faz <b>1</b> commit e envia. No meu repositório, o <code>git fetch</code> só traz o aviso: aparece <code>origin/ajuste-titulo</code> em <code>git branch -r</code>, sem mexer nos meus arquivos.",
            "Depois que a mudança dela entra na main e vai para o remoto, o <code>git pull</code> responde <code>Fast-forward</code> e o log passa a ter <b>2</b> commits.",
        ]) +
        code('''
$ git remote add origin ../nuvem/projeto.git    # [[origin|apelido do remoto; no GitHub seria a URL https://github.com/...]]
$ git remote -v
origin	../nuvem/projeto.git (fetch)
origin	../nuvem/projeto.git (push)
$ git push -u origin main
To ../nuvem/projeto.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.

# a colega, no computador dela:
$ git clone nuvem/projeto.git colega
Cloning into 'colega'...
done.
$ git switch -c ajuste-titulo
Switched to a new branch 'ajuste-titulo'
$ echo "mais uma tarefa" >> tarefas.txt    # sem editar um arquivo antes, o commit -am não teria o que registrar
$ git commit -am "acrescenta tarefa"           # [[-am|add dos arquivos já acompanhados e commit, de uma vez]]
[ajuste-titulo f583543] acrescenta tarefa
 1 file changed, 1 insertion(+)
$ git push -u origin ajuste-titulo
To <caminho do remoto>
 * [new branch]      ajuste-titulo -> ajuste-titulo
branch 'ajuste-titulo' set up to track 'origin/ajuste-titulo'.

# de volta ao meu computador:
$ git fetch
From ../nuvem/projeto
 * [new branch]      ajuste-titulo -> origin/ajuste-titulo
$ git branch -r
  origin/HEAD -> origin/main
  origin/ajuste-titulo
  origin/main
''') +
        '<p class=\"muted\">Saídas encurtadas: tirei os avisos de CRLF do Windows e as linhas de progresso que o Git imprime no terminal (como <code>Enumerating objects</code>). Os hashes são os da minha execução.</p>' +
        naotestado("Tudo isto foi com um remoto <b>em pasta local</b>. Não conectei ao GitHub de verdade, então não testei: a autenticação (token de acesso ou chave SSH), o <code>git push</code> para uma URL <code>https://github.com/...</code>, nem o <code>gh</code> (a linha de comando do GitHub). Nunca coloque token ou senha dentro da URL nem em um arquivo do repositório.") +
        erro("Dar <code>git push --force</code> numa branch compartilhada. Ele reescreve o histórico do remoto e pode apagar o trabalho de outras pessoas. Não testei o comando por esse motivo; a regra é evitá-lo, e confirmar com o time antes se for inevitável."),
        ponte("Subi minha branch. Como as outras pessoas revisam antes de ela entrar na main?", "Com o pull request."))

    corpo += secao("pull-request", 2, "Pull request: pedir para juntar, com revisão",
        "Posso fazer merge direto na main. Por que times usam pull request?",
        camada("Intuição", "É um <b>pedido formal</b>: 'terminei esta branch, alguém pode olhar antes de entrar?'. Os colegas veem exatamente o que mudou, comentam, pedem ajustes, e só depois a mudança entra. É o controle de qualidade do time.") +
        camada("Definição", "Um <b>pull request</b> (PR) é um pedido para integrar uma branch ao projeto principal. Em geral: a pessoa abre o PR, a equipe compara as mudanças e comenta, quem abriu faz novos commits se for preciso, e um mantenedor aprova e faz o merge. Em outras plataformas, como o GitLab, o nome é <i>merge request</i>. (IBM Think, página sobre pull request.) A IBM descreve três fluxos: <b>feature branch</b> (uma branch por mudança), <b>fork</b> (uma cópia sua do repositório alheio, comum em projetos abertos) e <b>git-flow</b> (um conjunto mais rígido de branches).") +
        '''<div class="stepper rv">
    <div class="stage">
      <div class="st"><b>1. Branch</b><p><code>git switch -c ajuste-titulo</code>. Nunca trabalhe direto na main.</p></div>
      <div class="st"><b>2. Commits</b><p>Faça commits pequenos, cada um com mensagem que explica o quê e por quê.</p></div>
      <div class="st"><b>3. Push da branch</b><p><code>git push -u origin ajuste-titulo</code>. Este passo eu testei com o remoto local.</p></div>
      <div class="st"><b>4. Abrir o PR</b><p>No site do GitHub: escolher a branch de origem e a de destino, escrever o que mudou e por quê. <mark class="hl p">não testado aqui</mark></p></div>
      <div class="st"><b>5. Revisão</b><p>Os colegas leem o diff e comentam. Se pedirem ajuste, você faz novos commits na mesma branch e o PR se atualiza. <mark class="hl p">não testado aqui</mark></p></div>
      <div class="st"><b>6. Merge</b><p>Alguém com permissão aprova e junta na main. Depois, <code>git pull</code> na main local e apague a branch já usada. <mark class="hl p">não testado aqui</mark></p></div>
    </div>
    <div class="bar2"><button class="btn sm" data-prev>← Voltar</button><div class="dots"></div><button class="btn sm pri" data-next>Próximo →</button></div>
  </div>''' +
        ex("o que o PR muda em relação ao merge direto", [
            "Merge direto na main: <b>1</b> pessoa decide sozinha. Erro entra e só aparece depois.",
            "Com PR: <b>se o time exigir revisão</b>, outra pessoa olha a mesma mudança antes de ela entrar (quem escreveu e quem revisa). O PR em si não garante isso: é uma regra do time ou do repositório. O PR registra a discussão junto do código, e fica fácil voltar depois e entender <i>por que</i> algo foi mudado.",
            "Na minha simulação, o equivalente do botão de merge foi rodar <code>git merge origin/ajuste-titulo</code> na main (respondeu <code>Fast-forward</code>) e <code>git push</code>. No GitHub quem faz isso é o servidor. <mark class=\"hl p\">o PR em si, não testado aqui</mark>",
        ]) +
        naotestado("Abrir, revisar e fazer o merge de um pull request no GitHub (pelo site ou pelo <code>gh pr create</code>). Descrevi o fluxo pela página da IBM; não tenho um repositório de teste conectado. Se for fazer o seu primeiro PR, faça num repositório de treino seu.") +
        erro("Abrir um PR enorme, com dezenas de arquivos e várias ideias misturadas. É ruim de revisar e a revisão vira só um 'ok'. Prefira um PR por assunto, pequeno, com título e descrição que expliquem o que mudou. (Boa prática geral, não é medição minha.)"),
        ponte("Sei o caminho completo. Quais são os tropeços que mais pegam quem está começando?", "Os erros comuns, e um jogo para treinar."))

    corpo += secao("fluxo", 3, "Fluxo de trabalho e erros comuns",
        "Conheço os comandos. Na hora de trabalhar de verdade, qual é a sequência certa, e onde as pessoas escorregam?",
        camada("Intuição", "É um hábito, como olhar os dois lados antes de atravessar a rua: <b>olhar o estado, trabalhar numa branch, registrar em pequenos pedaços, mostrar para alguém, só então juntar</b>.") +
        camada("Definição", "O fluxo básico, em ordem: (1) <code>git status</code> para saber onde está; (2) <code>git switch -c nome</code>; (3) editar e testar; (4) <code>git add</code> e <code>git commit</code>, várias vezes; (5) <code>git push -u origin nome</code>; (6) abrir o PR; (7) depois do merge, <code>git switch main</code>, <code>git pull</code> e apagar a branch usada com <code>git branch -d nome</code>.") +
        ex("o ciclo com os números do que rodei", [
            "<code>git branch -d feature</code> depois de um fast-forward: <code>Deleted branch feature (was 2efef5d).</code> A branch some; os <b>3</b> commits continuam na main.",
            "No remoto local, depois do <code>fetch</code>: <b>2</b> branches remotas de verdade (<code>origin/main</code> e <code>origin/ajuste-titulo</code>); a linha <code>origin/HEAD -&gt; origin/main</code> é só um atalho para a principal. Depois do <code>pull</code>, o log tem <b>2</b> commits.",
        ]) +
        '<p>Treine a decisão. Para cada situação, qual é a ação certa?</p>' +
        '''<div class="card sorter rv" data-demo="sorter" data-opts="a:add e commit|b:git switch -c|c:gitignore e rm --cached|d:pull request|e:git push">
    <div class="item" data-ans="b"><p>Quero testar uma ideia sem mexer na main.</p><span class="why">Crie uma branch: git switch -c nome. É uma etiqueta nova, barata, e a main fica intacta.</span></div>
    <div class="item" data-ans="c"><p>Meu arquivo de senhas foi commitado ontem e quero parar de acompanhá-lo.</p><span class="why">Troque a senha primeiro, porque ela ficou no histórico. Só o .gitignore não basta para arquivo já acompanhado: use git rm --cached para parar de acompanhá-lo daqui para a frente.</span></div>
    <div class="item" data-ans="d"><p>Terminei a minha branch e quero que alguém revise antes de ela entrar na main.</p><span class="why">É exatamente o pull request: pedido formal de integração, com revisão.</span></div>
    <div class="item" data-ans="a"><p>Alterei dois arquivos e quero registrar essa versão com uma mensagem.</p><span class="why">git add nos arquivos e git commit -m "mensagem". Com git status antes, para conferir o que entra.</span></div>
    <div class="item" data-ans="e"><p>Fiz commits na minha branch e quero que meus colegas a vejam no GitHub.</p><span class="why">git push -u origin nome envia a branch para o remoto. Sem o push, ela só existe no seu computador.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>''' +
        '<h3>Os erros mais comuns de quem está começando</h3>' +
        '<p>Resumo do que apareceu na apostila inteira, em ordem de quanto custa errar:</p>' +
        '<ol>' +
        '<li><b>Subir segredo (<code>.env</code>, chave privada) para o repositório.</b> Coloque no <code>.gitignore</code> <i>antes</i> do primeiro commit; se já foi, <b>troque a credencial primeiro</b> (o <code>git rm --cached</code> só tira dos commits futuros).</li>' +
        '<li><b>Commitar direto na main</b> em vez de criar uma branch e abrir PR.</li>' +
        '<li><b><code>git push --force</code> em branch compartilhada</b> (não testado aqui) e <b>rebase em commits já enviados</b> (alerta da IBM): reescrevem o histórico dos outros.</li>' +
        '<li><b>Não olhar o <code>git status</code></b> antes e depois de cada passo.</li>' +
        '<li><b>Resolver conflito sem ler</b> o arquivo e os marcadores.</li>' +
        '<li><b>Estranhar o aviso de CRLF</b> do Windows (visto de verdade, não é erro fatal) ou, ao contrário, ignorá-lo sem saber se o time usa a mesma regra.</li>' +
        '<li><b>Misturar o terminal:</b> comando de bash no PowerShell e vice-versa; <code>curl</code> que é alias; aspas erradas.</li>' +
        '<li><b>Apagar a chave privada de SSH sem backup</b>, ou compartilhá-la.</li>' +
        '</ol>' ,
        ponte("Cheguei ao fim da apostila. O que levar para a prova ou para o primeiro trabalho em grupo?", "A cola abaixo reúne o essencial."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>Remoto</b> = repositório em outro lugar, com apelido (<code>origin</code>). <code>push</code> envia, <code>fetch</code> só atualiza o que você sabe, <code>pull</code> traz para a branch, <code>clone</code> baixa tudo.",
        "<b>Pull request</b> = pedido formal de juntar uma branch, com revisão. Em outras plataformas: <i>merge request</i>. Fluxos: feature branch, fork, git-flow.",
        "Fluxo: <code>status</code> → branch → commits pequenos → <code>push</code> → PR → revisão → merge → <code>pull</code> na main.",
        "Segredo: <code>.gitignore</code> antes do primeiro commit; se vazou, <b>revogue ou troque a credencial</b> (o <code>git rm --cached</code> só vale daqui para a frente; o histórico guarda o segredo).",
        "Evite <code>push --force</code> em branch compartilhada e rebase de commits já enviados.",
        "Nunca coloque token ou senha em URL, em chat ou no repositório. Chave privada não se compartilha."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual a diferença entre <code>git fetch</code> e <code>git pull</code>?", [("a", "Nenhuma: são apelidos."), ("b", "O fetch envia, o pull baixa."), ("c", "O fetch só atualiza o que você sabe do remoto; o pull também traz as mudanças para a sua branch.")], "Na simulação, o fetch só criou <code>origin/ajuste-titulo</code> na lista de branches remotas. O pull foi o que fez a minha branch andar (Fast-forward).") + \
        quiz(2, "b", "Para que serve um pull request, em vez de um merge direto na main?", [("a", "Para o merge ficar mais rápido."), ("b", "Para a mudança ser revisada por outras pessoas antes de entrar."), ("c", "Para esconder o histórico dos commits.")], "O PR é o ponto de conversa: as pessoas veem o que mudou, comentam e pedem ajustes antes de juntar.") + \
        quiz(3, "a", "Você descobre que subiu uma chave de API no último commit, já enviado. Qual a reação certa?", [("a", "Tratar como vazada: revogar ou trocar a chave, e também tirá-la do repositório."), ("b", "Só apagar o arquivo e fazer outro commit; ninguém viu."), ("c", "Adicionar ao .gitignore e pronto.")], "O arquivo continua no histórico e em quem já baixou. A chave tem de ser trocada; tirar do repositório é o segundo passo. O <code>git rm --cached</code> só vale para os próximos commits, e limpar o histórico (filter-repo, BFG) exige force push e não substitui a troca (não testado aqui).") + \
        flash([
            ("O que é origin?", "O apelido padrão do repositório remoto: a URL que você registrou com git remote add."),
            ("Passos de um fluxo com pull request?", "Branch, commits, push da branch, abrir o PR, revisão, merge e depois pull na main."),
            ("O que fazer se um segredo foi commitado e enviado?", "Revogar ou trocar a credencial: é o passo obrigatório. O git rm --cached só tira dos commits futuros; o segredo continua no histórico e no remoto. Limpar o histórico exige filter-repo ou BFG e force push (não testado aqui)."),
            ("Por que evitar push --force em branch compartilhada?", "Porque reescreve o histórico do remoto e pode apagar o trabalho dos outros.")]) + \
        fontes("ibm_pr", "ibm_git") + '''
</section>'''
    body = recap("No capítulo 5 você aprendeu o Git no seu computador. Falta o que torna o Git um trabalho de equipe: o repositório remoto, o pull request e um fluxo combinado. Este último capítulo continua sendo <b>complemento</b> e reúne os erros mais comuns da apostila inteira.") + AVISO_COMP + corpo
    chapter(PASTA, 6, "github-pull-request", TITULO, "GitHub, pull request e fluxo de trabalho", "Capítulo 6 · Complemento",
            "Levar o repositório para um remoto, pedir revisão com um pull request e evitar os tropeços comuns.",
            chips(body, 40), body, scripts=[])
