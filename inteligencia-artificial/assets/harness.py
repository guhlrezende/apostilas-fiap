"""Harness dos exercícios. Fonte única: o Worker (runner-worker.js) e o script de verificação
(scripts/rodar_pyodide.mjs) carregam ESTE arquivo, para o navegador e o terminal se comportarem igual.

_ia_rodar(setup, codigo, teste) devolve {'estado', 'saida', 'mensagem', 'linha'}.
Estados: pass, fail, error, setup_error, test_error. O tempo esgotado (timeout) é decidido por quem chama.
No teste ficam disponíveis verificar(cond, mensagem) e a variável saida (texto impresso pelo código do leitor).
"""
import sys, io, traceback, builtins


class _Verificacao(AssertionError):
    pass


def verificar(condicao, mensagem='A verificação falhou.'):
    if not condicao:
        raise _Verificacao(mensagem)


def _sem_input(*a, **k):
    raise RuntimeError('input() não funciona aqui. Use valores dentro do código.')


def _linha_do_usuario(exc, nome):
    tb = exc.__traceback__
    linha = None
    for fr in traceback.extract_tb(tb):
        if fr.filename == nome:
            linha = fr.lineno
    if linha is None and isinstance(exc, SyntaxError) and exc.filename == nome:
        linha = exc.lineno
    return linha


def _msg(exc):
    texto = exc.msg if isinstance(exc, SyntaxError) and exc.msg else str(exc)
    return type(exc).__name__ + (': ' + texto if texto else '')


def _ia_rodar(setup, codigo, teste):
    ns = {'__name__': '__main__', 'verificar': verificar}
    builtins_antigo = builtins.input
    builtins.input = _sem_input
    saida = io.StringIO()
    out_antigo, err_antigo = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = saida
    try:
        if setup:
            try:
                exec(compile(setup, '<preparo>', 'exec'), ns)
            except BaseException as e:
                return {'estado': 'setup_error', 'saida': saida.getvalue(), 'mensagem': _msg(e), 'linha': None}
        try:
            exec(compile(codigo, '<seu codigo>', 'exec'), ns)
        except BaseException as e:
            return {'estado': 'error', 'saida': saida.getvalue(), 'mensagem': _msg(e), 'linha': _linha_do_usuario(e, '<seu codigo>')}
        if teste:
            ns['saida'] = saida.getvalue()
            try:
                exec(compile(teste, '<teste>', 'exec'), ns)
            except _Verificacao as e:
                return {'estado': 'fail', 'saida': saida.getvalue(), 'mensagem': str(e), 'linha': None}
            except BaseException as e:
                ln = _linha_do_usuario(e, '<seu codigo>')
                if ln is not None:
                    return {'estado': 'error', 'saida': saida.getvalue(), 'mensagem': _msg(e) + ' (aconteceu ao testar a sua função)', 'linha': ln}
                return {'estado': 'test_error', 'saida': saida.getvalue(), 'mensagem': _msg(e), 'linha': None}
        return {'estado': 'pass', 'saida': saida.getvalue(), 'mensagem': '', 'linha': None}
    finally:
        sys.stdout, sys.stderr = out_antigo, err_antigo
        builtins.input = builtins_antigo
