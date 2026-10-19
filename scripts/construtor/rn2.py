import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
import rn
PASTA, T, S, S_DATA = rn.PASTA, rn.T, rn.S, rn.S_DATA

# ---------------- CAP 4 ----------------
body4 = recap("No Capítulo 3 o Perceptron aprendeu a porta AND com a regra <code>w ← w + η(y − ŷ)x</code>. Agora trocamos a porta lógica por uma <b>decisão de negócio</b> e isolamos uma peça que costuma ser esquecida: o <b>bias</b>.") + '''
<section class="sec" id="decisao">
  <h2><span class="sn">1</span>A mesma conta, numa decisão de negócio</h2>
  <p class="gancho">AND vira "liberar a oferta só se as duas condições valem".</p>
  <p>Imagine uma regra: liberar uma oferta somente se o cliente <b>pagou em dia</b> <i>e</i> tem <b>alto engajamento</b>. Cada condição é 0 ou 1. A tabela do AND vira a tabela da decisão: só o caso <code>[1, 1]</code> libera.</p>
  <div class="tablewrap"><table>
    <tr><th>pagou em dia</th><th>engajado</th><th>liberar?</th></tr>
    <tr><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr>
  </table></div>
  <p>Com pesos <code>w₁ = w₂ = 1</code>, a soma <code>z = x₁ + x₂</code> vale 0, 1, 1 e 2. Falta decidir <b>onde cortar</b>. É exatamente o trabalho do bias.</p>
</section>

<section class="sec" id="bias">
  <h2><span class="sn">2</span>O bias é a nota de corte</h2>
  <p class="gancho">Sem ele, a reta é obrigada a passar pela origem.</p>
  <p>Mexa no bias e nos pesos da demo. Comece pelo ponto inicial (pesos 1 e 1, bias 0) e leia o que a tabela diz:</p>
  <div class="demo" data-demo="bias"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: sem bias e com bias −1,5</span>
    <div class="l"><div>Sem bias (<code>b = 0</code>): <code>[0,0]</code> dá <code>z = 0</code>. Com o degrau <code>z ≥ 0</code>, sai <b>1</b>. Errado. <code>[0,1]</code> e <code>[1,0]</code> dão <code>z = 1</code> e saem 1, também errados. Só <code>[1,1]</code> acerta: <b>3 erros em 4</b>.</div></div>
    <div class="l"><div>Com <code>b = −1,5</code>: as somas viram <code>−1,5</code>, <code>−0,5</code>, <code>−0,5</code> e <code>+0,5</code>. Só a última passa do zero. <b>4 acertos em 4</b>.</div></div>
    <div class="l"><div>Leitura de negócio: o bias <b>exige evidência suficiente</b> antes de responder 1. Uma evidência sozinha (soma 1) não basta.</div></div>
  </div>
  <div class="nota lembra"><span class="lbl">Em uma frase</span>Os pesos dizem <b>o quanto cada informação conta</b>. O bias diz <b>o quanto de evidência é preciso</b> para o neurônio disparar.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Em vez de escolher o bias à mão, dá para o modelo achá-lo sozinho?</div><p>Dá: é só deixar a regra de aprendizado rodar.</p></div>
</section>

<section class="sec" id="treino-mao">
  <h2><span class="sn">3</span>O modelo aprendendo o bias sozinho</h2>
  <p class="gancho">Clique em "Deixar o modelo aprender" na demo e compare com a conta abaixo.</p>
  <p>Partindo de pesos e bias zero, com <code>η = 0,1</code> e a ordem de exemplos <code>[0,0] → [0,1] → [1,0] → [1,1]</code>, as épocas ficam assim (a mesma tabela que a demo mostra):</p>
  <div class="tablewrap"><table>
    <tr><th>época</th><th>pesos ao fim</th><th>bias ao fim</th><th>erros</th></tr>
    <tr><td>1</td><td>[0,1; 0,1]</td><td>0,0</td><td>2</td></tr>
    <tr><td>2</td><td>[0,2; 0,1]</td><td>−0,1</td><td>3</td></tr>
    <tr><td>3</td><td>[0,2; 0,1]</td><td>−0,2</td><td>3</td></tr>
    <tr><td>4</td><td>[0,2; 0,2]</td><td>−0,2</td><td>2</td></tr>
    <tr><td>5</td><td>[0,2; 0,1]</td><td>−0,3</td><td>1</td></tr>
    <tr><td>6</td><td>[0,2; 0,1]</td><td>−0,3</td><td>0</td></tr>
  </table></div>
  <p>Repare que o bias <b>desce</b> a cada erro de "falso positivo" (o modelo respondeu 1 quando devia ser 0), e que na época 6 <b>não há mais erros</b>: o treino convergiu. O resultado, <code>w = [0,2; 0,1]</code> e <code>b = −0,3</code>, é <b>diferente</b> do −1,5 que escolhemos à mão, e é igualmente válido: qualquer reta que separe o [1,1] dos outros três serve. Se a ordem dos exemplos ou a taxa de aprendizado mudarem, os números mudam, mas o ponto é o mesmo.</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: ≥ ou &gt; de novo</span>Uma planilha que use <code>z &gt; 0</code> no degrau vai gerar uma tabela de épocas diferente da acima, porque o caso <code>z = 0</code> passa a responder 0. Confira sempre qual comparação a sua conta usa antes de comparar resultados.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "O AND vira uma <b>regra de negócio</b>: liberar só quando as duas condições valem.",
    "<b>Bias = nota de corte.</b> Sem ele, a fronteira passa pela origem e o caso [0,0] dispara errado (3 erros em 4 com pesos 1 e 1).",
    "Com <b>b = −1,5</b>, só a soma 2 passa do corte: 4 acertos em 4.",
    "A regra de aprendizado também ajusta o bias: <code>b ← b + η(y − ŷ)</code>. Aqui convergiu na época 6 (<code>w = [0,2; 0,1]</code>, <code>b = −0,3</code>).",
    "Existem <b>muitas</b> retas válidas. O treino acha uma delas."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Com pesos 1 e 1, bias 0 e degrau z ≥ 0, quantos dos 4 casos do AND o neurônio acerta?", [("a","Os 4."),("b","Só 1: o [1,1]."),("c","Nenhum.")], "Os casos [0,0], [0,1] e [1,0] dão z ≥ 0 e saem 1, errado. Só o [1,1] acerta.") + quiz(2, "a", "Por que b = −1,5 resolve o AND com pesos 1 e 1?", [("a","Porque só a soma 2 fica acima do corte, e as somas 0 e 1 ficam negativas."),("b","Porque muda os pesos."),("c","Porque troca o degrau por ReLU.")], "z = soma − 1,5: dá −1,5, −0,5, −0,5 e +0,5.") + quiz(3, "c", "O bias que o modelo aprendeu (−0,3) é diferente de −1,5. O que isso significa?", [("a","Que o treino falhou."),("b","Que o −1,5 está errado."),("c","Que há várias retas válidas; ambos separam o [1,1] dos demais.")], "O treino para quando para de errar, não quando acha 'a' solução única.") + flash([
    ("O que o bias representa?", "A nota de corte: quanto de evidência é preciso para o neurônio responder 1."),
    ("Como o bias é atualizado?", "b ← b + η·(y − ŷ), só quando o neurônio erra."),
    ("O que é um falso positivo aqui?", "O modelo responde 1 quando o correto era 0. Empurra o bias para baixo."),
    ("O que muda ao trocar ≥ por > no degrau?", "O caso z = 0 passa a responder 0, e a tabela de épocas muda.")]) + ponte("Um neurônio só resolve AND e OR. Como resolver o que ele não consegue?", "Com uma camada oculta: a MLP.", "Para onde vamos agora · Capítulo 5") + '''
