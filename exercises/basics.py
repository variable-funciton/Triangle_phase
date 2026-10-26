"""演習:三角比・三角関数の基礎(弧度法、有名角の値、扇形、相互関係、正弦定理・余弦定理、加法定理、2倍角)

誤答は、学生がよくする間違いから作る(why に、その誤答を選んだときの指摘を書く)。
"""
from fractions import Fraction as F
from math import gcd

from exercises.core import Problem, ProblemType, Retry, render, tex_fr, tex_frac_root, tex_root
from exercises.helpers import NICE_DEG, assemble, cos_deg, neg_tex, pi_tex, sin_deg, trig_tex

FN_TEX = {"sin": r"\sin", "cos": r"\cos", "tan": r"\tan"}
VALUE_POOL = ["0", r"\frac{1}{2}", r"-\frac{1}{2}", r"\frac{\sqrt{2}}{2}", r"-\frac{\sqrt{2}}{2}", r"\frac{\sqrt{3}}{2}",
              r"-\frac{\sqrt{3}}{2}", "1", "-1", r"\sqrt{3}", r"-\sqrt{3}", r"\frac{\sqrt{3}}{3}", r"-\frac{\sqrt{3}}{3}"]


def _pool(rng, why):
    p = list(VALUE_POOL)
    rng.shuffle(p)
    return [(t, why) for t in p]


# ============================================================
# 基本:度数法 → 弧度法
# ============================================================
def g_deg2rad(rng):
    deg = rng.choice([d for d in range(15, 361, 15)] + [-30, -45, -60, -90, -120, -135, -150])
    q = F(deg, 180)
    wrongs = [(pi_tex(F(180, deg)) if 180 % abs(deg) == 0 else None, "$\\frac{\\pi}{180}$ をかける。$\\frac{180}{\\theta}$ と逆にしていないか。"),
              (pi_tex(F(deg, 360)), "$180^\\circ=\\pi$ [rad]。$360^\\circ$ を $\\pi$ としていないか($360^\\circ=2\\pi$)。"),
              (pi_tex(F(deg, 90)), "$180^\\circ=\\pi$。$90^\\circ$ を $\\pi$ としていないか。"),
              (rf"{deg}\pi", "度の数にそのまま $\\pi$ をつけるのではなく、$\\frac{\\pi}{180}$ をかける。")]
    fill = [(pi_tex(q + F(k, 6)), "$\\frac{\\pi}{180}$ をかけて約分しよう。") for k in (1, -1, 2, 3)]
    return Problem(
        "度数法を弧度法に", "基本", rf"${deg}^\circ$ を弧度法で表せ。",
        assemble(pi_tex(q), wrongs, fill, value=float(q)),
        hints=[r"$180^\circ=\pi$ [rad]。", r"$\theta^\circ=\theta\times\dfrac{\pi}{180}$ [rad]。"],
        solution=[rf"$${deg}^\circ={deg}\times\frac{{\pi}}{{180}}={pi_tex(q)}$$"], meta=dict(deg=deg))


# ============================================================
# 基本:弧度法 → 度数法
# ============================================================
def g_rad2deg(rng):
    q = rng.choice([F(k, 12) for k in range(1, 25)] + [F(-1, 6), F(-1, 4), F(-1, 3), F(-2, 3), F(-3, 4), F(-5, 6)])
    deg = q * 180
    if deg.denominator != 1:
        raise Retry
    deg = int(deg)
    inv = F(180) / q
    wrongs = [(rf"{int(q * 360)}^\circ", "$\\pi$ [rad] $=180^\\circ$。$\\pi$ を $360^\\circ$ としていないか。"),
              (rf"{int(q * 90)}^\circ" if (q * 90).denominator == 1 else None, "$\\pi$ [rad] $=180^\\circ$。$\\pi$ を $90^\\circ$ としていないか。"),
              (rf"{int(inv)}^\circ" if inv.denominator == 1 else None, "$\\frac{180}{\\pi}$ をかける。逆数にしていないか。")]
    fill = [(rf"{deg + k}^\circ", "$\\pi=180^\\circ$ を代入して計算しよう。") for k in (15, -15, 30, 45)]
    return Problem(
        "弧度法を度数法に", "基本", rf"${pi_tex(q)}$ [rad] を度数法で表せ。",
        assemble(rf"{deg}^\circ", wrongs, fill, value=deg),
        hints=[r"$\pi$ [rad] $=180^\circ$ なので、$\pi$ に $180^\circ$ を代入すればよい。"],
        solution=[rf"$${pi_tex(q)}={tex_fr(q)}\times 180^\circ={deg}^\circ$$"], meta=dict(q=str(q)))


