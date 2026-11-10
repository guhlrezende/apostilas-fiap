/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */
window.APOSTILA = {
  "id": "github-uso",
  "titulo": "GitHub: como usar do jeito certo",
  "caps": [
    {
      "n": 1,
      "file": "cap-1-git-github-conta.html",
      "titulo": "Git x GitHub, conta, 2FA e o seu e-mail",
      "aula": "Complemento",
      "tempo": 35,
      "resumo": "O que o GitHub acrescenta ao Git, como criar e proteger a conta (2FA, passkey, códigos de recuperação) e o que o e-mail dos seus commits mostra para o mundo.",
      "pergunta": "Tenho a conta protegida e a identidade certa nos commits. Onde meu projeto mora, e o que faz um repositório ser bem montado?"
    },
    {
      "n": 2,
      "file": "cap-2-repositorio.html",
      "titulo": "O repositório: visibilidade, README, licença e arquivos de saúde",
      "aula": "Complemento",
      "tempo": 45,
      "resumo": "Público x privado, README, LICENSE (sem aconselhamento jurídico), .gitignore, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY e templates, montados num repositório local.",
      "pergunta": "O repositório está montado no meu computador. Como o GitHub e o meu computador passam a conversar?"
    },
    {
      "n": 3,
      "file": "cap-3-remoto-e-autenticacao.html",
      "titulo": "Remoto, clone, fork, fetch, pull, push e autenticação",
      "aula": "Complemento",
      "tempo": 50,
      "resumo": "origin, main, clone x fork, upstream, a diferença entre fetch, pull e push (com divergência rodada de verdade) e as formas de se autenticar: token, SSH e gh, e o que nunca colar.",
      "pergunta": "Já consigo enviar código. Como planejo o trabalho e o registro de quem faz o quê?"
    },
    {
      "n": 4,
      "file": "cap-4-issues-e-projects.html",
      "titulo": "Issues, labels, milestones, referências e Projects",
      "aula": "Complemento",
      "tempo": 35,
      "resumo": "Issue como unidade de trabalho, labels e milestones, as referências #123 e Closes #123 (e a regra do branch padrão) e Projects.",
      "pergunta": "Tenho issues organizadas. Como transformo uma delas em código revisado e entregue?"
    },
    {
      "n": 5,
      "file": "cap-5-branch-pr-e-merge.html",
      "titulo": "Branches, GitHub Flow, pull request e tipos de merge",
      "aula": "Complemento",
      "tempo": 60,
      "resumo": "O fluxo completo de um PR (draft, descrição, revisão, checks, conflito), merge commit x squash x rebase com o grafo resultante e como desfazer um merge com revert -m 1.",
      "pergunta": "Sei levar uma mudança minha até a main. E num projeto que não é meu, onde eu nem tenho permissão de escrita?"
    },
    {
      "n": 6,
      "file": "cap-6-fork-e-contribuicao.html",
      "titulo": "Fork, upstream e contribuição em projeto de terceiros",
      "aula": "Complemento",
      "tempo": 45,
      "resumo": "Quando usar fork, como manter o fork em dia, a etiqueta de quem contribui e um diagrama interativo de origin, upstream e PR.",
      "pergunta": "Contribuo sem esbarrar nos outros. Em equipe, o que impede alguém de quebrar a main?"
    },
    {
      "n": 7,
      "file": "cap-7-proteger-a-main.html",
      "titulo": "Proteger a main: proteção de branch, rulesets e CODEOWNERS",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Por que não commitar direto na main em equipe, o que cada regra de proteção exige, rulesets, CODEOWNERS e uma demo que diz se um PR pode entrar.",
      "pergunta": "A main está protegida. E as tarefas repetitivas (testar, publicar, versionar), quem faz?"
    },
    {
      "n": 8,
      "file": "cap-8-actions-pages-releases.html",
      "titulo": "Actions, Pages, releases e versionamento",
      "aula": "Complemento",
      "tempo": 50,
      "resumo": "Workflow em YAML, gatilhos, secrets e permissões mínimas, o que o GITHUB_TOKEN não faz, Pages, tags e releases com versionamento semântico.",
      "pergunta": "Automatizei e publiquei. E se um segredo vazar, ou eu errar feio, como protejo e como me recupero?"
    },
    {
      "n": 9,
      "file": "cap-9-seguranca-gh-e-portfolio.html",
      "titulo": "Segurança, gh, recuperação de erros e portfólio",
      "aula": "Complemento",
      "tempo": 55,
      "resumo": "Secret scanning, push protection e Dependabot, a ordem certa quando um segredo vaza (com árvore de decisão), o gh no terminal, erros comuns com a saída real e como montar um perfil sem prometer emprego.",
      "pergunta": ""
    }
  ]
};
