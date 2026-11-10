# Próximos passos (retomar daqui)

Estado em 10/11/2026. Tudo o que está listado como publicado abaixo está no GitHub. O GitHub Pages **ainda não foi ligado**: é preciso ligar em Settings > Pages (Deploy from a branch, main, / root). O endereço esperado é https://guhlrezende.github.io/apostilas-fiap/ (confirmar abrindo).

## Publicadas (12)

Machine Learning, Bancos de Dados e SQL, Python e Pensamento Computacional, Cibersegurança (com a Kill Chain), Cloud e AWS, Redes Neurais e Deep Learning, Estatística com R e Python, Gestão Ágil e Pitch, Sistemas Embarcados com ESP32, **Terminal e Git** (6 cap.), **Deploy e Hospedagem** (7 cap.) e **GitHub: como usar do jeito certo** (9 cap., `github-uso/`, geradores `scripts/construtor/gh*.py`, base `docs/referencias/github.md`, teste das demos em `scripts/testar_demos_github.js`). As três últimas passaram por revisão adversarial e correção antes do commit. Tudo que depende do site do GitHub (PR real, proteção de branch, Actions rodando, Pages) está marcado "não testado aqui" nos capítulos.

## Em andamento
- **Temas visuais por apostila** (decisão: manter o fio comum do caderno e vestir cada tema por cima). Arquivos novos esperados: `assets/temas.css`, `scripts/construtor/temas.py`, `scripts/contraste_temas.py`, `docs/TEMAS.md`. **Integração ainda não feita**: pôr `data-tema` no `<html>` e o link das fontes nos geradores (`bld.py`), cartões do hub com a identidade de cada apostila, regenerar tudo, rodar `checar.py` e a `design-review` (celular 390px e tema escuro). Exige contraste mínimo 4,5:1.

## Fila (nesta ordem)

1. Integrar os temas e regenerar (acima).
2. **Docker**: base em `docs/referencias/ibm-docker-containers.md`. Precisa do Docker Desktop aberto para rodar build, run, volume e compose de verdade. Sem isso, nenhum exemplo pode aparecer como testado.
3. **Angular e Front-end**: base em `docs/referencias/ibm-frontend-angular.md` (angular.dev, versão 22). Criar projeto de teste em pasta temporária e rodar os exemplos; atenção ao espaço em disco (`node_modules`).
4. **Capítulos de complemento nas apostilas existentes**, a partir de `docs/referencias/ibm-complementos-existentes.md` e `kdnuggets-complementos.md`. Usar só o conceito dos artigos de blog e refazer exemplo e código rodando antes. Itens mais valiosos: ML (vazamento por engenharia de atributos, validação cruzada estratificada/por grupo/temporal, métricas de classificação, regularização, MLOps), BD (funções de janela, OLTP x OLAP, modelagem dimensional, NoSQL e CAP), Cloud (serverless, multicloud), Cyber (zero trust, NIST CSF, resposta a incidentes), Estatística (pressupostos da regressão, multicolinearidade), Embarcados (UART/SPI/I2C, ADC).
5. Pendências de baixa prioridade da revisão de 19/10: quizzes de Cyber e Cloud em que a opção certa é a mais longa; `aria-live` nas áreas de resposta das demos; teclado nas linhas da demo "ponte" do BD; Tab capturado no editor de SQL.

## Regras que valem para todas

- Repositório **público**: sem nome completo, RM, e-mail pessoal, nome de professor ou de colega, nem a empresa do Challenge. Sem solução de trabalho com prazo aberto (Sprint 2 do Challenge até 30/11, CP3 de ML e de Redes Neurais, Sprint Retrô).
- Sem travessão no texto. Fio condutor em todo capítulo (`recap`, `gancho`, `ponte`). Todo número do texto tem de bater com o que a demo mostra.
- **Fatos sobre produto e plataforma só com fonte lida e data.** Preço, plano gratuito e limite sem página oficial lida viram "confira na página oficial". Comando mostrado como saída real tem de ter sido rodado; o resto fica "não testado aqui", visível no texto.
- Lições das revisões: no PowerShell 5.1 limpo o `>` grava UTF-16 (quebra `.gitignore`; use `Set-Content -Encoding ascii`); `git rm --cached` não tira segredo do histórico (revogar a credencial primeiro); `git revert` de merge exige `-m 1`.
- Geradores em `scripts/construtor/` (um `bld.py` com `chapter`, `hub` e `manifest`, mais arquivos por apostila). Edite o gerador e rode de novo, não só o HTML. Rode com `python` (não `-I`). Verificar sempre: `python scripts/checar.py`.
- Commit e push só quando o dono do repo mandar.

## Ferramentas e ambiente

R 4.6.1, RStudio, PlatformIO (`python -m platformio`), Node 24, Python 3.13, Git 2.56 e `gh` 2.101. O disco C: está com pouco espaço livre (cerca de 12 GB): cuidado com Docker e `node_modules`.
