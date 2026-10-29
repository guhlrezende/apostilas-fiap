"""Análise de dados com conferência (apostila de AI Builder, cap. 7).

A IA escreve a primeira versão do código; você confere os números com uma segunda conta
independente antes de colocar qualquer valor em um relatório.
Rodar:  pip install pandas  e depois  python analise.py
"""
import pandas as pd

# Dados fictícios de atendimentos de uma loja (mesmos números do capítulo).
dados = pd.DataFrame({
    "canal":   ["WhatsApp", "WhatsApp", "E-mail", "WhatsApp", "E-mail", "Telefone", "E-mail", "Telefone"],
    "minutos": [4, 6, 18, 5, 22, 9, 15, 11],
    "resolvido": [True, True, False, True, True, True, False, True],
})

# 1) A pergunta de negócio: qual canal resolve mais rápido e com mais sucesso?
resumo = dados.groupby("canal").agg(
    atendimentos=("minutos", "size"),
    minutos_medio=("minutos", "mean"),
    taxa_resolucao=("resolvido", "mean"),
).round(2)
print(resumo)

# 2) A conferência: refazer uma das contas por outro caminho.
email = dados[dados["canal"] == "E-mail"]["minutos"]
media_manual = sum(email) / len(email)
assert round(media_manual, 2) == resumo.loc["E-mail", "minutos_medio"], "as duas contas não batem"
print(f"Conferido: média do e-mail = {media_manual:.2f} min")
