"""三角関数の値を厳密に扱うための小さな数の体系。

15° の倍数の角の sin・cos の値は、すべて
    c1 + c2·√2 + c3·√3 + c6·√6   （c は有理数）
の形で書ける。この形の数どうしの和・差・積は再びこの形になるので、
積和・和積の公式や合成の計算を「近似なし」で確かめられる。
"""

from __future__ import annotations

import math
from fractions import Fraction

BASIS = (1, 2, 3, 6)
# √i · √j = k · √m  の表
_MUL = {
    (1, 1): (1, 1), (1, 2): (1, 2), (1, 3): (1, 3), (1, 6): (1, 6),
    (2, 2): (2, 1), (2, 3): (1, 6), (2, 6): (2, 3),
    (3, 3): (3, 1), (3, 6): (3, 2),
    (6, 6): (6, 1),
}


class Q236:
    """c1 + c2√2 + c3√3 + c6√6 （c は Fraction）"""

    __slots__ = ("c",)

    def __init__(self, c1=0, c2=0, c3=0, c6=0):
        self.c = {1: Fraction(c1), 2: Fraction(c2), 3: Fraction(c3), 6: Fraction(c6)}

    @classmethod
    def sqrt_of(cls, n: int, coef=1) -> "Q236":
        """coef·√n （n は 1, 2, 3, 6）"""
        q = cls()
        q.c[n] = Fraction(coef)
        return q

    # ---- 演算 ----
    @staticmethod
    def _wrap(x) -> "Q236":
        return x if isinstance(x, Q236) else Q236(Fraction(x))

    def __add__(self, o):
        o = self._wrap(o)
        return Q236(*(self.c[k] + o.c[k] for k in BASIS))

    __radd__ = __add__

    def __neg__(self):
        return Q236(*(-self.c[k] for k in BASIS))

    def __sub__(self, o):
        return self + (-self._wrap(o))

    def __rsub__(self, o):
        return self._wrap(o) - self

    def __mul__(self, o):
        o = self._wrap(o)
        out = {k: Fraction(0) for k in BASIS}
        for i in BASIS:
            for j in BASIS:
                if self.c[i] and o.c[j]:
                    f, m = _MUL[(min(i, j), max(i, j))]
                    out[m] += self.c[i] * o.c[j] * f
        return Q236(*(out[k] for k in BASIS))

    __rmul__ = __mul__

    def __truediv__(self, o):
        """有理数でのみ割れる"""
        o = Fraction(o) if not isinstance(o, Q236) else o.as_rational()
        return Q236(*(self.c[k] / o for k in BASIS))

    def __eq__(self, o):
        try:
            o = self._wrap(o)
        except (TypeError, ValueError):
            return NotImplemented
        return all(self.c[k] == o.c[k] for k in BASIS)

    def __hash__(self):
        return hash(tuple(self.c[k] for k in BASIS))

    def __float__(self):
        return sum(float(self.c[k]) * math.sqrt(k) for k in BASIS)

    def __repr__(self):
        return f"Q236({', '.join(str(self.c[k]) for k in BASIS)})"

    def is_zero(self) -> bool:
        return all(v == 0 for v in self.c.values())

    def is_rational(self) -> bool:
        return all(self.c[k] == 0 for k in (2, 3, 6))

    def as_rational(self) -> Fraction:
        if not self.is_rational():
            raise ValueError("無理数を含む")
        return self.c[1]

    # ---- 表示 ----
    def _parts(self):
        """(共通分母 d, 全体の符号が負か, [(基底, 分子)]) — √ の大きい項から、正の項を先に並べる"""
        terms = [(k, v) for k, v in self.c.items() if v != 0]
        d = math.lcm(*(v.denominator for _, v in terms))
        nums = [(k, int(v * d)) for k, v in terms]
        neg = all(n < 0 for _, n in nums)
        if neg:
            nums = [(k, -n) for k, n in nums]
        nums.sort(key=lambda t: (t[1] < 0, -t[0]))
        return d, neg, nums

    def latex(self) -> str:
        if self.is_zero():
            return "0"
        d, neg, nums = self._parts()
        parts = []
        for i, (k, n) in enumerate(nums):
            mag = abs(n)
            body = str(mag) if k == 1 else (rf"\sqrt{{{k}}}" if mag == 1 else rf"{mag}\sqrt{{{k}}}")
            sign = ("-" if n < 0 else "") if i == 0 else (" - " if n < 0 else " + ")
            parts.append(sign + body)
        inner = "".join(parts)
        if d != 1:
            s = rf"\frac{{{inner}}}{{{d}}}"
        else:
            s = f"({inner})" if (neg and len(nums) > 1) else inner
        return ("-" + s) if neg else s

    def text(self) -> str:
        """グラフのラベルなど LaTeX が使えない場所用"""
        if self.is_zero():
            return "0"
        d, neg, nums = self._parts()
        parts = []
        for i, (k, n) in enumerate(nums):
            mag = abs(n)
            body = str(mag) if k == 1 else (f"√{k}" if mag == 1 else f"{mag}√{k}")
            sign = ("−" if n < 0 else "") if i == 0 else (" − " if n < 0 else " + ")
            parts.append(sign + body)
        inner = "".join(parts)
        if d != 1:
            inner = (f"({inner})" if len(nums) > 1 else inner) + f"/{d}"
        elif neg and len(nums) > 1:
            inner = f"({inner})"
        return ("−" + inner) if neg else inner


