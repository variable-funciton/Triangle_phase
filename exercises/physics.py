"""演習:三角関数の応用(斜方投射、バネの単振動、波、モンキーハンティング、リサージュ図形)"""
import math
from fractions import Fraction as F

from exercises.core import Problem, ProblemType, Retry, render, tex_fr
from exercises.helpers import Q236, assemble, pi_tex, sin_deg, cos_deg

G = 9.8


def num(x, d=2):
    s = f"{x:.{d}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def unit(t, u):
    return rf"{t}\ \text{{{u}}}"


# ============================================================
# 基本:斜方投射の飛距離
# ============================================================
def g_range(rng):
    v0 = rng.choice([7, 14, 21, 28])
    K = F(v0 * v0 * 10, 98)                 # v0² / g(9.8)
    th = rng.choice([15, 30, 45, 60, 75])
    L = sin_deg(2 * th) * K
    wrongs = [(unit((sin_deg(th) * K).latex(), "m"), "飛距離は $\\dfrac{v_0^2\\sin 2\\theta}{g}$。$\\sin\\theta$ ではなく $\\sin 2\\theta$。"),
              (unit((sin_deg(2 * th) * K * F(1, 2)).latex(), "m"), "$\\sin 2\\theta=2\\sin\\theta\\cos\\theta$。2 を忘れていないか。"),
              (unit((sin_deg(2 * th) * K * 2).latex(), "m"), "滞空時間 $\\frac{2v_0\\sin\\theta}{g}$ と水平方向の速さ $v_0\\cos\\theta$ の積を確かめよう。"),
              (unit((cos_deg(2 * th) * K).latex(), "m") if float(cos_deg(2 * th)) > 1e-9 else None, "$\\sin 2\\theta$ と $\\cos 2\\theta$ を取り違えていないか。"),
              (unit((cos_deg(th) * K).latex(), "m"), "飛距離の式を確かめよう。")]
    return Problem("斜方投射の飛距離", "基本",
                   rf"水平な地面から、初速度 ${v0}$ m/s、水平との角 ${th}^\circ$ でボールを投げた。飛距離を求めよ。"
                   r"ただし重力加速度を $g=9.8$ m/s²、空気抵抗はないものとする。",
                   assemble(unit(L.latex(), "m"), wrongs, value=float(L)),
                   hints=[r"飛距離 $L=\dfrac{v_0^2\sin 2\theta}{g}$($=$ 水平方向の速さ $v_0\cos\theta$ × 滞空時間 $\dfrac{2v_0\sin\theta}{g}$)。",
                          rf"$\dfrac{{v_0^2}}{{g}}=\dfrac{{{v0 * v0}}}{{9.8}}={tex_fr(K)}$"],
                   solution=[rf"$$L=\frac{{v_0^2\sin 2\theta}}{{g}}=\frac{{{v0}^2\times\sin {2 * th}^\circ}}{{9.8}}={tex_fr(K)}\times{sin_deg(2 * th).latex()}={L.latex()}\ \text{{m}}$$"],
                   meta=dict(v0=v0, th=th))


# ============================================================
# 標準:最高点の高さ
# ============================================================
def g_height(rng):
    v0 = rng.choice([7, 14, 21, 28])
    K = F(v0 * v0 * 10, 98)
    th = rng.choice([30, 45, 60, 90])
    s2 = (sin_deg(th) * sin_deg(th)).as_rational()
    H = K * s2 / 2
    wrongs = [(unit(tex_fr(K * s2), "m"), "最高点の高さは $\\dfrac{(v_0\\sin\\theta)^2}{2g}$。2 で割り忘れていないか。"),
              (unit((sin_deg(th) * K * F(1, 2)).latex(), "m"), "$\\sin\\theta$ を 2 乗し忘れていないか。"),
              (unit(tex_fr(K * (1 - s2) / 2), "m") if s2 != F(1, 2) else unit(tex_fr(K), "m"), "鉛直方向の初速度は $v_0\\sin\\theta$。$\\cos\\theta$ を使っていないか。"),
              (unit(tex_fr(K / 2), "m"), "鉛直方向の初速度 $v_0\\sin\\theta$ を使う。")]
    return Problem("斜方投射の最高点の高さ", "標準",
                   rf"初速度 ${v0}$ m/s、水平との角 ${th}^\circ$ で投げたボールの最高点の高さ(投げた点から)を求めよ。$g=9.8$ m/s² とする。",
                   assemble(unit(tex_fr(H), "m"), wrongs, value=float(H)),
                   hints=[r"鉛直方向は初速度 $v_0\sin\theta$ の鉛直投げ上げ。最高点では鉛直方向の速さが 0。",
                          r"$H=\dfrac{(v_0\sin\theta)^2}{2g}$"],
                   solution=[rf"$$H=\frac{{(v_0\sin\theta)^2}}{{2g}}=\frac{{{v0}^2\times\left({sin_deg(th).latex()}\right)^2}}{{2\times 9.8}}={tex_fr(H)}\ \text{{m}}$$"],
                   meta=dict(v0=v0, th=th))


