import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *

PASTA = "redes-neurais"
TITULO = "Redes Neurais e Deep Learning"
T = TITULO
S = ["demos/rn.js"]
S_DATA = ["rn-data.js", "demos/rn.js"]
CAPS = [
 dict(n=1, file="cap-1-do-neuronio-a-rede.html", titulo="Do neurônio à rede", aula="Aula 2", tempo=35,
      resumo="Entradas, pesos, bias, funções de ativação e como neurônios formam camadas.",
      pergunta="A rede está montada. Mas como ela descobre os pesos certos, e como errar sem perceber?"),
 dict(n=2, file="cap-2-aprender-e-errar.html", titulo="Como a rede aprende (e erra)", aula="Aula 2", tempo=45,
      resumo="Previsão, erro, gradiente e taxa de aprendizado; overfitting, viés de confundimento e como salvar o modelo.",
      pergunta="Para entender de verdade, vamos começar pelo menor modelo possível: um único neurônio que aprende."),
 dict(n=3, file="cap-3-perceptron.html", titulo="O Perceptron", aula="Aulas 3 e 4", tempo=45,
      resumo="O primeiro neurônio que aprende, a regra de atualização dos pesos e o limite do XOR.",
      pergunta="O Perceptron aprende. Mas para que serve o bias, e o que acontece numa decisão de negócio?"),
 dict(n=4, file="cap-4-treino-e-bias.html", titulo="Treinando à mão e o papel do bias", aula="Aulas 5 e 6", tempo=40,
      resumo="Uma época de treino passo a passo, o bias como nota de corte e o modelo aprendendo o bias sozinho.",
      pergunta="Um neurônio só resolve AND e OR. Como resolver o que ele não consegue?"),
 dict(n=5, file="cap-5-mlp.html", titulo="A MLP: camada oculta", aula="Aula 7", tempo=50,
      resumo="Prever o consumo de energia: uma reta falha, uma rede com camada oculta desenha o U. Mais o XOR resolvido.",
      pergunta="A rede funcionou. Mas o que acontece por dentro quando ela treina?"),
 dict(n=6, file="cap-6-por-dentro-do-treino.html", titulo="Por dentro do treino (complemento)", aula="Complemento", tempo=40,
      resumo="Backpropagation com um exemplo numérico, funções de perda, épocas, otimizadores e como evitar overfitting.",
      pergunta="Uma camada oculta basta para tabelas. E para imagens, texto e voz?"),
 dict(n=7, file="cap-7-deep-learning.html", titulo="Deep Learning e arquiteturas (complemento)", aula="Complemento", tempo=40,
      resumo="Convolução, RNN e LSTM, Transformers, transfer learning, frameworks e os riscos de levar um modelo a produção.",
      pergunta="Todas essas redes aprendem por gradiente. Existe um jeito de otimizar sem ele?"),
 dict(n=8, file="cap-8-algoritmos-geneticos.html", titulo="Algoritmos Genéticos (complemento)", aula="Complemento", tempo=40,
      resumo="Seleção, cruzamento e mutação para otimizar sem gradiente, e onde isso é usado.",
      pergunta=""),
]
manifest(PASTA, "redes-neurais", TITULO, CAPS)
hub(PASTA, TITULO, "Redes Neurais Artificiais, Deep Learning e Algoritmos Genéticos", "Apostila de Redes Neurais e Deep Learning",
    "Do neurônio artificial até a rede que aprende o XOR, passando por overfitting, convolução e algoritmos genéticos. Com redes treinando de verdade na sua tela.",
    ["<b>8</b> capítulos", "<b>~5h30</b> de estudo ativo", "redes treinando no navegador"],
    '<p>A história é a de um problema que <mark class="hl">uma reta não resolve</mark>. Começamos com um neurônio, vemos o que ele consegue (e o que não consegue: o XOR), e então empilhamos camadas até a rede desenhar a curva que faltava. Cada capítulo responde à limitação do anterior. Os capítulos 6 a 8 são complemento: o que acontece por dentro do treino, as arquiteturas modernas e uma família de algoritmos que otimiza sem gradiente.</p>',
    'Os números de erro (RMSE) da rede de energia vêm do <b>scikit-learn</b>, rodados sobre o mesmo arquivo da aula. As redes pequenas das demos são treinadas <b>de verdade no navegador</b>, mas não são a mesma implementação, então os números delas não são comparáveis aos do notebook.')

