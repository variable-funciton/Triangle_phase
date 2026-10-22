// ブラウザ側で動くページ（逆三角関数・接線の傾き・テイラー展開・リサージュ）の計算のテスト
//   node tests/test_widgets_js.js
const assert = require("assert");
const TU = require("../assets/common_core.js");
const IT = require("../assets/inverse_trig_core.js");
const TS = require("../assets/tangent_slope_core.js");
const TY = require("../assets/taylor_core.js");
const LJ = require("../assets/lissajous_core.js");
const near = (a, b, e) => assert.ok(Math.abs(a - b) < (e || 1e-9), `${a} != ${b}`);
const M = TU.MINUS;

// ---- 共通 ----
assert.strictEqual(TU.exactValue(Math.sqrt(3) / 2).tex, "\\frac{\\sqrt{3}}{2}");
assert.strictEqual(TU.exactValue(-Math.sqrt(2) / 2).text, M + "√2/2");
assert.strictEqual(TU.exactValue(-0.5).tex, "-\\frac{1}{2}");
assert.strictEqual(TU.exactValue(1 / Math.sqrt(3)).tex, "\\frac{1}{\\sqrt{3}}");
assert.strictEqual(TU.exactValue(0.3333).exact, false);
assert.strictEqual(TU.angle(5 / 6, "rad").tex, "\\frac{5\\pi}{6}");
assert.strictEqual(TU.ticks(-1, 1, "rad", 0.5).texts.join(","), [M + "π", M + "π/2", "0", "π/2", "π"].join(","));
assert.strictEqual(TU.factorial(5), 120);

// ---- 逆三角関数 ----
near(IT.principal("sin", 0.5), 1 / 6);
near(IT.principal("cos", -0.5), 2 / 3);
near(IT.principal("tan", -1), -1 / 4);
assert.deepStrictEqual(IT.solutions("sin", -0.5, 0, 2).map(x => Math.round(x * 6)), [7, 11]);
assert.deepStrictEqual(IT.solutions("cos", Math.sqrt(3) / 2, 0, 2).map(x => Math.round(x * 6)), [1, 11]);
assert.deepStrictEqual(IT.solutions("tan", Math.sqrt(3), -1, 1).map(x => Math.round(x * 3)), [-2, 1]);
assert.deepStrictEqual(IT.solutions("sin", 1, 0, 2).map(x => x * 2), [1]);        // 重解は 1 つ
assert.deepStrictEqual(IT.solutions("sin", 1.5, 0, 2), []);                        // 範囲外
for (const fn of ["sin", "cos", "tan"]) {            // 解はすべて方程式をみたす
  for (const k of [-0.9, -0.3, 0, 0.42, 0.99]) {
    IT.solutions(fn, k, -2, 2).forEach(x => near(IT.SPECS[fn].base(x * Math.PI), k, 1e-9));
  }
}
assert.strictEqual(IT.generalTex("sin", 0.5), "x = \\frac{\\pi}{6} + 2n\\pi,\\quad x = \\frac{5\\pi}{6} + 2n\\pi");
assert.strictEqual(IT.generalTex("sin", -1), "x = -\\frac{\\pi}{2} + 2n\\pi");
assert.strictEqual(IT.generalTex("cos", 0.5), "x = \\pm \\frac{\\pi}{3} + 2n\\pi");
assert.strictEqual(IT.generalTex("tan", 1), "x = \\frac{\\pi}{4} + n\\pi");
assert.ok(IT.generalTex("sin", 0.3).includes("\\theta"));
assert.strictEqual(IT.angleShow(1 / 3).tex, "\\frac{\\pi}{3}");
assert.strictEqual(IT.angleShow(0.3 / Math.PI).exact, false);
assert.ok(IT.curve("tan", -4, 4).y.some(v => v === null));                      // 漸近線で切れる