</section>'''
chapter(PASTA, 4, "treino-e-bias", T, "Treinando à mão e o papel do bias", "Capítulo 4 · Aulas 5 e 6",
        "Uma decisão de negócio como porta AND e o bias como nota de corte.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "ajuste o bias e veja o corte"], body4, scripts=S)

# ---------------- CAP 5 ----------------
body5 = recap("No Capítulo 3 o XOR derrotou o neurônio único, e no Capítulo 4 vimos que o bias desloca a reta. Agora empilhamos neurônios: com uma <b>camada oculta</b>, a rede deixa de desenhar só retas. Aplicamos isso a um problema real em forma de U: o consumo de energia de um prédio ao longo da temperatura.") + '''
<section class="sec" id="problema">
  <h2><span class="sn">1</span>O problema: energia em forma de U</h2>
  <p class="gancho">Frio liga o aquecedor, calor liga o ar-condicionado, o meio é barato.</p>
  <p>O arquivo <code>consumo_energia_mlp.csv</code> tem <b>365 dias</b> com a temperatura média e o consumo de energia (kWh). Os dados são <b>sintéticos</b> (gerados por computador para ilustrar o problema), não medições de um prédio real. A relação não é uma reta: o consumo é <b>alto no frio, baixo em temperatura amena e alto de novo no calor</b>. Os dados foram divididos em <b>treino e teste</b> (<code>test_size = 0,25</code>, <code>random_state = 42</code>): <b>273 dias</b> para treinar e <b>92</b> para avaliar.</p>
  <p>Como régua de comparação usamos três modelos: a <b>média</b> do treino (o chute mais ingênuo), uma <b>reta</b> (regressão linear) e a <b>MLP</b>. A métrica é o <b>RMSE</b>, o erro típico em kWh no conjunto de teste (menor é melhor).</p>
  <div class="demo" data-demo="mlpenergia"></div>
  <div class="tablewrap"><table>
    <tr><th>Modelo</th><th>RMSE no teste</th></tr>
    <tr><td>Média (chute ingênuo)</td><td>5,90</td></tr>
    <tr><td>Reta (regressão linear)</td><td>5,91</td></tr>
    <tr><td><b>MLP</b> (camada oculta de 8 neurônios, ReLU)</td><td><b>1,54</b></td></tr>
  </table></div>
  <p>Repare que a <b>reta empata com a média</b> (5,91 contra 5,90): como o U é simétrico, a melhor reta é quase horizontal e não explica nada. Já a MLP reduz o erro a cerca de <b>um quarto</b>. Lendo a curva da rede: 34,82 kWh a 10 °C, 22,70 a 16 °C, 18,28 a 23 °C, 23,75 a 30 °C e 34,58 a 36 °C, com o mínimo de <b>17,91 kWh perto de 26,5 °C</b>.</p>
  <div class="nota cuidado"><span class="lbl">Cuidado: extrapolar</span>Os dados de treino vão até 37,8 °C. Perguntar à rede sobre 45 °C é <b>extrapolação</b>: ela devolve um número, mas sem base nenhuma nos dados. Sempre cheque se a entrada está dentro da faixa vista no treino.</div>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Por que 8 neurônios? E por que ReLU? Cada escolha é um experimento.</div><p>Rode os três.</p></div>
