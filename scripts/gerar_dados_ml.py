"""Gera machine-learning/ml-data.js: dados reais usados nas demos (Iris, Insurance e resultados do scikit-learn).

Uso:  python scripts/gerar_dados_ml.py
Precisa de: numpy, pandas, scikit-learn e internet (le o insurance.csv do mesmo link usado nas aulas).
O arquivo gerado nao deve ser editado a mao.
"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

iris = load_iris()
I = [[float(r[2]), float(r[3]), float(r[0]), float(r[1]), int(c)] for r, c in zip(iris.data, iris.target)]

df = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")
regs = ["northeast","northwest","southeast","southwest"]
INS = [[int(r.age), round(float(r.bmi),2), int(r.children), 1 if r.smoker=="yes" else 0, 1 if r.sex=="male" else 0, regs.index(r.region), round(float(r.charges),2)] for r in df.itertuples()]

X = df.drop(columns="charges"); y = df["charges"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
num, cat = ["age","bmi","children"], ["sex","smoker","region"]
pre = lambda: ColumnTransformer([("num", StandardScaler(), num), ("cat", OneHotEncoder(handle_unknown="ignore"), cat)])
def mk(**kw): return Pipeline([("pre", pre()), ("m", KNeighborsRegressor(**kw))])

# grade da aula: k 1..20 x weights x metric, cv=5 (RMSE no treino)
grid = {}
for metric in ["euclidean","manhattan"]:
    for w in ["uniform","distance"]:
        row=[]
        for k in range(1,21):
            s = cross_val_score(mk(n_neighbors=k, weights=w, metric=metric), Xtr, ytr, cv=5, scoring="neg_root_mean_squared_error")
            row.append(round(float(-s.mean()),1))
        grid[f"{metric}|{w}"]=row
# confere com GridSearchCV
g = GridSearchCV(Pipeline([("pre", pre()),("m",KNeighborsRegressor())]),
    {"m__n_neighbors":list(range(1,21)),"m__weights":["uniform","distance"],"m__metric":["euclidean","manhattan"]},
    cv=5, scoring="neg_root_mean_squared_error").fit(Xtr,ytr)
print("best", g.best_params_, round(-g.best_score_,1))

# curva de k (euclidean/uniform): treino, teste e CV
kc = {"train":[], "test":[], "cv":[]}
rm = lambda a,b: float(mean_squared_error(a,b)**0.5)
for k in range(1,41):
    m = mk(n_neighbors=k).fit(Xtr,ytr)
    kc["train"].append(round(rm(ytr,m.predict(Xtr)),1)); kc["test"].append(round(rm(yte,m.predict(Xte)),1))
    kc["cv"].append(round(float(-cross_val_score(mk(n_neighbors=k),Xtr,ytr,cv=5,scoring="neg_root_mean_squared_error").mean()),1))

# holdout x CV por semente (baseline k=5)
hold=[]; cvs=[]
for sd in range(60):
    a,b,c,d = train_test_split(X,y,test_size=0.2,random_state=sd)
    hold.append(round(rm(d, mk(n_neighbors=5).fit(a,c).predict(b)),1))
    cvs.append(round(float(-cross_val_score(mk(n_neighbors=5),X,y,cv=KFold(5,shuffle=True,random_state=sd),scoring="neg_root_mean_squared_error").mean()),1))

# baseline e tunado no teste
base = mk(n_neighbors=5).fit(Xtr,ytr); tun = g.best_estimator_
def mets(p): return {"MAE":round(mean_absolute_error(yte,p),2),"MSE":round(mean_squared_error(yte,p),0),"RMSE":round(rm(yte,p),2),"R2":round(r2_score(yte,p),4)}
ref = {"baseline":mets(base.predict(Xte)),"tunado":mets(tun.predict(Xte))}
print(ref)

# regressao linear com tudo (get_dummies drop_first + StandardScaler no treino)
D = pd.get_dummies(X, drop_first=True, dtype=float)
a,b,c,d = train_test_split(D,y,test_size=0.2,random_state=42)
sc = StandardScaler().fit(a); lr = LinearRegression().fit(sc.transform(a),c); p = lr.predict(sc.transform(b))
lin = {"cols":list(D.columns),"coef":[round(float(v),1) for v in lr.coef_],"intercept":round(float(lr.intercept_),1),
       "R2":round(r2_score(d,p),4),"RMSE":round(rm(d,p),2),"MAE":round(mean_absolute_error(d,p),2),"MSE":round(float(mean_squared_error(d,p)),2)}
print(lin)
# bmi so, e bmi+smoker, no conjunto inteiro
def r2_of(cols):
    Z = pd.get_dummies(X[cols], drop_first=True, dtype=float)
    return round(float(LinearRegression().fit(Z,y).score(Z,y)),3)
print("R2 bmi", r2_of(["bmi"]), "bmi+smoker", r2_of(["bmi","smoker"]))
# reta de minimos quadrados IMC -> charges/1000 (conjunto todo)
bm = df["bmi"].values; ch = df["charges"].values/1000
b1 = float(np.cov(bm,ch,bias=True)[0,1]/np.var(bm)); b0 = float(ch.mean()-b1*bm.mean())
print("reta bmi->charges/1000", round(b0,4), round(b1,4))
# estatisticas da idade
ag=df["age"]
st={"min":int(ag.min()),"max":int(ag.max()),"mean":round(float(ag.mean()),3),"std_pop":round(float(ag.std(ddof=0)),3),"median":float(ag.median()),"q1":float(ag.quantile(.25)),"q3":float(ag.quantile(.75))}
print(st)

out = {"IRIS":I,"INS":INS,"GRID":grid,"KCURVE":kc,"HOLD":hold,"CVS":cvs,"REF":ref,"LIN":lin,"AGE":st,"BMILINE":[round(b0,4),round(b1,4)]}
js = "/* Dados reais gerados com scikit-learn 1.6 e o dataset Insurance (ver docs). Nao editar a mao. */\nwindow.MLDATA = " + json.dumps(out, separators=(",",":"), ensure_ascii=False) + ";\n"
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "machine-learning", "ml-data.js"),"w",encoding="utf-8").write(js)
print(len(js))
