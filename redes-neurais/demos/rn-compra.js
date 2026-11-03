/* Demos do capítulo 9 (MLP de classificação). Os pesos vêm de rn-compra-data.js, gerado pelo scikit-learn. */
(function () {
  var E = window.Estudo;
  function pct(v) { return (v * 100).toFixed(1).replace(".", ",") + "%"; }
  function f3(v) { return v.toFixed(3).replace(".", ","); }
  function rgbOf(cor) { var t = document.createElement("canvas"); t.width = t.height = 1; var x = t.getContext("2d"); x.fillStyle = cor; x.fillRect(0, 0, 1, 1); var d = x.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2]]; }

  /* a mesma conta que o MLPClassifier faz: padroniza, camada oculta ReLU, saída sigmoide */
  function prever(D, tempo, desconto) {
    var x = [(tempo - D.scaler.media[0]) / D.scaler.desvio[0], (desconto - D.scaler.media[1]) / D.scaler.desvio[1]], z = D.b2;
    for (var j = 0; j < D.b1.length; j++) {
      var h = Math.max(0, x[0] * D.W1[0][j] + x[1] * D.W1[1][j] + D.b1[j]);
      z += h * D.W2[j];
    }
    return 1 / (1 + Math.exp(-z));
  }
  function probReta(D, tempo, desconto) {
    var x0 = (tempo - D.scaler.media[0]) / D.scaler.desvio[0], x1 = (desconto - D.scaler.media[1]) / D.scaler.desvio[1];
    return 1 / (1 + Math.exp(-(D.reta.w[0] * x0 + D.reta.w[1] * x1 + D.reta.b)));
  }
  window.RNCOMPRA_PREVER = prever;

  E.demos.mlpcompra = function (el) {
    var D = window.RNCOMPRA;
    el.innerHTML = '<h4>Quem compra? 1000 visitantes gerados por computador</h4>' +
      '<canvas style="height:340px;cursor:default"></canvas>' +
      '<div class="legend"><span><i style="background:var(--c1)"></i>comprou</span><span><i style="background:var(--c0)"></i>não comprou</span></div>' +
      '<div class="ctrls"><label>tempo no site <input type="range" id="ct" min="0" max="20" step="0.5" value="10"><output id="cto"></output> min</label>' +
      '<label>desconto <input type="range" id="cd" min="0" max="20" step="0.5" value="10"><output id="cdo"></output> %</label>' +
      '<label><input type="checkbox" id="cm" checked> fundo da MLP</label><label><input type="checkbox" id="cr"> reta</label></div>' +
      '<div class="tablewrap"><table><tr><th>modelo</th><th class="n">acurácia no teste</th></tr>' +
      '<tr><td>chutar "ninguém compra"</td><td class="n">' + f3(D.regua) + '</td></tr>' +
      '<tr><td>reta (regressão logística)</td><td class="n">' + f3(D.acc_reta) + '</td></tr>' +
      '<tr class="dest"><td>MLP (8 neurônios ReLU, saída sigmoide)</td><td class="n">' + f3(D.acc_mlp) + '</td></tr></table></div>' +
      '<div class="read"></div>';
    var cv = el.querySelector("canvas"), ct = el.querySelector("#ct"), cd = el.querySelector("#cd"), cm = el.querySelector("#cm"), cr = el.querySelector("#cr"), rd = el.querySelector(".read");
    var L = 20, pad = { l: 44, r: 10, t: 10, b: 34 };
    var api = E.canvas(cv, function (ctx, w, h, c) {
      function X(x) { return pad.l + x / L * (w - pad.l - pad.r); }
      function Y(y) { return pad.t + (1 - y / L) * (h - pad.t - pad.b); }
      var G = D.grade.n, cw = (w - pad.l - pad.r) / (G - 1), ch = (h - pad.t - pad.b) / (G - 1);
      if (cm.checked) { /* fundo: imagem G x G esticada com suavização, sem emendas entre as células */
        var rgb1 = rgbOf(c.c1), rgb0 = rgbOf(c.c0), off = document.createElement("canvas"); off.width = off.height = G;
        var octx = off.getContext("2d"), img = octx.createImageData(G, G);
        for (var k = 0; k < D.grade.prob.length; k++) {
          var i = k % G, j = Math.floor(k / G), p = D.grade.prob[k], o = ((G - 1 - j) * G + i) * 4, rgb = p > 0.5 ? rgb1 : rgb0;
          img.data[o] = rgb[0]; img.data[o + 1] = rgb[1]; img.data[o + 2] = rgb[2]; img.data[o + 3] = Math.round((0.08 + 0.37 * Math.abs(p - 0.5) * 2) * 255);
        }
        octx.putImageData(img, 0, 0);
        ctx.imageSmoothingEnabled = true; ctx.drawImage(off, X(0) - cw / 2, Y(L) - ch / 2, (w - pad.l - pad.r) + cw, (h - pad.t - pad.b) + ch);
      }
      ctx.save(); ctx.lineWidth = 1; ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif"; ctx.textAlign = "center";
      for (var a = 0; a <= L; a += 5) { ctx.beginPath(); ctx.moveTo(X(a), pad.t); ctx.lineTo(X(a), h - pad.b); ctx.stroke(); ctx.fillText(a, X(a), h - pad.b + 14); }
      ctx.textAlign = "right"; for (var b = 0; b <= L; b += 5) { ctx.beginPath(); ctx.moveTo(pad.l, Y(b)); ctx.lineTo(w - pad.r, Y(b)); ctx.stroke(); ctx.fillText(b, pad.l - 6, Y(b) + 4); }
      ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.textAlign = "center"; ctx.fillText("tempo no site (min)", (pad.l + w - pad.r) / 2, h - 4);
      ctx.translate(12, (pad.t + h - pad.b) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText("desconto (%)", 0, 0); ctx.restore();
      ctx.globalAlpha = 0.6;
      D.pts.forEach(function (p) { ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 2.6, 0, 6.2832); ctx.fillStyle = p[2] ? c.c1 : c.c0; ctx.fill(); });
      ctx.globalAlpha = 1;
      if (cr.checked) { /* a reta onde a probabilidade da regressão logística é 0,5 */
        ctx.beginPath(); var ini = false;
        for (var t = 0; t <= L; t += 0.25) {
          /* resolve desconto tal que w0*xt + w1*xd + b = 0 */
          var xt = (t - D.scaler.media[0]) / D.scaler.desvio[0], xd = -(D.reta.w[0] * xt + D.reta.b) / D.reta.w[1], dd = xd * D.scaler.desvio[1] + D.scaler.media[1];
          if (dd < 0 || dd > L) continue; if (!ini) { ctx.moveTo(X(t), Y(dd)); ini = true; } else ctx.lineTo(X(t), Y(dd));
        }
        ctx.lineWidth = 3; ctx.strokeStyle = c.ink; ctx.setLineDash([7, 5]); ctx.stroke(); ctx.setLineDash([]);
      }
      var tx = +ct.value, dx = +cd.value;
      ctx.beginPath(); ctx.arc(X(tx), Y(dx), 8, 0, 6.2832); ctx.lineWidth = 3; ctx.strokeStyle = c.ink; ctx.stroke();
      ctx.beginPath(); ctx.arc(X(tx), Y(dx), 3, 0, 6.2832); ctx.fillStyle = c.ink; ctx.fill();
    });
    function rep() {
      var tx = +ct.value, dx = +cd.value, p = prever(D, tx, dx), pr = probReta(D, tx, dx);
      el.querySelector("#cto").textContent = tx.toFixed(1).replace(".", ","); el.querySelector("#cdo").textContent = dx.toFixed(1).replace(".", ",");
      rd.innerHTML = "Para <b>" + tx.toFixed(1).replace(".", ",") + " min</b> e <b>" + dx.toFixed(1).replace(".", ",") + "%</b> de desconto, a MLP diz <b>" + pct(p) + "</b> de chance de compra (" + (p > 0.5 ? "responde 1: compra" : "responde 0: não compra") + "). A reta diz " + pct(pr) + ". " +
        "A conta é feita aqui no navegador com os pesos que o scikit-learn aprendeu, e bate com o <code>predict_proba</code>. Repare na <b>faixa do meio</b>: quem fica pouco ou demais não compra, mesmo com desconto.";
      api.paint();
    }
    el.addEventListener("input", rep); el.addEventListener("change", rep); rep();
  };

  E.demos.expcompra = function (el) {
    var D = window.RNCOMPRA.exp;
    function linhas(o, rot) { return Object.keys(o).map(function (k) { return '<tr class="' + (o[k] > 0.7 ? "dest" : "") + '"><td><code>' + rot(k) + '</code></td><td class="n">' + f3(o[k]) + '</td></tr>'; }).join(""); }
    el.innerHTML = '<h4>Os experimentos A e B da aula (valores reais)</h4><div class="grid2"><div><b>A: neurônios ocultos (<code>relu</code>, semente 42)</b><div class="tablewrap"><table><tr><th>camada oculta</th><th class="n">acurácia</th></tr>' +
      linhas(D.A, function (k) { return "(" + k + ",)"; }) + '</table></div></div><div><b>B: ativação (<code>(8,)</code>, semente 42)</b><div class="tablewrap"><table><tr><th>ativação</th><th class="n">acurácia</th></tr>' +
      linhas(D.B, function (k) { return k; }) + '</table></div></div></div>' +
      '<div class="read"><b>A:</b> com 1, 2 ou 3 neurônios (semente 42) a rede não achou a faixa e ficou perto da régua (0,632). Com 3 neurônios e outras sementes ela acha: ' + Object.keys(D.A3_sementes).map(function (s) { return "semente " + s + " → " + f3(D.A3_sementes[s]); }).join(", ") +
      '. Poucos neurônios dão pouca capacidade e dependem da sorte do sorteio inicial. <b>B:</b> com <code>identity</code> a rede inteira vira uma reta e cai para o patamar da reta (0,640).</div>';
  };
})();