</section>

<section class="sec" id="experimentos">
  <h2><span class="sn">2</span>Três experimentos controlados</h2>
  <p class="gancho">Mude uma coisa por vez e meça.</p>
  <div class="demo" data-demo="experimentos"></div>
  <div class="grid2">
    <div class="card rv"><b>A. Número de neurônios</b><p>1 neurônio: 5,91 (uma reta, nada aprendido). 2: 5,85. <b>3: 1,54</b>. 8: 1,54. Com 3 neurônios a rede <b>pode</b> montar o U, mas depende da semente: com outras sementes o treino de 3 neurônios fica preso em RMSE por volta de 4,7 (a semente 1, por exemplo). Com 8 neurônios o resultado é estável, e por isso o código usa 8. Mais neurônios custam mais e arriscam overfitting.</p></div>
    <div class="card rv"><b>B. Função de ativação</b><p>ReLU 1,54; tanh 1,38; logística 1,48; <b>identidade 5,98</b>. Com a identidade a rede vira uma conta linear (Capítulo 1) e volta a falhar. É a prova experimental de que a <b>não linearidade</b> é o que faz a camada oculta valer.</p></div>
    <div class="card rv"><b>C. Taxa de aprendizado</b><p>0,0001: RMSE 4,69 e treinou até o limite de 2000 épocas. 0,001: 2,16 em 625 épocas. <b>0,01: 1,54 em 200</b>. 0,1: 1,56 em 46 épocas. Muito baixa não chega; muito alta acelera mas pode ficar menos precisa.</p></div>
    <div class="card rv"><b>O que o scaler faz</b><p>As entradas (e o alvo, o consumo) são padronizados (média 0, desvio 1) antes da rede. O <code>StandardScaler</code> é ajustado <b>só no treino</b> e depois aplicado ao teste. Ajustar no conjunto inteiro vazaria informação do teste para o treino.</p></div>
  </div>
  <div class="nota exemplo"><span class="lbl">Código da rede</span>
<pre><code><span class="k">from</span> sklearn.neural_network <span class="k">import</span> MLPRegressor
<span class="k">from</span> sklearn.preprocessing <span class="k">import</span> StandardScaler
<span class="k">from</span> sklearn.model_selection <span class="k">import</span> train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=42)
sc = StandardScaler().fit(X_tr)                  <span class="c"># aprende média/desvio só no treino</span>
sy = StandardScaler().fit(y_tr.to_frame())       <span class="c"># o consumo (y) também é padronizado</span>
rede = MLPRegressor(hidden_layer_sizes=(8,),    <span class="c"># 1 camada oculta, 8 neurônios</span>
                    activation="relu",
                    learning_rate_init=0.01,
                    max_iter=2000, random_state=42)
rede.fit(sc.transform(X_tr), sy.transform(y_tr.to_frame()).ravel())
pred = sy.inverse_transform(rede.predict(sc.transform(X_te)).reshape(-1, 1)).ravel()   <span class="c"># volta para kWh</span></code></pre></div>
  <p>Os números acima vêm de um treino real do scikit-learn sobre o mesmo arquivo. Mudar a semente (<code>random_state</code>) ou a versão da biblioteca mexe nos decimais, e com <b>poucos</b> neurônios pode mudar o resultado inteiro (veja o experimento A). Com 8 neurônios, a história se mantém: a reta falha, a camada oculta acerta e a identidade volta a falhar. Estes valores vêm de uma conferência feita com o arquivo real, e não das anotações de aula (complemento).</p>
</section>

