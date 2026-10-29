"""Primeira chamada à API do Claude (apostila do Claude, cap. 4).

Precisa de uma chave da Claude Console na variável de ambiente ANTHROPIC_API_KEY.
Rodar:  pip install anthropic   e depois   python primeira_chamada.py
"""
import anthropic

cliente = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do ambiente

resposta = cliente.messages.create(
    model="claude-sonnet-5-5",   # ID do modelo, conferido na página de modelos em 29/10/2026
    max_tokens=500,              # teto da resposta, em tokens
    system="Você é um tutor de programação. Responda em português, em no máximo 3 frases.",
    messages=[
        {"role": "user", "content": "O que é uma API, explicado para quem vem do Direito?"},
    ],
)

print(resposta.content[0].text)   # o texto da resposta
print(resposta.stop_reason)       # por que parou: end_turn, max_tokens, tool_use...
print(resposta.usage.input_tokens, resposta.usage.output_tokens)  # o que você paga