# ============================================================
# 基本:有名角の三角関数の値(0°〜360°) / 標準:負の角・360°をこえる角
# ============================================================
def _value_problem(rng, level):
    fn = rng.choice(["sin", "cos", "tan"])
    base = rng.choice(NICE_DEG[1:])
    if fn == "tan" and base in (90, 270):
        raise Retry
    if level == "基本":
        deg = base
    else:
        deg = base + 360 * rng.choice([-2, -1, 1, 2])
        if not (-720 < deg < 1080) or 0 <= deg < 360:
            raise Retry
    ans = trig_tex(fn, base)
    other = {"sin": "cos", "cos": "sin", "tan": None}[fn]
    q = F(deg, 180)
    wrongs = [(neg_tex(ans), "符号を確かめよう。角がどの象限にあるか(単位円の点の x 座標・y 座標の符号)を考える。"),
              (trig_tex(other, base) if other else None, "$\\sin$ は単位円の点の $y$ 座標、$\\cos$ は $x$ 座標。取り違えていないか。")]
    if fn == "tan" and ans not in ("0",):
        inv = {r"\sqrt{3}": r"\frac{\sqrt{3}}{3}", r"\frac{\sqrt{3}}{3}": r"\sqrt{3}", r"-\sqrt{3}": r"-\frac{\sqrt{3}}{3}",
               r"-\frac{\sqrt{3}}{3}": r"-\sqrt{3}"}.get(ans)
        wrongs.append((inv, "$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$。分母と分子が逆になっていないか。"))
    if other:
        wrongs.append((neg_tex(trig_tex(other, base)), "$\\sin$ と $\\cos$、符号の両方を確かめよう。"))
    unit = rng.random() < 0.5
    ang = pi_tex(q) if unit else rf"{deg}^\circ"
    sol = []
    if level == "標準":
        k = (deg - base) // 360
        sol.append(rf"${ang}={pi_tex(F(base, 180)) if unit else str(base) + '^\\circ'}"
                   rf"{'+' if k > 0 else '-'}{abs(k) if abs(k) != 1 else ''}\times{'2\\pi' if unit else '360^\\circ'}$ なので、"
                   rf"${FN_TEX[fn]}\,{ang}={FN_TEX[fn]}\,{pi_tex(F(base, 180)) if unit else str(base) + '^\\circ'}$(周期性)")
    sol.append(rf"単位円上で角 ${base}^\circ$ の点は $\left({cos_deg(base).latex()},\ {sin_deg(base).latex()}\right)$")
    sol.append(rf"よって $${FN_TEX[fn]}\,{ang}={ans}$$")
    return Problem(
        "三角関数の値" + ("" if level == "基本" else "(負の角・一周をこえる角)"), level,
        rf"${FN_TEX[fn]}\left({ang}\right)$ の値を求めよ。",
        assemble(ans, wrongs, _pool(rng, "単位円をかいて、点の座標を確かめよう。"), value=float(trig_val(fn, base))),
        hints=[r"単位円上の点 $(\cos\theta,\ \sin\theta)$ を考える。$\tan\theta=\dfrac{\sin\theta}{\cos\theta}$。",
               r"$360^\circ$($2\pi$)ずらしても値は変わらない(周期性)。" if level == "標準" else
               r"$30^\circ, 45^\circ, 60^\circ$ の直角三角形の辺の比を思い出そう。"],
        solution=sol, meta=dict(fn=fn, deg=deg))


