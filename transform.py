"""演習:グラフの変換と合成(テントマップ f と台形 g、拡大・平行移動、合成関数、漸化式)

f(x) = 2x (0 ≦ x ≦ 1/2)、2 − 2x (1/2 < x ≦ 1)、0(それ以外)  … 「テントマップの変換と合成」のページと同じ
g(x) = 3x (0 ≦ x < 1/3)、1 (1/3 ≦ x < 2/3)、3 − 3x (2/3 ≦ x < 1)、0(それ以外)
"""
from fractions import Fraction as F

from exercises.core import Problem, ProblemType, Retry, render, tex_fr
from exercises.helpers import assemble
from utils.tent import tent_exact

DEF_F = r"f(x)=\begin{cases}2x & (0\le x\le\frac12)\\ 2-2x & (\frac12<x\le1)\\ 0 & (\text{それ以外})\end{cases}"
DEF_G = r"g(x)=\begin{cases}3x & (0\le x<\frac13)\\ 1 & (\frac13\le x<\frac23)\\ 3-3x & (\frac23\le x<1)\\ 0 & (\text{それ以外})\end{cases}"


def g_exact(x):
    x = F(x)
    if 0 <= x < F(1, 3):
        return 3 * x
    if F(1, 3) <= x < F(2, 3):
        return F(1)
    if F(2, 3) <= x < 1:
        return 3 - 3 * x
    return F(0)


def f_exact(x):
    x = F(x)
    return tent_exact(x) if 0 <= x <= 1 else F(0)


# ============================================================
# 基本:関数の値と合成関数の値
# ============================================================
def g_compose(rng):
    x = rng.choice([F(k, 12) for k in range(1, 12)] + [F(k, 8) for k in range(1, 8)])
    order = rng.choice(["fg", "gf", "ff"])
    fx, gx = f_exact(x), g_exact(x)
    if order == "fg":
        ans, inner, outer, lhs = f_exact(gx), gx, "f", r"f(g(x))"
        swap = g_exact(fx)
    elif order == "gf":
        ans, inner, outer, lhs = g_exact(fx), fx, "g", r"g(f(x))"
        swap = f_exact(gx)
    else:
        ans, inner, outer, lhs = f_exact(fx), fx, "f", r"f(f(x))"
        swap = fx
    wrongs = [(tex_fr(swap), "合成の順番を確かめよう。$f(g(x))$ は、先に $g$、その結果に $f$ をほどこす。"),
              (tex_fr(inner), "内側の関数の値を求めたあと、外側の関数にもう一度代入する。"),
              (tex_fr(fx * gx), "合成関数は積ではない。"), (tex_fr(1 - ans), "場合分けのどの式を使うか、区間を確かめよう。"),
              (tex_fr(ans + F(1, 2)), "場合分けの区間を確かめよう。")]
    xt = tex_fr(x)
    return Problem("合成関数の値", "基本",
                   rf"$${DEF_F}\qquad {DEF_G}$$" + "\n\n" + rf"のとき、$x={xt}$ における ${lhs}$ の値を求めよ。",
                   assemble(tex_fr(ans), wrongs, value=float(ans)),
                   hints=[r"内側から順に計算する。たとえば $f(g(x))$ なら、まず $g(x)$ を求めて、それを $f$ に代入する。",
                          r"代入する値がどの区間にあるかで、使う式が変わる。"],
                   solution=[rf"内側:${'g' if order == 'fg' else 'f'}\left({xt}\right)={tex_fr(inner)}$",
                             rf"外側:${outer}\left({tex_fr(inner)}\right)={tex_fr(ans)}$"], meta=dict(x=str(x), order=order))


# ============================================================
# 標準:変換したテントの頂点
# ============================================================
def g_vertex(rng):
    a = rng.choice([1, 2, 3, F(1, 2), -1, -2])
    b = rng.choice([1, 2, 3, F(1, 2)])
    p = rng.choice([0, 1, 2, -1, F(1, 2)])
    q = rng.choice([0, 1, -1, 2])
    vx, vy = F(p) + F(1, 2) / F(b), F(a) + F(q)
    pt = lambda X, Y: rf"\left({tex_fr(X)},\ {tex_fr(Y)}\right)"  # noqa: E731
    wrongs = [(pt(F(p) - F(1, 2) / F(b), vy), "$x-p$ が $\\frac{1}{2b}$ になる所なので、$x=p+\\frac{1}{2b}$。符号を確かめよう。"),
              (pt(F(p) + F(b, 2), vy), "$b(x-p)=\\frac12$ を解くと $x=p+\\frac{1}{2b}$。$b$ をかけていないか。"),
              (pt(vx, F(a) - F(q)), "$y$ 方向は $a$ 倍してから $q$ 足す。"),
              (pt(vx, F(q)), "頂点の高さは $a\\cdot f\\left(\\frac12\\right)+q=a+q$。"), (pt(F(p) + F(1, 2), vy), "$x$ 方向に $\\frac1b$ 倍することを忘れていないか。")]
    def tx(v, var):  # noqa: E306
        return "" if v == 1 else ("-" if v == -1 else tex_fr(v))
    inner = rf"{tx(b, 'x')}" + (rf"(x{'-' if p > 0 else '+'}{tex_fr(abs(F(p)))})" if p != 0 else "x")
    expr = rf"y={tx(a, '')}f\left({inner}\right)" + ("" if q == 0 else (f"+{q}" if q > 0 else f"{q}"))
    return Problem("変換したグラフの頂点", "標準",
                   rf"テントマップ $f(x)$(頂点 $\left(\frac12,\ 1\right)$)を変換した ${expr}$ のグラフの頂点の座標を求めよ。",
                   assemble(pt(vx, vy), wrongs),
                   hints=[r"$y=af(b(x-p))+q$ は、$x$ 方向に $\frac1b$ 倍、$p$ 平行移動、$y$ 方向に $a$ 倍、$q$ 平行移動したもの。",
                          r"頂点は $b(x-p)=\frac12$ となる $x$ で、高さは $a\cdot1+q$。"],
                   solution=[rf"$b(x-p)=\frac12$ より $x={tex_fr(F(p))}+\dfrac{{1}}{{2\cdot{tex_fr(F(b))}}}={tex_fr(vx)}$",
                             rf"高さは ${tex_fr(F(a))}\times1+{tex_fr(F(q))}={tex_fr(vy)}$、頂点 ${pt(vx, vy)}$"],
                   meta=dict(a=str(a), b=str(b), p=str(p), q=str(q)))