# ============================================================
# 基本:滞空時間
# ============================================================
def g_time(rng):
    v0 = rng.choice([F(49, 10), F(98, 10), F(147, 10), F(196, 10)])
    K = 2 * v0 / F(98, 10)
    th = rng.choice([30, 45, 60])
    T = sin_deg(th) * K
    wrongs = [(unit((sin_deg(th) * K / 2).latex(), "s"), "滞空時間は最高点に達するまでの時間の 2 倍。"),
              (unit((cos_deg(th) * K).latex(), "s") if th != 45 else None, "鉛直方向の初速度は $v_0\\sin\\theta$。$\\cos\\theta$ ではない。"),
              (unit(tex_fr(K), "s"), "鉛直方向の初速度 $v_0\\sin\\theta$ を使う。"),
              (unit((sin_deg(th) * K * 2).latex(), "s"), "$y=v_0\\sin\\theta\\cdot t-\\frac12gt^2=0$ を解こう。")]
    return Problem("斜方投射の滞空時間", "基本",
                   rf"初速度 ${num(float(v0), 1)}$ m/s、水平との角 ${th}^\circ$ で水平な地面から投げたボールが、地面に落ちるまでの時間を求めよ。$g=9.8$ m/s² とする。",
                   assemble(unit(T.latex(), "s"), wrongs, value=float(T)),
                   hints=[r"鉛直方向の位置 $y=v_0\sin\theta\cdot t-\frac12gt^2$ が再び 0 になる時刻。", r"$T=\dfrac{2v_0\sin\theta}{g}$"],
                   solution=[rf"$$T=\frac{{2v_0\sin\theta}}{{g}}=\frac{{2\times{num(float(v0), 1)}\times{sin_deg(th).latex()}}}{{9.8}}={T.latex()}\ \text{{s}}$$"],
                   meta=dict(v0=float(v0), th=th))


# ============================================================
# 基本:バネの単振動の周期
# ============================================================
SHM = [(F(1, 2), 2), (F(1, 2), 8), (1, 4), (1, 16), (2, 8), (2, 50), (F(1, 10), 10), (F(2, 5), 10), (F(9, 10), 10),
       (F(1, 5), 20), (4, 16), (F(1, 4), 25)]


def g_shm(rng):
    m, k = rng.choice(SHM)
    r = F(m) / k
    rt = F(math.isqrt(r.numerator), math.isqrt(r.denominator))
    if rt * rt != r:
        raise Retry
    T = 2 * rt
    inv = F(k) / F(m)
    ir = F(math.isqrt(inv.numerator), math.isqrt(inv.denominator))
    wrongs = [(unit(pi_tex(2 * ir), "s") if ir * ir == inv else None, "$T=2\\pi\\sqrt{\\dfrac{m}{k}}$。$m$ と $k$ を逆にしていないか。"),
              (unit(pi_tex(2 * r), "s"), "平方根をとり忘れていないか。"),
              (unit(pi_tex(rt), "s"), "$T=2\\pi\\sqrt{m/k}$。$2$ を忘れていないか($\\omega=\\sqrt{k/m}$、$T=\\frac{2\\pi}{\\omega}$)。"),
              (unit(tex_fr(rt), "s"), "それは $\\sqrt{m/k}$。周期は $2\\pi$ をかける。"),
              (unit(pi_tex(4 * rt), "s"), "周期の式を確かめよう。")]
    mt = tex_fr(F(m)) if F(m).denominator != 10 and F(m).denominator != 5 else num(float(m), 1)
    return Problem("バネの単振動の周期", "基本",
                   rf"ばね定数 ${k}$ N/m のばねに質量 ${mt}$ kg のおもりをつけて単振動させる。周期を求めよ。",
                   assemble(unit(pi_tex(T), "s"), wrongs, value=float(T) * math.pi),
                   hints=[r"角振動数 $\omega=\sqrt{\dfrac{k}{m}}$、周期 $T=\dfrac{2\pi}{\omega}=2\pi\sqrt{\dfrac{m}{k}}$。"],
                   solution=[rf"$$T=2\pi\sqrt{{\frac{{m}}{{k}}}}=2\pi\sqrt{{\frac{{{mt}}}{{{k}}}}}=2\pi\times{tex_fr(rt)}={pi_tex(T)}\ \text{{s}}$$"],
                   meta=dict(m=float(m), k=k))


