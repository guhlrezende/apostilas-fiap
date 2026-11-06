"""Gerador da apostila Deploy e Hospedagem (pasta deploy-hospedagem/).

Uso:  python scripts/construtor/dp.py
Gera: deploy-hospedagem/index.html (hub), capitulos.js e os sete capítulos.
As demos (deploy-hospedagem/demos/*.js) são escritas à mão; este script só gera o HTML.
"""
from dp_base import *
import dp1, dp2, dp3

manifest(PASTA, "deploy-hospedagem", TITULO, CAPS)
hub(PASTA, TITULO, "Complemento · Do arquivo ao site no ar", "Apostila de Deploy e Hospedagem",
    "Como colocar um site no ar: a web por dentro, DNS, HTTPS, tipos de hospedagem, três caminhos de publicação, CI/CD, segredos e o que fazer depois que subiu, com cinco simuladores.",
    ["<b>7</b> capítulos", "<b>~4h55</b> de estudo ativo", "5 demos: HTTP, DNS, certificado, onde hospedar e CI/CD", "complemento, não foi dado em aula"],
    '<p>Esta apostila é <mark class="hl">complemento</mark>: <b>nada dela foi dado em aula</b>. A pergunta que a conduz é: <b>como um arquivo no meu computador vira um site que qualquer pessoa abre?</b> Primeiro vem a base (cliente, servidor, HTTP, IP e portas), depois o nome (DNS) e a conversa protegida (HTTPS e certificado). Em seguida, onde o site pode morar (estático, PaaS, VPS, serverless) e três jeitos de publicar um site estático. Por fim, automatizar com CI/CD sem vazar segredos, e o que olhar depois que subiu.</p>'
    '<p>O que eu consegui rodar vem sem aviso; o que não consegui (nenhum deploy real, nginx, certbot, VPS) vem marcado como <mark class="hl p">não testado aqui</mark>. <b>Preços, planos gratuitos e telas de painel não aparecem como fato</b>: eles mudam, e a regra é conferir na página oficial do serviço.</p>',
    'O que veio de leitura (IBM e documentação oficial de cada ferramenta) está marcado como <b>complemento</b>, e cada capítulo termina com as fontes. Os comandos foram rodados em um Windows 11 com Git Bash e PowerShell 5.1, contra sites públicos de teste, servidores locais e pastas temporárias. Os domínios e IPs dos exemplos (<code>meusite.example</code>, <code>exemplo.test</code>) são inventados.',
    extra_scripts=[])

p = REPO + PASTA + "/index.html"
s = open(p, encoding="utf-8").read()
s = s.replace("  <footer class=\"rodape\">", fontes_todas() + "\n  <footer class=\"rodape\">", 1)
s = s.replace("Atualizada nos domingos, conforme as aulas da semana. Projeto de estudo, feito a partir das anotações pessoais de aula.",
              "Projeto de estudo. Complemento a partir de leitura e de testes; não é material de aula.")
open(p, "w", encoding="utf-8").write(s)

dp1.cap1(); dp1.cap2(); dp2.cap3(); dp2.cap4(); dp3.cap5(); dp3.cap6(); dp3.cap7()
print("deploy-hospedagem ok: hub + 7 capítulos")