def trig_val(fn, deg):
    from exercises.helpers import trig_val as tv
    return tv(fn, deg)


def g_value(rng):
    return _value_problem(rng, "基本")


def g_value_ext(rng):
    return _value_problem(rng, "標準")


# ============================================================
# 基本:扇形の弧の長さと面積
# ============================================================
def g_sector(rng):
    r = rng.randint(2, 12)
    q = rng.choice([F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(5, 6), F(5, 4), F(4, 3)])
    kind = rng.choice(["弧の長さ", "面積"])
    deg = int(q * 180)
    if kind == "弧の長さ":
        ans = pi_tex(r * q)
        wrongs = [(pi_tex(r * q / 2), "弧の長さは $r\\theta$。$\\frac12$ がつくのは面積。"),
                  (pi_tex(r * r * q / 2), "それは面積 $\\frac12 r^2\\theta$。弧の長さは $r\\theta$。"),
                  (str(r * deg), "角は弧度法(ラジアン)で代入する。度数のまま $r\\theta$ に入れていないか。"),
                  (pi_tex(2 * r * q), "弧の長さは $r\\theta$。円周 $2\\pi r$ の公式と混ざっていないか。")]
        sol = [rf"$$l=r\theta={r}\times{pi_tex(q)}={pi_tex(r * q)}$$"]
    else:
        ans = pi_tex(F(r * r) * q / 2)
        wrongs = [(pi_tex(F(r * r) * q), "面積は $\\frac12 r^2\\theta$。$\\frac12$ を忘れていないか。"),
                  (pi_tex(F(r) * q / 2), "面積は $\\frac12 r^2\\theta$。$r$ を 2 乗し忘れていないか。"),
                  (pi_tex(r * q), "それは弧の長さ $r\\theta$。面積は $\\frac12 r^2\\theta$。"),
                  (tex_fr(F(r * r * deg, 2)), "角は弧度法で代入する。度数のまま入れていないか。")]
        sol = [rf"$$S=\frac12 r^2\theta=\frac12\times{r}^2\times{pi_tex(q)}={ans}$$"]
    return Problem(
        f"扇形の{kind}", "基本",
        rf"半径 ${r}$、中心角 ${pi_tex(q)}$ の扇形の{kind}を求めよ。",
        assemble(ans, wrongs), hints=[r"弧の長さ $l=r\theta$、面積 $S=\dfrac12r^2\theta=\dfrac12rl$($\theta$ は弧度法)。"],
        solution=sol, meta=dict(r=r, q=str(q), kind=kind))


# ============================================================
# 基本:相互関係(sin から cos・tan)
# ============================================================
TRIPLES = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17)]
QUAD = {1: (1, 1, "0<\\theta<\\frac{\\pi}{2}"), 2: (1, -1, "\\frac{\\pi}{2}<\\theta<\\pi"),
        3: (-1, -1, "\\pi<\\theta<\\frac{3\\pi}{2}"), 4: (-1, 1, "\\frac{3\\pi}{2}<\\theta<2\\pi")}


