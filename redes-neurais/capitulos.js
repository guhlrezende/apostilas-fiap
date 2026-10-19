/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */
window.APOSTILA = {
  "id": "redes-neurais",
  "titulo": "Redes Neurais e Deep Learning",
  "caps": [
    {
      "n": 1,
      "file": "cap-1-do-neuronio-a-rede.html",
      "titulo": "Do neurônio à rede",
      "aula": "Aula 2",
      "tempo": 35,
      "resumo": "Entradas, pesos, bias, funções de ativação e como neurônios formam camadas.",
      "pergunta": "A rede está montada. Mas como ela descobre os pesos certos, e como errar sem perceber?"
    },
    {
      "n": 2,
      "file": "cap-2-aprender-e-errar.html",
      "titulo": "Como a rede aprende (e erra)",
      "aula": "Aula 2",
      "tempo": 45,
      "resumo": "Previsão, erro, gradiente e taxa de aprendizado; overfitting, viés de confundimento e como salvar o modelo.",
      "pergunta": "Para entender de verdade, vamos começar pelo menor modelo possível: um único neurônio que aprende."
    },
    {
      "n": 3,
      "file": "cap-3-perceptron.html",
      "titulo": "O Perceptron",
      "aula": "Aulas 3 e 4",
      "tempo": 45,
      "resumo": "O primeiro neurônio que aprende, a regra de atualização dos pesos e o limite do XOR.",
      "pergunta": "O Perceptron aprende. Mas para que serve o bias, e o que acontece numa decisão de negócio?"
    },
    {
      "n": 4,
      "file": "cap-4-treino-e-bias.html",
      "titulo": "Treinando à mão e o papel do bias",
      "aula": "Aulas 5 e 6",
      "tempo": 40,
      "resumo": "Uma época de treino passo a passo, o bias como nota de corte e o modelo aprendendo o bias sozinho.",
      "pergunta": "Um neurônio só resolve AND e OR. Como resolver o que ele não consegue?"
    },
    {
      "n": 5,
      "file": "cap-5-mlp.html",
      "titulo": "A MLP: camada oculta",
      "aula": "Aula 7",
      "tempo": 50,
      "resumo": "Prever o consumo de energia: uma reta falha, uma rede com camada oculta desenha o U. Mais o XOR resolvido.",
      "pergunta": "A rede funcionou. Mas o que acontece por dentro quando ela treina?"
    },
    {
      "n": 6,
      "file": "cap-6-por-dentro-do-treino.html",
      "titulo": "Por dentro do treino (complemento)",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Backpropagation com um exemplo numérico, funções de perda, épocas, otimizadores e como evitar overfitting.",
      "pergunta": "Uma camada oculta basta para tabelas. E para imagens, texto e voz?"
    },
    {
      "n": 7,
      "file": "cap-7-deep-learning.html",
      "titulo": "Deep Learning e arquiteturas (complemento)",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Convolução, RNN e LSTM, Transformers, transfer learning, frameworks e os riscos de levar um modelo a produção.",
      "pergunta": "Todas essas redes aprendem por gradiente. Existe um jeito de otimizar sem ele?"
    },
    {
      "n": 8,
      "file": "cap-8-algoritmos-geneticos.html",
      "titulo": "Algoritmos Genéticos (complemento)",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Seleção, cruzamento e mutação para otimizar sem gradiente, e onde isso é usado.",
      "pergunta": ""
    }
  ]
};