# ============================================================
# 基本:波の式(速さ・振動数)
# ============================================================
def g_wave(rng):
    A = rng.choice([F(1, 10), F(1, 5), F(1, 2), 2])
    T = rng.choice([F(1, 5), F(1, 2), F(2), F(4)])
    lam = rng.choice([F(2, 5), F(1), F(2), F(3), F(6)])
    ask = rng.choice(["速さ", "振動数"])
    tx = lambda q: num(float(q), 2)  # noqa: E731
    expr = rf"y={tx(A)}\sin 2\pi\left(\frac{{t}}{{{tx(T)}}}-\frac{{x}}{{{tx(lam)}}}\right)"
    if ask == "速さ":
        ans = lam / T
        wrongs = [(unit(tx(T / lam), "m/s"), "波の速さは $v=\\dfrac{\\lambda}{T}$。逆にしていないか。"),
                  (unit(tx(lam * T), "m/s"), "$v=f\\lambda=\\dfrac{\\lambda}{T}$。$T$ をかけていないか。"),
                  (unit(tx(A / T), "m/s"), "振幅 $A$ は速さに関係しない。"), (unit(tx(lam), "m/s"), "1 周期 $T$ で 1 波長 $\\lambda$ 進む。")]
        u = "m/s"
        sol = [rf"式から周期 $T={tx(T)}$ s、波長 $\lambda={tx(lam)}$ m", rf"$$v=\frac{{\lambda}}{{T}}={tx(ans)}\ \text{{m/s}}$$"]
    else:
        ans = 1 / T
        wrongs = [(unit(tx(T), "Hz"), "それは周期 $T$。振動数は $f=\\dfrac{1}{T}$。"),
                  (unit(tx(1 / lam), "Hz"), "振動数は時間 $t$ の係数から読む($\\frac{t}{T}$ の $T$)。"),
                  (unit(tx(2 / T), "Hz"), "$2\\pi$ はくくり出してある。$f=\\dfrac1T$。"), (unit(tx(lam / T), "Hz"), "それは波の速さ。")]
        u = "Hz"
        sol = [rf"式から周期 $T={tx(T)}$ s", rf"$$f=\frac{{1}}{{T}}={tx(ans)}\ \text{{Hz}}$$"]
    return Problem(f"波の{ask}", "基本",
                   rf"時刻 $t$ [s]、位置 $x$ [m] での変位が ${expr}$ [m] で表される波の{ask}を求めよ。",
                   assemble(unit(tx(ans), u), wrongs, value=float(ans)),
                   hints=[r"$y=A\sin 2\pi\left(\dfrac{t}{T}-\dfrac{x}{\lambda}\right)$:$T$ が周期、$\lambda$ が波長。",
                          r"振動数 $f=\dfrac1T$、波の速さ $v=f\lambda=\dfrac{\lambda}{T}$。"],
                   solution=sol, meta=dict(T=float(T), lam=float(lam), ask=ask))


