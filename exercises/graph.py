"""演習:三角関数のグラフ(周期・最大最小・平行移動・グラフから式・方程式・不等式・角の変換)"""
from fractions import Fraction as F

from exercises.core import Problem, ProblemType, Retry, render, tex_fr
from exercises.fig import same_graph
from exercises.helpers import assemble, pi_tex
from utils.trig import Wave

B_CHOICES = [F(2), F(3), F(4), F(1, 2), F(1, 3), F(2, 3), F(3, 2)]


def coef_tex(A):
    return "" if A == 1 else "-" if A == -1 else tex_fr(A)


def bx_tex(B):
    if B == 1:
        return "x"
    return (str(B) if B.denominator == 1 else tex_fr(B)) + "x"


def inner_tex(B, c):
    """Bx + c(c は π の何倍か)"""
    if c == 0:
        return bx_tex(B)
    return bx_tex(B) + (" + " if c > 0 else " - ") + pi_tex(abs(c))


def const_tex(beta):
    return "" if beta == 0 else (" + " if beta > 0 else " - ") + tex_fr(abs(beta))


# ============================================================
# 基本:周期
# ============================================================
def g_period(rng):
    fn = rng.choice(["sin", "cos", "tan"])
    B = rng.choice(B_CHOICES)
    A = rng.choice([1, 2, 3, -1, -2, F(1, 2)])
    c = rng.choice([F(0), F(1, 3), F(-1, 4), F(1, 2), F(1, 6)])
    base = F(1) if fn == "tan" else F(2)
    ans = base / B
    expr = rf"y={coef_tex(A)}\{fn}\left({inner_tex(B, c)}\right)"
    wrongs = [(pi_tex(base * B), "周期は $\\frac{2\\pi}{B}$($\\tan$ は $\\frac{\\pi}{B}$)。$B$ をかけていないか。"),
              (pi_tex(base), "$x$ の係数 $B$ で割るのを忘れていないか。"),
              (pi_tex((3 - base) / B), "$\\sin,\\ \\cos$ の周期は $2\\pi$、$\\tan$ の周期は $\\pi$。もとの周期を確かめよう。"),
              (pi_tex(base / B / 2), "周期は $\\frac{2\\pi}{B}$。2 で割りすぎていないか。")]
    return Problem("三角関数の周期", "基本", rf"関数 ${expr}$ の周期を求めよ。",
                   assemble(pi_tex(ans), wrongs, value=float(ans)),
                   hints=[r"$y=\sin x,\ \cos x$ の周期は $2\pi$、$y=\tan x$ の周期は $\pi$。",
                          r"$x$ の係数が $B$ なら、グラフは $x$ 軸方向に $\frac1B$ 倍され、周期も $\frac1B$ 倍になる。振幅や平行移動は周期に関係しない。"],
                   solution=[rf"$x$ の係数は ${tex_fr(B)}$ なので、周期は $\dfrac{{{pi_tex(base)}}}{{{tex_fr(B)}}}={pi_tex(ans)}$"],
                   meta=dict(fn=fn, B=str(B)))


