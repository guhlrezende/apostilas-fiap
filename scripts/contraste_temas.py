"""Confere o contraste WCAG dos temas visuais (assets/temas.css) em claro e escuro.

Uso:  python scripts/contraste_temas.py            (resumo: menor razao por tema)
      python scripts/contraste_temas.py --tudo     (todos os pares de todos os temas)
Sai com codigo 1 se algum par ficar abaixo de 4.5:1 ou se houver inconsistencia nos blocos.

Como resolve os tokens (igual ao navegador): base do estudo.css (claro ou escuro) +
bloco claro do tema + (no escuro) bloco escuro do tema. Por isso todo token definido no
bloco claro tem de ser repetido nos blocos escuros, senao o valor claro vaza para o escuro.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MIN = 4.5
SOBREPOSICAO = 0.18   # decoracao tem 14%; testa com 18% de folga (nao e o piso 4.5, e a cor de fundo sob o texto)


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


def limpar(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def regras(css, dentro_dark=False):
    """Lista (dark?, seletor, corpo) percorrendo @media; so entra em @media dark, ignora as outras."""
    saida, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        sel = css[i:j].strip()
        d, k = 1, j + 1
        while k < n and d:
            if css[k] == "{":
                d += 1
            elif css[k] == "}":
                d -= 1
            k += 1
        corpo = css[j + 1:k - 1]
        if sel.startswith("@media"):
            if "prefers-color-scheme:dark" in sel.replace(" ", ""):
                saida += regras(corpo, True)
        elif sel.startswith("@"):
            pass  # @keyframes etc.
        else:
            saida.append((dentro_dark, sel, corpo))
        i = k
    return saida


def tokens(corpo):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"--([\w-]+)\s*:\s*([^;]+)", corpo)}


def decl(corpo, prop):
    m = re.search(r"(?:^|;)\s*" + re.escape(prop) + r"\s*:\s*([^;]+)", corpo)
    return m.group(1).strip() if m else None


# ---------- cor e contraste ----------
def cor(v):
    v = v.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", v)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", v)
    if m:
        h = m.group(1)
        return (int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16), 1.0)
    m = re.fullmatch(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)", v)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4) or 1))
    raise ValueError("cor nao reconhecida: " + v)


def misturar(topo, base, a):
    """topo com opacidade a sobre base (ambos RGB)."""
    return tuple(round(topo[i] * a + base[i] * (1 - a)) for i in range(3)) + (1.0,)


def lum(c):
    def f(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def razao(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


# ---------- leitura dos css ----------
def ler_base():
    r = regras(limpar(ler("assets/estudo.css")))
    claro, escuro = {}, {}
    for dark, sel, corpo in r:
        if sel == ":root" and not dark:
            claro.update(tokens(corpo))
        elif dark and sel == ':root:not([data-theme="light"])':
            escuro.update(tokens(corpo))
    return claro, {**claro, **escuro}


def ler_temas():
    r = regras(limpar(ler("assets/temas.css")))
    temas, avisos = {}, []
    for dark, sel, corpo in r:
        m = re.fullmatch(r':root\[data-tema="([\w-]+)"\](:not\(\[data-theme="light"\]\)|\[data-theme="dark"\])?', sel)
        if m:
            t = temas.setdefault(m.group(1), {"claro": {}, "esc_media": None, "esc_attr": None, "chip": {}, "cardL": {}, "cardD": {}})
            if m.group(2) is None:
                t["claro"] = tokens(corpo)
            elif m.group(2).startswith(":not"):
                t["esc_media"] = tokens(corpo)
            else:
                t["esc_attr"] = tokens(corpo)
            continue
        m = re.fullmatch(r'\[data-tema="([\w-]+)"\]', sel)
        if m:
            t = temas.setdefault(m.group(1), {"claro": {}, "esc_media": None, "esc_attr": None, "chip": {}, "cardL": {}, "cardD": {}})
            t["meta"] = corpo
            continue
        m = re.fullmatch(r':root\[data-tema="([\w-]+)"\] \.chip', sel)
        if m:
            t = temas.setdefault(m.group(1), {"claro": {}, "esc_media": None, "esc_attr": None, "chip": {}, "cardL": {}, "cardD": {}})
            t["chip"] = {"bg": decl(corpo, "background"), "fg": decl(corpo, "color")}
            continue
        m = re.fullmatch(r'(?::root(?::not\(\[data-theme="light"\]\)|\[data-theme="dark"\]) )?\.hubgrid \.cap-card\[data-tema="([\w-]+)"\]', sel)
        if m:
            t = temas.setdefault(m.group(1), {"claro": {}, "esc_media": None, "esc_attr": None, "chip": {}, "cardL": {}, "cardD": {}})
            t["cardD" if (dark or sel.startswith(":root")) else "cardL"].update(tokens(corpo))
    for tid, t in temas.items():
        if t["esc_media"] is None or t["esc_attr"] is None:
            avisos.append(f"{tid}: falta bloco escuro (@media e/ou [data-theme=dark])")
            continue
        if t["esc_media"] != t["esc_attr"]:
            avisos.append(f"{tid}: os dois blocos escuros sao diferentes")
        faltam = sorted(set(t["claro"]) - set(t["esc_media"]))
        if faltam:
            avisos.append(f"{tid}: tokens do claro sem par no escuro (vazam): {', '.join(faltam)}")
    avisos += conferir_temas_py(temas)
    return temas, avisos


def conferir_temas_py(temas):
    """Confere scripts/construtor/temas.py contra o css: ids, cor do papel e fonte do titulo."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("temas_py", os.path.join(RAIZ, "scripts", "construtor", "temas.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    av = []
    for tid in sorted(set(temas) ^ set(mod.TEMAS)):
        av.append(f"{tid}: existe so em um dos dois (temas.css x temas.py)")
    for tid, py in mod.TEMAS.items():
        t = temas.get(tid)
        if not t or t["esc_media"] is None:
            continue
        if py["cor_tema_claro"].lower() != t["claro"].get("paper", "").lower():
            av.append(f"{tid}: cor_tema_claro difere de --paper (claro)")
        if py["cor_tema_escuro"].lower() != t["esc_media"].get("paper", "").lower():
            av.append(f"{tid}: cor_tema_escuro difere de --paper (escuro)")
        head = tokens(t.get("meta", "")).get("f-head", "")
        if py["fonte_titulo"] not in head:
            av.append(f"{tid}: fonte_titulo '{py['fonte_titulo']}' nao aparece em --f-head")
        if py["fontes_url"] and py["fonte_titulo"].replace(" ", "+") not in py["fontes_url"]:
            av.append(f"{tid}: fontes_url nao carrega a fonte do titulo")
        if mod.tema_attr(tid) != f'data-tema="{tid}"':
            av.append(f"{tid}: tema_attr incorreto")
    return av


