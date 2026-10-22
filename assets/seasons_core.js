/*
 * 季節の変化：日の長さ（昼の長さ）と月平均気温
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var DEG = Math.PI / 180;

  /** 太陽の赤緯 δ [度] の近似（春分 ≒ 3 月 21 日 = 1 月 1 日から 80 日目 で 0） */
  function declination(N) { return 23.44 * Math.sin(2 * Math.PI * (N - 81) / 365); }

  /**
   * 昼の長さ [時間]（太陽の中心が地平線より上にある時間。大気による屈折などは考えない）
   *   cos H0 = −tan φ tan δ、 昼の長さ = 2 H0 / 15°
   */
  function dayLength(lat, N) {
    var c = -Math.tan(lat * DEG) * Math.tan(declination(N) * DEG);
    if (c <= -1) return 24;
    if (c >= 1) return 0;
    return 2 * Math.acos(c) / DEG / 15;
  }

  // 気象庁の平年値（1991〜2020 年）の月平均気温 [℃]
  var TEMPS = {
    sapporo: { name: "札幌", lat: 43.06, data: [-3.2, -2.7, 1.1, 7.3, 13.0, 17.0, 21.1, 22.3, 18.6, 12.1, 5.2, -0.9] },
    tokyo: { name: "東京", lat: 35.69, data: [5.4, 6.1, 9.4, 14.3, 18.8, 21.9, 25.7, 26.9, 23.3, 18.0, 12.5, 7.7] },
    naha: { name: "那覇", lat: 26.21, data: [17.3, 17.5, 19.1, 21.5, 24.2, 27.2, 29.1, 29.0, 27.9, 25.5, 22.5, 19.0] },
  };

  /** 気温のモデル  T(m) = β + A sin(2π(m − α)/12)  （m は月、1〜12） */
  function model(p, m) { return p.beta + p.A * Math.sin(2 * Math.PI * (m - p.alpha) / 12); }

  /**
   * 12 か月のデータにいちばん合う A, α, β（最小二乗法）。
   * T ≒ β + a sin ωm + b cos ωm と表して、a, b を求め、三角関数の合成で A sin(ωm − ωα) にする。
   */
  function fit(data) {
    var w = 2 * Math.PI / 12, a = 0, b = 0, beta = 0;
    data.forEach(function (T, i) { var m = i + 1; a += T * Math.sin(w * m); b += T * Math.cos(w * m); beta += T; });
    a *= 2 / 12; b *= 2 / 12; beta /= 12;
    var A = Math.sqrt(a * a + b * b);
    var alpha = -Math.atan2(b, a) / w;        // a sin ωm + b cos ωm = A sin(ωm − ωα)
    alpha = ((alpha % 12) + 12) % 12;
    return { A: A, alpha: alpha, beta: beta, a: a, b: b };
  }

  /** ずれの大きさ（二乗平均平方根） */
  function rms(p, data) {
    var s = 0; data.forEach(function (T, i) { var d = model(p, i + 1) - T; s += d * d; });
    return Math.sqrt(s / data.length);
  }

  var MONTH_START = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  /** 1 月 1 日を 1 とした通し日 → "3/21" */
  function dateText(N) {
    var m = 11; while (m > 0 && N <= MONTH_START[m]) m--;
    return (m + 1) + "/" + (N - MONTH_START[m]);
  }

  var api = { declination: declination, dayLength: dayLength, TEMPS: TEMPS, model: model, fit: fit, rms: rms, dateText: dateText, MONTH_START: MONTH_START };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SE = api;
})(this);
