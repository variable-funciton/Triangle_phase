"""三角関数の合成  a sin x + b cos x = R sin(x + α) = R cos(x + β) の計算。

a, b は 1, √2, √3 の有理数倍（Q236）で与え、R・α・β をできるだけ厳密に表示する。
角度は「π の何倍か」を Fraction で表す（きれいな角でなければ None）。
"""

from __future__ import annotations

import math
from fractions import Fraction

from .angles import angle_latex, pi_latex
from .exact import Q236, cos_deg, sin_deg, sqrt_latex

# 係数 a, b の選択肢（小さい順）
COEF_OPTIONS = sorted(
    [Q236(n) for n in range(-4, 5)]
    + [Q236.sqrt_of(2, s) for s in (1, -1)]
    + [Q236.sqrt_of(3, s) for s in (1, -1, 2, -2)]
    + [Q236(Fraction(s, 2)) for s in (1, -1)]
    + [Q236.sqrt_of(3, Fraction(s, 2)) for s in (1, -1)],
    key=float,
)


def nice_pi(theta: float, denom: int = 12):
    """theta[rad] が π/denom の整数倍なら Fraction（π 単位）を返す"""
    k = theta / math.pi * denom
    if abs(k - round(k)) < 1e-9:
        return Fraction(round(k), denom)
    return None


def normalize_pi(q: Fraction, mode: str) -> Fraction:
    """角（π 単位）を mode = 'pm'（−π < θ ≤ π）または 'pos'（0 ≤ θ < 2π）に直す"""
    q = q % 2
    if mode == "pm" and q > 1:
        q -= 2
    return q


def normalize_rad(t: float, mode: str) -> float:
    t = math.fmod(t, 2 * math.pi)
    if t < 0:
        t += 2 * math.pi
    if mode == "pm" and t > math.pi + 1e-12:
        t -= 2 * math.pi
    return t


def coef_latex(c: Q236, func: str, first: bool) -> str:
    """係数つきの項（例: '\\sqrt{3}\\sin x', ' - \\cos x'）。c = 0 なら空文字"""
    if c.is_zero():
        return ""
    neg = float(c) < 0
    mag = -c if neg else c
    m = "" if mag == Q236(1) else mag.latex()
    sign = ("-" if neg else "") if first else (" - " if neg else " + ")
    return rf"{sign}{m}\{func} x"


