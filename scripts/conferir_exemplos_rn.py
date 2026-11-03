"""Reproduz os numeros dos exemplos proprios da apostila de Redes Neurais
(cap. 4: bias e arredondamento; cap. 7: softmax, metricas de classe rara, autoencoder).
Uso: python scripts/conferir_exemplos_rn.py   (precisa de numpy e scikit-learn)"""
from fractions import Fraction as F
import numpy as np, sklearn

X = [(0, 0), (0, 1), (1, 0), (1, 1)]; Y = [0, 0, 0, 1]

def perceptron(com_bias=True, num=F, arred=None, eta="0.1", maxep=6):
    w = [num(0), num(0)]; b = num(0); e = num(eta); log = []
    for ep in range(1, maxep + 1):
        erros = 0
        for (x1, x2), y in zip(X, Y):
            z = w[0] * x1 + w[1] * x2 + (b if com_bias else 0)
            yh = 1 if z >= 0 else 0
            if yh != y:
                erros += 1; d = e * (y - yh)
                w = [w[0] + d * x1, w[1] + d * x2]
                if com_bias: b = b + d
                if arred is not None: w = [round(v, arred) for v in w]; b = round(b, arred)
        log.append((ep, [float(v) for v in w], float(b), erros))
        if erros == 0: break
    return log

print("== cap. 4 ==")
print("sem bias (6 epocas):", perceptron(com_bias=False))
print("com bias, conta exata:", perceptron())
print("com bias, float sem arredondar:", perceptron(num=float))
print("com bias, float arredondando a 2 casas:", perceptron(num=float, arred=2))

print("\n== cap. 7: softmax ==")
z = np.array([2.0, 1.0, 0.1]); p = np.exp(z) / np.exp(z).sum()
print("softmax", p.round(3), "soma", p.sum().round(3))
print("sigmoide(2)", round(1 / (1 + np.exp(-2)), 3))

print("\n== cap. 7: classe rara (1000 casos, 20 positivos; inventado) ==")
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
y = np.array([1] * 20 + [0] * 980)
chute = np.zeros(1000, int)
modelo = np.zeros(1000, int); modelo[:12] = 1; modelo[20:24] = 1   # 12 acertos, 8 perdidos, 4 alarmes falsos
for nome, yp in (("chute 'nunca'", chute), ("modelo", modelo)):
    print(nome, "acc", accuracy_score(y, yp), "prec", round(precision_score(y, yp, zero_division=0), 3),
          "rec", round(recall_score(y, yp), 3), "f1", round(f1_score(y, yp), 3))

print("\n== cap. 7: autoencoder (scikit-learn %s) ==" % sklearn.__version__)
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
rng = np.random.RandomState(0)
def normais(n):
    t = rng.normal(0, 1, n)
    return np.c_[t + rng.normal(0, .1, n), 2 * t + rng.normal(0, .1, n), -t + rng.normal(0, .1, n)]
Xtr, Xval = normais(500), normais(200)
t = rng.normal(0, 1, 20)   # anomalias: a relacao entre as colunas quebra
Xan = np.c_[t, -2 * t + rng.normal(0, .1, 20), rng.normal(0, 1, 20)]
esc = StandardScaler().fit(Xtr)
A, V, N = esc.transform(Xtr), esc.transform(Xval), esc.transform(Xan)
ae = MLPRegressor(hidden_layer_sizes=(4, 1, 4), activation="tanh", max_iter=3000, random_state=0).fit(A, A)
erro = lambda M: ((ae.predict(M) - M) ** 2).mean(axis=1)
e_tr, e_val, e_an = erro(A), erro(V), erro(N)
lim = e_tr.mean() + 3 * e_tr.std()
print("erro medio treino %.4f | normais novos %.4f | anomalias %.4f" % (e_tr.mean(), e_val.mean(), e_an.mean()))
print("limiar (media + 3 desvios no treino): %.4f" % lim)
print("normais novos acima do limiar: %d de %d | anomalias acima: %d de %d" % ((e_val > lim).sum(), len(V), (e_an > lim).sum(), len(N)))
