"""Gerador da apostila GitHub: como usar do jeito certo (pasta github-uso/).

Uso:  python scripts/construtor/gh.py
Gera: github-uso/index.html (hub), capitulos.js e os nove capítulos.
As demos (github-uso/demos/*.js) são escritas à mão; este script só gera o HTML.
"""
from gh_base import *
import gh1, gh2, gh3

manifest(PASTA, "github-uso", TITULO, CAPS)
hub(PASTA, TITULO, "Complemento · Colaboração, segurança e automação no GitHub", "Apostila de GitHub: como usar do jeito certo",
    "Da conta ao pull request, da proteção da main ao segredo que vazou: como usar o GitHub de forma correta e profissional, com cinco simuladores e laboratórios para fazer no seu repositório.",
    ["<b>9</b> capítulos", "<b>~6h55</b> de estudo ativo", "5 demos: tipos de merge, vida de um PR, fork e upstream, regras da main e segredo vazado", "complemento, não foi dado em aula"],
    '<p>Esta apostila é <mark class="hl">complemento</mark>: <b>nada dela foi dado em aula</b>. Ela continua a de <a href="../terminal-git/index.html">Terminal e Git</a> e <b>assume o Git básico</b> dos capítulos 5 e 6 de lá (commit, branch, merge, remoto, push). Aqui o foco é o que o GitHub acrescenta. Primeiro a conta e o repositório, depois como o seu computador conversa com ele e como você prova quem é. Em seguida, o trabalho em equipe: issues, branches, pull request e os três tipos de merge, fork e contribuição. Por fim, o que protege tudo isso: regras para a main, Actions, releases, segurança, recuperação de erros e um perfil honesto.</p>'
    '<p>O Git eu rodei de verdade, com repositórios locais fazendo o papel do GitHub. <b>Tudo que depende do site</b> (PR real, revisão, Actions rodando, proteção de branch, Pages, releases, secret scanning) vem marcado como <mark class="hl p">não testado aqui</mark>. Eu não usei nenhuma conta do GitHub para escrever isto. <b>Preços e limites de plano não aparecem como fato.</b></p>',
    'Cada capítulo termina com um <b>laboratório</b>: passos para fazer num repositório <b>seu</b>, cada um com a prova de que deu certo. As fontes (documentação do GitHub, Pro Git, manual do <code>gh</code>) estão no fim de cada capítulo e aqui no hub, lidas em 10/11/2026. Telas e planos do GitHub mudam: onde está escrito <b>confira</b>, eu não afirmo.',
    extra_scripts=[])

p = REPO + PASTA + "/index.html"
s = open(p, encoding="utf-8").read()
s = s.replace("  <footer class=\"rodape\">", fontes_todas() + "\n  <footer class=\"rodape\">", 1)
s = s.replace("Atualizada nos domingos, conforme as aulas da semana. Projeto de estudo, feito a partir das anotações pessoais de aula.",
              "Projeto de estudo. Complemento a partir de leitura e de testes; não é material de aula.")
open(p, "w", encoding="utf-8").write(s)

gh1.cap1(); gh1.cap2(); gh1.cap3(); gh2.cap4(); gh2.cap5(); gh2.cap6(); gh3.cap7(); gh3.cap8(); gh3.cap9()
print("github-uso ok: hub + 9 capítulos")