<section class="sec" id="xor">
  <h2><span class="sn">3</span>O XOR, finalmente resolvido</h2>
  <p class="gancho">A promessa do Capítulo 3.</p>
  <p>Uma MLP pequena (2 entradas, 2 ou mais neurônios ocultos, 1 saída) aprende o XOR porque a camada oculta <b>transforma o espaço</b>: cada neurônio oculto desenha uma reta, e a saída combina as duas. Treine na demo e acompanhe o erro caindo. Compare com o Perceptron simples do Capítulo 3, que errava 3 ou 4 dos 4 casos para sempre.</p>
  <div class="demo" data-demo="xor"></div>
  <div class="nota lembra"><span class="lbl">Por que funciona</span>Dois neurônios ocultos podem calcular, por exemplo, "pelo menos um" (OR) e "os dois" (AND). A saída então faz "OR e não AND", que é justamente o XOR. A camada oculta cria as <b>características intermediárias</b> que uma reta sozinha não tinha.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Energia x temperatura tem forma de <b>U</b>: uma reta não explica (RMSE 5,91, igual à média 5,90). A MLP chega a <b>1,54</b>.",
    "Divisão: 365 dias, <code>test_size = 0,25</code>, <code>random_state = 42</code> → 273 de treino e 92 de teste. O scaler é ajustado <b>só no treino</b>.",
    "Neurônios: 1 → 5,91; 2 → 5,85; <b>3 → 1,54</b>; 8 → 1,54. Ativação: <b>identidade → 5,98</b> (sem não linearidade, a rede falha).",
    "Taxa de aprendizado: 0,0001 → 4,69 (2000 épocas); 0,001 → 2,16; <b>0,01 → 1,54 (200)</b>; 0,1 → 1,56 (46).",
    "A MLP resolve o <b>XOR</b>: a camada oculta cria características intermediárias. Fora da faixa do treino (45 °C), a rede só <b>extrapola</b>."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Por que a regressão linear teve RMSE quase igual ao da média (5,91 x 5,90) nos dados de energia?", [("a","Porque a reta usou poucos dados."),("b","Porque o RMSE é inválido para retas."),("c","Porque o U é simétrico: a melhor reta fica quase horizontal e não explica a variação.")], "Frio e calor elevam o consumo; uma reta não consegue subir dos dois lados.") + quiz(2, "a", "No experimento B, a ativação identidade deu RMSE 5,98. O que isso mostra?", [("a","Sem não linearidade, a rede inteira equivale a uma conta linear e perde a curva."),("b","Que a identidade é a melhor ativação."),("c","Que o teste está vazado.")], "Linear de linear continua linear: a camada oculta deixa de contribuir.") + quiz(3, "b", "O que significa pedir à rede a previsão para 45 °C se o treino foi até 37,8 °C?", [("a","Uma previsão confiável."),("b","Extrapolação: a rede devolve um número sem respaldo nos dados."),("c","Um erro de sintaxe.")], "Fora da faixa de treino a previsão não tem base. Cheque sempre a faixa das entradas.") + quiz(4, "b", "Por que ajustar o StandardScaler apenas no treino?", [("a","Para economizar memória."),("b","Para não vazar informação do conjunto de teste para o treino."),("c","Porque o teste não pode ser padronizado.")], "A média e o desvio do teste não deveriam ter participado do ajuste.") + flash([
    ("O que é RMSE?", "A raiz do erro quadrático médio: o erro típico, na mesma unidade do alvo (aqui, kWh)."),
    ("Por que a camada oculta resolve o XOR?", "Ela cria características intermediárias (como OR e AND) que a saída combina."),
    ("Quantos parâmetros tem a rede 1-8-1?", "(1×8 + 8) + (8×1 + 1) = 25."),
    ("O que é extrapolar?", "Prever fora da faixa vista no treino. O resultado não tem respaldo nos dados.")]) + ponte("A rede funcionou. Mas o que acontece por dentro quando ela treina?", "Vamos abrir a caixa: backpropagation, com contas que cabem na mão.", "Para onde vamos agora · Capítulo 6") + '''
</section>'''
chapter(PASTA, 5, "mlp", T, "A MLP: camada oculta", "Capítulo 5 · Aula 7",
        "Uma rede com camada oculta resolve o U da energia e o XOR; três experimentos controlados mostram o que importa.",
        ["<b>~50 min</b>", "3 demos · 4 testes · 4 flashcards", "dados reais do scikit-learn"], body5, scripts=S_DATA)

