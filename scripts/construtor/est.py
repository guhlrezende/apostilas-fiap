import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
from trace_python import trace_html

PASTA = "estatistica"
TITULO = "Estatística com R e Python"
T = TITULO
S = ["demos/est.js"]
CAPS = [
 dict(n=1, file="cap-1-o-mapa.html", titulo="Estatística: o mapa", aula="Aula 1", tempo=35,
      resumo="O que é estatística, de onde veio, a pirâmide DIKW, as etapas de um estudo e população x amostra.",
      pergunta="Todo estudo começa nos dados. De onde eles vêm, e como não estragar a base antes de analisar?"),
 dict(n=2, file="cap-2-pesquisa-e-amostra.html", titulo="Pesquisa, questionário e amostra", aula="Aula 2", tempo=45,
      resumo="As 11 etapas da pesquisa, método e técnica, o questionário bem montado, a LGPD e quantas pessoas entrevistar.",
      pergunta="Com a base coletada, o que dá para fazer com ela? Primeiro, entender o que cada coluna é."),
 dict(n=3, file="cap-3-variaveis-e-tabelas.html", titulo="Variáveis, tabelas e gráficos (complemento)", aula="Complemento", tempo=40,
      resumo="Tipos de variável, tabela de frequência, histograma, regra de Sturges e como escolher o gráfico.",
      pergunta="Para transformar a base em números e gráficos você precisa de uma ferramenta. Vamos a ela."),
 dict(n=4, file="cap-4-python-e-r.html", titulo="Python e R na prática", aula="Aulas 3 e 4", tempo=55,
      resumo="Lógica, ambientes, calculadora, decisões, laços, objetos, data frame e leitura de arquivos, lado a lado em Python e R.",
      pergunta="Com a base carregada, vem a pergunta central da estatística descritiva: como resumir tudo isso em poucos números?"),
 dict(n=5, file="cap-5-descritiva.html", titulo="Estatística descritiva (complemento)", aula="Complemento", tempo=50,
      resumo="Média, mediana, moda, variância, desvio, quartis, boxplot e outliers, com cálculo à mão e ao vivo.",
      pergunta="Resumir uma variável é o começo. O que muda quando há duas variáveis ao mesmo tempo?"),
 dict(n=6, file="cap-6-correlacao.html", titulo="Correlação e o que vem depois (complemento)", aula="Complemento", tempo=40,
      resumo="Correlação de Pearson, reta de regressão, R², o quarteto de Anscombe e o caminho até o machine learning.",
      pergunta=""),
]
manifest(PASTA, "estatistica", TITULO, CAPS)
hub(PASTA, TITULO, "Estatística com R e Python", "Apostila de Estatística com R e Python",
    "De como nasce uma base de dados até a reta de regressão, com R e Python lado a lado e demos de estatística ao vivo.",
    ["<b>6</b> capítulos", "<b>~4h30</b> de estudo ativo", "calculadoras e gráficos ao vivo"],
    '<p>Estatística é a arte de <mark class="hl">transformar dados em decisão sob incerteza</mark>. A apostila segue o caminho de um estudo de verdade: entender o mapa, planejar a pesquisa e a amostra, classificar as variáveis, carregar os dados em Python e R, resumi-los com medidas descritivas e, por fim, relacionar duas variáveis. Cada capítulo termina com a pergunta que o próximo responde. Os capítulos 3, 5 e 6 são complemento: o assunto é da ementa, mas as anotações de aula ainda não chegaram lá.</p>',
    'Os exemplos de Python foram executados e os números conferidos. Os exemplos de <b>R</b> foram escritos e conferidos contra a documentação, mas <b>não rodados</b> neste ambiente (sem R instalado). Dados de exemplo são fictícios.')

# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo: o mapa do território. Não pressupõe nada. Ao fim, você sabe o que é estatística, de onde ela veio, em que ordem se faz um estudo e a diferença entre população e amostra, vocabulário que os próximos capítulos usam o tempo todo.", "Ponto de partida") + '''
<section class="sec" id="o-que-e">
  <h2><span class="sn">1</span>O que é estatística</h2>
  <p class="gancho">Uma ferramenta de Estado que virou ferramenta de todo mundo.</p>
  <p>A palavra <b>estatística</b> vem do latim <i>statisticum</i>, ligada a "estadista": nasceu como instrumento do Estado para contar e registrar a população. Hoje é o ramo da ciência que desenvolve métodos para <b>coletar, organizar, analisar, interpretar e apresentar dados</b>, com três objetivos: <b>descrever</b> fenômenos, fazer <b>inferências</b> e apoiar <b>decisões em condições de incerteza</b>.</p>
  <p>A relação com a matemática é a de um ramo aplicado: a matemática é mais antiga e ampla (a palavra grega <i>máthema</i> é interpretada, no material da aula, como "decodificar" (em geral, o termo significa "aprendizado" ou "conhecimento")), e a estatística é a parte dela voltada a lidar com dados e incerteza.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Se nasceu para contar gente, como chegou a ser uma ciência?</div><p>Com uma enfermeira e um gráfico.</p></div>
