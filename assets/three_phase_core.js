/*
 * 三相交流  va = sin θ、 vb = sin(θ − d)、 vc = sin(θ − 2d)（ふつうは d = 120°）
 *   d = 120° のとき va + vb + vc = 0（sin(θ − 120°) + sin(θ + 120°) = 2 sin θ cos 120° = −sin θ）
 *   線間電圧 va − vb = √3 sin(θ + 30°)
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  function phases(Vm, th, dDeg) {
    var d = dDeg * D;
    return [Vm * Math.sin(th), Vm * Math.sin(th - d), Vm * Math.sin(th - 2 * d)];
  }
  function sum(Vm, th, dDeg) { var p = phases(Vm, th, dDeg); return p[0] + p[1] + p[2]; }

  /** 3 つの和の最大値（d によって変わる。d = 120° なら 0） */
  function sumAmplitude(Vm, dDeg) {
    var d = dDeg * D, re = 1 + Math.cos(d) + Math.cos(2 * d), im = -Math.sin(d) - Math.sin(2 * d);
    return Vm * Math.sqrt(re * re + im * im);
  }

  /** 線間電圧 va − vb の最大値（d = 120° なら √3 Vm） */
  function lineAmplitude(Vm, dDeg) { return Vm * 2 * Math.abs(Math.sin(dDeg * D / 2)); }

  var api = { phases: phases, sum: sum, sumAmplitude: sumAmplitude, lineAmplitude: lineAmplitude };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.TP = api;
})(this);
