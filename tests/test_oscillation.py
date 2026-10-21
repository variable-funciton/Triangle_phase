import math
import numpy as np
from utils.oscillation import (G, damped_motion, damped_turning_points, free_motion, friction_motion,
                               friction_turning_points, omega, period, wave_displacement)

def test_oscillation():
    k, m, x0 = 20.0, 0.5, 0.2
    w = omega(k, m)
    assert abs(period(k, m) - 2 * math.pi * math.sqrt(m / k)) < 1e-12
    t = np.linspace(0, 5, 5001)
    assert np.allclose(free_motion(x0, k, m, t), x0 * np.cos(w * t))
    # 動摩擦: 振幅は半周期ごとに 2d ずつ減る（等差数列）、止まる位置は |x| ≤ d
    mu = 0.1
    pts, t_stop, d = friction_turning_points(x0, k, m, mu)
    amps = [abs(p[1]) for p in pts]
    assert abs(d - mu * m * G / k) < 1e-12
    assert all(abs((amps[i] - amps[i + 1]) - 2 * d) < 1e-12 for i in range(len(amps) - 1))
    assert amps[-1] <= d < amps[-2]
    assert all(abs((pts[i + 1][0] - pts[i][0]) - math.pi / w) < 1e-12 for i in range(len(pts) - 1))
    x = friction_motion(x0, k, m, mu, t)
    assert np.max(np.abs(np.diff(x))) < 0.01                       # とぎれずにつながる
    assert np.allclose(x[t > t_stop + 0.01], pts[-1][1])             # 止まったあとは動かない
    for tp, xp in pts:
        assert abs(float(friction_motion(x0, k, m, mu, [tp])[0]) - xp) < 1e-9
    assert friction_turning_points(0.01, k, m, mu)[1] == 0.0        # 摩擦力の方が大きいと動かない
    # 速さに比例する抵抗: 折り返し点の振幅は等比数列
    g = 0.5
    tp = damped_turning_points(x0, k, m, g, 6)
    for tt, xx in tp:
        assert abs(float(damped_motion(x0, k, m, g, [tt])[0]) - xx) < 1e-12
    r = [abs(tp[i + 1][1] / tp[i][1]) for i in range(5)]
    assert max(r) - min(r) < 1e-12 and r[0] < 1
    assert np.allclose(damped_motion(x0, k, m, 0.0, t), free_motion(x0, k, m, t))
    # 波: 1 周期後・1 波長先で同じ値、速さ λ/T
    xs = np.linspace(0, 4, 50)
    y0 = wave_displacement(xs, 0.3, 0.2, 2.0, 1.5)
    assert np.allclose(y0, wave_displacement(xs, 0.3 + 1.5, 0.2, 2.0, 1.5))
    assert np.allclose(y0, wave_displacement(xs + 2.0, 0.3, 0.2, 2.0, 1.5))
    v = 2.0 / 1.5
    assert np.allclose(wave_displacement(xs + v * 0.4, 0.3 + 0.4, 0.2, 2.0, 1.5), y0)    # +x 向きに速さ v で進む

if __name__ == "__main__":
    test_oscillation(); print("test_oscillation ok")