# ============================================================
# 基本:最大値・最小値
# ============================================================
def g_maxmin(rng):
    fn = rng.choice(["sin", "cos"])
    A = rng.choice([2, 3, -2, -3, F(1, 2), F(-1, 2), 4, -1])
    beta = rng.choice([1, 2, -1, -2, 3, F(1, 2)])
    B = rng.choice([F(1), F(2), F(1, 2), F(3)])
    c = rng.choice([F(0), F(1, 3), F(-1, 6)])
    ask = rng.choice(["最大値", "最小値"])
    mx, mn = beta + abs(A), beta - abs(A)
    ans = mx if ask == "最大値" else mn
    other = mn if ask == "最大値" else mx
    wrong_signed = (beta + A) if ask == "最大値" else (beta - A)
    expr = rf"y={coef_tex(A)}\{fn}\left({inner_tex(B, c)}\right){const_tex(beta)}"
    wrongs = [(tex_fr(wrong_signed) if wrong_signed != ans else None, "振幅は $|A|$。$A<0$ のとき、最大値は $\\beta+|A|=\\beta-A$。"),
              (tex_fr(abs(A)) if abs(A) != ans else None, "$y$ 軸方向の平行移動 $\\beta$ を足し忘れていないか。"),
              (tex_fr(other), f"それは{'最小値' if ask == '最大値' else '最大値'}。"),
              (tex_fr(ans + 1), "$-1\\le\\sin\\theta\\le1$ から範囲を考えよう。"), (tex_fr(ans - 1), "$-1\\le\\sin\\theta\\le1$ から範囲を考えよう。")]
    return Problem(f"三角関数の{ask}", "基本", rf"関数 ${expr}$ の{ask}を求めよ。",
                   assemble(tex_fr(ans), wrongs, value=float(ans)),
                   hints=[r"$-1\le\sin\theta\le1$ なので、$A\sin\theta+\beta$ は $\beta-|A|$ から $\beta+|A|$ の値をとる。",
                          r"$B$ や平行移動は最大値・最小値に関係しない。"],
                   solution=[rf"$-1\le\{fn}(\cdots)\le1$ より、$y$ は ${tex_fr(beta)}-{tex_fr(abs(A))}$ から ${tex_fr(beta)}+{tex_fr(abs(A))}$ まで",
                             rf"{ask}は ${tex_fr(ans)}$"], meta=dict(A=str(A), beta=str(beta), ask=ask))


# ============================================================
# 標準:平行移動の量(sin(Bx − c) の形)
# ============================================================
def g_shift(rng):
    fn = rng.choice(["sin", "cos"])
    B = rng.choice([F(2), F(3), F(1, 2), F(4)])
    c = rng.choice([F(1, 3), F(1, 2), F(2, 3), F(1, 4), F(1, 6), F(-1, 3), F(-1, 2), F(-1, 4)])
    shift = c / B
    d = "右" if shift > 0 else "左"
    expr = rf"y=\{fn}\left({bx_tex(B)}{' - ' if c > 0 else ' + '}{pi_tex(abs(c))}\right)"
    opp = "左" if d == "右" else "右"
    ans = rf"x\text{{ 軸方向に }}{pi_tex(shift)}"
    wrongs = [(rf"x\text{{ 軸方向に }}{pi_tex(c)}", f"${bx_tex(B)}-c$ のままではなく、$x$ の係数 ${tex_fr(B)}$ でくくって ${tex_fr(B)}(x-\\alpha)$ の形にする。"),
              (rf"x\text{{ 軸方向に }}{pi_tex(c * B)}", f"$x$ の係数でくくると $\\alpha=\\dfrac{{c}}{{B}}$。$B$ をかけていないか。"),
              (rf"x\text{{ 軸方向に }}{pi_tex(-shift)}", "符号を確かめよう。$\\sin(x-\\alpha)$ は $x$ 軸の正の向き($+\\alpha$)に平行移動。"),
              (rf"x\text{{ 軸方向に }}{pi_tex(-c)}", "くくり方と符号の両方を確かめよう。")]
    sol = [rf"$${expr.replace('y=', 'y=')}=\{fn} {tex_fr(B)}\left(x{' - ' if shift > 0 else ' + '}{pi_tex(abs(shift))}\right)$$",
           rf"よって $y=\{fn} {tex_fr(B)}x$ のグラフを $x$ 軸方向に ${pi_tex(shift)}$({d}へ ${pi_tex(abs(shift))}$)平行移動したもの"]
    return Problem("平行移動の量", "標準",
                   rf"関数 ${expr}$ のグラフは、$y=\{fn} {bx_tex(B)}$ のグラフをどれだけ平行移動したものか。",
                   assemble(ans, wrongs, value=float(shift)),
                   hints=[r"$x$ の係数でくくって $\sin B(x-\alpha)$ の形にする。", r"$y=f(x-\alpha)$ は $y=f(x)$ を $x$ 軸方向に $\alpha$ 平行移動したもの。"],
                   solution=sol, meta=dict(B=str(B), c=str(c)))


# ============================================================
# 標準:グラフから式を読む(図あり)
# ============================================================
def _wave_tex(fn, A, B, al, beta):
    w = Wave(fn, F(A), F(B), F(al), F(beta))
    return w.latex()