</section>

<section class="sec" id="historia">
  <h2><span class="sn">2</span>Uma história curta</h2>
  <p class="gancho">Do censo à rosa de Nightingale.</p>
  <div class="tl rv">
    <div class="ev"><b>Antiguidade</b><span>Povos organizados em Estados (egípcios, babilônios, chineses, romanos...) faziam levantamentos censitários.</span></div>
    <div class="ev"><b>Séc. XVII</b><span>Pascal, Fermat e Huygens dão os primeiros passos da teoria da probabilidade.</span></div>
    <div class="ev"><b>1858</b><span>Florence Nightingale publica relatórios com gráficos e mostra que doença evitável matava mais soldados que ferimento em batalha.</span></div>
    <div class="ev"><b>Fim do séc. XIX</b><span>Galton, Edgeworth, Karl Pearson e Yule consolidam a estatística moderna.</span></div>
    <div class="ev"><b>2011 a 2016</b><span>A "Indústria 4.0" e a explosão de dados trazem a estatística para o centro de IA e ciência de dados.</span></div>
  </div>
  <p>O ponto da história de Nightingale é prático: o <b>gráfico bem escolhido convenceu quem decidia</b>, e a saúde militar mudou. Estatística, no fim, é a ponte entre números e ação.</p>
  <div class="nota lembra"><span class="lbl">Por que a agricultura aparece nessa história</span>A matemática primitiva se apoiou em <b>clima, agricultura, comércio e registro</b>: quem planta precisa de calendário, medida de terra e controle de estoque. Sociedades sedentárias tinham mais necessidade desse conhecimento do que as nômades.</div>
</section>

<section class="sec" id="dikw">
  <h2><span class="sn">3</span>Dado, informação, conhecimento, sabedoria</h2>
  <p class="gancho">Número solto não decide nada.</p>
  <p>A pirâmide <b>DIKW</b> mostra o que acontece quando se sobe de nível de abstração: <b>dado</b> (observação bruta) → <b>informação</b> (dado organizado e com contexto) → <b>conhecimento</b> (informação interpretada, com padrão ou relação) → <b>sabedoria</b> (conhecimento aplicado com julgamento, que diz o que fazer). Classifique:</p>
  <div class="card sorter rv" data-demo="sorter" data-opts="d:Dado|i:Informação|c:Conhecimento|s:Sabedoria">
    <div class="item" data-ans="d"><p><b>37,8</b></p><span class="why">Dado: uma observação bruta, sem contexto nenhum.</span></div>
    <div class="item" data-ans="i"><p>A temperatura média de hoje foi <b>37,8 °C</b>, a mais alta do mês.</p><span class="why">Informação: o dado ganhou unidade, data e comparação.</span></div>
    <div class="item" data-ans="c"><p>Nos dias acima de 37 °C, as vendas de ventilador <b>sobem</b> bastante.</p><span class="why">Conhecimento: uma relação entre duas coisas, extraída de várias informações.</span></div>
    <div class="item" data-ans="s"><p>Reforçar o estoque de ventiladores <b>antes</b> da próxima onda de calor prevista.</p><span class="why">Sabedoria: o conhecimento virou decisão, com julgamento sobre custo e risco.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
</section>

<section class="sec" id="etapas">
  <h2><span class="sn">4</span>As etapas de um estudo estatístico</h2>
  <p class="gancho">Uma ordem que se repete em quase todo projeto de dados.</p>
  <ol>
    <li><b>Identificar o problema e o objetivo.</b> Sem pergunta, qualquer número serve.</li>
    <li><b>Coletar e tratar os dados</b>, respeitando a <b>LGPD</b> (tema do Capítulo 2).</li>
    <li><b>Análise univariada</b>: estatística descritiva de cada variável sozinha (Capítulos 3 a 5).</li>
    <li><b>Estatística inferencial</b>: concluir sobre a população a partir da amostra.</li>
    <li><b>Análise bivariada</b>: correlação e associação entre duas variáveis (Capítulo 6).</li>
    <li><b>Análise multivariada</b>: predição, classificação e agrupamento (é onde entra o machine learning).</li>
  </ol>
  <p>A lista não é rígida: outras etapas podem entrar conforme a natureza do estudo. Quanto à origem dos dados, o <b>dado primário</b> é coletado por você para responder à sua pergunta, e o <b>dado secundário</b> já foi coletado por outros. No Brasil, o <b>IBGE</b> é a referência pública para dados secundários, tanto brutos quanto já tratados.</p>