# ---------------- CAP 6 ----------------
body6 = recap("Nos capítulos anteriores o treino foi uma caixa: você apertou o botão e os pesos mudaram. Aqui abrimos a caixa com <b>uma única conta numérica</b>, do começo ao fim. Este capítulo é um complemento: não vem das notas da aula, mas explica o que as aulas assumem.") + '''
<section class="sec" id="exemplo">
  <h2><span class="sn">1</span>Backpropagation com números</h2>
  <p class="gancho">Dois pesos, uma entrada, um passo de ajuste.</p>
  <p>Rede minúscula: uma entrada <code>x</code>, um neurônio oculto com peso <code>w₁</code> e ativação ReLU, e uma saída com peso <code>w₂</code> (linear). Ou seja: <code>h = ReLU(w₁·x)</code> e <code>ŷ = w₂·h</code>. A perda é o erro ao quadrado: <code>L = (ŷ − y)²</code>.</p>
  <div class="ex rv"><span class="t">Exemplo resolvido: um passo completo</span>
    <div class="l"><div><b>Dados:</b> <code>x = 2</code>, <code>y = 3</code> (resposta correta), <code>w₁ = 0,5</code>, <code>w₂ = 1,0</code>, taxa <code>η = 0,1</code>.</div></div>
    <div class="l"><div><b>Passada para frente:</b> <code>z = w₁·x = 1</code>; <code>h = ReLU(1) = 1</code>; <code>ŷ = w₂·h = 1</code>; <code>L = (1 − 3)² = <b>4</b></code>.</div></div>
    <div class="l"><div><b>Passada para trás</b> (regra da cadeia, da saída para a entrada): <code>dL/dŷ = 2(ŷ − y) = −4</code>.</div></div>
    <div class="l"><div><code>dL/dw₂ = dL/dŷ · h = −4 · 1 = <b>−4</b></code>. <code>dL/dh = dL/dŷ · w₂ = −4</code>.</div></div>
    <div class="l"><div>A ReLU deixa passar o gradiente (z &gt; 0, derivada 1). <code>dL/dw₁ = dL/dh · x = −4 · 2 = <b>−8</b></code>.</div></div>
    <div class="l"><div><b>Atualização</b> (<code>w ← w − η · gradiente</code>): <code>w₁ = 0,5 − 0,1·(−8) = <b>1,3</b></code>; <code>w₂ = 1,0 − 0,1·(−4) = <b>1,4</b></code>.</div></div>
    <div class="l"><div><b>Conferindo:</b> <code>h = 1,3·2 = 2,6</code>; <code>ŷ = 1,4·2,6 = 3,64</code>; <code>L = (3,64 − 3)² = <b>0,4096</b></code>. A perda caiu de 4 para 0,41 em <b>um</b> passo.</div></div>
  </div>
  <p>Os gradientes são negativos (o erro diminui quando o peso <b>aumenta</b>), por isso o sinal de menos da fórmula os transforma em soma. Numa rede real é a mesma conta, repetida para milhões de pesos, em lotes de exemplos, com o auxílio de bibliotecas que calculam as derivadas automaticamente.</p>
  <div class="ponte rv"><div class="t">Para onde vamos agora</div><div class="q">Usamos o erro ao quadrado. Existem outros? E como organizar milhares de passos?</div><p>Perdas, épocas e otimizadores.</p></div>
</section>

<section class="sec" id="perdas">
  <h2><span class="sn">2</span>Funções de perda</h2>
  <p class="gancho">A perda define o que significa "errar".</p>
  <div class="tablewrap"><table>
    <tr><th>Perda</th><th>Para quê</th><th>Ideia</th></tr>
    <tr><td><b>MSE</b> (erro quadrático médio)</td><td>regressão</td><td>penaliza erros grandes mais que proporcionalmente</td></tr>
    <tr><td><b>MAE</b> (erro absoluto médio)</td><td>regressão</td><td>menos sensível a valores extremos</td></tr>
    <tr><td><b>Entropia cruzada binária</b></td><td>classificação em 2 classes (sigmoide)</td><td>pune forte quem está confiante e errado</td></tr>
    <tr><td><b>Entropia cruzada categórica</b></td><td>várias classes (softmax)</td><td>mede o quão longe a distribuição está da certa</td></tr>
  </table></div>
  <p>O RMSE do Capítulo 5 é só a raiz do MSE, para voltar à unidade original (kWh).</p>
</section>

<section class="sec" id="treino-pratica">
  <h2><span class="sn">3</span>Épocas, lotes e otimizadores</h2>
  <p class="gancho">Como milhares de passos viram um treino.</p>
  <ul>
    <li><b>Época</b>: uma passada completa por todos os exemplos de treino.</li>
    <li><b>Lote</b> (<i>batch</i>): o grupo de exemplos usado para calcular um passo. Em um exemplo hipotético com 273 exemplos e lote de 32 (o <code>MLPRegressor</code> usa por padrão lotes de até 200), uma época tem 9 passos (8 de 32 e 1 de 17).</li>
    <li><b>SGD</b> (gradiente descendente estocástico): atualiza com o gradiente de cada lote. Simples, mas sensível à taxa de aprendizado.</li>
    <li><b>Adam</b>: ajusta o passo de cada peso com base no histórico dos gradientes. É o padrão em muitos projetos e é o otimizador padrão do <code>MLPRegressor</code> do scikit-learn.</li>
  </ul>
  <h3>Como evitar o overfitting na prática</h3>
  <ul>
    <li><b>Regularização L2</b>: acrescenta à perda uma penalidade pelo tamanho dos pesos (no scikit-learn, o parâmetro <code>alpha</code>).</li>
    <li><b>Dropout</b>: desliga neurônios ao acaso durante o treino.</li>
    <li><b>Early stopping</b>: acompanhar a perda numa parte reservada dos dados (validação) e parar quando ela volta a subir.</li>
    <li><b>Mais dados</b>, de qualidade e variados.</li>
  </ul>
  <div class="nota lembra"><span class="lbl">Três conjuntos</span>Treino ajusta os pesos. <b>Validação</b> ajuda a escolher hiperparâmetros e a hora de parar. <b>Teste</b> só é usado uma vez, no fim, para estimar o desempenho real.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">4</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>Backpropagation</b> = regra da cadeia da saída para a entrada, para saber quanto cada peso contribuiu para a perda.",
    "No exemplo: <code>L = 4</code> → gradientes −8 e −4 → pesos 1,3 e 1,4 → <code>ŷ = 3,64</code> → <code>L = 0,4096</code>.",
    "<b>Perda</b>: MSE/MAE na regressão; entropia cruzada na classificação.",
    "<b>Época</b> = passada completa; <b>lote</b> = grupo por passo. <b>Adam</b> e <b>SGD</b> são otimizadores.",
    "Contra o overfitting: regularização, dropout, early stopping, mais dados. Teste só no fim."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "a", "No exemplo, dL/dw₁ = −8. Com η = 0,1, qual o novo w₁ (partindo de 0,5)?", [("a","1,3."),("b","0,3."),("c","−0,3.")], "w₁ − η·gradiente = 0,5 − 0,1·(−8) = 1,3. Gradiente negativo aumenta o peso.") + quiz(2, "c", "Qual perda é adequada para prever um valor contínuo, como preço?", [("a","Entropia cruzada categórica."),("b","Entropia cruzada binária."),("c","MSE ou MAE.")], "Regressão usa perdas de distância; as entropias cruzadas são para probabilidades.") + quiz(3, "b", "O que é early stopping?", [("a","Treinar com menos neurônios."),("b","Parar o treino quando o erro de validação deixa de melhorar."),("c","Descartar o conjunto de teste.")], "A partir de certo ponto a rede só memoriza o treino; parar antes ajuda a generalizar.") + flash([
    ("O que o backpropagation calcula?", "O gradiente da perda em relação a cada peso, propagando o erro da saída para a entrada."),
    ("O que é um lote?", "O grupo de exemplos usado para calcular um passo de atualização."),
    ("O que faz o Adam?", "Adapta o tamanho do passo de cada peso usando o histórico dos gradientes."),
    ("Para que serve a validação?", "Escolher hiperparâmetros e decidir quando parar, sem tocar no teste.")]) + ponte("Uma camada oculta basta para tabelas. E para imagens, texto e voz?", "É aí que entram as redes profundas.", "Para onde vamos agora · Capítulo 7") + '''