# ---------------- CAP 1 ----------------
body1 = recap("Este é o primeiro capítulo. Você não precisa saber nada de redes neurais: basta ter visto a ideia de que um modelo de machine learning aprende com exemplos. Daqui em diante, cada capítulo abre com a pergunta que o anterior deixou em aberto.", "Ponto de partida") + '''
<section class="sec" id="o-que-e">
  <h2><span class="sn">1</span>O que é uma rede neural</h2>
  <p class="gancho">Um modelo de matemática, vagamente inspirado em um cérebro.</p>
  <p>Uma <b>rede neural artificial</b> é um modelo matemático inspirado, <i>de forma bem simplificada</i>, nos neurônios biológicos. Ela recebe dados de entrada, processa por várias <b>camadas</b> de neurônios artificiais ligados por <b>pesos</b> e produz uma saída: uma previsão, uma classificação, um número. O <mark class="hl">aprendizado</mark> é o processo de ajustar esses pesos, repetidamente, até a rede acertar (ou chegar perto) nos dados de treino.</p>
  <p>A aula organiza o assunto seguindo o fluxo real: <b>como o dado entra e é processado</b> (estrutura), <b>como a rede responde</b> (inferência), <b>como aprende com o erro</b> (treinamento) e <b>quais os riscos</b>. Este capítulo cobre a estrutura.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Qual é a menor peça dessa máquina?</div><p>O neurônio.</p></div>
</section>

<section class="sec" id="neuronio">
  <h2><span class="sn">2</span>O neurônio: soma, pesos e ativação</h2>
  <p class="gancho">Três passos, sempre os mesmos.</p>
  <ol>
    <li><b>Receber</b> uma ou mais entradas.</li>
    <li><b>Multiplicar</b> cada entrada pelo <b>peso</b> da conexão, <b>somar</b> tudo e acrescentar o <b>bias</b> (viés): <code>z = x₁·w₁ + x₂·w₂ + ... + b</code>.</li>
    <li>Passar <code>z</code> pela <b>função de ativação</b> e <b>repassar</b> o resultado à próxima camada.</li>
  </ol>
  <p>Mexa em tudo e acompanhe a conta:</p>
  <div class="demo" data-demo="neuronio"></div>
  <div class="tablewrap"><table>
    <tr><th>Neurônio biológico</th><th>Neurônio artificial</th></tr>
    <tr><td>Dendritos</td><td>Entradas (x₁, x₂, ...)</td></tr>
    <tr><td>Sinapses</td><td>Pesos (w₁, w₂, ...)</td></tr>
    <tr><td>Corpo celular (soma)</td><td>Somatório: <code>z = Σ wᵢxᵢ + b</code></td></tr>
    <tr><td>Axônio (dispara se passa de um limiar)</td><td>Função de ativação → saída</td></tr>
  </table></div>
  <div class="grid2">
    <div class="card rv"><b>Peso</b><p>O número que multiplica o sinal de cada conexão. É o principal parâmetro <b>aprendido</b>: peso grande (em valor absoluto) = a conexão influencia muito a decisão. No começo, costuma ser pequeno e aleatório.</p></div>
    <div class="card rv"><b>Bias</b><p>Um valor somado ao final. Desloca a decisão: pense nos pesos como "o quanto cada informação conta" e no bias como "a nota de corte". (O Capítulo 4 mostra o que acontece sem ele.)</p></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">A função de ativação decide o formato da saída. Quais existem, e por que ela é indispensável?</div><p>Veja as mais comuns.</p></div>
</section>

<section class="sec" id="ativacoes">
  <h2><span class="sn">3</span>Funções de ativação</h2>
  <p class="gancho">Sem elas, mil camadas valem uma só.</p>
  <div class="demo" data-demo="ativacoes"></div>
  <div class="tablewrap"><table>
    <tr><th>Função</th><th>O que faz</th><th>Onde se usa</th></tr>
    <tr><td><b>Degrau</b></td><td>1 se z ≥ 0, senão 0</td><td>o Perceptron clássico (Capítulo 3)</td></tr>
    <tr><td><b>ReLU</b></td><td>zera o negativo, mantém o positivo</td><td>camadas ocultas: simples e eficiente</td></tr>
    <tr><td><b>Sigmoide</b></td><td>comprime para (0, 1)</td><td>saída de classificação binária (probabilidade)</td></tr>
    <tr><td><b>Tanh</b></td><td>comprime para (−1, 1), centrada em zero</td><td>camadas ocultas de redes menores (aparece no experimento do Capítulo 5)</td></tr>
    <tr><td><b>Sigmoide (ou logística)</b></td><td colspan="2">é a mesma função: o scikit-learn a chama de <code>logistic</code></td></tr>
    <tr><td><b>Softmax</b></td><td>generaliza a sigmoide: várias saídas que somam 1</td><td>saída de classificação com várias classes ("83% gato, 17% cachorro")</td></tr>
    <tr><td><b>Linear / identidade</b></td><td>devolve z, sem alterar</td><td>saída de <b>regressão</b> (prever um número)</td></tr>
  </table></div>
  <div class="nota lembra"><span class="lbl">Por que não linear em tudo?</span>Uma conta linear aplicada a outra conta linear continua sendo <b>uma</b> conta linear. Sem uma ativação <b>não linear</b> nas camadas ocultas, a rede inteira se comporta como uma única camada e perde a capacidade de aprender curvas. A última ativação define o <b>formato da saída</b>: linear para números, sigmoide ou softmax para probabilidades.</div>
</section>

<section class="sec" id="camadas">
  <h2><span class="sn">4</span>Camadas, parâmetros e hiperparâmetros</h2>
  <p class="gancho">Quem aprende, e quem é escolhido por você?</p>
  <ul>
    <li><b>Camada de entrada</b>: recebe os dados brutos (e não calcula nada).</li>
    <li><b>Camadas ocultas</b>: processamento intermediário. Quanto mais fundas, mais abstratas as características que extraem (daí o <i>deep</i> learning: muitas camadas).</li>
    <li><b>Camada de saída</b>: o resultado.</li>
    <li>Os <b>filamentos</b> são as conexões: por elas o sinal flui, multiplicado pelo peso de cada uma.</li>
  </ul>
  <div class="grid2">
    <div class="card rv"><b>Parâmetros</b><p>O que a rede <b>aprende</b>: os <b>pesos</b> e os <b>vieses</b> de todos os neurônios. Uma rede com 1 entrada, 8 neurônios ocultos e 1 saída tem (1×8) + 8 + (8×1) + 1 = <b>25</b> parâmetros.</p></div>
    <div class="card rv"><b>Hiperparâmetros</b><p>O que <b>você escolhe</b> antes de treinar: número de camadas e neurônios, função de ativação, <b>taxa de aprendizado</b>, número de épocas.</p></div>
  </div>
  <p>Antes de entrar na rede, o dado costuma ser <b>pré-processado</b> (redimensionado, normalizado para uma escala padrão como 0 a 1). A qualidade e a representatividade da entrada definem em grande parte o que a rede consegue aprender: um padrão acidental no dado (como o fundo de uma foto) pode ser aprendido no lugar do conceito desejado. O Capítulo 2 mostra um caso real.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Neurônio</b>: <code>z = Σ wᵢxᵢ + b</code>, depois <b>ativação</b>. <b>Peso</b> diz o quanto cada entrada conta; <b>bias</b> é a nota de corte.",
    "<b>Ativação não linear</b> (ReLU, sigmoide, softmax...) é o que dá à rede capacidade de aprender curvas. Sem ela, a rede é uma conta linear só.",
    "A ativação da <b>saída</b> define o formato: linear (número), sigmoide (probabilidade), softmax (várias classes).",
    "<b>Parâmetros</b> (pesos e vieses) são aprendidos. <b>Hiperparâmetros</b> (camadas, taxa de aprendizado, épocas) são escolhidos por você.",
    "Camadas: entrada, ocultas (mais fundas, mais abstratas) e saída."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que uma rede de várias camadas sem função de ativação não linear não é melhor que uma camada só?", [("a","Porque as camadas ocultas não têm pesos."),("b","Porque compor contas lineares dá, no fim, uma única conta linear."),("c","Porque a saída sempre é zero.")], "Linear de linear continua linear. A não linearidade entre as camadas é o que permite aprender curvas.") + quiz(2, "c", "Qual ativação usar na saída de uma rede que prevê o preço de uma casa?", [("a","Sigmoide."),("b","Softmax."),("c","Linear (sem limitar a saída).")], "Preço é um número contínuo, que não deve ser 'espremido' entre 0 e 1.") + quiz(3, "a", "Quantos parâmetros tem uma rede 3-5-2 (3 entradas, 5 neurônios ocultos, 2 saídas)?", [("a","(3×5 + 5) + (5×2 + 2) = 32."),("b","3 + 5 + 2 = 10."),("c","3 × 5 × 2 = 30.")], "Cada camada tem pesos (entradas × neurônios) e um bias por neurônio: 15 + 5 + 10 + 2 = 32.") + flash([
    ("O que é um peso?", "O número que multiplica o sinal de uma conexão. É o que a rede aprende."),
    ("Parâmetro x hiperparâmetro?", "Parâmetro é aprendido (pesos e vieses). Hiperparâmetro é escolhido por quem treina."),
    ("Para que serve a ReLU?", "Zera o negativo e mantém o positivo: ativação simples e eficiente para camadas ocultas."),
    ("O que a softmax devolve?", "Probabilidades para várias classes, que somam 1.")]) + ponte("A rede está montada. Mas como ela descobre os pesos certos, e como errar sem perceber?", "Pelo erro: ela prevê, mede o quanto errou e se corrige.", "Para onde vamos agora · Capítulo 2") + '''
