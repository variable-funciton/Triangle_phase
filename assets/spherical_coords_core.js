/*
 * 極座標・球面座標・緯度経度と大円距離
 *   角度の引数はすべて「度」。内部でラジアンに直す。
 * テスト: node tests/test_spherical_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  /** 平面の極座標 (r, θ) → (x, y) */
  function polar(r, th) { return [r * Math.cos(th * D), r * Math.sin(th * D)]; }

  /** 球面座標（数学）：r、z 軸からの角 θ、x 軸からの角 φ → (x, y, z) */
  function sph(r, th, ph) {
    var s = Math.sin(th * D);
    return [r * s * Math.cos(ph * D), r * s * Math.sin(ph * D), r * Math.cos(th * D)];
  }

  /** 緯度・経度 → 半径 R の球面上の点。緯度 = 90° − θ、経度 = φ */
  function geo(lat, lon, R) {
    R = R === undefined ? 1 : R;
    var c = Math.cos(lat * D);
    return [R * c * Math.cos(lon * D), R * c * Math.sin(lon * D), R * Math.sin(lat * D)];
  }

  /** (x, y, z) → [緯度, 経度]（度） */
  function toGeo(v) {
    var r = Math.hypot(v[0], v[1], v[2]);
    return [Math.asin(Math.max(-1, Math.min(1, v[2] / r))) / D, Math.atan2(v[1], v[0]) / D];
  }

  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function norm(a) { var r = Math.hypot(a[0], a[1], a[2]); return [a[0] / r, a[1] / r, a[2] / r]; }

  /** 2 点の中心角（度）。atan2 を使うと、ごく近い 2 点でも誤差が小さい */
  function centralAngle(lat1, lon1, lat2, lon2) {
    var p = geo(lat1, lon1), q = geo(lat2, lon2);
    var c = cross(p, q);
    return Math.atan2(Math.hypot(c[0], c[1], c[2]), dot(p, q)) / D;
  }

  /**
   * 球面の余弦法則（北極 N を頂点とする球面三角形）で求めた cos（中心角）
   *   cos θ = cos(90° − φ1) cos(90° − φ2) + sin(90° − φ1) sin(90° − φ2) cos Δλ
   *         = sin φ1 sin φ2 + cos φ1 cos φ2 cos Δλ
   */
  function cosCentral(lat1, lon1, lat2, lon2) {
    return Math.sin(lat1 * D) * Math.sin(lat2 * D) + Math.cos(lat1 * D) * Math.cos(lat2 * D) * Math.cos((lon2 - lon1) * D);
  }

  /** 大円距離（半径 R、中心角 × R） */
  function distance(lat1, lon1, lat2, lon2, R) { return R * centralAngle(lat1, lon1, lat2, lon2) * D; }

  /** 緯線（緯度 lat の円）の長さ 2πR cos(緯度) */
  function latCircle(lat, R) { return 2 * Math.PI * R * Math.cos(lat * D); }

  /** 大円の弧（球面上の最短の道）の点列 [[x, y, z], ...]（半径 R） */
  function greatArc(lat1, lon1, lat2, lon2, n, R) {
    n = n || 60; R = R === undefined ? 1 : R;
    var p = geo(lat1, lon1), q = geo(lat2, lon2), w = Math.acos(Math.max(-1, Math.min(1, dot(p, q)))), out = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n, v;
      if (w < 1e-9) v = p;
      else {
        var a = Math.sin((1 - t) * w) / Math.sin(w), b = Math.sin(t * w) / Math.sin(w);
        v = [a * p[0] + b * q[0], a * p[1] + b * q[1], a * p[2] + b * q[2]];
      }
      out.push([R * v[0], R * v[1], R * v[2]]);
    }
    return out;
  }

  /** 経度の差を −180°〜180° にそろえる */
  function wrapLon(d) { d = ((d + 180) % 360 + 360) % 360 - 180; return d; }

  /** 地図（緯度・経度をそのまま縦横にした地図）の上で、2 点を直線で結んだ道の点列 [[緯度, 経度], ...] */
  function mapLine(lat1, lon1, lat2, lon2, n) {
    n = n || 60;
    var dl = wrapLon(lon2 - lon1), out = [];
    for (var i = 0; i <= n; i++) out.push([lat1 + (lat2 - lat1) * i / n, lon1 + dl * i / n]);
    return out;
  }

  /** 点列 [[x, y, z]] の長さ（折れ線） */
  function pathLength(pts) {
    var s = 0;
    for (var i = 1; i < pts.length; i++) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1], pts[i][2] - pts[i - 1][2]);
    return s;
  }

  /** [[緯度, 経度]] → 球面上の点列 */
  function geoPath(ll, R) { return ll.map(function (p) { return geo(p[0], p[1], R); }); }

  /** 大円の弧を [[緯度, 経度]] で（地図にかくため。経度は連続になるようにつなぐ） */
  function greatArcLL(lat1, lon1, lat2, lon2, n) {
    var pts = greatArc(lat1, lon1, lat2, lon2, n), out = [], prev = null;
    pts.forEach(function (v) {
      var g = toGeo(v);
      if (prev !== null) g[1] = prev + wrapLon(g[1] - prev);
      prev = g[1]; out.push(g);
    });
    return out;
  }

  var CITIES = [
    { key: "tokyo", name: "東京", lat: 35.68, lon: 139.69 },
    { key: "osaka", name: "大阪", lat: 34.69, lon: 135.50 },
    { key: "sapporo", name: "札幌", lat: 43.06, lon: 141.35 },
    { key: "naha", name: "那覇", lat: 26.21, lon: 127.68 },
    { key: "singapore", name: "シンガポール", lat: 1.35, lon: 103.82 },
    { key: "sydney", name: "シドニー", lat: -33.87, lon: 151.21 },
    { key: "london", name: "ロンドン", lat: 51.51, lon: -0.13 },
    { key: "newyork", name: "ニューヨーク", lat: 40.71, lon: -74.01 },
    { key: "sf", name: "サンフランシスコ", lat: 37.77, lon: -122.42 },
  ];
  function city(key) { for (var i = 0; i < CITIES.length; i++) if (CITIES[i].key === key) return CITIES[i]; return CITIES[0]; }

  /** 緯度・経度を「北緯 35.68°」のような文字に */
  function latText(lat) { return (lat >= 0 ? "北緯 " : "南緯 ") + Math.abs(lat).toFixed(2).replace(/\.?0+$/, "") + "°"; }
  function lonText(lon) { return (lon >= 0 ? "東経 " : "西経 ") + Math.abs(lon).toFixed(2).replace(/\.?0+$/, "") + "°"; }

  var api = { D: D, polar: polar, sph: sph, geo: geo, toGeo: toGeo, dot: dot, cross: cross, norm: norm, centralAngle: centralAngle,
    cosCentral: cosCentral, distance: distance, latCircle: latCircle, greatArc: greatArc, greatArcLL: greatArcLL, wrapLon: wrapLon,
    mapLine: mapLine, pathLength: pathLength, geoPath: geoPath, CITIES: CITIES, city: city, latText: latText, lonText: lonText };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SC = api;
})(this);
