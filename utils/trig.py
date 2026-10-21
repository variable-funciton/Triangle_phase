"""y = A·f(B(x − t)) + β （f = sin または cos）の計算ロジック。

Streamlit や Plotly に依存しない純粋な計算部分だけをここに置き、テスト可能にしている。
t は「π の何倍か」を表す Fraction で持つ（例: t = 1/3 は π/3）。
π の倍数で表せない小数の t（例: 1.25 rad）は、π 単位の float（1.25/π）で持つ。
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction

import numpy as np

from .angles import MINUS, frac_latex, frac_text, pi_latex, pi_text, to_fraction

# 1 周期を 4 等分した点での基本形の値（x = 0, π/2, π, 3π/2, 2π）
BASE_KEY_VALUES = {
    "sin": [0, 1, 0, -1, 0],
    "cos": [1, 0, -1, 0, 1],
}


@dataclass(frozen=True)
class Wave:
    func: str = "sin"           # "sin" or "cos"
    A: Fraction = Fraction(1)   # 振幅の倍率（負なら上下反転）
    B: Fraction = Fraction(1)   # x 方向の倍率（正）
    t: Fraction = Fraction(0)   # x 方向の平行移動量（π 単位。小数の角は float）
    beta: Fraction = Fraction(0)  # y 方向の平行移動量

    def __post_init__(self):
        if self.func not in BASE_KEY_VALUES:
            raise ValueError("func must be 'sin' or 'cos'")
        for name in ("A", "B", "t", "beta"):
            v = getattr(self, name)
            if name == "t" and isinstance(v, float):
                continue          # 小数の角はそのまま（π の分数に近似しない）
            object.__setattr__(self, name, to_fraction(v))
        if self.B <= 0:
            raise ValueError("B must be positive")

    # ---- 値の計算 ----
    def y(self, x: np.ndarray) -> np.ndarray:
        f = np.sin if self.func == "sin" else np.cos
        return float(self.A) * f(float(self.B) * (x - float(self.t) * np.pi)) + float(self.beta)

    def with_(self, **kwargs) -> "Wave":
        return replace(self, **kwargs)

    # ---- グラフの特徴量 ----
    @property
    def period(self) -> Fraction:
        """周期（π 単位）= 2π / B"""
        return Fraction(2) / self.B

    @property
    def amplitude(self) -> Fraction:
        return abs(self.A)

    @property
    def y_max(self) -> Fraction:
        return self.beta + abs(self.A)

    @property
    def y_min(self) -> Fraction:
        return self.beta - abs(self.A)

    def key_points(self):
        """1 周期 [t, t + 周期] を 4 等分した 5 点 (x[π 単位], y) のリスト。"""
        q = self.period / 4
        return [
            (self.t + k * q, self.beta + self.A * v)
            for k, v in enumerate(BASE_KEY_VALUES[self.func])
        ]

    def base_key_points(self):
        """基本形 y = sin x / cos x の対応する 5 点。"""
        return [(Fraction(k, 2), Fraction(v)) for k, v in enumerate(BASE_KEY_VALUES[self.func])]

    # ---- 数式（LaTeX） ----
    def latex(self, form: str = "factored") -> str:
        """form = "factored": A sin B(x − t) + β,  "expanded": A sin(Bx − Bt) + β"""
        return "y = " + _coef(self.A) + _func_part(self.func, self.B, self.t, form) + _const(self.beta)

    def text(self, form: str = "factored") -> str:
        """グラフの中に書く用の式（LaTeX を使わない）。例: 'y = 2 sin 2(x − π/3) + 1'"""
        A, B, t = self.A, self.B, self.t
        coef = "" if A == 1 else MINUS if A == -1 else frac_text(A) + " "
        bx = "x" if B == 1 else f"{frac_text(B)}x" if B.denominator == 1 else f"({frac_text(B)})x"
        if t == 0:
            inner = f" {bx}"
        else:
            sh = (f" {MINUS} " if t > 0 else " + ") + pi_text(abs(t))
            if B == 1:
                inner = f"(x{sh})"
            elif form == "expanded":
                bt = B * t
                inner = f"({bx}" + (f" {MINUS} " if bt > 0 else " + ") + pi_text(abs(bt)) + ")"
            else:
                inner = f" {frac_text(B)}(x{sh})"
        const = "" if self.beta == 0 else (" + " if self.beta > 0 else f" {MINUS} ") + frac_text(abs(self.beta))
        return f"y = {coef}{self.func}{inner}{const}"


def _coef(A: Fraction) -> str:
    if A == 1:
        return ""
    if A == -1:
        return "-"
    return frac_latex(A)


def _bx(B: Fraction) -> str:
    if B == 1:
        return "x"
    if B.denominator == 1:
        return f"{B.numerator}x"
    return rf"\frac{{{B.numerator}}}{{{B.denominator}}}x"


def _signed_pi(q: Fraction) -> str:
    """' - \\frac{\\pi}{3}' / ' + \\pi' のような符号付きの項"""
    return (" - " if q > 0 else " + ") + pi_latex(abs(q))


def _func_part(func: str, B: Fraction, t: Fraction, form: str) -> str:
    fn = rf"\{func}"
    if t == 0:
        inner = _bx(B)
        return rf"{fn} {inner}"
    if B == 1:
        return rf"{fn}\left(x{_signed_pi(t)}\right)"
    if form == "expanded":
        return rf"{fn}\left({_bx(B)}{_signed_pi(B * t)}\right)"
    return rf"{fn} {frac_latex(B)}\left(x{_signed_pi(t)}\right)"


def _const(beta: Fraction) -> str:
    if beta == 0:
        return ""
    return (" + " if beta > 0 else " - ") + frac_latex(abs(beta))