def var_nome(v):
    m = re.fullmatch(r"var\(--([\w-]+)\)", v or "")
    return m.group(1) if m else None


def resolver(base, *camadas):
    r = dict(base)
    for c in camadas:
        r.update(c)
    return r


def pares(tk, chip):
    """Lista (nome, fg, bg, minimo) para um conjunto de tokens ja resolvido."""
    C = lambda n: cor(tk[n])
    P = []
    for fg, bgs in [("ink", ["paper", "paper-2", "card", "desk", "pen-soft", "green-soft", "amber-soft", "red-soft"]),
                    ("muted", ["paper", "paper-2", "card", "desk", "pen-soft"]),
                    ("pen", ["paper", "paper-2", "card", "desk", "pen-soft"]),
                    ("red", ["red-soft", "paper", "card"]),
                    ("green", ["green-soft", "paper", "card", "desk"]),
                    ("amber", ["amber-soft"])]:
        for bg in bgs:
            P.append((f"{fg} sobre {bg}", C(fg), C(bg), MIN))
    for acento in ("pen", "green", "c1"):
        P.append((f"papel sobre {acento} (texto em botao/numero)", C("paper"), C(acento), MIN))
    # chip
    cbg = var_nome(chip.get("bg")) or "card"
    cfg = var_nome(chip.get("fg")) or "muted"
    P.append((f"chip: {cfg} sobre {cbg}", C(cfg), C(cbg), MIN))
    P.append((f"chip (b): ink sobre {cbg}", C("ink"), C(cbg), MIN))
    # destaques (mark.hl): ink sobre papel com o marca-texto
    for h in ("hl-y", "hl-p", "hl-g", "hl-b"):
        c = C(h)
        P.append((f"ink sobre {h} no papel", C("ink"), misturar(c, C("paper"), c[3]), MIN))
    return P


