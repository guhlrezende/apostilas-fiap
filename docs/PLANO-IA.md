# Plano: apostila "Inteligência Artificial" (trilha completa)

Decidido em 13/11/2026, ampliado no mesmo dia depois de levantar currículos de referência (`docs/referencias/curriculos-ia.md`) e os livros (`docs/referencias/livros-ia.md`). Pasta `inteligencia-artificial/`, geradores `scripts/construtor/ia*.py`, entrada em `data/apostilas.js`.

**Público:** amigos que sabem Python básico. Interativa, com exercícios.
**Identidade visual própria**, diferente do caderno das outras apostilas. Direção a decidir pelo fluxo `design-flow` (propor 2 ou 3 e o dono escolhe). Assets em `inteligencia-artificial/assets/`, sem mexer em `assets/estudo.css` das outras.
**Exercícios:** código Python que roda no navegador (Pyodide), com teste automático. Conferir versão e origem do Pyodide antes de usar. Complementar com quizzes e lacunas, laboratório de prompt com respostas simuladas e marcadas como tal, e um projeto por parte.
**Princípio:** a trilha NÃO repete nem indica o que as outras apostilas cobrem (Machine Learning, Redes Neurais e Deep Learning, Estatística, Python, Cloud...). Sem "veja a apostila X".
Fora por já existir: KNN, regressão linear, treino/teste, validação cruzada, GridSearch, scalers, OneHot, vazamento e Pipeline; perceptron, MLP, deep learning, algoritmos genéticos; estatística descritiva e inferência.
**Livros** (pasta local, com direitos autorais): só roteiro e conferência. Texto e código nossos, rodados. "Para ir além" só com título e autor.

## Capítulos (20, em 5 partes)

| # | Título | Conteúdo |
|---|---|---|
| | **Parte 1: entender** | |
| 1 | O mapa da IA | IA simbólica x aprender com exemplos, linha do tempo verificada, generativa, agentes, panorama das áreas (visão, recomendação, séries, reforço, anomalias), o que ela faz bem e mal |
| | **Parte 2: dados e modelos clássicos** | |
| 2 | Dados reais | limpeza (datas, texto, codificação), ausentes, engenharia de atributos |
| 3 | Classificação e métricas | regressão logística, Naive Bayes, matriz de confusão, precisão, recall, F1, ROC, limiar |
| 4 | Árvores, florestas e boosting | impureza, bagging, boosting (XGBoost), quando usar cada um |
| 5 | Desbalanceamento e explicabilidade | classe rara, pesos, reamostrar do jeito certo, importância por permutação, dependência parcial |
| 6 | Sem rótulo | k-means, PCA, detecção de anomalias |
| | **Parte 3: como os LLMs funcionam** | |
| 7 | Tokens e embeddings | BPE, contar tokens, similaridade, busca semântica |
| 8 | Atenção e Transformer | atenção à mão em NumPy, Transformer completo |
| 9 | Treinar e ajustar um LLM | pré-treino por próximo token, SFT, LoRA, RLHF e DPO, temperatura, top-p, janela de contexto, quantização |
| 10 | Alucinação, avaliação e limites | por que erra com segurança, benchmarks e contaminação, modelos de raciocínio, custo e energia |
| | **Parte 4: usar IA na prática** | |
| 11 | Engenharia de prompt e contexto | instrução, contexto, exemplos, formato de saída, o que perdeu utilidade |
| 12 | Avaliar prompts | conjunto fixo de casos, métricas verificáveis, evals offline |
| 13 | RAG | chunking, embeddings, busca híbrida, reranker, citação, Recall@k e MRR |
| 14 | Agentes, ferramentas e MCP | workflow x agente, quando não usar, padrões, permissões |
| 15 | Segurança de LLM | OWASP Top 10, injeção de prompt, menor privilégio, humano no laço |
| 16 | IA para quem programa | o que faz e não faz, revisar código gerado, segurança, testes |
| 17 | Segundo cérebro com Claude Code e Obsidian | material próprio + prompt copiável |
| | **Parte 5: responsabilidade** | |
| 18 | Viés, justiça e privacidade | COMPAS, Gender Shades, métricas de justiça incompatíveis, LGPD |
| 19 | Regulação e uso responsável | AI Act, PL 2338, direito autoral, impacto no trabalho, carbono |
| 20 | Projeto final | auditoria de viés com model card |

Ordem: sequencial, um capítulo por vez (cada um termina com a ponte para o próximo). Publicar por capítulo (uma linha em `CAPS` de `ia_base.py`).

## Regras específicas
- Cap. 17: sem nome do colega, sem nome do vault pessoal. Comandos de instalação e requisitos só com fonte oficial lida e data (a apresentação trazia conferência de 05/11/2026; reconferir).
- Fatos de produto, modelo, lei e preço: só de página oficial lida, com data. O que for marcado [não confirmado] em `curriculos-ia.md` precisa ser conferido antes de entrar.
- Código: rodar e colar a saída real. Número do texto igual ao da demo. Experimentos sem GPU e sem chave de API.
- Regras gerais do repo (sem travessão, fio condutor `recap/gancho/ponte`, 5 camadas por conceito, público: sem dados pessoais).
- Skills de terceiros do GitHub: só depois do ok do dono, com leitura prévia do SKILL.md, licença e tamanho. Nada instalado até agora.

## Ordem e custo
Um escritor `sonnet` por capítulo e `refutador` na revisão. Nota de uso: 240 a 490 mil tokens por escritor; 20 capítulos são vários milhões de tokens, então vai ser em vários dias. Medir o gasto real do cap. 1 e registrar no Registro de uso de tokens do Vault.
Depois da IA, voltar à fila de `PROXIMOS-PASSOS.md`. Ligar o GitHub Pages ao fim, com ok do dono.

## Andamento
- [x] Leitura dos livros e dos currículos de referência (13/11)
- [x] Identidade visual própria (Laboratório), casca, mapa da trilha, fontes locais (13/11)
- [x] Motor de exercícios com Pyodide 314.0.7 local, pacotes por exercício (pandas 3.0.2 local), script `scripts/rodar_pyodide.mjs` (13/11)
- [x] Quiz, lacunas e glossário em tooltip (13/11)
- [x] Hub da apostila e entrada no site (13/11)
- [x] Cap. 1 publicado (13/11) e Cap. 2 publicado (13/11), no GitHub Pages
- [x] scikit-learn local (1.8.0 + SciPy, joblib, threadpoolctl; hash conferido) e Cap. 3 escrito, revisado e verificado (15/11), ainda não publicado; Worker pré-importa pacotes pesados\n- [x] Cap. 4 escrito, revisado e verificado (15/11), ainda não publicado\n- [ ] Cap. 5 em diante
- [ ] Componentes restantes: arrastar e soltar, "ache o erro", laboratório de prompt
- [ ] Passes de acessibilidade e responsivo, e design review
- [ ] Data do lançamento público do ChatGPT (sem fonte aberta lida)
Nota: os geradores `scripts/construtor/ia*.py` citados no início são da identidade antiga e não são usados. Os capítulos são HTML escritos sobre `modelo.html`.


