"""フーリエ級数（周期 2π の波を sin, cos の足し合わせで表す）。

係数の求め方には積分が必要なので、ここでは代表的な波について「答え」の係数を用意しておく。
各波は  a0 + Σ ( a_n cos nx + b_n sin nx )  の a0, a_n, b_n で表す。
"""

from __future__ import annotations

import math

import numpy as np


def _square(x):
    return np.sign(np.sin(x))


def _saw(x):
    return (np.asarray(x) + np.pi) % (2 * np.pi) - np.pi


def _triangle(x):
    return np.abs(_saw(x))


def _half(x):
    return np.maximum(np.sin(x), 0.0)


def _full(x):
    return np.abs(np.sin(x))


WAVES = {
    "square": dict(
        name="矩形波（くけいは）", func=_square, a0=0.0,
        a=lambda n: 0.0,
        b=lambda n: 4 / (math.pi * n) if n % 2 == 1 else 0.0,
        tex=r"\frac{4}{\pi}\left(\sin x + \frac{1}{3}\sin 3x + \frac{1}{5}\sin 5x + \frac{1}{7}\sin 7x + \cdots\right)",
        note="奇数倍の sin だけ。n 倍の波の大きさは 1/n。",
        discontinuous=True,
    ),
    "saw": dict(
        name="のこぎり波", func=_saw, a0=0.0,
        a=lambda n: 0.0,
        b=lambda n: 2 * (-1) ** (n + 1) / n,
        tex=r"2\left(\sin x - \frac{1}{2}\sin 2x + \frac{1}{3}\sin 3x - \frac{1}{4}\sin 4x + \cdots\right)",
        note="すべての n 倍の sin。符号が交互で、大きさは 1/n。",
        discontinuous=True,
    ),
    "triangle": dict(
        name="三角波（テントマップのくり返し）", func=_triangle, a0=math.pi / 2,
        a=lambda n: -4 / (math.pi * n * n) if n % 2 == 1 else 0.0,
        b=lambda n: 0.0,
        tex=r"\frac{\pi}{2} - \frac{4}{\pi}\left(\cos x + \frac{1}{3^2}\cos 3x + \frac{1}{5^2}\cos 5x + \cdots\right)",
        note="奇数倍の cos だけ。大きさは 1/n² なので、すぐに近づく（角はあるが、とぎれがない）。",
        discontinuous=False,
    ),
    "half": dict(
        name="半波整流（sin の正の部分だけ）", func=_half, a0=1 / math.pi,
        a=lambda n: -2 / (math.pi * (n * n - 1)) if n % 2 == 0 else 0.0,
        b=lambda n: 0.5 if n == 1 else 0.0,
        tex=r"\frac{1}{\pi} + \frac{1}{2}\sin x - \frac{2}{\pi}\left(\frac{\cos 2x}{1\cdot 3} + \frac{\cos 4x}{3\cdot 5} + \frac{\cos 6x}{5\cdot 7} + \cdots\right)",
        note="交流からダイオードで負の部分を取り除いた電圧の形。",
        discontinuous=False,
    ),
    "full": dict(
        name="全波整流（|sin x|）", func=_full, a0=2 / math.pi,
        a=lambda n: -4 / (math.pi * (n * n - 1)) if n % 2 == 0 else 0.0,
        b=lambda n: 0.0,
        tex=r"\frac{2}{\pi} - \frac{4}{\pi}\left(\frac{\cos 2x}{1\cdot 3} + \frac{\cos 4x}{3\cdot 5} + \frac{\cos 6x}{5\cdot 7} + \cdots\right)",
        note="交流の負の部分を正に折り返した電圧の形。周期は π になる。",
        discontinuous=False,
    ),
}


def terms(key: str, N: int):
    """n = 1..N の 0 でない項 [(n, 'cos' or 'sin', 係数)]"""
    w = WAVES[key]
    out = []
    for n in range(1, N + 1):
        an, bn = w["a"](n), w["b"](n)
        if an:
            out.append((n, "cos", an))
        if bn:
            out.append((n, "sin", bn))
    return out


def term_values(x, n: int, kind: str, c: float):
    return c * (np.cos(n * x) if kind == "cos" else np.sin(n * x))


def partial_sum(key: str, x, N: int):
    """n = N 倍の波までの和"""
    x = np.asarray(x, dtype=float)
    y = np.full_like(x, WAVES[key]["a0"])
    for n, kind, c in terms(key, N):
        y = y + term_values(x, n, kind, c)
    return y


def amplitudes(key: str, N: int):
    """各 n 倍の波の大きさ √(a_n² + b_n²)（スペクトル）"""
    w = WAVES[key]
    return [math.hypot(w["a"](n), w["b"](n)) for n in range(1, N + 1)]


def custom_sum(x, coefs_sin, coefs_cos=(), const=0.0):
    x = np.asarray(x, dtype=float)
    y = np.full_like(x, const)
    for n, c in enumerate(coefs_sin, start=1):
        y = y + c * np.sin(n * x)
    for n, c in enumerate(coefs_cos, start=1):
        y = y + c * np.cos(n * x)
    return y
