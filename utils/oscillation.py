"""バネの単振動（摩擦なし・動摩擦・速さに比例する抵抗）と、横波・縦波の計算。

単振動:  x = x0 cos ωt,  ω = √(k/m),  T = 2π/ω
動摩擦（動摩擦係数 μ）:
    動く向きと反対に一定の力 μmg がはたらくので、つり合いの位置が d = μmg/k だけずれた単振動を
    半周期ずつつなげた動きになる。半周期ごとに振幅が 2d ずつ減る（等差数列）。
    |x| ≤ d の位置で止まると、ばねの力が摩擦力以下なので静止したままになる（静止摩擦係数も μ とする）。
速さに比例する抵抗（減衰の強さ γ）:
    x = x0 e^{−γt}(cos ω't + (γ/ω') sin ω't),  ω' = √(ω² − γ²)
    折り返し点の振幅は半周期ごとに e^{−γπ/ω'} 倍になる（等比数列）。
波:  y = A sin 2π(t/T − x/λ)（+x 向きに進む波）
"""

from __future__ import annotations

import math

import numpy as np

G = 9.8


def omega(k: float, m: float) -> float:
    return math.sqrt(k / m)


def period(k: float, m: float) -> float:
    return 2 * math.pi / omega(k, m)


# ---------------- 摩擦なし ----------------
def free_motion(x0, k, m, t):
    return x0 * np.cos(omega(k, m) * np.asarray(t, dtype=float))


# ---------------- 動摩擦 ----------------
def friction_turning_points(x0, k, m, mu, g=G, max_half=1000):
    """折り返し点 [(時刻, 位置)] と止まる時刻（動かなければ 0）"""
    w = omega(k, m)
    d = mu * m * g / k
    pts = [(0.0, float(x0))]
    if abs(x0) <= d:
        return pts, 0.0, d
    x, t = float(x0), 0.0
    for _ in range(max_half):
        c = math.copysign(d, x)          # 動く向きの反対に摩擦 → つり合いの位置が c にずれる
        x = 2 * c - x
        t += math.pi / w
        pts.append((t, x))
        if abs(x) <= d:
            break
    return pts, t, d


def friction_motion(x0, k, m, mu, t, g=G):
    w = omega(k, m)
    pts, t_stop, d = friction_turning_points(x0, k, m, mu, g)
    t = np.asarray(t, dtype=float)
    x = np.full_like(t, pts[-1][1])
    for (t0, xs), (t1, _) in zip(pts[:-1], pts[1:]):
        c = math.copysign(d, xs)
        mask = (t >= t0) & (t <= t1)
        x[mask] = c + (xs - c) * np.cos(w * (t[mask] - t0))
    return x


# ---------------- 速さに比例する抵抗 ----------------
def damped_motion(x0, k, m, gamma, t):
    w = omega(k, m)
    if gamma >= w:
        raise ValueError("γ < ω の範囲（振動する場合）だけ扱う")
    wd = math.sqrt(w * w - gamma * gamma)
    t = np.asarray(t, dtype=float)
    return x0 * np.exp(-gamma * t) * (np.cos(wd * t) + gamma / wd * np.sin(wd * t))


def damped_turning_points(x0, k, m, gamma, n_half):
    w = omega(k, m)
    wd = math.sqrt(w * w - gamma * gamma)
    return [(n * math.pi / wd, x0 * (-1) ** n * math.exp(-gamma * n * math.pi / wd)) for n in range(n_half + 1)]


def damped_envelope(x0, gamma, t):
    return x0 * np.exp(-gamma * np.asarray(t, dtype=float))


# ---------------- 波 ----------------
def wave_displacement(x, t, A, lam, T, direction=1):
    """y = A sin 2π(t/T − direction·x/λ)。direction = +1 で +x 向き、−1 で −x 向きに進む"""
    return A * np.sin(2 * np.pi * (t / T - direction * np.asarray(x, dtype=float) / lam))