</section>'''
chapter(PASTA, 6, "por-dentro-do-treino", T, "Por dentro do treino (complemento)", "Capítulo 6 · Complemento",
        "Backpropagation em um exemplo numérico, perdas, épocas, otimizadores e regularização.",
        ["<b>~40 min</b>", "0 demos · 3 testes · 4 flashcards", "uma conta completa à mão"], body6, scripts=S)

# ---------------- CAP 7 ----------------
body7 = recap("A MLP do Capítulo 5 ligava <b>todos</b> os neurônios a <b>todos</b> os da camada seguinte, e tratava as entradas como uma lista sem ordem. Imagens, texto e voz têm <b>estrutura</b> (vizinhança, sequência). As arquiteturas deste capítulo, também um complemento, usam essa estrutura.") + '''
<section class="sec" id="cnn">
  <h2><span class="sn">1</span>Convolução: olhar para vizinhanças</h2>
  <p class="gancho">Um filtro pequeno que desliza pela imagem.</p>
  <p>Uma <b>rede convolucional</b> (CNN) usa <b>filtros</b> pequenos (por exemplo 3×3) que deslizam pela imagem. Em cada posição, multiplica-se o filtro pelos pixels vizinhos e soma-se, produzindo um mapa que destaca um padrão (uma borda vertical, uma textura). O <b>mesmo</b> filtro é reaproveitado em toda a imagem, o que reduz muito o número de pesos em comparação a uma MLP. Experimente os filtros:</p>
  <div class="demo" data-demo="conv"></div>
  <p>Nas primeiras camadas os filtros detectam bordas e texturas. Nas seguintes, combinações dessas (cantos, olhos, rodas), e nas últimas, objetos inteiros. É a ideia de <i>features hierárquicas</i> do Capítulo 2, agora automática. As camadas de <b>pooling</b> reduzem o tamanho dos mapas, guardando o que mais importa.</p>
</section>

<section class="sec" id="sequencias">
  <h2><span class="sn">2</span>Sequências: RNN, LSTM e Transformers</h2>
  <p class="gancho">Quando a ordem importa.</p>
  <div class="grid2">
    <div class="card rv"><b>RNN e LSTM</b><p>Redes recorrentes processam um item por vez e carregam uma "memória" do que viram. A LSTM acrescenta portas que decidem o que lembrar e o que esquecer, e foi dominante em tradução e voz por anos.</p></div>
    <div class="card rv"><b>Transformers</b><p>Introduzidos em 2017 (artigo <i>Attention Is All You Need</i>), usam <b>atenção</b>: cada palavra pode "olhar" diretamente para todas as outras da frase, em paralelo. Estão na base dos grandes modelos de linguagem.</p></div>
  </div>
</section>

<section class="sec" id="prontos">
  <h2><span class="sn">3</span>Não comece do zero: transfer learning e frameworks</h2>
  <p class="gancho">Treinar uma rede grande custa caro. Reaproveitar custa pouco.</p>
  <p><b>Transfer learning</b> é partir de uma rede já treinada em milhões de exemplos (como a MobileNet, para imagens) e ajustar apenas as últimas camadas ao seu problema. Foi o que o Teachable Machine do Capítulo 2 fez. Vantagens: precisa de muito menos dados e tempo. Desvantagem: herda os vieses do modelo original.</p>
  <div class="tablewrap"><table>
    <tr><th>Framework</th><th>Origem</th><th>Nota</th></tr>
    <tr><td><b>TensorFlow</b></td><td>Google, 2015</td><td>muito usado em produção; <b>Keras</b> é sua interface de alto nível</td></tr>
    <tr><td><b>PyTorch</b></td><td>Meta, 2016</td><td>muito usado em pesquisa, estilo mais "Python puro"</td></tr>
    <tr><td><b>scikit-learn</b></td><td>2007</td><td>MLPs simples e todo o resto do ML clássico (usado no Capítulo 5)</td></tr>
    <tr><td><b>JAX</b></td><td>Google, 2018</td><td>derivadas automáticas e compilação rápida</td></tr>
  </table></div>
