/*
 * 一般形 y = A f(B(x − α)) + β の計算と数式の組み立て（ブラウザでも Node でも動く純粋な関数だけ）
 *
 * 角度は「π の何倍か」(piVal) で持つ。例: α = π/3 → 1/3、α = 1.25 rad → 1.25/π。
 * テスト: node tests/test_general_form_js.js
 */
(function (root) {
  "use strict";

  var EPS = 1e-9;
  var MINUS = "−";
  var BASE_KEY_VALUES = { sin: [0, 1, 0, -1, 0], cos: [1, 0, -1, 0, 1] };

  function gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { var t = a % b; a = b; b = t; }
    return a || 1;
  }

  /** x が分母 maxDen 以下の分数とみなせるなら [分子, 分母]（約分済み）、そうでなければ null */
  function toFrac(x, maxDen) {
    maxDen = maxDen || 24;
    for (var d = 1; d <= maxDen; d++) {
      var n = Math.round(x * d);
      if (Math.abs(x * d - n) < EPS * d) {
        var g = gcd(n, d);
        return [n / g, d / g];
      }
    }
    return null;
  }

  /** 小数を最大 digits 桁で表示（末尾の 0 は消す）。-0 は 0 にする */
  function fmtNum(v, digits) {
    if (digits === undefined) digits = 2;
    var s = (Math.round(v * Math.pow(10, digits)) / Math.pow(10, digits)).toFixed(digits);
    if (s.indexOf(".") >= 0) s = s.replace(/0+$/, "").replace(/\.$/, "");
    if (s === "-0") s = "0";
    return s;
  }

  function isZero(v) { return Math.abs(v) < EPS; }
  function isOne(v) { return Math.abs(v - 1) < EPS; }

  // ---------------- 角度の表示 ----------------
  /** π の分数 [n, d] を LaTeX に（符号つき） */
  function piFracTex(n, d) {
    if (n === 0) return "0";
    var sign = n < 0 ? "-" : "";
    var an = Math.abs(n);
    var num = an === 1 ? "\\pi" : an + "\\pi";
    return d === 1 ? sign + num : sign + "\\frac{" + num + "}{" + d + "}";
  }

  function piFracText(n, d) {
    if (n === 0) return "0";
    var sign = n < 0 ? MINUS : "";
    var an = Math.abs(n);
    var num = an === 1 ? "π" : an + "π";
    return d === 1 ? sign + num : sign + num + "/" + d;
  }

  /**
   * 角度（π 単位の値）を表示用に変換する。
   * 弧度法: 分母 24 以下の π の分数なら π を使った形、そうでなければ小数（ラジアン）
   * 度数法: 度（小数 2 桁まで）
   * 戻り値 {tex, text, exact}
   */
  function angle(piVal, unit) {
    if (unit === "deg") {
      var deg = piVal * 180;
      var exactDeg = Math.abs(deg - Math.round(deg * 100) / 100) < 1e-7;
      var s = fmtNum(deg, 2);
      return { tex: s + "^\\circ", text: s.replace("-", MINUS) + "°", exact: exactDeg };
    }
    var f = toFrac(piVal, 24);
    if (f) return { tex: piFracTex(f[0], f[1]), text: piFracText(f[0], f[1]), exact: true };
    var r = piVal * Math.PI;
    var s2 = fmtNum(r, 2);
    return { tex: s2, text: s2.replace("-", MINUS), exact: Math.abs(r - Number(s2)) < 1e-7 };
  }

  function num(v) {
    var s = fmtNum(v, 2);
    return { tex: s, text: s.replace("-", MINUS), exact: Math.abs(v - Number(s)) < 1e-7 };
  }

  // ---------------- 数式 ----------------
  function coefTex(A) {
    if (isOne(A)) return "";
    if (isOne(-A)) return "-";
    return fmtNum(A) + " ";
  }

  function coefText(A) {
    if (isOne(A)) return "";
    if (isOne(-A)) return MINUS;
    return fmtNum(A).replace("-", MINUS) + " ";
  }

  function constTex(beta) {
    if (isZero(beta) || fmtNum(beta) === "0") return "";
    return (beta > 0 ? " + " : " - ") + fmtNum(Math.abs(beta));
  }

  function constText(beta) {
    if (isZero(beta) || fmtNum(beta) === "0") return "";
    return (beta > 0 ? " + " : " " + MINUS + " ") + fmtNum(Math.abs(beta));
  }

  /** x − α の部分。α は π 単位 */
  function shiftTex(alpha, unit) {
    return (alpha > 0 ? " - " : " + ") + angle(Math.abs(alpha), unit).tex;
  }

  function shiftText(alpha, unit) {
    return (alpha > 0 ? " " + MINUS + " " : " + ") + angle(Math.abs(alpha), unit).text;
  }

  function alphaIsZero(alpha, unit) {
    return isZero(alpha) || angle(alpha, unit).text === "0" || angle(alpha, unit).text === "0°";
  }

  function bIsOne(B) { return fmtNum(B) === "1"; }

  /**
   * 式の LaTeX。form = "factored": A sin B(x − α) + β,  "expanded": A sin(Bx − Bα) + β,
   *              "phase": A sin(Bx − α) + β（よくある間違いの形）
   * w = {func, A, B, alpha(π 単位), beta}
   */
  function formulaTex(w, unit, form) {
    var fn = "\\" + w.func;
    if (fmtNum(w.A) === "0") {
      return "y = " + (fmtNum(w.beta) === "0" ? "0" : fmtNum(w.beta));
    }
    var bx = bIsOne(w.B) ? "x" : fmtNum(w.B) + "x";
    var inner;
    if (alphaIsZero(w.alpha, unit)) {
      inner = fn + " " + bx;
    } else if (bIsOne(w.B)) {
      inner = fn + "\\left(x" + shiftTex(w.alpha, unit) + "\\right)";
    } else if (form === "phase") {
      inner = fn + "\\left(" + bx + shiftTex(w.alpha, unit) + "\\right)";
    } else if (form === "expanded") {
      var ba = w.B * w.alpha;
      inner = fn + "\\left(" + bx + (ba > 0 ? " - " : " + ") + angle(Math.abs(ba), unit).tex + "\\right)";
    } else {
      inner = fn + " " + fmtNum(w.B) + "\\left(x" + shiftTex(w.alpha, unit) + "\\right)";
    }
    return "y = " + coefTex(w.A) + inner + constTex(w.beta);
  }

  /** グラフの凡例などに書く式（LaTeX を使わない） */
  function formulaText(w, unit, form) {
    if (fmtNum(w.A) === "0") return "y = " + fmtNum(w.beta).replace("-", MINUS);
    var bx = bIsOne(w.B) ? "x" : fmtNum(w.B) + "x";
    var inner;
    if (alphaIsZero(w.alpha, unit)) {
      inner = w.func + " " + bx;
    } else if (bIsOne(w.B)) {
      inner = w.func + "(x" + shiftText(w.alpha, unit) + ")";
    } else if (form === "phase") {
      inner = w.func + "(" + bx + shiftText(w.alpha, unit) + ")";
    } else if (form === "expanded") {
      var ba = w.B * w.alpha;
      inner = w.func + "(" + bx + (ba > 0 ? " " + MINUS + " " : " + ") + angle(Math.abs(ba), unit).text + ")";
    } else {
      inner = w.func + " " + fmtNum(w.B) + "(x" + shiftText(w.alpha, unit) + ")";
    }
    return "y = " + coefText(w.A) + inner + constText(w.beta);
  }

  /** 展開した形も並べて書くべきか（B ≠ 1 かつ α ≠ 0） */
  function needsExpanded(w, unit) {
    return fmtNum(w.A) !== "0" && !bIsOne(w.B) && !alphaIsZero(w.alpha, unit);
  }

  /** B·α が π の分数（または度の小数 2 桁）でぴったり表せるか */
  function expandedIsExact(w, unit) {
    return angle(Math.abs(w.B * w.alpha), unit).exact;
  }

  // ---------------- 値・特徴量 ----------------
  function yValue(w, x) {
    var f = w.func === "sin" ? Math.sin : Math.cos;
    return w.A * f(w.B * (x - w.alpha * Math.PI)) + w.beta;
  }

  function sample(w, loPi, hiPi, n) {
    n = n || 600;
    var xs = new Array(n), ys = new Array(n);
    for (var i = 0; i < n; i++) {
      var x = (loPi + (hiPi - loPi) * i / (n - 1)) * Math.PI;
      xs[i] = x; ys[i] = yValue(w, x);
    }
    return { x: xs, y: ys };
  }

  function period(w) { return 2 / w.B; }                 // π 単位
  function amplitude(w) { return Math.abs(w.A); }
  function yMax(w) { return w.beta + Math.abs(w.A); }
  function yMin(w) { return w.beta - Math.abs(w.A); }

  /** 1 周期 [α, α + 周期] を 4 等分した 5 点 [x(π 単位), y] */
  function keyPoints(w) {
    var q = period(w) / 4;
    return BASE_KEY_VALUES[w.func].map(function (v, k) {
      return [w.alpha + k * q, w.beta + w.A * v];
    });
  }

  function baseKeyPoints(func) {
    return BASE_KEY_VALUES[func].map(function (v, k) { return [k / 2, v]; });
  }

  /** すべての波の 1 周期が入る x の範囲（π 単位、0.5π 単位に丸める） */
  function xRange(waves, cap) {
    cap = cap || 9;
    var lo = -1, hi = 3;
    waves.forEach(function (w) {
      lo = Math.min(lo, w.alpha);
      hi = Math.max(hi, w.alpha + period(w));
    });
    lo = Math.floor(lo * 2 + EPS) / 2;
    hi = Math.min(Math.ceil(hi * 2 - EPS) / 2, lo + cap + 1);
    return [lo, hi];
  }

  /** y の表示範囲（0.5 刻みに切り上げて、スライダーを動かしても細かく揺れないようにする） */
  function yLimit(waves) {
    var m = 0;
    waves.forEach(function (w) { m = Math.max(m, Math.abs(yMax(w)), Math.abs(yMin(w))); });
    return Math.max(1.5, Math.ceil((m + 0.3) * 2) / 2);
  }

  /** x 軸の目盛り（π 単位で step 刻み） */
  function ticks(loPi, hiPi, unit) {
    var step = (hiPi - loPi) <= 6 ? 0.5 : 1;
    var vals = [], texts = [];
    for (var k = Math.ceil(loPi / step - EPS); k * step <= hiPi + EPS; k++) {
      var q = k * step;
      vals.push(q * Math.PI);
      texts.push(angle(q, unit).text);
    }
    return { vals: vals, texts: texts };
  }

  /** 段階的に変形するときの 5 つの波 */
  function steps(w) {
    var b = { func: w.func, A: 1, B: 1, alpha: 0, beta: 0 };
    return [
      b,
      { func: w.func, A: 1, B: w.B, alpha: 0, beta: 0 },
      { func: w.func, A: 1, B: w.B, alpha: w.alpha, beta: 0 },
      { func: w.func, A: w.A, B: w.B, alpha: w.alpha, beta: 0 },
      { func: w.func, A: w.A, B: w.B, alpha: w.alpha, beta: w.beta },
    ];
  }

  var api = {
    toFrac: toFrac, fmtNum: fmtNum, angle: angle, num: num,
    formulaTex: formulaTex, formulaText: formulaText,
    needsExpanded: needsExpanded, expandedIsExact: expandedIsExact,
    alphaIsZero: alphaIsZero, bIsOne: bIsOne,
    yValue: yValue, sample: sample, period: period, amplitude: amplitude, yMax: yMax, yMin: yMin,
    keyPoints: keyPoints, baseKeyPoints: baseKeyPoints, xRange: xRange, yLimit: yLimit, ticks: ticks,
    steps: steps, MINUS: MINUS,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GF = api;
})(this);
