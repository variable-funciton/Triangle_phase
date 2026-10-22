/*
 * 交流の電力と力率
 *   v = Vm sin ωt、 i = Im sin(ωt − φ)
 *   p = v i = (Vm Im / 2) {cos φ − cos(2ωt − φ)}   （積和の公式  sin A sin B = −{cos(A+B) − cos(A−B)}/2）
 *   平均の電力 P = (Vm Im / 2) cos φ = V I cos φ（V, I は実効値）。cos φ を力率という。
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";

  function power(Vm, Im, phi, wt) { return Vm * Math.sin(wt) * Im * Math.sin(wt - phi); }
  function powerFormula(Vm, Im, phi, wt) { return Vm * Im / 2 * (Math.cos(phi) - Math.cos(2 * wt - phi)); }

  /** 1 周期の平均（数値） */
  function meanPower(Vm, Im, phi, n) {
    n = n || 2000; var s = 0;
    for (var i = 0; i < n; i++) s += power(Vm, Im, phi, 2 * Math.PI * (i + 0.5) / n);
    return s / n;
  }

  var api = { power: power, powerFormula: powerFormula, meanPower: meanPower };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PW = api;
})(this);
