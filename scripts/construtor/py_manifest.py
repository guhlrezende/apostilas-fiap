import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # trace_python.py
from bld import *
from trace_python import trace_html

PASTA = "python"
TITULO = "Python e Pensamento Computacional"
CAPS = [
 dict(n=1, file="cap-1-linguagens-e-variaveis.html", titulo="Linguagens, variáveis e tipos", aula="Aula 1", tempo=35,
      resumo="Compilada x interpretada x transpilada, variáveis e constantes, tipos básicos e operadores.",
      pergunta="Já sei guardar valores. Como faço o programa receber dados de quem o usa?"),
 dict(n=2, file="cap-2-entrada-e-f-strings.html", titulo="Entrada, operadores e f-strings", aula="Aula 2", tempo=35,
      resumo="input() sempre devolve texto, conversão com int e float, contas e formatação de saída.",
      pergunta="O programa lê e calcula, mas faz sempre a mesma coisa. Como ele decide o que fazer?"),
 dict(n=3, file="cap-3-decisoes.html", titulo="Decisões: if, lógica e match-case", aula="Aulas 2, 4 e 7", tempo=45,
      resumo="if/elif/else, comparações, and/or/not e o match-case para menus e faixas.",
      pergunta="Decide uma vez. E se eu tiver muitos valores, ou precisar repetir a decisão?"),
 dict(n=4, file="cap-4-listas.html", titulo="Listas e outras coleções", aula="Aula 5", tempo=40,
      resumo="Índices, fatias, métodos, mutabilidade, e uma visão de tupla, dicionário e conjunto.",
      pergunta="Tenho uma coleção de valores. Como aplico o mesmo tratamento a cada um sem escrever 100 vezes?"),
 dict(n=5, file="cap-5-lacos.html", titulo="Laços: for e while", aula="Aulas 5 e 6", tempo=40,
      resumo="for sobre sequências, while por condição, range, break, continue e o perigo do loop infinito.",
      pergunta="Já repito e decido. Como organizo dados em duas dimensões e blocos reutilizáveis?"),
 dict(n=6, file="cap-6-matrizes-e-funcoes.html", titulo="Matrizes e funções", aula="Aula 7", tempo=45,
      resumo="Lista de listas, matriz[y][x], percorrer com for aninhado, def, parâmetros, return e escopo.",
      pergunta="Meu código funciona no meu computador. Como guardo as versões e compartilho com outras pessoas?"),
 dict(n=7, file="cap-7-git-e-github.html", titulo="Git e GitHub", aula="Aula 3", tempo=35,
      resumo="Controle de versão, staging, commit, push, repositório público e privado, e boas práticas.",
      pergunta="Tenho todas as peças. Dá para usá-las num problema de verdade, sem fórmula pronta?"),
 dict(n=8, file="cap-8-o-cofre.html", titulo="Algoritmo na prática: o cofre", aula="Aula 9", tempo=40,
      resumo="Os quatro pilares do pensamento computacional aplicados a um jogo de senha, com um solver que elimina hipóteses.",
      pergunta="Escrevi programas inteiros. O que mais o Python tem que eu ainda não usei?"),
 dict(n=9, file="cap-9-alem-do-basico.html", titulo="Para ir além (complemento)", aula="Complemento", tempo=45,
      resumo="Strings, dicionários na prática, arquivos, tratamento de erros, módulos e boas práticas.",
      pergunta=""),
]

if __name__ == "__main__":
    manifest(PASTA, "python", TITULO, CAPS)
    hub(PASTA, TITULO, "Computational Thinking with Python", "Apostila de Python e Pensamento Computacional",
        "De guardar um valor em uma variável até resolver um jogo de senha com algoritmo. O código roda passo a passo na página, para você ver cada variável mudar.",
        ["<b>9</b> capítulos", "<b>~6h</b> de estudo ativo", "código <b>rastreado</b> linha a linha"],
        '<p>Aprender Python não é decorar comandos. É aprender a <mark class="hl">pensar em passos</mark>: dividir o problema, achar padrões, abstrair e escrever uma regra que o computador possa seguir. Cada capítulo acrescenta uma peça e abre com a pergunta que a peça anterior deixou sem resposta.</p>',
        'Os trechos de código desta apostila foram <b>executados de verdade</b>: o passo a passo e as saídas mostrados vêm do próprio Python, e não de um palpite.')
    print("manifest ok")
