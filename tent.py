"""テントマップとその変換・合成の計算（後期課題5 対応）。

    f(x) = 2x (0 ≤ x ≤ 1/2),  2 − 2x (1/2 < x ≤ 1),  0 (それ以外)
    g(x) = 3x (0 ≤ x < 1/3),  1 (1/3 ≤ x < 2/3),  3 − 3x (2/3 ≤ x < 1),  0 (それ以外)   … 課題5 の台形
区間の外を 0 とするのは課題5 の定義に合わせたもの（合成のときに内側の値が [0, 1] の外に出ても計算できる）。
表示用には区間の外を「描かない（NaN）」にする関数も用意する。
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np


# ---------------- 基本の関数 ----------------
def tent(x, outside=0.0):
    x = np.asarray(x, dtype=float)
    y = np.full_like(x, outside, dtype=float)
    m1 = (x >= 0) & (x <= 0.5)
    m2 = (x > 0.5) & (x <= 1)
    y[m1] = 2 * x[m1]
    y[m2] = 2 - 2 * x[m2]
    return y


def trapezoid(x, outside=0.0):
    x = np.asarray(x, dtype=float)
    y = np.full_like(x, outside, dtype=float)
    m1 = (x >= 0) & (x < 1 / 3)
    m2 = (x >= 1 / 3) & (x < 2 / 3)
    m3 = (x >= 2 / 3) & (x < 1)
    y[m1] = 3 * x[m1]
    y[m2] = 1.0
    y[m3] = 3 - 3 * x[m3]
    return y


def transformed(x, a, b, p, q, base=tent, outside=0.0):
    """y = a·base(b(x − p)) + q。outside が NaN のときは定義域の外を描かない"""
    inner = b * (np.asarray(x, dtype=float) - p)
    y = base(inner, outside=np.nan)
    if np.isnan(outside):
        return a * y + q
    return np.where(np.isnan(y), outside, a * y + q)


def transformed_vertices(a, b, p, q):
    """テントの両端と頂点 (0,0), (1/2,1), (1,0) の移り先"""
    return [(p, q), (p + 1 / (2 * b), a + q), (p + 1 / b, q)]


# ---------------- 合成 ----------------
def compose(outer, inner):
    return lambda x: outer(inner(x))


def iterate_fn(n: int):
    """f を n 回合成した関数 f^n"""
    def fn(x):
        y = np.asarray(x, dtype=float)
        for _ in range(n):
            y = tent(y)
        return y
    return fn


def iterate_vertices(n: int):
    """f^n の折れ目（x = k/2^n）と値（0 と 1 が交互）"""
    m = 2 ** n
    return [(Fraction(k, m), k % 2) for k in range(m + 1)]


def tent_exact(x: Fraction) -> Fraction:
    if 0 <= x <= Fraction(1, 2):
        return 2 * x
    if Fraction(1, 2) < x <= 1:
        return 2 - 2 * x
    return Fraction(0)


def orbit(x0, n: int) -> list[Fraction]:
    """漸化式 x_{k+1} = f(x_k) を分数で厳密に計算（小数だと 2 倍をくり返すうちに誤差で 0 になってしまう）"""
    x = Fraction(x0)
    out = [x]
    for _ in range(n):
        x = tent_exact(x)
        out.append(x)
    return out


def dense_grid(lo: float, hi: float, n_extra: int = 4000, depth: int = 8):
    """折れ目（k/2^depth, k/3·2^j など）を含む細かい x の格子。折れ線の角を正確に描くため"""
    base = np.linspace(lo, hi, n_extra)
    m = 2 ** depth * 3
    ks = np.arange(int(np.floor(lo * m)), int(np.ceil(hi * m)) + 1) / m
    return np.unique(np.concatenate([base, ks[(ks >= lo) & (ks <= hi)]]))