def g_mutual(rng):
    a, b, c = rng.choice(TRIPLES)
    quad = rng.choice([1, 2, 3, 4])
    ss, sc, rangetex = QUAD[quad]
    given = rng.choice(["sin", "cos"])
    ask = rng.choice(["cos" if given == "sin" else "sin", "tan"])
    s, co = F(ss * a, c), F(sc * b, c)
    vals = {"sin": s, "cos": co, "tan": s / co}
    ans = vals[ask]
    gval = vals[given]
    wrongs = [(tex_fr(-ans), "符号を確かめよう。$\\theta$ の範囲から、どの象限にあるかを考える。")]
    if ask == "tan":
        wrongs += [(tex_fr(1 / ans), "$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$。分母と分子が逆になっていないか。"),
                   (tex_fr(-1 / ans), "$\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}$ の分母・分子と符号を確かめよう。")]
    else:
        wrongs += [(tex_fr(F(1) - gval * gval), "$\\sin^2\\theta+\\cos^2\\theta=1$ から求めるのは 2 乗の値。最後に平方根をとる。"),
                   (tex_fr(ss * sc * gval) if abs(gval) != abs(ans) else None, "もう一方の値は $\\sqrt{1-(\\text{与えられた値})^2}$。")]
    fill = [(tex_fr(ans + d), "$\\sin^2\\theta+\\cos^2\\theta=1$ を使って計算しよう。") for d in (F(1, c), F(-1, c), F(2, c))]
    other = "cos" if given == "sin" else "sin"
    sol = [rf"$\{other}^2\theta=1-\{given}^2\theta=1-\left({tex_fr(gval)}\right)^2={tex_fr(1 - gval * gval)}$",
           rf"${rangetex}$ では $\{other}\theta {'>' if vals[other] > 0 else '<'} 0$ なので $\{other}\theta={tex_fr(vals[other])}$"]
    if ask == "tan":
        sol.append(rf"$$\tan\theta=\frac{{\sin\theta}}{{\cos\theta}}={tex_fr(ans)}$$")
    return Problem(
        "三角関数の相互関係", "基本",
        rf"${rangetex}$ で $\{given}\theta={tex_fr(gval)}$ のとき、$\{ask}\theta$ の値を求めよ。",
        assemble(tex_fr(ans), wrongs, fill, value=float(ans)),
        hints=[r"$\sin^2\theta+\cos^2\theta=1$、$\tan\theta=\dfrac{\sin\theta}{\cos\theta}$。",
               r"$\theta$ の範囲(何象限か)で、$\sin\theta,\ \cos\theta$ の符号が決まる。"],
        solution=sol, meta=dict(abc=(a, b, c), quad=quad, given=given, ask=ask))


# ============================================================
# 標準:正弦定理
# ============================================================
SURD = {30: (F(1, 2), 1), 45: (F(1, 2), 2), 60: (F(1, 2), 3), 90: (F(1), 1), 120: (F(1, 2), 3), 135: (F(1, 2), 2),
        150: (F(1, 2), 1)}


def surd_tex(coef, rad):
    """coef·√rad(rad は平方因子なし)の LaTeX"""
    return tex_frac_root(coef.numerator, coef.denominator, rad)


def surd_div(c1, r1, c2, r2):
    """(c1√r1)/(c2√r2) = (c1/(c2 r2))√(r1 r2) を簡単に"""
    coef, rad = F(c1) / (F(c2) * r2), r1 * r2
    k = 1
    for p in (2, 3, 5, 7):
        while rad % (p * p) == 0:
            rad //= p * p
            k *= p
    return coef * k, rad


