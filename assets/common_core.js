/*
 * ブラウザ側のページで共通に使う計算・表示の部品（Node でもテストできる純粋な関数だけ）
 *   TU.fmtNum(1.50) → "1.5"、TU.angle(1/3, "rad").tex → "\frac{\pi}{3}"、TU.exactValue(Math.sqrt(3)/2).tex → "\frac{\sqrt{3}}{2}"
 */
(function (root) {
  "use strict";

  var EPS = 1e-9;
  var MINUS = "−";

  function gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { var t = a % b; a = b; b = t; }
    return a || 1;
  }

  /** x が分母 maxDen 以下の分数とみなせるなら [分子, 分母]（約分済み）、そうでなければ null */
  function toFrac(x, maxDen, tol) {
    maxDen = maxDen || 24;
    tol = tol || EPS;
    for (var d = 1; d <= maxDen; d++) {
      var n = Math.round(x * d);
      if (Math.abs(x * d - n) < tol * d) {
        var g = gcd(n, d);
        return [n / g, d / g];
      }
    }
    return null;
  }

  /** 小数を最大 digits 桁で表示（末尾の 0 は消す）。-0 は 0 にする */
  function fmtNum(v, digits) {
    if (digits === undefined) digits = 2;
    var p = Math.pow(10, digits);
    var s = (Math.round(v * p) / p).toFixed(digits);
    if (s.indexOf(".") >= 0) s = s.replace(/0+$/, "").replace(/\.$/, "");
    if (s === "-0") s = "0";
    return s;
  }

  function minus(s) { return s.replace(/-/g, MINUS); }

  function piFracTex(n, d) {
    if (n === 0) return "0";
    var sign = n < 0 ? "-" : "";
    var an = Math.abs(n);
    var num = an === 1 ? "\\pi" : an + "\\pi";
    return d === 1 ? sign + num : sign + "\\frac{" + num + "}{" + d + "}";
  }

  function piFracText(n, d) {
    if (n === 0) return "0";
    var sign = n < 0 ? MINUS : "";
    var an = Math.abs(n);
    var num = an === 1 ? "π" : an + "π";
    return d === 1 ? sign + num : sign + num + "/" + d;
  }

  /**
   * 角度（π 単位の値 piVal）を表示用に。
   * 弧度法: 分母 maxDen 以下の π の分数ならその形、そうでなければ小数（ラジアン）
   * 度数法: 度（小数 2 桁まで）
   * 戻り値 {tex, text, exact}
   */
  function angle(piVal, unit, maxDen) {
    if (unit === "deg") {
      var deg = piVal * 180;
      var s = fmtNum(deg, 2);
      return { tex: s + "^\\circ", text: minus(s) + "°", exact: Math.abs(deg - Number(s)) < 1e-7 };
    }
    var f = toFrac(piVal, maxDen || 24);
    if (f) return { tex: piFracTex(f[0], f[1]), text: piFracText(f[0], f[1]), exact: true };
    var r = piVal * Math.PI;
    var s2 = fmtNum(r, 2);
    return { tex: s2, text: minus(s2), exact: Math.abs(r - Number(s2)) < 1e-7 };
  }

  // よく出てくる無理数（sin・cos・tan の有名角の値）
  var NICE = [
    [Math.sqrt(2) / 2, "\\frac{\\sqrt{2}}{2}", "√2/2"],
    [Math.sqrt(3) / 2, "\\frac{\\sqrt{3}}{2}", "√3/2"],
    [Math.sqrt(3), "\\sqrt{3}", "√3"],
    [1 / Math.sqrt(3), "\\frac{1}{\\sqrt{3}}", "1/√3"],
    [Math.sqrt(2), "\\sqrt{2}", "√2"],
    [(Math.sqrt(6) - Math.sqrt(2)) / 4, "\\frac{\\sqrt{6}-\\sqrt{2}}{4}", "(√6−√2)/4"],
    [(Math.sqrt(6) + Math.sqrt(2)) / 4, "\\frac{\\sqrt{6}+\\sqrt{2}}{4}", "(√6+√2)/4"],
    [2 - Math.sqrt(3), "2-\\sqrt{3}", "2−√3"],
    [2 + Math.sqrt(3), "2+\\sqrt{3}", "2+√3"],
  ];

  /**
   * 数値 v を、ぴったり表せるなら有理数・有名な無理数で、そうでなければ小数で表す。
   * 戻り値 {tex, text, exact}
   */
  function exactValue(v, digits) {
    var f = toFrac(v, 12);
    if (f) {
      var sg = f[0] < 0 ? "-" : "";
      var an = Math.abs(f[0]);
      if (f[1] === 1) return { tex: String(f[0]), text: minus(String(f[0])), exact: true };
      return { tex: sg + "\\frac{" + an + "}{" + f[1] + "}", text: (sg ? MINUS : "") + an + "/" + f[1], exact: true };
    }
    for (var i = 0; i < NICE.length; i++) {
      var n = NICE[i];
      if (Math.abs(Math.abs(v) - n[0]) < 1e-9) {
        var neg = v < 0;
        var tx = n[1];
        // 「−(√6−√2)/4」のような負の 2 項は全体に − をつける
        return { tex: (neg ? "-" : "") + tx, text: (neg ? MINUS : "") + n[2], exact: true };
      }
    }
    var s = fmtNum(v, digits === undefined ? 3 : digits);
    return { tex: s, text: minus(s), exact: false };
  }

  /** 小数表示（{tex, text, exact}） */
  function num(v, digits) {
    var s = fmtNum(v, digits === undefined ? 2 : digits);
    return { tex: s, text: minus(s), exact: Math.abs(v - Number(s)) < 1e-9 };
  }

  /** x 軸の目盛り（π 単位で step 刻み）。値はラジアン */
  function ticks(loPi, hiPi, unit, step) {
    step = step || ((hiPi - loPi) <= 6 ? 0.5 : 1);
    var vals = [], texts = [];
    for (var k = Math.ceil(loPi / step - EPS); k * step <= hiPi + EPS; k++) {
      var q = k * step;
      vals.push(q * Math.PI);
      texts.push(angle(q, unit).text);
    }
    return { vals: vals, texts: texts };
  }

  function linspace(a, b, n) {
    var out = new Array(n);
    for (var i = 0; i < n; i++) out[i] = a + (b - a) * i / (n - 1);
    return out;
  }

  function factorial(n) { var f = 1; for (var i = 2; i <= n; i++) f *= i; return f; }

  var api = {
    EPS: EPS, MINUS: MINUS, gcd: gcd, toFrac: toFrac, fmtNum: fmtNum, minus: minus,
    piFracTex: piFracTex, piFracText: piFracText, angle: angle, exactValue: exactValue, num: num,
    ticks: ticks, linspace: linspace, factorial: factorial,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.TU = api;
})(this);
