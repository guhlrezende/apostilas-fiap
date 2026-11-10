"""Temas visuais das apostilas (ver docs/TEMAS.md).

Cada apostila ganha identidade propria por cima do caderno: o gerador escreve
data-tema="<id>" no <html>, carrega a fonte do titulo e liga assets/temas.css depois
de assets/estudo.css. O id e o nome da pasta da apostila. O hub raiz nao usa tema.

As cores 'cor_tema_*' sao o fundo do papel (para <meta name="theme-color">) e precisam
bater com --paper do tema em assets/temas.css (scripts/contraste_temas.py confere).
"""

GF = "https://fonts.googleapis.com/css2?family={fam}:wght@700&display=swap"


def _url(familia):
    return GF.format(fam=familia.replace(" ", "+"))


def _t(nome, claro, escuro, fonte, emoji):
    return {
        "nome": nome,
        "cor_tema_claro": claro,
        "cor_tema_escuro": escuro,
        "fonte_titulo": fonte,
        "fontes_url": _url(fonte),
        "emoji": emoji,
    }


TEMAS = {
    "terminal-git": _t("Terminal e Git", "#f2f6ef", "#0c110e", "Space Mono", "⌨️"),
    "github-uso": _t("GitHub na prática", "#fafbfd", "#0d1117", "Hubot Sans", "🐙"),
    "deploy-hospedagem": _t("Deploy e Hospedagem", "#f4f9fe", "#0b1622", "Sora", "🚀"),
    "cloud-aws": _t("Cloud e AWS", "#fbf8f3", "#0f1826", "Archivo", "☁️"),
    "ciberseguranca": _t("Cibersegurança", "#f7f5f5", "#0b0b0e", "Chakra Petch", "🛡️"),
    "banco-de-dados": _t("Bancos de Dados e SQL", "#f3f8f7", "#0a1517", "IBM Plex Sans Condensed", "🗄️"),
    "machine-learning": _t("Machine Learning", "#f9f7fd", "#12101e", "Space Grotesk", "🤖"),
    "redes-neurais": _t("Redes Neurais e Deep Learning", "#fbf6fb", "#140c1a", "Syne", "🧠"),
    "estatistica": _t("Estatística", "#fcfdff", "#10151f", "Fraunces", "📊"),
    "embarcados": _t("Sistemas Embarcados com ESP32", "#f1f7f1", "#0a1710", "Oxanium", "🔌"),
    "python": _t("Python e Pensamento Computacional", "#fbfcfe", "#0f1a2a", "Fredoka", "🐍"),
}


def tema_attr(pasta):
    """Atributo para o <html>: 'data-tema="id"' ou '' se a pasta nao tem tema."""
    return f'data-tema="{pasta}"' if pasta in TEMAS else ""


def fontes_link(pasta):
    """<link> da fonte do titulo do tema, ou '' (Inter, JetBrains Mono e Caveat ja vem do bloco FONTS)."""
    t = TEMAS.get(pasta)
    if not t or not t["fontes_url"]:
        return ""
    return f'<link rel="stylesheet" href="{t["fontes_url"]}">'


def fontes_link_todas():
    """Um unico <link> com a fonte de titulo de todos os temas, para o hub raiz (cartoes das apostilas)."""
    fam = "&".join("family=" + t["fonte_titulo"].replace(" ", "+") + ":wght@700" for t in TEMAS.values())
    return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">'
