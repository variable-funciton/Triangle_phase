/*
 * 分子の形と結合角
 *   中心の原子から 2 つの原子までの距離（結合距離）を a、結合角を θ とすると、
 *   2 つの原子の間の距離  d² = a² + a² − 2a·a cos θ  （余弦定理）、 d = 2a sin(θ/2)
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";

  // 結合距離 [nm] と結合角 [°]（代表的な値）
  var MOLECULES = [
    { key: "co2", name: "二酸化炭素 CO₂", center: "C", side: "O", a: 0.116, angle: 180, shape: "直線形" },
    { key: "bf3", name: "三フッ化ホウ素 BF₃", center: "B", side: "F", a: 0.131, angle: 120, shape: "平面三角形" },
    { key: "ch4", name: "メタン CH₄", center: "C", side: "H", a: 0.109, angle: 109.5, shape: "正四面体形" },
    { key: "nh3", name: "アンモニア NH₃", center: "N", side: "H", a: 0.101, angle: 106.7, shape: "三角錐形" },
    { key: "h2o", name: "水 H₂O", center: "O", side: "H", a: 0.096, angle: 104.5, shape: "折れ線形" },
  ];

  function distance(a, thDeg) { var t = thDeg * Math.PI / 180; return Math.sqrt(2 * a * a - 2 * a * a * Math.cos(t)); }
  function distanceHalf(a, thDeg) { return 2 * a * Math.sin(thDeg * Math.PI / 360); }

  /** 正四面体の結合角：立方体の中心から、となり合わない 4 頂点へのベクトルのなす角。cos θ = −1/3 */
  var TETRA = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]];
  function angleBetween(u, v) {
    var dot = u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
    var nu = Math.hypot(u[0], u[1], u[2]), nv = Math.hypot(v[0], v[1], v[2]);
    return Math.acos(dot / (nu * nv)) * 180 / Math.PI;
  }

  var api = { MOLECULES: MOLECULES, distance: distance, distanceHalf: distanceHalf, TETRA: TETRA, angleBetween: angleBetween };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.MO = api;
})(this);
