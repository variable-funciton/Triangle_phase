/*
 * リサージュ図形  x = A sin(a t + δ),  y = B sin(b t)
 * テスト: node tests/test_widgets_js.js
 */
(function (root) {
  "use strict";
  var TU = root.TU || require("./common_core.js");

  function point(p, t) { return [p.A * Math.sin(p.a * t + p.delta), p.B * Math.sin(p.b * t)]; }

  /** a : b を簡単な整数比 [p, q] に（分母 12 まで）。できなければ null */
  function ratio(a, b) {
    var f = TU.toFrac(a / b, 12, 1e-7);
    return f && f[0] > 0 ? f : null;
  }

  /** 図形が閉じる（元にもどる）までの時間 T。a = p g, b = q g なら T = 2π q / b。比が簡単でなければ null */
  function period(a, b) {
    var r = ratio(a, b);
    return r ? 2 * Math.PI * r[1] / b : null;
  }

  /** t0〜t1 の軌跡 */
  function curve(p, t0, t1, n) {
    n = n || Math.min(8000, Math.max(600, Math.ceil((t1 - t0) * Math.max(p.a, p.b) * 25)));
    var xs = new Array(n), ys = new Array(n);
    for (var i = 0; i < n; i++) {
      var t = t0 + (t1 - t0) * i / (n - 1);
      xs[i] = p.A * Math.sin(p.a * t + p.delta); ys[i] = p.B * Math.sin(p.b * t);
    }
    return { x: xs, y: ys };
  }

  /** a = b のとき：楕円が y 軸と交わる点の y 座標の絶対値 = B |sin δ| */
  function yIntercept(p) { return p.B * Math.abs(Math.sin(p.delta)); }

  /** 係数の LaTeX（1 は省略） */
  function coefTex(v) { var s = TU.fmtNum(v, 2); return s === "1" ? "" : s; }

  /** 式の LaTeX */
  function formulaTex(p) {
    var d = TU.toFrac(p.delta / Math.PI, 12);
    var dTex = d ? TU.piFracTex(d[0], d[1]) : TU.fmtNum(p.delta, 2);
    var at = coefTex(p.a) + "t", bt = coefTex(p.b) + "t";
    var xIn = dTex === "0" ? "\\sin " + at : "\\sin\\left(" + at + " + " + dTex + "\\right)";
    return "x = " + coefTex(p.A) + xIn + ",\\qquad y = " + coefTex(p.B) + "\\sin " + bt;
  }

  var api = { point: point, ratio: ratio, period: period, curve: curve, yIntercept: yIntercept, formulaTex: formulaTex };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.LJ = api;
})(this);