</section>

<section class="sec" id="populacao">
  <h2><span class="sn">5</span>População, amostra, unidade e censo</h2>
  <p class="gancho">Quase nunca dá para perguntar a todo mundo.</p>
  <ul>
    <li><b>População</b>: o conjunto inteiro que interessa estudar (finito ou infinito).</li>
    <li><b>Amostra</b>: um subconjunto da população.</li>
    <li><b>Unidade estatística</b>: cada elemento individual (uma pessoa, uma peça, um dia).</li>
    <li><b>Censo</b>: quando o estudo abrange <b>todos</b> os elementos.</li>
  </ul>
  <p>Amostras são preferidas por razão de <b>custo e tempo</b>: ouvir todo mundo costuma ser caro e demorado. O preço é a incerteza, e a estatística inferencial existe para medi-la.</p>
  <div class="card sorter rv" data-demo="sorter" data-opts="pop:População|am:Amostra|cen:Censo">
    <div class="item" data-ans="pop"><p>Todos os 12 mil funcionários de uma empresa.</p><span class="why">É o conjunto inteiro de interesse: a população.</span></div>
    <div class="item" data-ans="am"><p>300 funcionários sorteados para responder a pesquisa de clima.</p><span class="why">Um subconjunto da população: amostra.</span></div>
    <div class="item" data-ans="cen"><p>O IBGE visitando todos os domicílios do país em um recenseamento.</p><span class="why">Abrange todos os elementos: censo.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
</section>

<section class="sec" id="ia">
  <h2><span class="sn">6</span>Estatística e inteligência artificial</h2>
  <p class="gancho">O alicerce que ninguém vê no produto final.</p>
  <p>O termo <i>Industrie 4.0</i> foi apresentado em 2011 na Feira de Hannover, e em 2016 ganhou destaque no Fórum Econômico Mundial, em Davos. O resultado foi um <b>aumento enorme no volume de dados</b>. Os "três Vs" do <b>Big Data</b> resumem o problema: <b>volume</b>, <b>variedade</b> e <b>velocidade</b>. <b>Ciência de dados</b> combina estatística, matemática e computação para extrair informação útil; <b>inteligência artificial</b> cria sistemas que aprendem padrões a partir de dados em vez de serem programados caso a caso.</p>
  <p>Em outras palavras, o machine learning que você vê em outras disciplinas é, em boa parte, <b>estatística aplicada em escala</b>. Entender população, amostra, variável e incerteza é o que separa usar uma biblioteca de entender o que ela devolve.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">7</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Estatística</b>: coletar, organizar, analisar, interpretar e apresentar dados para descrever, inferir e decidir sob incerteza.",
    "Nasceu do Estado (<i>statisticum</i>); a visualização de Nightingale (1858) é um marco de uso para decisão.",
    "<b>DIKW</b>: dado → informação → conhecimento → sabedoria, cada nível mais abstrato.",
    "<b>Etapas</b>: problema → coleta (LGPD) → univariada → inferência → bivariada → multivariada.",
    "<b>População</b> x <b>amostra</b> x <b>unidade</b> x <b>censo</b>. Dado <b>primário</b> (você coleta) x <b>secundário</b> (outros coletaram; IBGE)."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Qual das opções é um exemplo de dado secundário?", [("a","Respostas de um questionário que você mesmo aplicou."),("b","Uma tabela de população por município baixada do IBGE."),("c","Uma medição feita por você com um termômetro.")], "Secundário é o que já foi coletado por outra pessoa ou instituição.") + quiz(2, "a", "Por que quase sempre se usa amostra em vez de censo?", [("a","Por custo e tempo: coletar de todos costuma ser caro e demorado."),("b","Porque o censo é proibido."),("c","Porque a amostra é sempre mais precisa.")], "A amostra troca um pouco de precisão por economia, e a inferência mede essa troca.") + quiz(3, "c", "Qual é o nível mais alto da pirâmide DIKW?", [("a","Conhecimento."),("b","Informação."),("c","Sabedoria: conhecimento aplicado com julgamento.")], "Cada nível acrescenta contexto e abstração; no topo está o saber o que fazer.") + flash([
    ("O que é uma unidade estatística?", "Cada elemento individual da população (uma pessoa, uma peça, um dia)."),
    ("Dado primário x secundário?", "Primário: coletado por você para o seu estudo. Secundário: já coletado por outros."),
    ("O que são os três Vs do Big Data?", "Volume, variedade e velocidade."),
    ("Quais as etapas de um estudo estatístico?", "Problema, coleta, univariada, inferência, bivariada e multivariada.")]) + ponte("Todo estudo começa nos dados. De onde eles vêm, e como não estragar a base antes de analisar?", "Planejando a pesquisa, o questionário e a amostra.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "o-mapa", T, "Estatística: o mapa", "Capítulo 1 · Aula 1",
        "O que é estatística, de onde veio e como se organiza um estudo.",
        ["<b>~35 min</b>", "2 demos · 3 testes · 4 flashcards", "classifique dado, informação e amostra"], body1, scripts=S)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 você viu as etapas de um estudo, e a segunda é <b>coletar e tratar os dados</b>. Este capítulo é essa etapa: como planejar a pesquisa, escrever um questionário que não enviese as respostas, respeitar a LGPD e definir <b>quantas pessoas</b> entrevistar.") + '''