</section>'''
chapter(PASTA, 1, "do-neuronio-a-rede", T, "Do neurônio à rede", "Capítulo 1 · Aula 2",
        "A estrutura de uma rede neural: neurônios, pesos, ativações e camadas.",
        ["<b>~35 min</b>", "2 demos · 3 testes · 4 flashcards", "mexa em um neurônio"], body1, scripts=S)

# ---------------- CAP 2 ----------------
body2 = recap("No Capítulo 1 a rede foi montada: neurônios, pesos, camadas e ativações. Mas os pesos começam aleatórios, e uma rede aleatória não serve para nada. Este capítulo mostra como os pesos são ajustados, e o risco central do aprendizado: <b>acertar o treino sem entender o problema</b>.") + '''
<section class="sec" id="inferencia">
  <h2><span class="sn">1</span>Prever: o caminho de ida</h2>
  <p class="gancho">O dado entra, atravessa as camadas e sai uma resposta.</p>
  <p>O <b>predict</b> é o momento em que o modelo já treinado recebe um dado <b>novo</b> e produz a saída com os parâmetros já ajustados. Duas formas de saída:</p>
  <div class="grid2">
    <div class="card rv"><b>Regressão: um número</b><p>A saída é <b>linear</b>, qualquer valor real (preço de uma casa, consumo de energia).</p></div>
    <div class="card rv"><b>Classificação: probabilidades</b><p>A saída aplica <b>sigmoide</b> (2 classes) ou <b>softmax</b> (várias): "83% gato, 17% cachorro". A classe prevista é a de maior probabilidade. (O nome <i>regressão logística</i>, apesar da palavra, é classificação.)</p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado</span>Probabilidade alta <b>não garante</b> que o modelo aprendeu o conceito certo. Ele pode estar confiante por ter aprendido um atalho do conjunto de treino. É o assunto da seção 4.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">E quando o palpite está errado? Como a rede se corrige?</div><p>Medindo o erro e andando na direção que o reduz.</p></div>
