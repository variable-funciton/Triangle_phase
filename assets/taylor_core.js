/*
 * sin x, cos x の x = x0 のまわりでの多項式近似（テイラー展開）
 *   f(x) ≈ c0 + c1 (x − x0) + c2 (x − x0)^2 + … + cn (x − x0)^n
 * 係数は sin → cos → −sin → −cos → sin … のくり返しを k! で割ったもの。
 * テスト: node tests/test_widgets_js.js
 */
(function (root) {
  "use strict";
  var TU = root.TU || require("./common_core.js");

  var F = { sin: Math.sin, cos: Math.cos };
  // k 回目の「傾きをとる」操作で現れる関数（4 回で元にもどる）
  var CYCLE = {
    sin: [["\\sin", 1], ["\\cos", 1], ["\\sin", -1], ["\\cos", -1]],
    cos: [["\\cos", 1], ["\\sin", -1], ["\\cos", -1], ["\\sin", 1]],
  };

  /** k 番目の係数の分子（k! で割る前）の値 */
  function numer(fn, k, x0) {
    var c = CYCLE[fn][k % 4];
    return c[1] * (c[0] === "\\sin" ? Math.sin(x0) : Math.cos(x0));
  }

  function coeffs(fn, x0, n) {
    var out = [];
    for (var k = 0; k <= n; k++) out.push(numer(fn, k, x0) / TU.factorial(k));
    return out;
  }

  /** 多項式の値（ホーナー法） */
  function evalP(cs, x0, x) {
    var t = x - x0, v = 0;
    for (var k = cs.length - 1; k >= 0; k--) v = v * t + cs[k];
    return v;
  }

  /** |P(x) − f(x)| < tol となる x0 を含む区間 [lo, hi]（x0 から外へ向かって調べる） */
  function goodRange(fn, x0, n, tol, limit) {
    tol = tol || 0.01; limit = limit || 12;
    var cs = coeffs(fn, x0, n), f = F[fn], step = 0.005;
    function ok(x) { return Math.abs(evalP(cs, x0, x) - f(x)) < tol; }
    var hi = x0, lo = x0;
    while (hi - x0 < limit && ok(hi + step)) hi += step;
    while (x0 - lo < limit && ok(lo - step)) lo -= step;
    return [lo, hi];
  }

  /** (x − x0) の LaTeX */
  function shiftTex(x0Tex, x0) {
    if (Math.abs(x0) < 1e-12) return "x";
    var neg = x0 < 0;
    var mag = neg ? x0Tex.replace(/^-/, "") : x0Tex;
    return "\\left(x " + (neg ? "+ " : "- ") + mag + "\\right)";
  }

  function powTex(base, k) {
    if (k === 0) return "";
    if (k === 1) return base;
    return base + "^{" + k + "}";
  }

  /** 項を並べて、per 個ごとに改行した aligned 環境にする */
  function joinTerms(lhs, terms, per) {
    if (!terms.length) return lhs + " 0";
    per = per || 4;
    var lines = [], cur = "";
    terms.forEach(function (t, i) {
      var s = t.sign < 0 ? " - " : (i === 0 ? "" : " + ");
      if (i === 0 && t.sign < 0) s = "-";
      cur += s + t.body;
      if ((i + 1) % per === 0 && i < terms.length - 1) { lines.push(cur); cur = ""; }
    });
    lines.push(cur);
    if (lines.length === 1) return lhs + " " + lines[0];
    return "\\begin{aligned}" + lhs + " & " + lines[0] + "\\\\ & " + lines.slice(1).join("\\\\ & ") + "\\end{aligned}";
  }

  /**
   * 文字のままの形：sin x ≈ sin x0 + cos x0 (x − x0) − (sin x0 / 2!)(x − x0)^2 − …
   */
  function symbolicTex(fn, n) {
    var terms = [];
    for (var k = 0; k <= n; k++) {
      var c = CYCLE[fn][k % 4], f = c[0] + " x_0";
      var body = k === 0 ? f : k === 1 ? f + "\\,(x - x_0)" : "\\frac{" + f + "}{" + k + "!}(x - x_0)^{" + k + "}";
      terms.push({ sign: c[1], body: body });
    }
    return joinTerms("\\" + fn + " x \\approx", terms, 4);
  }

  /**
   * 値を入れた形。x0 が有名角なら √ を使ったぴったりの値、そうでなければ小数。
   * 値が 0 の項は書かない。戻り値 {tex, exact}
   */
  function valuedTex(fn, x0, n) {
    var x0Frac = TU.toFrac(x0 / Math.PI, 12);
    var x0Tex = x0Frac ? TU.piFracTex(x0Frac[0], x0Frac[1]) : TU.fmtNum(x0, 2);
    var exact = true, terms = [];
    var sh = shiftTex(x0Tex, x0);
    for (var k = 0; k <= n; k++) {
      var v = numer(fn, k, x0);
      if (Math.abs(v) < 1e-12) continue;
      var e = x0Frac ? TU.exactValue(Math.abs(v)) : null;
      if (!e || !e.exact) { exact = false; e = { tex: TU.fmtNum(Math.abs(v), 3) }; }
      var mag = e.tex === "1" ? "" : e.tex;
      var body;
      if (k === 0) body = e.tex;
      else if (k === 1) body = mag + (mag ? "\\," : "") + sh;
      else body = (mag ? mag + "\\cdot " : "") + "\\frac{" + powTex(sh, k) + "}{" + k + "!}";
      terms.push({ sign: v < 0 ? -1 : 1, body: body });
    }
    return { tex: joinTerms("\\" + fn + " x \\approx", terms, 4), exact: exact };
  }

  /** 係数を小数にした形：0.5 + 0.866(x − 0.52) − 0.25(x − 0.52)^2 … */
  function decimalTex(fn, x0, n) {
    var cs = coeffs(fn, x0, n), terms = [];
    var sh = shiftTex(TU.fmtNum(x0, 2), x0);
    cs.forEach(function (c, k) {
      if (Math.abs(numer(fn, k, x0)) < 1e-12) return;
      var m = Math.abs(c);
      var ms = m >= 0.01 ? TU.fmtNum(m, 4) : m >= 0.001 ? String(Number(m.toPrecision(3)))
        : m.toExponential(2).replace(/e([-+])(\d+)/, function (_, sg, d) { return "\\times 10^{" + (sg === "-" ? "-" : "") + d + "}"; });
      var body = k === 0 ? ms : (ms === "1" ? "" : ms) + powTex(sh, k);
      terms.push({ sign: c < 0 ? -1 : 1, body: body });
    });
    return joinTerms("\\" + fn + " x \\approx", terms, 4);
  }

  var api = { F: F, numer: numer, coeffs: coeffs, evalP: evalP, goodRange: goodRange,
    symbolicTex: symbolicTex, valuedTex: valuedTex, decimalTex: decimalTex };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.TY = api;
})(this);
