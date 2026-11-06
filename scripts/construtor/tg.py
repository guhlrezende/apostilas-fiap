"""Gerador da apostila Terminal e Git (pasta terminal-git/).

Uso:  python scripts/construtor/tg.py
Gera: terminal-git/index.html (hub), terminal-git/capitulos.js e os seis capítulos.
As demos (terminal-git/demos/*.js) são escritas à mão; este script só gera o HTML.
"""
from tg_base import *
import tg1, tg2, tg3

manifest(PASTA, "terminal-git", TITULO, CAPS)
hub(PASTA, TITULO, "Complemento · Linha de comando e controle de versão", "Apostila de Terminal e Git",
    "Do primeiro comando ao pull request: terminal, pipes, permissões, SSH, Git e GitHub, com PowerShell e Git Bash lado a lado e um terminal simulado para treinar.",
    ["<b>6</b> capítulos", "<b>~3h55</b> de estudo ativo", "4 demos: terminal, pipes, permissões e grafo do Git", "complemento, não foi dado em aula"],
    '<p>Esta apostila é <mark class="hl">complemento</mark>: <b>nada dela foi dado em aula</b>. Ela anda em degraus. Primeiro você aprende a falar com o computador por texto (terminal, shell, arquivos). Depois a ligar comandos pequenos para fazer algo maior (pipes, redirecionamento, grep, awk). Em seguida vem o que faz isso útil de verdade: permissões, variáveis, scripts, processos, curl e SSH. Por fim, o Git guarda o histórico e o GitHub leva isso para o trabalho em equipe.</p>'
    '<p>Em todo comando que existe nos dois mundos, mostro o <b>Git Bash e o PowerShell</b>. O que eu consegui rodar vem sem aviso; o que não consegui vem marcado como <mark class="hl p">não testado aqui</mark>.</p>',
    'O que veio de leitura (IBM, Microsoft, documentação do Git) está marcado como <b>complemento</b>, e cada capítulo termina com as fontes. <b>Algumas fontes da IBM têm de 2011 a 2022</b>: confira flags e versões antes de depender delas. Os comandos foram rodados em um Windows 11 com Git Bash e PowerShell 5.1.',
    extra_scripts=[])

# o hub do bld não tem seção de fontes: acrescento antes do rodapé
p = REPO + PASTA + "/index.html"
s = open(p, encoding="utf-8").read()
s = s.replace("  <footer class=\"rodape\">", fontes_todas() + "\n  <footer class=\"rodape\">", 1)
s = s.replace("Atualizada nos domingos, conforme as aulas da semana. Projeto de estudo, feito a partir das anotações pessoais de aula.",
              "Projeto de estudo. Complemento a partir de leitura e de testes; não é material de aula.")
open(p, "w", encoding="utf-8").write(s)

tg1.cap1(); tg1.cap2(); tg2.cap3(); tg2.cap4(); tg3.cap5(); tg3.cap6()
print("terminal-git ok: hub + 6 capítulos")
