// 学科別の応用ページの計算のテスト:  node tests/test_applied_js.js
const assert = require("assert");
const near = (a, b, e) => assert.ok(Math.abs(a - b) < (e || 1e-9), `${a} != ${b}`);
const R = p => require("../assets/" + p + "_core.js");
const FW = R("ferris"), SE = R("seasons"), CR = R("crank"), RO = R("rotation"), IC = R("incline"),
  AC = R("ac"), TP = R("three_phase"), PW = R("ac_power"), MO = R("molecule"), BR = R("bragg"),
  SH = R("shadow"), SV = R("survey"), SL = R("slope");
const D = Math.PI / 180;

// ---- 観覧車 ----
const fw = { r: 50, T: 16, h0: 55 };
near(FW.height(fw, 0), 5); near(FW.height(fw, 4), 55); near(FW.height(fw, 8), 105);
const ab = FW.above(fw, 80);
near(ab.t1, 16 / 3); near(ab.duration, 16 / 3);
near(FW.height(fw, ab.t1), 80);
assert.ok(FW.above(fw, 200).none); assert.ok(FW.above(fw, 0).all);
const pos = FW.position(fw, 3); near(Math.hypot(pos[0], pos[1] - 55), 50);

// ---- 季節 ----
near(SE.dayLength(35.69, 81), 12, 0.05);                       // 春分はほぼ 12 時間
assert.ok(SE.dayLength(35.69, 172) > 14.3 && SE.dayLength(35.69, 172) < 14.6);
assert.strictEqual(SE.dayLength(70, 172), 24); assert.strictEqual(SE.dayLength(70, 355), 0);
near(SE.dayLength(0, 100), 12, 1e-9);
for (const k in SE.TEMPS) {
  const d = SE.TEMPS[k].data, f = SE.fit(d);
  near(f.beta, d.reduce((a, b) => a + b) / 12);
  // 最小二乗：A, α を少し動かすとずれが大きくなる
  const e0 = SE.rms(f, d);
  for (const dA of [-0.3, 0.3]) assert.ok(SE.rms({ ...f, A: f.A + dA }, d) > e0);
  for (const da of [-0.2, 0.2]) assert.ok(SE.rms({ ...f, alpha: f.alpha + da }, d) > e0);
  // 合成：a sin + b cos = A sin(ωm − ωα)
  for (const m of [1, 4.5, 9]) near(f.a * Math.sin(Math.PI * m / 6) + f.b * Math.cos(Math.PI * m / 6), f.A * Math.sin(Math.PI * (m - f.alpha) / 6));
}
assert.strictEqual(SE.dateText(355), "12/21");

// ---- クランク ----
for (const th of [0, 0.5, 1.2, 2, Math.PI, 4, 5.5]) near(CR.cosineCheck(4, 12, th), 0, 1e-9);
near(CR.piston(4, 12, 0), 16); near(CR.piston(4, 12, Math.PI), 8); near(CR.piston(4, 12, Math.PI / 2), Math.sqrt(128));
near(CR.piston(4, 1e6, 1) - 1e6, 4 * Math.cos(1), 1e-4);         // l → ∞ で単振動
near(Math.sin(CR.rodAngle(4, 12, 1)), 4 * Math.sin(1) / 12);

// ---- 回転 ----
near(RO.omega(60), 2 * Math.PI); near(RO.speed(0.3, 120), 0.3 * 4 * Math.PI);
near(RO.gearN2(1200, 15, 45), 400); near(RO.beltN2(30, 10, 25), 12);
const g = RO.gearOutline(0, 0, 10, 20, 2, 0); assert.ok(g.x.length > 100);

// ---- 斜面 ----
const F = IC.forces(2, 30, 0.4);
near(F.along, 9.8, 1e-9); near(F.normal, 9.8 * Math.sqrt(3), 1e-9); assert.ok(F.slides); near(F.accel, 9.8 * (0.5 - 0.4 * Math.cos(30 * D)));
const F2 = IC.forces(2, 20, 0.5); assert.ok(!F2.slides); near(F2.friction, F2.along);
near(IC.frictionAngle(1), 45); near(IC.frictionAngle(0.5), Math.atan(0.5) / D);
const fa = IC.frictionAngle(0.7);
assert.ok(!IC.forces(1, fa - 0.01, 0.7).slides && IC.forces(1, fa + 0.01, 0.7).slides);

// ---- 交流 ----
near(AC.meanSquare(141.42, 50), 141.42 ** 2 / 2, 1e-6); near(AC.rms(100 * Math.SQRT2), 100);
near(AC.v(10, 50, 0.005), 10);   // 1/4 周期で最大