def g_sine_law(rng):
    A, B = rng.sample([30, 45, 60, 90, 120, 135], 2)
    if A + B >= 180:
        raise Retry
    a = rng.randint(2, 9)
    kind = rng.choice(["辺", "外接円"])
    sA, sB = SURD[A], SURD[B]
    if kind == "辺":
        coef, rad = surd_div(a * sB[0], sB[1], sA[0], sA[1])
        ans = surd_tex(coef, rad)
        c2, r2 = surd_div(a * sA[0], sA[1], sB[0], sB[1])
        wrongs = [(surd_tex(c2, r2), "$\\dfrac{a}{\\sin A}=\\dfrac{b}{\\sin B}$ から $b=\\dfrac{a\\sin B}{\\sin A}$。分母と分子が逆になっていないか。"),
                  (surd_tex(a * sB[0], sB[1]), "$\\sin A$ で割り忘れていないか。"),
                  (surd_tex(coef * 2, rad), "正弦定理の式を確かめよう($2R$ は外接円の直径)。")]
        st = rf"$\triangle ABC$ で $a={a},\ A={A}^\circ,\ B={B}^\circ$ のとき、$b$ を求めよ。"
        sol = [r"正弦定理 $\dfrac{a}{\sin A}=\dfrac{b}{\sin B}$ より",
               rf"$$b=\frac{{a\sin B}}{{\sin A}}=\frac{{{a}\times{sin_deg(B).latex()}}}{{{sin_deg(A).latex()}}}={ans}$$"]
    else:
        coef, rad = surd_div(a, 1, 2 * sA[0], sA[1])
        ans = surd_tex(coef, rad)
        wrongs = [(surd_tex(coef * 2, rad), "$\\dfrac{a}{\\sin A}=2R$。$\\dfrac{a}{\\sin A}$ は直径 $2R$ なので、半径は 2 で割る。"),
                  (surd_tex(a * sA[0] / 2, sA[1]), "$R=\\dfrac{a}{2\\sin A}$。$\\sin A$ をかけるのではなく割る。"),
                  (surd_tex(*surd_div(a, 1, 2 * sB[0], sB[1])) if A != B else None, "辺 $a$ に向かい合う角は $A$。$\\sin B$ を使っていないか。")]
        st = rf"$\triangle ABC$ で $a={a},\ A={A}^\circ$ のとき、外接円の半径 $R$ を求めよ。"
        sol = [r"正弦定理 $\dfrac{a}{\sin A}=2R$ より",
               rf"$$R=\frac{{a}}{{2\sin A}}=\frac{{{a}}}{{2\times{sin_deg(A).latex()}}}={ans}$$"]
    fill = [(surd_tex(coef + d, rad), "正弦定理の式を確かめよう。") for d in (F(1), F(-1), F(1, 2))]
    return Problem("正弦定理", "標準", st, assemble(ans, wrongs, fill),
                   hints=[r"正弦定理 $\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=2R$($R$ は外接円の半径)。"],
                   solution=sol, meta=dict(A=A, B=B, a=a, kind=kind))


# ============================================================
# 標準:余弦定理
# ============================================================
def g_cos_law(rng):
    b, c = rng.randint(1, 8), rng.randint(1, 8)
    A = rng.choice([60, 90, 120])
    cosA = {60: F(1, 2), 90: F(0), 120: F(-1, 2)}[A]
    a2 = b * b + c * c - 2 * b * c * cosA
    if a2.denominator != 1 or a2 <= 0:
        raise Retry
    a2 = int(a2)
    kind = rng.choice(["辺", "角"])
    if kind == "辺":
        ans = tex_root(a2)
        wrongs = [(tex_root(int(b * b + c * c + 2 * b * c * cosA)), "余弦定理は $a^2=b^2+c^2-2bc\\cos A$。$\\cos A$ の項の符号を確かめよう。"),
                  (str(a2), "$a^2$ を求めたあと、平方根をとる。"),
                  (tex_root(int(b * b + c * c - b * c * cosA)), "余弦定理の $2bc\\cos A$ の 2 を忘れていないか。")]
        fill = [(tex_root(a2 + d), "余弦定理に代入して計算しよう。") for d in (1, -1, 2, 3)]
        st = rf"$\triangle ABC$ で $b={b},\ c={c},\ A={A}^\circ$ のとき、$a$ を求めよ。"
        sol = [rf"$$a^2=b^2+c^2-2bc\cos A={b}^2+{c}^2-2\cdot{b}\cdot{c}\cdot\left({tex_fr(cosA)}\right)={a2}$$",
               rf"$a>0$ より $a={ans}$"]
        out = assemble(ans, wrongs, fill)
    else:
        ans = rf"{A}^\circ"
        wrongs = [(rf"{180 - A}^\circ" if A != 90 else r"45^\circ", "$\\cos A$ の符号を確かめよう。$\\cos A<0$ なら $A$ は鈍角。"),
                  (r"30^\circ", "$\\cos A$ の値から角を求めるとき、$\\sin$ の値と取り違えていないか。"),
                  (r"150^\circ", "$\\cos A=\\dfrac{b^2+c^2-a^2}{2bc}$。分子の符号を確かめよう。")]
        fill = [(r"135^\circ", "余弦定理の変形を確かめよう。"), (r"45^\circ", "余弦定理の変形を確かめよう。")]
        st = rf"$\triangle ABC$ で $a={tex_root(a2)},\ b={b},\ c={c}$ のとき、角 $A$ を求めよ。"
        sol = [rf"$$\cos A=\frac{{b^2+c^2-a^2}}{{2bc}}=\frac{{{b * b}+{c * c}-{a2}}}{{2\cdot{b}\cdot{c}}}={tex_fr(cosA)}$$",
               rf"$0^\circ<A<180^\circ$ より $A={A}^\circ$"]
        out = assemble(ans, wrongs, fill)
    return Problem("余弦定理", "標準", st, out,
                   hints=[r"余弦定理 $a^2=b^2+c^2-2bc\cos A$、変形すると $\cos A=\dfrac{b^2+c^2-a^2}{2bc}$。"],
                   solution=sol, meta=dict(b=b, c=c, A=A, kind=kind))


