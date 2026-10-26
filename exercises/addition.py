"""演習:加法定理の応用(三角関数の合成、合成と最大・最小、積和・和積の公式)"""
from fractions import Fraction as F

from exercises.core import Problem, ProblemType, Retry, render, tex_fr, tex_frac_root
from exercises.helpers import Q236, assemble, cos_deg, pi_tex, sin_deg

# (a, b) = (k·ca√ra, k·cb√rb) と R, α(度)の組。a sin x + b cos x = R sin(x + α)
BASE_PAIRS = [((1, 1), (1, 3), (2, 1), 60), ((1, 3), (1, 1), (2, 1), 30), ((1, 1), (1, 1), (1, 2), 45),
              ((1, 1), (-1, 1), (1, 2), -45), ((-1, 1), (1, 1), (1, 2), 135), ((-1, 1), (1, 3), (2, 1), 120),
              ((1, 3), (-1, 1), (2, 1), -30), ((1, 1), (-1, 3), (2, 1), -60), ((-1, 3), (1, 1), (2, 1), 150),
              ((-1, 1), (-1, 1), (1, 2), -135), ((-1, 3), (-1, 1), (2, 1), -150)]


def surd(c, r):
    return tex_frac_root(c, 1, r) if isinstance(c, int) else tex_frac_root(c.numerator, c.denominator, r)


def coef_term(c, r, fn, first):
    """係数 c√r と関数 fn の項(符号つき)"""
    s = surd(abs(c), r)
    s = "" if s == "1" else s
    sign = ("-" if c < 0 else "") if first else (" - " if c < 0 else " + ")
    return f"{sign}{s}\\{fn} x"


def norm180(d):
    d = d % 360
    return d - 360 if d > 180 else d


def sin_form(Rtex, al):
    if al == 0:
        return rf"{Rtex}\sin x"
    return rf"{Rtex}\sin\left(x{' + ' if al > 0 else ' - '}{pi_tex(F(abs(al), 180))}\right)"


def q236_surd(c, r):
    return Q236.sqrt_of(r, c) if r != 1 else Q236(c)


def _pick(rng):
    (ca, ra), (cb, rb), (cR, rR), al = rng.choice(BASE_PAIRS)
    k = rng.choice([1, 1, 2, 3])
    return k * ca, ra, k * cb, rb, k * cR, rR, al


# ============================================================
# 基本:三角関数の合成
# ============================================================
def g_synth(rng):
    a, ra, b, rb, R, rR, al = _pick(rng)
    expr = coef_term(a, ra, "sin", True) + coef_term(b, rb, "cos", False)
    Rtex = surd(R, rR)
    Rtex1 = "" if Rtex == "1" else Rtex
    ans = sin_form(Rtex1, al)
    R2 = R * R * rR
    wrongs = [(sin_form(Rtex1, norm180(90 - al)), "$\\cos\\alpha=\\dfrac{a}{R},\\ \\sin\\alpha=\\dfrac{b}{R}$。$a$ と $b$ の役割を逆にしていないか。"),
              (sin_form(Rtex1, -al), "$\\alpha$ の符号を確かめよう。点 $(a,\\ b)$ がどの象限にあるかで決まる。"),
              (sin_form(str(R2), al), "$R=\\sqrt{a^2+b^2}$。平方根をとり忘れていないか。"),
              (sin_form(Rtex1, norm180(al + 180)), "点 $(a,\\ b)$ の位置から角 $\\alpha$ を読もう。")]
    return Problem(
        "三角関数の合成", "基本",
        rf"${expr}$ を $r\sin(x+\alpha)$ の形に表せ。ただし $r>0,\ -\pi<\alpha\le\pi$ とする。",
        assemble(ans, wrongs, value=al),
        hints=[r"点 $(a,\ b)$ をとり、$r=\sqrt{a^2+b^2}$、$\cos\alpha=\dfrac{a}{r},\ \sin\alpha=\dfrac{b}{r}$。",
               r"$a\sin x+b\cos x=r(\sin x\cos\alpha+\cos x\sin\alpha)=r\sin(x+\alpha)$(加法定理)。"],
        solution=[rf"$r=\sqrt{{a^2+b^2}}=\sqrt{{{R2}}}={Rtex}$",
                  rf"$\cos\alpha=\dfrac{{{surd(a, ra)}}}{{{Rtex}}},\ \sin\alpha=\dfrac{{{surd(b, rb)}}}{{{Rtex}}}$ より $\alpha={pi_tex(F(al, 180))}$",
                  rf"$${expr}={ans}$$"], meta=dict(a=(a, ra), b=(b, rb), al=al))


