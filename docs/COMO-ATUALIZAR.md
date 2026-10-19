# Rotina de domingo: como atualizar as apostilas

Todo domingo entram os capítulos das aulas da semana. O processo é sempre o mesmo, e cada passo termina com algo que dá para conferir.

## 1. Juntar o material (10 min)

Reúna o que saiu das aulas: anotações, slides, notebooks, planilhas. Decida **capítulo novo** ou **ampliar um capítulo existente**. Regra prática: se o assunto responde a uma pergunta que o último capítulo deixou aberta, é capítulo novo; se aprofunda algo que já existe, entra no capítulo atual.

## 2. Escrever o capítulo (o grosso do tempo)

1. Copie `template/capitulo-modelo.html` para `<apostila>/cap-N-nome.html`.
2. Preencha na ordem: **recap** (onde paramos), **seções**, **fechamento**. Cada seção tem um *gancho* no começo e uma *ponte* no fim.
3. Para cada conceito importante, escreva as cinco camadas: **intuição**, **definição precisa**, **exemplo resolvido com número**, **código comentado** (quando houver) e **erro comum**.
4. Adicione ao fim: cola da prova, 3 ou 4 testes rápidos (com explicação da resposta) e 4 flashcards.
5. Registre o capítulo em `<apostila>/capitulos.js`.

Se precisar de demos novas, crie `<apostila>/demos/cap-N.js`. Use dados reais quando possível (para ML, `python scripts/gerar_dados_ml.py` regenera `ml-data.js`).

## 3. Conferir (5 min)

```bash
python scripts/checar.py      # links, demos registradas, sintaxe dos scripts, dados pessoais
python scripts/serve.py       # abre em http://localhost:4323
```

Na página, confira: o console sem erro; cada demo responde; tema claro e escuro; largura de celular (sem rolagem horizontal); e **todo número do texto bate com o que a demo mostra**.

## 4. Regras de conteúdo

- **Sem dados pessoais.** Nada de nome completo, RM ou e-mail. O `checar.py` barra alguns padrões, mas a leitura final é sua.
- **Sem solução de trabalho aberto.** Resultado de checkpoint ou challenge só entra depois do prazo de entrega.
- **Nada copiado dos slides.** Explique com as suas palavras e, quando um dado vier do material da aula, diga que veio.
- **Marque o que é complemento.** O que não foi dado em aula entra como "complemento".
- **Sem travessão no texto** (use vírgula, ponto, dois-pontos ou parênteses).

## 5. Subir

```bash
git add -A
git commit -m "ML: capítulo N sobre <assunto>"
git push
```

Se o GitHub Pages estiver ativo, o site atualiza sozinho em alguns minutos.
