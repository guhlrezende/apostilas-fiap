from gh_base import *


def cap1():
    corpo = ""
    corpo += secao("git-x-github", 1, "Git e GitHub não são a mesma coisa",
        "Todo mundo diz “sobe no Git” quando quer dizer “sobe no GitHub”. Dá para ser uma coisa sem a outra?",
        camada("Intuição", "Git é o caderno de histórico que fica no <b>seu</b> computador. GitHub é um prédio na internet com estantes onde você guarda cópias desses cadernos, e que ainda tem sala de reunião, quadro de tarefas e vigia na porta. O caderno funciona sem o prédio. O prédio é que não faz sentido sem os cadernos.") +
        camada("Definição", "<b>Git</b> é o programa que registra o histórico de um projeto. <b>GitHub</b> é um serviço na nuvem que hospeda repositórios Git e acrescenta revisão de código (pull request), issues, automação (Actions), páginas, releases e controle de acesso. GitLab e Bitbucket fazem o mesmo papel; no GitLab o equivalente do pull request se chama <i>merge request</i>. Eu não li a documentação deles, então não detalho aqui. Os comandos <code>git</code> são os mesmos nos três. (Fonte: GitHub Docs e Pro Git, lidos em 10/11/2026.)") +
        ex("um repositório inteiro, sem GitHub nenhum", [
            "Numa pasta temporária nova rodei <code>git init</code>, escrevi um <code>README.md</code> e fiz um commit. Tudo funcionou: histórico, branch, log.",
            "O <code>git remote -v</code> voltou <b>vazio</b>: o repositório não conhece nenhum endereço na internet. Ele só passa a falar com o GitHub quando você adiciona um remoto (capítulo 3).",
            "Conclusão prática: se o GitHub sair do ar ou você ficar sem internet, o seu histórico continua inteiro no seu computador.",
        ]) +
        code('''
$ git init -b main treino
$ cd treino
$ printf '# treino\\n' > README.md
$ git add . ; git commit -qm "docs: cria README"
$ git remote -v                 # nada: nenhum remoto configurado
$ git branch --show-current
main
''') +
        SAIDA_LOCAL +
        erro("Achar que “o código está seguro porque está no GitHub”, ou que “o Git é o site”. O GitHub guarda uma cópia, e quem controla o que entra nela é você (e as regras do repositório). Um <code>git push</code> errado também sobe errado."),
        ponte("O caderno é meu, o prédio é do GitHub. Para entrar nele, preciso de uma conta. O que faz uma conta ser segura?", "Criar com cuidado e ligar a verificação em duas etapas."))

    corpo += secao("conta-2fa", 2, "Conta, perfil, 2FA e passkey",
        "Criar conta é só preencher um formulário. Por que a documentação insiste tanto no segundo fator?",
        camada("Intuição", "Sua conta é a chave do prédio inteiro: seus repositórios, os de quem te deu acesso e as chaves de publicação. Só a senha é uma tranca simples. A verificação em duas etapas (2FA) é uma segunda tranca que o ladrão de senha não tem.") +
        camada("Definição", "A conta é criada em <code>github.com/signup</code>, com e-mail verificado. O <b>nome de usuário</b> aparece em todo commit, PR e no perfil: escolha um que você aceite mostrar em público. A <b>2FA</b> aceita app autenticador (TOTP), SMS, chaves de segurança (FIDO2, Touch ID, Windows Hello) e <b>passkeys</b>. A página oficial recomenda uma passkey com um método reserva (TOTP ou SMS). O GitHub Mobile pode ser segundo fator, mas só depois de configurar TOTP ou SMS. Os <b>códigos de recuperação</b> devem ser baixados e guardados: a página avisa que o suporte <b>não consegue restaurar</b> a conta de quem perde o 2FA e os métodos de recuperação. A mesma página informa que, desde março de 2023, o GitHub exige 2FA de quem contribui com código no GitHub.com. (Fonte: GitHub Docs, lido em 10/11/2026.)") +
        tabela(["Método", "O que é", "Cuidado"], [
            ["Passkey", "credencial no aparelho ou no gerenciador, usada com biometria ou PIN", "tenha um método reserva (a própria página recomenda)"],
            ["App autenticador (TOTP)", "código de 6 dígitos que muda a cada 30 segundos", "troca de celular: transfira o app antes, ou use os códigos de recuperação"],
            ["Chave de segurança (FIDO2)", "dispositivo físico ou o Windows Hello, Touch ID", "guarde uma segunda chave, se puder"],
            ["SMS", "código por mensagem", "é o método que a documentação coloca como reserva, não como principal"],
            ["Códigos de recuperação", "lista de códigos de uso único", "guarde num cofre de senhas, <b>nunca</b> num arquivo do repositório nem em chat"],
        ]) +
        naotestado("Não criei conta nem liguei 2FA para escrever isto. Eu <b>não descrevo as telas</b> (nomes de menus e botões mudam): siga o assistente do próprio GitHub e confira cada método na página oficial listada nas fontes.") +
        erro("Ligar a 2FA e não baixar os códigos de recuperação. Se o celular some, a conta pode ficar perdida, e o suporte não a restaura. Guarde os códigos <b>fora</b> do aparelho que gera o segundo fator."),
        ponte("A conta está protegida. E o meu nome e o meu e-mail, que vão em cada commit: quem vê?", "Todo mundo, se o repositório for público."))

    corpo += secao("email-commit", 3, "O e-mail que vai em cada commit",
        "Fiz um commit com o e-mail da minha caixa pessoal. Alguém consegue ler isso depois?",
        camada("Intuição", "Todo commit carrega uma etiqueta com nome e e-mail do autor, como o remetente de uma carta. Num repositório público, a carta e o remetente ficam expostos para sempre. Por isso existe um endereço de fachada: o <code>noreply</code>.") +
        camada("Definição", "O GitHub associa um commit à sua conta pelo <b>e-mail do commit</b>, e só e-mails adicionados e verificados na conta contam. Existe a opção “Keep my email address private”; com ela, o commit feito pela interface web usa o endereço <code>noreply</code> da sua conta. <b>Commits antigos continuam com o e-mail antigo</b>: trocar a configuração não reescreve o passado (para isso seria preciso reescrever o histórico, capítulo 9). O <b>formato exato</b> do endereço noreply não estava na página que li: copie-o da tela de e-mails da sua conta (<b>confira</b>). A página também cita como bloquear pushes que exponham o e-mail pessoal, mas eu não li esse guia. (Fonte: GitHub Docs e Pro Git, lidos em 10/11/2026.)") +
        ex("o e-mail do commit fica gravado, e eu consigo ler", [
            "Para não mexer na minha configuração real, apontei <code>GIT_CONFIG_GLOBAL</code> para um arquivo temporário. Assim o <code>--global</code> só escreveu nesse arquivo.",
            "Configurei nome, e-mail (um espaço reservado, <code>SEU-EMAIL-NOREPLY</code>, que você troca pelo endereço da sua conta) e <code>init.defaultBranch main</code>.",
            "Depois de um commit, o <code>git log -1 --format='%an | %ae | %s'</code> mostrou o nome, o e-mail e a mensagem: tudo isso <b>viaja junto com o commit</b>.",
        ]) +
        code('''
$ git config --global user.name "Seu Nome ou Apelido"
$ git config --global user.email "SEU-EMAIL-NOREPLY"     # copie o endereco noreply da sua conta
$ git config --global init.defaultBranch main
$ git config --global --list --show-origin
file:C:/Users/voce/.gitconfig	user.name=Aluno Exemplo
file:C:/Users/voce/.gitconfig	user.email=SEU-EMAIL-NOREPLY
file:C:/Users/voce/.gitconfig	init.defaultbranch=main
$ git log -1 --format='%an | %ae | %s'
Aluno Exemplo | SEU-EMAIL-NOREPLY | docs: README, LICENSE, gitignore e templates (Closes #7)
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 10/11/2026 com um arquivo de configuração temporário. Nas máquinas, <code>--global</code> escreve no <code>.gitconfig</code> da sua pasta de usuário. Aqui o nome “Aluno Exemplo” é inventado.</p>' +
        erro("Usar o nome completo e o e-mail pessoal sem perceber, em repositório público. O que está num commit publicado não some trocando a configuração depois. Decida o nome e o e-mail <b>antes</b> do primeiro commit público."),
        ponte("Conta protegida, identidade definida. Onde fica o meu projeto, e o que o faz ficar bem montado?", "No repositório."))

    corpo += aviso_lab() + lab("cap1", "conta e identidade",
        "Este laboratório é na sua conta e no seu computador. Nenhum passo exige colar senha ou token em lugar nenhum.",
        ["Confira com <code>git --version</code> que o Git está instalado. Se for a primeira vez, rode os três <code>git config --global</code> do exemplo acima, com o e-mail noreply da sua conta (copiado da tela de e-mails dela).",
         "Rode <code>git config --global --list --show-origin</code> e confirme que o nome, o e-mail e o <code>init.defaultbranch</code> aparecem. Se aparecer um e-mail pessoal onde devia estar o noreply, corrija antes do primeiro commit público.",
         "Na sua conta, confirme que há pelo menos <b>dois métodos</b> de segundo fator (por exemplo passkey e app autenticador) e que você baixou os <b>códigos de recuperação</b> e os guardou num cofre de senhas.",
         "Leia o seu perfil em modo anônimo (uma janela privada do navegador): o que aparece para quem não está logado? Ajuste nome e bio se algo ali você não quer mostrar.",
         "Prova de que deu certo: um commit de teste numa pasta nova e o <code>git log -1 --format='%an | %ae'</code> mostram o nome e o e-mail que <b>você escolheu</b>, e nenhum e-mail pessoal."])

    fim = fechamento(4,
        ["<b>Git</b> guarda o histórico no seu computador; <b>GitHub</b> hospeda repositórios Git e acrescenta PR, issues, Actions, Pages e releases. Um repositório Git funciona sem GitHub.",
         "Ligue a <b>2FA</b>, de preferência passkey com método reserva, e <b>guarde os códigos de recuperação</b>: o suporte não restaura a conta de quem perde tudo.",
         "O nome de usuário e o e-mail do commit são <b>públicos</b> em repositório público. Use o endereço <code>noreply</code> da sua conta (copie da tela de e-mails; o formato exato eu não confirmei).",
         "Commits antigos <b>não</b> mudam quando você troca a configuração.",
         "<code>git config --global --list --show-origin</code> mostra de onde vem cada valor."],
        [quiz(1, "b", "Um colega diz que o projeto dele está “no Git, então está no GitHub”. Qual a correção?", [("a", "Está certo: Git e GitHub são o mesmo programa."), ("b", "O Git guarda o histórico no computador dele; o GitHub só tem a cópia que ele enviar com push."), ("c", "O GitHub é que cria o histórico, o Git só envia.")], "Git é o programa de histórico. O GitHub é um serviço que hospeda repositórios Git. Sem <code>git push</code> para um remoto, nada vai para lá."),
         quiz(2, "c", "Qual combinação a página oficial de 2FA recomenda?", [("a", "Só SMS."), ("b", "Só a senha forte."), ("c", "Passkey com um método reserva (TOTP ou SMS), mais os códigos de recuperação guardados.")], "A mesma página avisa que o suporte não restaura a conta de quem perde o 2FA e também a recuperação."),
         quiz(3, "a", "Você trocou o e-mail da configuração do Git hoje. O que acontece com os commits de ontem?", [("a", "Continuam com o e-mail antigo."), ("b", "Passam a ter o e-mail novo automaticamente."), ("c", "São apagados.")], "O e-mail fica gravado em cada commit. Mudar o futuro não reescreve o passado."),
         quiz(4, "b", "Por que a apostila escreve <code>SEU-EMAIL-NOREPLY</code> em vez de um endereço?", [("a", "Porque o GitHub não tem esse recurso."), ("b", "Porque o formato exato não estava na página lida: você copia da tela de e-mails da sua conta."), ("c", "Porque e-mail não pode aparecer em commit.")], "Onde eu não confirmei, escrevo “confira”. Aqui, o dado certo está na sua conta.")],
        [("Dá para usar Git sem GitHub?", "Sim. O Git funciona só no seu computador; o GitHub é um lugar para hospedar e colaborar."),
         ("O que fazer logo depois de ligar a 2FA?", "Baixar e guardar os códigos de recuperação, e ter um segundo método."),
         ("Quem consegue ver o e-mail de um commit público?", "Qualquer pessoa. Use o endereço noreply da conta."),
         ("Trocar o <code>user.email</code> corrige commits antigos?", "Não. Só os novos. Os antigos ficam como estavam.")],
        fontes("gh_sobre", "gh_conta", "gh_2fa", "gh_email", "progit"),
        prox=(2, "Onde o projeto mora?", "No repositório: visibilidade, README, licença e os arquivos de saúde."))
    publicar(1, "git-github-conta", "Git x GitHub, conta, 2FA e o seu e-mail",
             "O que é cada coisa, como proteger a conta e o que o e-mail dos seus commits conta para o mundo.",
             f"Você já viu commit, branch, merge e pull request simples na apostila de <a href='{TG5}'>Terminal e Git</a> (capítulos <a href='{TG5}'>5</a> e <a href='{TG6}'>6</a>). Esta apostila <b>assume esse básico</b> e não o repete: ela cuida do que o GitHub acrescenta. A pergunta que abre tudo: <b>o que é, de fato, o GitHub, e como entro nele do jeito certo?</b>",
             corpo + fim, 35)


def cap2():
    corpo = ""
    corpo += secao("visibilidade", 1, "Público, privado e o que “público” significa",
        "Vou criar o repositório. Marco público ou privado, e dá para voltar atrás?",
        camada("Intuição", "Público é um mural na praça: qualquer um lê e copia. Privado é um armário trancado: só entra quem você der a chave. A diferença que pega: <b>o que foi para o mural não volta</b>, mesmo que você apague depois.") +
        camada("Definição", "<b>Público</b>: qualquer pessoa na internet acessa e lê. <b>Privado</b>: só você, quem recebeu acesso e membros da organização com permissão. <b>Interno</b> existe só em organização no GitHub Enterprise Cloud, e não importa numa conta pessoal. Quem tem permissão de administrador pode mudar a visibilidade. (GitHub Docs, lido em 10/11/2026.) A regra prática é minha: tudo que vai para um repositório público já deve ser tratado como copiado por alguém (cópias, forks e caches), então senhas, tokens, <code>.env</code>, CPF, dados de cliente, finanças e saúde <b>não entram</b>.") +
        tabela(["Pergunta", "Público", "Privado"], [
            ["Quem lê", "qualquer pessoa", "você, convidados e a organização com permissão"],
            ["Serve para", "portfólio, projeto aberto, material de estudo", "trabalho em andamento, código de empresa, o que ainda não pode aparecer"],
            ["Risco principal", "vazar o que não devia (não tem volta)", "esquecer que alguns recursos de segurança mudam conforme o plano (confira)"],
        ]) +
        erro("Começar privado “só para testar”, pôr uma chave dentro, e tornar público depois. A chave segue no histórico inteiro. Antes de mudar a visibilidade, releia o <b>histórico</b>, não só os arquivos de agora."),
        ponte("Decidi a visibilidade. O que um visitante precisa encontrar logo na porta?", "Um README que explique o projeto."))

    corpo += secao("readme-licenca", 2, "README e LICENSE",
        "Um estranho abre o meu repositório. O que ele precisa ver para entender o projeto em um minuto?",
        camada("Intuição", "O README é a recepção: o que é isto, para que serve, como eu começo. A licença é o aviso na porta que diz o que os outros podem fazer com o seu código. Sem ela, a porta diz “não pode nada”.") +
        camada("Definição", "O <b>README</b> deve trazer o essencial: o que o projeto faz, como instalar, como rodar, onde pedir ajuda e quem mantém. Documentação longa vai para uma wiki ou para <code>docs/</code>. O GitHub procura o README em <code>.github/</code>, na raiz e em <code>docs/</code>, nessa ordem, e mostra o primeiro que achar; conteúdo acima de 500 KiB é truncado na tela. A <b>licença</b> diz o que os outros podem fazer. <b>Sem licença, o código continua protegido por direito autoral e ninguém tem permissão explícita de usar, copiar ou alterar.</b> O guia de open source cita três licenças populares: MIT (permissiva e curta, exige manter o aviso de copyright e a licença), Apache 2.0 (permissiva, com cláusula de patentes) e GPLv3 (copyleft: quem distribui versão modificada precisa liberá-la sob a mesma licença). Compare opções em <code>choosealicense.com</code>. O arquivo se chama <code>LICENSE</code> ou <code>LICENSE.md</code>, e o GitHub mostra o nome da licença no topo quando a reconhece. <b>Isto não é aconselhamento jurídico</b>: para um caso específico, procure quem entende do assunto. (GitHub Docs e Open Source Guides, lidos em 10/11/2026.)") +
        code('''
# README.md minimo (tres linhas uteis valem mais que um modelo enorme)
# Nome do projeto
O que faz: lista as tarefas da turma e calcula a media.
Como rodar: python app.py   (precisa de Python 3.10 ou superior)
''') +
        naotestado("Escolher a licença pelo site (opção ao criar o repositório, ou “Add file” e “Choose a license template”) está na documentação, mas eu não vi a tela.") +
        erro("README que só diz “projeto de estudo”. Quem chega não sabe nem como rodar. E subir código sem licença esperando que “todo mundo pode usar”: sem licença, a permissão não existe."),
        ponte("A recepção está pronta. E o que não deve nem entrar no repositório?", "O .gitignore e os arquivos que organizam a comunidade."))

    corpo += secao("saude", 3, ".gitignore, arquivos de saúde e templates",
        "Quero que as pessoas saibam como contribuir, como reportar um problema de segurança e o que não é para subir. Onde isso fica escrito?",
        camada("Intuição", "É o regulamento do prédio: o que pode entrar (<code>.gitignore</code> diz o que <b>não</b> entra), como se comportar (código de conduta), como pedir mudança (CONTRIBUTING) e a quem avisar de uma falha grave (SECURITY).") +
        camada("Definição", "O “perfil da comunidade” do GitHub confere se um repositório público tem README, CODE_OF_CONDUCT, CONTRIBUTING, LICENSE, uma política de segurança e templates de issue. Segundo a página sobre arquivos de saúde padrão, <code>CONTRIBUTING.md</code>, <code>CODE_OF_CONDUCT.md</code> e <code>SECURITY.md</code> podem ficar na raiz, em <code>.github/</code> ou em <code>docs/</code>, e o GitHub procura em <code>.github</code> primeiro, depois na raiz, depois em <code>docs</code>. Os <b>templates de issue</b> ficam em <code>.github/ISSUE_TEMPLATE/</code>, em Markdown (cabeçalho com <code>name:</code> e <code>about:</code>) ou em formulário <code>.yml</code> (<code>name:</code> e <code>description:</code>). O <b>template de PR</b> é <code>pull_request_template.md</code>, na raiz, em <code>docs/</code> ou em <code>.github/</code>, e só vale depois de ir para o branch padrão. (GitHub Docs, lido em 10/11/2026.) O <code>.gitignore</code> só vale para arquivo que o Git ainda <b>não</b> rastreia.") +
        tabela(["Arquivo", "Para que serve"], [
            ["<code>README.md</code>", "o que é, como instalar e rodar"],
            ["<code>LICENSE</code>", "o que os outros podem fazer com o código"],
            ["<code>CONTRIBUTING.md</code>", "como contribuir, rodar testes e o que o projeto aceita"],
            ["<code>CODE_OF_CONDUCT.md</code>", "regras de convivência e o que fazer se alguém descumprir"],
            ["<code>SECURITY.md</code>", "a quem e como reportar uma vulnerabilidade, em privado"],
            ["<code>.github/ISSUE_TEMPLATE/</code>", "formulários padronizados para abrir issue"],
            ["<code>.github/pull_request_template.md</code>", "texto que já vem preenchido na descrição de um PR"],
        ]) +
        ex("montando tudo isso num repositório local e conferindo", [
            "Numa pasta nova criei <code>README.md</code>, <code>.gitignore</code> (com <code>node_modules/</code> e <code>segredo.txt</code>), um <code>LICENSE</code> de mentira, um template de issue em Markdown e um <code>pull_request_template.md</code>. Também criei um <code>segredo.txt</code> com um valor falso.",
            "O <code>git status -s</code> listou as pastas e arquivos novos, mas <b>não</b> o <code>segredo.txt</code>: o <code>.gitignore</code> o escondeu. O <code>git check-ignore -v</code> disse qual linha da regra decidiu.",
            "Depois do <code>git add .</code> e do commit, o <code>git ls-files</code> mostrou só os arquivos de saúde. O segredo falso ficou de fora, como queríamos.",
        ]) +
        code('''
$ mkdir -p .github/ISSUE_TEMPLATE
$ git status -s
?? .github/
?? .gitignore
?? LICENSE
?? README.md                         # segredo.txt NAO aparece: foi ignorado
$ git check-ignore -v segredo.txt
.gitignore:2:segredo.txt	segredo.txt   # arquivo:linha:padrao e o arquivo
$ git add . ; git commit -qm "docs: README, LICENSE, gitignore e templates"
$ git ls-files
.github/ISSUE_TEMPLATE/bug.md
.github/pull_request_template.md
.gitignore
LICENSE
README.md
''') +
        SAIDA_LOCAL +
        '<p>Um exemplo de template de issue em Markdown (o formato do cabeçalho vem da documentação; o conteúdo é meu):</p>' +
        code('''
---
name: Relato de bug
about: Algo nao funciona como deveria
labels: bug
---

## O que aconteceu

## Como reproduzir
''') +
        '<p><b>Armadilha no PowerShell 5.1.</b> O operador <code>&gt;</code> pode gravar o <code>.gitignore</code> em UTF-16 e o Git deixa de entender a regra. O teste completo está no <a href="' + TG5 + '">capítulo 5 de Terminal e Git</a> (seção do <code>.gitignore</code>). Aqui basta: grave com <code>Set-Content -Encoding ascii</code> (ou use o Git Bash) e confirme com <code>git status</code>.</p>' +
        naotestado("Não vi o painel de “perfil da comunidade” do GitHub, nem como um template de PR aparece na tela de abrir um PR. A regra de que o template só vale no branch padrão vem da documentação.") +
        erro("Criar o <code>.gitignore</code> <b>depois</b> de já ter feito commit do arquivo secreto. O <code>.gitignore</code> não tira nada do histórico (capítulo 9). Ou escrever <code>.env</code> e esquecer que <code>.env.local</code> é outro arquivo."),
        ponte("O repositório está montado no meu computador, com tudo no lugar. Como ele chega ao GitHub?", "Com um remoto, e com uma forma de provar que sou eu."))

    corpo += aviso_lab() + lab("cap2", "criar o repositório de treino",
        "Este é o exercício 1 da lista: um repositório de treino com README e licença. Nas telas do GitHub, siga o assistente deles (eu não descrevo botões).",
        ["Crie, na sua conta, um repositório <b>público</b> chamado <code>treino-github</code>, com README e a licença que você escolher depois de comparar opções (por exemplo MIT). Anote por que escolheu essa.",
         "No seu computador, crie as pastas <code>.github/ISSUE_TEMPLATE/</code> e os arquivos do exemplo acima: um template de issue e um <code>pull_request_template.md</code>. Crie um <code>.gitignore</code> com <code>segredo.txt</code> e confirme com <code>git check-ignore -v segredo.txt</code>.",
         "Crie um <code>segredo.txt</code> com o texto <code>valor falso</code> (nunca uma credencial verdadeira) e confirme que ele <b>não</b> aparece no <code>git status -s</code>.",
         "Se você usa PowerShell, grave o <code>.gitignore</code> com <code>Set-Content -Encoding ascii</code> e confirme que a regra funcionou.",
         "Prova de que deu certo: o <code>git ls-files</code> lista os arquivos de saúde e <b>não</b> lista o <code>segredo.txt</code>. Quando você enviar (capítulo 3), a página do repositório mostra o nome da licença no topo."])

    fim = fechamento(4,
        ["Público: qualquer um lê, e o que foi publicado <b>não volta</b>. Privado: só quem recebeu acesso.",
         "README: o que é, como instalar, como rodar. <b>Sem licença, ninguém tem permissão explícita de usar o código.</b> MIT e Apache 2.0 são permissivas; GPLv3 é copyleft. Isto não é aconselhamento jurídico.",
         "<code>CONTRIBUTING</code>, <code>CODE_OF_CONDUCT</code> e <code>SECURITY</code> ficam na raiz, em <code>.github/</code> ou em <code>docs/</code> (a busca começa por <code>.github</code>). Templates de issue: <code>.github/ISSUE_TEMPLATE/</code>.",
         "<code>.gitignore</code> só vale para arquivo ainda não rastreado. No PowerShell 5.1 limpo, <code>&gt;</code> pode gravar UTF-16 e quebrar a regra: use <code>Set-Content -Encoding ascii</code>.",
         "<code>git check-ignore -v arquivo</code> diz qual regra decidiu."],
        [quiz(1, "c", "Um repositório público não tem arquivo <code>LICENSE</code>. O que isso significa para quem quer usar o código?", [("a", "Que é de domínio público."), ("b", "Que pode copiar à vontade."), ("c", "Que não há permissão explícita: o código segue protegido por direito autoral.")], "Sem licença, ninguém recebeu permissão. A licença é o que diz o que os outros podem fazer."),
         quiz(2, "b", "Você já fez commit de um <code>segredo.txt</code> e agora o põe no <code>.gitignore</code>. O que acontece?", [("a", "O arquivo some do histórico."), ("b", "O <code>.gitignore</code> não tira do histórico nem do rastreamento do que já foi commitado."), ("c", "O GitHub apaga o commit.")], "O <code>.gitignore</code> só vale para arquivos ainda não rastreados. Para o histórico, veja o capítulo 9."),
         quiz(3, "a", "Onde o GitHub procura o <code>CONTRIBUTING.md</code>, segundo a página de arquivos de saúde?", [("a", "Em <code>.github</code>, depois na raiz, depois em <code>docs</code>."), ("b", "Só na pasta <code>src</code>."), ("c", "Só dentro do README.")], "As três pastas valem, com essa ordem de busca."),
         quiz(4, "c", "Qual comando mostra <b>qual linha</b> do <code>.gitignore</code> decidiu ignorar um arquivo?", [("a", "<code>git status -s</code>"), ("b", "<code>git ls-files</code>"), ("c", "<code>git check-ignore -v arquivo</code>")], "O <code>-v</code> mostra o arquivo, o número da linha e o padrão que casou. O <code>git ls-files</code> só lista o que já é rastreado.")],
        [("O que o README deve ter?", "O que o projeto faz, como instalar, como rodar, onde pedir ajuda e quem mantém."),
         ("Quais as três famílias de licença citadas?", "MIT e Apache 2.0 (permissivas) e GPLv3 (copyleft). Não é aconselhamento jurídico."),
         ("Onde ficam os templates de issue?", "Em <code>.github/ISSUE_TEMPLATE/</code>, em Markdown ou formulário <code>.yml</code>."),
         ("Como saber qual regra do .gitignore pegou um arquivo?", "<code>git check-ignore -v arquivo</code>.")],
        fontes("gh_repos", "gh_readme", "gh_licenca", "gh_comunidade", "gh_health", "gh_prtemplate", "osstart", "gitignore"),
        prox=(3, "Como o GitHub e o meu computador conversam?", "Remoto, clone, fork, fetch, pull, push e autenticação."))
    publicar(2, "repositorio", "O repositório: visibilidade, README, licença e arquivos de saúde",
             "Público ou privado, o que mostrar na porta e como deixar o repositório pronto para quem chega.",
             "No capítulo 1 você deixou a conta e a identidade prontas. A pergunta que ficou: <b>onde o projeto mora e o que faz um repositório ser bem montado?</b> Aqui o repositório é montado primeiro no seu computador, que é onde dá para testar.",
             corpo + fim, 45)


def cap3():
    corpo = ""
    corpo += secao("remoto", 1, "Remoto, origin, main, clone e fork",
        "Quando eu digito <code>git push</code> sem dizer para onde, para onde vai?",
        camada("Intuição", "O remoto é um contato salvo no celular: um apelido para o endereço de outro repositório. O apelido padrão é <code>origin</code> (de “origem”, o lugar de onde você clonou). Clonar é fotocopiar o caderno do outro. Fazer <i>fork</i> é fotocopiar o caderno <b>dentro do prédio</b>, na sua estante, para você poder mexer sem pedir licença.") +
        camada("Definição", "<b>Remoto</b>: apelido para outro repositório; <code>git remote -v</code> mostra as URLs. <b>Clone</b>: cópia para o seu PC; você só consegue dar push se tiver permissão de escrita nele. <b>Fork</b>: cópia do repositório na <b>sua conta</b> do GitHub; você dá push no seu fork e abre um PR para o original, que se chama <i>upstream</i>. É assim que se contribui com projeto de terceiros (capítulo 6). <code>main</code> é o nome da branch padrão de projetos novos: o GitHub passou a criar repositórios com <code>main</code> a partir de 1º de outubro de 2020 (isso eu li em fonte secundária, não no blog oficial, então trate como informação a confirmar). Repositórios antigos não mudam sozinhos. Para o seu Git local criar <code>main</code> em repositórios novos, use <code>git config --global init.defaultBranch main</code>. (GitHub Docs e Pro Git, lidos em 10/11/2026.)") +
        code('''
$ git clone https://github.com/seu-usuario/seu-repo.git        # NAO testado aqui (depende do GitHub)
$ git remote -v
$ git remote add upstream https://github.com/dono-original/repo.git
''') +
        ex("conectar um repositório novo a um remoto e enviar", [
            "Criei um repositório bare (<code>nuvem.git</code>, o papel do GitHub), um projeto com <code>git init -b main</code> e adicionei o remoto: <code>git remote add origin ../nuvem.git</code>.",
            "<code>git push -u origin main</code> enviou e guardou o vínculo (o <code>-u</code>): depois disso, <code>git push</code> e <code>git pull</code> sem argumentos sabem para onde ir.",
            "<code>git branch -vv</code> mostrou <code>[origin/main]</code> ao lado da <code>main</code>: é o vínculo registrado.",
        ]) +
        code('''
$ git init -q -b main projeto ; cd projeto
$ git remote add origin ../nuvem.git
$ git remote -v
origin	../nuvem.git (fetch)
origin	../nuvem.git (push)
$ git push -u origin main
To ../nuvem.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
$ git branch -vv
* main f76f8cc [origin/main] docs: cria README e .gitignore
''') +
        SAIDA_NUVEM +
        erro("Clonar o repositório de outra pessoa e tentar dar push nele. Sem permissão de escrita, o push falha. O caminho é fork + PR. Outro erro: <code>origin</code> apontando para o lugar errado (o original em vez do seu fork); confira com <code>git remote -v</code> e corrija com <code>git remote set-url origin URL</code>."),
        ponte("Já sei onde estão as cópias. E se alguém enviar algo enquanto eu também trabalhei?", "Aí aparece a diferença entre fetch, pull e push."))

    corpo += secao("fetch-pull-push", 2, "fetch, pull, push e a divergência",
        "Um colega enviou um commit enquanto eu fazia o meu. O que acontece quando eu tento sincronizar?",
        camada("Intuição", "<code>fetch</code> é olhar a caixa de correio sem abrir as cartas dentro de casa: você vê o que chegou, e seus arquivos não mudam. <code>pull</code> é buscar e já misturar na sua branch. <code>push</code> é entregar o que você fez.") +
        camada("Definição", "<code>git fetch</code> baixa o que mudou no remoto e atualiza <code>origin/main</code>, <b>sem tocar</b> nos seus arquivos. <code>git pull</code> faz fetch e depois merge (ou rebase, se configurado) na sua branch. <code>git push</code> envia seus commits. Quando os dois lados andaram, a história <b>diverge</b>: o push é recusado (<i>non-fast-forward</i>) e o <code>pull --ff-only</code> falha, porque não dá para só avançar. Aí você escolhe, de propósito, merge ou rebase.") +
        ex("a divergência, rodada de verdade", [
            "Tenho 1 commit local que ainda não enviei. O colega (um segundo clone) envia 1 commit. O <code>git fetch</code> trouxe <code>origin/main</code> novo e o <code>git status -sb</code> mostrou <b>[ahead 1, behind 1]</b>: um à frente, um atrás.",
            "O <code>git pull --ff-only</code> falhou com <code>fatal: Not possible to fast-forward, aborting.</code>: o histórico divergiu, então só avançar é impossível.",
            "O <code>git pull --no-rebase --no-edit</code> funcionou: criou um commit de merge. Em outra rodada, meu <code>git push</code> foi recusado com <code>! [rejected] ... (fetch first)</code> porque o colega tinha enviado antes. A saída é sempre buscar, integrar e enviar de novo.",
        ]) +
        code('''
$ git fetch
From ../nuvem
   f76f8cc..f61146a  main       -> origin/main
$ git status -sb | head -1
## main...origin/main [ahead 1, behind 1]
$ git pull --ff-only
hint: Diverging branches can't be fast-forwarded, you need to either:
hint:
hint: 	git merge --no-ff
hint:
hint: or:
hint:
hint: 	git rebase
hint:
hint: Disable this message with "git config set advice.diverging false"
fatal: Not possible to fast-forward, aborting.
$ git pull --no-rebase --no-edit
Merge made by the 'ort' strategy.
 c.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 c.txt
$ git push origin main                          # numa segunda rodada em que o colega enviou antes
To ../nuvem.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '../nuvem.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
''') +
        SAIDA_NUVEM +
        erro("Tratar <code>--force</code> como a saída do push recusado. Forçar sobrescreve o histórico dos outros. A saída certa é <code>git fetch</code>, integrar (<code>merge</code> ou <code>rebase</code>) e fazer push de novo. E confundir fetch com pull: fetch é seguro para só olhar; o pull altera a sua branch."),
        ponte("Sei sincronizar com um remoto. Mas o GitHub não aceita qualquer um: como ele sabe que sou eu?", "Pela autenticação: token, SSH ou gh."))

    corpo += secao("auth", 3, "Autenticação: token, SSH, gh e o que nunca colar",
        "Digitei a senha da minha conta no <code>git push</code> e deu erro. Por quê?",
        camada("Intuição", "Senha de conta é uma chave-mestra: se ela vazasse num comando, abriria tudo. Então o GitHub passou a pedir <b>chaves específicas</b> para o Git: um token (que você pode limitar e revogar), um par de chaves SSH ou o login do <code>gh</code>.") +
        camada("Definição", "Desde <b>13 de agosto de 2021</b> o GitHub.com não aceita a senha da conta para operações Git: é preciso token de acesso (por exemplo, um token pessoal), chave SSH ou token de instalação de app. (Changelog do GitHub, lido em 10/11/2026.) Os tokens têm prefixos: <code>ghp_</code> (pessoal clássico) e <code>github_pat_</code> (fine-grained). A página de expiração recomenda <b>definir validade</b>; token sem uso por um ano é revogado; dá para revogar a qualquer hora; token enviado por push a repositório público é revogado automaticamente. No <b>SSH</b>, a chave privada fica no seu PC (use senha de chave) e a pública vai para a conta; chave sem uso por um ano é removida. A página não diz qual tipo de chave o GitHub recomenda: Ed25519 é prática comum, mas <b>confira</b>. O <b>Git Credential Manager</b> (<code>credential.helper manager</code>) guarda as credenciais no cofre do Windows.") +
        tabela(["Forma", "Como funciona", "Quando usar"], [
            ["HTTPS com token", "o Git pede usuário e um token no lugar da senha; o gerenciador guarda no cofre", "o caminho mais simples no Windows"],
            ["SSH", "par de chaves: privada no seu PC, pública cadastrada na conta", "quem já usa SSH e não quer digitar token"],
            ["<code>gh auth login</code>", "o <code>gh</code> faz o login e configura o Git para usar o mesmo", "quem usa o <code>gh</code>: o caminho menos manual"],
        ]) +
        ex("gerar um par de chaves descartável, sem cadastrar em lugar nenhum", [
            "No Git Bash: <code>ssh-keygen -t ed25519 -f chave-descartavel -N \"\" -C teste</code> criou o par. O arquivo <code>.pub</code> é a chave pública (começa com <code>ssh-ed25519</code>) e é a única que sai do PC.",
            "No <b>PowerShell 5.1</b> uma string vazia some ao chegar no programa nativo: o <code>-N \"\"</code> precisa virar <code>-N '\"\"'</code>. Com isso funcionou também.",
            "Eu <b>não</b> cadastrei a chave e <b>não</b> rodei <code>ssh -T</code> contra o GitHub.",
        ]) +
        code('''
$ ssh-keygen -t ed25519 -f chave-descartavel -N "" -C teste
Generating public/private ed25519 key pair.
Your identification has been saved in chave-descartavel
Your public key has been saved in chave-descartavel.pub
$ cut -c1-12 chave-descartavel.pub
ssh-ed25519
PS> ssh-keygen -t ed25519 -f chave-ps -N '""' -C teste      # no PS 5.1, a string vazia precisa dessas aspas
Generating public/private ed25519 key pair.
''') +
        '<p>O que o Git grava quando você põe o token <b>dentro da URL</b> do remoto (com um valor falso, claro):</p>' +
        code('''
$ git remote add origin https://usuario:TOKEN_FALSO_AQUI[[@|separa o token do endereco]]github.com/seu-usuario/repo.git
$ grep url .git/config
	url = https://usuario:TOKEN_FALSO_AQUI[[@|separa o token do endereco]]github.com/seu-usuario/repo.git    # em texto puro, no disco
$ git remote set-url origin https://github.com/seu-usuario/repo.git         # a correcao
$ grep url .git/config
	url = https://github.com/seu-usuario/repo.git
''') +
        SAIDA_AUTH +
        '<div class="nota erro"><span class="lbl">O que NUNCA colar, em chat, repositório ou URL</span><ul><li>A senha da conta.</li><li>Um token (<code>ghp_</code>, <code>github_pat_</code>, <code>gho_</code>...). Se colou, <b>revogue antes de qualquer coisa</b>.</li><li>A chave <b>privada</b> SSH (o arquivo sem <code>.pub</code>).</li><li>Um código de recuperação do 2FA.</li><li>O token dentro da URL do remoto: ele fica em <code>.git/config</code> e no histórico do shell.</li><li>Variável de ambiente com segredo em arquivo do repositório.</li></ul>Se um token apareceu em conversa ou em arquivo commitado, a ordem é: revogar, gerar outro, guardar no gerenciador. Só depois, se for o caso, limpar histórico (capítulo 9).</div>' +
        naotestado("Não rodei <code>gh auth login</code>, <code>ssh -T</code> com o GitHub, nem um push HTTPS com token. O <code>gh auth status</code> mostra conta e escopos: não cole a saída em chat. Os nomes e limites de tokens vêm da página lida; os passos de tela eu não vi.") +
        erro("Colar o token no lugar da senha “para ver se vai” e depois deixá-lo no histórico do terminal. Ou receber <code>Permission denied (publickey)</code> e achar que o GitHub caiu: normalmente a chave pública não foi cadastrada, ou a chave certa não está carregada no <code>ssh-agent</code>."),
        ponte("Estou conectado e autenticado. Antes de escrever código, como registro o que precisa ser feito?", "Com issues."))

    corpo += aviso_lab() + lab("cap3", "clonar, ramificar e enviar",
        "Exercício 2 da lista, mais a comparação entre HTTPS e SSH. Use o <code>treino-github</code> do capítulo 2.",
        ["Autentique-se do jeito que preferir (<code>gh auth login</code>, que guia o fluxo, ou um token/SSH pela documentação). <b>Não cole</b> o token em lugar nenhum. Confirme com <code>gh auth status</code> sem copiar a saída para fora do seu terminal.",
         "Clone o repositório por HTTPS. Depois clone <b>outra cópia</b> por SSH (se você configurou SSH). Em cada uma, rode <code>git remote -v</code> e anote a diferença entre as URLs.",
         "Crie a branch <code>feature/teste-1</code>, faça <b>dois</b> commits com mensagens descritivas e rode <code>git push -u origin feature/teste-1</code>.",
         "Compare: <code>git branch -r</code> no terminal e a lista de branches no site do GitHub mostram a mesma branch nova.",
         "Prova de que deu certo: <code>git branch -vv</code> mostra <code>[origin/feature/teste-1]</code>, e o <code>.git/config</code> do clone <b>não</b> contém nenhum token na URL (<code>grep url .git/config</code>)."])

    fim = fechamento(4,
        ["<code>origin</code> é o apelido do remoto de onde você clonou. <code>git remote -v</code> mostra; <code>git push -u</code> grava o vínculo.",
         "<b>Clone</b>: cópia no PC. <b>Fork</b>: cópia na sua conta do GitHub, para contribuir com o que não é seu. O original é o <i>upstream</i>.",
         "<code>fetch</code> só olha; <code>pull</code> = fetch + merge; <code>push</code> envia. Histórico divergente: <code>pull --ff-only</code> falha, e o push é recusado. Resolva com merge ou rebase, não com <code>--force</code>.",
         "Desde 13/08/2021 <b>senha de conta não vale</b> para o Git: token, SSH ou <code>gh</code>. No PowerShell 5.1, <code>-N '\"\"'</code> para senha de chave vazia.",
         "<b>Nunca</b> colar token, chave privada, senha ou código de recuperação em chat, repositório ou na URL do remoto. Vazou: revogar primeiro."],
        [quiz(1, "c", "Você tem commits locais e o colega enviou outro. O que o <code>git pull --ff-only</code> faz?", [("a", "Mistura tudo sem perguntar."), ("b", "Apaga o commit do colega."), ("c", "Falha, porque o histórico divergiu e só avançar é impossível.")], "O <code>--ff-only</code> só aceita avançar. Com divergência, ele recusa e você escolhe merge ou rebase."),
         quiz(2, "a", "Qual comando atualiza <code>origin/main</code> sem mexer nos seus arquivos?", [("a", "<code>git fetch</code>"), ("b", "<code>git pull</code>"), ("c", "<code>git push</code>")], "O fetch só baixa. O pull baixa e integra."),
         quiz(3, "b", "Você tentou dar push por HTTPS com a senha da conta e foi recusado. Por quê?", [("a", "O repositório é privado."), ("b", "Desde 2021 o GitHub não aceita senha da conta para o Git: use token, SSH ou gh."), ("c", "O Git está desatualizado.")], "A mudança foi anunciada no changelog do GitHub de 12/08/2021 e passou a valer em 13/08/2021."),
         quiz(4, "b", "Você pôs o token na URL do remoto. Onde ele fica gravado?", [("a", "Só na memória."), ("b", "Em texto puro no <code>.git/config</code> do repositório."), ("c", "Só no GitHub.")], "Na execução que fiz, o <code>grep url .git/config</code> mostrou a URL com o valor. Use o gerenciador de credenciais.")],
        [("Para que serve o <code>-u</code> no primeiro push?", "Guarda o vínculo com <code>origin/main</code>, para <code>git push</code> e <code>git pull</code> funcionarem sem argumentos."),
         ("Clone x fork?", "Clone é a cópia no seu PC. Fork é uma cópia na sua conta do GitHub, para propor mudança num projeto que você não pode alterar."),
         ("O que nunca colar em chat?", "Senha, token, chave privada, código de recuperação. E nada de token na URL do remoto."),
         ("Push recusado por <i>fetch first</i>: e agora?", "<code>git fetch</code>, integrar com merge ou rebase e fazer push de novo. Sem <code>--force</code>.")],
        fontes("gh_blog_senha", "gh_tokens", "gh_ssh", "gitcred", "progit_dist", "gh_contribuir"),
        prox=(4, "Como planejo o trabalho?", "Issues, labels, milestones e Projects."))
    publicar(3, "remoto-e-autenticacao", "Remoto, clone, fork, fetch, pull, push e autenticação",
             "Como o seu computador conversa com o GitHub, o que muda quando dois lados andam e como provar quem você é sem expor nada.",
             "No capítulo 2 você montou o repositório no seu computador. A pergunta que ficou: <b>como o GitHub e o meu computador passam a conversar, e como ele sabe que sou eu?</b>",
             corpo + fim, 50)
