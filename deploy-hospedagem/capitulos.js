/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */
window.APOSTILA = {
  "id": "deploy-hospedagem",
  "titulo": "Deploy e Hospedagem",
  "caps": [
    {
      "n": 1,
      "file": "cap-1-como-a-web-funciona.html",
      "titulo": "Como a web funciona: cliente, servidor, HTTP, IP e portas",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Quem pede e quem responde, a conversa em HTTP (métodos, cabeçalhos e códigos de status), e o papel do IP e das portas, com um simulador de requisição.",
      "pergunta": "Entendo o pedido e a resposta. Mas o navegador só sabe o nome do site: como ele descobre o endereço do servidor?"
    },
    {
      "n": 2,
      "file": "cap-2-dns-e-dominio.html",
      "titulo": "DNS e domínio: uma consulta passo a passo",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Domínio, subdomínio e registros (A, AAAA, CNAME, MX, TXT, NS), a cadeia resolvedor, raiz, TLD e autoritativo, cache e TTL, com um simulador.",
      "pergunta": "O nome virou um IP. Como eu sei que estou falando com o servidor certo, e que ninguém lê a conversa no meio do caminho?"
    },
    {
      "n": 3,
      "file": "cap-3-https-tls-certificado.html",
      "titulo": "HTTPS, TLS e certificado",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "O que o TLS garante, o que o navegador confere num certificado, a cadeia de autoridades e o que o cadeado não promete, com erros reais de certificado.",
      "pergunta": "A conexão é segura. Mas onde o meu site vai morar? Qual a diferença entre um servidor estático, um PaaS, um VPS e uma função serverless?"
    },
    {
      "n": 4,
      "file": "cap-4-tipos-de-hospedagem.html",
      "titulo": "Tipos de hospedagem e quando usar cada um",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Estático, PaaS, container, VPS e serverless, mais IaaS, PaaS e SaaS, com uma árvore de decisão que recomenda e justifica.",
      "pergunta": "Já sei onde posso hospedar. Como eu faço o site chegar lá, de fato?"
    },
    {
      "n": 5,
      "file": "cap-5-publicar-site-estatico.html",
      "titulo": "Publicar um site estático por três caminhos",
      "aula": "Complemento",
      "tempo": 50,
      "resumo": "GitHub Pages, uma plataforma de deploy (Cloudflare Pages, Netlify ou Vercel) e um VPS com nginx, SSH e scp/rsync, com os comandos e o aviso do que não foi testado.",
      "pergunta": "Consigo publicar à mão. E se eu quiser que cada push publique sozinho, sem vazar a senha da plataforma?"
    },
    {
      "n": 6,
      "file": "cap-6-ci-cd-segredos.html",
      "titulo": "CI/CD, DevOps básico e segredos",
      "aula": "Complemento",
      "tempo": 45,
      "resumo": "Integração, entrega e implantação contínuas, variáveis de ambiente, .env, .gitignore e o que fazer quando um segredo vaza, com uma esteira simulada.",
      "pergunta": "O site está no ar e publica sozinho. O que eu olho depois, e como volto atrás se algo quebrar?"
    },
    {
      "n": 7,
      "file": "cap-7-depois-que-subiu.html",
      "titulo": "Depois que subiu: monitorar, logs, rollback, custo e checklist",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "Monitoramento e observabilidade, ler um log de acesso, rollback com git revert, cuidado com custo e um checklist de lançamento.",
      "pergunta": ""
    }
  ]
};
