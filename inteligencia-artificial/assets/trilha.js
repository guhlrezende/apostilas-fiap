/* Dados da trilha: 5 partes, 20 capítulos (docs/PLANO-IA.md).
   Para publicar um capítulo: preencha "file" com o nome do .html dele. Sem "file" ele aparece como "em breve". */
window.IA_TRILHA = {
  partes: [
    { n: 1, nome: "Entender", caps: [1] },
    { n: 2, nome: "Dados e modelos clássicos", caps: [2, 3, 4, 5, 6] },
    { n: 3, nome: "Como os LLMs funcionam", caps: [7, 8, 9, 10] },
    { n: 4, nome: "Usar IA na prática", caps: [11, 12, 13, 14, 15, 16, 17] },
    { n: 5, nome: "Responsabilidade", caps: [18, 19, 20] }
  ],
  caps: [
    { n: 1, titulo: "O mapa da IA", file: "cap-1-o-mapa-da-ia.html" },
    { n: 2, titulo: "Dados reais", file: "cap-2-dados-reais.html" },
    { n: 3, titulo: "Classificação e métricas", file: null },
    { n: 4, titulo: "Árvores, florestas e boosting", file: null },
    { n: 5, titulo: "Desbalanceamento e explicabilidade", file: null },
    { n: 6, titulo: "Sem rótulo", file: null },
    { n: 7, titulo: "Tokens e embeddings", file: null },
    { n: 8, titulo: "Atenção e Transformer", file: null },
    { n: 9, titulo: "Treinar e ajustar um LLM", file: null },
    { n: 10, titulo: "Alucinação, avaliação e limites", file: null },
    { n: 11, titulo: "Engenharia de prompt e contexto", file: null },
    { n: 12, titulo: "Avaliar prompts", file: null },
    { n: 13, titulo: "RAG", file: null },
    { n: 14, titulo: "Agentes, ferramentas e MCP", file: null },
    { n: 15, titulo: "Segurança de LLM", file: null },
    { n: 16, titulo: "IA para quem programa", file: null },
    { n: 17, titulo: "Segundo cérebro com Claude Code e Obsidian", file: null },
    { n: 18, titulo: "Viés, justiça e privacidade", file: null },
    { n: 19, titulo: "Regulação e uso responsável", file: null },
    { n: 20, titulo: "Projeto final", file: null }
  ]
};