# ============================================================
# 標準:合成して最大値・最小値
# ============================================================
def g_synth_max(rng):
    a, ra, b, rb, R, rR, al = _pick(rng)
    c = rng.choice([0, 1, 2, -1, 3])
    ask = rng.choice(["最大値", "最小値"])
    expr = coef_term(a, ra, "sin", True) + coef_term(b, rb, "cos", False) + ("" if c == 0 else (" + " if c > 0 else " - ") + str(abs(c)))
    Rq = q236_surd(R, rR)
    ans = (Q236(c) + Rq) if ask == "最大値" else (Q236(c) - Rq)
    other = (Q236(c) - Rq) if ask == "最大値" else (Q236(c) + Rq)
    s_ab = q236_surd(abs(a), ra) + q236_surd(abs(b), rb)
    naive = (Q236(c) + s_ab) if ask == "最大値" else (Q236(c) - s_ab)
    R2 = Q236(R * R * rR)
    sq = (Q236(c) + R2) if ask == "最大値" else (Q236(c) - R2)
    wrongs = [(naive.latex(), "$\\sin x$ と $\\cos x$ が同時に最大になることはない。合成して $r\\sin(x+\\alpha)$ の形にする。"),
              (sq.latex(), "$r=\\sqrt{a^2+b^2}$。平方根をとり忘れていないか。"),
              (other.latex(), f"それは{'最小値' if ask == '最大値' else '最大値'}。"),
              (Rq.latex() if c != 0 else (Rq * 2).latex(), "定数項を足し忘れていないか。")]
    Rtex = surd(R, rR)
    return Problem(
        f"合成して{ask}", "標準", rf"関数 $y={expr}$ の{ask}を求めよ。",
        assemble(ans.latex(), wrongs, value=float(ans)),
        hints=[r"$a\sin x+b\cos x=r\sin(x+\alpha)$ と合成する。", r"$-1\le\sin(x+\alpha)\le1$ なので、$-r\le r\sin(x+\alpha)\le r$。"],
        solution=[rf"$y={sin_form('' if Rtex == '1' else Rtex, al)}" + ("" if c == 0 else (" + " if c > 0 else " - ") + str(abs(c))) + "$",
                  rf"$-1\le\sin(x+\alpha)\le1$ より、{ask}は ${ans.latex()}$"], meta=dict(al=al, c=c))


# ============================================================
# 標準:区間での最大値・最小値(0 ≦ x ≦ π)
# ============================================================
def g_synth_range(rng):
    a, ra, b, rb, R, rR, al = _pick(rng)
    lo, hi = al, al + 180      # x + α の範囲(度)
    vals = [sin_deg(lo % 360), sin_deg(hi % 360)]
    mx = max(vals, key=float)
    mn = min(vals, key=float)
    for t in (90, 270, 450, -90):
        if lo <= t <= hi:
            if t % 360 == 90:
                mx = Q236(1)
            else:
                mn = Q236(-1)
    Rq = q236_surd(R, rR)
    M, m = Rq * mx, Rq * mn
    expr = coef_term(a, ra, "sin", True) + coef_term(b, rb, "cos", False)
    def pair(x, y):  # noqa: E306
        return rf"\text{{最大値 }}{x.latex()},\ \text{{最小値 }}{y.latex()}"
    ans = pair(M, m)
    wrongs = [(pair(Rq, -Rq), "$x$ の範囲が $0\\le x\\le\\pi$ なので、$x+\\alpha$ の範囲を求めて、その範囲での $\\sin$ の値を考える。"),
              (pair(Rq * max(vals, key=float), Rq * min(vals, key=float)), "区間の端だけでなく、途中で $\\sin$ が $\\pm1$ になるところも調べよう。"),
              (pair(-m, -M), "符号を確かめよう。"), (pair(M, -Rq), "最小値をとる位置を確かめよう。"), (pair(Rq, m), "最大値をとる位置を確かめよう。")]
    Rtex = surd(R, rR)
    return Problem(
        "区間での最大値・最小値", "標準", rf"$0\le x\le\pi$ のとき、関数 $y={expr}$ の最大値と最小値を求めよ。",
        assemble(ans, wrongs, value=(float(M), float(m))),
        hints=[r"まず $y=r\sin(x+\alpha)$ と合成する。", r"$0\le x\le\pi$ のとき $x+\alpha$ の範囲を求め、単位円で $\sin$ の値の範囲を読む。"],
        solution=[rf"$y={sin_form('' if Rtex == '1' else Rtex, al)}$",
                  rf"$0\le x\le\pi$ より ${pi_tex(F(lo, 180))}\le x+\alpha\le {pi_tex(F(hi, 180))}$",
                  rf"この範囲で $\sin(x+\alpha)$ は ${mn.latex()}$ から ${mx.latex()}$ まで変化するので、${ans}$"],
        meta=dict(al=al))


