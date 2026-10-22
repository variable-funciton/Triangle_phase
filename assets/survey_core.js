/*
 * 測量と三角比
 *   ① 高さ：距離 d、仰角 θ、目の高さ e → 高さ H = d tan θ + e
 *   ② 川幅（三角測量）：基線 AB = c、∠A = α、∠B = β → AC = c sin β / sin(α + β)（正弦定理）、川幅 = AC sin α
 *   ③ トラバース測量：方位角 a（北から時計回り）、距離 L → Δx（北）= L cos a、Δy（東）= L sin a
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  function height(d, thDeg, eye) { return d * Math.tan(thDeg * D) + (eye || 0); }

  /** C の位置（A を原点、B を (c, 0)、C は上側）と、AC、川幅（C から AB への距離） */
  function triangulate(c, aDeg, bDeg) {
    var a = aDeg * D, b = bDeg * D, g = Math.PI - a - b;
    if (g <= 0) return null;
    var AC = c * Math.sin(b) / Math.sin(g), BC = c * Math.sin(a) / Math.sin(g);
    return { AC: AC, BC: BC, gamma: g / D, C: [AC * Math.cos(a), AC * Math.sin(a)], width: AC * Math.sin(a) };
  }

  // トラバース：真の測点（x = 北, y = 東）[m]
  var TRUE_PTS = [[0, 0], [62.4, 38.1], [41.7, 105.3], [-20.5, 96.0], [-48.2, 33.6]];

  /** 方位角 [°]（北から時計回り、0〜360） */
  function bearing(p, q) { var a = Math.atan2(q[1] - p[1], q[0] - p[0]) / D; return (a + 360) % 360; }

  /** 真の測点から、各辺の距離と方位角（測った値）を作る。err で決まった大きさの誤差を加える */
  var NOISE = [[0.6, -0.4], [-0.9, 0.7], [0.3, 1.0], [-0.5, -0.8], [0.8, 0.2]];
  function measurements(errAngle, errDist) {
    var n = TRUE_PTS.length, out = [];
    for (var i = 0; i < n; i++) {
      var p = TRUE_PTS[i], q = TRUE_PTS[(i + 1) % n];
      var L = Math.hypot(q[0] - p[0], q[1] - p[1]), a = bearing(p, q);
      out.push({ L: L + NOISE[i][1] * errDist, a: a + NOISE[i][0] * errAngle, Ltrue: L, atrue: a });
    }
    return out;
  }

  /** 測った値から座標を順に計算。最後の点が出発点にもどらない分が閉合誤差 */
  function traverse(meas) {
    var pts = [[0, 0]], x = 0, y = 0, total = 0;
    meas.forEach(function (m) {
      var dx = m.L * Math.cos(m.a * D), dy = m.L * Math.sin(m.a * D);
      m.dx = dx; m.dy = dy; x += dx; y += dy; total += m.L; pts.push([x, y]);
    });
    var err = Math.hypot(x, y);
    return { pts: pts, closure: err, total: total, ratio: err > 1e-9 ? total / err : Infinity, ex: x, ey: y };
  }

  var api = { height: height, triangulate: triangulate, TRUE_PTS: TRUE_PTS, bearing: bearing, measurements: measurements, traverse: traverse };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SV = api;
})(this);
