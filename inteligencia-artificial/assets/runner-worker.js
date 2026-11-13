/* Worker (tipo módulo) do motor de exercícios: carrega o Pyodide local e executa código + teste.
   O harness Python fica em harness.py (fonte única, também usada por scripts/rodar_pyodide.mjs).
   Entrada:  {tipo:"rodar", id, setup, codigo, teste}  |  {tipo:"pacotes", id, lista:["pandas"]}
   Saída:    {tipo:"pronto"} | {tipo:"progresso", texto} | {tipo:"falha-carga", erro}
             | {tipo:"pacotes-ok", id} | {tipo:"pacotes-falha", id, erro}
             | {tipo:"resultado", id, estado, saida, mensagem, linha}
   Estados: pass, fail, error, setup_error, test_error (timeout é decidido pela página, que reinicia este Worker). */
import { loadPyodide } from "./pyodide/pyodide.mjs";

var py = null, rodar = null, fila = Promise.resolve();

async function iniciar() {
  try {
    self.postMessage({ tipo: "progresso", texto: "Carregando o Python (só na primeira vez)..." });
    py = await loadPyodide({ indexURL: new URL("pyodide/", import.meta.url).href });
    var r = await fetch(new URL("harness.py", import.meta.url));
    if (!r.ok) throw new Error("harness.py não encontrado (" + r.status + ")");
    await py.runPythonAsync(await r.text());
    rodar = py.globals.get("_ia_rodar");
    self.postMessage({ tipo: "pronto" });
  } catch (e) {
    self.postMessage({ tipo: "falha-carga", erro: String(e && e.message || e) });
  }
}
var pronto = iniciar();

/* Um item por vez: pacotes e execuções nunca se sobrepõem */
self.onmessage = function (ev) {
  var m = ev.data;
  fila = fila.then(async function () {
    await pronto;
    if (!rodar) return;
    if (m.tipo === "pacotes") {
      try {
        await py.loadPackage(m.lista);
        self.postMessage({ tipo: "pacotes-ok", id: m.id });
      } catch (e) {
        self.postMessage({ tipo: "pacotes-falha", id: m.id, erro: String(e && e.message || e) });
      }
    } else if (m.tipo === "rodar") {
      try {
        var r = rodar(m.setup || "", m.codigo || "", m.teste || "");
        var o = r.toJs({ dict_converter: Object.fromEntries });
        r.destroy();
        self.postMessage({ tipo: "resultado", id: m.id, estado: o.estado, saida: o.saida, mensagem: o.mensagem, linha: o.linha });
      } catch (e) {
        self.postMessage({ tipo: "resultado", id: m.id, estado: "test_error", saida: "", mensagem: "Falha interna do motor: " + String(e && e.message || e), linha: null });
      }
    }
  });
};