</section>

<section class="sec" id="treino">
  <h2><span class="sn">2</span>Aprender: erro, gradiente e taxa de aprendizado</h2>
  <p class="gancho">Errou? Descubra qual peso mais contribuiu e mexa nele.</p>
  <p>O ciclo de treino repete, muitas vezes: <b>(1)</b> a rede <b>prevê</b>; <b>(2)</b> compara com o valor real e calcula um <b>erro</b> (a <i>perda</i>, ou <i>loss</i>); <b>(3)</b> o algoritmo de <b>backpropagation</b> (retropropagação) calcula o quanto <b>cada peso</b> contribuiu para o erro, da saída para a entrada; <b>(4)</b> um otimizador, como o <b>gradiente descendente</b>, ajusta cada peso <b>na direção que reduz o erro</b>. Todo o capítulo 6 destrincha esses passos com números.</p>
  <p>A intuição cabe numa imagem: o erro como uma <b>paisagem</b>, e o treino como descer a ladeira. A <b>taxa de aprendizado</b> (<i>learning rate</i>) é o <b>tamanho do passo</b>. Experimente passos de tamanhos diferentes:</p>
  <div class="demo" data-demo="gradiente"></div>
  <div class="grid2">
    <div class="card rv"><b>Taxa muito alta</b><p>Passos grandes demais: a rede "pula" em torno do ponto ótimo ou diverge.</p></div>
    <div class="card rv"><b>Taxa muito baixa</b><p>Aprende devagar demais, e pode empacar em soluções ruins ou gastar tempo e recursos à toa.</p></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Treinar mais é sempre melhor? O erro de treino cai sempre. E o de teste?</div><p>Nem sempre.</p></div>