# ============================================================
# 標準:f を n 回合成したグラフの山の数
# ============================================================
def g_iterate(rng):
    n = rng.randint(2, 6)
    ans = 2 ** (n - 1)
    wrongs = [(str(2 * n), "合成するたびに山の数は 2 倍になる(足し算ではない)。"), (str(2 ** n), "1 回(f そのもの)のとき山は 1 つ。$2^{n-1}$ 個。"),
              (str(n), "グラフをかいて確かめよう。1 回合成するごとに、各山が 2 つに分かれる。"), (str(2 ** (n - 1) + 1), "山の数は $2^{n-1}$。")]
    return Problem("合成をくり返したグラフ", "標準",
                   rf"テントマップ $f$ を ${n}$ 回合成した関数 $\underbrace{{f(f(\cdots f}}_{{{n}\text{{回}}}}(x)\cdots))$ の、$0\le x\le1$ でのグラフの山(値 1 をとる点)の数を求めよ。",
                   assemble(str(ans), wrongs, value=ans),
                   hints=[r"$f$ の値が 0 から 1 まで上がる区間で、もう一度 $f$ をほどこすと、山が 1 つできる。", r"1 回:1 個、2 回:2 個、3 回:4 個、…"],
                   solution=[rf"合成するたびに山の数は 2 倍になるので、${n}$ 回では $2^{{{n - 1}}}={ans}$ 個"], meta=dict(n=n))


# ============================================================
# 基本:漸化式 x_{k+1} = f(x_k)
# ============================================================
def g_orbit(rng):
    x0 = rng.choice([F(1, 5), F(2, 5), F(1, 7), F(2, 7), F(3, 7), F(1, 9), F(2, 9), F(1, 3), F(1, 6), F(3, 10)])
    k = rng.choice([2, 3])
    xs = [x0]
    for _ in range(k):
        xs.append(f_exact(xs[-1]))
    ans = xs[k]
    wrongs = [(tex_fr(xs[k - 1]), f"$x_{{{k}}}$ は $f$ を ${k}$ 回ほどこした値。回数を確かめよう。"),
              (tex_fr(2 ** k * x0) if 2 ** k * x0 != ans else None, "$\\frac12$ をこえたら $2-2x$ の式を使う。"),
              (tex_fr(f_exact(ans)), f"$x_0$ から数えて ${k}$ 回。"), (tex_fr(1 - ans), "場合分けを確かめよう。"), (tex_fr(ans / 2), "計算を確かめよう。")]
    return Problem("漸化式とテントマップ", "基本",
                   rf"テントマップ $f$ を使って $x_0={tex_fr(x0)},\ x_{{n+1}}=f(x_n)$ で数列を作る。$x_{{{k}}}$ を求めよ。",
                   assemble(tex_fr(ans), wrongs, value=float(ans)),
                   hints=[r"$x_1=f(x_0),\ x_2=f(x_1),\ \dots$ と順に計算する。", r"$\frac12$ 以下なら $2x$、$\frac12$ より大きければ $2-2x$。"],
                   solution=[r"$" + r",\ ".join(rf"x_{{{i}}}={tex_fr(v)}" for i, v in enumerate(xs)) + "$"], meta=dict(x0=str(x0), k=k))


REGISTRY = [
    ProblemType("compose", "合成関数の値", "基本", g_compose),
    ProblemType("orbit", "漸化式とテントマップ", "基本", g_orbit),
    ProblemType("vertex", "変換したグラフの頂点", "標準", g_vertex),
    ProblemType("iterate", "合成をくり返したグラフ", "標準", g_iterate),
]

TITLE = "グラフの変換と合成"


def tab():
    render("transform", REGISTRY, TITLE)