# ============================================================
# 基本:積和の公式
# ============================================================
def kx(k):
    return "x" if k == 1 else f"{k}x"


def g_prod_sum(rng):
    m = rng.randint(2, 7)
    n = rng.randint(1, m - 1)
    kind = rng.choice(["sc", "cc", "ss", "cs"])
    p, q = kx(m + n), kx(m - n)
    half = r"\frac{1}{2}"
    if kind == "sc":
        lhs = rf"\sin {kx(m)}\cos {kx(n)}"
        ans = rf"{half}(\sin {p}+\sin {q})"
        wrongs = [(rf"\sin {p}+\sin {q}", "積和の公式には $\\frac12$ がつく。"),
                  (rf"{half}(\sin {p}-\sin {q})", "$\\sin\\alpha\\cos\\beta=\\frac12\\{\\sin(\\alpha+\\beta)+\\sin(\\alpha-\\beta)\\}$。符号を確かめよう。"),
                  (rf"{half}(\cos {p}+\cos {q})", "$\\sin\\times\\cos$ の積は $\\sin$ の和になる。")]
    elif kind == "cs":
        lhs = rf"\cos {kx(m)}\sin {kx(n)}"
        ans = rf"{half}(\sin {p}-\sin {q})"
        wrongs = [(rf"{half}(\sin {p}+\sin {q})", "$\\cos\\alpha\\sin\\beta=\\frac12\\{\\sin(\\alpha+\\beta)-\\sin(\\alpha-\\beta)\\}$。符号を確かめよう。"),
                  (rf"\sin {p}-\sin {q}", "積和の公式には $\\frac12$ がつく。"),
                  (rf"{half}(\cos {q}-\cos {p})", "$\\cos\\times\\sin$ の積は $\\sin$ の和・差になる。")]
    elif kind == "cc":
        lhs = rf"\cos {kx(m)}\cos {kx(n)}"
        ans = rf"{half}(\cos {p}+\cos {q})"
        wrongs = [(rf"\cos {p}+\cos {q}", "積和の公式には $\\frac12$ がつく。"),
                  (rf"{half}(\cos {p}-\cos {q})", "$\\cos\\alpha\\cos\\beta=\\frac12\\{\\cos(\\alpha+\\beta)+\\cos(\\alpha-\\beta)\\}$。符号を確かめよう。"),
                  (rf"{half}(\sin {p}+\sin {q})", "$\\cos\\times\\cos$ の積は $\\cos$ の和になる。")]
    else:
        lhs = rf"\sin {kx(m)}\sin {kx(n)}"
        ans = rf"{half}(\cos {q}-\cos {p})"
        wrongs = [(rf"{half}(\cos {p}-\cos {q})", "$\\sin\\alpha\\sin\\beta=-\\frac12\\{\\cos(\\alpha+\\beta)-\\cos(\\alpha-\\beta)\\}$。符号を確かめよう。"),
                  (rf"{half}(\cos {p}+\cos {q})", "それは $\\cos\\alpha\\cos\\beta$ の公式。"),
                  (rf"\cos {q}-\cos {p}", "積和の公式には $\\frac12$ がつく。")]
    return Problem("積和の公式", "基本", rf"${lhs}$ を和または差の形に表せ。", assemble(ans, wrongs),
                   hints=[r"$\sin\alpha\cos\beta=\frac12\{\sin(\alpha+\beta)+\sin(\alpha-\beta)\}$",
                          r"$\cos\alpha\cos\beta=\frac12\{\cos(\alpha+\beta)+\cos(\alpha-\beta)\}$、$\sin\alpha\sin\beta=-\frac12\{\cos(\alpha+\beta)-\cos(\alpha-\beta)\}$"],
                   solution=[rf"$\alpha={kx(m)},\ \beta={kx(n)}$ とすると $\alpha+\beta={p},\ \alpha-\beta={q}$",
                             rf"$${lhs}={ans}$$"], meta=dict(m=m, n=n, kind=kind))


