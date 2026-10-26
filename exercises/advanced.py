"""演習:発展(逆三角関数の主値、接線の傾き、テイラー展開、球面座標・球面三角形)"""
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


# ============================================================
# 球面座標・緯度経度・球面三角形
# ============================================================
R_EARTH = 6400
SPH_TH = [30, 45, 60, 90, 120, 135, 150]
SPH_PH = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def kpi(q, unit=""):
    """q·π（q は Fraction）の LaTeX。unit をうしろにつける"""
    q = F(q)
    if q.denominator == 1:
        body = ("" if q.numerator == 1 else str(q.numerator)) + r"\pi"
    else:
        body = rf"\frac{{{'' if q.numerator == 1 else q.numerator}\pi}}{{{q.denominator}}}"
    return body + unit


def km(t):
    return t + r"\ \mathrm{km}"


def lat_tex(lat):
    return rf"\text{{{'北緯' if lat >= 0 else '南緯'}}}\ {abs(lat)}^\circ"


def lon_tex(lon):
    return rf"\text{{{'東経' if lon >= 0 else '西経'}}}\ {abs(lon)}^\circ"


def g_sph_xyz(rng):
    """球面座標(または緯度・経度)→ 直交座標"""
    geo = rng.random() < 0.4
    r = rng.choice([2, 4, 6])
    th, ph = rng.choice(SPH_TH), rng.choice(SPH_PH)
    comp = rng.choice(["x", "y", "z"])
    st_, ct, sp, cp = sin_deg(th), cos_deg(th), sin_deg(ph), cos_deg(ph)
    vals = {"x": r * st_ * cp, "y": r * st_ * sp, "z": r * ct}
    ans = vals[comp]
    if comp == "z":
        cands = [((r * st_).latex(), "$z$ 座標は $z$ 軸への影なので $r\\cos\\theta$($\\theta$ は $z$ 軸から測った角)。"),
                 ((-ans).latex(), "符号を確かめよう。"), ((r * ct * cp).latex(), "$z$ 座標は $\\varphi$ によらない。"),
                 (str(r), "$z$ 軸とのなす角 $\\theta$ を使う。")]
    else:
        other = vals["y" if comp == "x" else "x"]
        swap = r * ct * (cp if comp == "x" else sp)
        cands = [(swap.latex(), "床($xy$ 平面)に落とした長さは $\\rho=r\\sin\\theta$(cos ではない)。"),
                 (other.latex(), ("$x$" if comp == "x" else "$y$") + " 座標は $\\rho\\cos\\varphi$、$\\rho\\sin\\varphi$ のどちらか確かめよう。"),
                 ((-ans).latex(), "符号を確かめよう。"),
                 ((r * (cp if comp == "x" else sp)).latex(), "まず $\\rho=r\\sin\\theta$ を求めてから $\\cos\\varphi$($\\sin\\varphi$)をかける。")]
    fillers = [("0", "図をかいて確かめよう。"), (str(r), "図をかいて確かめよう。"), (tex_fr(F(r, 2)), "図をかいて確かめよう。")]
    if geo:
        lat, lon = 90 - th, (ph if ph <= 180 else ph - 360)
        stmt = (rf"地球を中心 O、半径 ${r}$ の球とし、赤道面を $xy$ 平面、北極の向きを $z$ 軸の正の向き、"
                rf"経度 $0^\circ$ の経線を含む向きを $x$ 軸の正の向きとする(東経を正の向きに測る)。"
                rf"${lat_tex(lat)}$、${lon_tex(lon)}$ の地点の ${comp}$ 座標を求めよ。")
        hints = [r"緯度は赤道(xy 平面)から測った角。$z=R\sin(\text{緯度})$、床に落とした長さは $\rho=R\cos(\text{緯度})$。",
                 r"$x=\rho\cos(\text{経度}),\ y=\rho\sin(\text{経度})$。西経は負の角として計算する。"]
        sol = [rf"$\rho={r}\cos({lat}^\circ)={(r * st_).latex()}$、$z={r}\sin({lat}^\circ)={(r * ct).latex()}$",
               rf"${comp}={ans.latex()}$"]
    else:
        stmt = (rf"球面座標 $(r,\ \theta,\ \varphi)=\left({r},\ {P(th)},\ {P(ph)}\right)$ で表される点の ${comp}$ 座標を求めよ。"
                r"ただし $\theta$ は $z$ 軸の正の向きから測った角、$\varphi$ は $x$ 軸の正の向きから測った角とする。")
        hints = [r"$z=r\cos\theta$、床($xy$ 平面)に落とした長さは $\rho=r\sin\theta$。",
                 r"$x=\rho\cos\varphi=r\sin\theta\cos\varphi,\ y=\rho\sin\varphi=r\sin\theta\sin\varphi$"]
        sol = [rf"$\rho={r}\sin {P(th)}={(r * st_).latex()}$、$z={r}\cos {P(th)}={(r * ct).latex()}$",
               rf"${comp}={ans.latex()}$"]
    return Problem("球面座標と直交座標", "基本", stmt, assemble(ans.latex(), cands, fillers, value=float(ans)),
                   hints=hints, solution=sol, meta=dict(r=r, th=th, ph=ph, comp=comp))