# ---------------- 15° の倍数の sin, cos ----------------
_SIN_BASE = {
    0: Q236(0),
    15: Q236(0, Fraction(-1, 4), 0, Fraction(1, 4)),   # (√6 − √2)/4
    30: Q236(Fraction(1, 2)),
    45: Q236(0, Fraction(1, 2)),                        # √2/2
    60: Q236(0, 0, Fraction(1, 2)),                     # √3/2
    75: Q236(0, Fraction(1, 4), 0, Fraction(1, 4)),    # (√6 + √2)/4
    90: Q236(1),
}


def is_nice_deg(deg) -> bool:
    return Fraction(deg) % 15 == 0


def sin_deg(deg) -> Q236:
    """deg が 15 の倍数のときの sin の厳密値"""
    if not is_nice_deg(deg):
        raise ValueError("15° の倍数のみ")
    d = int(Fraction(deg)) % 360
    if d <= 90:
        return _SIN_BASE[d]
    if d <= 180:
        return _SIN_BASE[180 - d]
    if d <= 270:
        return -_SIN_BASE[d - 180]
    return -_SIN_BASE[360 - d]


def cos_deg(deg) -> Q236:
    return sin_deg(90 - Fraction(deg))


# ---------------- 平方根の表示 ----------------
def sqrt_latex(x) -> str:
    """√x（x は非負の有理数）を k√m / d の形で表示"""
    x = Fraction(x)
    if x < 0:
        raise ValueError("負の数")
    if x == 0:
        return "0"
    p, q = x.numerator, x.denominator
    n = p * q  # √(p/q) = √(pq)/q
    k, m = 1, n
    f = 2
    while f * f <= m:
        while m % (f * f) == 0:
            k *= f
            m //= f * f
        f += 1
    g = math.gcd(k, q)
    k, q = k // g, q // g
    body = (str(k) if m == 1 else (rf"\sqrt{{{m}}}" if k == 1 else rf"{k}\sqrt{{{m}}}"))
    return body if q == 1 else rf"\frac{{{body}}}{{{q}}}"


def sqrt_text(x) -> str:
    """√x を LaTeX なしの文字列で（例: '2√3', '√2/2'）"""
    s = sqrt_latex(x)
    if s.startswith(r"\frac{"):
        num, den = s[len(r"\frac{"):-1].split("}{")
        s = f"{num}/{den}"
    return s.replace(r"\sqrt{", "√").replace("}", "")


def tan_deg(deg):
    """deg が 15 の倍数のときの tan の厳密値（定義されないときは None）。
    tan θ = (1 − cos 2θ) / sin 2θ を使う（sin 2θ は 1 項だけの数なので割り算ができる）"""
    if not is_nice_deg(deg):
        raise ValueError("15° の倍数のみ")
    d = int(Fraction(deg)) % 180
    if d == 0:
        return Q236(0)
    if d == 90:
        return None
    s2 = sin_deg(2 * d)
    inv = s2 * (1 / (s2 * s2).as_rational())
    return (1 - cos_deg(2 * d)) * inv