class Synthesis:
    def __init__(self, a: Q236, b: Q236, mode: str = "pm"):
        if a.is_zero() and b.is_zero():
            raise ValueError("a = b = 0 は合成できない")
        self.a, self.b, self.mode = a, b, mode
        self.R2 = (a * a + b * b).as_rational()     # 係数が 1 項ずつなので有理数
        self.R = math.sqrt(self.R2)
        self.alpha = normalize_rad(math.atan2(float(b), float(a)), mode)
        self.beta = normalize_rad(self.alpha - math.pi / 2, mode)
        self.alpha_pi = nice_pi(self.alpha)
        self.beta_pi = nice_pi(self.beta)
        if self.alpha_pi is not None:
            self.alpha_pi = normalize_pi(self.alpha_pi, mode)
        if self.beta_pi is not None:
            self.beta_pi = normalize_pi(self.beta_pi, mode)

    # ---- 表示 ----
    def lhs_latex(self) -> str:
        s = coef_latex(self.a, "sin", True)
        s += coef_latex(self.b, "cos", s == "")
        return s

    def R_latex(self) -> str:
        return sqrt_latex(self.R2)

    @staticmethod
    def _rel(q, rad: float, unit: str) -> str:
        """'= π/3' または '≈ 53.13°'（有名角でないとき）"""
        if q is not None:
            return "= " + angle_latex(q, unit)
        return rf"\approx {math.degrees(rad):.2f}^\circ"

    def alpha_rel(self, unit: str = "rad") -> str:
        return self._rel(self.alpha_pi, self.alpha, unit)

    def beta_rel(self, unit: str = "rad") -> str:
        return self._rel(self.beta_pi, self.beta, unit)

    def alpha_latex(self, unit: str = "rad") -> str:
        """α = … の右辺（有名角でなければ「α ≈ 53.13°」全体）"""
        return r"\alpha " + self.alpha_rel(unit)

    def beta_latex(self, unit: str = "rad") -> str:
        return r"\beta " + self.beta_rel(unit)

    @staticmethod
    def _shift(q, rad: float, sym: str, unit: str) -> str:
        if q is None:
            return rf"x + {sym}"   # α, β は角そのもの（負の値もとる）なので常に「+」
        if q == 0:
            return "x"
        mag = angle_latex(abs(q), unit)
        return rf"x {'+' if q > 0 else '-'} {mag}"

    def sin_form_latex(self, unit: str = "rad") -> str:
        R = "" if self.R2 == 1 else self.R_latex()
        return rf"{R}\sin\left({self._shift(self.alpha_pi, self.alpha, r'\alpha', unit)}\right)"

    def cos_form_latex(self, unit: str = "rad") -> str:
        R = "" if self.R2 == 1 else self.R_latex()
        return rf"{R}\cos\left({self._shift(self.beta_pi, self.beta, r'\beta', unit)}\right)"

    def ratio_latex(self, num: Q236, sign: int = 1) -> str:
        """num / R を厳密に（例: cos α = a/R）。R が無理数でも分母の有理化はせず a/R の形で表示"""
        if self.R2.denominator == 1 and math.isqrt(self.R2.numerator) ** 2 == self.R2.numerator:
            return (num * sign / math.isqrt(self.R2.numerator)).latex()
        # R² が平方数でないとき: num/R = num·R/R²
        val = num * sign
        if val.is_zero():
            return "0"
        return rf"\frac{{{val.latex()}}}{{{self.R_latex()}}}"

    # ---- 値 ----
    def value(self, x: float) -> float:
        return float(self.a) * math.sin(x) + float(self.b) * math.cos(x)

    def exact_value_at(self, x_pi: Fraction) -> Q236:
        """x = x_pi·π（15° の倍数）での厳密値"""
        deg = Fraction(x_pi) * 180
        return self.a * sin_deg(deg) + self.b * cos_deg(deg)

    def extrema(self, lo_pi: Fraction, hi_pi: Fraction, include_hi: bool = True, unit: str = "rad"):
        """区間 [lo, hi]（include_hi=False なら [lo, hi)）での最大・最小。
        戻り値: {"max": (値の LaTeX, 値, [x の LaTeX]), "min": (...)}"""
        lo, hi = float(lo_pi) * math.pi, float(hi_pi) * math.pi
        cands = []  # (値 float, 値 latex, x latex)
        for xq, ok in ((lo_pi, True), (hi_pi, include_hi)):
            if ok:
                v = self.exact_value_at(xq)
                cands.append((float(v), v.latex(), angle_latex(xq, unit)))
        # 内部の極値: x + α = π/2 + 2kπ（最大 R）, 3π/2 + 2kπ（最小 −R）
        for target, sgn in ((math.pi / 2, 1), (3 * math.pi / 2, -1)):
            base = target - self.alpha
            for k in range(-3, 4):
                x = base + 2 * k * math.pi
                if lo + 1e-12 < x < hi - 1e-12:
                    xq = nice_pi(x)
                    xl = angle_latex(xq, unit) if xq is not None else rf"{math.degrees(x):.2f}^\circ"
                    R = self.R_latex()
                    cands.append((sgn * self.R, R if sgn > 0 else f"-{R}", xl))
        out = {}
        for key, pick in (("max", max), ("min", min)):
            best = pick(c[0] for c in cands)
            same = [c for c in cands if abs(c[0] - best) < 1e-9]
            xs = list(dict.fromkeys(c[2] for c in same))
            out[key] = (same[0][1], best, xs)
        return out
