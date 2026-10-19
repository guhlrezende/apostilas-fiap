"""Confere o repositório antes de subir: links, demos registradas, sintaxe dos scripts e dados pessoais.

Uso:  python scripts/checar.py
Sai com código 1 se encontrar problema.

Os termos proibidos são montados em pedaços de propósito: assim este arquivo (que é público)
não contém o que ele mesmo procura.
"""
import glob
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
erros = []

PROIBIDOS = [
    (r"\b57\d{4}\b", "possível RM"),
    (r"Gus" + r"tavo\s+Hen" + r"rique", "nome completo"),
    (r"Lopes\s+Re" + r"zende", "nome completo"),
    (r"Mári" + r"o\s+And" + r"ré", "nome de professor"),
    (r"André\s+de\s+De" + r"us", "nome de professor"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "e-mail"),
    (r"\u2014", "travessão"),
    (r"Sem\s+Par" + r"ar", "empresa parceira"),
    (r"Fleet" + r"Force", "grupo do Challenge"),
    (r"Flex" + r"media", "empresa de exemplo da aula"),
    (r"Net" + r"Guard", "trabalho da faculdade"),
    (r"Vac" + r"cine\s+Sense", "trabalho em aberto"),
    (r"jogo\s+da\s+vel" + r"ha", "trabalho em aberto"),
]

DOMINIOS_FICTICIOS = ("@empresa.com", "@exemplo.com", "@email.com", "@example.com")
EXT_TEXTO = (".html", ".js", ".css", ".md", ".py", ".json", ".txt")
IGNORAR = (os.sep + ".git" + os.sep, "ml-data.js")


def ler(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


todos = [p for p in glob.glob(os.path.join(RAIZ, "**", "*"), recursive=True)
         if os.path.isfile(p) and p.endswith(EXT_TEXTO) and not any(i in p for i in IGNORAR)]
htmls = sorted(p for p in todos if p.endswith(".html") and os.sep + "template" + os.sep not in p)
jss = sorted(p for p in glob.glob(os.path.join(RAIZ, "**", "*.js"), recursive=True) if "ml-data.js" not in p)

# 1) dados pessoais e estilo em TODOS os arquivos de texto
for p in todos:
    s = ler(p)
    rel = os.path.relpath(p, RAIZ)
    for pad, nome in PROIBIDOS:
        achou = [m for m in re.finditer(pad, s)]
        if nome == "e-mail":  # e-mails fictícios de exemplo são permitidos
            achou = [m for m in achou if not m.group(0).lower().endswith(DOMINIOS_FICTICIOS)]
        if achou:
            erros.append(f"{rel}: contém {nome}")

# 2) demos registradas (e sem registro duplicado)
reg = {}
for j in jss:
    for nome in re.findall(r"demos\.(\w+)\s*=\s*function", ler(j)):
        reg.setdefault(nome, []).append(os.path.relpath(j, RAIZ))
for nome, onde in reg.items():
    if len(onde) > 1:
        erros.append(f"demo '{nome}' registrada em mais de um arquivo: {', '.join(onde)}")

# 3) cada página: links locais, demos, título, contagem de quizzes e demos
for h in htmls:
    rel = os.path.relpath(h, RAIZ)
    s = ler(h)
    for m in re.finditer(r'(?:href|src)="([^"#:][^"]*)"', s):
        alvo = m.group(1).split("?")[0]
        if alvo.startswith(("http", "mailto", "data:")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(h), alvo))):
            erros.append(f"{rel}: arquivo não encontrado: {alvo}")
    usadas = re.findall(r'data-demo="(\w+)"', s)
    scripts = [os.path.normpath(os.path.join(os.path.dirname(h), a)) for a in re.findall(r'<script src="([^"]+)"', s)]
    texto_scripts = "".join(ler(x) for x in scripts if os.path.exists(x))
    for d in usadas:
        if d not in reg:
            erros.append(f"{rel}: demo '{d}' sem função registrada")
        elif not re.search(r"demos\." + d + r"\s*=", texto_scripts):
            erros.append(f"{rel}: demo '{d}' existe, mas a página não carrega o script dela")
    if "<title>" not in s:
        erros.append(f"{rel}: sem <title>")
    # o chip "N demos · M testes" precisa bater com o conteúdo
    m = re.search(r"(\d+) demos? · (\d+) testes?", s)
    if m:
        n_demos = len(re.findall(r'class="demo"[^>]*data-demo=|class="card sorter[^>]*data-demo="sorter"', s))
        n_quiz = len(re.findall(r'class="quiz"', s))
        if int(m.group(1)) != n_demos or int(m.group(2)) != n_quiz:
            erros.append(f"{rel}: o chip diz {m.group(1)} demos e {m.group(2)} testes, mas a página tem {n_demos} demos e {n_quiz} testes")

# 4) manifestos apontam para arquivos que existem
for man in glob.glob(os.path.join(RAIZ, "*", "capitulos.js")):
    base = os.path.dirname(man)
    for f in re.findall(r'file:\s*"([^"]+)"', ler(man)):
        if not os.path.exists(os.path.join(base, f)):
            erros.append(f"{os.path.relpath(man, RAIZ)}: capítulo listado mas não existe: {f}")

# 5) sintaxe dos scripts (precisa do node)
try:
    for j in jss:
        r = subprocess.run(["node", "--check", j], capture_output=True, text=True)
        if r.returncode:
            erros.append(f"{os.path.relpath(j, RAIZ)}: erro de sintaxe\n{r.stderr.strip()}")
except FileNotFoundError:
    print("(node não encontrado: pulei a checagem de sintaxe dos .js)")

if erros:
    print(f"{len(erros)} problema(s):")
    for e in erros:
        print(" -", e)
    sys.exit(1)
print(f"Tudo certo: {len(htmls)} páginas, {len(jss)} scripts, {len(reg)} demos registradas.")