def g_lat_circle(rng):
    lat = rng.choice([30, 45, 60, -30, -45, -60])
    a = abs(lat)
    ans = 2 * R_EARTH * cos_deg(a)
    t = lambda q: km(q.latex() + r"\pi")  # noqa: E731
    cands = [(t(2 * R_EARTH * sin_deg(a)), "緯線の円の半径は $R\\cos(\\text{緯度})$(sin ではない)。"),
             (t(R_EARTH * cos_deg(a)), "円の周の長さは $2\\pi\\times$ 半径。"),
             (km(rf"{2 * R_EARTH}\pi"), "それは赤道の長さ。緯線の円の半径は、北(南)へ行くほど小さくなる。"),
             (t(2 * R_EARTH * cos_deg(a) / 2), "円の周の長さは $2\\pi\\times$ 半径。")]
    return Problem("緯線の長さ", "基本",
                   rf"地球を半径 ${R_EARTH}\ \mathrm{{km}}$ の球とするとき、${lat_tex(lat)}$ の緯線(同じ緯度の点を結んだ円)の長さを求めよ。",
                   assemble(t(ans), cands, value=float(ans) * math.pi),
                   hints=[r"緯線は、地軸に垂直な平面で地球を切った円。中心から見た図をかくと、その円の半径は $R\cos(\text{緯度})$。"],
                   solution=[rf"半径は ${R_EARTH}\cos {a}^\circ={(R_EARTH * cos_deg(a)).latex()}$",
                             rf"長さは $2\pi\times{(R_EARTH * cos_deg(a)).latex()}={t(ans)}$"],
                   meta=dict(lat=lat))


def g_gc_dist(rng):
    if rng.random() < 0.5:   # 同じ経線上
        lon = rng.choice([135, 140, -75, 0, 30])
        l1 = rng.choice([15, 30, 45, 60, 75, -15, -30, -45])
        l2 = rng.choice([x for x in (0, 15, 30, 45, 60, 75, -15, -30, -45, -60) if x != l1])
        d = abs(l1 - l2)
        wrong_d = abs(abs(l1) - abs(l2)) if l1 * l2 < 0 else (l1 + l2 if l1 + l2 <= 180 else None)
        stmt = rf"${lat_tex(l1)},\ {lon_tex(lon)}$ の地点と、${lat_tex(l2)},\ {lon_tex(lon)}$ の地点"
        key = "緯度の差"
        why_d = "北緯と南緯にまたがるときは、中心角は緯度の和(赤道をはさむ)。" if l1 * l2 < 0 else "同じ側(北どうし・南どうし)なら中心角は緯度の差。"
    else:                     # 赤道上
        g1 = rng.choice([0, 30, 45, 60, 90, 120, 135, 150, 165, -30, -60, -90, -120, -150])
        g2 = rng.choice([x for x in (0, 15, 45, 75, 90, 105, 135, 180, -15, -45, -75, -105, -135, -165) if x != g1])
        d = abs(g1 - g2)
        if d > 180:
            d = 360 - d
        wrong_d = abs(g1 - g2) if abs(g1 - g2) > 180 else (abs(abs(g1) - abs(g2)) if g1 * g2 < 0 else None)
        stmt = rf"赤道上の ${lon_tex(g1)}$ の地点と、赤道上の ${lon_tex(g2)}$ の地点"
        key = "経度の差"
        why_d = "経度の差が $180^\\circ$ をこえるときは、反対まわりのほうが近い。" if abs(g1 - g2) > 180 else "東経と西経にまたがるときは、経度の差は和になる。"
    if d == 0:
        raise Retry
    q = F(R_EARTH * d, 180)
    ans = km(kpi(q))
    cands = [(km(kpi(F(R_EARTH * wrong_d, 180))) if wrong_d else None, why_d),
             (km(str(R_EARTH * d)), "弧の長さは $R\\theta$ で、$\\theta$ はラジアン。度のまま使わない。"),
             (km(kpi(q * 2)), "弧の長さは $R\\theta$($2R\\theta$ ではない)。"),
             (km(kpi(q / 2)), "弧の長さは $R\\theta$。"),
             (km(kpi(F(R_EARTH * (360 - d), 180))), "短いほうの弧を選ぶ。")]
    return Problem("大円距離(同じ経線上・赤道上)", "基本",
                   rf"地球を半径 ${R_EARTH}\ \mathrm{{km}}$ の球とする。{stmt}の、地球の表面にそった最短距離を求めよ。",
                   assemble(ans, cands, value=float(q) * math.pi),
                   hints=[r"2 点を結ぶ大円の弧の長さは $R\theta$($\theta$ は中心角、ラジアン)。",
                          rf"どちらも同じ大円({'経線' if key == '緯度の差' else '赤道'})の上にあるので、中心角は{key}から求められる。"],
                   solution=[rf"中心角は ${d}^\circ={pi_tex(F(d, 180))}$",
                             rf"距離は ${R_EARTH}\times{pi_tex(F(d, 180))}={ans}$"],
                   meta=dict(d=d))


