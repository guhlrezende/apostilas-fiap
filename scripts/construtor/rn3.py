import os, sys, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bld import *
import rn
PASTA, T = rn.PASTA, rn.T
S_COMPRA = ["rn-compra-data.js", "demos/rn-compra.js"]

# Os números do capítulo vêm do arquivo gerado pelo scikit-learn (scripts/gerar_dados_rn_compra.py), nunca digitados à mão.
_raw = open(REPO + PASTA + "/rn-compra-data.js", encoding="utf-8").read()
D = json.loads(_raw[_raw.index("window.RNCOMPRA = ") + len("window.RNCOMPRA = "):].rstrip().rstrip(";"))

def c3(v): return f"{v:.3f}".replace(".", ",")
def c1(v): return f"{v:.1f}".replace(".", ",")
def pc(v): return f"{v * 100:.1f}".replace(".", ",") + "%"
def sig(z): return 1 / (1 + math.exp(-z))

nt = D["n_teste"]
acertos_regua, acertos_reta, acertos_mlp = round(D["regua"] * nt), round(D["acc_reta"] * nt), round(D["acc_mlp"] * nt)
pn = {(p["tempo"], p["desconto"]): p["prob"] for p in D["novos"]}
A, B, A3 = D["exp"]["A"], D["exp"]["B"], D["exp"]["A3_sementes"]
assert D["n_parametros"] == (2 * 8) + 8 + (8 * 1) + 1

