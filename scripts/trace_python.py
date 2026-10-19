"""Gera o JSON do componente `trace` (código passo a passo) executando um trecho de Python de verdade.

Uso no Python:
    from trace_python import trace_html
    html = trace_html("Título", "x = 5\\nprint(x)", notas={1: "explicação da linha 1"}, entradas=["10"])

As linhas são numeradas a partir de 1. `notas` mapeia o número da linha para o texto exibido
quando esse passo é mostrado. O valor pode ser um texto, uma lista (um texto por visita à linha)
ou uma função que recebe as variáveis do passo e devolve o texto. `entradas` são as respostas dadas ao input(). Como o número de
passos cresce rápido em laços, use ranges pequenos (o componente corta em `max_passos`).
"""
import builtins
import html as _html
import io
import json
import sys


def _fmt(v):
    if isinstance(v, float) and v == v and abs(v) != float('inf') and v == int(v):
        return {"__py": repr(v)}  # 150.0 (o JSON perderia o .0)
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple, dict, set)):
        try:
            return json.loads(json.dumps(v if not isinstance(v, (set, tuple)) else list(v), default=str))
        except Exception:
            return repr(v)
    return repr(v)


def trace_steps(code, entradas=(), notas=None, max_passos=60, ocultar=()):
    linhas = code.split("\n")
    notas = notas or {}
    passos, saida, it = [], io.StringIO(), iter(entradas)
    vis = {}
    glb = {"__name__": "__main__"}

    def meu_input(prompt=""):
        resp = next(it)
        saida.write(f"{prompt}{resp}\n")
        return resp

    def meu_print(*a, **k):
        k.pop("file", None)
        builtins.print(*a, file=saida, **k)

    def vars_do_frame(frame):
        base = frame.f_globals if frame.f_code.co_name == "<module>" else frame.f_locals
        out = {}
        for k, v in base.items():
            if k.startswith("__") or k in ocultar or callable(v) and not isinstance(v, type) and getattr(v, "__module__", None) == "__main__":
                continue
            if callable(v) or isinstance(v, type(sys)):
                continue
            out[k] = _fmt(v)
        return out

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<trace>":
            return None
        if event == "line" and len(passos) < max_passos:
            n = frame.f_lineno
            vis[n] = vis.get(n, 0) + 1
            v = vars_do_frame(frame)
            nota = notas.get(n, "")
            if callable(nota):
                nota = nota(v) or ""
            elif isinstance(nota, (list, tuple)):
                nota = nota[min(vis[n], len(nota)) - 1]
            passos.append({"l": n - 1, "v": v, "o": saida.getvalue().rstrip("\n"), "n": nota})
        return tracer

    gl = dict(glb, input=meu_input, print=meu_print)
    gl["__builtins__"] = builtins
    compilado = compile(code, "<trace>", "exec")
    sys.settrace(tracer)
    try:
        exec(compilado, gl)
    finally:
        sys.settrace(None)
    final_v = {k: _fmt(v) for k, v in gl.items() if not k.startswith("__") and k not in ("input", "print") and not callable(v) and not isinstance(v, type(sys))}
    passos.append({"l": -1, "v": final_v, "o": saida.getvalue().rstrip("\n"), "n": notas.get(0, "Fim do programa. O estado final das variáveis está na tabela.")})
    return {"code": linhas, "steps": passos}


def trace_html(titulo, code, notas=None, entradas=(), max_passos=60, ocultar=()):
    d = trace_steps(code.strip("\n"), entradas, notas, max_passos, ocultar)
    d["titulo"] = titulo
    texto = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    return f'<div class="demo" data-demo="trace"><script type="application/json">{texto}</script></div>'


if __name__ == "__main__":
    print(trace_html("Teste", "a = 5\nb = 7\na, b = b, a\nprint(a, b)"))