def g_from_graph(rng):
    fn = rng.choice(["sin", "cos"])
    A = rng.choice([1, 2, 3, -2, -1])
    B = rng.choice([F(1), F(2), F(1, 2)])
    al = rng.choice([F(0), F(1, 6), F(1, 4), F(1, 3), F(-1, 6), F(-1, 4), F(-1, 3)])
    beta = rng.choice([0, 0, 1, -1])
    spec = dict(kind="trig", func=fn, A=A, B=B, alpha=al, beta=beta, xr=(-1, 3 if B != F(1, 2) else 4))
    cands = [
        ((fn, -A, B, al, beta), "振幅の符号を確かめよう。$x=\\alpha$ でグラフが上がっていくか下がっていくかを見る。"),
        ((fn, A, 1 / B if B != 1 else F(2), al, beta), "周期を確かめよう。周期 $\\frac{2\\pi}{B}$ から $B$ を読む。"),
        ((fn, A, B, -al if al != 0 else F(1, 2), beta), "平行移動の向きを確かめよう。$\\sin B(x-\\alpha)$ は右へ $\\alpha$ ずれる。"),
        ((fn, A, B, al, beta + (1 if beta <= 0 else -1)), "中心線(最大値と最小値の真ん中)の高さ $\\beta$ を確かめよう。"),
        (("cos" if fn == "sin" else "sin", A, B, al, beta), "$x=\\alpha$ で中心線から始まるのが $\\sin$、最大値から始まるのが $\\cos$。"),
        ((fn, 2 * A if abs(A) == 1 else A // abs(A), B, al, beta), "振幅(中心線から山までの高さ)を確かめよう。"),
    ]
    rng.shuffle(cands)
    wrongs = []
    for (f2, A2, B2, al2, be2), why in cands:
        s2 = dict(kind="trig", func=f2, A=A2, B=B2, alpha=al2, beta=be2, xr=spec["xr"])
        if same_graph(spec, s2):
            continue
        wrongs.append((_wave_tex(f2, A2, B2, al2, be2), why))
    ans = _wave_tex(fn, A, B, al, beta)
    w = Wave(fn, F(A), F(B), F(al), F(beta))
    return Problem("グラフから式を読む", "標準", "次のグラフを表す式を、選択肢から選べ。",
                   assemble(ans, wrongs, value=None),
                   hints=[r"最大値と最小値から、振幅 $|A|$ と中心線の高さ $\beta$ を読む。",
                          r"山から次の山までの長さが周期 $\frac{2\pi}{B}$。",
                          r"中心線を上向きに横切る点($\sin$)や山の位置($\cos$)から、平行移動 $\alpha$ を読む。"],
                   solution=[rf"最大値 ${tex_fr(w.y_max)}$、最小値 ${tex_fr(w.y_min)}$ より、振幅 ${tex_fr(abs(F(A)))}$、中心線 $y={beta}$",
                             rf"周期は ${pi_tex(w.period)}$ なので $B={tex_fr(B)}$",
                             rf"よって ${ans}$"],
                   figure=spec, meta=dict(spec={k: str(v) for k, v in spec.items()}))


# ============================================================
# 基本:三角方程式(0 ≦ x < 2π)
# ============================================================
SIN_K = {"0": 0, r"\frac{1}{2}": 30, r"\frac{\sqrt{2}}{2}": 45, r"\frac{\sqrt{3}}{2}": 60, "1": 90,
         r"-\frac{1}{2}": -30, r"-\frac{\sqrt{2}}{2}": -45, r"-\frac{\sqrt{3}}{2}": -60, "-1": -90}
TAN_K = {"0": 0, "1": 45, r"\sqrt{3}": 60, r"\frac{1}{\sqrt{3}}": 30, "-1": -45, r"-\sqrt{3}": -60, r"-\frac{1}{\sqrt{3}}": -30}


def _norm(deg):
    return deg % 360


def _sols(fn, p):
    """主値 p(度)から 0 ≦ x < 360 の解(度)"""
    if fn == "sin":
        s = {_norm(p), _norm(180 - p)}
    elif fn == "cos":
        s = {_norm(p), _norm(-p)}
    else:
        s = {_norm(p), _norm(p + 180)}
    return sorted(s)


def _sol_tex(ds):
    return "x=" + r",\ ".join(pi_tex(F(d, 180)) for d in ds)


def g_equation(rng):
    fn = rng.choice(["sin", "cos", "tan"])
    if fn == "tan":
        kt, p = rng.choice(list(TAN_K.items()))
    else:
        kt, p = rng.choice(list(SIN_K.items()))
        if fn == "cos":
            p = 90 - p          # cos x = k の主値(0〜180°)
    ans = _sols(fn, p)
    other = {"sin": "cos", "cos": "sin", "tan": "sin"}[fn]
    wrongs = [(_sol_tex([_norm(p)]) if len(ans) > 1 else None, "解は 1 つとは限らない。$0\\le x<2\\pi$ の範囲で、単位円の点をすべて探そう。"),
              (_sol_tex(_sols(other, p)) if _sols(other, p) != ans else None,
               "単位円で、$\\sin$ は $y$ 座標、$\\cos$ は $x$ 座標が等しい点を探す。もう 1 つの解の求め方を確かめよう。"),
              (_sol_tex(_sols(fn, -p if fn != "cos" else 180 - p)), "右辺の符号を確かめよう。"),
              (_sol_tex(sorted({_norm(p + 180), _norm(p)})) if fn != "tan" else _sol_tex(sorted({_norm(p + 90), _norm(p + 270)})),
               "単位円で対称な点を確かめよう。")]
    fill = [(_sol_tex(sorted({_norm(p + d), _norm(180 - p + d)})), "単位円をかいて確かめよう。") for d in (30, 60, 90)]
    return Problem("三角方程式", "基本", rf"$0\le x<2\pi$ のとき、方程式 $\{fn} x={kt}$ を解け。",
                   assemble(_sol_tex(ans), wrongs, fill),
                   hints=[r"単位円で、$\sin x$ は $y$ 座標、$\cos x$ は $x$ 座標。$\tan x$ は原点と点を結ぶ直線の傾き。",
                          r"$\sin x=k$ の解は $\theta$ と $\pi-\theta$、$\cos x=k$ は $\theta$ と $2\pi-\theta$、$\tan x=k$ は $\theta$ と $\theta+\pi$。"],
                   solution=[rf"単位円で条件をみたす点を探すと、${_sol_tex(ans)}$"], meta=dict(fn=fn, k=kt))


# ============================================================
# 標準:三角不等式(0 ≦ x < 2π)
# ============================================================
def g_inequality(rng):
    fn = rng.choice(["sin", "cos"])
    kt, p = rng.choice([(r"\frac{1}{2}", 30), (r"\frac{\sqrt{2}}{2}", 45), (r"\frac{\sqrt{3}}{2}", 60), (r"-\frac{1}{2}", -30),
                        (r"-\frac{\sqrt{2}}{2}", -45), (r"-\frac{\sqrt{3}}{2}", -60)])
    ge = rng.random() < 0.5
    op = r"\ge" if ge else r"\le"
    P = lambda d: pi_tex(F(d, 180))  # noqa: E731
    if fn == "sin":
        a, b = _norm(p), _norm(180 - p)           # sin x = k の 2 解
        lo, hi = min(a, b), max(a, b)
        inside = rf"{P(lo)}\le x\le {P(hi)}"
        outside = rf"0\le x\le {P(lo)},\ {P(hi)}\le x<2\pi"
        ans = inside if (ge == (p > 0)) else outside
        alt = outside if ans == inside else inside
    else:
        c = 90 - p                                  # cos x = k の主値
        lo, hi = c, 360 - c
        inside = rf"{P(lo)}\le x\le {P(hi)}"
        outside = rf"0\le x\le {P(lo)},\ {P(hi)}\le x<2\pi"
        ans = outside if ge else inside
        alt = inside if ge else outside
    wrongs = [(alt, "不等号の向きを確かめよう。グラフ(または単位円)で、条件をみたすのはどちらの部分か。"),
              (rf"{P(_norm(p))}\le x\le {P(_norm(p) + 180)}" if fn == "sin" else rf"{P(90 - p)}\le x\le {P(270 - p)}",
               "端の角を確かめよう。もう 1 つの解は $\\sin$ なら $\\pi-\\theta$、$\\cos$ なら $2\\pi-\\theta$。"),
              (rf"{P(_norm(-p))}\le x\le {P(_norm(180 + p))}" if fn == "sin" else rf"{P(90 + p)}\le x\le {P(270 - p)}",
               "右辺の値の符号を確かめよう。"),
              (rf"0\le x\le {P(_norm(p) if _norm(p) else 30)}", "解は区間になる。境目の角を 2 つとも求めよう。")]
    return Problem("三角不等式", "標準", rf"$0\le x<2\pi$ のとき、不等式 $\{fn} x {op} {kt}$ を解け。",
                   assemble(ans, wrongs),
                   hints=[r"まず等号の方程式を解いて、境目の角を求める。",
                          rf"$y=\{fn} x$ のグラフと直線 $y={kt}$ をかいて、グラフが直線より{'上' if ge else '下'}にある $x$ の範囲を読む。"],
                   solution=[rf"$\{fn} x={kt}$ を解くと、境目の角は ${P(lo)}$ と ${P(hi)}$",
                             rf"グラフより ${ans}$"], meta=dict(fn=fn, p=p, ge=ge))


# ============================================================
# 基本:角の変換(位相のずれ)
# ============================================================
IDENT = [
    (r"\sin\left(x+\frac{\pi}{2}\right)", r"\cos x"), (r"\cos\left(x+\frac{\pi}{2}\right)", r"-\sin x"),
    (r"\sin\left(x-\frac{\pi}{2}\right)", r"-\cos x"), (r"\cos\left(x-\frac{\pi}{2}\right)", r"\sin x"),
    (r"\sin(x+\pi)", r"-\sin x"), (r"\cos(x+\pi)", r"-\cos x"), (r"\sin(\pi-x)", r"\sin x"), (r"\cos(\pi-x)", r"-\cos x"),
    (r"\sin\left(\frac{\pi}{2}-x\right)", r"\cos x"), (r"\cos\left(\frac{\pi}{2}-x\right)", r"\sin x"),
    (r"\sin(-x)", r"-\sin x"), (r"\cos(-x)", r"\cos x"),
]


def g_phase(rng):
    lhs, rhs = rng.choice(IDENT)
    whys = {r"\sin x": "$\\sin$ と $\\cos$ のどちらになるか確かめよう($\\frac{\\pi}{2}$ ずれると入れかわる)。",
            r"-\sin x": "符号を確かめよう。$x$ に小さい角(たとえば $0$)を代入して確かめるとよい。",
            r"\cos x": "$\\sin$ と $\\cos$ のどちらになるか確かめよう。",
            r"-\cos x": "符号を確かめよう。$x=0$ を代入して両辺を比べるとよい。"}
    wrongs = [(t, whys[t]) for t in (r"\sin x", r"-\sin x", r"\cos x", r"-\cos x") if t != rhs]
    return Problem("角の変換(位相のずれ)", "基本", rf"${lhs}$ を簡単にせよ。", assemble(rhs, wrongs),
                   hints=[r"単位円で、角 $x$ の点と角 $x+\frac{\pi}{2}$ などの点の位置関係を考える。",
                          r"$x=0$ や $x=\frac{\pi}{6}$ を代入して、両辺の値が等しいか確かめられる。"],
                   solution=[rf"加法定理(または単位円)より $${lhs}={rhs}$$"], meta=dict(lhs=lhs))


REGISTRY = [
    ProblemType("period", "周期", "基本", g_period),
    ProblemType("maxmin", "最大値・最小値", "基本", g_maxmin),
    ProblemType("equation", "三角方程式", "基本", g_equation),
    ProblemType("phase", "角の変換(位相のずれ)", "基本", g_phase),
    ProblemType("shift", "平行移動の量(sin(Bx − c) の形)", "標準", g_shift),
    ProblemType("graph", "グラフから式を読む(図あり)", "標準", g_from_graph),
    ProblemType("ineq", "三角不等式", "標準", g_inequality),
]

TITLE = "三角関数のグラフ"


def tab():
    render("graph", REGISTRY, TITLE)