body9 = recap("No Capítulo 5 a MLP previu um <b>número</b> (os kWh de um prédio) e uma reta falhou porque o consumo fazia um U. Agora a pergunta muda: <b>sim ou não</b>. Uma loja virtual quer saber se cada visitante vai comprar. A receita é a mesma (padronizar as entradas, uma camada oculta com ReLU, treinar), mas mudam a <b>saída</b>, a <b>métrica</b> e um detalhe da divisão dos dados.") + f'''
<section class="sec" id="problema">
  <h2><span class="sn">1</span>O problema: quem compra fica na faixa do meio</h2>
  <p class="gancho">Quem sai em um minuto não compra, quem se perde no site também não: compra quem fica o tempo certo.</p>
  <p>A tabela tem <b>{D["n"]} visitantes</b> com três colunas: <code>tempo_no_site</code> (de 0 a 20 minutos), <code>desconto</code> (de 0 a 20% de cupom) e <code>comprou</code> (1 ou 0). Os dados são <b>gerados por computador</b> com uma regra escondida (o próprio notebook da aula sorteia os visitantes), não são clientes de uma loja real. Compraram <b>{pc(D["pct_compra"])}</b>.</p>
  <p>A divisão é a mesma do Capítulo 5, com um acréscimo: <code>test_size = 0,25</code>, <code>random_state = 42</code> e <code>stratify = y</code>. Sobram <b>{D["n_treino"]} visitantes</b> para treinar e <b>{D["n_teste"]}</b> para testar. A régua de comparação é o chute mais preguiçoso, <b>"ninguém compra"</b>, que acerta <b>{c3(D["regua"])}</b> no teste. Qualquer modelo precisa passar disso para valer alguma coisa.</p>
  <div class="demo" data-demo="mlpcompra"></div>
  <div class="ex rv"><span class="t">Exemplo resolvido: o que a acurácia diz em pessoas</span>
    <div class="l"><div>Acurácia é a fração de acertos. No teste são <b>{nt}</b> visitantes. Chutar "ninguém compra": {c3(D["regua"])} × {nt} = <b>{acertos_regua}</b> acertos.</div></div>
    <div class="l"><div>A reta: {c3(D["acc_reta"])} × {nt} = <b>{acertos_reta}</b> acertos, ou seja, <b>só {acertos_reta - acertos_regua} a mais</b> que o chute. A MLP: {c3(D["acc_mlp"])} × {nt} = <b>{acertos_mlp}</b> acertos, <b>{acertos_mlp - acertos_regua} a mais</b> que o chute.</div></div>
    <div class="l"><div>Leitura: {c3(D["acc_mlp"])} só parece boa porque a régua é {c3(D["regua"])}. Sempre compare a acurácia com o que o chute ingênuo já entrega.</div></div>
  </div>
  <p>Repare que a reta (<b>{c3(D["acc_reta"])}</b>) empata com o chute. É a mesma história do U da energia: quem compra está numa <b>faixa</b> de tempo, e uma reta só consegue separar "de um lado" e "do outro". Ligue a opção "reta" na demo e veja que a linha tracejada corta a faixa em vez de desenhá-la. A MLP, com a camada oculta, desenha a faixa curva.</p>
  <div class="nota cuidado"><span class="lbl">Fonte e limite</span>Este capítulo foi montado a partir do notebook da Aula 9, com os números recalculados com o scikit-learn {D["versao_sklearn"]}. A parte teórica falada em aula não foi registrada: confira com o slide da professora quando ele estiver disponível. Os dados são inventados, então as conclusões de negócio abaixo servem para aprender o método, não para decidir um cupom de verdade.</div>
  {ponte("Se a receita é a mesma, o que exatamente mudou em relação à regressão?", "A saída da rede, a métrica e uma opção na divisão dos dados. Vamos ponto a ponto.")}
</section>

<section class="sec" id="classificacao">
  <h2><span class="sn">2</span>O que muda da regressão para a classificação</h2>
  <p class="gancho">A rede por dentro é igual. O que mudou foi a pergunta que fazemos a ela.</p>
  <div class="tablewrap"><table>
    <tr><th></th><th>Cap. 5 (energia)</th><th>Cap. 9 (compra)</th></tr>
    <tr><td>Pergunta</td><td>quantos kWh?</td><td>vai comprar? (1 ou 0)</td></tr>
    <tr><td>Entradas</td><td>1 (<code>temperatura</code>)</td><td>2 (<code>tempo_no_site</code>, <code>desconto</code>)</td></tr>
    <tr><td>Reta de comparação</td><td><code>LinearRegression</code></td><td><code>LogisticRegression</code></td></tr>
    <tr><td>Rede</td><td><code>MLPRegressor</code>, saída <code>identity</code></td><td><code>MLPClassifier</code>, saída <code>{D["saida"]}</code> (sigmoide)</td></tr>
    <tr><td>Métrica</td><td>RMSE (em kWh)</td><td><b>acurácia</b> (<code>.score</code>)</td></tr>
    <tr><td>Alvo padronizado?</td><td>sim</td><td><b>não</b>: só as entradas</td></tr>
    <tr><td>Resposta de negócio</td><td><code>.predict</code></td><td><code>.predict_proba(...)[:, 1]</code></td></tr>
  </table></div>
  <h3>Intuição, definição e exemplo</h3>
  <p><b>Intuição.</b> Na regressão, a última camada devolve qualquer número. Na classificação queremos algo que se leia como <b>chance</b>, entre 0 e 1. A função <b>sigmoide</b> faz isso: espreme qualquer valor para dentro desse intervalo.</p>
  <p><b>Definição.</b> A sigmoide é <code>σ(z) = 1 / (1 + e<sup>−z</sup>)</code>. A saída da rede é a probabilidade de a classe ser <b>1</b> (comprou). Para decidir, usa-se um corte em <b>0,5</b>: acima disso a rede responde 1, abaixo responde 0. O <code>predict_proba</code> devolve duas colunas (chance de 0 e chance de 1), e o <code>[:, 1]</code> pega a segunda, a de comprar.</p>
  <div class="ex rv"><span class="t">Exemplo resolvido: a sigmoide e a contagem de parâmetros</span>
    <div class="l"><div><code>z = 0</code> dá <code>σ = {sig(0):.3f}</code>. <code>z = 2</code> dá <b>{sig(2):.3f}</b>. <code>z = −2</code> dá <b>{sig(-2):.3f}</b>. <code>z = 5</code> dá <b>{sig(5):.3f}</b>. Quanto maior o <code>z</code>, mais perto de 1; quanto menor, mais perto de 0.</div></div>
    <div class="l"><div>Parâmetros da rede 2-8-1: pesos da entrada para a camada oculta (2 × 8 = 16), biases da camada oculta (8), pesos da oculta para a saída (8 × 1 = 8) e bias da saída (1). Total: <b>16 + 8 + 8 + 1 = {D["n_parametros"]}</b>.</div></div>
  </div>
  <p><b>Código comentado.</b> O treino leva <b>{D["epocas"]} épocas</b> até convergir:</p>
  <div class="nota exemplo"><span class="lbl">Código da rede</span>
<pre><code><span class="k">from</span> sklearn.neural_network <span class="k">import</span> MLPClassifier
<span class="k">from</span> sklearn.model_selection <span class="k">import</span> train_test_split
<span class="k">from</span> sklearn.preprocessing <span class="k">import</span> StandardScaler

X = dados[[<span class="s">"tempo_no_site"</span>, <span class="s">"desconto"</span>]]            <span class="c"># colchetes duplos: uma tabela com 2 colunas</span>
y = dados[<span class="s">"comprou"</span>]
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)   <span class="c"># stratify: mesma proporção de quem compra nos dois lados</span>
esc = StandardScaler()
X_tr_e = esc.fit_transform(X_tr)                          <span class="c"># aprende média e desvio SÓ no treino</span>
X_te_e = esc.transform(X_te)                              <span class="c"># o teste só recebe a conta pronta</span>

rede = MLPClassifier(hidden_layer_sizes=(8,), activation=<span class="s">"relu"</span>,
                     max_iter=1000, random_state=42)       <span class="c"># 1 camada oculta, 8 neurônios</span>
rede.fit(X_tr_e, y_tr)
acc = rede.score(X_te_e, y_te)                            <span class="c"># acurácia no teste</span>
prob = rede.predict_proba(esc.transform(novos))[:, 1]     <span class="c"># chance de comprar, de 0 a 1</span></code></pre></div>
  <h3>Os dois detalhes que costumam passar batido</h3>
  <div class="grid2">
    <div class="card rv"><b>stratify = y</b><p>Sem ele, o sorteio pode deixar mais compradores de um lado do que do outro. Com ele, a proporção fica a mesma: <b>{pc(D["pct_compra_treino"])}</b> no treino e <b>{pc(D["pct_compra_teste"])}</b> no teste. Importa mais quando a classe de interesse é rara.</p></div>
    <div class="card rv"><b>O alvo não é padronizado</b><p>Na regressão padronizamos também o consumo. Aqui o alvo é 0 ou 1, uma categoria, e deve continuar assim. Só as <b>entradas</b> passam pelo <code>StandardScaler</code>.</p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Erros comuns</span>(1) Chamar <code>.fit</code> no scaler com o teste: o <code>.fit</code> devolve o próprio scaler, não os dados, e a próxima célula quebra. No teste use sempre <code>.transform</code>. (2) Esquecer de padronizar os visitantes novos antes do <code>predict_proba</code>: a rede só entende a escala do treino. (3) Comemorar uma acurácia sem olhar a régua.</div>
  <div class="nota lembra"><span class="lbl">Complemento, não foi dado em aula</span>Por baixo dos panos, o <code>MLPClassifier</code> mede o erro com a <b>entropia cruzada</b> e não com o erro quadrático da regressão. A ideia é a mesma (o erro cai a cada época), mas a conta do erro é adequada a probabilidades.</div>
  {ponte("A rede de 8 neurônios acertou. Mas por que 8, e por que ReLU?", "Cada escolha é um experimento, como no Capítulo 5.")}
</section>

<section class="sec" id="experimentos">
  <h2><span class="sn">3</span>Os experimentos: neurônios e ativação</h2>
  <p class="gancho">Mude uma coisa por vez e meça.</p>
  <div class="demo" data-demo="expcompra"></div>
  <div class="grid2">
    <div class="card rv"><b>A. Poucos neurônios não bastam</b><p>Com 1, 2 e 3 neurônios (semente 42) a acurácia fica em {c3(A["1"])}, {c3(A["2"])} e {c3(A["3"])}, perto da régua de {c3(D["regua"])}: a rede não achou a faixa. Com <b>8</b> sobe para <b>{c3(A["8"])}</b>. Mas não é uma regra fixa de "3 não serve": com 3 neurônios e as sementes 0, 1 e 7 a rede <b>consegue</b> ({c3(A3["0"])}, {c3(A3["1"])} e {c3(A3["7"])}). Poucos neurônios dão menos capacidade e mais dependência do sorteio inicial dos pesos.</p></div>
    <div class="card rv"><b>B. A ativação precisa ser não linear</b><p>ReLU {c3(B["relu"])}, tanh {c3(B["tanh"])}, logística {c3(B["logistic"])} ficam todas perto de {c3(B["relu"])}. Já a <b>identidade</b> cai para <b>{c3(B["identity"])}</b>, o mesmo patamar da reta ({c3(D["acc_reta"])}). Sem não linearidade, camadas empilhadas valem uma conta linear só. É a mesma prova do Capítulo 5, agora na classificação.</p></div>
  </div>
  <div class="nota lembra"><span class="lbl">Complemento, não foi dado em aula</span>Compare com o Capítulo 5: lá, 3 neurônios já desenhavam o U em uma dimensão. Aqui, com duas entradas, desenhar uma faixa pede mais neurônios (ou mais sorte na semente). Quanto mais complexa a forma, mais capacidade a rede precisa.</div>
  <p>Os valores vêm de uma execução real do scikit-learn {D["versao_sklearn"]}. Outra versão da biblioteca ou outra semente mexe nos decimais, principalmente com poucos neurônios.</p>
</section>

<section class="sec" id="negocio">
  <h2><span class="sn">4</span>Da probabilidade à decisão de negócio</h2>
  <p class="gancho">O modelo não diz "vai comprar". Diz "tem tanta chance de comprar", e a decisão é nossa.</p>
  <p>Depois de treinar, a loja pergunta sobre visitantes novos. Cada linha é padronizada com o mesmo scaler do treino e passa pelo <code>predict_proba</code>:</p>
  <div class="tablewrap"><table>
    <tr><th>tempo no site</th><th>desconto</th><th class="n">chance de compra</th></tr>
''' + "".join(f'    <tr><td>{p["tempo"]} min</td><td>{p["desconto"]}%</td><td class="n"><b>{c3(p["prob"])}</b></td></tr>\n' for p in D["novos"]) + f'''  </table></div>
  <div class="grid2">
    <div class="card rv"><b>10 minutos, desconto de 0, 10 e 20%</b><p>A chance vai de <b>{c3(pn[(10,0)])}</b> para <b>{c3(pn[(10,10)])}</b> e para <b>{c3(pn[(10,20)])}</b>. O primeiro salto, de 0 para 10%, é de {c1((pn[(10,10)] - pn[(10,0)]) * 100)} pontos percentuais. O segundo, de 10 para 20%, só de {c1((pn[(10,20)] - pn[(10,10)]) * 100)}. <i>Leitura de negócio (complemento): vale comparar esse ganho pequeno com o custo do cupom maior.</i></p></div>
    <div class="card rv"><b>1 minuto e 19 minutos</b><p>Com 10% de desconto, quem fica 1 minuto tem chance de <b>{c3(pn[(1,10)])}</b>, e quem fica 19 minutos, <b>{c3(pn[(19,10)])}</b>. O cupom não resolve nenhum dos dois casos. <i>Hipótese (complemento): quem sai rápido nem olha a oferta; quem passa muito tempo pode estar perdido ou comparando preço em outro lugar.</i></p></div>
  </div>
  <div class="nota cuidado"><span class="lbl">Cuidado: dados inventados</span>Esses visitantes foram sorteados por uma regra que conhecemos. Em dados reais a faixa do meio não é garantida, e o desempenho tende a ser menor. O método é o que se aproveita.</div>
</section>

<section class="sec" id="fechamento">
  <h2><span class="sn">5</span>Fechamento do capítulo</h2>
  ''' + resumo([
    f"Classificação: a resposta é <b>sim ou não</b>. A saída da rede é a <b>sigmoide</b>, uma chance entre 0 e 1; o <code>predict_proba(...)[:, 1]</code> devolve a chance de comprar.",
    f"Divisão: {D['n']} visitantes, <code>test_size = 0,25</code>, <code>random_state = 42</code>, <code>stratify = y</code> → {D['n_treino']} de treino e {D['n_teste']} de teste. Só as <b>entradas</b> são padronizadas, e o scaler é ajustado só no treino.",
    f"Régua (chutar \"ninguém compra\"): <b>{c3(D['regua'])}</b>. Reta: <b>{c3(D['acc_reta'])}</b>, empate com a régua. MLP de 8 neurônios ReLU: <b>{c3(D['acc_mlp'])}</b>, em {D['epocas']} épocas.",
    f"Parâmetros da rede 2-8-1: 16 + 8 + 8 + 1 = <b>{D['n_parametros']}</b>.",
    f"Neurônios: 1 → {c3(A['1'])}; 2 → {c3(A['2'])}; 3 → {c3(A['3'])}; <b>8 → {c3(A['8'])}</b>. Ativação: relu {c3(B['relu'])}, tanh {c3(B['tanh'])}, logistic {c3(B['logistic'])}, <b>identity → {c3(B['identity'])}</b> (sem não linearidade, a rede vira uma reta).",
    "Acurácia só faz sentido ao lado da <b>régua</b>. O modelo entrega probabilidade; a decisão de negócio usa essa probabilidade."]) + '''
  <h3>Teste rápido</h3>
  ''' + quiz(1, "c", f"Por que a reta (regressão logística) ficou com acurácia {c3(D['acc_reta'])}, praticamente igual ao chute \"ninguém compra\"?", [("a", "Porque a reta usou poucos visitantes."), ("b", "Porque a acurácia não funciona com retas."), ("c", "Porque quem compra está numa faixa do meio, e uma reta só separa um lado do outro.")], "Comprar depende de um tempo \"médio\". Uma reta não desenha uma faixa; a camada oculta com ReLU desenha.") + quiz(2, "b", "O que devolve <code>rede.predict_proba(novos_esc)[:, 1]</code>?", [("a", "A classe prevista (0 ou 1) de cada visitante."), ("b", "A chance de a classe 1 (comprou) para cada visitante, entre 0 e 1."), ("c", "O erro da rede em cada época.")], "O <code>predict_proba</code> devolve uma coluna por classe; o <code>[:, 1]</code> pega a da classe 1, a de comprar.") + quiz(3, "a", "Para que serve o <code>stratify = y</code> no <code>train_test_split</code>?", [("a", "Manter a mesma proporção de compradores no treino e no teste."), ("b", "Embaralhar os dados mais uma vez."), ("c", "Padronizar as colunas.")], f"Com ele, a proporção de compradores fica {pc(D['pct_compra_treino'])} no treino e {pc(D['pct_compra_teste'])} no teste.") + quiz(4, "b", f"Com ativação <code>identity</code> nas camadas ocultas a acurácia foi {c3(B['identity'])}. O que isso mostra?", [("a", "Que a identidade é a melhor ativação."), ("b", "Que sem não linearidade a rede inteira vira uma conta linear e perde a faixa."), ("c", "Que o teste vazou para o treino.")], f"Camadas lineares empilhadas valem uma só. O resultado ({c3(B['identity'])}) fica no patamar da reta ({c3(D['acc_reta'])}).") + flash([
    ("Por que a saída da MLP de classificação é sigmoide?", "Ela espreme o valor para o intervalo de 0 a 1, que se lê como probabilidade de ser a classe 1."),
    ("Quantos parâmetros tem a rede 2-8-1?", f"(2×8 + 8) + (8×1 + 1) = {D['n_parametros']}."),
    ("O que é a régua na classificação?", f"A acurácia do chute ingênuo (\"ninguém compra\"): {c3(D['regua'])}. O modelo precisa ganhar dela."),
    ("O que o <code>.fit</code> do scaler devolve?", "O próprio scaler, não os dados. Para obter os dados do teste padronizados, use <code>.transform</code>.")]) + ponte("Fim por enquanto", "A apostila cresce junto com as aulas. Quando a teoria desta aula (gradiente e retropropagação na classificação) estiver registrada, este capítulo ganha uma seção nova.", titulo="Para onde vamos agora") + '''
</section>'''
chapter(PASTA, 9, "mlp-classificacao", T, "MLP de classificação: prever a compra", "Capítulo 9 · Aula 9",
        "A mesma rede da Aula 7, agora respondendo sim ou não: sigmoide, probabilidade de compra e acurácia.",
        ["<b>~45 min</b>", "2 demos · 4 testes · 4 flashcards", "dados reais do scikit-learn"], body9, scripts=S_COMPRA)
print("rn cap 9 ok")
