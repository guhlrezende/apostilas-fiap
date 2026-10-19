/* Funções compartilhadas pelas demos de ML (precisa de ml-data.js antes). */
(function () {
  var D = window.MLDATA, ML = window.ML = { D: D };

  ML.NOMES = ["setosa", "versicolor", "virginica"];
  ML.rng = function (seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
  ML.shuffle = function (arr, rnd) { var a = arr.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; };

  /* distância entre dois vetores */
  ML.dist = function (a, b, metric) {
    var s = 0, i;
    if (metric === "manhattan") { for (i = 0; i < a.length; i++) s += Math.abs(a[i] - b[i]); return s; }
    for (i = 0; i < a.length; i++) { var d = a[i] - b[i]; s += d * d; } return Math.sqrt(s);
  };
  /* k vizinhos de q em pts (cada pt = {x:[...], y:valor}) */
  ML.vizinhos = function (pts, q, k, metric) {
    var arr = pts.map(function (p, i) { return { i: i, d: ML.dist(p.x, q, metric), y: p.y }; });
    arr.sort(function (a, b) { return a.d - b.d; });
    return arr.slice(0, k);
  };
  ML.votar = function (neigh, nClasses, weights) {
    var v = new Array(nClasses).fill(0);
    neigh.forEach(function (n) { v[n.y] += weights === "distance" ? 1 / Math.max(n.d, 1e-9) : 1; });
    var best = 0; for (var c = 1; c < nClasses; c++) if (v[c] > v[best]) best = c;
    return { votos: v, classe: best };
  };
  ML.media = function (neigh, weights) {
    if (weights === "distance") { var sw = 0, s = 0; neigh.forEach(function (n) { var w = 1 / Math.max(n.d, 1e-9); sw += w; s += w * n.y; }); return s / sw; }
    return neigh.reduce(function (s, n) { return s + n.y; }, 0) / neigh.length;
  };
  ML.rmse = function (real, prev) { var s = 0; for (var i = 0; i < real.length; i++) { var e = real[i] - prev[i]; s += e * e; } return Math.sqrt(s / real.length); };

  /* mapeamento de coordenadas de dados para pixels */
  ML.plot = function (w, h, x0, x1, y0, y1, pad) {
    pad = pad || { l: 44, r: 12, t: 12, b: 34 };
    var P = { pad: pad,
      X: function (x) { return pad.l + (x - x0) / (x1 - x0) * (w - pad.l - pad.r); },
      Y: function (y) { return pad.t + (1 - (y - y0) / (y1 - y0)) * (h - pad.t - pad.b); },
      ix: function (px) { return x0 + (px - pad.l) / (w - pad.l - pad.r) * (x1 - x0); },
      iy: function (py) { return y0 + (1 - (py - pad.t) / (h - pad.t - pad.b)) * (y1 - y0); } };
    return P;
  };
  ML.axes = function (ctx, w, h, P, x0, x1, y0, y1, xs, ys, xl, yl, c, fmtY) {
    ctx.save(); ctx.lineWidth = 1; ctx.strokeStyle = c.line; ctx.fillStyle = c.muted; ctx.font = "11px Inter,system-ui,sans-serif";
    ctx.textAlign = "center";
    for (var x = Math.ceil(x0 / xs) * xs; x <= x1 + 1e-9; x += xs) { ctx.beginPath(); ctx.moveTo(P.X(x), P.pad.t); ctx.lineTo(P.X(x), h - P.pad.b); ctx.stroke(); ctx.fillText(+x.toFixed(2), P.X(x), h - P.pad.b + 14); }
    ctx.textAlign = "right";
    for (var y = Math.ceil(y0 / ys) * ys; y <= y1 + 1e-9; y += ys) { ctx.beginPath(); ctx.moveTo(P.pad.l, P.Y(y)); ctx.lineTo(w - P.pad.r, P.Y(y)); ctx.stroke(); ctx.fillText(fmtY ? fmtY(y) : +y.toFixed(2), P.pad.l - 6, P.Y(y) + 4); }
    ctx.fillStyle = c.ink; ctx.font = "600 12px Inter,system-ui,sans-serif"; ctx.textAlign = "center"; ctx.fillText(xl, (P.pad.l + w - P.pad.r) / 2, h - 4);
    ctx.save(); ctx.translate(12, (P.pad.t + h - P.pad.b) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText(yl, 0, 0); ctx.restore();
    ctx.restore();
  };
  ML.classCol = function (c, i) { return [c.c0, c.c1, c.c2][i]; };
})();