</section>

<section class="sec" id="overfit">
  <h2><span class="sn">3</span>Overfitting: decorar não é aprender</h2>
  <p class="gancho">A rede acertou 100% do treino e falhou na vida real.</p>
  <p>O <b>overfitting</b> (sobreajuste) acontece quando o modelo se ajusta <i>demais</i> às particularidades do treino, inclusive ao <b>ruído</b>, em vez de aprender o padrão geral. O sintoma: acurácia ou erro excelentes no treino e ruins em dados novos. Visualize com um modelo mais simples de ver, polinômios sobre pontos de uma curva com ruído. Aumente o grau (a complexidade) e compare o erro de treino com o de teste:</p>
  <div class="demo" data-demo="overfit"></div>
  <p>Formas de reduzir o overfitting: <b>mais dados, e mais diversos</b> (não só quantidade, mas variedade de situações); <b>regularização</b> (penalizar pesos muito grandes); <b>dropout</b> (desligar neurônios ao acaso durante o treino); e <b>early stopping</b> (parar antes de começar a memorizar). E, claro, a regra do Capítulo 2 de Machine Learning: avaliar sempre em dados que o modelo <b>nunca viu</b>.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Existe um erro mais traiçoeiro: aquele em que o modelo "generaliza" bem, mas aprendeu a coisa errada.</div><p>O experimento do gato e do cachorro mostra.</p></div>
</section>

