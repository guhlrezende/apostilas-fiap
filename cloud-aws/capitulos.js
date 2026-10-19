/* Manifesto da apostila. Para publicar um capítulo novo: adicione uma linha em caps. */
window.APOSTILA = {
  "id": "cloud-aws",
  "titulo": "Cloud e AWS",
  "caps": [
    {
      "n": 1,
      "file": "cap-1-o-que-e-nuvem.html",
      "titulo": "O que é nuvem",
      "aula": "Aula 1",
      "tempo": 35,
      "resumo": "IaaS, PaaS e SaaS, modelos de infraestrutura, TCO, regiões e zonas de disponibilidade e formas de cobrança.",
      "pergunta": "Colocar coisas na nuvem é fácil. Como saber quem pode mexer, e de quem é a responsabilidade de proteger?"
    },
    {
      "n": 2,
      "file": "cap-2-seguranca-e-iam.html",
      "titulo": "Segurança e IAM",
      "aula": "Aula 2",
      "tempo": 40,
      "resumo": "Responsabilidade compartilhada, usuários, grupos, políticas e roles, e o Deny que sempre vence.",
      "pergunta": "Já sei quem pode o quê. Como crio de fato uma máquina e a conecto?"
    },
    {
      "n": 3,
      "file": "cap-3-ec2.html",
      "titulo": "EC2: máquinas virtuais",
      "aula": "Aula 3",
      "tempo": 40,
      "resumo": "Instâncias, AMI, tipos, os três IPs, EBS e o passo a passo de subir um site com Apache.",
      "pergunta": "Uma máquina ligada o dia inteiro só para servir um HTML. Dá para pagar menos?"
    },
    {
      "n": 4,
      "file": "cap-4-s3.html",
      "titulo": "S3: arquivos sem servidor",
      "aula": "Aula 4",
      "tempo": 40,
      "resumo": "Buckets e objetos, site estático sem máquina virtual, as duas camadas de acesso e EBS x EFS x S3.",
      "pergunta": "Guardo arquivos sem servidor. E o banco de dados, precisa mesmo de uma máquina?"
    },
    {
      "n": 5,
      "file": "cap-5-rds.html",
      "titulo": "RDS: banco gerenciado",
      "aula": "Aula 5",
      "tempo": 40,
      "resumo": "MySQL na nuvem sem administrar servidor, endpoint, Security Group e o risco de abrir a porta ao mundo.",
      "pergunta": "Tenho arquivos no S3 e um banco no RDS. Quem leva os dados de um para o outro?"
    },
    {
      "n": 6,
      "file": "cap-6-lambda.html",
      "titulo": "Lambda: código sob demanda",
      "aula": "Aula 6",
      "tempo": 45,
      "resumo": "Funções serverless, limites, e o fluxo completo CSV no S3, Lambda e inserção no RDS.",
      "pergunta": "Os serviços funcionam juntos. Como eles se conectam por baixo, e como não gastar o que não devo?"
    },
    {
      "n": 7,
      "file": "cap-7-rede-e-boas-praticas.html",
      "titulo": "Rede, custos e boas práticas (complemento)",
      "aula": "Complemento",
      "tempo": 40,
      "resumo": "VPC, sub-redes, Security Group x NACL, os pilares de uma boa arquitetura, CLI e boto3, e como evitar custo surpresa.",
      "pergunta": ""
    }
  ]
};
