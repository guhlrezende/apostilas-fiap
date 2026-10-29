"""Testa o laço de ferramenta SEM chave e SEM internet: um servidor falso responde no lugar da API.

Rodar:  pip install anthropic pytest   e   pytest -q
O teste confere três coisas: o código pede a ferramenta certa, devolve o tool_result com o
tool_use_id certo e para quando o stop_reason vira end_turn.
"""
import json

import anthropic
try:  # versões novas do SDK usam o pacote httpx2; as antigas, httpx
    import httpx2 as httpx
except ImportError:
    import httpx

from ferramenta import conversar

pedidos = []


def api_falsa(request: httpx.Request) -> httpx.Response:
    corpo = json.loads(request.content)
    pedidos.append(corpo)
    base = {"id": "msg_teste", "type": "message", "role": "assistant", "model": corpo["model"],
            "stop_sequence": None, "usage": {"input_tokens": 10, "output_tokens": 5}}
    if len(pedidos) == 1:  # 1a volta: o "Claude" pede a ferramenta
        return httpx.Response(200, json={**base, "stop_reason": "tool_use", "content": [
            {"type": "tool_use", "id": "toolu_1", "name": "consultar_prazo", "input": {"numero": "1002"}}]})
    return httpx.Response(200, json={**base, "stop_reason": "end_turn", "content": [
        {"type": "text", "text": "O próximo prazo é 03/12/2026."}]})


def test_laco_de_ferramenta():
    cliente = anthropic.Anthropic(api_key="falsa", http_client=httpx.Client(transport=httpx.MockTransport(api_falsa)))
    texto = conversar("Qual o próximo prazo do processo 1002?", cliente)
    assert texto == "O próximo prazo é 03/12/2026."
    assert len(pedidos) == 2
    devolvido = pedidos[1]["messages"][-1]["content"][0]
    assert devolvido == {"type": "tool_result", "tool_use_id": "toolu_1", "content": "03/12/2026"}
