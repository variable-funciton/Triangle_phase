/*
 * 観覧車のゴンドラの高さ  h(t) = h0 − r cos(2πt / T)
 *   r: 半径 [m]、T: 1 周の時間 [分]、h0: 中心（軸）の高さ [m] = r + 乗り場の高さ
 * テスト: node tests/test_applied_js.js
 */
(function (root) {
  "use strict";

  function height(p, t) { return p.h0 - p.r * Math.cos(2 * Math.PI * t / p.T); }

  /** ゴンドラの位置（観覧車の中心を原点、乗り場が真下、反時計回り） */
  function position(p, t) {
    var th = 2 * Math.PI * t / p.T;
    return [p.r * Math.sin(th), p.h0 - p.r * Math.cos(th)];
  }

  /**
   * 高さ H 以上にいる時間帯（1 周目）。cos θ ≦ c (c = (h0 − H)/r) となる θ の範囲
   * 戻り値 {t1, t2, duration}（ずっと上なら t1 = 0, t2 = T、届かないなら duration = 0）
   */
  function above(p, H) {
    var c = (p.h0 - H) / p.r;
    if (c >= 1) return { t1: 0, t2: p.T, duration: p.T, all: true };
    if (c <= -1) return { t1: 0, t2: 0, duration: 0, none: true };
    var a = Math.acos(c);                        // 0 < a < π
    var t1 = p.T * a / (2 * Math.PI), t2 = p.T - t1;
    return { t1: t1, t2: t2, duration: t2 - t1 };
  }

  var api = { height: height, position: position, above: above };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.FW = api;
})(this);