<section class="sec" id="etapas-pesquisa">
  <h2><span class="sn">1</span>Pesquisa é processo, não improviso</h2>
  <div class="nota lembra"><span class="lbl">O que é complemento neste capítulo</span>A fórmula do tamanho da amostra (e a correção para população finita), os detalhes da LGPD, a escala Likert (1932) e a conta do NPS vêm de pesquisa complementar, e não do slide da aula. O resto (etapas, método, técnica, questionário) é da aula.</div>
  <p class="gancho">Dado ruim na entrada, conclusão ruim na saída.</p>
  <p><b>Pesquisa</b> é um <b>processo sistemático de investigação</b>, feito de um conjunto de atividades organizadas, com a finalidade de descobrir, produzir ou ampliar conhecimento. As palavras importantes são <i>sistemático</i> e <i>organizado</i>. As <b>11 etapas</b> de uma pesquisa formam a espinha dorsal de qualquer trabalho:</p>
  <div class="tl rv">
    <div class="ev"><b>1 e 2</b><span>Objeto de estudo e problema de pesquisa</span></div>
    <div class="ev"><b>3 e 4</b><span>Hipótese e objetivo</span></div>
    <div class="ev"><b>5 e 6</b><span>Referencial teórico e tipo de pesquisa</span></div>
    <div class="ev"><b>7</b><span>Metodologia (método e técnicas)</span></div>
    <div class="ev"><b>8 a 10</b><span>Resultados, discussão e conclusões</span></div>
    <div class="ev"><b>11</b><span>Referências</span></div>
  </div>
  <p>Cada etapa alimenta a seguinte. Pular uma costuma gerar um projeto sem lastro metodológico.</p>
</section>

<section class="sec" id="metodo">
  <h2><span class="sn">2</span>Método x técnica, quantitativo x qualitativo</h2>
  <p class="gancho">A metodologia é onde você decide como vai coletar e analisar.</p>
  <ul>
    <li><b>Método</b>: a forma geral de organizar a investigação (quantitativo, qualitativo ou misto).</li>
    <li><b>Técnica</b>: o procedimento prático de coleta (observação, entrevista, questionário, pesquisa bibliográfica, experimento).</li>
  </ul>
  <div class="tablewrap"><table>
    <tr><th></th><th>Quantitativo</th><th>Qualitativo</th></tr>
    <tr><td><b>Foco</b></td><td>medir, comparar, testar hipóteses</td><td>compreender experiências, causas, valores</td></tr>
    <tr><td><b>Amostra</b></td><td>grande, aleatória, para representar a população</td><td>menor, escolhida por relevância</td></tr>
    <tr><td><b>Coleta</b></td><td>questionário, formulário, experimento</td><td>entrevistas, grupos focais, observação</td></tr>
    <tr><td><b>Análise</b></td><td>tabelas, gráficos, inferência estatística</td><td>análise de conteúdo ou de discurso</td></tr>
    <tr><td><b>Pesquisador</b></td><td>procura não interferir</td><td>participa da interpretação</td></tr>
  </table></div>
  <p>Vantagens do quantitativo: tempo de resposta mais rápido, objetividade, validade e confiabilidade, amostras aleatórias que o tornam representativo. Desvantagens: negligencia o contexto social e cultural, não capta emoção e sentimento, depende de variáveis que podem ser definidas de forma arbitrária. A tensão entre essas listas é o argumento clássico a favor do <b>método misto</b>.</p>
  <div class="nota lembra"><span class="lbl">Experimento x questionário</span>As duas técnicas quantitativas são o <b>experimento</b> (controla e manipula variáveis para verificar <b>causa e efeito</b>) e o <b>questionário</b> (<i>survey</i>: série ordenada de perguntas respondidas sem entrevistador). Só o experimento sustenta falar em <b>causalidade</b>; o questionário permite falar em <b>associação</b>. O Capítulo 6 volta a isso.</div>
</section>

