"""Peças comuns do gerador da apostila Terminal e Git (tg.py e tg1.py a tg3.py)."""
import os, sys, re, html as _h
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bld import *

PASTA = "terminal-git"
TITULO = "Terminal e Git"

# ---------------- fontes ----------------
# chave: (rótulo, url, ano/indicação, origem)
FONTES = {
    "ibm_1031": ("IBM Developer: Prepare for LPIC-1 103.1, a linha de comando do Linux", "https://developer.ibm.com/tutorials/l-lpic1-103-1/", "2015", "IBM"),
    "ibm_shells": ("IBM Developer: Evolution of shells in Linux", "https://developer.ibm.com/articles/l-linux-shells/", "2011 (marcado como arquivado em 2023)", "IBM"),
    "ibm_1034": ("IBM Developer: Prepare for LPIC-1 103.4, streams, pipes e redirecionamentos", "https://developer.ibm.com/tutorials/l-lpic1-103-4/", "2015", "IBM"),
    "ibm_unixtext": ("IBM Developer: Introduction to text manipulation on UNIX-based systems", "https://developer.ibm.com/articles/au-unixtext/", "2012", "IBM"),
    "ibm_1045": ("IBM Developer: Prepare for LPIC-1 104.5, permissões e donos de arquivos", "https://developer.ibm.com/tutorials/l-lpic1-104-5/", "2016", "IBM"),
    "ibm_1051": ("IBM Developer: Prepare for LPIC-1 105.1, o ambiente do shell", "https://developer.ibm.com/tutorials/l-lpic1-105-1/", "2022", "IBM"),
    "ibm_1052": ("IBM Developer: Prepare for LPIC-1 105.2, scripts simples", "https://developer.ibm.com/tutorials/l-lpic1-105-2/", "2016", "IBM"),
    "ibm_ssh": ("IBM Developer: Getting started with SSH security and configuration", "https://developer.ibm.com/articles/au-sshsecurity/", "2014", "IBM"),
    "ibm_git": ("IBM Developer: How Git works, branches, merges e colaboração", "https://developer.ibm.com/tutorials/d-learn-workings-git/", "2021", "IBM"),
    "ibm_pr": ("IBM Think: What is a pull request?", "https://www.ibm.com/think/topics/pull-request", "sem data na página", "IBM"),
    "ms_pipe": ("Microsoft Learn: about_Pipelines (PowerShell)", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines", "documentação atual", "fora da IBM"),
    "ms_env": ("Microsoft Learn: about_Environment_Variables (PowerShell)", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables", "documentação atual", "fora da IBM"),
    "ms_ssh": ("Microsoft Learn: OpenSSH no Windows (instalação e primeiro uso)", "https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse", "documentação atual", "fora da IBM"),
    "git_ignore": ("Git: documentação oficial do gitignore", "https://git-scm.com/docs/gitignore", "documentação atual", "fora da IBM"),
}

def _fonte_li(k):
    rot, url, ano, orig = FONTES[k]
    return f'<li><a href="{url}" target="_blank" rel="noopener">{rot}</a> <span class="muted">({orig}, {ano})</span></li>'

AVISO_FONTES = ("Algumas fontes da IBM são de <b>2011 a 2022</b>. Os conceitos seguem valendo, mas flags, versões e detalhes de segurança "
                "(por exemplo, o tipo de chave de SSH) podem estar desatualizados. Confira no manual da sua versão.")

def fontes(*chaves, extra=""):
    """Bloco de fontes do fim do capítulo."""
    li = "".join(_fonte_li(k) for k in chaves)
    return (f'<details class="cola"><summary>Fontes deste capítulo (complemento)</summary><div class="in-body">'
            f'<p>{AVISO_FONTES}</p><ul>{li}</ul>{extra}'
            f'<p class="muted">Nada aqui foi copiado: o texto é meu, a partir da leitura. Onde um comando está marcado como <b>não testado aqui</b>, eu não consegui rodar no meu ambiente.</p></div></details>')

def fontes_todas():
    ibm = "".join(_fonte_li(k) for k, v in FONTES.items() if v[3] == "IBM")
    fora = "".join(_fonte_li(k) for k, v in FONTES.items() if v[3] != "IBM")
    return (f'<section class="sec" id="fontes">\n    <h2><span class="sn">4</span>Fontes e avisos</h2>\n'
            f'    <p class="gancho">De onde veio cada coisa, e o que eu não consegui conferir?</p>\n'
            f'    <div class="nota cuidado"><span class="lbl">Fontes antigas</span>{AVISO_FONTES}</div>\n'
            f'    <p>Esta apostila é <b>complemento</b>: nada daqui foi dado em aula. Ela nasceu da leitura das páginas abaixo (as da IBM são a base) e de comandos que eu rodei no Windows 11, com Git Bash e PowerShell 5.1. Onde a IBM não cobre o assunto (PowerShell, Git Bash, curl, .gitignore, processos), usei documentação oficial de outra organização ou o que testei, e marquei como tal.</p>\n'
            f'    <h3>IBM</h3><ul>{ibm}</ul>\n    <h3>Fora da IBM</h3><ul>{fora}</ul>\n'
            f'    <div class="nota lembra"><span class="lbl">Não testado aqui</span>Não consegui rodar: um login real por SSH (nem <code>ssh-copy-id</code>, <code>ssh-agent</code> ou a instalação do cliente pelo <code>Add-WindowsCapability</code>), um pull request no GitHub (nem o <code>gh</code> ou a autenticação com o GitHub), a política de execução de scripts do PowerShell, gravar variável de ambiente permanente, permissões em um Linux de verdade (o Git Bash no Windows não se comporta igual), <code>git push --force</code>, <code>git cherry-pick</code> e a limpeza de histórico com <code>git filter-repo</code> ou BFG. Esses pontos aparecem no texto com o aviso. O que eu rodei de verdade em 06/11/2026, em pastas temporárias: rebase, revert, conflito de merge, <code>ssh-keygen</code> (Git Bash e PowerShell), remoto em pasta local, <code>.gitignore</code> criado pelo PowerShell e os comandos de processo e de curl.</div>\n'
            f'  </section>\n')

# ---------------- código ----------------
def code(txt, prompt_ps=False):
    """Escapa o texto, colore comentários (# ...) e prompts, e aceita [[trecho|dica]] para a dica ao passar o mouse."""
    saida = []
    for ln in txt.strip("\n").split("\n"):
        e = _h.escape(ln, quote=False)
        m = re.match(r"^(\$ |PS> )(.*)$", e)
        pre = ""
        if m:
            pre = f'<span class="k">{m.group(1)}</span>'; e = m.group(2)
        # comentário: um # precedido de espaço ou início de linha, fora de aspas simples e duplas (aproximação)
        pos = None; q = None
        for i, ch in enumerate(e):
            if q:
                if ch == q: q = None
            elif ch in "\"'": q = ch
            elif ch == "#" and (i == 0 or e[i - 1] == " ") and not e[i:i + 2] == "#{":
                pos = i; break
        if pos is not None:
            e = e[:pos] + f'<span class="c">{e[pos:]}</span>'
        e = re.sub(r"\[\[(.+?)\|(.+?)\]\]", lambda g: f'<span class="an" tabindex="0" data-t="{g.group(2)}">{g.group(1)}</span>', e)
        saida.append(pre + e)
    return "<pre><code>" + "\n".join(saida) + "</code></pre>"

def secao(id_, n, titulo, gancho, corpo, ponte_html):
    return f'''<section class="sec" id="{id_}">
  <h2><span class="sn">{n}</span>{titulo}</h2>
  <p class="gancho">{gancho}</p>
{corpo}
  {ponte_html}
</section>'''

def ex(titulo, passos):
    ls = "".join(f'<div class="l"><div>{p}</div></div>' for p in passos)
    return f'<div class="ex rv"><span class="t">Exemplo resolvido: {titulo}</span>{ls}</div>'

def erro(txt, lbl="Erro comum"):
    return f'<div class="nota erro"><span class="lbl">{lbl}</span>{txt}</div>'

def naotestado(txt):
    return f'<div class="nota cuidado"><span class="lbl">Não testado aqui</span>{txt}</div>'

def camada(nome, txt):
    return f'<p><b>{nome}.</b> {txt}</p>'

def tabela(cab, linhas):
    h = "".join(f"<th>{c}</th>" for c in cab)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<div class="tablewrap"><table><tr>{h}</tr>{r}</table></div>'

def contar(body):
    d = len(re.findall(r'class="demo"[^>]*data-demo=|class="card sorter[^>]*data-demo="sorter"', body))
    q = len(re.findall(r'class="quiz"', body))
    return d, q

def chips(body, tempo, comp=True):
    d, q = contar(body)
    partes = []
    if d: partes.append(f"{d} demo{'s' if d != 1 else ''}")
    partes.append(f"{q} testes")
    partes.append("4 flashcards")
    lst = [f"<b>~{tempo} min</b>", " · ".join(partes)]
    if comp: lst.append("complemento, não foi dado em aula")
    return lst

AVISO_COMP = ('<div class="nota lembra"><span class="lbl">Complemento, não foi dado em aula</span>Este capítulo vem de leitura (tutoriais da IBM, documentação da Microsoft e do Git) '
              'e de comandos que eu rodei. Não é conteúdo de aula. Comandos que não consegui rodar aqui trazem o aviso <mark class="hl p">não testado aqui</mark>.</div>')

NOTA_SANITIZADA = ('<p class="muted" style="font-size:.85rem">Nas saídas mostradas, troquei meu nome de usuário do Windows por <code>voce</code>. '
                   'Datas, tamanhos e contagens são os da execução real. Hashes de commit mudam a cada pessoa.</p>')

CAPS = [
 dict(n=1, file="cap-1-terminal-e-shell.html", titulo="Terminal, shell e arquivos", aula="Complemento", tempo=35,
      resumo="O que são terminal e shell, Git Bash x PowerShell no Windows 11, como navegar por pastas e criar, copiar, mover e apagar arquivos.",
      pergunta="Sei andar por pastas e mexer em arquivos. Como junto comandos pequenos para fazer algo maior, sem abrir arquivo nenhum?"),
 dict(n=2, file="cap-2-pipes-e-texto.html", titulo="Pipes, redirecionamento e ferramentas de texto", aula="Complemento", tempo=40,
      resumo="Entrada, saída e erro, os operadores >, >>, 2> e |, e grep, sort, uniq, cut, sed e awk no básico, com o equivalente no PowerShell.",
      pergunta="Sei montar uma linha de montagem de comandos. Por que um script meu 'não roda' e como o shell sabe onde achar cada programa?"),
 dict(n=3, file="cap-3-permissoes-ambiente-scripts.html", titulo="Permissões, variáveis de ambiente, PATH e scripts", aula="Complemento", tempo=40,
      resumo="Permissões rwx e o número octal, variáveis de ambiente e PATH, e o primeiro script com código de saída, com as diferenças do Windows.",
      pergunta="Já escrevo um script que roda. E quando o programa não termina, ou está em outra máquina? Quem vê e encerra processos, e como entro num servidor remoto?"),
 dict(n=4, file="cap-4-processos-ssh-curl.html", titulo="Processos, SSH e curl", aula="Complemento", tempo=35,
      resumo="Ver e encerrar processos, falar com um site pelo terminal com curl e o conceito de SSH com par de chaves, sem credenciais reais.",
      pergunta="Domino o terminal. Como guardo o histórico do que eu faço nos arquivos, e voltar atrás quando erro?"),
 dict(n=5, file="cap-5-git-commit-branch-merge.html", titulo="Git: commit, branch, merge e .gitignore", aula="Complemento", tempo=45,
      resumo="Os três lugares do Git, commit, branches, merge (fast-forward e com dois pais), conflito e .gitignore, com um grafo que reage a comandos.",
      pergunta="Meu histórico está só no meu computador. Como levo isso para o GitHub e trabalho com outras pessoas?"),
 dict(n=6, file="cap-6-github-pull-request.html", titulo="GitHub, pull request e fluxo de trabalho", aula="Complemento", tempo=40,
      resumo="Remotos, push, pull e clone, o fluxo de pull request, revisão e merge, e os erros comuns de quem está começando.",
      pergunta=""),
]