// ---- 接線の傾き ----
for (const a of [-2, 0, 0.5, 1, Math.PI / 2, 3, 5]) {
  near(TS.tangentSlope("sin", a), Math.cos(a), 1e-8);
  near(TS.tangentSlope("cos", a), -Math.sin(a), 1e-8);
}
near(TS.secantSlope("sin", 0, 1), Math.sin(1));
assert.ok(Math.abs(TS.secantSlope("sin", 1, 0.01) - Math.cos(1)) < Math.abs(TS.secantSlope("sin", 1, 0.5) - Math.cos(1)));
assert.strictEqual(TS.table("sin")[0][2].tex, "1");
assert.strictEqual(TS.table("sin")[2][2].tex, "\\frac{\\sqrt{2}}{2}");

// ---- テイラー展開 ----
assert.deepStrictEqual(TY.coeffs("sin", 0, 5).map(c => +c.toFixed(6)), [0, 1, 0, -1 / 6, 0, 1 / 120].map(c => +c.toFixed(6)));
assert.deepStrictEqual(TY.coeffs("cos", 0, 4).map(c => +c.toFixed(6)), [1, 0, -0.5, 0, 1 / 24].map(c => +c.toFixed(6)));
for (const fn of ["sin", "cos"]) for (const x0 of [-3, 0, 0.7, Math.PI / 3, 4]) {
  const cs = TY.coeffs(fn, x0, 15);
  for (const d of [-1.5, 0, 1, 2]) near(TY.evalP(cs, x0, x0 + d), TY.F[fn](x0 + d), 1e-6);
  near(TY.evalP(TY.coeffs(fn, x0, 0), x0, x0), TY.F[fn](x0));            // 中心では値が一致
}
const g1 = TY.goodRange("sin", 0, 1), g7 = TY.goodRange("sin", 0, 7);
assert.ok(g7[1] - g7[0] > g1[1] - g1[0]);
assert.strictEqual(TY.valuedTex("sin", 0, 3).tex, "\\sin x \\approx x - \\frac{x^{3}}{3!}");
assert.strictEqual(TY.valuedTex("cos", 0, 2).tex, "\\cos x \\approx 1 - \\frac{x^{2}}{2!}");
const v6 = TY.valuedTex("sin", Math.PI / 6, 1);
assert.ok(v6.exact);
assert.strictEqual(v6.tex, "\\sin x \\approx \\frac{1}{2} + \\frac{\\sqrt{3}}{2}\\,\\left(x - \\frac{\\pi}{6}\\right)");
assert.strictEqual(TY.valuedTex("sin", 1.23, 2).exact, false);
assert.ok(TY.valuedTex("cos", -Math.PI / 3, 1).tex.includes("\\left(x + \\frac{\\pi}{3}\\right)"));
assert.ok(TY.symbolicTex("sin", 9).startsWith("\\begin{aligned}"));
assert.ok(TY.decimalTex("cos", Math.PI / 6, 15).includes("x - 0.52"));

// ---- リサージュ ----
assert.deepStrictEqual(LJ.ratio(3, 2), [3, 2]);
assert.deepStrictEqual(LJ.ratio(1.5, 1), [3, 2]);
assert.strictEqual(LJ.ratio(1.37, 1), null);
near(LJ.period(3, 2), 2 * Math.PI);
near(LJ.period(1.5, 1), 4 * Math.PI);
const p = { A: 1.5, B: 1, a: 3, b: 2, delta: Math.PI / 2 };
const T = LJ.period(p.a, p.b);
for (const t of [0.1, 1, 2.5]) { const q0 = LJ.point(p, t), q1 = LJ.point(p, t + T); near(q0[0], q1[0]); near(q0[1], q1[1]); }
const circle = { A: 1, B: 1, a: 1, b: 1, delta: Math.PI / 2 };
for (const t of [0, 0.7, 2]) { const q = LJ.point(circle, t); near(q[0] ** 2 + q[1] ** 2, 1); }
near(LJ.yIntercept({ A: 1, B: 2, a: 1, b: 1, delta: Math.PI / 6 }), 1);
assert.strictEqual(LJ.formulaTex(p), "x = 1.5\\sin\\left(3t + \\frac{\\pi}{2}\\right),\\qquad y = \\sin 2t");
assert.strictEqual(LJ.formulaTex({ A: 1, B: 1, a: 1, b: 1, delta: 0 }), "x = \\sin t,\\qquad y = \\sin t");

console.log("widgets: all tests passed");