# ============================================================
# 基本:和積の公式
# ============================================================
def g_sum_prod(rng):
    n = rng.randint(1, 5)
    m = n + 2 * rng.randint(1, 3)
    kind = rng.choice(["s+s", "s-s", "c+c", "c-c"])
    P, Q = kx((m + n) // 2), kx((m - n) // 2)
    if kind == "s+s":
        lhs, ans = rf"\sin {kx(m)}+\sin {kx(n)}", rf"2\sin {P}\cos {Q}"
        wrongs = [(rf"\sin {P}\cos {Q}", "和積の公式には 2 がつく。"), (rf"2\cos {P}\sin {Q}", "それは $\\sin A-\\sin B$ の公式。"),
                  (rf"2\sin {P}\sin {Q}", "$\\sin A+\\sin B=2\\sin\\frac{A+B}{2}\\cos\\frac{A-B}{2}$。")]
    elif kind == "s-s":
        lhs, ans = rf"\sin {kx(m)}-\sin {kx(n)}", rf"2\cos {P}\sin {Q}"
        wrongs = [(rf"2\sin {P}\cos {Q}", "それは $\\sin A+\\sin B$ の公式。"), (rf"\cos {P}\sin {Q}", "和積の公式には 2 がつく。"),
                  (rf"-2\cos {P}\sin {Q}", "符号を確かめよう。")]
    elif kind == "c+c":
        lhs, ans = rf"\cos {kx(m)}+\cos {kx(n)}", rf"2\cos {P}\cos {Q}"
        wrongs = [(rf"\cos {P}\cos {Q}", "和積の公式には 2 がつく。"), (rf"-2\sin {P}\sin {Q}", "それは $\\cos A-\\cos B$ の公式。"),
                  (rf"2\sin {P}\cos {Q}", "$\\cos A+\\cos B=2\\cos\\frac{A+B}{2}\\cos\\frac{A-B}{2}$。")]
    else:
        lhs, ans = rf"\cos {kx(m)}-\cos {kx(n)}", rf"-2\sin {P}\sin {Q}"
        wrongs = [(rf"2\sin {P}\sin {Q}", "$\\cos A-\\cos B=-2\\sin\\frac{A+B}{2}\\sin\\frac{A-B}{2}$。マイナスを忘れていないか。"),
                  (rf"2\cos {P}\cos {Q}", "それは $\\cos A+\\cos B$ の公式。"), (rf"-\sin {P}\sin {Q}", "和積の公式には 2 がつく。")]
    return Problem("和積の公式", "基本", rf"${lhs}$ を積の形に表せ。", assemble(ans, wrongs),
                   hints=[r"$\sin A+\sin B=2\sin\frac{A+B}{2}\cos\frac{A-B}{2}$、$\sin A-\sin B=2\cos\frac{A+B}{2}\sin\frac{A-B}{2}$",
                          r"$\cos A+\cos B=2\cos\frac{A+B}{2}\cos\frac{A-B}{2}$、$\cos A-\cos B=-2\sin\frac{A+B}{2}\sin\frac{A-B}{2}$"],
                   solution=[rf"$\dfrac{{A+B}}{{2}}={P},\ \dfrac{{A-B}}{{2}}={Q}$", rf"$${lhs}={ans}$$"], meta=dict(m=m, n=n, kind=kind))


# ============================================================
# 標準:積和・和積の公式で値を求める
# ============================================================
PAIRS = [(75, 15), (105, 15), (105, 75), (165, 15), (165, 75), (165, 105)]


def g_value_ps(rng):
    A, B = rng.choice(PAIRS)
    kind = rng.choice(["sc", "cc", "ss", "s+s", "c+c", "c-c", "s-s"])
    S, C = sin_deg, cos_deg
    if kind == "sc":
        lhs, val = rf"\sin {A}^\circ\cos {B}^\circ", S(A) * C(B)
        half_only = S(A + B) * F(1, 2)
        formula = rf"\frac12\{{\sin {A + B}^\circ+\sin {A - B}^\circ\}}"
    elif kind == "cc":
        lhs, val = rf"\cos {A}^\circ\cos {B}^\circ", C(A) * C(B)
        half_only = C(A + B) * F(1, 2)
        formula = rf"\frac12\{{\cos {A + B}^\circ+\cos {A - B}^\circ\}}"
    elif kind == "ss":
        lhs, val = rf"\sin {A}^\circ\sin {B}^\circ", S(A) * S(B)
        half_only = C(A - B) * F(1, 2)
        formula = rf"-\frac12\{{\cos {A + B}^\circ-\cos {A - B}^\circ\}}"
    elif kind == "s+s":
        lhs, val = rf"\sin {A}^\circ+\sin {B}^\circ", S(A) + S(B)
        half_only = S((A + B) // 2) * C((A - B) // 2)
        formula = rf"2\sin {(A + B) // 2}^\circ\cos {(A - B) // 2}^\circ"
    elif kind == "s-s":
        lhs, val = rf"\sin {A}^\circ-\sin {B}^\circ", S(A) - S(B)
        half_only = C((A + B) // 2) * S((A - B) // 2)
        formula = rf"2\cos {(A + B) // 2}^\circ\sin {(A - B) // 2}^\circ"
    elif kind == "c+c":
        lhs, val = rf"\cos {A}^\circ+\cos {B}^\circ", C(A) + C(B)
        half_only = C((A + B) // 2) * C((A - B) // 2)
        formula = rf"2\cos {(A + B) // 2}^\circ\cos {(A - B) // 2}^\circ"
    else:
        lhs, val = rf"\cos {A}^\circ-\cos {B}^\circ", C(A) - C(B)
        half_only = S((A + B) // 2) * S((A - B) // 2)
        formula = rf"-2\sin {(A + B) // 2}^\circ\sin {(A - B) // 2}^\circ"
    if val.is_zero():
        raise Retry
    prod = kind in ("sc", "cc", "ss")
    wrongs = [((val * 2).latex() if prod else (val * F(1, 2)).latex(),
               "積和の公式には $\\frac12$ がつく。" if prod else "和積の公式には 2 がつく。"),
              ((-val).latex(), "公式の符号を確かめよう。"),
              (half_only.latex(), "公式の 2 つの項を両方とも計算しよう。" if prod else "和積の公式の 2 をかけ忘れていないか。"),
              ((val + Q236(F(1, 2))).latex(), "公式に代入したあとの計算を確かめよう。")]
    return Problem("積和・和積の公式で値を求める", "標準", rf"${lhs}$ の値を求めよ。",
                   assemble(val.latex(), wrongs, value=float(val)),
                   hints=[r"積和の公式(積 → 和)または和積の公式(和 → 積)を使うと、有名角の値だけで計算できる。"],
                   solution=[rf"$${lhs}={formula}={val.latex()}$$"], meta=dict(A=A, B=B, kind=kind))


REGISTRY = [
    ProblemType("synth", "三角関数の合成", "基本", g_synth),
    ProblemType("prod_sum", "積和の公式", "基本", g_prod_sum),
    ProblemType("sum_prod", "和積の公式", "基本", g_sum_prod),
    ProblemType("synth_max", "合成して最大値・最小値", "標準", g_synth_max),
    ProblemType("synth_range", "区間での最大値・最小値", "標準", g_synth_range),
    ProblemType("value_ps", "積和・和積の公式で値を求める", "標準", g_value_ps),
]

TITLE = "加法定理の応用"


def tab():
    render("addition", REGISTRY, TITLE)