# ============================================================
# 標準:モンキーハンティングで当たるための最小の初速度
# ============================================================
def g_monkey(rng):
    a = rng.choice([10, 15, 20, 30, 40])
    b = rng.choice([5, 10, 15, 20])
    v = math.sqrt(G * (a * a + b * b) / (2 * b))
    ans = unit(num(v, 1), "m/s")
    wrongs = [(unit(num(math.sqrt(G * a * a / (2 * b)), 1), "m/s"), "O から B までの距離は $\\sqrt{a^2+b^2}$。$a$ だけを使っていないか。"),
              (unit(num(math.sqrt(G * (a * a + b * b) / b), 1), "m/s"), "条件は $b-\\frac12g{t^*}^2>0$。$\\frac12$ を忘れていないか。"),
              (unit(num(math.sqrt(2 * G * b), 1), "m/s"), "それは高さ $b$ から落ちたときの速さ。出会う時刻 $t^*=\\frac{\\sqrt{a^2+b^2}}{v_0}$ を使う。"),
              (unit(num(G * (a * a + b * b) / (2 * b), 1), "m/s"), "最後に平方根をとる。")]
    return Problem("モンキーハンティングの条件", "標準",
                   rf"原点 O から、点 $(a,\ b)=({a},\ {b})$ [m] にある物体 B を狙って弾を撃つ。撃つと同時に B が自由落下するとき、"
                   r"B が地面($y=0$)に落ちる前に当たるための初速度 $v_0$ の最小値(この値より大きければ当たる)を、小数第 1 位まで求めよ。$g=9.8$ m/s² とする。",
                   assemble(ans, wrongs, value=v),
                   hints=[r"弾が $x=a$ に着く時刻は $t^*=\dfrac{\sqrt{a^2+b^2}}{v_0}$。そのとき両方とも高さ $b-\frac12g{t^*}^2$ にある。",
                          r"当たる条件は $b-\frac12g{t^*}^2>0$。"],
                   solution=[rf"$$b-\frac{{g(a^2+b^2)}}{{2v_0^2}}>0\iff v_0>\sqrt{{\frac{{g(a^2+b^2)}}{{2b}}}}=\sqrt{{\frac{{9.8\times{a * a + b * b}}}{{{2 * b}}}}}\approx{num(v, 1)}$$"],
                   meta=dict(a=a, b=b))


# ============================================================
# 基本:リサージュ図形の形
# ============================================================
LISSA = [
    ((1, 1, "0"), r"\text{右上がりの線分}"), ((1, 1, r"\pi"), r"\text{右下がりの線分}"),
    ((1, 1, r"\frac{\pi}{2}"), r"\text{円}"), ((1, 1, r"\frac{\pi}{4}"), r"\text{傾いた楕円}"),
]
SHAPES = [r"\text{右上がりの線分}", r"\text{右下がりの線分}", r"\text{円}", r"\text{傾いた楕円}", r"\text{放物線の一部}"]


def g_lissajous(rng):
    (a, b, d), ans = rng.choice(LISSA)
    xin = "t" if d == "0" else rf"t+{d}"
    wrongs = [(s, "$t$ にいくつか値を代入して点をとるか、$x$ と $y$ の関係式を作ってみよう"
                  "($\\delta=\\frac{\\pi}{2}$ なら $x=\\cos t$ となり $x^2+y^2=1$)。") for s in SHAPES if s != ans]
    return Problem("リサージュ図形の形", "基本",
                   rf"媒介変数表示 $x=\sin({xin}),\ y=\sin t$ が表す図形はどれか。",
                   assemble(ans, wrongs),
                   hints=[r"同じ振動数の 2 つの振動の組み合わせ。位相差 $\delta$ で形が決まる。",
                          r"$\sin\left(t+\frac{\pi}{2}\right)=\cos t$、$\sin(t+\pi)=-\sin t$。"],
                   solution=[{"0": r"$x=y$ なので、$-1\le x\le1$ の右上がりの線分。",
                              r"\pi": r"$x=-\sin t=-y$ なので、右下がりの線分。",
                              r"\frac{\pi}{2}": r"$x=\cos t,\ y=\sin t$ なので $x^2+y^2=1$(円)。",
                              r"\frac{\pi}{4}": r"位相差が $0$ と $\frac{\pi}{2}$ の間なので、右上がりに傾いた楕円。"}[d]],
                   meta=dict(d=d))


REGISTRY = [
    ProblemType("range", "斜方投射の飛距離", "基本", g_range),
    ProblemType("time", "斜方投射の滞空時間", "基本", g_time),
    ProblemType("shm", "バネの単振動の周期", "基本", g_shm),
    ProblemType("wave", "波の速さ・振動数", "基本", g_wave),
    ProblemType("lissa", "リサージュ図形の形", "基本", g_lissajous),
    ProblemType("height", "斜方投射の最高点の高さ", "標準", g_height),
    ProblemType("monkey", "モンキーハンティングの条件", "標準", g_monkey),
]

TITLE = "三角関数の応用(物理)"


def tab():
    render("physics", REGISTRY, TITLE)