def g_girard(rng):
    while True:
        angs = [rng.choice(range(30, 180, 15)) for _ in range(3)]
        tot = sum(angs)
        if 180 < tot < 540:
            break
    E = F(tot - 180, 180)
    ans = pi_tex(E) + "r^2"
    cands = [(pi_tex(F(tot, 180)) + "r^2", "角の和から $\\pi$(180°)を引いた分が面積になる。"),
             (f"{tot - 180}r^2", "角はラジアンに直して計算する。"),
             (pi_tex(2 * E) + "r^2", "面積は $(\\alpha+\\beta+\\gamma-\\pi)r^2$。"),
             (pi_tex(E / 2) + "r^2", "面積は $(\\alpha+\\beta+\\gamma-\\pi)r^2$。"),
             (pi_tex(E) + "r", "面積なので $r^2$ をかける。")]
    a, b, c = angs
    return Problem("球面三角形の面積(ジラールの定理)", "基本",
                   rf"半径 $r$ の球面上の球面三角形で、3 つの角が ${a}^\circ,\ {b}^\circ,\ {c}^\circ$ のとき、その面積を求めよ。",
                   assemble(ans, cands, value=float(E) * math.pi),
                   hints=[r"ジラールの定理:面積 $=(\alpha+\beta+\gamma-\pi)\,r^2$(角はラジアン)。",
                          r"角の和が $180^\circ$ をこえた分(球過量)が、面積に比例する。"],
                   solution=[rf"$\alpha+\beta+\gamma={tot}^\circ={pi_tex(F(tot, 180))}$",
                             rf"面積は $\left({pi_tex(F(tot, 180))}-\pi\right)r^2={ans}$"],
                   meta=dict(angs=angs))


def g_sph_cos(rng):
    a, b = rng.choice(SPH_TH), rng.choice(SPH_TH)
    g = rng.choice([30, 45, 60, 90, 120, 135, 150])
    if a == 90 and b == 90:
        raise Retry
    ca, cb, sa, sb, cg = cos_deg(a), cos_deg(b), sin_deg(a), sin_deg(b), cos_deg(g)
    ans = ca * cb + sa * sb * cg
    cands = [((ca * cb - sa * sb * cg).latex(), "球面の余弦法則は $\\cos c=\\cos a\\cos b+\\sin a\\sin b\\cos\\gamma$(符号は ＋)。"),
             ((sa * sb + ca * cb * cg).latex(), "$\\cos\\gamma$ がかかるのは $\\sin a\\sin b$ のほう。"),
             ((ca * cb + sa * sb).latex(), "$\\cos\\gamma$ をかけ忘れていないか。"),
             ((ca * cb).latex(), "$\\sin a\\sin b\\cos\\gamma$ の項も足す。"),
             ((-ans).latex(), "符号を確かめよう。")]
    return Problem("球面の余弦法則", "標準",
                   rf"単位球面上の球面三角形 ABC で、辺 $a=\mathrm{{BC}}={P(a)}$、$b=\mathrm{{CA}}={P(b)}$(辺の長さは中心角)、"
                   rf"$\angle\mathrm{{C}}=\gamma={P(g)}$ のとき、辺 $c=\mathrm{{AB}}$ について $\cos c$ の値を求めよ。",
                   assemble(ans.latex(), cands, value=float(ans)),
                   hints=[r"球面の余弦法則:$\cos c=\cos a\cos b+\sin a\sin b\cos\gamma$",
                          r"C を北極に置き、A, B の座標から弦 AB の長さの 2 乗を 2 通りに表すと導ける(「球面三角形」のページ)。"],
                   solution=[rf"$\cos c=\cos {P(a)}\cos {P(b)}+\sin {P(a)}\sin {P(b)}\cos {P(g)}$",
                             rf"$=({ca.latex()})({cb.latex()})+({sa.latex()})({sb.latex()})({cg.latex()})={ans.latex()}$"],
                   meta=dict(a=a, b=b, g=g))


REGISTRY = [
    ProblemType("arc", "逆三角関数の値(主値)", "基本", g_arc),
    ProblemType("slope", "接線の傾き", "基本", g_slope),
    ProblemType("tcoef", "テイラー展開の係数", "基本", g_taylor_coef),
    ProblemType("arc_of", "逆三角関数と三角関数の組み合わせ", "標準", g_arc_of),
    ProblemType("sph_xyz", "球面座標と直交座標", "基本", g_sph_xyz),
    ProblemType("lat_circle", "緯線の長さ", "基本", g_lat_circle),
    ProblemType("gc_dist", "大円距離(同じ経線上・赤道上)", "基本", g_gc_dist),
    ProblemType("girard", "球面三角形の面積(ジラールの定理)", "基本", g_girard),
    ProblemType("tval", "テイラー展開で近似値", "標準", g_taylor_val),
    ProblemType("sph_cos", "球面の余弦法則", "標準", g_sph_cos),
]

TITLE = "発展(逆三角関数・接線・テイラー展開・球面)"


def tab():
    render("advanced", REGISTRY, TITLE)