<section class="sec" id="features">
  <h2><span class="sn">4</span>Features e o viés de confundimento</h2>
  <p class="gancho">A rede escolhe o atalho mais fácil, e não o mais inteligente.</p>
  <p><b>Features</b> (características) são os padrões que a rede extrai dos dados ao longo das camadas: em uma imagem, bordas e texturas nas primeiras camadas, e combinações mais abstratas (como "orelha pontuda") nas mais profundas. O ponto crucial: a rede <b>não escolhe features de forma "inteligente" ou alinhada à nossa intuição</b>. Ela escolhe <b>qualquer padrão estatístico</b> que reduza o erro no treino, mesmo que seja um atalho.</p>
  <div class="ex rv"><span class="t">O experimento do Teachable Machine</span>
    <div class="l"><div>Uma rede foi treinada para separar <b>gato</b> de <b>cachorro</b> com cerca de 40 imagens. Nas fotos de cachorro, o fundo era, em geral, um gramado verde.</div></div>
    <div class="l"><div>Ao testar com imagens novas, o modelo errava justamente quando o <b>fundo</b> contrariava o padrão: ele tinha aprendido "fundo verde = cachorro".</div></div>
    <div class="l"><div>Isso não é "decorar as 40 fotos". É o <b>viés de confundimento</b> (<i>confounding</i>): um padrão <b>correlacionado</b> com a resposta no dataset, mas sem relação com o conceito real. Acertou o treino e o teste parecido, e falhou na realidade.</div></div>
  </div>
  <p>Como o Teachable Machine usa <i>transfer learning</i> (a maior parte dos pesos vem pré-treinada de um modelo genérico, e só as últimas camadas se ajustam às suas classes), ele pode também herdar sensibilidade a padrões de fundo. A defesa é a <b>diversidade dos dados</b>: se os cachorros aparecem em fundos variados, o fundo deixa de ser um atalho útil.</p>
  <div class="nota exemplo"><span class="lbl">Complemento: salvar o modelo</span>Depois do treino, o modelo (a arquitetura e os pesos ajustados) precisa ser guardado, para não treinar tudo de novo. Em Python, um formato comum é o <b>pickle</b> (<code>.pkl</code>): <code>pickle.dump(modelo, arquivo)</code> salva e <code>pickle.load(arquivo)</code> recupera. Treina-se uma vez (caro) e reutiliza-se quantas vezes quiser, indo direto ao <i>predict</i>. Atenção de segurança: <b>nunca carregue um <code>.pkl</code> de fonte desconhecida</b>, porque o pickle pode executar código ao ser carregado.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Ciclo de treino: <b>prever → medir o erro → backpropagation → ajustar os pesos</b>, muitas vezes.",
    "<b>Gradiente descendente</b>: descer a ladeira do erro. <b>Taxa de aprendizado</b> = tamanho do passo (alta: diverge; baixa: lenta).",
    "<b>Overfitting</b>: erro baixo no treino, alto no teste. Combate: mais dados diversos, regularização, dropout, early stopping.",
    "<b>Viés de confundimento</b>: a rede aprende um atalho correlacionado (o fundo), e não o conceito. Defesa: dados diversos.",
    "Salvar o modelo: <code>pickle</code> (<code>.pkl</code>). Nunca carregue de fonte desconhecida."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Uma rede tem erro de treino quase zero e erro de teste alto. O que isso indica?", [("a","Underfitting."),("b","Que a taxa de aprendizado está baixa."),("c","Overfitting: ela decorou o treino e não generaliza.")], "O sintoma clássico do sobreajuste é a distância entre o desempenho no treino e no teste.") + quiz(2, "a", "No experimento gato x cachorro, o que explica o modelo errar quando o fundo mudava?", [("a","Ele aprendeu o fundo (um padrão correlacionado) em vez do animal."),("b","Ele decorou as 40 imagens."),("c","A taxa de aprendizado era alta.")], "Foi viés de confundimento: o atalho funcionava no dataset, mas não tinha relação com o conceito.") + quiz(3, "b", "O que acontece com uma taxa de aprendizado alta demais?", [("a","A rede aprende mais rápido e sempre melhor."),("b","Ela pode oscilar em torno do ponto ótimo ou divergir."),("c","Nada: a taxa não importa.")], "Passos grandes demais ultrapassam o mínimo, como a demo do gradiente mostrou.") + flash([
    ("O que é backpropagation?", "O algoritmo que calcula o quanto cada peso contribuiu para o erro, propagando o sinal da saída para a entrada."),
    ("O que é overfitting?", "Ajustar-se demais ao treino (inclusive ao ruído), e falhar em dados novos."),
    ("O que é viés de confundimento?", "Aprender um padrão correlacionado com a resposta no dataset, mas sem relação com o conceito real."),
    ("Para que serve o dropout?", "Desligar neurônios ao acaso no treino, para a rede não depender de caminhos específicos.")]) + ponte("Para entender de verdade, vamos começar pelo menor modelo possível: um único neurônio que aprende.", "O Perceptron.", "Para onde vamos agora · Capítulo 3") + '''
</section>'''
chapter(PASTA, 2, "aprender-e-errar", T, "Como a rede aprende (e erra)", "Capítulo 2 · Aula 2",
        "O ciclo de treino, o tamanho do passo e a armadilha de decorar ou de aprender o atalho errado.",
        ["<b>~45 min</b>", "2 demos · 3 testes · 4 flashcards", "gradiente e overfitting interativos"], body2, scripts=S)