# ============================================================
# 標準:加法定理で値を求める
# ============================================================
SPLIT = {15: (45, 30, "-"), 75: (45, 30, "+"), 105: (60, 45, "+"), 165: (120, 45, "+"), 195: (150, 45, "+"),
         255: (210, 45, "+"), 285: (240, 45, "+"), 345: (300, 45, "+")}


def g_addition(rng):
    deg = rng.choice(list(SPLIT))
    fn = rng.choice(["sin", "cos"])
    p, q, op = SPLIT[deg]
    sp, cp, sq, cq = sin_deg(p), cos_deg(p), sin_deg(q), cos_deg(q)
    if fn == "sin":
        val = sp * cq + cp * sq if op == "+" else sp * cq - cp * sq
        naive = sp + sq if op == "+" else sp - sq
        swapped = sp * cq - cp * sq if op == "+" else sp * cq + cp * sq
        formula = rf"\sin({p}^\circ{op}{q}^\circ)=\sin{p}^\circ\cos{q}^\circ{op}\cos{p}^\circ\sin{q}^\circ"
    else:
        val = cp * cq - sp * sq if op == "+" else cp * cq + sp * sq
        naive = cp + cq if op == "+" else cp - cq
        swapped = cp * cq + sp * sq if op == "+" else cp * cq - sp * sq
        mop = "-" if op == "+" else "+"
        formula = rf"\cos({p}^\circ{op}{q}^\circ)=\cos{p}^\circ\cos{q}^\circ{mop}\sin{p}^\circ\sin{q}^\circ"
    assert val == (sin_deg(deg) if fn == "sin" else cos_deg(deg))
    ans = val.latex()
    rad = rng.random() < 0.5                      # 弧度法と度数法を半々に
    def ang(d):  # noqa: E306
        return pi_tex(F(d, 180)) if rad else rf"{d}^\circ"
    wrongs = [(naive.latex(), "$\\sin(\\alpha+\\beta)\\neq\\sin\\alpha+\\sin\\beta$。加法定理を使う。"),
              (swapped.latex(), "加法定理の符号を確かめよう($\\cos$ の加法定理は符号が反対になる)。"),
              ((-val).latex(), "符号を確かめよう。角がどの象限にあるかで符号が決まる。"),
              ((cos_deg(deg) if fn == "sin" else sin_deg(deg)).latex(), "$\\sin$ と $\\cos$ を取り違えていないか。")]
    return Problem(
        "加法定理で値を求める", "標準", rf"加法定理を用いて、$\{fn}\,{ang(deg)}$ の値を求めよ。",
        assemble(ans, wrongs, value=float(val)),
        hints=[rf"${ang(deg)}={ang(p)}{op}{ang(q)}$ と分ける。",
               r"$\sin(\alpha\pm\beta)=\sin\alpha\cos\beta\pm\cos\alpha\sin\beta$、$\cos(\alpha\pm\beta)=\cos\alpha\cos\beta\mp\sin\alpha\sin\beta$。"],
        solution=[rf"$${formula if not rad else formula.replace(f'{p}^\\circ', ang(p) + ' ').replace(f'{q}^\\circ', ang(q) + ' ')}$$",
                  rf"$$={ans}$$"], meta=dict(deg=deg, fn=fn))


