"""Peças comuns do gerador da apostila GitHub: como usar do jeito certo (gh.py e gh1.py a gh3.py).
Reaproveita os blocos de tg_base.py (secao, ex, erro, camada, tabela, code, chips...) e troca pasta, título e fontes."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_base import *   # noqa: F401,F403  (bld.py vem junto)
import yaml

PASTA = "github-uso"
TITULO = "GitHub: como usar do jeito certo"
CONSULTA = "10/11/2026"
TG5 = "../terminal-git/cap-5-git-commit-branch-merge.html"
TG6 = "../terminal-git/cap-6-github-pull-request.html"


def _d(caminho, rot, nota=None):
    return (rot, "https://docs.github.com/en/" + caminho, nota or f"lida em {CONSULTA}", "GitHub Docs")


FONTES = {
    "gh_sobre": _d("get-started/start-your-journey/about-github-and-git", "GitHub Docs: About GitHub and Git"),
    "gh_conta": _d("get-started/start-your-journey/creating-an-account-on-github", "GitHub Docs: Creating an account on GitHub"),
    "gh_2fa": _d("authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication", "GitHub Docs: About two-factor authentication"),
    "gh_email": _d("account-and-profile/concepts/email-addresses", "GitHub Docs: Email addresses"),
    "gh_tokens": _d("authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation", "GitHub Docs: Token expiration and revocation"),
    "gh_ssh": _d("authentication/connecting-to-github-with-ssh/about-ssh", "GitHub Docs: About SSH"),
    "gh_remover": _d("authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository", "GitHub Docs: Removing sensitive data from a repository"),
    "gh_repos": _d("repositories/creating-and-managing-repositories/about-repositories", "GitHub Docs: About repositories"),
    "gh_readme": _d("repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes", "GitHub Docs: About READMEs"),
    "gh_comunidade": _d("communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories", "GitHub Docs: About community profiles for public repositories"),
    "gh_health": _d("communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file", "GitHub Docs: Creating a default community health file"),
    "gh_prtemplate": _d("communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository", "GitHub Docs: Creating a pull request template"),
    "gh_licenca": _d("communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository", "GitHub Docs: Adding a license to a repository"),
    "gh_flow": _d("get-started/using-github/github-flow", "GitHub Docs: GitHub flow"),
    "gh_pr": _d("pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests", "GitHub Docs: About pull requests"),
    "gh_merges": _d("pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges", "GitHub Docs: About pull request merges"),
    "gh_reviews": _d("pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-request-reviews", "GitHub Docs: About pull request reviews"),
    "gh_link": _d("issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue", "GitHub Docs: Linking a pull request to an issue"),
    "gh_contribuir": _d("get-started/exploring-projects-on-github/contributing-to-a-project", "GitHub Docs: Contributing to a project"),
    "gh_syncfork": _d("pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork", "GitHub Docs: Syncing a fork"),
    "gh_issues": _d("issues/tracking-your-work-with-issues/learning-about-issues/about-issues", "GitHub Docs: About issues"),
    "gh_projects": _d("issues/planning-and-tracking-with-projects/learning-about-projects/about-projects", "GitHub Docs: About Projects"),
    "gh_discussions": _d("discussions/collaborating-with-your-community-using-discussions/about-discussions", "GitHub Docs: About discussions"),
    "gh_rulesets": _d("repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets", "GitHub Docs: About rulesets"),
    "gh_protected": _d("repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "GitHub Docs: About protected branches"),
    "gh_owners": _d("repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners", "GitHub Docs: About code owners"),
    "gh_planos": _d("get-started/learning-about-github/githubs-plans", "GitHub Docs: GitHub's plans"),
    "gh_actions": _d("actions/writing-workflows/quickstart", "GitHub Docs: Quickstart for GitHub Actions"),
    "gh_actions_seg": _d("actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "GitHub Docs: Security hardening for GitHub Actions"),
    "gh_trigger": _d("actions/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow", "GitHub Docs: Triggering a workflow"),
    "gh_gtoken":_d("actions/security-for-github-actions/security-guides/automatic-token-authentication", "GitHub Docs: Automatic token authentication (GITHUB_TOKEN)"),
    "gh_pages": _d("pages/getting-started-with-github-pages/about-github-pages", "GitHub Docs: About GitHub Pages"),
    "gh_pages_fonte": _d("pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site", "GitHub Docs: Configuring a publishing source for GitHub Pages"),
    "gh_releases": _d("repositories/releasing-projects-on-github/about-releases", "GitHub Docs: About releases"),
    "gh_secret": _d("code-security/secret-scanning/introduction/about-secret-scanning", "GitHub Docs: About secret scanning"),
    "gh_dependabot": _d("code-security/getting-started/dependabot-quickstart-guide", "GitHub Docs: Dependabot quickstart guide"),
    "gh_seguranca": _d("code-security/getting-started/github-security-features", "GitHub Docs: GitHub security features"),
    "gh_profile": _d("account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme", "GitHub Docs: Managing your profile README"),
    "gh_blog_senha": ("GitHub Blog: Token authentication requirements for Git operations (changelog de 12/08/2021)", "https://github.blog/changelog/2021-08-12-git-password-authentication-is-shutting-down/", f"lida em {CONSULTA}", "GitHub Docs"),
    "progit": ("Pro Git: GitHub, account setup and configuration", "https://git-scm.com/book/en/v2/GitHub-Account-Setup-and-Configuration", f"lido em {CONSULTA}", "fora do GitHub"),
    "progit_dist": ("Pro Git: Distributed workflows", "https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows", f"lido em {CONSULTA}", "fora do GitHub"),
    "gitcred": ("Git: gitcredentials", "https://git-scm.com/docs/gitcredentials", f"lida em {CONSULTA}", "fora do GitHub"),
    "gitignore": ("Git: documentação oficial do gitignore", "https://git-scm.com/docs/gitignore", "página não relida em 10/11/2026; comportamento testado localmente em 06/11/2026", "fora do GitHub"),
    "ghcli": ("Manual do GitHub CLI (gh)", "https://cli.github.com/manual/", f"lido em {CONSULTA}", "fora do GitHub"),
    "osguide": ("Open Source Guides: How to contribute", "https://opensource.guide/how-to-contribute/", f"lido em {CONSULTA}", "fora do GitHub"),
    "osstart": ("Open Source Guides: Starting an open source project", "https://opensource.guide/starting-a-project/", f"lido em {CONSULTA}", "fora do GitHub"),
    "semver": ("Versionamento Semântico 2.0.0", "https://semver.org/lang/pt-BR/", f"lido em {CONSULTA}", "fora do GitHub"),
    "convcommits": ("Conventional Commits 1.0.0", "https://www.conventionalcommits.org/en/v1.0.0/", f"lido em {CONSULTA}", "fora do GitHub"),
    "changelog": ("Keep a Changelog 1.1.0", "https://keepachangelog.com/pt-BR/1.1.0/", f"lido em {CONSULTA}", "fora do GitHub"),
}


def _fonte_li(k):
    rot, url, ano, orig = FONTES[k]
    return f'<li><a href="{url}" target="_blank" rel="noopener">{rot}</a> <span class="muted">({orig}, {ano})</span></li>'


AVISO_FONTES = (f"Quase tudo vem da <b>documentação oficial do GitHub</b>, lida em <b>{CONSULTA}</b>, mais o livro Pro Git, o manual do <code>gh</code> e guias abertos. "
                "Telas, nomes de botões, planos, limites e preços do GitHub <b>mudam</b>: onde eu não abri a página, o texto diz <b>confira na página oficial</b>. "
                "<b>Nenhum valor de preço entra aqui.</b> Eu não usei nenhuma conta do GitHub para escrever esta apostila.")


def fontes(*chaves, extra=""):
    li = "".join(_fonte_li(k) for k in chaves)
    return (f'<details class="cola"><summary>Fontes deste capítulo (lidas em {CONSULTA})</summary><div class="in-body">'
            f'<p>{AVISO_FONTES}</p><ul>{li}</ul>{extra}'
            f'<p class="muted">Nada aqui foi copiado: o texto é meu, a partir da leitura. Onde algo está marcado como <b>não testado aqui</b>, eu não consegui rodar no meu ambiente.</p></div></details>')


def fontes_todas():
    gh = "".join(_fonte_li(k) for k, v in FONTES.items() if v[3] == "GitHub Docs")
    fora = "".join(_fonte_li(k) for k, v in FONTES.items() if v[3] != "GitHub Docs")
    return (f'<section class="sec" id="fontes">\n    <h2><span class="sn">4</span>Fontes e avisos</h2>\n'
            f'    <p class="gancho">De onde veio cada coisa, e o que eu não consegui conferir?</p>\n'
            f'    <div class="nota cuidado"><span class="lbl">Fontes e idade</span>{AVISO_FONTES}</div>\n'
            f'    <p>Esta apostila é <b>complemento</b>: nada daqui foi dado em aula. Ela assume o Git básico dos capítulos <a href="{TG5}">5</a> e <a href="{TG6}">6</a> da apostila de Terminal e Git e não o repete. Os comandos de Git foram rodados de verdade no Windows 11 (Git 2.56, Git Bash e PowerShell 5.1), em pastas temporárias, com o "GitHub" simulado por repositórios locais do tipo bare.</p>\n'
            f'    <h3>Documentação do GitHub</h3><ul>{gh}</ul>\n    <h3>Fora do GitHub</h3><ul>{fora}</ul>\n'
            f'    <div class="nota lembra"><span class="lbl">Não testado aqui</span>Tudo que depende do <b>site</b> do GitHub: criar conta, repositório, issue, pull request, revisão, fork, Actions rodando, proteção de branch e rulesets, CODEOWNERS, Pages, releases, secret scanning, push protection, Dependabot, <code>gh auth login</code> e qualquer <code>gh</code> que fale com a API. Também não rodei <code>git filter-repo</code> nem <code>git push --force</code>. Esses pontos trazem o aviso <mark class="hl p">não testado aqui</mark>. O que eu rodei de verdade em {CONSULTA}: <code>git</code> com remoto bare (push, fetch, pull, divergência, merge commit, squash, rebase, conflito, revert, reflog, tag), um fork simulado com dois bares, <code>ssh-keygen</code> (Git Bash e PowerShell) com chave descartável, o efeito do <code>&gt;</code> do PowerShell sobre o <code>.gitignore</code>, o vazamento de um segredo falso no histórico e o <code>--help</code> do <code>gh</code>.</div>\n'
            f'    <div class="nota cuidado"><span class="lbl">Dúvidas que eu não fechei</span>Se proteção de branch e rulesets estão disponíveis num repositório pessoal gratuito (a página de proteção lida não diz; a de rulesets cita planos Team e Enterprise), o formato exato do e-mail noreply, o tipo de chave SSH que o GitHub recomenda, o limite de repositórios fixados no perfil e se o autor pode aprovar o próprio PR. Onde esses pontos aparecem, está escrito <b>confira</b>.</div>\n'
            f'  </section>\n')


AVISO_COMP2 = ('<div class="nota lembra"><span class="lbl">Complemento, não foi dado em aula</span>Este capítulo vem da documentação oficial do GitHub, do Pro Git e de comandos que eu rodei. Não é conteúdo de aula. O que depende do site do GitHub e eu não pude testar traz o aviso <mark class="hl p">não testado aqui</mark>.</div>')

_ROD = 'Rodado de verdade em 10/11/2026 (Git 2.56 no Windows 11, Git Bash), em pasta temporária nova, fora do repositório. '
_VAR = ' Hashes, datas e caminhos mudam em cada máquina.</p>'
def _saida(txt):
    return '<p class="muted" style="font-size:.85rem">' + _ROD + txt + _VAR

SAIDA_LOCAL = _saida("Foi um repositório local, <b>sem remoto</b>.")
SAIDA_NUVEM = _saida("Um repositório bare local (<code>../nuvem.git</code>) fez o papel do GitHub; o colega foi um segundo clone dele.")
SAIDA_PROT = _saida("Um repositório bare local (<code>../prot.git</code>) com um hook <code>pre-receive</code> fez o papel do servidor.")
SAIDA_FORK = _saida("Dois repositórios bare locais (<code>original.git</code> e <code>fork.git</code>) simularam o original e o fork; o <code>git clone</code> grava o caminho completo, que aqui aparece abreviado como <code>...</code>.")
SAIDA_TAGS = _saida("Um repositório bare local recebeu a tag (o remoto foi só um caminho de pasta).")
SAIDA_AUTH = _saida("A chave SSH foi descartável e <b>não foi cadastrada</b> em lugar nenhum; o token da URL era falso e o repositório não tinha remoto real.")
SAIDA_ERROS = _saida("Foram repositórios locais: um sem remoto (<code>reflog</code> e <code>branch -D</code>) e um com remoto bare (commit direto na main).")


def yaml_code(txt):
    """Valida o YAML com um parser antes de escrever a página (erro de gerador, não de leitor)."""
    yaml.safe_load(txt)
    return code(txt)


def json_code(txt):
    json.loads(txt)
    return code(txt)


def lab(key, titulo, intro, itens):
    """Laboratório: lista de passos executáveis num repositório do próprio aluno, com marcação que o navegador lembra."""
    nd = "".join(f'<div class="nd" data-n="{i}"><b>{t}</b><br><label><input type="checkbox"> feito</label></div>' for i, t in enumerate(itens, 1))
    return (f'<h3>Laboratório: {titulo}</h3><p>{intro}</p>'
            f'<div class="thread rv" data-demo="checks" data-key="{key}">{nd}<p class="muted" style="margin:6px 0 0"><b class="chk-n">0 de {len(itens)}</b> passos feitos.</p></div>')


def aviso_lab():
    return ('<div class="nota cuidado"><span class="lbl">Só no seu repositório de treino</span>Faça tudo num repositório <b>seu</b> (por exemplo <code>treino-github</code>), na <b>sua</b> conta. '
            'Não use credencial real como exemplo, não suba dado pessoal e não faça push para repositório de outras pessoas. Eu <b>não</b> executei estes passos no site: são o roteiro para você, e cada um diz como confirmar que funcionou.</div>')


CAPS = [
 dict(n=1, file="cap-1-git-github-conta.html", titulo="Git x GitHub, conta, 2FA e o seu e-mail", aula="Complemento", tempo=35,
      resumo="O que o GitHub acrescenta ao Git, como criar e proteger a conta (2FA, passkey, códigos de recuperação) e o que o e-mail dos seus commits mostra para o mundo.",
      pergunta="Tenho a conta protegida e a identidade certa nos commits. Onde meu projeto mora, e o que faz um repositório ser bem montado?"),
 dict(n=2, file="cap-2-repositorio.html", titulo="O repositório: visibilidade, README, licença e arquivos de saúde", aula="Complemento", tempo=45,
      resumo="Público x privado, README, LICENSE (sem aconselhamento jurídico), .gitignore, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY e templates, montados num repositório local.",
      pergunta="O repositório está montado no meu computador. Como o GitHub e o meu computador passam a conversar?"),
 dict(n=3, file="cap-3-remoto-e-autenticacao.html", titulo="Remoto, clone, fork, fetch, pull, push e autenticação", aula="Complemento", tempo=50,
      resumo="origin, main, clone x fork, upstream, a diferença entre fetch, pull e push (com divergência rodada de verdade) e as formas de se autenticar: token, SSH e gh, e o que nunca colar.",
      pergunta="Já consigo enviar código. Como planejo o trabalho e o registro de quem faz o quê?"),
 dict(n=4, file="cap-4-issues-e-projects.html", titulo="Issues, labels, milestones, referências e Projects", aula="Complemento", tempo=35,
      resumo="Issue como unidade de trabalho, labels e milestones, as referências #123 e Closes #123 (e a regra do branch padrão) e Projects.",
      pergunta="Tenho issues organizadas. Como transformo uma delas em código revisado e entregue?"),
 dict(n=5, file="cap-5-branch-pr-e-merge.html", titulo="Branches, GitHub Flow, pull request e tipos de merge", aula="Complemento", tempo=60,
      resumo="O fluxo completo de um PR (draft, descrição, revisão, checks, conflito), merge commit x squash x rebase com o grafo resultante e como desfazer um merge com revert -m 1.",
      pergunta="Sei levar uma mudança minha até a main. E num projeto que não é meu, onde eu nem tenho permissão de escrita?"),
 dict(n=6, file="cap-6-fork-e-contribuicao.html", titulo="Fork, upstream e contribuição em projeto de terceiros", aula="Complemento", tempo=45,
      resumo="Quando usar fork, como manter o fork em dia, a etiqueta de quem contribui e um diagrama interativo de origin, upstream e PR.",
      pergunta="Contribuo sem esbarrar nos outros. Em equipe, o que impede alguém de quebrar a main?"),
 dict(n=7, file="cap-7-proteger-a-main.html", titulo="Proteger a main: proteção de branch, rulesets e CODEOWNERS", aula="Complemento", tempo=40,
      resumo="Por que não commitar direto na main em equipe, o que cada regra de proteção exige, rulesets, CODEOWNERS e uma demo que diz se um PR pode entrar.",
      pergunta="A main está protegida. E as tarefas repetitivas (testar, publicar, versionar), quem faz?"),
 dict(n=8, file="cap-8-actions-pages-releases.html", titulo="Actions, Pages, releases e versionamento", aula="Complemento", tempo=50,
      resumo="Workflow em YAML, gatilhos, secrets e permissões mínimas, o que o GITHUB_TOKEN não faz, Pages, tags e releases com versionamento semântico.",
      pergunta="Automatizei e publiquei. E se um segredo vazar, ou eu errar feio, como protejo e como me recupero?"),
 dict(n=9, file="cap-9-seguranca-gh-e-portfolio.html", titulo="Segurança, gh, recuperação de erros e portfólio", aula="Complemento", tempo=55,
      resumo="Secret scanning, push protection e Dependabot, a ordem certa quando um segredo vaza (com árvore de decisão), o gh no terminal, erros comuns com a saída real e como montar um perfil sem prometer emprego.",
      pergunta=""),
]


def fechamento(n, cola, quizzes, cards, fontes_html, prox=None):
    """Seção final do capítulo: cola da prova, testes, flashcards, fontes e (se houver) a ponte para o próximo."""
    p = ""
    if prox:
        p = ponte(prox[1], prox[2], f"Para onde vamos agora · Capítulo {prox[0]}")
    return (f'<section class="sec" id="fechamento">\n  <h2><span class="sn">{n}</span>Fechamento do capítulo</h2>\n  '
            + resumo(cola) + '\n  <h3>Teste rápido</h3>\n  ' + "".join(quizzes) + "\n  " + flash(cards) + "\n  " + fontes_html + "\n  " + p + "\n</section>")


def publicar(n, slug, titulo, sub, recap_txt, corpo, tempo, scripts=()):
    body = recap(recap_txt) + AVISO_COMP2 + corpo
    chapter(PASTA, n, slug, TITULO, titulo, f"Capítulo {n} · Complemento", sub, chips(body, tempo), body, scripts=list(scripts))