<section class="sec" id="questionario">
  <h2><span class="sn">3</span>O questionário</h2>
  <p class="gancho">Tão longo quanto necessário, tão curto quanto possível.</p>
  <p><b>Ciclo de vida</b>: elaborar → <b>validar</b> (para corrigir e ajustar) → enviar → o participante preenche → devolução pelo mesmo meio → encerrado o prazo, o pesquisador <b>valida e organiza a base</b> para análise. Ferramentas comuns: Google Forms, Microsoft Forms, Qualtrics, SurveyMonkey.</p>
  <div class="grid2">
    <div class="card rv"><b>Vantagens</b><p>Rapidez, precisão e custo menor; alcance amplo e geograficamente diverso; anonimato; menos interferência do pesquisador; flexibilidade para o respondente; uniformidade (todos veem as mesmas perguntas na mesma ordem).</p></div>
    <div class="card rv"><b>Desvantagens</b><p>Baixa taxa de retorno; ninguém esclarece dúvida durante o preenchimento; risco de resposta superficial; falta de controle sobre quem responde e em que condições; não serve a quem não lê.</p></div>
  </div>
  <h3>A estrutura em três páginas</h3>
  <ol>
    <li><b>Apresentação e consentimento</b>: objetivo, importância, número de perguntas e tempo médio, segurança e anonimato, contato do responsável e o <b>termo de aceite</b> ("concordo / não concordo").</li>
    <li><b>Perguntas de perfil</b> (idade, escolaridade...): caracterizam os participantes e permitem comparar grupos.</li>
    <li><b>Perguntas de conteúdo</b>: o tema investigado.</li>
  </ol>
  <div class="nota cuidado"><span class="lbl">LGPD: o mínimo que você precisa saber</span>A Lei nº 13.709/2018 (sancionada em 14/08/2018, em vigor desde 18/09/2020) foi muito inspirada no GDPR europeu. Para pesquisa: o <b>consentimento</b> deve ser <b>livre, informado e inequívoco</b>, para uma finalidade determinada; evite caixas pré-marcadas; guarde como provar que o participante aceitou. Dados como saúde, religião, origem racial e opinião política são <b>dados pessoais sensíveis</b>, e pedem cuidado redobrado: só colete se o objetivo exigir.</div>
</section>

<section class="sec" id="perguntas">
  <h2><span class="sn">4</span>Tipos de pergunta</h2>
  <p class="gancho">O tipo de pergunta define o tipo de dado que você vai ter.</p>
  <ul>
    <li><b>Dicotômica</b>: duas opções ("gosto / não gosto").</li>
    <li><b>Múltipla escolha</b>: uma opção entre várias (normalmente até cinco, mais "outro").</li>
    <li><b>Escala Likert</b>: grau de concordância ou satisfação, de 5 ou 7 pontos (criada por Rensis Likert em 1932).</li>
    <li><b>Escala de classificação</b>: ordenar itens por importância.</li>
    <li><b>Escala numérica</b>: um valor, como o NPS (0 a 10).</li>
  </ul>
  <div class="card sorter rv" data-demo="sorter" data-opts="d:Dicotômica|m:Múltipla escolha|l:Likert|n:Numérica">
    <div class="item" data-ans="d"><p>"Você já comprou neste site? (sim / não)"</p><span class="why">Duas opções: dicotômica.</span></div>
    <div class="item" data-ans="l"><p>"O atendimento foi rápido": discordo totalmente ... concordo totalmente.</p><span class="why">Grau de concordância em 5 pontos: Likert.</span></div>
    <div class="item" data-ans="n"><p>"De 0 a 10, qual a chance de você recomendar a empresa?"</p><span class="why">Valor numérico: escala numérica (é a pergunta do NPS).</span></div>
    <div class="item" data-ans="m"><p>"Qual seu sabor favorito? Calabresa, mussarela, frango, portuguesa, outro."</p><span class="why">Uma escolha entre várias: múltipla escolha.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <div class="ex rv"><span class="t">Exemplo resolvido: calculando um NPS</span>
    <div class="l"><div>Em 100 respostas à pergunta de 0 a 10: <b>50</b> notas 9 ou 10 (<b>promotores</b>), <b>30</b> notas 7 ou 8 (<b>neutros</b>) e <b>20</b> notas de 0 a 6 (<b>detratores</b>).</div></div>
    <div class="l"><div><code>NPS = % promotores − % detratores = 50% − 20% = <b>30</b></code>. Os neutros não entram na conta, mas contam no total.</div></div>
  </div>
  <p>Boa prática na Likert: número <b>ímpar</b> de pontos quando se quer permitir posição neutra, rótulos simétricos nas extremidades e a mesma direção em todas as afirmações.</p>
</section>

