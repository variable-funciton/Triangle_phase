/*
 * 勾配の表し方
 *   角度 θ、パーセント p = 100 tan θ [%]、パーミル 1000 tan θ [‰]、寸勾配（水平 10 寸に対する高さ [寸]）= 10 tan θ、
 *   比 1 : n（高さ 1 に対して水平 n）n = 1 / tan θ
 *   斜面に沿った長さ s と水平距離 = s cos θ、高さ = s sin θ
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  function fromAngle(thDeg) {
    var t = Math.tan(thDeg * D);
    return { deg: thDeg, tan: t, percent: 100 * t, permil: 1000 * t, sun: 10 * t, ratioN: t > 0 ? 1 / t : Infinity };
  }
  function angleFromPercent(p) { return Math.atan(p / 100) / D; }

  // 身近な勾配の例（角度でなく tan の値で決まっているものが多い）
  var EXAMPLES = [
    { name: "車いす用スロープ（1/12）", tan: 1 / 12 },
    { name: "鉄道の急な坂（80‰）", tan: 0.08 },
    { name: "急な道路「10%」の標識", tan: 0.1 },
    { name: "屋根の 4 寸勾配", tan: 0.4 },
    { name: "45°（100%）", tan: 1 },
  ];

  var api = { fromAngle: fromAngle, angleFromPercent: angleFromPercent, EXAMPLES: EXAMPLES };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SL = api;
})(this);