# ---------------- CAP 3 ----------------
body3 = recap("No Capítulo 2 você viu o ciclo de treino da rede inteira. Para enxergar cada peça com clareza, vamos voltar ao começo da história: o <b>Perceptron</b>, um único neurônio com ativação degrau e uma regra de aprendizado que cabe em duas linhas.") + '''
<section class="sec" id="historia">
  <h2><span class="sn">1</span>Uma história curta</h2>
  <p class="gancho">A ideia tem mais de 80 anos, e já quebrou o coração dos pesquisadores uma vez.</p>
  <div class="tl rv">
    <div class="ev"><b>1943</b><span>McCulloch e Pitts: o primeiro modelo matemático do neurônio.</span></div>
    <div class="ev"><b>1958</b><span>Rosenblatt: o Perceptron, o primeiro "neurônio" que aprende.</span></div>
    <div class="ev"><b>1969</b><span>Minsky e Papert provam o limite do XOR no livro <i>Perceptrons</i>; começa o primeiro "inverno da IA" (anos 1970).</span></div>
    <div class="ev"><b>1986</b><span>Rumelhart, Hinton e Williams: o backpropagation viabiliza as redes de várias camadas.</span></div>
    <div class="ev"><b>2012</b><span>AlexNet vence o ImageNet: o deep learning chega à visão computacional.</span></div>
    <div class="ev"><b>2017+</b><span>Transformers e os grandes modelos de linguagem.</span></div>
  </div>
  <div class="nota lembra"><span class="lbl">Um fato recente</span>Em 2024, o Nobel de Física foi para John Hopfield e Geoffrey Hinton pelos fundamentos das redes neurais artificiais, e o de Química para Demis Hassabis e John Jumper (AlphaFold) e David Baker (design de proteínas). A área saiu do laboratório para a ciência de ponta e para os negócios.</div>
</section>

<section class="sec" id="arquitetura">
  <h2><span class="sn">2</span>O Perceptron por dentro</h2>
  <p class="gancho">Entradas → pesos → soma → degrau → saída.</p>
<pre><code>z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b      <span class="c"># soma ponderada</span>
ŷ = f(z),   f(z) = 1 se z ≥ 0, senão 0  <span class="c"># função degrau</span></code></pre>
  <p>É exatamente o neurônio do Capítulo 1, com a ativação degrau. E a <b>fronteira de decisão</b> é a reta onde <code>z = 0</code>: de um lado a saída é 1, do outro, 0. O bias <b>desloca</b> essa reta; sem ele, ela seria obrigada a passar pela origem.</p>
  <h3>A regra de aprendizado</h3>
  <p>Para cada exemplo, o Perceptron prevê e compara com a resposta certa. <b>Só se errar</b>, ajusta:</p>
  <div class="formula">wᵢ ← wᵢ + η · (y − ŷ) · xᵢ<br>b  ← b  + η · (y − ŷ)<small>η é a taxa de aprendizado, y a resposta correta, ŷ a previsão e (y − ŷ) o erro.</small></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: treinando a porta AND</span>
    <div class="l"><div>Estado inicial: <code>w₁ = 0</code>, <code>w₂ = 0</code>, <code>b = 0</code>, <code>η = 0,1</code>. Exemplo: <b>(x₁ = 1, x₂ = 0)</b>, resposta correta <b>y = 0</b>.</div></div>
    <div class="l"><div><code>z = 0·1 + 0·0 + 0 = 0</code>. Como <code>z ≥ 0</code>, a previsão é <b>ŷ = 1</b>. Errou, porque y = 0.</div></div>
    <div class="l"><div>Erro: <code>y − ŷ = 0 − 1 = −1</code>.</div></div>
    <div class="l"><div><code>w₁ ← 0 + 0,1·(−1)·1 = <b>−0,1</b></code>; <code>w₂ ← 0 + 0,1·(−1)·0 = <b>0</b></code>; <code>b ← 0 + 0,1·(−1) = <b>−0,1</b></code>.</div></div>
    <div class="l"><div>O ciclo se repete por todos os exemplos, por várias <b>épocas</b>, até parar de errar.</div></div>
  </div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Ele aprende AND. Aprende tudo?</div><p>Teste você.</p></div>
</section>

<section class="sec" id="porta">
  <h2><span class="sn">3</span>Treine você: AND, OR e o problema do XOR</h2>
  <p class="gancho">Duas portas funcionam. A terceira não tem solução.</p>
  <div class="demo" data-demo="perceptron"></div>
  <p><b>AND</b> e <b>OR</b> são <b>linearmente separáveis</b>: uma única reta separa os 0 dos 1. O <b>XOR</b> ("um ou outro, mas não os dois") <b>não é</b>: não existe uma reta que separe (0,0) e (1,1) de (0,1) e (1,0). Por mais épocas que você rode, o Perceptron nunca zera os erros no XOR. Foi essa prova, de Minsky e Papert (1969), que <b>paralisou a pesquisa</b> em redes neurais por anos. A saída, décadas depois: <b>empilhar neurônios em camadas</b>, o assunto do Capítulo 5.</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: > ou ≥?</span>Algumas fontes usam <code>z &gt; 0</code> para disparar, e outras <code>z ≥ 0</code>. A diferença só aparece quando <code>z</code> é exatamente zero. Neste capítulo e nos notebooks da aula a regra é <b>z ≥ 0</b>. Em planilha, confira qual comparação a fórmula usa.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Perceptron</b> (Rosenblatt, 1958): <code>z = Σ wᵢxᵢ + b</code> e degrau. Um neurônio que <b>aprende</b>.",
    "<b>Regra</b>: <code>w ← w + η·(y − ŷ)·x</code> e <code>b ← b + η·(y − ŷ)</code>, só quando erra.",
    "A <b>fronteira de decisão</b> é uma reta; o bias a desloca.",
    "<b>AND</b> e <b>OR</b> são linearmente separáveis. <b>XOR</b> não é: o Perceptron nunca converge (livro <i>Perceptrons</i>, 1969; primeiro inverno da IA nos anos 1970).",
    "A saída: empilhar camadas (MLP) com backpropagation (1986)."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Com w₁ = w₂ = 0, b = 0, η = 0,1, a entrada (1, 1) e resposta y = 0, o Perceptron (degrau com ≥ 0) acerta?", [("a","Sim, a previsão é 0."),("b","Não: z = 0 dispara 1, o erro é −1 e os pesos viram −0,1, −0,1 e bias −0,1."),("c","Não muda nada.")], "z = 0 e, com ≥ 0, a saída é 1. O erro (0 − 1) = −1 corrige cada peso em η·erro·x = −0,1, e o bias em −0,1.") + quiz(2, "c", "Por que o XOR não pode ser aprendido por um Perceptron simples?", [("a","Porque tem poucos exemplos."),("b","Porque a taxa de aprendizado é fixa."),("c","Porque nenhuma reta separa os casos 0 dos casos 1.")], "O Perceptron só desenha uma fronteira reta. O XOR exige uma fronteira curva ou duas retas.") + quiz(3, "a", "Quando o Perceptron atualiza os pesos?", [("a","Apenas quando erra a previsão."),("b","Sempre, a cada exemplo."),("c","Só no fim da época.")], "Se o erro (y − ŷ) é zero, os termos de ajuste são zero e nada muda.") + flash([
    ("O que é uma fronteira de decisão?", "A linha onde z = 0: de um lado o neurônio responde 1, do outro 0."),
    ("O que é linearmente separável?", "Quando uma única reta separa as classes (como AND e OR)."),
    ("O que foi o inverno da IA?", "O período de queda de interesse e verba depois da prova de que o Perceptron não resolve o XOR."),
    ("O que é uma época?", "Uma passada completa por todos os exemplos de treino.")]) + ponte("O Perceptron aprende. Mas para que serve o bias, e o que acontece numa decisão de negócio?", "Treinar à mão, linha a linha, e depois isolar o papel do bias.", "Para onde vamos agora · Capítulo 4") + '''
</section>'''
chapter(PASTA, 3, "perceptron", T, "O Perceptron", "Capítulo 3 · Aulas 3 e 4",
        "O primeiro neurônio que aprende, como ele ajusta os pesos e por que o XOR o derrota.",
        ["<b>~45 min</b>", "1 demo · 3 testes · 4 flashcards", "treine AND, OR e XOR"], body3, scripts=S)
print("rn caps 1-3 ok")
