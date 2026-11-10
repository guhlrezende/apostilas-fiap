# Temas visuais das apostilas

O caderno (papel, margem, anotação manuscrita, recap, gancho e ponte) é o fio comum. Cada apostila veste um tema por cima: paleta, fonte do título, motivo gráfico no `.capa`, detalhes de `.card` e `.chip`. O hub raiz usa o caderno padrão, sem tema.

## Arquivos

- `assets/temas.css`: tokens e decoração de todos os temas. Carrega depois de `estudo.css`.
- `scripts/construtor/temas.py`: dicionário `TEMAS` (nome, cor do papel, fonte, emoji), `tema_attr(pasta)`, `fontes_link(pasta)` e `fontes_link_todas()` (para o hub raiz).
- `scripts/contraste_temas.py`: confere o contraste WCAG de todos os temas, claro e escuro.

## Como a integração funciona

1. O id do tema é o nome da pasta da apostila (`terminal-git`, `python`, ...).
2. O gerador escreve `data-tema="<id>"` no `<html>` (`tema_attr(pasta)`), logo depois do `lang`.
3. O `<head>` ganha a fonte do título (`fontes_link(pasta)`) e `<link rel="stylesheet" href="../assets/temas.css">` depois do `estudo.css`.
4. No hub raiz, cada `.cap-card` de apostila recebe `data-tema="<id>"` (o `estudo.js` já tem o `a.id`), e o `<head>` do `index.html` carrega `fontes_link_todas()` e o `temas.css`.

O tema só sobrescreve tokens e acrescenta decoração. Nenhum componente do `estudo.css` é copiado.

## Adicionar um tema novo

1. Crie as 3 partes em `assets/temas.css`, copiando um tema existente:
   - `:root[data-tema="ID"]{...}` (claro);
   - `@media (prefers-color-scheme:dark){ :root[data-tema="ID"]:not([data-theme="light"]){...} }` e `:root[data-tema="ID"][data-theme="dark"]{...}` (escuro, os dois blocos idênticos);
   - `[data-tema="ID"]{--f-head:...;--m-bg:...;--m-mask:...;--kick:"..."}` (fonte, motivo do `.capa` e prefixo do kicker);
   - os 3 blocos do cartão do hub (`--ta`, `--tb`, `--deco`, claro e escuro).
2. Tokens obrigatórios nos blocos de cor: `paper paper-2 card ink muted rule margin line pen pen-soft red red-soft green green-soft amber amber-soft c0 c1 c2 desk deco`. Todo token do bloco claro precisa existir também no escuro, senão o valor claro vaza (o bloco do tema vem depois do `estudo.css` e tem a mesma especificidade).
3. `--deco` é a cor do motivo. A decoração usa `var(--dc)` (14% de `--deco`); nunca passe de 14% nem empilhe mais de duas camadas.
4. Sem cor fixa em componente: use tokens. Animação só com `transform` e `opacity`, e desligada em `prefers-reduced-motion`.
5. Fonte: no máximo 1 família nova de título, com variante latina completa (acentos do português), confirmada no Google Fonts. O corpo continua Inter e o mono JetBrains Mono.
6. Registre o tema em `TEMAS` (`temas.py`): `cor_tema_claro` e `cor_tema_escuro` são o `--paper` de cada modo.

## Regra de contraste

Mínimo de 4.5:1 em todos os pares, nos dois modos: `ink` sobre `paper`, `paper-2`, `card`, `desk` e os fundos `-soft`; `muted` sobre `paper`, `paper-2`, `card`, `desk` e `pen-soft`; `pen` sobre `paper`, `card`, `desk` e `pen-soft`; `red`, `green` e `amber` sobre o respectivo `-soft`; o texto do chip; o papel sobre `pen`, `green` e `c1` (texto dentro de botão e numeração); e kicker, título e subtítulo sobre o papel misturado com a decoração.

```
python scripts/contraste_temas.py          # resumo com o pior par de cada tema
python scripts/contraste_temas.py --tudo   # todos os pares
```

Sai com erro se algum par ficar abaixo de 4.5:1, se faltar bloco escuro, se os dois blocos escuros divergirem, se um token claro não tiver par no escuro ou se `temas.py` não bater com o CSS (ids, cor do papel, fonte). Corrija a paleta, não o critério.

## Conferir no navegador

Abra uma página com `data-tema` em 390px e 1200px, nos dois modos, e confira que não há rolagem horizontal e que o console está limpo. Com `prefers-reduced-motion` ligado, cursor e radar do tema ficam parados.
