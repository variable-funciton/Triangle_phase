/*
 * 交流  v = Vm sin(2π f t)、 i = Im sin(2π f t − φ)
 *   実効値 Ve = Vm / √2（v² の平均が Vm²/2 になることから。sin²x = (1 − cos 2x)/2）
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";

  function v(Vm, f, t, ph) { return Vm * Math.sin(2 * Math.PI * f * t - (ph || 0)); }

  /** 1 周期の v² の平均（数値で計算） */
  function meanSquare(Vm, f, n) {
    n = n || 2000; var T = 1 / f, s = 0;
    for (var i = 0; i < n; i++) { var x = v(Vm, f, T * (i + 0.5) / n); s += x * x; }
    return s / n;
  }

  function rms(Vm) { return Vm / Math.SQRT2; }

  var api = { v: v, meanSquare: meanSquare, rms: rms };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.AC = api;
})(this);
