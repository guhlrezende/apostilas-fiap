# Pyodide local

Pyodide 314.0.7 (MPL-2.0), pacote oficial `pyodide-core-314.0.7.tar.bz2` da página de releases em https://github.com/pyodide/pyodide/releases (publicado em 14/09/2026). SHA-256 conferido contra o publicado pelo GitHub: `2abdcc2e35208af406e07724cffa85bc582ced97e9028383ecf5462541393f95`.

Copiados só os arquivos que o motor usa: `pyodide.mjs` (carregado por Worker do tipo módulo), `pyodide.asm.mjs`, `pyodide.asm.wasm`, `python_stdlib.zip`, `pyodide-lock.json`, `package.json`. Cerca de 13 MB, baixados uma vez e guardados pelo navegador. Esta pasta só tem o núcleo (Python puro, sem NumPy, pandas ou scikit-learn): pacotes entram quando um capítulo precisar, e cada um será conferido e registrado aqui.
Para atualizar: baixar o novo pacote core, conferir o hash e substituir estes arquivos.

## Pacotes (pandas), 13/11/2026
Baixados de `https://cdn.jsdelivr.net/pyodide/v314.0.7/full/` (CDN oficial do projeto; repare no `v` do caminho), cada arquivo conferido contra o `sha256` do `pyodide-lock.json` antes de salvar. Cerca de 7,9 MB. O Worker só os carrega quando um exercício declara `data-pacotes="pandas"`.

| Pacote | Versão | Arquivo | sha256 |
|---|---|---|---|
| numpy | 2.4.6 | `numpy-2.4.6-cp314-cp314-pyemscripten_2026_0_wasm32.whl` | `a292c1f5d7d8a2208cd5e94fc467604c131cabcd2fc14fed6eefde121e7fabdf` |
| pandas | 3.0.2 | `pandas-3.0.2-cp314-cp314-pyemscripten_2026_0_wasm32.whl` | `45ff57772cc2f366a8582c7d3097cc4e6676342ecd5a3c08184a43462d5a02ae` |
| python-dateutil | 2.9.0.post0 | `python_dateutil-2.9.0.post0-py2.py3-none-any.whl` | `9b13365edf9c188f570baf9c540bbb3029ada2a2dacb9694b3659941693ee9e5` |
| pytz | 2026.1.post1 | `pytz-2026.1.post1-py2.py3-none-any.whl` | `b8249d6450146e0b61e6d710dc02ebb35a904796c4c2f97fe87d4ac5872db36a` |
| six | 1.17.0 | `six-1.17.0-py2.py3-none-any.whl` | `228c50f73aa7addf2c2ccf2979c256802a59ab69cad8152b31b9443cc8140f42` |

Versões do navegador, não as do Python local: o pandas aqui é o 3.x (texto vira o tipo `str` por padrão, por exemplo). Para ver a saída real: `node scripts/rodar_pyodide.mjs --pacotes pandas --codigo "..."` a partir da raiz do repositório.
Para somar outro pacote (ex.: scikit-learn no Capítulo 3): baixar o fecho de dependências do `pyodide-lock.json`, conferir os hashes e listar aqui.

## Pacotes (scikit-learn), 15/11/2026
Mesmo método do pandas: baixados de `https://cdn.jsdelivr.net/pyodide/v314.0.7/full/`, cada arquivo conferido contra o `sha256` do `pyodide-lock.json` (numpy já estava aqui). Cerca de 18,7 MB a mais. Carregados só quando um exercício declara `data-pacotes="scikit-learn"` (o Pyodide puxa as dependências sozinho). Teste feito com `scripts/rodar_pyodide.mjs`: `sklearn 1.8.0`, `scipy 1.18.0`, `numpy 2.4.6`, e uma regressão logística ajustou e deu score.

| Pacote | Versão | Arquivo | sha256 |
|---|---|---|---|
| scikit-learn | 1.8.0 | `scikit_learn-1.8.0-cp314-cp314-pyemscripten_2026_0_wasm32.whl` | `432f560f54c5283d13e9d7c11dddc8bdf2f15aec326cc1d7314f600786154181` |
| scipy | 1.18.0 | `scipy-1.18.0-cp314-cp314-pyemscripten_2026_0_wasm32.whl` | `17ee329a957863516d1bb6a6aaa0c60576fac027e9cd3d43de27f58b5b599b50` |
| joblib | 1.5.3 | `joblib-1.5.3-py3-none-any.whl` | `fb2860ff70d0b6b43a3df5e3ce52d3a938ad2fcacd80a3f2f3f37e930843e607` |
| threadpoolctl | 3.6.0 | `threadpoolctl-3.6.0-py3-none-any.whl` | `3521783ffb6bf212e03fb67ec1955af206d6ba7ea09ac21f200875077bbbe7c2` |
