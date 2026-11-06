"""Peças comuns do gerador da apostila Deploy e Hospedagem (dp.py e dp1.py a dp3.py).
Reaproveita os blocos de tg_base.py (secao, ex, erro, camada, tabela, code, chips...) e troca pasta, título e fontes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_base import *   # noqa: F401,F403  (bld.py vem junto)

PASTA = "deploy-hospedagem"
TITULO = "Deploy e Hospedagem"
CONSULTA = "06/11/2026"

# chave: (rótulo, url, ano/indicação, origem)
FONTES = {
    "ibm_dns": ("IBM Think: What Is DNS (Domain Name System)?", "https://www.ibm.com/think/topics/dns", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_tls": ("IBM Think: What is Transport Layer Security (TLS)?", "https://www.ibm.com/think/topics/transport-layer-security", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_net": ("IBM Think: What Is Computer Networking?", "https://www.ibm.com/think/topics/networking", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_lb": ("IBM Think: What Is Load Balancing?", "https://www.ibm.com/think/topics/load-balancing", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_cicd": ("IBM Think: What Is CI/CD?", "https://www.ibm.com/think/topics/ci-cd", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_devops": ("IBM Think: What Is DevOps?", "https://www.ibm.com/think/topics/devops", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_iaas": ("IBM Think: IaaS, PaaS, SaaS: What's the difference?", "https://www.ibm.com/think/topics/iaas-paas-saas", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_paas": ("IBM Think: What Is Platform as a Service (PaaS)?", "https://www.ibm.com/think/topics/paas", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_containers": ("IBM Think: What are containers?", "https://www.ibm.com/think/topics/containers", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_serverless": ("IBM Think: What Is Serverless Computing?", "https://www.ibm.com/think/topics/serverless", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_vps": ("IBM Think: O que é um Virtual Private Server (VPS)?", "https://www.ibm.com/think/topics/vps", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_obs": ("IBM Think: Observability versus monitoring", "https://www.ibm.com/think/topics/observability-vs-monitoring", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_secrets": ("IBM Think: What is secrets management?", "https://www.ibm.com/think/topics/secrets-management", f"sem data lida; consultada em {CONSULTA}", "IBM"),
    "ibm_codeengine": ("IBM Developer: Deploying apps to IBM Code Engine from GitHub or local sources", "https://developer.ibm.com/tutorials/awb-deploy-apps-ibm-code-engine-github-local-sources/", "publicado em 26/11/2024", "IBM"),
    "ibm_cos": ("IBM Cloud docs: Hosting static websites in IBM Cloud Object Storage", "https://ondeck.console.cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-static-website-options", f"sem data; endereço espelho 'ondeck'; consultada em {CONSULTA}", "IBM"),
    "mdn_http": ("MDN: Uma visão geral do HTTP", "https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Overview", "documentação atual", "fora da IBM"),
    "gh_pages": ("GitHub Docs: Creating a GitHub Pages site", "https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site", f"consultada em {CONSULTA}", "fora da IBM"),
    "cf_pages": ("Cloudflare Docs: Direct Upload (Pages)", "https://developers.cloudflare.com/pages/get-started/direct-upload/", f"consultada em {CONSULTA}", "fora da IBM"),
    "netlify": ("Netlify Docs: Choose your path", "https://docs.netlify.com/get-started/", f"consultada em {CONSULTA}", "fora da IBM"),
    "vercel": ("Vercel Docs: Deploying to Vercel", "https://vercel.com/docs/deployments", "lida na pesquisa de apoio de 06/11/2026", "fora da IBM"),
    "nginx": ("nginx: Beginner's Guide", "https://nginx.org/en/docs/beginners_guide.html", f"consultada em {CONSULTA}", "fora da IBM"),
    "openssh": ("OpenSSH", "https://www.openssh.org/", "site oficial", "fora da IBM"),
    "certbot": ("Certbot (EFF)", "https://certbot.eff.org/instructions", f"consultada em {CONSULTA} (a página lida não traz os comandos)", "fora da IBM"),
    "gh_secrets": ("GitHub Docs: Using secrets in GitHub Actions", "https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions", f"consultada em {CONSULTA}", "fora da IBM"),
    "gitignore": ("Git: documentação oficial do gitignore", "https://git-scm.com/docs/gitignore", f"lida em {CONSULTA} (padrões e negação com !; não trata de codificação)", "fora da IBM"),
    "badssl": ("badssl.com (sites públicos feitos para testar erros de certificado)", "https://badssl.com/", f"usado em testes de {CONSULTA}", "fora da IBM"),
}

def _fonte_li(k):
    rot, url, ano, orig = FONTES[k]
    return f'<li><a href="{url}" target="_blank" rel="noopener">{rot}</a> <span class="muted">({orig}, {ano})</span></li>'

AVISO_FONTES = ("As páginas da IBM usadas aqui são de <b>ibm.com/think</b> (não li uma data nelas) e um tutorial de <b>novembro de 2024</b> (Code Engine). "
                "Os conceitos são estáveis, mas nomes de produtos, telas e limites mudam: confira na documentação atual antes de depender de um detalhe. "
                "<b>Preços e planos gratuitos não aparecem nesta apostila de propósito</b>, porque mudam; olhe a página oficial do serviço.")

def fontes(*chaves, extra=""):
    li = "".join(_fonte_li(k) for k in chaves)
    return (f'<details class="cola"><summary>Fontes deste capítulo (complemento)</summary><div class="in-body">'
            f'<p>{AVISO_FONTES}</p><ul>{li}</ul>{extra}'
            f'<p class="muted">Nada aqui foi copiado: o texto é meu, a partir da leitura. Onde um comando está marcado como <b>não testado aqui</b>, eu não consegui rodar no meu ambiente.</p></div></details>')

def fontes_todas():
    ibm = "".join(_fonte_li(k) for k, v in FONTES.items() if v[3] == "IBM")
    fora = "".join(_fonte_li(k) for k, v in FONTES.items() if v[3] != "IBM")
    return (f'<section class="sec" id="fontes">\n    <h2><span class="sn">4</span>Fontes e avisos</h2>\n'
            f'    <p class="gancho">De onde veio cada coisa, e o que eu não consegui conferir?</p>\n'
            f'    <div class="nota cuidado"><span class="lbl">Fontes e idade</span>{AVISO_FONTES}</div>\n'
            f'    <p>Esta apostila é <b>complemento</b>: nada daqui foi dado em aula. Ela nasceu da leitura das páginas abaixo (as da IBM são a base) e de comandos que eu rodei no Windows 11, com Git Bash e PowerShell 5.1, contra sites públicos de teste, servidores locais e pastas temporárias. A IBM <b>não cobre</b> HTTP em detalhe, GitHub Pages, Cloudflare Pages, Netlify, Vercel, nginx nem SSH para deploy: nesses pontos usei a documentação de cada projeto e marquei como <b>fora da IBM</b>.</p>\n'
            f'    <h3>IBM</h3><ul>{ibm}</ul>\n    <h3>Fora da IBM</h3><ul>{fora}</ul>\n'
            f'    <div class="nota lembra"><span class="lbl">Não testado aqui</span>Não consegui rodar: nenhum deploy real (GitHub Pages, Cloudflare Pages, Netlify, Vercel, VPS), <code>certbot</code>, <code>nginx</code> (não está instalado aqui), <code>rsync</code> (também não), <code>scp</code> ou <code>ssh</code> contra um servidor, nem uma esteira de CI de verdade no GitHub Actions (só conferi que o YAML é válido). Esses pontos trazem o aviso <mark class="hl p">não testado aqui</mark> no texto. O que eu rodei de verdade em 06/11/2026: <code>curl</code>, <code>nslookup</code>, <code>Resolve-DnsName</code>, <code>Test-NetConnection</code> e <code>openssl s_client</code> contra sites públicos de teste, <code>python -m http.server</code> em localhost, <code>git</code> (inclusive push para um remoto em pasta local, <code>revert</code>, <code>check-ignore</code> e a perda do segredo no histórico) e o efeito do <code>&gt;</code> do PowerShell sobre o <code>.gitignore</code>.</div>\n'
            f'    <div class="nota cuidado"><span class="lbl">Não verificado</span>Preços, planos gratuitos, cotas e nomes exatos de botões e telas de painel. Onde aparece "confira na página oficial", é porque eu não afirmo.</div>\n'
            f'  </section>\n')

AVISO_COMP2 = ('<div class="nota lembra"><span class="lbl">Complemento, não foi dado em aula</span>Este capítulo vem de leitura (páginas da IBM e documentação oficial de cada ferramenta) '
               'e de comandos que eu rodei. Não é conteúdo de aula. Comandos que não consegui rodar aqui trazem o aviso <mark class="hl p">não testado aqui</mark>.</div>')

CAPS = [
 dict(n=1, file="cap-1-como-a-web-funciona.html", titulo="Como a web funciona: cliente, servidor, HTTP, IP e portas", aula="Complemento", tempo=40,
      resumo="Quem pede e quem responde, a conversa em HTTP (métodos, cabeçalhos e códigos de status), e o papel do IP e das portas, com um simulador de requisição.",
      pergunta="Entendo o pedido e a resposta. Mas o navegador só sabe o nome do site: como ele descobre o endereço do servidor?"),
 dict(n=2, file="cap-2-dns-e-dominio.html", titulo="DNS e domínio: uma consulta passo a passo", aula="Complemento", tempo=40,
      resumo="Domínio, subdomínio e registros (A, AAAA, CNAME, MX, TXT, NS), a cadeia resolvedor, raiz, TLD e autoritativo, cache e TTL, com um simulador.",
      pergunta="O nome virou um IP. Como eu sei que estou falando com o servidor certo, e que ninguém lê a conversa no meio do caminho?"),
 dict(n=3, file="cap-3-https-tls-certificado.html", titulo="HTTPS, TLS e certificado", aula="Complemento", tempo=40,
      resumo="O que o TLS garante, o que o navegador confere num certificado, a cadeia de autoridades e o que o cadeado não promete, com erros reais de certificado.",
      pergunta="A conexão é segura. Mas onde o meu site vai morar? Qual a diferença entre um servidor estático, um PaaS, um VPS e uma função serverless?"),
 dict(n=4, file="cap-4-tipos-de-hospedagem.html", titulo="Tipos de hospedagem e quando usar cada um", aula="Complemento", tempo=40,
      resumo="Estático, PaaS, container, VPS e serverless, mais IaaS, PaaS e SaaS, com uma árvore de decisão que recomenda e justifica.",
      pergunta="Já sei onde posso hospedar. Como eu faço o site chegar lá, de fato?"),
 dict(n=5, file="cap-5-publicar-site-estatico.html", titulo="Publicar um site estático por três caminhos", aula="Complemento", tempo=50,
      resumo="GitHub Pages, uma plataforma de deploy (Cloudflare Pages, Netlify ou Vercel) e um VPS com nginx, SSH e scp/rsync, com os comandos e o aviso do que não foi testado.",
      pergunta="Consigo publicar à mão. E se eu quiser que cada push publique sozinho, sem vazar a senha da plataforma?"),
 dict(n=6, file="cap-6-ci-cd-segredos.html", titulo="CI/CD, DevOps básico e segredos", aula="Complemento", tempo=45,
      resumo="Integração, entrega e implantação contínuas, variáveis de ambiente, .env, .gitignore e o que fazer quando um segredo vaza, com uma esteira simulada.",
      pergunta="O site está no ar e publica sozinho. O que eu olho depois, e como volto atrás se algo quebrar?"),
 dict(n=7, file="cap-7-depois-que-subiu.html", titulo="Depois que subiu: monitorar, logs, rollback, custo e checklist", aula="Complemento", tempo=40,
      resumo="Monitoramento e observabilidade, ler um log de acesso, rollback com git revert, cuidado com custo e um checklist de lançamento.",
      pergunta=""),
]