# ============================================================
# 標準:2倍角の公式
# ============================================================
def g_double(rng):
    a, b, c = rng.choice(TRIPLES)
    quad = rng.choice([1, 2])
    ss, sc, rangetex = QUAD[quad]
    s, co = F(ss * a, c), F(sc * b, c)
    ask = rng.choice(["sin", "cos"])
    if ask == "sin":
        ans = 2 * s * co
        wrongs = [(tex_fr(2 * s), "$\\sin 2\\alpha\\neq 2\\sin\\alpha$。$\\sin 2\\alpha=2\\sin\\alpha\\cos\\alpha$。"),
                  (tex_fr(-ans), "$\\cos\\alpha$ の符号を確かめよう($\\alpha$ の範囲に注意)。"),
                  (tex_fr(s * co), "$\\sin 2\\alpha=2\\sin\\alpha\\cos\\alpha$。2 を忘れていないか。")]
        sol = [rf"$\cos\alpha={tex_fr(co)}$($\sin^2\alpha+\cos^2\alpha=1$ と ${rangetex.replace(chr(92) + 'theta', chr(92) + 'alpha')}$ から)",
               rf"$$\sin 2\alpha=2\sin\alpha\cos\alpha=2\cdot{tex_fr(s)}\cdot\left({tex_fr(co)}\right)={tex_fr(ans)}$$"]
    else:
        ans = 1 - 2 * s * s
        wrongs = [(tex_fr(2 * co), "$\\cos 2\\alpha\\neq 2\\cos\\alpha$。$\\cos 2\\alpha=1-2\\sin^2\\alpha$。"),
                  (tex_fr(1 - s * s), "$\\cos 2\\alpha=1-2\\sin^2\\alpha$。2 を忘れていないか。"),
                  (tex_fr(-ans), "$\\cos 2\\alpha=\\cos^2\\alpha-\\sin^2\\alpha$。順番(符号)を確かめよう。")]
        sol = [rf"$$\cos 2\alpha=1-2\sin^2\alpha=1-2\left({tex_fr(s)}\right)^2={tex_fr(ans)}$$"]
    fill = [(tex_fr(ans + F(d, c * c)), "2倍角の公式に代入して計算しよう。") for d in (1, -1, 7, -7)]
    return Problem(
        "2倍角の公式", "標準",
        rf"${rangetex.replace(chr(92) + 'theta', chr(92) + 'alpha')}$ で $\sin\alpha={tex_fr(s)}$ のとき、$\{ask} 2\alpha$ の値を求めよ。",
        assemble(tex_fr(ans), wrongs, fill, value=float(ans)),
        hints=[r"$\sin 2\alpha=2\sin\alpha\cos\alpha$、$\cos 2\alpha=1-2\sin^2\alpha=2\cos^2\alpha-1$。",
               r"$\cos\alpha$ が必要なら、$\sin^2\alpha+\cos^2\alpha=1$ と $\alpha$ の範囲から求める。"],
        solution=sol, meta=dict(abc=(a, b, c), quad=quad, ask=ask))


REGISTRY = [
    ProblemType("deg2rad", "度数法を弧度法に", "基本", g_deg2rad),
    ProblemType("rad2deg", "弧度法を度数法に", "基本", g_rad2deg),
    ProblemType("value", "有名角の三角関数の値", "基本", g_value),
    ProblemType("sector", "扇形の弧の長さ・面積", "基本", g_sector),
    ProblemType("mutual", "三角関数の相互関係", "基本", g_mutual),
    ProblemType("value_ext", "負の角・一周をこえる角の値", "標準", g_value_ext),
    ProblemType("sine_law", "正弦定理", "標準", g_sine_law),
    ProblemType("cos_law", "余弦定理", "標準", g_cos_law),
    ProblemType("addition", "加法定理で値を求める", "標準", g_addition),
    ProblemType("double", "2倍角の公式", "標準", g_double),
]

TITLE = "三角比・三角関数の基礎"


def tab():
    render("basics", REGISTRY, TITLE)
