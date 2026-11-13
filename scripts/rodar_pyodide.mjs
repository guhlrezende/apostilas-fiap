/* Roda código Python da apostila de IA no MESMO motor do navegador (Pyodide local + harness.py),
   para colar saídas reais nos capítulos e conferir os exercícios.

   Uso (a partir da raiz do repositório):
     node scripts/rodar_pyodide.mjs --html inteligencia-artificial/cap-2-dados-reais.html
         Para cada <section class="experimento" data-ex="..."> confere: a solução PASSA e o código inicial NÃO passa.
         Imprime a saída real da solução. Sai com código 1 se algo falhar.
     node scripts/rodar_pyodide.mjs --py arquivo.py [--pacotes pandas,numpy]
         Roda um arquivo e imprime a saída real (sem teste).
     node scripts/rodar_pyodide.mjs --codigo "print(1+1)" [--pacotes pandas]
   Versões: Python e pacotes são os de assets/pyodide (não os do Python do seu computador). */
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const raiz = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pasta = resolve(raiz, "inteligencia-artificial/assets/pyodide") + "/";
const { loadPyodide } = await import(pathToFileURL(pasta + "pyodide.mjs").href);

const args = process.argv.slice(2);
const op = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const pacotesArg = (op("--pacotes") || "").split(",").map((x) => x.trim()).filter(Boolean);

const py = await loadPyodide({ indexURL: pasta });
py.runPython(readFileSync(resolve(raiz, "inteligencia-artificial/assets/harness.py"), "utf-8"));
const rodar = py.globals.get("_ia_rodar");
const carregados = new Set();
async function pacotes(lista) {
  const falt = lista.filter((p) => !carregados.has(p));
  if (falt.length) { await py.loadPackage(falt); falt.forEach((p) => carregados.add(p)); }
}
function executar(setup, codigo, teste) {
  const r = rodar(setup || "", codigo || "", teste || "");
  const o = r.toJs({ dict_converter: Object.fromEntries });
  r.destroy();
  return o;
}
const campo = (sec, cls) => { const m = sec.match(new RegExp('<script type="text/plain" class="' + cls + '">\\n?([\\s\\S]*?)</script>')); return m ? m[1].replace(/\s+$/, "") : ""; };

let falhou = false;
if (op("--html")) {
  const html = readFileSync(resolve(raiz, op("--html")), "utf-8");
  const secs = html.match(/<section class="experimento"[\s\S]*?<\/section>/g) || [];
  console.log(`${secs.length} experimento(s) em ${op("--html")}`);
  for (const sec of secs) {
    const id = (sec.match(/data-ex="([^"]+)"/) || [])[1] || "?";
    const pk = ((sec.match(/data-pacotes="([^"]*)"/) || [])[1] || "").split(",").map((x) => x.trim()).filter(Boolean);
    await pacotes(pk);
    const prep = campo(sec, "py-preparo"), ini = campo(sec, "py-inicial"), teste = campo(sec, "py-teste"), sol = campo(sec, "py-solucao");
    console.log(`\n=== ${id}${pk.length ? " (pacotes: " + pk.join(", ") + ")" : ""}`);
    if (!sol) { console.log("  SEM py-solucao: nada a conferir"); falhou = true; continue; }
    const rs = executar(prep, sol, teste);
    console.log(`  solução: ${rs.estado}${rs.mensagem ? " | " + rs.mensagem : ""}`);
    if (rs.estado !== "pass") falhou = true;
    console.log("  --- saída real da solução ---");
    console.log(rs.saida.replace(/^/gm, "  | ").trimEnd());
    const ri = executar(prep, ini, teste);
    console.log(`  código inicial: ${ri.estado}${ri.mensagem ? " | " + ri.mensagem : ""}`);
    if (ri.estado === "pass") { console.log("  PROBLEMA: o código inicial já passa no teste"); falhou = true; }
  }
} else if (op("--py") || op("--codigo")) {
  await pacotes(pacotesArg);
  const codigo = op("--py") ? readFileSync(resolve(op("--py")), "utf-8") : op("--codigo");
  const r = executar("", codigo, "");
  console.log(r.saida.trimEnd());
  if (r.estado !== "pass") { console.error(`\n[${r.estado}] ${r.mensagem}${r.linha ? " (linha " + r.linha + ")" : ""}`); falhou = true; }
} else {
  console.error("Uso: --html capitulo.html | --py arquivo.py [--pacotes a,b] | --codigo \"...\" [--pacotes a,b]");
  falhou = true;
}
process.exit(falhou ? 1 : 0);
