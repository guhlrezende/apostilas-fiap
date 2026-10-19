# Próximos passos (retomar daqui)

Estado em 19/10/2026. Nada foi enviado ao GitHub depois do primeiro commit (só a apostila de Machine Learning está publicada). Tudo o que está abaixo existe só no disco.

## Pronto, testado no navegador e ainda sem commit

| Apostila | Pasta | Capítulos | Observações |
|---|---|---|---|
| Bancos de Dados e SQL | `banco-de-dados/` | 8 | SQL real via sql.js (CDN). Bases em `bases.js`. Cap. 8 é complemento. |
| Python e Pensamento Computacional | `python/` | 9 | Código rastreado (`trace`) gerado com `scripts/trace_python.py`. Cap. 9 é complemento. |
| Cibersegurança | `ciberseguranca/` | 6 (+1 adiado) | Cap. 6 é complemento. O **cap. 7 (Kill Chain) está desligado** até o CP03 de Cyber vencer (26/10 23:59): depois disso, ponha `PUBLICAR_KILL_CHAIN = True` em `scripts/construtor/cy_manifest.py`, rode `cy_manifest.py` e `cy3.py` e ajuste `caps` em `data/apostilas.js`. Reusa a demo `inject` de `banco-de-dados/`. |
| Cloud e AWS | `cloud-aws/` | 7 | Preços e limites hedged ("mudam"). |
| Redes Neurais e Deep Learning | `redes-neurais/` | 8 | Resultados reais do scikit-learn em `rn-data.js`. Cap. 6 a 8 são complemento (backprop, deep learning, algoritmos genéticos). |
| Estatística com R e Python | `estatistica/` | 6 | Cap. 3, 5 e 6 são complemento. O código em R foi **rodado no R 4.6.1** em 19/10 (resultados batem com o texto); os exemplos estão em `estatistica/exemplos/exemplos.R`, linkado no cap. 4. |
| Gestão Ágil e Pitch | `gestao-agil/` | 6 | Sem nome de empresa parceira, professor ou colega. Limites de tempo dos eventos vêm do Guia do Scrum (complemento). |
| Sistemas Embarcados com ESP32 | `embarcados/` | 7 | Código C++ **compilado** em 19/10 com PlatformIO (esp32dev, Arduino, DHT sensor library 1.4.6), sem erro; não testado em placa. Sem a solução do CP3 aberto (só os conceitos do DHT22). |

Antes de subir: `python scripts/checar.py` (passa hoje), `python scripts/serve.py`, conferir celular e tema escuro, e a revisão independente (feita em 19/10 por quatro subagentes; os achados confirmados de fato, regra e bug foram corrigidos). O README e o `data/apostilas.js` já listam todas como prontas.

## Regras que valem para todas

- Repositório **público**: sem nome completo, RM, e-mail pessoal, nome de professor ou de colega, nem a empresa do Challenge. Sem solução de trabalho com prazo aberto (CP03 de Python, CP03 de Cyber, CP3 do AICSS, entre outros).
- Sem travessão no texto. Fio condutor em todo capítulo (`recap`, `gancho`, `ponte`). Todo número do texto tem de bater com o que a demo mostra.
- Os capítulos são gerados por scripts em `scripts/construtor/` (um `bld.py` com as funções `chapter`, `hub` e `manifest`, mais um arquivo por apostila). Depois de gerados, **dá para editar o HTML direto**. Para rodar um gerador: `cd scripts/construtor && python py1.py` (use `python` e não `python -I`, por causa dos imports locais).
- `scripts/trace_python.py` executa um trecho de Python e produz o passo a passo do componente `trace`.
- Um hook do projeto bloqueia a escrita de travessão pela ferramenta de edição.

## Pendências já conhecidas

- **Prazos abertos** que a apostila não pode antecipar: CP03 de Python (20/10), CP3 de AICSS (21/10), CP03 de Cyber (26/10). `scripts/checar.py` já barra alguns termos.
- Da revisão de 19/10, **não** corrigido (baixa prioridade): quizzes de Cyber e Cloud em que a opção certa é a mais longa; `.ponte` só no fim de cada capítulo (e não de cada seção); `aria-live` nas áreas de resposta das demos; teclado nas linhas da demo "ponte" do BD; Tab capturado no editor de SQL.
- Os exercícios dos slides de BD (cap. 4 seção 5 e cap. 7) trazem solução: conferir se algum vale como entrega com prazo aberto.
- Código **R** e **C++** foram verificados em 19/10 (R 4.6.1 + readxl, PlatformIO 6.2.0). Ferramentas instaladas no PC: R, RStudio, PlatformIO Core (`python -m platformio`). O C++ só foi compilado; falta rodar na placa/Wokwi.

- Os testes automáticos do painel de preview só disparam as demos depois de um quadro renderizado. Para testar, chame `Estudo.demos.x(el)` à mão.
- Quando chegar a próxima aula de uma disciplina, a nota vira capítulo novo: copie o último gerador de `scripts/construtor/` como base.
- Ativar o GitHub Pages só se o Gustavo pedir.
