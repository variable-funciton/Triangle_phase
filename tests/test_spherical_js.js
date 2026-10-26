// 球面座標・球面三角形の計算のテスト:  node tests/test_spherical_js.js
const assert = require("assert");
const near = (a, b, e) => assert.ok(Math.abs(a - b) < (e || 1e-9), `${a} != ${b}`);
const SC = require("../assets/spherical_coords_core.js"), ST = require("../assets/spherical_triangle_core.js");
const D = Math.PI / 180;

// ---- 極座標・球面座標 ----
near(SC.polar(2, 60)[0], 1); near(SC.polar(2, 60)[1], Math.sqrt(3));
for (const [r, th, ph] of [[1, 30, 45], [2, 120, 200], [3, 90, 0], [1.5, 10, 300]]) {
  const v = SC.sph(r, th, ph);
  near(Math.hypot(...v), r);
  near(v[2], r * Math.cos(th * D)); near(Math.hypot(v[0], v[1]), r * Math.sin(th * D));
  // 緯度 = 90° − θ、経度 = φ
  const g = SC.geo(90 - th, ph, r); g.forEach((x, i) => near(x, v[i]));
  const ll = SC.toGeo(v); near(ll[0], 90 - th); near(SC.wrapLon(ll[1] - ph), 0, 1e-9);
}
// 中心角：球面の余弦法則と一致
for (const [a, b] of [["tokyo", "london"], ["tokyo", "newyork"], ["sydney", "sf"], ["tokyo", "osaka"]]) {
  const p = SC.city(a), q = SC.city(b);
  near(Math.cos(SC.centralAngle(p.lat, p.lon, q.lat, q.lon) * D), SC.cosCentral(p.lat, p.lon, q.lat, q.lon), 1e-12);
  // 大円の弧の長さ = 中心角、地図上の直線は大円より長い（同じ経線・赤道上以外）
  const arc = SC.greatArc(p.lat, p.lon, q.lat, q.lon, 400);
  near(SC.pathLength(arc), SC.centralAngle(p.lat, p.lon, q.lat, q.lon) * D, 1e-5);
  const ml = SC.pathLength(SC.geoPath(SC.mapLine(p.lat, p.lon, q.lat, q.lon, 400)));
  assert.ok(ml >= SC.pathLength(arc) - 1e-9);
  const gl = SC.greatArcLL(p.lat, p.lon, q.lat, q.lon, 50);
  for (let i = 1; i < gl.length; i++) assert.ok(Math.abs(gl[i][1] - gl[i - 1][1]) < 30);  // 経度が連続
}
near(SC.distance(0, 0, 0, 90, 6400), 3200 * Math.PI);           // 赤道上で 90°
near(SC.distance(30, 135, 60, 135, 6400), 6400 * Math.PI / 6);  // 同じ経線上
near(SC.latCircle(60, 6400), 6400 * Math.PI);
const tl = SC.distance(35.68, 139.69, 51.51, -0.13, 6371);
assert.ok(tl > 9500 && tl < 9620, String(tl));                   // 東京–ロンドン 約 9560 km
near(SC.wrapLon(190), -170); near(SC.wrapLon(-200), 160);

// ---- 球面三角形 ----
const o = ST.solve(ST.PRESETS[0].V);
near(o.a, Math.PI / 2); near(o.b, Math.PI / 2); near(o.c, Math.PI / 2);
near(o.alpha, Math.PI / 2); near(o.beta, Math.PI / 2); near(o.gamma, Math.PI / 2);
near(o.E, Math.PI / 2); near(o.lhuilier, Math.PI / 2, 1e-9);     // 球面の 1/8 = 4π/8
const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
for (let k = 0; k < 300; k++) {
  const V = [0, 1, 2].map(() => [Math.asin(2 * rnd() - 1) / D, 360 * rnd() - 180]);
  const t = ST.solve(V);
  if (t.degenerate || Math.min(t.a, t.b, t.c) < 0.02) continue;
  // 余弦法則で求めた角 = ベクトルで求めた角
  near(ST.angleFromSides(t.a, t.b, t.c), t.alpha, 1e-6);
  near(ST.angleFromSides(t.b, t.c, t.a), t.beta, 1e-6);
  near(ST.angleFromSides(t.c, t.a, t.b), t.gamma, 1e-6);
  near(Math.cos(t.c), Math.cos(t.a) * Math.cos(t.b) + Math.sin(t.a) * Math.sin(t.b) * Math.cos(t.gamma), 1e-9);
  // 正弦法則
  near(Math.sin(t.alpha) / Math.sin(t.a), Math.sin(t.beta) / Math.sin(t.b), 1e-6);
  // ジラール = リュイリエ、角の和は π より大きく 5π より小さい
  near(t.E, t.lhuilier, 1e-6);
  assert.ok(t.sum > Math.PI && t.sum < 5 * Math.PI);
}
// 縮めると E → 0、面積は平面の三角形に近づく
const big = ST.PRESETS[1].V;
let prev = Infinity;
for (const k of [1, 0.5, 0.2, 0.05, 0.01]) {
  const t = ST.solve(ST.shrink(big, k));
  assert.ok(t.E < prev); prev = t.E;
  if (k <= 0.05) near(t.E / t.flat, 1, 0.01);
}
const m = ST.angleMark(ST.geo(0, 0), ST.geo(0, 90), ST.geo(90, 0), 0.1, 10);
near(ST.arc(m[0], ST.geo(0, 0)), 0.1); near(ST.arc(m[10], ST.geo(0, 0)), 0.1);
console.log("spherical js: ok");
