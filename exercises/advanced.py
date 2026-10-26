"""演習:発展(逆三角関数の主値、接線の傾き、テイラー展開)"""
import math
from fractions import Fraction as F

from exercises.core import Problem, ProblemType, Retry, render, tex_fr
from exercises.helpers import assemble, cos_deg, pi_tex, sin_deg

SIN_VALS = [("0", 0), (r"\frac{1}{2}", 30), (r"\frac{\sqrt{2}}{2}", 45), (r"\frac{\sqrt{3}}{2}", 60), ("1", 90),
            (r"-\frac{1}{2}", -30), (r"-\frac{\sqrt{2}}{2}", -45), (r"-\frac{\sqrt{3}}{2}", -60), ("-1", -90)]
TAN_VALS = [("0", 0), ("1", 45), (r"\sqrt{3}", 60), (r"\frac{1}{\sqrt{3}}", 30), ("-1", -45), (r"-\sqrt{3}", -60),
            (r"-\frac{1}{\sqrt{3}}", -30)]


def P(deg):
    return pi_tex(F(deg, 180))


# ============================================================
# 基本:逆三角関数の値(主値)
# ============================================================
def g_arc(rng):
    fn = rng.choice(["sin", "cos", "tan"])
    if fn == "tan":
        kt, p = rng.choice(TAN_VALS)
    else:
        kt, p = rng.choice(SIN_VALS)
        if fn == "cos":
            p = 90 - p
    ans = P(p)
    cands = [(P(90 - p) if fn != "cos" else P(90 - p), "$\\sin$ と $\\cos$ の値を取り違えていないか。"),
             (P(-p) if p != 0 else P(180), "主値の範囲を確かめよう。" + {"sin": "$\\arcsin$ は $-\\frac{\\pi}{2}$ 〜 $\\frac{\\pi}{2}$。",
                                                                      "cos": "$\\arccos$ は $0$ 〜 $\\pi$。",
                                                                      "tan": "$\\arctan$ は $-\\frac{\\pi}{2}$ 〜 $\\frac{\\pi}{2}$。"}[fn]),
             (P(180 - p) if fn == "sin" else P(360 - p) if fn == "cos" else P(p + 180),
              "値が同じになる角はたくさんあるが、主値はその範囲の中の 1 つだけ。"),
             (P(p + 30), "単位円をかいて確かめよう。"), (P(p - 30), "単位円をかいて確かめよう。")]
    return Problem("逆三角関数の値(主値)", "基本", rf"$\arc{fn}\left({kt}\right)$ の値を求めよ。", assemble(ans, cands),
                   hints=[rf"$\arc{fn} k$ は「$\{fn}\theta=k$ となる角のうち、主値の範囲にあるもの」。",
                          r"主値の範囲:$\arcsin$ と $\arctan$ は $-\frac{\pi}{2}$ 〜 $\frac{\pi}{2}$、$\arccos$ は $0$ 〜 $\pi$。"],
                   solution=[rf"$\{fn}\theta={kt}$ で、主値の範囲にある角は $\theta={ans}$"], meta=dict(fn=fn, p=p))


# ============================================================
# 標準:arcsin(sin θ) などの値
# ============================================================
def g_arc_of(rng):
    fn = rng.choice(["sin", "cos", "tan"])
    deg = rng.choice([d for d in range(-330, 360, 30) if d % 90 != 0] + [d for d in (135, -135, 225, 315, -45, 45)])
    if fn == "tan" and deg % 180 in (90,):
        raise Retry
    if fn == "sin":
        v = math.degrees(math.asin(math.sin(math.radians(deg))))
    elif fn == "cos":
        v = math.degrees(math.acos(math.cos(math.radians(deg))))
    else:
        v = math.degrees(math.atan(math.tan(math.radians(deg))))
    ans = round(v)
    if ans == deg:
        raise Retry
    cands = [(P(deg), f"$\\arc{fn}(\\{fn}\\theta)=\\theta$ となるのは、$\\theta$ が主値の範囲にあるときだけ。"),
             (P(-ans) if ans != 0 else P(180), "符号を確かめよう。"),
             (P(180 - ans) if fn != "cos" else P(360 - ans), "主値の範囲に入る角を選ぼう。"), (P(ans + 90), "単位円で確かめよう。")]
    return Problem("逆三角関数と三角関数の組み合わせ", "標準", rf"$\arc{fn}\left(\{fn} {P(deg)}\right)$ の値を求めよ。",
                   assemble(P(ans), cands),
                   hints=[rf"まず $\{fn} {P(deg)}$ の値を求める。", r"その値をとる角のうち、主値の範囲にあるものを探す。"],
                   solution=[rf"$\{fn} {P(deg)}$ と同じ値をとる、主値の範囲の角は ${P(ans)}$"], meta=dict(fn=fn, deg=deg))


