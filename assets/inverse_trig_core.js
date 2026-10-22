/*
 * 逆三角関数の主値（arcsin, arccos, arctan）の計算
 * テスト: node tests/test_widgets_js.js
 */
(function (root) {
  "use strict";
  var TU = root.TU || require("./common_core.js");

  var S3 = Math.sqrt(3), S2 = Math.sqrt(2);
  var SPECS = {
    sin: {
      base: Math.sin, inv: Math.asin, name: "\\sin", inv_tex: "\\arcsin", alt_tex: "\\sin^{-1}",
      dom: [-0.5, 0.5], kmin: -1, kmax: 1, closed: [true, true],
      presets: [-1, -S3 / 2, -S2 / 2, -0.5, 0, 0.5, S2 / 2, S3 / 2, 1],
    },
    cos: {
      base: Math.cos, inv: Math.acos, name: "\\cos", inv_tex: "\\arccos", alt_tex: "\\cos^{-1}",
      dom: [0, 1], kmin: -1, kmax: 1, closed: [true, true],
      presets: [-1, -S3 / 2, -S2 / 2, -0.5, 0, 0.5, S2 / 2, S3 / 2, 1],
    },
    tan: {
      base: Math.tan, inv: Math.atan, name: "\\tan", inv_tex: "\\arctan", alt_tex: "\\tan^{-1}",
      dom: [-0.5, 0.5], kmin: -4, kmax: 4, closed: [false, false],
      presets: [-S3, -1, -1 / S3, 0, 1 / S3, 1, S3],
    },
  };

  /** 主値 θ（π 単位） */
  function principal(fn, k) { return SPECS[fn].inv(k) / Math.PI; }

  /** 主値の範囲（π 単位）を「−π/2 ≦ y ≦ π/2」のような LaTeX に */
  function rangeTex(fn, v) {
    var sp = SPECS[fn];
    var lt = sp.closed[0] ? " \\le " : " < ", rt = sp.closed[1] ? " \\le " : " < ";
    return TU.angle(sp.dom[0], "rad").tex + lt + v + rt + TU.angle(sp.dom[1], "rad").tex;
  }

  function domainTex(fn, v) {
    if (fn === "tan") return "-\\infty < " + v + " < \\infty";
    return "-1 \\le " + v + " \\le 1";
  }

  /**
   * 方程式 f(x) = k の解のうち lo ≦ x < hi（π 単位）にあるものを小さい順に
   * sin: θ + 2nπ, π − θ + 2nπ / cos: ±θ + 2nπ / tan: θ + nπ
   */
  function solutions(fn, k, lo, hi) {
    if (fn !== "tan" && (k < -1 - 1e-12 || k > 1 + 1e-12)) return [];
    var th = principal(fn, Math.max(-1, Math.min(1, k)));
    if (fn === "tan") th = principal(fn, k);
    var bases = fn === "sin" ? [th, 1 - th] : fn === "cos" ? [th, -th] : [th];
    var per = fn === "tan" ? 1 : 2;
    var out = [];
    bases.forEach(function (b) {
      for (var n = Math.floor((lo - b) / per) - 1; b + n * per < hi + 1e-12; n++) {
        var x = b + n * per;
        if (x >= lo - 1e-12 && x < hi - 1e-12) out.push(x);
      }
    });
    out.sort(function (a, b) { return a - b; });
    var uniq = [];
    out.forEach(function (x) { if (!uniq.length || Math.abs(x - uniq[uniq.length - 1]) > 1e-9) uniq.push(x); });
    return uniq;
  }

  /** 角度（π 単位）の表示。π の分数（分母 12 まで）でなければ小数と度 */
  function angleShow(piVal) {
    if (TU.toFrac(piVal, 12)) { var a = TU.angle(piVal, "rad", 12); return { tex: a.tex, text: a.text, exact: true }; }
    var r = TU.fmtNum(piVal * Math.PI, 3), d = TU.fmtNum(piVal * 180, 1);
    return { tex: "\\approx " + r + "\\ (" + d + "^\\circ)", text: "≈ " + TU.minus(r) + "（" + TU.minus(d) + "°）", exact: false };
  }

  /** 項「θ + 2nπ」の LaTeX（θ は π 単位。0 なら「2nπ」だけ） */
  function plusTerm(thTex, per) {
    var p = per === 2 ? "2n\\pi" : "n\\pi";
    if (thTex === "0") return p;
    return thTex + " + " + p;
  }

  /**
   * 一般解の LaTeX。θ がきれいな値でないときは θ のまま書く（呼び出し側で θ ≈ … を添える）
   * sin: x = θ + 2nπ, π − θ + 2nπ / cos: x = ±θ + 2nπ / tan: x = θ + nπ
   */
  function generalTex(fn, k) {
    var th = principal(fn, fn === "tan" ? k : Math.max(-1, Math.min(1, k)));
    var exact = !!TU.toFrac(th, 12);
    var T = exact ? TU.angle(th, "rad", 12).tex : "\\theta";
    if (fn === "sin") {
      var T2 = exact ? TU.angle(1 - th, "rad", 12).tex : "\\pi - \\theta";
      var d = (((1 - 2 * th) % 2) + 2) % 2;
      if (exact && (d < 1e-9 || d > 2 - 1e-9)) return "x = " + plusTerm(T, 2);
      return "x = " + plusTerm(T, 2) + ",\\quad x = " + plusTerm(T2, 2);
    }
    if (fn === "cos") {
      if (exact && (Math.abs(th) < 1e-9 || Math.abs(th - 1) < 1e-9)) return "x = " + plusTerm(T, 2);
      return "x = \\pm " + T + " + 2n\\pi";
    }
    return "x = " + plusTerm(T, 1);
  }

  /** 基本の関数を [lo, hi]（ラジアン）で描く点列。tan は漸近線の近くで切る */
  function curve(fn, lo, hi, n) {
    n = n || 800;
    var xs = [], ys = [], f = SPECS[fn].base;
    for (var i = 0; i < n; i++) {
      var x = lo + (hi - lo) * i / (n - 1);
      var y = f(x);
      if (fn === "tan") {
        var c = Math.cos(x);
        if (Math.abs(c) < 0.02) { xs.push(x); ys.push(null); continue; }
      }
      xs.push(x); ys.push(y);
    }
    return { x: xs, y: ys };
  }

  var api = { SPECS: SPECS, principal: principal, rangeTex: rangeTex, domainTex: domainTex,
    solutions: solutions, generalTex: generalTex, angleShow: angleShow, curve: curve };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.IT = api;
})(this);
