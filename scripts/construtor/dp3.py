from dp_base import *
S6 = ["demos/dp-core.js", "demos/cap-6.js"]


def cap5():
    corpo = ""
    corpo += secao("preparar", 1, "Antes de publicar: a pasta e o teste local",
        "Tenho três caminhos pela frente. O que é igual em todos eles?",
        camada("Intuição", "Publicar um site estático é entregar uma pasta. Antes de escolher o caminho, a pasta tem de estar certa: o servidor procura um arquivo de entrada e segue os caminhos que você escreveu.") +
        camada("Definição", "Pré-requisitos: um <code>index.html</code> na <b>raiz</b> da pasta publicada, e o CSS, o JS e as imagens com caminhos <b>relativos</b> (<code>estilo.css</code>, não <code>/estilo.css</code>). Servidores Linux tratam <code>Sobre.html</code> e <code>sobre.html</code> como arquivos diferentes. Se o projeto tem etapa de build, o que se publica é a <b>pasta gerada</b> (<code>dist</code>, <code>build</code> ou <code>public</code>), não a do código-fonte.") +
        ex("conferir antes, no computador", [
            "Entre na pasta do site e rode <code>python -m http.server 8765 --bind 127.0.0.1</code>. Abra <code>http://127.0.0.1:8765</code> no navegador. Se abrir direitinho assim, os caminhos funcionam num servidor de verdade.",
            "Conferi com o <code>curl</code>: pedir <code>/</code> deu 200; pedir um nome que não existia deu <b>404</b>, como no capítulo 1.",
            "O mesmo vale no PowerShell: <code>python -m http.server 8765 --bind 127.0.0.1</code> é um comando do Python, igual nos dois shells.",
        ]) +
        code('''
$ python -m http.server 8765 --bind 127.0.0.1     # na pasta do site; Ctrl+C encerra
$ curl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1:8765/
200
$ curl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1:8765/nada
404
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026, num servidor local. Maiúsculas e minúsculas no nome do arquivo (<code>Index.html</code> contra <code>index.html</code>) <b>dependem do sistema</b>: segundo a minha pesquisa de apoio, num servidor Linux são arquivos diferentes. Não testei num Linux.</p>' +
        erro("Caminho absoluto que só funciona na raiz do domínio. Um erro comum: um <code>/estilo.css</code> funciona quando o site mora em <code>meusite.example/</code>, mas quebra quando mora em <code>usuario.github.io/projeto/</code> (subpasta). Use caminho relativo, e abra o site publicado para conferir o CSS carregando."),
        ponte("A pasta está pronta e testada. Qual é o caminho mais curto até o ar?", "Pelo GitHub Pages, que usa o Git que você já conhece."))

    corpo += secao("caminho-a", 2, "Caminho A: GitHub Pages",
        "Já uso Git e GitHub. Dá para o site sair do repositório?",
        camada("Intuição", "O GitHub Pages lê uma pasta de uma branch do seu repositório e publica o conteúdo como site. Atualizar é dar <code>git push</code>.") +
        camada("Definição", "Segundo a documentação do GitHub (lida em 06/11/2026): em <b>Settings</b> do repositório existe a seção <b>Pages</b>, onde se escolhe publicar a partir de uma <b>branch</b> e de uma <b>pasta</b> (por exemplo, <code>/docs</code> da <code>main</code>). O arquivo de entrada (<code>index.html</code>) precisa estar no topo da pasta escolhida. Mudanças podem levar até <b>10 minutos</b> para aparecer. Para donos de conta no plano Free, o repositório precisa ser <b>público</b>. Quando se publica a partir de uma branch, o GitHub Pages usa o Jekyll por padrão para montar o site; a documentação diz que um arquivo vazio chamado <code>.nojekyll</code> na raiz da fonte de publicação desliga isso (confirmado na leitura de 06/11/2026).") +
        ex("o Git de ponta a ponta, rodado em um remoto de mentira", [
            "Não posso empurrar para um GitHub de verdade (isso seria publicar algo). Então criei um repositório \"remoto\" numa pasta local (<code>git init --bare</code>) e repeti os comandos que você usaria: <code>git init</code>, <code>add</code>, <code>commit</code>, <code>branch -M main</code>, <code>remote add origin</code> e <code>push -u origin main</code>.",
            "A saída confirmou: <code>[new branch] main -> main</code> e <code>branch 'main' set up to track 'origin/main'</code>. O <code>git status -sb</code> ficou em <code>## main...origin/main</code>, sem diferença entre local e remoto.",
            "Contra o GitHub de verdade, a única diferença é a URL do <code>origin</code>, que fica <code>https://github.com/SEU_USUARIO/SEU_REPO.git</code> (e o login).",
        ]) +
        code('''
$ git init -q -b main            # o -b main escolhe o nome da branch inicial
$ git add .
$ git commit -qm "Primeira versao do site"
$ git branch -M main
$ git remote add origin ../remoto.git     # no GitHub: https://github.com/SEU_USUARIO/SEU_REPO.git
$ git push -u origin main
To ../remoto.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
$ git remote -v
origin	../remoto.git (fetch)
origin	../remoto.git (push)
$ git status -sb
## main...origin/main
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026, num remoto local. Usei só um texto de teste e nenhuma conta do GitHub.</p>' +
        naotestado("O <code>push</code> para o GitHub, ativar o Pages em Settings e abrir o endereço gerado <b>não foram feitos</b>. Também não descrevo botões ou telas do painel: a documentação diz onde fica a opção, mas não lista os rótulos exatos do menu, e eu não vi a tela. Siga a documentação oficial atual.") +
        erro("Esperar a mudança aparecer na hora. A documentação fala em até 10 minutos, e o navegador ainda pode mostrar a versão guardada. Teste em aba anônima antes de achar que o push falhou. E lembre-se de que o conteúdo é <b>público</b>: tire do repositório o que não pode ser visto (veja o capítulo 6)."),
        ponte("O GitHub Pages serve bem para um site simples. E se eu quiser ligar o deploy a uma plataforma própria para sites?", "Com Cloudflare Pages, Netlify ou Vercel."))

    corpo += secao("caminho-b", 3, "Caminho B: plataforma de deploy (Cloudflare Pages, Netlify ou Vercel)",
        "Quero uma plataforma feita para publicar sites. O que elas têm em comum?",
        camada("Intuição", "Você entrega a pasta (arrastando, enviando por comando ou conectando o repositório) e a plataforma devolve um endereço. As três fazem o trabalho de servidor por você: é PaaS (capítulo 4) especializado em sites.") +
        camada("Definição", "O que cada documentação oficial diz (lidas em 06/11/2026, exceto a da Vercel, lida na pesquisa de apoio do mesmo dia):") +
        tabela(["Plataforma", "Formas de enviar o site, segundo a documentação"], [
            ["Cloudflare Pages", "arrastar a pasta no painel (Direct Upload) ou usar a linha de comando do <code>wrangler</code>"],
            ["Netlify", "arrastar a pasta, conectar um repositório Git (cada push publica de novo) ou usar a CLI; a página lida não lista os comandos da CLI"],
            ["Vercel", "Git (a cada push), CLI, arrastar a pasta ou API"],
        ]) +
        '<p>Para o Cloudflare Pages, a documentação (Direct Upload) traz o <code>wrangler pages deploy</code> e o <code>--branch</code> para preview, que conferi na leitura de 06/11/2026; o <code>login</code> e o <code>project create</code> vêm da pesquisa de apoio do mesmo dia. Os passos de linha de comando (<code>NOME_DA_PASTA</code> é a pasta com o site pronto). O mesmo funciona no Git Bash e no PowerShell:</p>' +
        code('''
$ npx wrangler login                          # abre o navegador para você entrar na conta
$ npx wrangler pages project create           # pergunta o nome do projeto e a branch de produção
$ npx wrangler pages deploy NOME_DA_PASTA     # envia a pasta e publica
$ npx wrangler pages deploy NOME_DA_PASTA --branch=teste   # publica uma versão de teste (preview)
''') +
        naotestado("Esses quatro comandos vêm da documentação do Cloudflare e <b>eu não os rodei</b>: exigem uma conta e criam um projeto de verdade. Segundo a página lida em 06/11/2026, o limite de <b>25 MiB por arquivo</b> vale tanto para o Wrangler quanto para o envio pelo painel; o de <b>20.000 arquivos</b> é do Wrangler (o painel tem outro, de 1.000 arquivos). Conferir de novo na hora de usar. Para Netlify e Vercel eu só li as formas de enviar, não rodei nenhuma e não mostro comandos da CLI, porque as páginas que li não os trazem.") +
        erro("Publicar a pasta errada. Se há etapa de build, o diretório de saída (<code>dist</code>, <code>build</code>, <code>public</code>) é o que se envia, não a pasta do código-fonte. Outro tropeço é arquivo grande demais (acima do limite do plano): comprima as imagens antes. Quanto a custo e plano gratuito, <b>confira na página oficial de cada serviço</b>; eu não afirmo nenhum número."),
        ponte("As plataformas escondem o servidor. E se eu quiser o servidor, com o nginx e tudo?", "Com um VPS."))

    corpo += secao("caminho-c", 4, "Caminho C: um VPS com nginx, SSH e scp ou rsync",
        "Quero entender o que a plataforma faz por baixo. Como eu mesmo ponho um site no ar numa máquina minha?",
        camada("Intuição", "É montar a loja inteira: alugar o espaço (o VPS), pôr o balcão (o servidor web, o <b>nginx</b>), arrumar a mercadoria (os arquivos) e colocar a placa na rua (o DNS). Tudo é seu: o bom e os problemas.") +
        camada("Definição", "O <b>nginx</b> é um servidor web: ele escuta a porta 80, olha o endereço pedido e entrega arquivos de uma pasta (<code>root</code>). Cada site é descrito num bloco <code>server</code>, com blocos <code>location</code> para os caminhos. Depois de mudar a configuração é preciso <b>recarregar</b> (<code>nginx -s reload</code>); se a configuração tiver erro, o nginx mantém a antiga funcionando. (nginx.org.) Para chegar à máquina usa-se o <b>SSH</b> (porta 22), e para levar arquivos, <code>scp</code> ou <code>rsync</code>.") +
        naotestado("<b>Tudo desta seção é exemplo e não foi rodado.</b> Eu não tenho um VPS, o nginx e o rsync não estão instalados aqui e não consegui contratar nada. Os comandos seguem a documentação do nginx e o conhecimento geral de Ubuntu; os valores em maiúsculas (<code>IP_DO_SERVIDOR</code>, <code>USUARIO</code>) são lugares para você trocar.") +
        ex("a sequência, em ordem", [
            "Contratar um VPS com Ubuntu, anotar o IP e cadastrar sua chave SSH pública (veja a apostila de <a href='../terminal-git/index.html'>Terminal e Git</a>, capítulo sobre SSH). Preço: confira com o provedor.",
            "Conectar: <code>ssh USUARIO@IP_DO_SERVIDOR</code>. Instalar o servidor: <code>sudo apt update</code> e <code>sudo apt install nginx</code>.",
            "Criar a pasta de destino no servidor (<code>mkdir -p</code>) e levar os arquivos do seu computador com <code>scp</code> (cópia simples) ou <code>rsync</code> (copia só o que mudou), sem esquecer os arquivos que começam com ponto.",
            "Configurar o nginx (exemplo abaixo), <b>ativar o site</b> (link em <code>sites-enabled</code>), testar a configuração, recarregar e apontar o DNS (um registro <b>A</b>, capítulo 2) para o IP do VPS.",
            "Liberar as portas 22, 80 e 443 no firewall e ativar HTTPS (capítulo 3).",
        ]) +
        code('''
# EXEMPLO, nao testado (nao ha VPS aqui). No seu computador (Git Bash ou PowerShell, os dois tem scp/ssh):
# 1) cria a pasta de destino no servidor (o scp nao cria a pasta pai)
$ ssh USUARIO@IP_DO_SERVIDOR "mkdir -p /home/USUARIO/meu-site"
# 2) copia a pasta inteira; o "/." no fim leva tambem os arquivos que comecam com ponto (.nojekyll, .htaccess)
$ scp -r ./meu-site/. USUARIO@IP_DO_SERVIDOR:/home/USUARIO/meu-site/
# alternativa que copia so o que mudou (precisa de rsync nos dois lados; o -n so simula):
$ rsync -avzn --delete ./meu-site/ USUARIO@IP_DO_SERVIDOR:/home/USUARIO/meu-site/
# No servidor, depois do ssh. /var/www e do root: por isso copiamos para a home e usamos sudo
$ sudo mkdir -p /var/www/meusite
$ sudo cp -r /home/USUARIO/meu-site/. /var/www/meusite/
# ativa o site no nginx (Ubuntu/Debian: o nginx so carrega o que esta em sites-enabled)
$ sudo ln -s /etc/nginx/sites-available/meusite /etc/nginx/sites-enabled/meusite
$ sudo rm /etc/nginx/sites-enabled/default     # tira o site padrao do ar (so o link; o arquivo original fica)
$ sudo nginx -t                    # testa a configuracao (comando conhecido; a pagina lida do nginx nao o cita)
$ sudo systemctl reload nginx      # ou: nginx -s reload, como na documentacao
''') +
        '<p>Duas notas sobre esse bloco, ambas <mark class="hl p">não testadas aqui</mark>. (1) <b>Permissão:</b> a pasta <code>/var/www</code> pertence ao root, então um <code>scp</code> ou <code>rsync</code> direto para <code>/var/www/meusite</code> com o seu usuário comum dá <i>permission denied</i>. Os jeitos usuais são: copiar para a sua home e mover com <code>sudo</code> (como acima), ou dar a pasta ao seu usuário uma vez (<code>sudo chown -R USUARIO: /var/www/meusite</code>) e aí copiar direto, ou ainda <code>rsync --rsync-path="sudo rsync"</code> (exige <code>sudo</code> sem senha). (2) <b>Ativar o site:</b> em Ubuntu e Debian, o arquivo em <code>sites-available</code> só vale depois do link simbólico em <code>sites-enabled</code>. Sem ele, o <code>nginx -t</code> passa (a configuração antiga está certa) e você continua vendo a <b>página padrão</b> do nginx. Mesmo com o link, o site <code>default</code> costuma atender qualquer nome que não bata com algum <code>server_name</code> (inclusive o acesso pelo IP): por isso removi o link dele, ou então marque o seu bloco com <code>listen 80 default_server;</code>. Em outras distribuições a organização das pastas muda: veja a documentação da sua.</p>' +
        '<p>O arquivo de configuração do site (por exemplo, <code>/etc/nginx/sites-available/meusite</code>). Esta é a configuração de exemplo, no formato do guia do nginx:</p>' +
        code('''
# EXEMPLO de configuracao, nao testado
server {
    listen 80;
    server_name seudominio.example;     # troque pelo seu dominio
    root /var/www/meusite;              # a pasta com index.html
    index index.html;

    location / {
        try_files $uri $uri/ =404;      # arquivo, depois pasta, senao 404
    }
}
''') +
        tabela(["", "A: GitHub Pages", "B: Cloudflare, Netlify ou Vercel", "C: VPS com nginx"], [
            ["Quem cuida do servidor", "o GitHub", "a plataforma", "você"],
            ["Esforço inicial", "baixo", "baixo", "alto"],
            ["Atualizar o site", "<code>git push</code>", "arrastar, CLI ou push", "<code>scp</code>/<code>rsync</code> (ou CI, capítulo 6)"],
            ["Quando escolher", "portfólio e documentação", "site estático com deploy automático", "controle total e aprender administração"],
            ["O que eu testei", "o Git até o push (em remoto local)", "nada (só li a documentação)", "nada (só exemplo)"],
        ]) +
        erro("Quatro tropeços de VPS. (1) <b>Mudar a configuração e não recarregar</b>: nada muda até o reload. (2) <b>Porta bloqueada</b>: o nginx roda, mas o firewall não libera 80/443. (3) <b>Permissão negada</b>: o seu usuário não escreve em <code>/var/www</code> (é do root), e o usuário do nginx precisa conseguir <i>ler</i> os arquivos. (4) <b>Esquecer o link em sites-enabled</b>: aparece a página padrão do nginx. E o cuidado de ouro: o <code>--delete</code> do rsync <b>apaga no destino</b> o que não existe na origem. Rode antes com <code>-n</code> (simulação), sempre."),
        ponte("Os três caminhos funcionam, mas à mão. E se cada push publicar sozinho, sem eu digitar a senha da plataforma?", "Com CI/CD e segredos."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "Antes de tudo: <code>index.html</code> na raiz, caminhos <b>relativos</b> e teste local com <code>python -m http.server</code>.",
        "Se há build, publique a pasta <b>gerada</b> (<code>dist</code>, <code>build</code>, <code>public</code>).",
        "<b>GitHub Pages</b>: publica uma branch/pasta do repositório; mudanças podem levar até 10 minutos; plano Free exige repositório público.",
        "<b>Plataformas</b> (Cloudflare, Netlify, Vercel): você entrega a pasta ou conecta o Git; a plataforma serve.",
        "<b>VPS</b>: você cuida de ssh, nginx, firewall, DNS e HTTPS. Configuração só vale depois do <b>reload</b>.",
        "<code>rsync --delete</code> apaga no destino: simule antes com <code>-n</code>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Seu site abre no seu computador, mas depois de publicado o CSS não carrega. Qual a causa mais provável?", [("a", "O servidor não suporta CSS."), ("b", "O DNS está errado."), ("c", "O caminho do CSS é absoluto (<code>/estilo.css</code>) e o site mora numa subpasta, ou o nome do arquivo difere em maiúsculas.")], "Caminho absoluto só funciona quando o site está na raiz do domínio. E em Linux, <code>Estilo.css</code> e <code>estilo.css</code> são arquivos diferentes.") + \
        quiz(2, "a", "Você editou o arquivo de configuração do nginx e nada mudou no site. O que falta?", [("a", "Testar e recarregar a configuração."), ("b", "Reiniciar o computador do visitante."), ("c", "Trocar o navegador.")], "O nginx só aplica a nova configuração depois do reload. Se a configuração tiver erro, ele mantém a antiga.") + \
        quiz(3, "b", "Por que simular o <code>rsync</code> com <code>-n</code> antes de rodar com <code>--delete</code>?", [("a", "Porque o <code>-n</code> deixa mais rápido."), ("b", "Porque o <code>--delete</code> apaga no destino o que não existe na origem, e a simulação mostra o que seria apagado."), ("c", "Porque sem o <code>-n</code> o rsync não conecta.")], "Rodar direto pode apagar arquivos do servidor que você queria manter. A simulação mostra tudo antes.") + \
        flash([
            ("O que o GitHub Pages precisa para publicar?", "Uma branch e uma pasta do repositório, com <code>index.html</code> no topo dela. Plano Free: repositório público."),
            ("Por que usar caminhos relativos no site?", "Porque o caminho absoluto <code>/arquivo</code> quebra quando o site mora numa subpasta."),
            ("O que fazer depois de mudar a configuração do nginx?", "Testar e recarregar (<code>nginx -s reload</code>); sem isso a mudança não vale."),
            ("Qual a diferença de scp e rsync?", "O scp copia tudo. O rsync copia só o que mudou (e com <code>--delete</code> remove o que sobrou no destino).")]) + \
        fontes("gh_pages", "cf_pages", "netlify", "vercel", "nginx", "openssh", "ibm_vps") + \
        ponte("Sei publicar à mão. Falta automatizar sem vazar a senha da plataforma.", "Com CI/CD e segredos.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
    recap_html = recap("No capítulo 4 você escolheu o tipo de hospedagem. A pergunta agora é concreta: <b>como o site chega lá?</b> Este capítulo, <b>complemento</b> como os demais, mostra três caminhos, e diz com franqueza o que eu rodei e o que só li.")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 5, "publicar-site-estatico", TITULO, "Publicar um site estático por três caminhos", "Capítulo 5 · Complemento",
            "GitHub Pages, uma plataforma de deploy e um VPS com nginx, com os comandos e o aviso de cada um.",
            chips(body, 50), body, scripts=[])


def cap6():
    corpo = ""
    corpo += secao("cicd", 1, "CI/CD e DevOps: deploy a cada push",
        "Publicar à mão funciona uma vez. E na vigésima, com três pessoas mexendo no mesmo site?",
        camada("Intuição", "É uma esteira de fábrica. Cada vez que alguém envia código, uma máquina roda a mesma lista de tarefas: baixar, instalar, testar, montar. Se um teste quebrar, a esteira para antes de publicar algo quebrado.") +
        camada("Definição", "<b>Integração contínua (CI)</b>: enviar código com frequência e rodar build e testes a cada envio. <b>Entrega contínua</b>: o código fica sempre <i>pronto</i> para subir, mas uma pessoa aprova. <b>Implantação contínua</b>: sobe para produção automaticamente, sem aprovação. <b>DevOps</b> é o conjunto de práticas e cultura que une desenvolvimento e operação, e inclui infraestrutura como código e monitoramento. (IBM.)") +
        '<div class="demo" data-demo="pipelineSim"></div>' +
        ex("lendo a esteira simulada", [
            "A esteira tem <b>5 etapas</b>: baixar o código, instalar dependências, rodar os testes, gerar o build e publicar.",
            "Com os testes passando, no modo <b>só CI</b>, as 4 primeiras passam e a etapa 5 \"não roda\": o resultado é o aviso de que está tudo certo.",
            "No modo <b>entrega contínua</b>, a etapa 5 fica <b>aguardando</b> até alguém aprovar. No modo <b>implantação contínua</b>, ela roda sozinha, e <b>falha</b> se o segredo de deploy não estiver cadastrado.",
            "Se os testes falham, as etapas 4 e 5 ficam \"não rodou\" e o site no ar continua sendo a versão anterior. É esse o valor da esteira.",
        ]) +
        '<p>Um exemplo de arquivo de workflow do GitHub Actions com essas 5 etapas. Eu conferi que o YAML é válido (um parser leu 1 job e 5 passos), mas <b>não rodei</b> no GitHub:</p>' +
        code('''
# .github/workflows/publicar.yml   (EXEMPLO, nao rodou no GitHub)
name: publicar
on:
  push:
    branches: [main]
jobs:
  build-e-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4          # confira a versao atual da action
      - name: Instalar dependencias
        run: npm ci
      - name: Rodar os testes
        run: npm test
      - name: Gerar o build
        run: npm run build
      - name: Publicar
        run: ./deploy.sh dist              # seu script de deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}   # veio do cofre do GitHub, nunca do repositorio
''') +
        naotestado("Esse workflow é um <b>exemplo genérico</b>. O <code>deploy.sh</code> não existe, os comandos <code>npm</code> supõem um projeto Node e a versão da action pode estar desatualizada. A documentação do GitHub diz que o segredo é criado em <b>Settings</b>, na parte de segurança, em <b>Secrets and variables</b> e depois <b>Actions</b> (lida em 06/11/2026); não vi a tela.") +
        erro("Fazer a esteira publicar mesmo com o teste falhando (por exemplo, deixando o deploy numa etapa que não depende do teste). O sentido da CI é <b>barrar</b>. Na demo, derrube os testes no modo de implantação contínua e veja que nada vai ao ar."),
        ponte("A esteira precisa de uma credencial para publicar. Onde ela mora, se não pode ficar no código?", "Em variáveis de ambiente e segredos."))

    corpo += secao("variaveis", 2, "Variáveis de ambiente e segredos",
        "Meu programa precisa de uma senha de banco, uma chave de API. Onde eu escrevo isso?",
        camada("Intuição", "No código, <b>nunca</b>. Código vai para o repositório, o repositório pode ser público e o histórico guarda tudo. O valor sensível mora <b>fora</b> do código, em um lugar que o programa consulta na hora de rodar: a <b>variável de ambiente</b>.") +
        camada("Definição", "<b>Variável de ambiente</b> é um par nome/valor que o sistema entrega ao programa quando ele começa. O mesmo código roda em lugares diferentes (seu computador, a esteira, a produção) com valores diferentes, sem mudar uma linha. <b>Segredo</b> é um valor sensível (senha, token, chave). Boas práticas de gestão de segredos, segundo a IBM: cofre central, rotação (trocar de tempos em tempos), mínimo privilégio e registro de acesso. A IBM não trata de variáveis de ambiente como tema próprio; o uso aparece no tutorial do Code Engine.") +
        ex("a mesma variável, nos dois shells", [
            "Programa de teste: um script Node de uma linha que mostra a variável <code>PORTA</code>.",
            "No <b>Git Bash</b>: <code>PORTA=8080 node -e '...'</code> define a variável só para aquele comando. Resultado: <code>porta: 8080 | outra: undefined</code>. Uma variável que não foi definida (<code>OUTRA</code>) aparece como <code>undefined</code>, e não dá erro.",
            "No <b>PowerShell</b>: <code>$env:PORTA = \"8080\"</code> define na sessão; <code>Remove-Item Env:PORTA</code> tira. Rodei o mesmo script antes e depois: <code>porta: 8080</code> e <code>porta: undefined</code>.",
        ]) +
        code('''
$ PORTA=8080 node -e 'console.log("porta:", process.env.PORTA, "| outra:", process.env.OUTRA)'
porta: 8080 | outra: undefined
PS> "console.log('porta:', process.env.PORTA)" | Set-Content -Encoding ascii t.js   # um arquivo de teste
PS> $env:PORTA = "8080"; node t.js
porta: 8080
PS> Remove-Item Env:PORTA; node t.js
porta: undefined
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026, em pasta temporária. No PowerShell, <code>node -e</code> com aspas é chato de escrever, por isso usei um arquivo. As variáveis aqui valem só para a sessão; gravar variável permanente no Windows não foi testado.</p>' +
        '<p>Em plataformas e em esteiras, a variável é cadastrada no painel ou no cofre de segredos do serviço (no GitHub Actions, a sintaxe <code>${{ secrets.NOME }}</code> do exemplo acima). Conteúdo de segredo <b>pode aparecer em log</b> se você mandar imprimir: não imprima.</p>' +
        erro("Colocar a chave \"só para testar\" direto no código e prometer tirar depois. O <b>histórico do Git guarda</b> mesmo que você apague no commit seguinte (a seção 4 mostra isso rodando). Se o repositório for público, qualquer um lê. Se um dia a chave real entrar no código, trate como vazada."),
        ponte("Se o segredo fica fora do código, como evito que um arquivo local com segredos suba por engano?", "Com o .gitignore."))

    corpo += secao("gitignore", 3, ".env, .gitignore e a armadilha do PowerShell",
        "Tenho um arquivo local com as variáveis. Como garanto que o Git nunca o envie?",
        camada("Intuição", "O <code>.gitignore</code> é a lista de \"não levar\" do Git. Entra o que é segredo (<code>.env</code>), o que é gerado (<code>node_modules/</code>, <code>dist/</code>) e o que é só seu. O que vai para o repositório é um <b>modelo sem valores</b>, o <code>.env.example</code>, para quem clonar saber quais variáveis precisa criar.") +
        camada("Definição", "<code>.env</code> é, por convenção, um arquivo de texto com linhas <code>NOME=valor</code> que alguns programas leem no início. O <code>.gitignore</code> usa padrões: <code>.env*</code> casa com <code>.env</code> e <code>.env.local</code>, e uma linha <code>!.env.example</code> reabre uma exceção. O comando <code>git check-ignore -v arquivo</code> diz qual regra decidiu, mesmo que o arquivo nem exista. (Git, documentação do gitignore.)") +
        ex("testar as regras sem criar o arquivo de segredo", [
            "Num repositório temporário, escrevi um <code>.gitignore</code> com <code>.env*</code>, <code>!.env.example</code> e <code>node_modules/</code>. Não criei nenhum arquivo <code>.env</code>: o <code>check-ignore</code> responde pelo caminho.",
            "<code>.env</code> e <code>.env.local</code> casam com a regra da linha 1: <b>ignorados</b>. <code>.env.example</code> casa com a linha 2, que começa com <code>!</code>: <b>não é ignorado</b>, vai para o repositório.",
            "Um erro típico: usar só <code>.env</code> no <code>.gitignore</code>. Com ele, <code>.env</code> é ignorado, mas <code>.env.local</code> <b>não</b> (testei: o <code>git check-ignore</code> não achou regra e saiu com código 1).",
        ]) +
        code('''
$ printf '.env*\\n!.env.example\\nnode_modules/\\n' > .gitignore
$ git check-ignore -v .env
.gitignore:1:.env*	.env
$ git check-ignore -v .env.local
.gitignore:1:.env*	.env.local
$ git check-ignore -v .env.example
.gitignore:2:!.env.example	.env.example         # o "!" mostra que a regra libera este arquivo
$ printf '.env\\n' > .gitignore ; git check-ignore -v .env.local ; echo "codigo: $?"
codigo: 1                                            # .env.local NAO foi ignorado
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026. Note que o <code>check-ignore</code> sai com código 0 mesmo quando a regra é uma exceção com <code>!</code>; leia o texto da saída, não só o código.</p>' +
        '<p><b>A armadilha do PowerShell.</b> Num PowerShell 5.1 limpo (<code>powershell.exe -NoProfile</code>), o operador <code>&gt;</code> grava o arquivo em <b>UTF-16</b> (bytes iniciais 255,254). O Git espera texto simples, e o <code>.gitignore</code> deixa de funcionar. Eu rodei dos dois jeitos num repositório temporário, com uma pasta <code>node_modules</code> de verdade:</p>' +
        code('''
PS> "node_modules/" > .gitignore
PS> [IO.File]::ReadAllBytes(".gitignore")[0..7] | ForEach-Object { '{0:X2}' -f $_ }    # primeiros bytes
FF FE 6E 00 6F 00 64 00                      # FF FE = marca de UTF-16; cada letra ocupa 2 bytes
PS> git status --short
?? .gitignore
?? index.html
?? node_modules/                            # o Git NAO entendeu a regra: a pasta apareceu

PS> "node_modules/" | Set-Content -Encoding ascii .gitignore
PS> git status --short
?? .gitignore
?? index.html                               # agora node_modules/ sumiu: foi ignorada
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026 com <code>powershell.exe -NoProfile</code> (5.1) e Git 2.56. Testei quatro jeitos numa pasta temporária com <code>node_modules</code> de verdade: <code>&gt;</code> gravou UTF-16 e o Git <b>não</b> ignorou a pasta; <code>Set-Content -Encoding ascii</code> funcionou; <code>Set-Content -Encoding utf8</code> e <code>Out-File -Encoding utf8</code> gravaram UTF-8 <b>com BOM</b> (bytes 239,187,191) e <b>neste Git também funcionou</b>. Eu não provei por que o <code>&gt;</code> se comporta diferente em outras máquinas (perfil, versão do PowerShell), então não afirmo a causa: o resultado pode variar, e a regra segura é gravar com <code>Set-Content -Encoding ascii</code>, que foi o jeito testado e não depende de BOM. No Git Bash o <code>&gt;</code> não tem esse problema.</p>' +
        erro("Criar o <code>.gitignore</code> <b>depois</b> de já ter feito commit do arquivo. O <code>.gitignore</code> só vale para arquivos que o Git ainda não rastreia. Quem já foi commitado continua no histórico (próxima seção)."),
        ponte("E se, mesmo assim, o segredo foi commitado?", "Aí o plano é outro."))

    corpo += secao("vazou", 4, "Se o segredo foi commitado",
        "Commitei uma chave sem querer. Apago o arquivo e tudo certo?",
        camada("Intuição", "Não. É como mandar uma carta e perceber o erro: tirar a carta da sua mesa não a tira da caixa do correio. O Git guarda o histórico, e quem clonou antes, ou um robô que varre repositórios públicos, já pode ter copiado.") +
        camada("Definição", "<code>git rm --cached arquivo</code> tira o arquivo do <b>rastreamento atual</b>, mas o commit antigo continua no histórico, e o conteúdo dele continua legível. Limpar o histórico (com ferramentas como <code>git filter-repo</code> ou BFG) reduz o risco, mas não desfaz o que já foi copiado. Por isso, o passo obrigatório é <b>revogar e trocar a credencial</b>: no serviço que emitiu a chave, invalide a antiga e crie outra. A IBM recomenda rotação e mínimo privilégio como práticas de segredos.") +
        ex("o segredo ainda está no histórico, rodado", [
            "Num repositório temporário, criei um arquivo com um valor <b>falso</b> (<code>CHAVE_FALSA_123</code>) e fiz o commit \"sem querer\".",
            "Depois pus o nome do arquivo no <code>.gitignore</code>, rodei <code>git rm --cached</code> e fiz um segundo commit. O <code>git status</code> ficou limpo: parece resolvido.",
            "Mas o <code>git log --all --oneline -S CHAVE_FALSA_123</code> listou <b>2 commits</b> que mexeram nessa string, e o <code>git show HEAD~1:segredo.txt</code> imprimiu a chave. O valor segue legível no commit anterior.",
        ]) +
        code('''
$ echo "CHAVE_FALSA_123" > segredo.txt ; git add . ; git commit -qm "sem querer"
$ echo "segredo.txt" > .gitignore ; git rm -q --cached segredo.txt ; git add .gitignore ; git commit -qm "tira do rastreio"
$ git status --short                    # vazio: parece que acabou
$ git log --all --oneline -S CHAVE_FALSA_123
262811c tira do rastreio
5d93383 sem querer
$ git show HEAD~1:segredo.txt
CHAVE_FALSA_123                         # continua ali, no commit anterior
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026, com valor inventado. Os hashes mudam a cada pessoa.</p>' +
        tabela(["Ordem", "O que fazer se vazou"], [
            ["1", "<b>Revogar e trocar a credencial</b> no serviço de origem. É o passo que realmente fecha a porta."],
            ["2", "Guardar a nova em variável de ambiente ou cofre, nunca no código."],
            ["3", "Pôr o arquivo no <code>.gitignore</code> e remover do rastreamento (<code>git rm --cached</code>)."],
            ["4", "Se quiser, limpar o histórico (<code>git filter-repo</code> ou BFG) e avisar quem clonou."],
            ["5", "Olhar o log de acesso do serviço para ver se alguém usou a chave."],
        ]) +
        naotestado("A limpeza de histórico (<code>git filter-repo</code>, BFG) e <code>git push --force</code> <b>não foram testados aqui</b>. São operações que reescrevem o histórico compartilhado; faça com cuidado e combine com a equipe antes.") +
        erro("Achar que o passo 3 resolve. Ele só impede um <i>novo</i> vazamento. Quem tem acesso ao histórico antigo continua vendo a chave. Sem o passo 1, a chave segue valendo."),
        ponte("O site está no ar, publica sozinho e os segredos estão guardados. O que olhar depois?", "Monitorar, ler logs e saber voltar atrás."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>CI</b>: build e testes a cada envio. <b>Entrega contínua</b>: pronto para subir, com aprovação. <b>Implantação contínua</b>: sobe sozinho.",
        "Teste falhou: a esteira <b>barra</b> o deploy; o site no ar continua na versão anterior.",
        "Segredo <b>não</b> vai no código. Mora em variável de ambiente ou cofre (no GitHub Actions: <code>secrets</code>).",
        "<code>.env</code> no <code>.gitignore</code>; no repositório vai o <code>.env.example</code> sem valores. O padrão <code>.env*</code> cobre <code>.env.local</code> e <code>.env</code> sozinho, não.",
        "PowerShell 5.1: o <code>&gt;</code> pode gravar UTF-16 e quebrar o <code>.gitignore</code>. Use <code>Set-Content -Encoding ascii</code> (testado); <code>utf8</code> grava BOM, que funcionou no meu Git mas não é a opção segura.",
        "<code>git rm --cached</code> <b>não</b> tira do histórico. O passo obrigatório é <b>revogar e trocar a credencial</b>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Na demo, no modo <b>implantação contínua</b>, os testes falham. O que acontece com o site no ar?", [("a", "É atualizado, mas com um aviso."), ("b", "Nada é publicado; continua a versão anterior."), ("c", "É apagado.")], "A esteira para na etapa dos testes. As etapas de build e de publicar não rodam.") + \
        quiz(2, "c", "Você commitou uma chave de API e logo fez <code>git rm --cached</code> num commit seguinte. O que ainda precisa ser feito, obrigatoriamente?", [("a", "Nada: o arquivo saiu do rastreamento."), ("b", "Apagar a pasta <code>.git</code>."), ("c", "Revogar a chave e criar outra, porque ela continua no histórico.")], "O histórico guarda o conteúdo antigo. A chave precisa ser invalidada no serviço que a emitiu.") + \
        quiz(3, "a", "O <code>.gitignore</code> tem só a linha <code>.env</code>. O que acontece com um arquivo <code>.env.local</code>?", [("a", "Não é ignorado por essa regra e pode ser commitado."), ("b", "É ignorado automaticamente."), ("c", "O Git dá erro.")], "Na execução que fiz, o <code>git check-ignore</code> não achou regra para <code>.env.local</code>. O padrão <code>.env*</code> cobre os dois.") + \
        quiz(4, "b", "Num PowerShell 5.1 limpo, <code>\"node_modules/\" &gt; .gitignore</code> deixou a pasta aparecer no <code>git status</code>. Por quê?", [("a", "O Git não suporta pastas."), ("b", "O <code>&gt;</code> gravou o arquivo em UTF-16 e o Git não leu a regra."), ("c", "A pasta <code>node_modules</code> não existe.")], "A solução é gravar com <code>Set-Content -Encoding ascii</code> e conferir de novo com <code>git status</code>.") + \
        flash([
            ("Diferença entre entrega contínua e implantação contínua?", "Na entrega, uma pessoa aprova o último passo. Na implantação, o código sobe sozinho."),
            ("Por que não pôr a chave no código?", "Porque o repositório pode ser público e o histórico guarda tudo, mesmo o que você apagou depois."),
            ("O que o .env.example guarda?", "Os nomes das variáveis, sem valores reais, para quem clonar saber o que precisa criar."),
            ("Primeiro passo se um segredo vazou?", "Revogar e trocar a credencial no serviço que a emitiu.")]) + \
        fontes("ibm_cicd", "ibm_devops", "ibm_secrets", "ibm_codeengine", "gh_secrets", "gitignore") + \
        ponte("O site está no ar e publica sozinho. E agora?", "Monitorar, ler logs, saber voltar atrás e fechar um checklist.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
    recap_html = recap("No capítulo 5 você publicou por três caminhos, à mão. A pergunta que ficou: <b>e se cada push publicar sozinho, sem expor a senha da plataforma?</b> Este capítulo, que é <b>complemento</b>, responde com CI/CD, variáveis de ambiente, <code>.gitignore</code> e o que fazer quando um segredo vaza.")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 6, "ci-cd-segredos", TITULO, "CI/CD, DevOps básico e segredos", "Capítulo 6 · Complemento",
            "Deploy automático, onde guardar uma senha e o que fazer quando ela vai parar no repositório.",
            chips(body, 45), body, scripts=S6)


def cap7():
    corpo = ""
    corpo += secao("monitorar", 1, "Monitorar: saber que caiu antes do visitante",
        "O site subiu. Como descubro que ele caiu, sem ficar atualizando a página?",
        camada("Intuição", "É o painel do carro. Você não abre o motor toda hora, mas quer uma luz que acenda quando algo vai mal. <b>Monitorar</b> é isso: medir o que você já sabe que importa e avisar quando sai do normal. <b>Observabilidade</b> é ir além e entender o <i>porquê</i> a partir do que o sistema emite.") +
        camada("Definição", "Segundo a IBM, monitoramento acompanha métricas conhecidas (por exemplo, se o serviço está no ar, uso de CPU) e avisa de problemas; observabilidade usa <b>métricas, logs e traces</b> para entender a causa. Para um site pequeno, o monitoramento mais útil é o \"está respondendo?\" com o código de status e o tempo de resposta.") +
        ex("um verificador de site em uma linha", [
            "Com o <code>curl</code>, pedi três vezes o mesmo site público, com 1 segundo de pausa, e imprimi o código e o tempo total.",
            "Resultado: três linhas <b>200</b>, com tempos entre <b>0,059 s</b> e <b>0,069 s</b>. Se uma linha trouxesse 5xx, ou 000 (sem conexão), o alarme seria disparado.",
            "No PowerShell, o <code>Measure-Command { Invoke-WebRequest ... }</code> deu a mesma informação: <b>200 em 147 ms</b> numa medição (uma medição só).",
        ]) +
        code('''
$ for i in 1 2 3; do curl -s -o /dev/null -w "%{http_code} %{time_total}s\\n" https://example.com; sleep 1; done
200 0.069051s
200 0.061540s
200 0.059067s
PS> $t = Measure-Command { $r = Invoke-WebRequest -Uri https://example.com -UseBasicParsing }
PS> "{0} em {1:N0} ms" -f $r.StatusCode, $t.TotalMilliseconds
200 em 147 ms
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026. Os tempos dependem da sua rede; o que importa é o formato da checagem. Serviços de monitoramento fazem exatamente isso de tempos em tempos e avisam por mensagem; não testei nenhum deles nem sei o plano gratuito de cada um.</p>' +
        erro("Monitorar só a página inicial. O site pode abrir na raiz e falhar numa rota importante (o formulário de contato, por exemplo). Inclua pelo menos uma página \"profunda\" na checagem, e confira o <b>conteúdo</b> quando for crítico, não só o código 200."),
        ponte("Sei que algo falhou. Como descubro o quê?", "Lendo o log."))

    corpo += secao("logs", 2, "Ler um log de acesso",
        "Tem erro 404 e 500 aparecendo. Onde vejo quem pediu o quê?",
        camada("Intuição", "O servidor anota cada pedido numa linha, como o caderno de visitas de uma portaria: quem veio, quando, o que pediu e o que respondeu. É a primeira coisa a abrir quando algo está estranho.") +
        camada("Definição", "O <b>log de acesso</b> do nginx e de servidores parecidos tem, em cada linha, o IP do cliente, a data, a requisição, o código de status e o tamanho da resposta. Com as ferramentas de texto da apostila de Terminal e Git (<code>grep</code>, <code>awk</code>, <code>sort</code>, <code>uniq</code>) dá para resumir. O <b>log de erros</b> é separado e guarda o que o servidor ou a aplicação reclamou.") +
        ex("resumindo um log de mentira", [
            "Escrevi um arquivo com 7 linhas no formato de log de acesso, só para treinar (IPs de exemplo, nada de servidor real).",
            "Contando os códigos de status (nono campo de cada linha): <b>3 respostas 200</b>, <b>3 respostas 404</b> e <b>1 resposta 500</b>.",
            "Os caminhos que deram 404 foram <code>/Sobre.html</code> (maiúscula trocada: o arquivo se chama <code>sobre.html</code>), <code>/wp-login.php</code> e <code>/.env</code>. Os dois últimos são o tipo de tentativa automática de <b>procurar páginas e arquivos sensíveis</b>: o 404 foi o servidor negando que existe, e é por isso que o <code>.env</code> nunca pode ficar numa pasta publicada.",
            "O único 500 foi um <code>POST /contato</code>: o formulário tem um bug no servidor. Esse é o que se investiga primeiro no log de erros.",
        ]) +
        code('''
$ awk '{print $9}' acesso.log | sort | uniq -c | sort -rn      # conta os codigos de status
      3 404
      3 200
      1 500
$ grep -c ' 404 ' acesso.log                                   # quantos 404
3
$ awk '$9==404 {print $7}' acesso.log                          # quais caminhos deram 404
/Sobre.html
/wp-login.php
/.env
$ grep ' 500 ' acesso.log
203.0.113.5 - - [06/Nov/2026:12:02:10 +0000] "POST /contato HTTP/1.1" 500 0 "-" "Mozilla/5.0"
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026, num arquivo temporário que escrevi à mão com IPs de exemplo. Em servidor de verdade o caminho do arquivo varia por sistema e por configuração; num Ubuntu com nginx costuma ser algo como <code>/var/log/nginx/access.log</code>, mas isso é conhecimento geral e <b>não testado aqui</b>.</p>' +
        erro("Gastar tempo com cada 404 de robô. Pedidos a <code>/wp-login.php</code> ou <code>/.env</code> num site que não usa isso são ruído de varredura: o importante é o 404 ser mesmo 404 (e não a entrega do arquivo!). O que merece atenção é o <b>5xx</b> e o 404 de páginas que existem."),
        ponte("Achei o bug depois do deploy. Como volto ao que funcionava, rápido?", "Com o rollback."))

    corpo += secao("rollback", 3, "Rollback: voltar ao que funcionava",
        "Subi uma versão quebrada. O site está fora. Qual a saída mais rápida?",
        camada("Intuição", "É o desfazer. Em vez de consertar às pressas com o site caído, você volta para a última versão boa, respira, e conserta com calma. A pergunta que decide é: <b>consigo voltar em um passo?</b>") +
        camada("Definição", "<b>Rollback</b> é restabelecer uma versão anterior. Com Git, o jeito seguro é <code>git revert</code>: ele cria um <b>novo commit</b> que desfaz o anterior e mantém o histórico (e funciona com push normal). O <code>git reset --hard</code> seguido de <code>push --force</code> reescreve o histórico compartilhado e é mais arriscado. Plataformas costumam permitir reimplantar uma versão anterior; <b>não testei</b> nenhuma.") +
        ex("desfazer uma versão quebrada, rodado", [
            "Num repositório temporário, o <code>index.html</code> tinha o commit bom. Troquei o conteúdo, commitei como \"v2 quebrada\" e o log ficou com 2 commits.",
            "<code>git revert --no-edit HEAD</code> criou um <b>terceiro</b> commit chamado <code>Revert \"v2 quebrada\"</code>. O conteúdo do arquivo voltou ao do primeiro commit (confirmei com <code>cat</code>).",
            "O histórico segue inteiro: 3 commits. Se o deploy é automático (capítulo 6), é esse revert que dispara a publicação da versão boa.",
        ]) +
        code('''
$ git log --oneline
c9ec437 v2 quebrada
9545595 Primeira versao do site
$ git revert --no-edit HEAD
[main 81b1098] Revert "v2 quebrada"
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git log --oneline
81b1098 Revert "v2 quebrada"
c9ec437 v2 quebrada
9545595 Primeira versao do site
$ cat index.html
<!doctype html><title>oi</title><h1>ola</h1>
''') +
        '<p class="muted" style="font-size:.85rem">Rodado em 06/11/2026. Os hashes mudam a cada pessoa.</p>' +
        naotestado("Reimplantar versão anterior pelo painel de uma plataforma e o <code>git push --force</code> não foram testados. Se o problema foi no banco de dados ou numa variável de ambiente, voltar o código pode não bastar.") +
        erro("Não ter para onde voltar. Quem publica copiando arquivos por cima no servidor (<code>scp</code>) perde a versão anterior. Guarde as versões (Git, tags, o histórico da plataforma) e, antes de uma mudança grande, anote qual é a última versão boa."),
        ponte("Sei monitorar, achar o erro e voltar atrás. Antes de dar tudo por pronto, o que mais confiro?", "Custo e um checklist de lançamento."))

    corpo += secao("checklist", 4, "Custo e checklist de lançamento",
        "O site está no ar e estável. Falta o quê para eu dizer \"lançado\"?",
        camada("Intuição", "Lançar é mais que subir: é deixar o site achável, seguro e barato de manter. Um checklist tira da cabeça o que é fácil esquecer.") +
        camada("Definição", "Sobre <b>custo</b>: o que cobra varia por modelo. Serverless cobra por execução, VPS costuma cobrar por mês, plataformas têm limites de tráfego e de tamanho. Eu <b>não cito valores</b>, porque preços e planos gratuitos mudam. Antes de contratar: leia a página oficial de preços na data de hoje, veja o que acontece quando o limite acaba (o site para? cobra a mais?), e ponha um alerta de gasto onde o serviço permitir (não testei nenhum).") +
        tabela(["Antes de divulgar", "Como conferir"], [
            ["O endereço abre por <b>HTTPS</b> e o HTTP redireciona", "<code>curl -sI http://seudominio</code> deve dar um 3xx com <code>Location: https://</code> (capítulo 3; no PowerShell 5.1 use <code>curl.exe</code>)"],
            ["O DNS aponta para o lugar certo, com <code>www</code> e sem", "<code>nslookup seudominio 1.1.1.1</code> (capítulo 2)"],
            ["O certificado está válido e com data de vencimento anotada", "<code>openssl s_client</code> ou o cadeado do navegador"],
            ["Nenhum segredo no repositório e <code>.env</code> no <code>.gitignore</code>", "<code>git check-ignore -v .env</code>; olhar o histórico com <code>git log -S</code>"],
            ["Nenhum link ou imagem quebrado (caminhos relativos, maiúsculas e minúsculas)", "abrir as páginas no endereço publicado, em aba anônima"],
            ["Página de erro 404 amigável", "pedir um caminho que não existe"],
            ["Monitoramento do \"está no ar\" ligado e com alerta", "o verificador da seção 1 ou um serviço de monitoramento"],
            ["Sei fazer rollback e já testei uma vez", "<code>git revert</code> no repositório de teste"],
            ["Conferi o custo e os limites na página oficial, hoje", "anotar a data da conferência"],
            ["Backup do que não está no Git (banco, uploads)", "se aplicável: restaurar uma vez para provar que funciona"],
        ]) +
        erro("Marcar o checklist de cabeça. Cada item tem um jeito de <b>provar</b>, e é isso que vale. \"Acho que está com HTTPS\" não é o mesmo que o <code>curl</code> mostrando um redirecionamento para https."),
        ponte("Terminou o caminho: do pedido HTTP até o site no ar e monitorado.", "Agora o fechamento."))

    corpo += '''<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
        "<b>Monitorar</b> é medir o que você já sabe que importa (está no ar? quanto demora?) e avisar. <b>Observabilidade</b> usa métricas, logs e traces para entender o porquê.",
        "Log de acesso: IP, data, requisição, <b>status</b>, tamanho. Resuma com <code>awk '{print $9}' | sort | uniq -c</code>.",
        "5xx é o que se investiga primeiro. Ruído de robô (404 em <code>/wp-login.php</code>, <code>/.env</code>) é comum.",
        "<b>Rollback</b> com Git: <code>git revert</code> (novo commit que desfaz) é mais seguro que reescrever o histórico.",
        "Custo: não decore valores. Leia a página oficial de preços na data de uso e veja o que acontece quando o limite acaba.",
        "Checklist: HTTPS, DNS, certificado, segredos, links, 404, monitoramento, rollback, custo e backup, cada um com um jeito de provar."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Depois de um deploy, o log mostra vários <b>500</b> em <code>POST /contato</code>. O que isso aponta?", [("a", "O visitante digitou o endereço errado."), ("b", "Um erro no servidor ou no código dessa rota."), ("c", "O DNS mudou.")], "A família 5xx é erro do lado do servidor. O 404 é que indicaria pedido a algo que não existe.") + \
        quiz(2, "a", "Qual a vantagem do <code>git revert</code> sobre <code>git reset --hard</code> + <code>push --force</code> para voltar uma versão?", [("a", "Ele cria um novo commit que desfaz o anterior, mantendo o histórico e funcionando com push normal."), ("b", "Ele apaga todos os commits antigos."), ("c", "Ele publica automaticamente em qualquer plataforma.")], "O revert preserva a história compartilhada. Reescrever o histórico e forçar o push pode atrapalhar quem trabalha com você.") + \
        quiz(3, "c", "Por que esta apostila não traz preços nem cotas de planos gratuitos?", [("a", "Porque todos os serviços são grátis."), ("b", "Porque preço não importa."), ("c", "Porque mudam com frequência; a conferência certa é na página oficial, na data em que você for usar.")], "Preço e limite são os dados que mais envelhecem. O hábito certo é conferir na hora de contratar.") + \
        flash([
            ("Monitoramento x observabilidade?", "Monitorar avisa quando algo conhecido sai do normal. Observabilidade (métricas, logs, traces) ajuda a entender a causa."),
            ("Como contar os códigos de status de um log de acesso?", "<code>awk '{print $9}' acesso.log | sort | uniq -c | sort -rn</code>, se o status for o nono campo."),
            ("Como voltar uma versão com Git sem reescrever o histórico?", "<code>git revert</code>, que cria um commit desfazendo o anterior."),
            ("Um item do checklist e como provar?", "HTTPS: <code>curl -sI http://seudominio</code> deve dar um 3xx com <code>Location: https://</code> (Git Bash ou <code>curl.exe</code>).")]) + \
        fontes("ibm_obs", "ibm_devops", "ibm_serverless", "ibm_vps") + \
        '''
</section>'''
    recap_html = recap("No capítulo 6 o site passou a publicar sozinho, com segredos guardados. A pergunta que ficou: <b>o que olhar depois que subiu, e como voltar atrás se quebrar?</b> Este último capítulo, <b>complemento</b> como os outros, fecha o ciclo com monitoramento, logs, rollback, custo e um checklist.")
    body = recap_html + AVISO_COMP2 + corpo
    chapter(PASTA, 7, "depois-que-subiu", TITULO, "Depois que subiu: monitorar, logs, rollback, custo e checklist", "Capítulo 7 · Complemento",
            "O que olhar depois do deploy, como ler um log, como voltar atrás e o que conferir antes de divulgar.",
            chips(body, 40), body, scripts=[])
