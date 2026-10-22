/*
 * X 線回折（ブラッグの法則）  2d sin θ = nλ
 *   となり合う原子の面で反射した X 線の道のりの差は 2d sin θ。これが波長の整数倍のとき、波が強め合う。
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  function pathDiff(d, thDeg) { return 2 * d * Math.sin(thDeg * D); }

  /** 強め合う角度 θ_n（n = 1, 2, …）[°]。2d sin θ = nλ をみたすもの */
  function braggAngles(d, lam) {
    var out = [];
    for (var n = 1; n * lam <= 2 * d + 1e-12; n++) out.push({ n: n, th: Math.asin(n * lam / (2 * d)) / D });
    return out;
  }

  /**
   * N 枚の面からの反射を重ね合わせた強さ（最大を 1 に）。
   * 位相差 δ = 2π (2d sin θ)/λ、強さ ∝ sin²(Nδ/2) / sin²(δ/2)
   */
  function intensity(d, lam, thDeg, N) {
    var delta = 2 * Math.PI * pathDiff(d, thDeg) / lam;
    var s = Math.sin(delta / 2);
    if (Math.abs(s) < 1e-9) return 1;
    var v = Math.sin(N * delta / 2) / (N * s);
    return v * v;
  }

  /** 2 つの波の和の振幅（道のりの差 Δ のとき 2|cos(πΔ/λ)|） */
  function twoWaveAmp(d, lam, thDeg) { return 2 * Math.abs(Math.cos(Math.PI * pathDiff(d, thDeg) / lam)); }

  var api = { pathDiff: pathDiff, braggAngles: braggAngles, intensity: intensity, twoWaveAmp: twoWaveAmp };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.BR = api;
})(this);
