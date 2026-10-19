import os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")).replace(chr(92), "/") + "/"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Caveat:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'

def chapter(pasta, n, slug, apostila_titulo, titulo, kicker, sub, chips, body, scripts=(), sql=False):
    """Escreve <pasta>/cap-N-slug.html. scripts: caminhos relativos à pasta da apostila."""
    sc = "".join(f'<script src="{s}"></script>\n' for s in scripts)
    sqls = '<script src="../assets/estudo-sql.js"></script>\n' if sql else ""
    chips_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Cap. {n}: {titulo} | Apostila de {apostila_titulo}</title>
{FONTS}
<link rel="stylesheet" href="../assets/estudo.css">
<script src="../assets/estudo.js"></script>
{sqls}<script src="capitulos.js"></script>
{sc}</head>
<body data-cap="{n}" data-root="../">
<article class="paper">

<header class="capa">
  <div class="kicker">{kicker}</div>
  <h1>{titulo}</h1>
  <p class="sub">{sub}</p>
  <div class="meta">{chips_html}</div>
  <span class="num">{n}</span>
</header>

{body}

</article>
</body>
</html>
'''
    os.makedirs(REPO + pasta, exist_ok=True)
    open(REPO + pasta + f"/cap-{n}-{slug}.html", "w", encoding="utf-8").write(html)

def hub(pasta, apostila_titulo, kicker, titulo, sub, chips, intro_html, como_html="", extra_scripts=()):
    sc = "".join(f'<script src="{s}"></script>\n' for s in extra_scripts)
    chips_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Apostila de {apostila_titulo}</title>
{FONTS}
<link rel="stylesheet" href="../assets/estudo.css">
<script src="../assets/estudo.js"></script>
<script src="capitulos.js"></script>
{sc}</head>
<body data-hub data-root="../">
<article class="paper">
  <header class="capa">
    <div class="kicker">{kicker}</div>
    <h1>{titulo}</h1>
    <p class="sub">{sub}</p>
    <div class="meta">{chips_html}</div>
    <span class="num">{apostila_titulo[:2].upper()}</span>
  </header>

  <section class="sec">
    <h2><span class="sn">1</span>A história que esta apostila conta</h2>
    {intro_html}
    <div class="thread" id="thread"></div>
  </section>

  <section class="sec">
    <h2><span class="sn">2</span>Os capítulos</h2>
    <div class="hubgrid" id="caps"></div>
  </section>

  <section class="sec">
    <h2><span class="sn">3</span>Como estudar com isto aqui</h2>
    <div class="grid2">
      <div class="nota"><span class="lbl">Dica</span>Faça um capítulo por sessão. Leia o <b>gancho</b> do começo, mexa em <b>todas</b> as demos (é onde a ideia fixa) e só então abra as respostas dos testes.</div>
      <div class="nota lembra"><span class="lbl">Lembra</span>{como_html or "O que não foi dado em aula vem marcado como <b>complemento</b>. Números conferidos rodando aparecem como tal."}</div>
    </div>
  </section>

  <footer class="rodape">Atualizada nos domingos, conforme as aulas da semana. Projeto de estudo, feito a partir das anotações pessoais de aula.</footer>
</article>
</body>
</html>
'''
    open(REPO + pasta + "/index.html", "w", encoding="utf-8").write(html)

def manifest(pasta, id_, titulo, caps):
    import json
    js = "/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */\nwindow.APOSTILA = " + json.dumps({"id": id_, "titulo": titulo, "caps": caps}, ensure_ascii=False, indent=2) + ";\n"
    open(REPO + pasta + "/capitulos.js", "w", encoding="utf-8").write(js)

# blocos reutilizáveis
def ponte(q, p, titulo="Para onde vamos agora"):
    return f'<div class="ponte rv"><div class="t">{titulo}</div><div class="q">{q}</div><p>{p}</p></div>'

def recap(txt, titulo="Onde paramos"):
    return f'<div class="recap rv"><b>{titulo}</b>{txt}</div>'

def quiz(n, ans, q, opts, fb):
    o = "".join(f'<button data-k="{k}">{t}</button>' for k, t in opts)
    return f'<div class="quiz" data-ans="{ans}"><span class="qt">Pergunta {n}</span><p class="qq">{q}</p>\n    <div class="opts">{o}</div>\n    <div class="fb">{fb}</div></div>'

def flash(cards):
    c = "".join(f'<button class="fc" type="button"><span class="fr"><small>Pergunta</small><b>{f}</b></span><span class="bk">{v}</span></button>' for f, v in cards)
    return f'<h3>Flashcards (clique para virar)</h3>\n  <div class="flash">{c}</div>'

def resumo(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="resumo rv"><h3>Cola da prova</h3><ul>{li}</ul></div>'

import html as _h
def sqlbox(db, q, titulo="Rode o SQL aqui", expect=None):
    q = _h.escape(q, quote=False)
    e = f' data-expect="{expect}"' if expect is not None else ""
    return f'<div class="demo" data-demo="sql" data-db="{db}"{e} data-titulo="{titulo}"><pre class="q">{q}</pre></div>'
