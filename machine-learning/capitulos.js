/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps (com file). */
window.APOSTILA = {
  id: "machine-learning",
  titulo: "Machine Learning",
  caps: [
    { n: 1, file: "cap-1-mapa.html", titulo: "O mapa do território", aula: "Aula 1", tempo: 25,
      resumo: "O que é ML, onde ele mora dentro da IA, os três jeitos de aprender e o ciclo de um projeto.",
      pergunta: "Se o computador aprende com exemplos, como eu sei que ele aprendeu de verdade e não só decorou?" },
    { n: 2, file: "cap-2-aprender-nao-e-decorar.html", titulo: "Aprender não é decorar", aula: "Aula 2", tempo: 35,
      resumo: "Treino e teste, generalização e o seu primeiro modelo: KNN classificando flores.",
      pergunta: "E se eu não quiser prever uma classe, e sim um número, como o custo de um seguro?" },
    { n: 3, file: "cap-3-knn-para-numeros.html", titulo: "KNN para números", aula: "Aula 3", tempo: 50,
      resumo: "Média dos vizinhos, distância e escala, MAE, MSE, RMSE, R², o k certo, validação cruzada e GridSearchCV.",
      pergunta: "O KNN só mede distância entre números. E as colunas de texto? E a régua de cada coluna?" },
    { n: 4, file: "cap-4-preparar-os-dados.html", titulo: "Preparar os dados", aula: "Aula 7", tempo: 40,
      resumo: "OneHotEncoder, os três scalers, vazamento de dados e como o Pipeline protege você.",
      pergunta: "O KNN decide por vizinhança. Existe um modelo que aprende uma fórmula em vez de guardar os dados?" },
    { n: 5, file: "cap-5-regressao-linear.html", titulo: "A reta que melhor se ajusta", aula: "Aula 8", tempo: 45,
      resumo: "Intercepto, coeficiente, resíduos, mínimos quadrados, R² e quem pesa mais no custo.",
      pergunta: "Já tenho todas as peças. Como encaixá-las num projeto do começo ao fim, sem trapacear?" },
    { n: 6, file: "cap-6-o-metodo.html", titulo: "O método: juntando tudo", aula: "Integração", tempo: 30,
      resumo: "Um roteiro de nove passos para melhorar um modelo com honestidade, mais a trilha para ir além.",
      pergunta: "" }
  ]
};
