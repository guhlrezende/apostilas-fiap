# Apostilas de estudo

Site estático (HTML, CSS e JS puro, sem build) com apostilas interativas das aulas da FIAP. Uma pasta por disciplina; cada capítulo é um `.html`.

## Comandos
- Ver: `python scripts/serve.py` (porta 4323, sem cache).
- Verificar antes de subir: `python scripts/checar.py` (links, demos registradas, sintaxe dos `.js`, dados pessoais, travessão).
- Regenerar dados de ML: `python scripts/gerar_dados_ml.py` (precisa de scikit-learn e internet).
- Rotina semanal: `docs/COMO-ATUALIZAR.md`. Modelo de capítulo: `template/capitulo-modelo.html`.

## Regras que não dá para deduzir do código
- **Repositório público.** Nunca coloque nome completo, RM, e-mail ou credenciais. Se precisar de nome, só o primeiro.
- **Nada de solução de trabalho com prazo aberto** (checkpoint, challenge). Só depois da entrega.
- **Não copie slides.** Explique com palavras próprias; marque o que é "complemento, não foi dado em aula".
- **Sem travessão no texto.** Português do Brasil, tom de estudante explicando, sem clichê de IA.
- **Todo número do texto tem de bater com a demo** (rode a demo e confira). Números de scikit-learn vêm de `gerar_dados_ml.py`, nunca à mão.
- **Fio condutor:** o capítulo abre com `.recap`; cada seção abre com `.gancho` e fecha com `.ponte`. Sem tópico solto.
- Cada conceito importante tem 5 camadas: intuição, definição, exemplo resolvido com número, código comentado, erro comum.

## Arquitetura
- `assets/estudo.js` monta a casca (topo, sidebar, progresso) a partir de `window.APOSTILA` (`<pasta>/capitulos.js`) e inicializa os componentes por classe. Demos são funções em `Estudo.demos.<nome>`, ligadas por `data-demo="<nome>"`; só rodam quando entram na tela.
- `assets/estudo.css` guarda todos os tokens de cor (claro e escuro). Não use cor fixa nos componentes.
- Demos com canvas usam `Estudo.canvas` (DPR, resize e tema) e `Estudo.pointer`.
- Capítulo novo = copiar o template + uma linha em `capitulos.js`. Apostila nova = pasta nova + entrada em `data/apostilas.js`.

## Pegadinhas
- O `IntersectionObserver` do painel de preview só dispara quando há quadro renderizado. Em teste automático, chame `Estudo.demos.x(el)` à mão se a demo não aparecer.
- Botão dentro de botão não funciona em HTML (o parser fecha o externo). Use `div role="button"`.
- Verificação visual: tela de celular (390px), tema escuro e console sem erro.
