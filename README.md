# Apostilas de estudo

Apostilas interativas feitas a partir das aulas da faculdade. Cada aula vira um capítulo que explica o **porquê**, deixa você **mexer nos números** e termina com perguntas para se testar. O caderno cresce todo domingo.

## O que tem aqui

| Apostila | Capítulos | Estado |
|---|---|---|
| [Machine Learning](machine-learning/index.html) | 6 | publicada: mapa da IA, treino e teste, KNN, métricas, validação cruzada, scalers, vazamento de dados, regressão linear e o roteiro de um projeto |
| [Bancos de Dados e SQL](banco-de-dados/index.html) | 8 | pronta localmente: modelagem, DDL, DML, agregações, JOINs, views e triggers, com SQL de verdade na página |
| [Python e Pensamento Computacional](python/index.html) | 9 | pronta localmente: variáveis até funções, Git e um algoritmo de jogo, com código rastreado |
| [Cibersegurança](ciberseguranca/index.html) | 6 | pronta localmente: OSI, IP, DNS, ataques, criptografia e defesa (o capítulo da Kill Chain entra depois de 26/10) |
| [Cloud e AWS](cloud-aws/index.html) | 7 | pronta localmente: modelos de nuvem, IAM, EC2, S3, RDS e Lambda, com custos e limites |
| [Redes Neurais e Deep Learning](redes-neurais/index.html) | 8 | pronta localmente: do neurônio ao MLP, com redes treinando no navegador, mais deep learning e algoritmos genéticos |
| [Estatística com R e Python](estatistica/index.html) | 6 | pronta localmente: pesquisa e amostra, variáveis, Python e R, descritiva e correlação (código em R não rodado aqui) |
| [Gestão Ágil e Pitch](gestao-agil/index.html) | 6 | pronta localmente: Scrum, user story, Kanban e WIP, pitch e UML |
| [Sistemas Embarcados com ESP32](embarcados/index.html) | 7 | pronta localmente: GPIO, LED, Serial, C++, botão e DHT22 (código C++ não compilado aqui) |
| [Ferramentas de AI Builder](ai-builder/index.html) | 9 | trilha própria (complemento): APIs, n8n, Make, Zapier, Docker, Cursor, v0, Bolt, Replit, API com FastAPI, análise de dados e portfólio |
| [Claude](claude/index.html) | 7 | trilha própria (complemento): modelos, app, prompt engineering, API, ferramentas e MCP, Claude Code com skills, subagentes e hooks |

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
machine-learning/          uma pasta por apostila (as outras seguem o mesmo molde)
  capitulos.js             lista de capítulos (navegação e progresso)
  cap-N-*.html             um arquivo por capítulo
  demos/cap-N.js           demos de cada capítulo
  ml-data.js, ml-core.js   dados reais e funções de apoio
template/                  modelo de capítulo
scripts/                   serve.py, checar.py, gerar_dados_ml.py, trace_python.py, construtor/
docs/COMO-ATUALIZAR.md     a rotina de domingo
```

## Atualizar toda semana

Veja [docs/COMO-ATUALIZAR.md](docs/COMO-ATUALIZAR.md). Antes de subir, rode `python scripts/checar.py`.

## Sobre o conteúdo

Material de estudo pessoal, escrito a partir das anotações de aula e sem cópia dos slides. Onde um número vem do material da aula ou do scikit-learn, o texto diz. O que é complemento (não foi dado em aula) vem marcado.
