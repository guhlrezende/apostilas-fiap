# Apostilas de estudo

Apostilas interativas feitas a partir das aulas da faculdade. Cada aula vira um capítulo que explica o **porquê**, deixa você **mexer nos números** e termina com perguntas para se testar. O caderno cresce todo domingo.

## O que tem aqui

| Apostila | Capítulos | Estado |
|---|---|---|
| [Machine Learning](machine-learning/index.html) | 6 | publicada: mapa da IA, treino e teste, KNN, métricas, validação cruzada, scalers, vazamento de dados, regressão linear e o roteiro de um projeto |
| Banco de dados com MySQL | | será refeita neste mesmo estilo |

## Como cada capítulo é montado

- **Fio condutor:** cada capítulo abre com a pergunta que sobrou do anterior e termina com a pergunta que leva ao próximo.
- **Explicação em camadas:** intuição, definição, exemplo resolvido com número, código comentado e o erro comum.
- **Demos com dados reais:** gráficos interativos em cima do Iris e do Insurance, e vários resultados vêm direto do scikit-learn.
- **Para se testar:** quizzes com a resposta explicada, flashcards e uma "cola da prova".
- O progresso (capítulos lidos e checklists) fica salvo no navegador. Tema claro e escuro, e funciona no celular.

## Ver no computador

Não precisa instalar nada: abra `index.html` no navegador. Para ver com um servidor local (sem cache):

```bash
python scripts/serve.py
```

e acesse <http://localhost:4323>.

## Estrutura

```
index.html                 página inicial
assets/                    estudo.css e estudo.js (design system e componentes, compartilhados)
data/apostilas.js          lista de apostilas da página inicial
machine-learning/          uma pasta por apostila
  capitulos.js             lista de capítulos (navegação e progresso)
  cap-N-*.html             um arquivo por capítulo
  demos/cap-N.js           demos de cada capítulo
  ml-data.js, ml-core.js   dados reais e funções de apoio
template/                  modelo de capítulo
scripts/                   serve.py, checar.py, gerar_dados_ml.py
docs/COMO-ATUALIZAR.md     a rotina de domingo
```

## Atualizar toda semana

Veja [docs/COMO-ATUALIZAR.md](docs/COMO-ATUALIZAR.md). Antes de subir, rode `python scripts/checar.py`.

## Sobre o conteúdo

Material de estudo pessoal, escrito a partir das anotações de aula e sem cópia dos slides. Onde um número vem do material da aula ou do scikit-learn, o texto diz. O que é complemento (não foi dado em aula) vem marcado.
