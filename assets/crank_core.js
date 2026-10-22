/*
 * ピストン・クランク機構
 *   クランクの中心 O を原点、クランク半径 r、連接棒（コンロッド）の長さ l、クランク角 θ
 *   クランクピン P = (r cos θ, r sin θ)、ピストンの位置 x = r cos θ + √(l² − r² sin² θ)
 *   （三角形 OPQ に余弦定理  l² = r² + x² − 2 r x cos θ  を使って x について解いたもの）
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";

  function piston(r, l, th) { return r * Math.cos(th) + Math.sqrt(l * l - r * r * Math.sin(th) * Math.sin(th)); }

  /** 単振動で近似した位置（l が r よりずっと長いとき）： x ≈ l + r cos θ */
  function shm(r, l, th) { return l + r * Math.cos(th); }

  /** 連接棒が水平となす角 φ（正弦定理  r / sin φ = l / sin θ  から sin φ = r sin θ / l） */
  function rodAngle(r, l, th) { return Math.asin(r * Math.sin(th) / l); }

  /** 余弦定理が成り立っているかの確認用：l² − (r² + x² − 2 r x cos θ) */
  function cosineCheck(r, l, th) { var x = piston(r, l, th); return l * l - (r * r + x * x - 2 * r * x * Math.cos(th)); }

  var api = { piston: piston, shm: shm, rodAngle: rodAngle, cosineCheck: cosineCheck };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CR = api;
})(this);
