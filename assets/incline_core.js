/*
 * 斜面上の物体と力の分解
 *   重力 mg を、斜面に平行な成分 mg sin θ と、斜面に垂直な成分 mg cos θ に分ける。
 *   最大摩擦力 μ N = μ mg cos θ。 mg sin θ > μ mg cos θ（tan θ > μ）ですべり出す。
 *   ここでは簡単のため、静止摩擦係数と動摩擦係数を同じ μ とする。
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var G = 9.8;

  function forces(m, thDeg, mu) {
    var th = thDeg * Math.PI / 180, W = m * G;
    var along = W * Math.sin(th), normal = W * Math.cos(th), fmax = mu * normal;
    var slides = along > fmax + 1e-12;
    return { W: W, along: along, normal: normal, fmax: fmax, slides: slides,
      friction: slides ? fmax : along, accel: slides ? G * (Math.sin(th) - mu * Math.cos(th)) : 0 };
  }

  /** 摩擦角（すべり出す角度） tan θ = μ */
  function frictionAngle(mu) { return Math.atan(mu) * 180 / Math.PI; }

  var api = { G: G, forces: forces, frictionAngle: frictionAngle };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.IC = api;
})(this);
