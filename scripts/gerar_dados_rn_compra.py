"""Gera redes-neurais/rn-compra-data.js: dados e resultados reais do capitulo 9 (MLP de classificacao).

Uso:  python scripts/gerar_dados_rn_compra.py
Precisa de: numpy, pandas, scikit-learn (testado com 1.6.1). Nao precisa de internet.
Os 1000 visitantes sao gerados por computador com a mesma regra e a mesma semente (42) do notebook da aula.
O arquivo gerado nao deve ser editado a mao.
"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

# ---- dados (mesma regra do notebook da aula) ----
rng = np.random.default_rng(42)
n = 1000
tempo = rng.uniform(0, 20, n)
desconto = rng.uniform(0, 20, n)
logit = 3 - 1.5 * ((tempo - 10) / 3) ** 2 + 0.3 * (desconto - 10)
prob_compra = 1 / (1 + np.exp(-logit))
comprou = (rng.uniform(size=n) < prob_compra).astype(int)
dados = pd.DataFrame({"tempo_no_site": tempo.round(1), "desconto": desconto.round(1), "comprou": comprou})

X = dados[["tempo_no_site", "desconto"]]
y = dados["comprou"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
esc = StandardScaler()
X_tr_e = esc.fit_transform(X_tr)
X_te_e = esc.transform(X_te)

def treina(camadas=(8,), ativ="relu", semente=42):
    r = MLPClassifier(hidden_layer_sizes=camadas, activation=ativ, max_iter=1000, random_state=semente)
    r.fit(X_tr_e, y_tr)
    return r

reta = LogisticRegression().fit(X_tr_e, y_tr)
rede = treina()
regua = 1 - float(y_te.mean())

novos = pd.DataFrame({"tempo_no_site": [10, 10, 10, 1, 19], "desconto": [0, 10, 20, 10, 10]})
prob_novos = rede.predict_proba(esc.transform(novos))[:, 1]

exp_A = {str(k): round(float(treina((k,)).score(X_te_e, y_te)), 3) for k in (1, 2, 3, 8)}
exp_B = {a: round(float(treina((8,), a).score(X_te_e, y_te)), 3) for a in ("relu", "tanh", "logistic", "identity")}
sementes_3 = {str(s): round(float(treina((3,), "relu", s).score(X_te_e, y_te)), 3) for s in (0, 1, 7)}

# grade da regiao de decisao da MLP, para o desenho (probabilidade em 0..1)
G = 40
grade = []
for j in range(G):
    for i in range(G):
        grade.append([i * 20 / (G - 1), j * 20 / (G - 1)])
p_grade = rede.predict_proba(esc.transform(pd.DataFrame(grade, columns=["tempo_no_site", "desconto"])))[:, 1]

out = {
    "versao_sklearn": sklearn.__version__,
    "n": n,
    "pct_compra": round(float(y.mean()), 3),
    "pct_compra_treino": round(float(y_tr.mean()), 3), "pct_compra_teste": round(float(y_te.mean()), 3),
    "n_treino": int(len(X_tr)), "n_teste": int(len(X_te)),
    "regua": round(regua, 3),
    "acc_reta": round(float(reta.score(X_te_e, y_te)), 3),
    "acc_mlp": round(float(rede.score(X_te_e, y_te)), 3),
    "epocas": int(rede.n_iter_),
    "saida": rede.out_activation_,
    "n_parametros": int(sum(c.size for c in rede.coefs_) + sum(b.size for b in rede.intercepts_)),
    "pts": [[float(a), float(b), int(c)] for a, b, c in dados.itertuples(index=False)],
    "scaler": {"media": [round(float(v), 10) for v in esc.mean_], "desvio": [round(float(v), 10) for v in esc.scale_]},
    "reta": {"w": [float(v) for v in reta.coef_[0]], "b": float(reta.intercept_[0])},
    "W1": [[float(v) for v in linha] for linha in rede.coefs_[0]],
    "b1": [float(v) for v in rede.intercepts_[0]],
    "W2": [float(v[0]) for v in rede.coefs_[1]],
    "b2": float(rede.intercepts_[1][0]),
    "novos": [{"tempo": int(a), "desconto": int(b), "prob": round(float(p), 3)} for a, b, p in zip(novos.tempo_no_site, novos.desconto, prob_novos)],
    "exp": {"A": exp_A, "B": exp_B, "A3_sementes": sementes_3},
    "grade": {"n": G, "lado": 20, "prob": [round(float(p), 3) for p in p_grade]},
}

dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "redes-neurais", "rn-compra-data.js")
cab = ("/* Resultados reais do scikit-learn " + sklearn.__version__ + " para o capitulo 9 (MLP de classificacao): 1000 visitantes gerados por computador "
       "(semente 42, regra do notebook da aula), reta (LogisticRegression) e MLPClassifier de 8 neuronios ReLU. "
       "Gerado por scripts/gerar_dados_rn_compra.py; nao editar a mao. */\n")
open(dest, "w", encoding="utf-8").write(cab + "window.RNCOMPRA = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
print("ok", os.path.normpath(dest))
print({k: out[k] for k in ("n_treino", "n_teste", "pct_compra", "regua", "acc_reta", "acc_mlp", "epocas", "saida", "n_parametros")})
print("novos", out["novos"]); print("A", exp_A); print("B", exp_B); print("A(3)", sementes_3)
