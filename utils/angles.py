"""角度・分数の表示用ユーティリティ（π を単位とした分数 Fraction を文字列化する）。

角度はすべて「π の何倍か」を表す Fraction で扱う。
    例: Fraction(1, 2) -> π/2,  Fraction(-3, 4) -> -3π/4
float が渡されたときは「π の倍数で表せない小数の角」とみなし、ラジアン（または度）の小数で表示する。
    例: 1.25/π（= 1.25 rad）-> '1.25'、度数法なら '71.6°'
Plotly の目盛りは LaTeX を表示できないため、Unicode 版 (pi_text) と
Streamlit の数式表示用の LaTeX 版 (pi_latex) を用意している。
"""

from __future__ import annotations

import math
from fractions import Fraction

MINUS = "−"  # Unicode マイナス（グラフ上で見やすい）


def to_fraction(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(value).limit_denominator(1000)


# ---------- π を単位とする角度 ----------
def _dec(v: float, digits: int = 4) -> str:
    s = f"{v:.{digits}g}"
    return s.replace("-", MINUS)


def pi_text(q) -> str:
    """π の倍数を Unicode 文字列にする。 1/2 -> 'π/2', -3/2 -> '−3π/2'（float なら小数のラジアン）"""
    if isinstance(q, float):
        return _dec(q * math.pi, 3)
    q = to_fraction(q)
    if q == 0:
        return "0"
    sign = MINUS if q < 0 else ""
    p, d = abs(q.numerator), q.denominator
    num = "π" if p == 1 else f"{p}π"
    return f"{sign}{num}" if d == 1 else f"{sign}{num}/{d}"


def pi_latex(q) -> str:
    """π の倍数を LaTeX にする。 1/2 -> '\\frac{\\pi}{2}', -3 -> '-3\\pi'（float なら小数のラジアン）"""
    if isinstance(q, float):
        return f"{q * math.pi:.3g}"
    q = to_fraction(q)
    if q == 0:
        return "0"
    sign = "-" if q < 0 else ""
    p, d = abs(q.numerator), q.denominator
    num = r"\pi" if p == 1 else rf"{p}\pi"
    return f"{sign}{num}" if d == 1 else rf"{sign}\frac{{{num}}}{{{d}}}"


def deg_text(q) -> str:
    """π の倍数を度数法の文字列にする。 1/2 -> '90°'"""
    if isinstance(q, float):
        return _dec(q * 180) + "°"
    deg = to_fraction(q) * 180
    if deg.denominator == 1:
        s = str(abs(deg.numerator))
    else:
        s = f"{abs(float(deg)):g}"
    return f"{MINUS if deg < 0 else ''}{s}°"


def deg_latex(q) -> str:
    if isinstance(q, float):
        return rf"{q * 180:.4g}^\circ"
    deg = to_fraction(q) * 180
    s = str(deg.numerator) if deg.denominator == 1 else f"{float(deg):g}"
    return rf"{s}^\circ"


def angle_text(q, unit: str = "rad") -> str:
    return deg_text(q) if unit == "deg" else pi_text(q)


def angle_latex(q, unit: str = "rad") -> str:
    return deg_latex(q) if unit == "deg" else pi_latex(q)


# ---------- 一般の分数（振幅・倍率など） ----------
def frac_text(q) -> str:
    """3/2 -> '3/2', -1/2 -> '−1/2', 2 -> '2'"""
    q = to_fraction(q)
    sign = MINUS if q < 0 else ""
    p, d = abs(q.numerator), q.denominator
    return f"{sign}{p}" if d == 1 else f"{sign}{p}/{d}"


def frac_latex(q) -> str:
    q = to_fraction(q)
    sign = "-" if q < 0 else ""
    p, d = abs(q.numerator), q.denominator
    return f"{sign}{p}" if d == 1 else rf"{sign}\frac{{{p}}}{{{d}}}"


def pi_ticks(x_min_pi, x_max_pi, step_pi, unit: str = "rad"):
    """x 軸の目盛り（値[rad], ラベル）を step_pi 刻みで作る。"""
    import math

    step = to_fraction(step_pi)
    lo = math.ceil(to_fraction(x_min_pi) / step)
    hi = math.floor(to_fraction(x_max_pi) / step)
    qs = [k * step for k in range(lo, hi + 1)]
    return [float(q) * math.pi for q in qs], [angle_text(q, unit) for q in qs]
