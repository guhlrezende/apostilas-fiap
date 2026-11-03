/* Demo do capítulo 10 da apostila de Python: o que os testes dizem quando o código tem um defeito.
   As saídas abaixo foram copiadas de execuções reais de `python -m unittest` (Python 3.13),
   só com o caminho dos arquivos encurtado. */
(function () {
  var E = window.Estudo;
  function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  var OK = ".....\n----------------------------------------------------------------------\nRan 5 tests in 0.001s\n\nOK";
  var CASOS = {
    ok: {
      rot: "Código correto",
      trecho: "return round(preco * (1 - percentual / 100), 2)",
      saida: OK,
      nota: "Os 5 testes passam. Cada ponto é um teste que passou."
    },
    a: {
      rot: "Defeito 1: divide por 10 em vez de 100",
      trecho: "return round(preco * (1 - percentual / 10), 2)",
      saida: "F....\n======================================================================\nFAIL: test_dez_por_cento (test_loja.TestDesconto.test_dez_por_cento)\n----------------------------------------------------------------------\nTraceback (most recent call last):\n  File \"test_loja.py\", line 10, in test_dez_por_cento\n    self.assertEqual(loja.desconto(50.0, 10), 45.0)\nAssertionError: 0.0 != 45.0\n\n----------------------------------------------------------------------\nRan 5 tests in 0.004s\n\nFAILED (failures=1)",
      nota: "<b>F de falha</b>: o código rodou até o fim e devolveu um valor diferente do esperado. A última linha mostra o que veio (0.0) e o que era esperado (45.0). Os outros 4 testes seguem passando: o teste que falhou aponta o defeito."
    },
    b: {
      rot: "Defeito 2: a validação do percentual sumiu",
      trecho: "if False:      # antes: if percentual < 0 or percentual > 100:",
      saida: ".F...\n======================================================================\nFAIL: test_percentual_invalido (test_loja.TestDesconto.test_percentual_invalido)\n----------------------------------------------------------------------\nTraceback (most recent call last):\n  File \"test_loja.py\", line 16, in test_percentual_invalido\n    with self.assertRaises(ValueError):\n         ~~~~~~~~~~~~~~~~^^^^^^^^^^^^\nAssertionError: ValueError not raised\n\n----------------------------------------------------------------------\nRan 5 tests in 0.003s\n\nFAILED (failures=1)",
      nota: "Os testes de valor continuam verdes, e só o teste do caminho de erro acusa o defeito. Sem esse teste, ninguém perceberia."
    },
    c: {
      rot: "Defeito 3: o try/except foi retirado de pedir_quantidade",
      trecho: "n = int(texto)      # antes: dentro de try/except ValueError",
      saida: "....E\n======================================================================\nERROR: test_pede_de_novo_apos_erro (test_loja.TestPedirQuantidade.test_pede_de_novo_apos_erro)\n----------------------------------------------------------------------\nTraceback (most recent call last):\n  File \"test_loja.py\", line 28, in test_pede_de_novo_apos_erro\n    resultado = loja.pedir_quantidade()\n  File \"loja.py\", line 12, in pedir_quantidade\n    n = int(texto)\nValueError: invalid literal for int() with base 10: 'abc'\n\n----------------------------------------------------------------------\nRan 5 tests in 0.003s\n\nFAILED (errors=1)",
      nota: "<b>E de erro</b>: não foi um <code>assert</code> que falhou, foi uma exceção inesperada (<code>ValueError</code>) estourando dentro do código. Falha e erro são coisas diferentes, e o resumo final conta cada uma."
    }
  };

  E.demos.testesdefeito = function (el) {
    var h = '<h4>Quebre o código e veja o que os testes dizem</h4><div class="ctrls"><label>Versão do <code>loja.py</code>: <select>';
    Object.keys(CASOS).forEach(function (k) { h += '<option value="' + k + '">' + esc(CASOS[k].rot) + '</option>'; });
    h += '</select></label><button class="btn sm pri" type="button">▶ python -m unittest</button></div>' +
      '<pre class="jq" style="margin:8px 0"></pre><pre class="out" style="margin:8px 0;min-height:4em"></pre><div class="read"></div>';
    el.innerHTML = h;
    var sel = el.querySelector("select"), jq = el.querySelector(".jq"), out = el.querySelector(".out"), rd = el.querySelector(".read");
    function mostra() {
      var c = CASOS[sel.value];
      jq.textContent = "# loja.py\n" + c.trecho;
      out.textContent = "(escolha uma versão e clique para rodar os testes)";
      rd.innerHTML = "Os mesmos 5 testes do capítulo rodam contra a versão escolhida.";
    }
    sel.addEventListener("change", mostra);
    el.querySelector("button").addEventListener("click", function () {
      var c = CASOS[sel.value];
      out.textContent = c.saida;
      rd.innerHTML = c.nota;
    });
    mostra();
  };
})();