def pares_decoracao(tk, decos):
    P = []
    for d in decos:
        dec = cor(tk[d])
        for fundo in ("paper", "card"):
            bg = misturar(dec, cor(tk[fundo]), SOBREPOSICAO)
            for fg in ("pen", "ink", "muted"):
                tag = {"pen": "kicker", "ink": "titulo", "muted": "subtitulo"}[fg]
                P.append((f"{tag} ({fg}) sobre {fundo}+{d} {int(SOBREPOSICAO*100)}%", cor(tk[fg]), bg, MIN))
    return P


def main():
    tudo = "--tudo" in sys.argv
    base_claro, base_escuro = ler_base()
    temas, avisos = ler_temas()
    falhas = [("lint", a) for a in avisos]
    resumo = []
    for tid in sorted(temas):
        t = temas[tid]
        if t["esc_media"] is None:
            continue
        linha = {"tema": tid}
        for modo in ("claro", "escuro"):
            if modo == "claro":
                tk = resolver(base_claro, t["claro"])
                card = t["cardL"]
                base_hub = base_claro
            else:
                tk = resolver(base_escuro, t["claro"], t["esc_media"])
                card = t["cardD"]
                base_hub = base_escuro
            ps = pares(tk, t["chip"])
            decos = ["deco"] + (["c1"] if tid in ("gestao-agil", "python") else [])
            ps += pares_decoracao(tk, decos)
            # cartao no hub: texto padrao do caderno sobre o cartao com a decoracao do tema
            if "deco" in card:
                bg = misturar(cor(card["deco"]), cor(base_hub["card"]), 0.11)  # no cartao a decoracao tem 9%
                for fg in ("ink", "muted"):
                    ps.append((f"hub: {fg} sobre cartao+deco", cor(base_hub[fg]), bg, MIN))
            res = [(razao(a, b), n, m) for n, a, b, m in ps]
            res.sort(key=lambda x: x[0])
            linha[modo] = res[0]
            for r, n, m in res:
                if r < m:
                    falhas.append((f"{tid} {modo}", f"{n}: {r:.2f} (min {m})"))
                if tudo:
                    print(f"{tid:18} {modo:6} {r:6.2f}  {n}")
        resumo.append(linha)
    print(f"{'tema':20}{'claro':>7}  {'pior par (claro)':44}{'escuro':>7}  pior par (escuro)")
    for l in resumo:
        a, b = l["claro"], l["escuro"]
        print(f"{l['tema']:20}{a[0]:7.2f}  {a[1][:43]:44}{b[0]:7.2f}  {b[1][:43]}")
    if falhas:
        print(f"\nFALHAS ({len(falhas)}):")
        for ctx, msg in falhas:
            print(f"  [{ctx}] {msg}")
        sys.exit(1)
    print(f"\nOK: {len(resumo)} temas, claro e escuro, todos os pares >= {MIN}:1")


if __name__ == "__main__":
    main()
