/*
 * sin x（cos x）のグラフの接線の傾きを数値で求める（微分の公式は使わない）
 * テスト: node tests/test_widgets_js.js
 */
(function (root) {
  "use strict";
  var TU = root.TU || require("./common_core.js");

  var F = { sin: Math.sin, cos: Math.cos };
  // 傾きのグラフの「答え」（微分を学ぶと分かる）
  var ANSWER = {
    sin: { f: Math.cos, tex: "\\cos x", text: "cos x" },
    cos: { f: function (x) { return -Math.sin(x); }, tex: "-\\sin x", text: "−sin x" },
  };

  /** 2 点 P(a, f(a)), Q(a+h, f(a+h)) を通る直線（割線）の傾き */
  function secantSlope(fn, a, h) { return (F[fn](a + h) - F[fn](a)) / h; }

  /**
   * 接線の傾き。h をとても小さくした割線の傾き（左右対称にとって誤差を小さくする）
   * 小数第 6 位くらいまで正確
   */
  function tangentSlope(fn, a) {
    var h = 1e-5;
    return (F[fn](a + h) - F[fn](a - h)) / (2 * h);
  }

  /** 直線 y = m(x − a) + b を x0〜x1 で */
  function lineSeg(a, b, m, x0, x1) { return { x: [x0, x1], y: [m * (x0 - a) + b, m * (x1 - a) + b] }; }

  /** 有名な角での傾きの表 [角(π 単位), 傾き(数値), 答え(正確な値)] */
  function table(fn) {
    var qs = [0, 1 / 6, 1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 4, 5 / 6, 1, 3 / 2, 2];
    return qs.map(function (q) {
      var a = q * Math.PI;
      return [q, tangentSlope(fn, a), TU.exactValue(ANSWER[fn].f(a))];
    });
  }

  var api = { F: F, ANSWER: ANSWER, secantSlope: secantSlope, tangentSlope: tangentSlope, lineSeg: lineSeg, table: table };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.TS = api;
})(this);
