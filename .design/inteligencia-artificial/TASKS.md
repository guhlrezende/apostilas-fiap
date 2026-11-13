# Build Tasks: Apostila "Inteligência Artificial"

Generated from: .design/inteligencia-artificial/DESIGN_BRIEF.md
Date: 2026-11-13

Filosofia: **Laboratório** (relatório científico editorial, branco-gelo, grafite, verde-laboratório; cor por parte só no mapa). Tokens prontos em `inteligencia-artificial/assets/tokens.css`.

Regras do repositório que valem em toda tarefa: sem travessão, PT-BR, repositório público (sem dado pessoal), `python scripts/checar.py` limpo, verificação visual em 390px, tema escuro e console sem erro. `assets/estudo.css` e `estudo.js` não são alterados: a IA tem casca e CSS próprios.

## Foundation
- [x] **Casca da apostila (topo, leitura, tema, progresso)**: página-modelo em `inteligencia-artificial/` com coluna de leitura de 68ch, grade de papel milimetrado, alternador claro/escuro/sistema e barra de progresso; fontes com fallback de sistema. Done: abre em `python scripts/serve.py`, passa em 390/768/1024/1440, contraste conferido. _Modifies: padrão `capitulos.js` e `data/apostilas.js` (reaproveita o formato); CSS e JS próprios; tokens novos._
- [x] **Mapa da trilha**: sidebar (gaveta no celular) com as 5 partes e 20 capítulos, cor da parte, capítulo atual, concluídos e progresso em `localStorage` (try/catch), navegável por teclado. Done: clicar leva ao capítulo, estado não depende só de cor. _New component. Depends on: Casca._
- [x] **Fontes locais**: baixar Fraunces, IBM Plex Sans e JetBrains Mono (woff2, só os pesos usados, subset latino) para `assets/fontes/` com `@font-face` e `font-display: swap`; decidir a serifa dos títulos com o texto renderizado. Done: nenhuma requisição externa na aba Rede. Requer ok do dono com origem e tamanho. _New. Depends on: Casca._

## Core UI
- [x] **Célula de exercício com Pyodide**: editor, Rodar, Enviar, dica e solução em etapas; Pyodide em Web Worker servido localmente, timeout com reinício do Worker e os 6 estados de resultado (pass, fail, error, timeout, setup_error, test_error) com `aria-live`. Versão e origem do Pyodide e do editor conferidas em fonte oficial lida, com data. Done: um exercício de exemplo passa, falha, dá erro e é cortado num `while True`, sem travar a página. _New component. É o item de maior risco: vem antes dos demais. Depends on: Casca._
- [x] **Blocos de leitura**: recap, gancho, ponte, figura numerada com legenda e alt, nota de margem, "Para ir além" (só título e autor), bloco de código com saída real colada e copiar. _Modifies o vocabulário `.recap/.gancho/.ponte`; figura, nota e saída são new._
- [ ] **Quiz, lacuna e arrastar** (rodada 1 feita em 13/11: quiz e lacuna; falta arrastar e soltar): quiz de cenário com explicação para acerto e erro, lacunas e arrastar e soltar com versão para toque. Done: tudo operável por teclado. _Modifies `.quiz` e `.sorter` do modelo._

## Interactions & States
- [ ] **Ache o erro, glossário em tooltip, laboratório de prompt** (rodada 1 feita em 13/11: glossário; faltam ache o erro e laboratório): clicar na linha suspeita; tooltips fixos no `body` (nunca cortados, também por toque e teclado); laboratório com respostas simuladas e marcadas como tal. Covers: hover, foco, toque, vazio, erro. _New components._
- [x] **Estados de carga e falha do Pyodide**: progresso na primeira carga, mensagem honesta se falhar (sem internet para pacotes, arquivo ausente) e nova tentativa. _Depends on: Célula de exercício._

## Piloto
- [x] **Capítulo 1, "O mapa da IA"**: página real usando todos os blocos, com ao menos um exercício executável, quiz, figura, glossário e ponte para o Cap. 2; texto e números de demos rodadas. Fatos de linha do tempo só de fonte lida, com data. Escrito por escritor `sonnet`, revisado pelo `refutador`. _Depends on: todas as tarefas acima. Registrar o gasto de tokens no Registro de uso._
- [x] **Registro da apostila**: entrada em `data/apostilas.js` (`pronta` só quando houver capítulo publicado) e `capitulos.js` da IA com a linha do Cap. 1. _Modifies `data/apostilas.js`._

## Responsive & Polish
- [ ] **Passe responsivo**: 390, 768, 1024 e 1440; editor com rolagem interna, sem rolagem horizontal da página; alvos de toque de 44px; tema escuro.
- [ ] **Passe de acessibilidade**: contraste 4,5:1 (3:1 em interface) nos dois temas e nas 5 cores do mapa; foco visível; teclado em todo exercício; `prefers-reduced-motion`; cor nunca como único sinal; fonte do corpo a partir de 16px.

## Review
- [ ] **Design review**: rodar `/design-review` contra o brief, com capturas em `.design/inteligencia-artificial/screenshots/`. Depois, `design:accessibility-review`.
