/*
 * 回転と弧度法：角速度・周速・転がる距離・歯車とベルトの回転数比
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";

  /** 回転数 N [rpm]（1 分あたりの回転数）→ 角速度 ω [rad/s] */
  function omega(N) { return 2 * Math.PI * N / 60; }

  /** 周速（円周上の点の速さ）v = r ω  [r の単位/s] */
  function speed(r, N) { return r * omega(N); }

  /** 歯車：かみ合う 2 つの歯車の回転数  N2 = N1 × z1 / z2（反対向き） */
  function gearN2(N1, z1, z2) { return N1 * z1 / z2; }

  /** ベルト車：N2 = N1 × r1 / r2（同じ向き）。ベルトの速さ r1 ω1 = r2 ω2 */
  function beltN2(N1, r1, r2) { return N1 * r1 / r2; }

  /** 歯車の輪郭（歯数 z、ピッチ円半径 R、歯の高さ h、回転角 rot） */
  function gearOutline(cx, cy, R, z, h, rot, n) {
    n = n || z * 16;
    var xs = [], ys = [];
    for (var i = 0; i <= n; i++) {
      var a = 2 * Math.PI * i / n;
      var s = Math.sin(z * a);
      var rr = R + h * Math.max(-1, Math.min(1, 2.2 * s)) / 2;   // 台形に近い歯
      xs.push(cx + rr * Math.cos(a + rot)); ys.push(cy + rr * Math.sin(a + rot));
    }
    return { x: xs, y: ys };
  }

  var api = { omega: omega, speed: speed, gearN2: gearN2, beltN2: beltN2, gearOutline: gearOutline };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.RO = api;
})(this);
