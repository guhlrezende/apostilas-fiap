# Design Brief: Apostila "Inteligência Artificial" (trilha completa)

Decidido em 13/11/2026. Direção escolhida pelo dono: **Laboratório**, com a cor por parte da trilha **só no mapa de navegação**.

## Problem

Quem sabe Python básico e quer entender IA de verdade encontra duas coisas ruins: material que só mostra o resultado (prompt mágico, caixa preta) ou texto técnico que não deixa mexer. Numa trilha de 20 capítulos é fácil se perder: não saber onde está, o que já viu e por que o capítulo existe. E exercício que não roda no lugar vira leitura passiva.

## Solution

Uma apostila que parece um **caderno de laboratório digital**: cada conceito vira um experimento que o leitor roda (Python no navegador, com teste automático) e cujo resultado confere com o texto. Um mapa fixo mostra as 5 partes e os 20 capítulos, com progresso. O texto longo é confortável; o bloco de exercício é o que se destaca na página.

## Experience Principles

1. **Rodar antes de acreditar** -- todo número do texto vem de código que o leitor pode executar; o experimento é o protagonista da seção, não um enfeite no fim.
2. **Orientação constante** -- o leitor sempre sabe em que parte e capítulo está, o que já fez e qual é a ponte para o próximo. A cor aparece só onde ajuda a se situar (mapa), não decora o texto.
3. **Texto longo em primeiro lugar** -- leitura confortável vence efeito visual. Pouco chrome, bastante respiro, uma coluna de leitura.

## Aesthetic Direction

- **Philosophy**: relatório de laboratório / caderno científico editorial. Figuras numeradas ("Fig. 3"), notas de margem, protocolo de experimento.
- **Tone**: calmo, preciso, curioso, sem pressa. Como um estudante cuidadoso explicando, não como produto de IA.
- **Reference points**: artigos do Distill e do Observable, documentação de bibliotecas bem escritas, cadernos de laboratório impressos.
- **Anti-references**: roxo e ciano de "produto de IA", gradiente, brilho neon, robô e cérebro como ilustração, efeito de vidro, painel de chat falso. Também não o caderno creme com caneta azul das outras apostilas.

## Existing Patterns

Existe uma base compartilhada (`assets/estudo.css`, `assets/estudo.js`) que **não será alterada**. A apostila de IA terá CSS e tokens próprios em `inteligencia-artificial/assets/`, reaproveitando só o vocabulário de componentes.

- Typography: Inter, Bricolage Grotesque, Caveat, JetBrains Mono (identidade caderno). A IA troca por serifa editorial + IBM Plex Sans + JetBrains Mono, servidas localmente.
- Colors: papel creme `#fbf6e8`, tinta `#1d2333`, caneta `#2c52c4`. A IA usa branco-gelo, grafite e verde-laboratório (~`#0B7A5C`); tema escuro nativo.
- Spacing: escala própria, definida nos tokens.
- Components: casca montada por `estudo.js` a partir de `capitulos.js`; classes como `.recap`, `.gancho`, `.ponte`, `.quiz`, `.sorter`, `.stepper`, `.demo`. Demos são funções ligadas por `data-demo`.

## Component Inventory

| Component | Status | Notes |
| --- | --- | --- |
| Casca (topo, sidebar, progresso) | Modify | Visual novo; mesma estrutura e `capitulos.js` |
| Mapa da trilha | New | 5 partes, 20 capítulos, cor por parte, progresso e capítulo atual |
| Célula de exercício (editor + Rodar + Enviar) | New | Pyodide em Web Worker, 6 estados de resultado |
| Resultado do teste | New | pass, fail, error, timeout, setup_error, test_error, cada um com mensagem própria |
| Figura numerada com legenda | New | "Fig. N", SVG ou canvas, alt text |
| Nota de margem / "Para ir além" | New | Só título e autor nos livros |
| Recap, gancho, ponte | Exists | Estilo novo |
| Quiz (cenário, lacuna) | Modify | Foco em aplicação, não memória |
| Arrastar e soltar | Modify | Com versão para toque |
| "Ache o erro" | New | Clicar na linha suspeita |
| Laboratório de prompt | New | Respostas simuladas e marcadas como simuladas |
| Glossário em tooltip | New | Fixo no `body`, nunca cortado |
| Bloco de código | Modify | Saída real colada, cópia com um clique |
| Model card / projeto por parte | New | Estrutura de entrega do projeto final |
| Alternar tema | Exists | Claro e escuro |

## Key Interactions

- **Rodar** executa o código sem teste; **Enviar** roda o teste e só conta tentativa se o código mudou. O estado vira mensagem clara; o traceback mostra só as linhas do leitor.
- Loop infinito não trava a página: o Worker é reiniciado após o limite de tempo e o aviso explica que o estado foi perdido.
- Primeira carga do Pyodide mostra progresso; se falhar, mensagem honesta com como tentar de novo.
- Mapa: clicar leva ao capítulo, a parte atual fica destacada, capítulos concluídos marcados. Persistência só local (`localStorage` com try/catch).
- Dica e solução do exercício abrem sob demanda, em etapas.
- Movimento só onde explica (fluxo de dados, treino); `prefers-reduced-motion` desliga tudo isso.

## Responsive Behavior

Mobile primeiro (390px). Coluna de leitura única, mapa vira gaveta; editor de código com rolagem horizontal interna, sem rolagem horizontal da página. Alvos de toque de 44px. Em telas largas, coluna de leitura de 68 a 74 caracteres com margem para notas. Verificar 390, 768, 1024 e 1440.

## Accessibility Requirements

Contraste 4,5:1 (3:1 para elementos de interface) em claro e escuro, inclusive nas cores do mapa. Foco visível sempre. Todo exercício e demo operável por teclado. Cor nunca é o único sinal (ícone e texto no resultado e no mapa). Texto alternativo nas figuras. Anúncio do resultado do teste em região `aria-live`. Fontes do corpo a partir de 16px.

## Out of Scope

- Qualquer mudança em `estudo.css` ou nas outras 11 apostilas.
- Conteúdo dos capítulos (cada um tem o seu escritor e revisão).
- Conta de usuário, servidor, ranking, banco de dados. Tudo estático.
- Ligar o GitHub Pages (só com ok do dono, ao fim).
- Instalar skills de terceiros.
- Dependência de CDN para Python ou editor: Pyodide e editor são servidos localmente, com versão e origem conferidas em fonte oficial antes de usar.