// ---- 三相 ----
for (const th of [0, 0.3, 1, 2.5, 4]) near(TP.sum(1, th, 120), 0, 1e-12);
near(TP.sumAmplitude(1, 120), 0, 1e-12); near(TP.sumAmplitude(1, 0), 3);
near(TP.lineAmplitude(1, 120), Math.sqrt(3));
for (const th of [0.2, 1.7]) { const p = TP.phases(1, th, 120); near(p[0] - p[1], Math.sqrt(3) * Math.sin(th + 30 * D)); }

// ---- 電力 ----
for (const wt of [0, 0.4, 1.3, 3]) near(PW.power(2, 3, 0.7, wt), PW.powerFormula(2, 3, 0.7, wt), 1e-12);
near(PW.meanPower(Math.SQRT2 * 100, Math.SQRT2 * 5, 60 * D), 250, 1e-6);
near(PW.meanPower(1, 1, Math.PI / 2), 0, 1e-9);

// ---- 分子 ----
near(MO.distance(0.096, 104.5), MO.distanceHalf(0.096, 104.5), 1e-12);
near(MO.distance(1, 180), 2); near(MO.distance(1, 120), Math.sqrt(3)); near(MO.distance(1, 60), 1);
near(Math.cos(MO.angleBetween(MO.TETRA[0], MO.TETRA[1]) * D), -1 / 3, 1e-12);
for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) near(MO.angleBetween(MO.TETRA[i], MO.TETRA[j]), MO.angleBetween(MO.TETRA[0], MO.TETRA[1]), 1e-9);

// ---- ブラッグ ----
const angs = BR.braggAngles(0.282, 0.154);
assert.strictEqual(angs.length, 3); near(angs[0].th, Math.asin(0.154 / 0.564) / D);
angs.forEach(a => { near(BR.pathDiff(0.282, a.th), a.n * 0.154, 1e-12); near(BR.intensity(0.282, 0.154, a.th, 10), 1, 1e-6); near(BR.twoWaveAmp(0.282, 0.154, a.th), 2, 1e-9); });
assert.ok(BR.intensity(0.282, 0.154, 25, 10) < 0.05);
assert.strictEqual(BR.braggAngles(0.1, 0.3).length, 0);

// ---- 日影 ----
near(SH.noonAltitude(35.7, -23.44), 30.86, 1e-9);
near(SH.altitude(35.7, -23.44, 12), SH.noonAltitude(35.7, -23.44), 1e-9);    // 正午の高度 = 南中高度
const v = SH.sunVector(35.7, 10, 9.3); near(Math.hypot(...v), 1, 1e-12);
const tip = SH.shadowTip(35.7, -23.44, 12, 1); near(tip[0], 0, 1e-12); near(tip[1], 1 / Math.tan(30.86 * D), 1e-9);
assert.ok(SH.shadowTip(35.7, 0, 9, 1)[0] < 0);           // 午前の影は西向き
assert.strictEqual(SH.shadowTip(35.7, -23.44, 3, 1), null);
near(SH.minSpacing(20, 35.7, -23.44), 20 / Math.tan(30.86 * D));

// ---- 測量 ----
near(SV.height(30, 35, 1.5), 30 * Math.tan(35 * D) + 1.5);
const T = SV.triangulate(50, 70, 60);
near(T.AC, 50 * Math.sin(60 * D) / Math.sin(130 * D)); near(T.width, T.AC * Math.sin(70 * D)); near(T.gamma, 50);
near(Math.hypot(T.C[0] - 50, T.C[1]), T.BC, 1e-9);                     // C と B の距離が正弦定理の BC と一致
assert.strictEqual(SV.triangulate(10, 100, 90), null);
near(SV.bearing([0, 0], [1, 0]), 0); near(SV.bearing([0, 0], [0, 1]), 90); near(SV.bearing([0, 0], [-1, 0]), 180);
const r0 = SV.traverse(SV.measurements(0, 0)); near(r0.closure, 0, 1e-9);   // 誤差なしなら閉じる
r0.pts.slice(0, 5).forEach((p, i) => { near(p[0], SV.TRUE_PTS[i][0], 1e-9); near(p[1], SV.TRUE_PTS[i][1], 1e-9); });
assert.ok(SV.traverse(SV.measurements(1, 0.5)).closure > 0.1);

// ---- 勾配 ----
const s10 = SL.fromAngle(SL.angleFromPercent(10));
near(s10.percent, 10); near(s10.permil, 100); near(s10.ratioN, 10);
near(SL.fromAngle(45).percent, 100); near(SL.angleFromPercent(100), 45);
near(SL.fromAngle(Math.atan(0.4) / D).sun, 4);

console.log("applied: all tests passed");