# ============================================================
# 基本:接線の傾き
# ============================================================
def g_slope(rng):
    fn = rng.choice(["sin", "cos"])
    deg = rng.choice([0, 30, 45, 60, 90, 120, 135, 150, 180, 240, 270, 300])
    val = cos_deg(deg) if fn == "sin" else -sin_deg(deg)
    ans = val.latex()
    other = (sin_deg(deg) if fn == "sin" else cos_deg(deg)).latex()
    cands = [(other, "それは関数の値(点の $y$ 座標)。傾きは、" + ("$\\sin x$ の接線の傾き $=\\cos x$。" if fn == "sin" else "$\\cos x$ の接線の傾き $=-\\sin x$。")),
             ((-val).latex(), "符号を確かめよう。" + ("" if fn == "sin" else "$\\cos x$ の傾きは $-\\sin x$(マイナスがつく)。")),
             ((-sin_deg(deg) if fn == "sin" else cos_deg(deg)).latex(), "傾きを並べた関数を確かめよう(「接線の傾きと cos x」のページ)。"),
             ("1", "グラフの形から、その点で上り坂か下り坂かを確かめよう。"), ("0", "その点で接線は水平か確かめよう。"),
             (r"\frac{1}{2}", "傾きの値を確かめよう。")]
    return Problem("接線の傾き", "基本", rf"$y=\{fn} x$ のグラフの、$x={P(deg)}$ における接線の傾きを求めよ。",
                   assemble(ans, cands, value=float(val)),
                   hints=[r"$y=\sin x$ の接線の傾きを並べると $y=\cos x$、$y=\cos x$ の接線の傾きを並べると $y=-\sin x$。"],
                   solution=[rf"傾きは $" + (r"\cos x" if fn == "sin" else r"-\sin x") + rf"$ に $x={P(deg)}$ を代入して ${ans}$"],
                   meta=dict(fn=fn, deg=deg))


# ============================================================
# 基本:テイラー展開の係数
# ============================================================
def g_taylor_coef(rng):
    fn = rng.choice(["sin", "cos"])
    k = rng.randint(1, 4)
    n = 2 * k + 1 if fn == "sin" else 2 * k
    c = F((-1) ** k, math.factorial(n))
    ans = tex_fr(c)
    cands = [(tex_fr(-c), "符号は項ごとに交互に変わる:$+,\\ -,\\ +,\\ \\dots$"), (tex_fr(F((-1) ** k, n)), "分母は $n$ ではなく $n!$(階乗)。"),
             (tex_fr(F((-1) ** k, math.factorial(n - 1))), f"$x^{{{n}}}$ の係数の分母は ${n}!$。"),
             (tex_fr(F((-1) ** (k + 1), n)), "階乗と符号の両方を確かめよう。"), ("0", "$\\sin x$ は奇数乗、$\\cos x$ は偶数乗の項だけが現れる。")]
    return Problem("テイラー展開の係数", "基本",
                   rf"$\{fn} x$ を $x=0$ のまわりで展開した多項式(マクローリン展開)で、$x^{{{n}}}$ の係数を求めよ。",
                   assemble(ans, cands, value=float(c)),
                   hints=[r"$\sin x=x-\dfrac{x^3}{3!}+\dfrac{x^5}{5!}-\cdots$、$\cos x=1-\dfrac{x^2}{2!}+\dfrac{x^4}{4!}-\cdots$"],
                   solution=[rf"$x^{{{n}}}$ の項は $\displaystyle {'+' if k % 2 == 0 else '-'}\frac{{x^{{{n}}}}}{{{n}!}}$ なので、係数は ${ans}$"],
                   meta=dict(fn=fn, n=n))


# ============================================================
# 標準:テイラー展開で近似値
# ============================================================
def g_taylor_val(rng):
    fn = rng.choice(["sin", "cos"])
    x = rng.choice([F(1, 10), F(2, 10), F(3, 10), F(1, 2)])
    xf = float(x)
    if fn == "sin":
        v = xf - xf ** 3 / 6
        poly = r"x-\dfrac{x^3}{6}"
        w1, w2, w3 = xf, xf - xf ** 3 / 3, xf + xf ** 3 / 6
    else:
        v = 1 - xf ** 2 / 2
        poly = r"1-\dfrac{x^2}{2}"
        w1, w2, w3 = 1.0, 1 - xf ** 2, 1 + xf ** 2 / 2
    f5 = lambda y: f"{y:.5f}"  # noqa: E731
    cands = [(f5(w1), "それは 1 次(0 次)の近似。2 つ目の項まで使う。"), (f5(w2), "$3!=6$($2!=2$)で割る。"),
             (f5(w3), "符号を確かめよう(交互に $+,\\ -$)。"), (f5(v + 0.001), "計算を確かめよう。")]
    return Problem("テイラー展開で近似値", "標準",
                   rf"$\{fn} x\approx {poly}$ を用いて、$\{fn} {tex_fr(x) if x.denominator != 10 else f'{xf:.1f}'}$ の近似値を小数第 5 位まで求めよ。",
                   assemble(f5(v), cands, value=v),
                   hints=[rf"$x={xf}$ を代入する。", r"$x$ が小さいほど、近似はよくなる(「テイラー展開」のページで確かめよう)。"],
                   solution=[rf"$${poly.replace(chr(92) + 'dfrac', chr(92) + 'frac')}={f5(v)}$$",
                             rf"(本当の値は $\{fn} {xf}={f5(math.sin(xf) if fn == 'sin' else math.cos(xf))}\cdots$)"],
                   meta=dict(fn=fn, x=xf))


REGISTRY = [
    ProblemType("arc", "逆三角関数の値(主値)", "基本", g_arc),
    ProblemType("slope", "接線の傾き", "基本", g_slope),
    ProblemType("tcoef", "テイラー展開の係数", "基本", g_taylor_coef),
    ProblemType("arc_of", "逆三角関数と三角関数の組み合わせ", "標準", g_arc_of),
    ProblemType("tval", "テイラー展開で近似値", "標準", g_taylor_val),
]

TITLE = "発展(逆三角関数・接線・テイラー展開)"


def tab():
    render("advanced", REGISTRY, TITLE)