</section>

<section class="sec" id="riscos">
  <h2><span class="sn">4</span>Riscos de levar um modelo à produção</h2>
  <p class="gancho">Acertar no notebook não é o mesmo que ser confiável no mundo.</p>
  <ul>
    <li><b>Viés nos dados</b>: se o treino não representa todos os públicos, o modelo erra mais com quem ficou de fora.</li>
    <li><b>Explicabilidade</b>: redes são pouco transparentes. Técnicas como <b>SHAP</b> e <b>LIME</b> estimam o que pesou em cada previsão.</li>
    <li><b>Deriva (drift)</b>: o mundo muda e o desempenho cai com o tempo. É preciso monitorar.</li>
    <li><b>Privacidade e lei</b>: no Brasil, a LGPD (art. 20) dá ao titular o direito de pedir <b>revisão de decisões tomadas unicamente por tratamento automatizado</b>.</li>
    <li><b>Segurança</b>: modelos serializados (<code>.pkl</code>) podem executar código ao carregar.</li>
  </ul>
  <div class="nota lembra"><span class="lbl">Cinco perguntas antes de treinar</span>(1) Qual decisão o modelo vai influenciar? (2) Os dados representam quem será afetado? (3) Como saber que ele errou, e quanto custa o erro? (4) Alguém consegue revisar uma decisão contestada? (5) Quando e como o modelo será reavaliado?</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "<b>CNN</b>: filtros pequenos deslizam pela imagem e são reaproveitados, detectando bordas, texturas e depois formas.",
    "<b>RNN/LSTM</b> processam sequências com memória. <b>Transformers</b> (2017) usam atenção e dominam a linguagem.",
    "<b>Transfer learning</b> reaproveita uma rede pré-treinada: menos dados e tempo, mas herda vieses.",
    "Frameworks: TensorFlow/Keras, PyTorch, scikit-learn, JAX.",
    "Em produção: viés, explicabilidade (SHAP/LIME), drift, LGPD art. 20 e segurança de arquivos de modelo."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "b", "Por que uma CNN usa muito menos pesos que uma MLP para imagens?", [("a","Porque ignora os pixels."),("b","Porque reaproveita o mesmo filtro pequeno em toda a imagem."),("c","Porque só olha o centro.")], "O compartilhamento de pesos do filtro é o que reduz os parâmetros.") + quiz(2, "c", "O que é transfer learning?", [("a","Treinar do zero com mais dados."),("b","Copiar o conjunto de teste."),("c","Reaproveitar uma rede pré-treinada e ajustar as últimas camadas.")], "Menos dados e tempo; cuidado com os vieses herdados.") + quiz(3, "a", "O que a LGPD (art. 20) garante em decisões automatizadas?", [("a","O direito de pedir revisão de decisões tomadas unicamente por tratamento automatizado."),("b","Que todo modelo seja de código aberto."),("c","Que ninguém use redes neurais.")], "É um direito do titular dos dados; vale conferir o texto da lei no caso concreto.") + flash([
    ("O que é um filtro convolucional?", "Uma pequena matriz que desliza pela imagem e realça um padrão local."),
    ("O que é atenção?", "O mecanismo em que cada elemento da sequência pondera os demais para construir sua representação."),
    ("O que é drift?", "Mudança dos dados do mundo real ao longo do tempo, que degrada o modelo."),
    ("Para que servem SHAP e LIME?", "Para estimar quais variáveis pesaram em uma previsão.")]) + ponte("Todas essas redes aprendem por gradiente. Existe um jeito de otimizar sem ele?", "Existe: inspirar-se na evolução.", "Para onde vamos agora · Capítulo 8") + '''
</section>'''
chapter(PASTA, 7, "deep-learning", T, "Deep Learning e arquiteturas (complemento)", "Capítulo 7 · Complemento",
        "Convolução, sequências, transfer learning, frameworks e os riscos de produção.",
        ["<b>~40 min</b>", "1 demo · 3 testes · 4 flashcards", "filtros convolucionais ao vivo"], body7, scripts=S)