<section class="sec" id="amostra">
  <h2><span class="sn">5</span>Quantas pessoas entrevistar?</h2>
  <p class="gancho">O tamanho da amostra é calculado, não chutado.</p>
  <p>Para populações grandes ou indefinidas, a fórmula clássica é <code>n = Z² · p · q / e²</code>, em que <b>Z</b> é o escore do nível de confiança (90% → 1,645; 95% → 1,96; 99% → 2,576), <b>p</b> é a proporção esperada do evento (use 0,5 se não souber, o cenário mais conservador), <b>q = 1 − p</b> e <b>e</b> é a margem de erro. Para população <b>finita</b> de tamanho N, corrige-se: <code>n ajustado = n / (1 + (n − 1)/N)</code>.</p>
  <div class="demo" data-demo="amostra"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: o 385 que aparece em todo lugar</span>
    <div class="l"><div>Confiança 95% (Z = 1,96), p = q = 0,5, margem de erro 5% (e = 0,05).</div></div>
    <div class="l"><div><code>n = 1,96² · 0,5 · 0,5 / 0,05² = 3,8416 · 0,25 / 0,0025 = <b>384,16</b></code>, que se arredonda <b>para cima</b>: <b>385</b> (as fontes às vezes dizem 384 ou 385).</div></div>
    <div class="l"><div>Com população finita de 1.000 pessoas: <code>384,16 / (1 + 383,16/1000) = 277,7</code> → <b>278</b>. Perceba como a população pequena exige menos.</div></div>
    <div class="l"><div>Com margem de 2,5% em vez de 5%, o n vai a <b>1.537</b>: <b>metade da margem, quatro vezes a amostra</b>.</div></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado</span>A fórmula supõe amostra <b>aleatória</b> da população. Se só quem tem tempo e interesse responde (autosseleção), o n pode ser enorme e a amostra ainda assim não representar ninguém. Tamanho não corrige viés de seleção.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">6</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Pesquisa</b> é processo sistemático; as 11 etapas vão de objeto e problema até referências.",
    "<b>Método</b> (quanti, quali, misto) x <b>técnica</b> (questionário, entrevista, experimento...). Só o <b>experimento</b> sustenta causalidade.",
    "<b>Questionário</b>: 3 páginas (consentimento, perfil, conteúdo), validado antes do envio; vantagens (custo, alcance, anonimato) e desvantagens (retorno baixo, resposta superficial).",
    "<b>LGPD</b> (Lei 13.709/2018): consentimento livre, informado e inequívoco; dados sensíveis pedem cuidado redobrado.",
    "<b>n = Z²·p·q/e²</b>: 95%, p = 0,5, e = 5% → 385. Metade da margem, quádruplo da amostra. Aleatoriedade vale mais que tamanho."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual técnica permite falar em causa e efeito, e não só em associação?", [("a","O questionário."),("b","A entrevista."),("c","O experimento, que controla e manipula variáveis.")], "Sem controle das variáveis não dá para separar causa de coincidência.") + quiz(2, "a", "Com confiança 95%, p = 0,5 e margem de 5%, qual a amostra mínima para uma população grande?", [("a","385 (384,16 arredondado para cima)."),("b","96."),("c","1.000.")], "1,96² × 0,25 / 0,05² = 384,16, arredondado para cima.") + quiz(3, "b", "O que acontece com o n se você reduzir a margem de erro de 5% para 2,5%?", [("a","Dobra."),("b","Quadruplica."),("c","Não muda.")], "A margem entra elevada ao quadrado no denominador: metade da margem, quatro vezes a amostra.") + flash([
    ("O que é consentimento na LGPD?", "Manifestação livre, informada e inequívoca do titular, para uma finalidade determinada."),
    ("O que são promotores e detratores no NPS?", "Promotores dão 9 ou 10, detratores dão de 0 a 6. NPS = % promotores − % detratores."),
    ("Por que usar p = 0,5 quando não se sabe a proporção?", "Porque é o cenário mais conservador: dá o maior n possível."),
    ("Método x técnica?", "Método é a forma geral de investigar. Técnica é o procedimento de coleta (questionário, entrevista...).")]) + ponte("Com a base coletada, o que dá para fazer com ela? Primeiro, entender o que cada coluna é.", "Classificando variáveis e montando tabelas de frequência.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "pesquisa-e-amostra", T, "Pesquisa, questionário e amostra", "Capítulo 2 · Aula 2",
        "Planejar a pesquisa, montar um bom questionário, respeitar a LGPD e calcular a amostra.",
        ["<b>~45 min</b>", "2 demos · 3 testes · 4 flashcards", "calculadora de tamanho de amostra"], body2, scripts=S)

