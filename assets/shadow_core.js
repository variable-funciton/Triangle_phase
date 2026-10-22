/*
 * 太陽の高さと影（日影）
 *   φ: 緯度、δ: 太陽の赤緯（夏至 +23.4°、春分・秋分 0°、冬至 −23.4°）、H: 時角（正午 0°、1 時間で 15°）
 *   太陽の向き（東・北・上の成分）
 *     東 = −cos δ sin H、 北 = sin δ cos φ − cos δ cos H sin φ、 上 = sin δ sin φ + cos δ cos H cos φ
 *   南中高度 h = 90° − φ + δ、 影の長さ L = (高さ) / tan h
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";
  var D = Math.PI / 180;

  function declination(N) { return 23.44 * Math.sin(2 * Math.PI * (N - 81) / 365); }

  /** 太陽の向きの単位ベクトル [東, 北, 上]。hour: 太陽時（12 が南中） */
  function sunVector(lat, decl, hour) {
    var p = lat * D, d = decl * D, H = (hour - 12) * 15 * D;
    return [-Math.cos(d) * Math.sin(H), Math.sin(d) * Math.cos(p) - Math.cos(d) * Math.cos(H) * Math.sin(p),
      Math.sin(d) * Math.sin(p) + Math.cos(d) * Math.cos(H) * Math.cos(p)];
  }

  function altitude(lat, decl, hour) { return Math.asin(Math.max(-1, Math.min(1, sunVector(lat, decl, hour)[2]))) / D; }

  /** 南中高度 [°] */
  function noonAltitude(lat, decl) { return 90 - lat + decl; }

  /** 高さ h の棒の影の先端 [東, 北]（太陽が地平線の下なら null） */
  function shadowTip(lat, decl, hour, h) {
    var s = sunVector(lat, decl, hour);
    if (s[2] <= 0.01) return null;
    return [-h * s[0] / s[2], -h * s[1] / s[2]];
  }

  /** 影の長さ L = h / tan(太陽高度) */
  function shadowLength(h, altDeg) { return altDeg <= 0 ? Infinity : h / Math.tan(altDeg * D); }

  /** 南中時に北側の建物に日が当たるための最小の間隔 */
  function minSpacing(Hb, lat, decl) { return shadowLength(Hb, noonAltitude(lat, decl)); }

  var api = { declination: declination, sunVector: sunVector, altitude: altitude, noonAltitude: noonAltitude, shadowTip: shadowTip, shadowLength: shadowLength, minSpacing: minSpacing };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SH = api;
})(this);