# ---------------- CAP 8 ----------------
body8 = recap("Tudo até aqui ajustava pesos descendo um gradiente. Mas há problemas sem derivada útil, como escolher uma rota, uma escala de horários ou um desenho de peça. Este capítulo, o último e também um complemento, mostra um jeito diferente de otimizar: <b>imitar a evolução</b>.") + '''
<section class="sec" id="ideia">
  <h2><span class="sn">1</span>A ideia</h2>
  <p class="gancho">Gerar muitas soluções, deixar as melhores se reproduzirem.</p>
  <p>Um <b>algoritmo genético</b> mantém uma <b>população</b> de soluções candidatas e repete ciclos de seleção e variação:</p>
  <ol>
    <li><b>Avaliar</b> cada indivíduo com uma função de <b>aptidão</b> (<i>fitness</i>): quão boa é essa solução?</li>
    <li><b>Selecionar</b> os mais aptos como pais (torneio, roleta...).</li>
    <li><b>Cruzar</b> (<i>crossover</i>): misturar partes de dois pais para formar filhos.</li>
    <li><b>Mutar</b>: alterar aleatoriamente uma pequena parte, para manter a diversidade.</li>
    <li><b>Elitismo</b> (opcional): manter os melhores intactos para não perdê-los.</li>
    <li>Repetir por várias <b>gerações</b>.</li>
  </ol>
  <div class="demo" data-demo="genetico"></div>
  <p>Na demo, cada indivíduo é uma frase de letras sorteadas e a aptidão é quantas letras coincidem com o alvo. Só os 20% melhores da população viram pais, o filho pega o começo de um pai e o fim do outro (cruzamento de um ponto) e cada letra pode mudar ao acaso (mutação). Mude a taxa de mutação e o tamanho da população e observe: <b>sem mutação</b>, a população fica presa sem novidade; <b>mutação muito alta</b> faz a busca virar quase aleatória (o efeito aparece melhor com um alvo longo).</p>
</section>

<section class="sec" id="vs">
  <h2><span class="sn">2</span>Gradiente x algoritmo genético</h2>
  <p class="gancho">Cada um para um tipo de problema.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>Gradiente (redes neurais)</th><th>Algoritmo genético</th></tr>
    <tr><td>Precisa de derivada?</td><td>sim</td><td>não: só precisa avaliar a aptidão</td></tr>
    <tr><td>Tipo de problema</td><td>funções suaves, muitos parâmetros</td><td>combinatórios, descontínuos, de desenho</td></tr>
    <tr><td>Custo</td><td>um passo barato, milhões de passos</td><td>muitas avaliações por geração</td></tr>
    <tr><td>Garantia</td><td>mínimo local</td><td>nenhuma: boa solução, não necessariamente a melhor</td></tr>
  </table></div>
  <div class="ex rv"><span class="t">Um caso conhecido</span>
    <div class="l"><div>A NASA usou algoritmos evolutivos para projetar a antena da missão Space Technology 5 (lançada em 2006). O formato, torto e pouco intuitivo para um engenheiro, foi encontrado pela busca e atendia aos requisitos da missão.</div></div>
  </div>
  <p>Outros usos: rotas e escalas de trabalho, alocação de recursos, ajuste de hiperparâmetros e até a estrutura de redes neurais (neuroevolução). Uma dica prática: se o seu problema tem derivadas e muitos dados, comece pelo gradiente; se é um quebra-cabeça de escolhas discretas, considere um algoritmo genético ou outra heurística.</p>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">3</span>Fechamento do capítulo</h2>
  ''' + resumo([
    "Algoritmo genético: <b>população → aptidão → seleção → cruzamento → mutação → nova geração</b>.",
    "<b>Mutação</b> mantém a diversidade; <b>elitismo</b> preserva os melhores.",
    "Não precisa de derivada: serve para problemas combinatórios e de desenho.",
    "Não garante o ótimo, só boas soluções. Redes neurais usam gradiente; algoritmos genéticos, evolução."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", "Qual a função da mutação em um algoritmo genético?", [("a","Calcular a aptidão."),("b","Escolher os pais."),("c","Manter a diversidade, introduzindo pequenas alterações aleatórias.")], "Sem mutação a população tende a ficar presa em soluções parecidas.") + quiz(2, "a", "Para qual problema um algoritmo genético é mais natural que o gradiente?", [("a","Escolher uma sequência de rotas, onde não há derivada."),("b","Ajustar os pesos de uma MLP suave."),("c","Calcular uma média.")], "Quando só dá para avaliar a qualidade de uma solução completa, a busca evolutiva funciona.") + flash([
    ("O que é aptidão (fitness)?", "Uma nota que diz o quão boa é uma solução candidata."),
    ("O que é cruzamento?", "Combinar partes de dois pais para gerar filhos."),
    ("O que é elitismo?", "Copiar os melhores indivíduos intactos para a próxima geração."),
    ("O algoritmo genético garante o ótimo?", "Não: costuma achar boas soluções, sem garantia.")]) + '''
  <div class="ponte rv"><div class="t">Fim da apostila</div><div class="q">Do neurônio à evolução.</div><p>Se algum ponto ficou solto, volte ao capítulo correspondente e refaça a demo. A repetição ativa é o que fixa.</p></div>
</section>'''
chapter(PASTA, 8, "algoritmos-geneticos", T, "Algoritmos Genéticos (complemento)", "Capítulo 8 · Complemento",
        "Seleção, cruzamento e mutação: otimizar sem gradiente.",
        ["<b>~40 min</b>", "1 demo · 2 testes · 4 flashcards", "evolua uma população"], body8, scripts=S)
print("rn caps 4-8 ok")
