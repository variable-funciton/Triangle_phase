/*
 * 球面三角形（単位球）：辺（中心角）・角・球過量・面積
 *   頂点は緯度・経度（度）で与える。辺・角の戻り値はラジアン。
 * テスト: node tests/test_spherical_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  function geo(lat, lon) { var c = Math.cos(lat * D); return [c * Math.cos(lon * D), c * Math.sin(lon * D), Math.sin(lat * D)]; }
  function toGeo(v) { var r = Math.hypot(v[0], v[1], v[2]); return [Math.asin(Math.max(-1, Math.min(1, v[2] / r))) / D, Math.atan2(v[1], v[0]) / D]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function len(a) { return Math.hypot(a[0], a[1], a[2]); }
  function norm(a) { var r = len(a); return [a[0] / r, a[1] / r, a[2] / r]; }
  function clamp(x) { return Math.max(-1, Math.min(1, x)); }

  /** 2 点の中心角（ラジアン） */
  function arc(p, q) { return Math.atan2(len(cross(p, q)), dot(p, q)); }

  /** p から q へ向かう大円の、p での接線の向き */
  function tangent(p, q) { var d = dot(p, q); return norm([q[0] - d * p[0], q[1] - d * p[1], q[2] - d * p[2]]); }

  /** 頂点 p での角（q と r へ向かう大円のなす角、ラジアン） */
  function vertexAngle(p, q, r) {
    var u = tangent(p, q), w = tangent(p, r);
    return Math.atan2(len(cross(u, w)), dot(u, w));
  }

  /** 辺 a, b, c（ラジアン）から、球面の余弦法則で角 α（辺 a の向かい）を求める */
  function angleFromSides(a, b, c) { return Math.acos(clamp((Math.cos(a) - Math.cos(b) * Math.cos(c)) / (Math.sin(b) * Math.sin(c)))); }

  /** リュイリエの公式で球過量 E（ラジアン） */
  function lhuilier(a, b, c) {
    var s = (a + b + c) / 2;
    var t = Math.tan(s / 2) * Math.tan((s - a) / 2) * Math.tan((s - b) / 2) * Math.tan((s - c) / 2);
    return 4 * Math.atan(Math.sqrt(Math.max(0, t)));
  }

  /** 平面の三角形の面積（ヘロンの公式）。辺は球面上の弧の長さを使う（小さい三角形との比較用） */
  function heron(a, b, c) { var s = (a + b + c) / 2; return Math.sqrt(Math.max(0, s * (s - a) * (s - b) * (s - c))); }

  /**
   * 3 頂点（[緯度, 経度] × 3）から、辺・角・球過量などをまとめて求める
   *   a = BC, b = CA, c = AB（中心角）、α = ∠A, β = ∠B, γ = ∠C
   */
  function solve(V) {
    var A = geo(V[0][0], V[0][1]), B = geo(V[1][0], V[1][1]), C = geo(V[2][0], V[2][1]);
    var a = arc(B, C), b = arc(C, A), c = arc(A, B);
    var al = vertexAngle(A, B, C), be = vertexAngle(B, C, A), ga = vertexAngle(C, A, B);
    var deg = Math.min(a, b, c) < 1e-6 || Math.abs(dot(A, cross(B, C))) < 1e-9;   // 3 点が 1 つの大円の上
    var E = deg ? 0 : al + be + ga - Math.PI;
    return { P: [A, B, C], a: a, b: b, c: c, alpha: al, beta: be, gamma: ga, sum: al + be + ga, E: E, degenerate: deg,
      lhuilier: deg ? 0 : lhuilier(a, b, c), flat: heron(a, b, c) };
  }

  /** p から q へ、中心角の割合 t だけ進んだ点（大円に沿って） */
  function slerp(p, q, t) {
    var w = arc(p, q);
    if (w < 1e-12) return p.slice();
    var s = Math.sin(w), k1 = Math.sin((1 - t) * w) / s, k2 = Math.sin(t * w) / s;
    return [k1 * p[0] + k2 * q[0], k1 * p[1] + k2 * q[1], k1 * p[2] + k2 * q[2]];
  }

  /** 大円の弧の点列 */
  function arcPoints(p, q, n, R) {
    n = n || 50; R = R || 1; var out = [];
    for (var i = 0; i <= n; i++) { var v = slerp(p, q, i / n); out.push([R * v[0], R * v[1], R * v[2]]); }
    return out;
  }

  /** 頂点 p の角を表す小さな弧（球面上、p から中心角 eps の所）の点列 */
  function angleMark(p, q, r, eps, n) {
    n = n || 24; eps = eps || 0.12;
    var u = tangent(p, q), w = tangent(p, r), th = Math.acos(clamp(dot(u, w)));
    // u から w へ回す：w の u に垂直な成分
    var d = dot(u, w), v = norm([w[0] - d * u[0], w[1] - d * u[1], w[2] - d * u[2]]), out = [];
    if (!isFinite(v[0])) v = u;
    for (var i = 0; i <= n; i++) {
      var s = th * i / n, c = Math.cos(s), sn = Math.sin(s);
      var dir = [c * u[0] + sn * v[0], c * u[1] + sn * v[1], c * u[2] + sn * v[2]];
      var ce = Math.cos(eps), se = Math.sin(eps);
      out.push([ce * p[0] + se * dir[0], ce * p[1] + se * dir[1], ce * p[2] + se * dir[2]]);
    }
    return out;
  }

  /** 3 点の「中心」（ベクトルの和の向き） */
  function centroid(V) {
    var P = V.map(function (v) { return geo(v[0], v[1]); });
    var g = norm([P[0][0] + P[1][0] + P[2][0], P[0][1] + P[1][1] + P[2][1], P[0][2] + P[1][2] + P[2][2]]);
    return g;
  }

  /** 三角形を中心に向かって縮める（各頂点を、中心からの中心角の k 倍の所へ）。戻り値は [緯度, 経度] × 3 */
  function shrink(V, k) {
    var g = centroid(V);
    if (!isFinite(g[0])) return V.map(function (v) { return v.slice(); });
    return V.map(function (v) { return toGeo(slerp(g, geo(v[0], v[1]), k)); });
  }

  var PRESETS = [
    { key: "octant", name: "北極と赤道上の 2 点（角がすべて 90°）", V: [[90, 0], [0, 0], [0, 90]] },
    { key: "big", name: "大きな三角形", V: [[70, 20], [-10, -20], [5, 110]] },
    { key: "cities", name: "東京・ロンドン・ニューヨーク", V: [[35.68, 139.69], [51.51, -0.13], [40.71, -74.01]] },
    { key: "japan", name: "札幌・那覇・東京（小さい三角形）", V: [[43.06, 141.35], [26.21, 127.68], [35.68, 139.69]] },
    { key: "lune", name: "細長い三角形（月形に近い）", V: [[80, 0], [-80, 0], [0, 40]] },
  ];

  /** ラジアン → 度 */
  function deg(x) { return x / D; }

  var api = { D: D, geo: geo, toGeo: toGeo, dot: dot, cross: cross, norm: norm, arc: arc, tangent: tangent, vertexAngle: vertexAngle,
    angleFromSides: angleFromSides, lhuilier: lhuilier, heron: heron, solve: solve, slerp: slerp, arcPoints: arcPoints,
    angleMark: angleMark, centroid: centroid, shrink: shrink, PRESETS: PRESETS, deg: deg };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ST = api;
})(this);
