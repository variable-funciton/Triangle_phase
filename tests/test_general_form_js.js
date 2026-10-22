// 一般形ページのブラウザ側計算のテスト:  node tests/test_general_form_js.js
const assert = require("assert");
const GF = require("../assets/general_form_core.js");

const W = (o) => Object.assign({ func: "sin", A: 1, B: 1, alpha: 0, beta: 0 }, o);
const M = GF.MINUS;

// 分数・数値の表示
assert.deepStrictEqual(GF.toFrac(2 / 3), [2, 3]);
assert.deepStrictEqual(GF.toFrac(-0.25), [-1, 4]);
assert.strictEqual(GF.toFrac(1 / Math.PI), null);
assert.strictEqual(GF.fmtNum(1.5), "1.5");
assert.strictEqual(GF.fmtNum(2.0), "2");
assert.strictEqual(GF.fmtNum(-0.001), "0");
assert.strictEqual(GF.fmtNum(0.333333), "0.33");

// 角度
assert.strictEqual(GF.angle(1 / 3, "rad").tex, "\\frac{\\pi}{3}");
assert.strictEqual(GF.angle(-2 / 3, "rad").tex, "-\\frac{2\\pi}{3}");
assert.strictEqual(GF.angle(1, "rad").text, "π");
assert.strictEqual(GF.angle(-1 / 2, "rad").text, M + "π/2");
assert.strictEqual(GF.angle(1.25 / Math.PI, "rad").tex, "1.25");
assert.strictEqual(GF.angle(1 / 3, "deg").tex, "60^\\circ");
assert.strictEqual(GF.angle(-1 / 4, "deg").text, M + "45°");
assert.strictEqual(GF.angle(2 / 1.37, "rad").exact, false);

// 式
assert.strictEqual(GF.formulaTex(W({}), "rad"), "y = \\sin x");
assert.strictEqual(GF.formulaTex(W({ A: 2, B: 2, alpha: 1 / 3, beta: 1 }), "rad"),
  "y = 2 \\sin 2\\left(x - \\frac{\\pi}{3}\\right) + 1");
assert.strictEqual(GF.formulaTex(W({ A: 2, B: 2, alpha: 1 / 3, beta: 1 }), "rad", "expanded"),
  "y = 2 \\sin\\left(2x - \\frac{2\\pi}{3}\\right) + 1");
assert.strictEqual(GF.formulaTex(W({ func: "cos", A: -1, alpha: -1 / 4, beta: -0.5 }), "rad"),
  "y = -\\cos\\left(x + \\frac{\\pi}{4}\\right) - 0.5");
assert.strictEqual(GF.formulaTex(W({ B: 1.5 }), "rad"), "y = \\sin 1.5x");
assert.strictEqual(GF.formulaTex(W({ A: 0, beta: 1 }), "rad"), "y = 1");
assert.strictEqual(GF.formulaTex(W({ alpha: 1.25 / Math.PI }), "rad"), "y = \\sin\\left(x - 1.25\\right)");
assert.strictEqual(GF.formulaTex(W({ B: 2, alpha: 1 / 6 }), "deg", "expanded"),
  "y = \\sin\\left(2x - 60^\\circ\\right)");
assert.strictEqual(GF.formulaText(W({ A: -1.5, B: 0.5, alpha: -1 / 2, beta: 2 }), "rad"),
  "y = " + M + "1.5 sin 0.5(x + π/2) + 2");
assert.strictEqual(GF.formulaTex(W({ B: 2, alpha: 1 / 3 }), "rad", "phase"),
  "y = \\sin\\left(2x - \\frac{\\pi}{3}\\right)");
assert.strictEqual(GF.formulaText(W({ B: 2, alpha: -1 / 3 }), "rad", "phase"), "y = sin(2x + π/3)");
assert.ok(GF.needsExpanded(W({ B: 2, alpha: 1 / 3 }), "rad"));
assert.ok(!GF.needsExpanded(W({ B: 1, alpha: 1 / 3 }), "rad"));
assert.ok(!GF.needsExpanded(W({ B: 2, alpha: 0 }), "rad"));
assert.ok(GF.expandedIsExact(W({ B: 1.5, alpha: 1 / 3 }), "rad"));     // π/2
assert.ok(!GF.expandedIsExact(W({ B: 1.37, alpha: 1 / 3 }), "rad"));

// 値・特徴量（Python の Wave と同じ式）
const w = W({ A: 2, B: 2, alpha: 1 / 3, beta: 1 });
assert.ok(Math.abs(GF.yValue(w, Math.PI / 3) - 1) < 1e-12);
assert.ok(Math.abs(GF.yValue(w, Math.PI / 3 + Math.PI / 4) - 3) < 1e-12);
assert.strictEqual(GF.period(w), 1);
assert.strictEqual(GF.yMax(w), 3);
assert.strictEqual(GF.yMin(w), -1);
const kp = GF.keyPoints(w);
assert.strictEqual(kp.length, 5);
kp.forEach(([x, y]) => assert.ok(Math.abs(GF.yValue(w, x * Math.PI) - y) < 1e-12));
GF.keyPoints(W({ func: "cos", A: -1.3, B: 0.7, alpha: -0.4, beta: 0.2 }))
  .forEach(([x, y]) => assert.ok(Math.abs(GF.yValue(W({ func: "cos", A: -1.3, B: 0.7, alpha: -0.4, beta: 0.2 }), x * Math.PI) - y) < 1e-12));

// 範囲・目盛り
assert.deepStrictEqual(GF.xRange([W({})]), [-1, 3]);
assert.deepStrictEqual(GF.xRange([W({ B: 0.5, alpha: 1 / 3 })]), [-1, 4.5]);
assert.strictEqual(GF.yLimit([W({})]), 1.5);
assert.strictEqual(GF.yLimit([W({ A: 2, beta: 1 })]), 3.5);
const tk = GF.ticks(-1, 3, "rad");
assert.strictEqual(tk.texts[0], M + "π");
assert.strictEqual(tk.texts.length, 9);
assert.strictEqual(GF.ticks(-1, 3, "deg").texts[2], "0°");

// 段階的な変形の最後は元の波
assert.deepStrictEqual(GF.steps(w)[4], w);
assert.deepStrictEqual(GF.steps(w)[0], W({}));

console.log("general_form_core.js: all tests passed");