# ---------------- CAP 3 ----------------
body3 = recap("A pesquisa do Capítulo 2 produz uma base: linhas com respondentes e colunas com respostas. Antes de calcular qualquer coisa, é preciso saber <b>que tipo de coluna</b> é cada uma, porque isso decide quais contas e gráficos fazem sentido. Este capítulo é um complemento: é a etapa descritiva da ementa, ainda sem anotação de aula.") + '''
<section class="sec" id="tipos">
  <h2><span class="sn">1</span>Tipos de variável</h2>
  <p class="gancho">Nem todo número é número.</p>
  <div class="tablewrap"><table>
    <tr><th>Tipo</th><th>Subtipo</th><th>Exemplo</th><th>O que dá para fazer</th></tr>
    <tr><td rowspan="2"><b>Qualitativa</b> (categorias)</td><td>nominal</td><td>cidade, time, cor</td><td>contar, moda</td></tr>
    <tr><td>ordinal</td><td>escolaridade, satisfação (Likert)</td><td>contar, moda, mediana (há ordem)</td></tr>
    <tr><td rowspan="2"><b>Quantitativa</b> (números)</td><td>discreta</td><td>nº de filhos, nº de compras</td><td>tudo acima, mais média e desvio</td></tr>
    <tr><td>contínua</td><td>idade, altura, salário</td><td>tudo acima, em qualquer precisão</td></tr>
  </table></div>
  <div class="card sorter rv" data-demo="sorter" data-opts="nom:Qualitativa nominal|ord:Qualitativa ordinal|dis:Quantitativa discreta|con:Quantitativa contínua">
    <div class="item" data-ans="nom"><p>Cidade de moradia do respondente.</p><span class="why">Categorias sem ordem: nominal.</span></div>
    <div class="item" data-ans="ord"><p>Nível de escolaridade (fundamental, médio, superior).</p><span class="why">Categorias com ordem natural: ordinal.</span></div>
    <div class="item" data-ans="dis"><p>Número de filhos.</p><span class="why">Contagem: só assume valores inteiros, é discreta.</span></div>
    <div class="item" data-ans="con"><p>Altura em metros.</p><span class="why">Medida: pode assumir qualquer valor num intervalo, é contínua.</span></div>
    <div class="muted" style="margin-top:10px"><b class="sc">0 de 0 certas</b></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado: número que é categoria</span>CEP, número de telefone e código de produto parecem números, mas são <b>nominais</b>: somar CEPs não significa nada. E a média de uma escala Likert (por exemplo 3,7) é discutível, porque a distância entre "concordo" e "concordo totalmente" não é necessariamente igual à distância entre os outros pontos.</div>
</section>

<section class="sec" id="frequencia">
  <h2><span class="sn">2</span>Tabela de frequência</h2>
  <p class="gancho">A primeira coisa que se faz com uma coluna.</p>
  <p>Cada categoria ganha quatro números: <b>fi</b> (frequência absoluta: quantas vezes apareceu), <b>fr</b> (relativa: fi dividido pelo total, em %), <b>Fi</b> (acumulada: soma das fi até ali) e <b>Fr</b> (acumulada relativa). Clique em + e − para mudar as respostas e veja tudo se recalcular:</p>
  <div class="demo" data-demo="freq"></div>
  <p>No exemplo inicial, são 40 respostas: 2, 5, 9, 16 e 8. A moda é "Satisfeito" (16 respostas, 40,0%), e <b>24 de 40 (60%)</b> estão satisfeitos ou muito satisfeitos. A mediana cai em "Satisfeito" porque é nessa categoria que a frequência acumulada passa de 20 (a metade de 40): 2 + 5 + 9 = 16 está abaixo, 16 + 16 = 32 está acima.</p>
</section>

<section class="sec" id="histograma">
  <h2><span class="sn">3</span>Variável contínua: classes e histograma</h2>
  <p class="gancho">Para números contínuos, a categoria é um intervalo.</p>
  <p>Idade ou salário têm muitos valores diferentes. A tabela de frequência vira uma tabela por <b>classes</b> (intervalos), e o gráfico correspondente é o <b>histograma</b>: barras coladas, porque o eixo é contínuo. Quantas classes? Uma regra prática é a de <b>Sturges</b>: <code>k ≈ 1 + 3,322 · log₁₀(n)</code>. Mexa no controle e compare:</p>
  <div class="demo" data-demo="histograma"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: 40 idades em 6 classes</span>
    <div class="l"><div>Menor idade 19, maior 52: <b>amplitude = 52 − 19 = 33</b>.</div></div>
    <div class="l"><div>Sturges para n = 40: <code>log₁₀(40) = 1,602</code>, então <code>k = 1 + 3,322·1,602 = <b>6,32</b></code>, ou seja, <b>6 classes</b>.</div></div>
    <div class="l"><div>Largura: <code>33 / 6 = 5,5</code>; arredondando para cima para inteiros, <b>6 anos</b> por classe.</div></div>
    <div class="l"><div>Contagem: 19 a 24 → <b>13</b>; 25 a 30 → <b>15</b>; 31 a 36 → <b>8</b>; 37 a 42 → <b>2</b>; 43 a 48 → <b>1</b>; 49 a 54 → <b>1</b>. Soma: 40. Acumulada: 13, 28, 36, 38, 39, 40.</div></div>
    <div class="l"><div>Leitura: a distribuição é <b>assimétrica à direita</b>: a maioria está entre 19 e 30, e poucas pessoas mais velhas esticam a "cauda" para a direita. Por isso (em geral, é a regra prática) a <b>média (28,4)</b> fica acima da <b>mediana (27)</b>.</div></div>
  </div>
</section>

<section class="sec" id="graficos">
  <h2><span class="sn">4</span>Qual gráfico usar</h2>
  <p class="gancho">A pergunta que decide o gráfico é: o que eu quero mostrar?</p>
  <div class="tablewrap"><table>
    <tr><th>Quero mostrar...</th><th>Use</th></tr>
    <tr><td>comparar categorias</td><td>barras (ordene as barras)</td></tr>
    <tr><td>a forma da distribuição de uma variável contínua</td><td>histograma ou boxplot</td></tr>
    <tr><td>evolução no tempo</td><td>linhas</td></tr>
    <tr><td>relação entre duas variáveis quantitativas</td><td>dispersão (Capítulo 6)</td></tr>
    <tr><td>partes de um todo, com poucas categorias</td><td>pizza (ou, melhor, barras)</td></tr>
  </table></div>
  <div class="nota cuidado"><span class="lbl">Erro comum</span>Barras com o eixo vertical <b>cortado</b> (começando em 90, por exemplo) exageram diferenças pequenas. Em gráfico de barras, o zero deve estar no eixo. Histograma, por sua vez, não é gráfico de barras: as barras são coladas e a <b>largura</b> da classe importa.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Qualitativa</b> (nominal, ordinal) x <b>quantitativa</b> (discreta, contínua). O tipo decide as contas e gráficos permitidos.",
    "<b>Tabela de frequência</b>: fi, fr, Fi e Fr. Em ordinal use moda e mediana, não média.",
    "<b>Contínua</b>: classes e histograma. Sturges: <code>k ≈ 1 + 3,322·log₁₀(n)</code> (n = 40 → 6 classes).",
    "As 40 idades: 13, 15, 8, 2, 1 e 1 pessoas por classe; assimetria à direita; média 28,4 &gt; mediana 27.",
    "Barras para categorias (com zero no eixo), histograma para contínuas, linhas para tempo, dispersão para duas variáveis."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "O CEP de uma pessoa é uma variável de qual tipo?", [("a","Quantitativa contínua."),("b","Qualitativa nominal: parece número, mas é um código sem ordem nem soma com sentido."),("c","Quantitativa discreta.")], "Não faz sentido somar nem tirar média de CEPs; ele só identifica uma categoria.") + quiz(2, "c", "Em uma pergunta Likert, qual medida de tendência central é a mais segura?", [("a","A média."),("b","O desvio padrão."),("c","A moda e a mediana, por ser uma variável ordinal.")], "A ordem existe, mas as distâncias entre os pontos não são garantidamente iguais.") + quiz(3, "a", "Com n = 100 observações, pela regra de Sturges, quantas classes (aprox.) usar?", [("a","Cerca de 8 (1 + 3,322 × 2 = 7,64)."),("b","Cerca de 100."),("c","Cerca de 2.")], "log₁₀(100) = 2, então k ≈ 1 + 3,322 × 2 = 7,6, arredondando para 8.") + flash([
    ("O que é fr?", "Frequência relativa: fi dividido pelo total, em proporção ou %."),
    ("Por que o histograma tem barras coladas?", "Porque o eixo é contínuo: uma classe termina onde a próxima começa."),
    ("O que é assimetria à direita?", "Cauda longa para os valores altos; em geral, a média fica acima da mediana."),
    ("Discreta x contínua?", "Discreta resulta de contagem (inteiros). Contínua resulta de medida (qualquer valor num intervalo).")]) + ponte("Para transformar a base em números e gráficos você precisa de uma ferramenta. Vamos a ela.", "Python e R, lado a lado.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "variaveis-e-tabelas", T, "Variáveis, tabelas e gráficos (complemento)", "Capítulo 3 · Complemento",
        "Que tipo de coluna é cada uma, como montar a tabela de frequência e o histograma.",
        ["<b>~40 min</b>", "3 demos · 3 testes · 4 flashcards", "tabela de frequência e histograma ao vivo"], body3, scripts=S)
print("est caps 1-3 ok")
