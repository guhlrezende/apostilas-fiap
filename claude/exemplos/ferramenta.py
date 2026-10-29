"""Claude chamando uma ferramenta sua: o laço completo (apostila do Claude, cap. 5).

O Claude não executa nada sozinho: ele PEDE a ferramenta (bloco tool_use), o seu código
executa e devolve o resultado (bloco tool_result). O laço repete até o stop_reason ser end_turn.
Rodar:  pip install anthropic   e   python ferramenta.py   (precisa de ANTHROPIC_API_KEY)
"""
import anthropic

PRAZOS = {"1001": "15/11/2026", "1002": "03/12/2026"}  # dados fictícios


def consultar_prazo(numero: str) -> str:
    """A ferramenta de verdade: aqui seria uma consulta ao seu sistema."""
    return PRAZOS.get(numero, "processo não encontrado")


FERRAMENTAS = [{
    "name": "consultar_prazo",
    "description": "Consulta o próximo prazo de um processo pelo número interno de 4 dígitos.",
    "input_schema": {
        "type": "object",
        "properties": {"numero": {"type": "string", "description": "Número interno, ex.: 1001"}},
        "required": ["numero"],
    },
}]


def conversar(pergunta: str, cliente: anthropic.Anthropic) -> str:
    mensagens = [{"role": "user", "content": pergunta}]
    while True:
        resp = cliente.messages.create(
            model="claude-sonnet-5-5", max_tokens=500, tools=FERRAMENTAS, messages=mensagens,
        )
        if resp.stop_reason != "tool_use":                 # terminou: devolve o texto
            return "".join(b.text for b in resp.content if b.type == "text")
        mensagens.append({"role": "assistant", "content": resp.content})
        resultados = []
        for bloco in resp.content:                         # pode vir mais de um pedido
            if bloco.type == "tool_use" and bloco.name == "consultar_prazo":
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": bloco.id,               # liga o resultado ao pedido certo
                    "content": consultar_prazo(**bloco.input),
                })
        mensagens.append({"role": "user", "content": resultados})


if __name__ == "__main__":
    print(conversar("Qual o próximo prazo do processo 1002?", anthropic.Anthropic()))
