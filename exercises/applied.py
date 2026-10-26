"""演習:学科別の応用(学科共通・機械・電気・化学・都市)"""
from fractions import Fraction as F
from math import gcd

from exercises.core import Problem, ProblemType, Retry, render, tex_fr, tex_root
from exercises.helpers import Q236, assemble, cos_deg, pi_tex, sin_deg, tan_deg


def unit(t, u):
    return rf"{t}\ \text{{{u}}}"


def over_tan(x, th):
    """x / tan θ(θ = 30, 45, 60)を厳密に(x は整数)"""
    return {30: Q236.sqrt_of(3, x), 45: Q236(x), 60: Q236.sqrt_of(3, F(x, 3))}[th]


def num(x, d=1):
    s = f"{x:.{d}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ============================================================
# 学科共通:観覧車
# ============================================================
def g_ferris(rng):
    r = rng.choice([20, 25, 30, 40, 50])
    T = rng.choice([12, 15, 18, 20, 24])
    a = rng.choice([2, 4, 5])
    k = rng.randint(1, 11)
    t = F(T * k, 12)
    h0 = r + a
    h = Q236(h0) - cos_deg(30 * k) * r
    wrongs = [(unit((Q236(h0) - sin_deg(30 * k) * r).latex(), "m"), "乗り場(いちばん下)から回るので、中心より $r\\cos\\theta$ だけ下。$\\sin$ ではない。"),
              (unit((Q236(h0) + cos_deg(30 * k) * r).latex(), "m"), "$h=h_0-r\\cos\\theta$。符号を確かめよう($\\theta=0$ でいちばん下)。"),
              (unit((Q236(a) - cos_deg(30 * k) * r).latex(), "m"), "中心の高さは $h_0=r+a$。"),
              (unit((Q236(h0) - cos_deg(30 * k) * r * 2).latex(), "m"), "$\\theta=\\dfrac{2\\pi t}{T}$ を確かめよう。")]
    return Problem("【共通】観覧車の高さ", "基本",
                   rf"半径 ${r}$ m、1 周 ${T}$ 分の観覧車がある。いちばん下のゴンドラの高さは ${a}$ m である。"
                   rf"いちばん下で乗ってから ${tex_fr(t)}$ 分後のゴンドラの高さを求めよ。",
                   assemble(unit(h.latex(), "m"), wrongs, value=float(h)),
                   hints=[r"中心の高さ $h_0=r+a$。回った角を $\theta$ とすると $h=h_0-r\cos\theta$。", r"$\theta=\dfrac{2\pi t}{T}$"],
                   solution=[rf"$\theta=\dfrac{{2\pi\times{tex_fr(t)}}}{{{T}}}={pi_tex(F(k, 6))}$",
                             rf"$$h={h0}-{r}\cos {pi_tex(F(k, 6))}={h.latex()}\ \text{{m}}$$"], meta=dict(r=r, T=T, a=a, k=k))


def g_ferris_time(rng):
    r = rng.choice([20, 30, 40, 50])
    T = rng.choice([12, 15, 18, 24])
    a = rng.choice([2, 5])
    c, th = rng.choice([(F(1, 2), 60), (F(0), 90), (F(-1, 2), 120)])
    h0 = r + a
    H = h0 - c * r
    dur = F(T) * (1 - F(th, 180))
    wrongs = [(unit(tex_fr(F(T) * F(th, 180)), "分"), "それは H より低い所にいる時間。"),
              (unit(tex_fr(F(T) * (1 - F(th, 360))), "分"), "$\\cos\\theta\\le c$ をみたす $\\theta$ は $\\theta_0\\le\\theta\\le2\\pi-\\theta_0$。両端を確かめよう。"),
              (unit(tex_fr(F(T, 2)), "分") if th != 90 else unit(tex_fr(F(T, 4)), "分"), "中心より上か下かだけでなく、$\\cos\\theta$ の値から角を求めよう。"),
              (unit(tex_fr(F(T) * F(th, 360)), "分"), "1 周 $2\\pi$ が $T$ 分に対応する。")]
    return Problem("【共通】観覧車で高い所にいる時間", "標準",
                   rf"半径 ${r}$ m、1 周 ${T}$ 分、いちばん下のゴンドラの高さ ${a}$ m の観覧車で、"
                   rf"1 周のうち高さ ${tex_fr(H)}$ m 以上にいるのは何分間か。",
                   assemble(unit(tex_fr(dur), "分"), wrongs, value=float(dur)),
                   hints=[r"$h=h_0-r\cos\theta\ge H$ ⇔ $\cos\theta\le\dfrac{h_0-H}{r}$。", r"単位円で、$x$ 座標が $c$ 以下になる角の範囲を考える。"],
                   solution=[rf"$h_0={h0}$。${h0}-{r}\cos\theta\ge{tex_fr(H)}$ ⇔ $\cos\theta\le{tex_fr(c)}$",
                             rf"${pi_tex(F(th, 180))}\le\theta\le{pi_tex(2 - F(th, 180))}$ の間(1 周の ${tex_fr(1 - F(th, 180))}$)",
                             rf"$${T}\times{tex_fr(1 - F(th, 180))}={tex_fr(dur)}\ \text{{分}}$$"], meta=dict(r=r, T=T, th=th))


# ============================================================
# 機械
# ============================================================
def g_rpm(rng):
    N = rng.choice([30, 60, 90, 120, 150, 300, 600, 900, 1200, 1500, 1800, 3000])
    w = F(N, 30)
    wrongs = [(unit(pi_tex(2 * N), "rad/s"), "rpm は 1 分間の回転数。60 で割って 1 秒あたりにする。"),
              (unit(pi_tex(F(N, 60)), "rad/s"), "1 回転は $2\\pi$ rad。2 をかけ忘れていないか。"),
              (unit(tex_fr(F(N, 60)), "rad/s"), "それは 1 秒あたりの回転数。角速度は $2\\pi$ をかける。"),
              (unit(pi_tex(F(N, 15)), "rad/s"), "$\\omega=\\dfrac{2\\pi N}{60}$。")]
    return Problem("【機械】回転数と角速度", "基本", rf"毎分 ${N}$ 回転({N} rpm)する軸の角速度 $\omega$ を求めよ。",
                   assemble(unit(pi_tex(w), "rad/s"), wrongs, value=float(w)),
                   hints=[r"1 回転は $2\pi$ rad。1 分は 60 秒。", r"$\omega=\dfrac{2\pi N}{60}$ [rad/s]"],
                   solution=[rf"$$\omega=\frac{{2\pi\times{N}}}{{60}}={pi_tex(w)}\ \text{{rad/s}}$$"], meta=dict(N=N))


def g_gear(rng):
    z1, z2 = rng.sample([12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 48, 60], 2)
    N1 = rng.choice([60, 120, 180, 240, 360, 600, 720, 1200])
    N2 = F(N1 * z1, z2)
    if N2.denominator != 1:
        raise Retry
    N2 = int(N2)
    wrongs = [(unit(tex_fr(F(N1 * z2, z1)), "rpm"), "歯数の多い歯車ほどゆっくり回る。$N_2=N_1\\times\\dfrac{z_1}{z_2}$。逆にしていないか。"),
              (unit(str(N1), "rpm"), "歯数が違えば回転数も変わる。"),
              (unit(str(N1 + z1 - z2), "rpm"), "回転数は歯数に反比例する(かみ合う点の速さが同じ)。"),
              (unit(str(N2 * 2), "rpm"), "$N_2=N_1\\times\\dfrac{z_1}{z_2}$ に代入しよう。")]
    return Problem("【機械】歯車の回転数", "基本",
                   rf"歯数 ${z1}$ の歯車 A が毎分 ${N1}$ 回転している。A とかみ合う歯数 ${z2}$ の歯車 B の回転数を求めよ。",
                   assemble(unit(str(N2), "rpm"), wrongs, value=N2),
                   hints=[r"かみ合う歯車は、1 秒間に送る歯の数が同じ:$z_1N_1=z_2N_2$。"],
                   solution=[rf"$${z1}\times{N1}={z2}\times N_2\quad\Rightarrow\quad N_2={N2}\ \text{{rpm}}$$"], meta=dict(z1=z1, z2=z2, N1=N1))


def g_crank(rng):
    r = rng.randint(2, 6)
    l = rng.randint(r + 3, 15)
    th = rng.choice([90, 0, 180, 90])
    if th == 90:
        ans = tex_root(l * l - r * r)
    elif th == 0:
        ans = str(l + r)
    else:
        ans = str(l - r)
    wrongs = [(str(l), "$l$ だけでは単振動の近似。余弦定理 $l^2=r^2+x^2-2rx\\cos\\theta$ から $x$ を求める。"),
              (tex_root(l * l + r * r), "$\\theta=90^\\circ$ のとき、$x^2+r^2=l^2$(直角三角形の斜辺は $l$)。"),
              (str(l - r) if th != 180 else str(l + r), "$\\cos\\theta$ の符号を確かめよう。"),
              (str(l + r) if th != 0 else tex_root(l * l - r * r), "クランク角 $\\theta$ のときの三角形を考えよう。")]
    return Problem("【機械】ピストンの位置(余弦定理)", "標準" if th == 90 else "基本",
                   rf"クランク半径 $r={r}$ cm、連接棒の長さ $l={l}$ cm のピストン・クランク機構で、クランク角 $\theta={th}^\circ$ のときの、"
                   r"クランクの中心からピストンピンまでの距離 $x$ [cm] を求めよ。",
                   assemble(ans, wrongs),
                   hints=[r"余弦定理 $l^2=r^2+x^2-2rx\cos\theta$。", r"$x=r\cos\theta+\sqrt{l^2-r^2\sin^2\theta}$"],
                   solution=[rf"$$x=r\cos\theta+\sqrt{{l^2-r^2\sin^2\theta}}={r}\cos {th}^\circ+\sqrt{{{l}^2-{r}^2\sin^2 {th}^\circ}}={ans}$$"],
                   meta=dict(r=r, l=l, th=th))


def g_friction(rng):
    mu, th = rng.choice([(r"\frac{1}{\sqrt{3}}", 30), ("1", 45), (r"\sqrt{3}", 60)])
    wrongs = [(rf"{90 - th}^\circ" if th != 45 else r"60^\circ", "摩擦角は $\\tan\\theta=\\mu$。$\\sin$ や $\\cos$ と取り違えていないか。"),
              (r"15^\circ", "$\\tan\\theta=\\mu$ となる角を、有名角の $\\tan$ の値から探そう。"),
              (r"75^\circ", "$\\mu mg\\cos\\theta=mg\\sin\\theta$ から $\\tan\\theta=\\mu$。"),
              (r"30^\circ" if th != 30 else r"90^\circ", "$\\tan 30^\\circ=\\frac{1}{\\sqrt3},\\ \\tan 45^\\circ=1,\\ \\tan 60^\\circ=\\sqrt3$。")]
    return Problem("【機械】摩擦角", "基本",
                   rf"板の上に物体をのせ、板をゆっくり傾けていく。物体と板の静止摩擦係数が $\mu={mu}$ のとき、物体がすべり出す角度を求めよ。",
                   assemble(rf"{th}^\circ", wrongs, value=th),
                   hints=[r"すべらせる力 $mg\sin\theta$ と最大摩擦力 $\mu mg\cos\theta$ が等しくなる角。", r"$\tan\theta=\mu$"],
                   solution=[rf"$mg\sin\theta=\mu mg\cos\theta$ より $\tan\theta=\mu={mu}$、よって $\theta={th}^\circ$"], meta=dict(th=th))


# ============================================================
# 電気
# ============================================================
def g_ac_peak(rng):
    Ve = rng.choice([100, 200, 50, 6600, 120, 230])
    rev = rng.random() < 0.4
    if not rev:
        ans = rf"{Ve}\sqrt{{2}}"
        wrongs = [(rf"{tex_fr(F(Ve, 2))}\sqrt{{2}}", "実効値 $=\\dfrac{\\text{最大値}}{\\sqrt2}$ なので、最大値は実効値の $\\sqrt2$ 倍。割っていないか。"),
                  (str(2 * Ve), "最大値は実効値の $\\sqrt2$ 倍(2 倍ではない)。"),
                  (str(Ve), "表示されている電圧(実効値)と最大値は違う。"), (rf"{Ve}\sqrt{{3}}", "単相の交流では $\\sqrt2$ 倍。$\\sqrt3$ は三相の線間電圧。")]
        st = rf"実効値 ${Ve}$ V の交流電圧の最大値 $V_m$ [V] を求めよ。"
        sol = [rf"$$V_m=\sqrt2\,V={Ve}\sqrt2\ (\approx {num(Ve * 2 ** 0.5)})\ \text{{V}}$$"]
    else:
        ans = str(Ve)
        wrongs = [(rf"{Ve}\sqrt{{2}}", "実効値は最大値の $\\frac{1}{\\sqrt2}$ 倍。"), (rf"{tex_fr(F(Ve, 2))}\sqrt{{2}}", "$\\dfrac{V_m}{\\sqrt2}$ を計算しよう。"),
                  (str(2 * Ve), "実効値は最大値より小さい。"), (rf"{Ve}\sqrt{{3}}", "$\\sqrt3$ ではなく $\\sqrt2$。")]
        st = rf"最大値 ${Ve}\sqrt{{2}}$ V の交流電圧の実効値 $V$ [V] を求めよ。"
        sol = [rf"$$V=\frac{{V_m}}{{\sqrt2}}=\frac{{{Ve}\sqrt2}}{{\sqrt2}}={Ve}\ \text{{V}}$$"]
    return Problem("【電気】交流の最大値と実効値", "基本", st, assemble(ans, wrongs),
                   hints=[r"正弦波の交流では、実効値 $V=\dfrac{V_m}{\sqrt2}$($v^2$ の平均の平方根)。"], solution=sol, meta=dict(Ve=Ve, rev=rev))


def g_ac_omega(rng):
    f = rng.choice([50, 60])
    ask = rng.choice(["角周波数", "周期"])
    if ask == "角周波数":
        ans = unit(pi_tex(2 * f), "rad/s")
        wrongs = [(unit(pi_tex(f), "rad/s"), "$\\omega=2\\pi f$。2 を忘れていないか。"), (unit(pi_tex(F(2, f)), "rad/s"), "$\\omega=2\\pi f$。$f$ で割るのではない。"),
                  (unit(str(f), "rad/s"), "周波数 $f$ [Hz] と角周波数 $\\omega$ [rad/s] は違う。"), (unit(pi_tex(4 * f), "rad/s"), "$\\omega=2\\pi f$ に代入しよう。")]
        sol = [rf"$$\omega=2\pi f=2\pi\times{f}={pi_tex(2 * f)}\ \text{{rad/s}}$$"]
    else:
        ans = unit(tex_fr(F(1000, f)), "ms")
        wrongs = [(unit(str(f), "ms"), "周期 $T=\\dfrac1f$。"), (unit(tex_fr(F(500, f)), "ms"), "1 周期で 1 回振動する。$T=\\dfrac1f$。"),
                  (unit(tex_fr(F(2000, f)), "ms"), "$T=\\dfrac1f$ s を ms にする(1000 倍)。"), (unit(tex_fr(F(1, f)), "ms"), "単位を確かめよう($\\frac1f$ s は ms ではない)。")]
        sol = [rf"$$T=\frac{{1}}{{f}}=\frac{{1}}{{{f}}}\ \text{{s}}={tex_fr(F(1000, f))}\ \text{{ms}}$$"]
    return Problem(f"【電気】交流の{ask}", "基本", rf"周波数 ${f}$ Hz の交流の{ask}を求めよ。", assemble(ans, wrongs),
                   hints=[r"周期 $T=\dfrac1f$、角周波数 $\omega=2\pi f$($v=V_m\sin\omega t$ の $\omega$)。"], solution=sol, meta=dict(f=f, ask=ask))


def g_three_phase(rng):
    V = rng.choice([100, 115, 200, 230, 400])
    ans = rf"{V}\sqrt{{3}}"
    wrongs = [(str(3 * V), "線間電圧は相の電圧の $\\sqrt3$ 倍(3 倍ではない)。"), (rf"{V}\sqrt{{2}}", "$\\sqrt2$ は最大値と実効値の関係。線間電圧は $\\sqrt3$ 倍。"),
              (str(2 * V), "2 つの相の差は、120° ずれた 2 つの sin の差。和積の公式で $2\\sin 60^\\circ=\\sqrt3$ 倍になる。"), (str(V), "2 つの相の電圧の差を考えよう。")]
    return Problem("【電気】三相交流の線間電圧", "基本",
                   rf"各相の電圧(実効値)が ${V}$ V の三相交流で、2 本の電線の間の電圧(線間電圧、実効値)を求めよ。",
                   assemble(ans, wrongs),
                   hints=[r"$\sin\theta-\sin(\theta-120^\circ)=\sqrt3\sin(\theta+30^\circ)$(合成・和積の公式)。"],
                   solution=[rf"線間電圧は相の電圧の $\sqrt3$ 倍なので ${V}\sqrt3\ (\approx{num(V * 3 ** 0.5)})$ V"], meta=dict(V=V))


def g_power(rng):
    V = rng.choice([100, 200])
    I = rng.choice([2, 4, 5, 10])
    ph = rng.choice([0, 30, 45, 60, 90])
    P = cos_deg(ph) * (V * I)
    wrongs = [(unit((sin_deg(ph) * (V * I)).latex(), "W") if ph not in (45,) else None, "有効電力は $VI\\cos\\varphi$($\\sin\\varphi$ は無効電力)。"),
              (unit(str(V * I), "W"), "位相がずれると電力がもどる分がある。力率 $\\cos\\varphi$ をかける。"),
              (unit((cos_deg(ph) * (V * I * 2)).latex(), "W"), "$V,\\ I$ が実効値なら $P=VI\\cos\\varphi$(最大値なら $\\frac12V_mI_m\\cos\\varphi$)。"),
              (unit((cos_deg(ph) * F(V * I, 2)).latex(), "W"), "$V,\\ I$ は実効値なので $\\frac12$ はいらない。")]
    return Problem("【電気】交流の電力", "基本",
                   rf"電圧 ${V}$ V、電流 ${I}$ A(ともに実効値)で、電流が電圧より ${ph}^\circ$ 遅れているとき、平均の電力(有効電力)を求めよ。",
                   assemble(unit(P.latex(), "W"), wrongs, value=float(P)),
                   hints=[r"積和の公式から、平均の電力は $P=VI\cos\varphi$($\cos\varphi$ が力率)。"],
                   solution=[rf"$$P=VI\cos\varphi={V}\times{I}\times\cos {ph}^\circ={P.latex()}\ \text{{W}}$$"], meta=dict(V=V, I=I, ph=ph))


# ============================================================
# 化学
# ============================================================
def g_molecule(rng):
    th, ans = rng.choice([(60, "a"), (90, r"\sqrt{2}\,a"), (120, r"\sqrt{3}\,a"), (180, "2a")])
    pool = {60: "a", 90: r"\sqrt{2}\,a", 120: r"\sqrt{3}\,a", 180: "2a"}
    wrongs = [(t, "余弦定理 $d^2=a^2+a^2-2a^2\\cos\\theta$ に代入しよう($\\cos 120^\\circ=-\\frac12$ など)。") for k, t in pool.items() if k != th]
    wrongs.append((r"\frac{\sqrt{3}}{2}a", "$d=2a\\sin\\frac{\\theta}{2}$。2 をかけ忘れていないか。"))
    return Problem("【化学】結合角と原子間の距離", "基本",
                   rf"中心の原子から 2 つの原子までの距離(結合距離)がともに $a$、結合角が ${th}^\circ$ のとき、2 つの原子の間の距離 $d$ を求めよ。",
                   assemble(ans, wrongs),
                   hints=[r"2 辺が $a$、間の角が $\theta$ の三角形に余弦定理:$d^2=a^2+a^2-2a\cdot a\cos\theta$。"],
                   solution=[rf"$$d^2=2a^2-2a^2\cos {th}^\circ={tex_fr(2 - 2 * (cos_deg(th).as_rational()))}a^2\quad\Rightarrow\quad d={ans}$$"],
                   meta=dict(th=th))


def g_bragg(rng):
    lam = rng.choice([F(15, 100), F(1, 10), F(2, 10), F(154, 1000)])
    n = rng.choice([1, 1, 2])
    th = rng.choice([30, 45, 60])
    d = float(n * lam) / (2 * float(sin_deg(th)))
    ans = unit(num(d, 3), "nm")
    wrongs = [(unit(num(float(n * lam) * 2 * float(sin_deg(th)), 3), "nm"), "$2d\\sin\\theta=n\\lambda$ を $d$ について解くと $d=\\dfrac{n\\lambda}{2\\sin\\theta}$。"),
              (unit(num(float(n * lam) / float(sin_deg(th)), 3), "nm"), "道のりの差は $2d\\sin\\theta$。2 を忘れていないか。"),
              (unit(num(float(n * lam) / (2 * float(cos_deg(th))), 3), "nm"), "$\\theta$ は X 線と原子の面のなす角。$\\cos$ ではなく $\\sin$。"),
              (unit(num(float(lam) / (2 * float(sin_deg(th))), 3), "nm") if n != 1 else unit(num(2 * d, 3), "nm"), "$n$ を確かめよう。")]
    return Problem("【化学】ブラッグの法則", "基本",
                   rf"波長 ${num(float(lam), 3)}$ nm の X 線を結晶に当てると、原子の面とのなす角 $\theta={th}^\circ$ で "
                   rf"$n={n}$ の強い反射が起きた。原子の面の間隔 $d$ を小数第 3 位まで求めよ。",
                   assemble(ans, wrongs, value=d),
                   hints=[r"ブラッグの法則 $2d\sin\theta=n\lambda$。"],
                   solution=[rf"$$d=\frac{{n\lambda}}{{2\sin\theta}}=\frac{{{n}\times{num(float(lam), 3)}}}{{2\sin {th}^\circ}}\approx{num(d, 3)}\ \text{{nm}}$$"],
                   meta=dict(lam=float(lam), n=n, th=th))


# ============================================================
# 都市
# ============================================================
def g_noon(rng):
    lat = rng.choice([26, 31, 34, 35, 36, 38, 43])
    season, dec = rng.choice([("夏至", F(234, 10)), ("春分", F(0)), ("冬至", F(-234, 10))])
    h = 90 - lat + dec
    tx = lambda x: num(float(x), 1)  # noqa: E731
    deg = lambda x: rf"{x}^\circ"  # noqa: E731
    wrongs = [(deg(tx(90 - lat - dec)) if dec != 0 else deg(tx(lat)), "夏至は $\\delta=+23.4^\\circ$(太陽が高い)、冬至は $-23.4^\\circ$。符号を確かめよう。"),
              (deg(tx(lat + dec)), "南中高度は $90^\\circ-\\varphi+\\delta$。"), (deg(tx(90 - lat)) if dec != 0 else deg(tx(90 + lat)), "季節による太陽の赤緯 $\\delta$ を足し忘れていないか。"),
              (deg(tx(180 - lat + dec)), "南中高度は $90^\\circ-\\varphi+\\delta$。")]
    return Problem("【都市】南中高度", "基本",
                   rf"北緯 ${lat}^\circ$ の地点での、{season}の日の太陽の南中高度を求めよ。太陽の赤緯は夏至 $+23.4^\circ$、春分 $0^\circ$、冬至 $-23.4^\circ$ とする。",
                   assemble(deg(tx(h)), wrongs, value=float(h)),
                   hints=[r"南中高度 $h=90^\circ-\varphi+\delta$($\varphi$:緯度、$\delta$:太陽の赤緯)。"],
                   solution=[rf"$$h=90^\circ-{lat}^\circ+({tx(dec)}^\circ)={tx(h)}^\circ$$"], meta=dict(lat=lat, dec=float(dec)))


def g_shadow(rng):
    H = rng.randint(2, 20)
    h = rng.choice([30, 45, 60])
    t = tan_deg(h)
    L = over_tan(H, h)
    wrongs = [(unit((t * H).latex(), "m") if h != 45 else unit(tex_root(2 * H * H), "m"), "影の長さ $L$ は $\\tan h=\\dfrac{H}{L}$ から $L=\\dfrac{H}{\\tan h}$。かけていないか。"),
              (unit((sin_deg(h) * H).latex(), "m"), "$\\tan h=\\dfrac{\\text{高さ}}{\\text{影の長さ}}$ を使う。"),
              (unit((cos_deg(h) * H).latex(), "m"), "$\\tan h=\\dfrac{\\text{高さ}}{\\text{影の長さ}}$ を使う。"),
              (unit(str(2 * H), "m"), "太陽の高さ $h$ の $\\tan$ を使おう。")]
    return Problem("【都市】影の長さ", "基本", rf"太陽の高さ(高度)が ${h}^\circ$ のとき、高さ ${H}$ m の建物の影の長さを求めよ。",
                   assemble(unit(L.latex(), "m"), wrongs, value=float(L)),
                   hints=[r"建物の高さ $H$、影の長さ $L$ と太陽の高さ $h$ の関係は $\tan h=\dfrac{H}{L}$。"],
                   solution=[rf"$$L=\frac{{H}}{{\tan h}}=\frac{{{H}}}{{{t.latex()}}}={L.latex()}\ \text{{m}}$$"], meta=dict(H=H, h=h))


def g_survey(rng):
    d = rng.choice([10, 12, 15, 20, 24, 30, 36, 40])
    th = rng.choice([30, 45, 60])
    e = rng.choice([1, 2])
    t = tan_deg(th)
    Hq = t * d + e
    wrongs = [((t * d).latex(), "目(器械)の高さ $e$ を足し忘れていないか。"),
              ((sin_deg(th) * d + e).latex(), "$\\tan\\theta=\\dfrac{\\text{高さの差}}{\\text{水平距離}}$。$\\sin$ ではない。"),
              ((over_tan(d, th) + e).latex() if th != 45 else (Q236(d) * 2 + e).latex(), "$\\tan\\theta=\\dfrac{\\text{高さの差}}{d}$ から、高さの差 $=d\\tan\\theta$。割っていないか。"),
              ((cos_deg(th) * d + e).latex(), "$\\tan$ を使う。")]
    return Problem("【都市】仰角で高さを測る", "基本",
                   rf"建物から水平に ${d}$ m はなれた所で、高さ ${e}$ m の目(器械)から屋上を見上げた角(仰角)が ${th}^\circ$ だった。建物の高さ [m] を求めよ。",
                   assemble(Hq.latex(), wrongs, value=float(Hq)),
                   hints=[r"高さの差 $=d\tan\theta$。最後に目の高さ $e$ を足す。"],
                   solution=[rf"$$H=d\tan\theta+e={d}\tan {th}^\circ+{e}={Hq.latex()}$$"], meta=dict(d=d, th=th, e=e))


def g_slope(rng):
    kind = rng.choice(["rise", "percent"])
    if kind == "rise":
        p = rng.choice([2, 4, 5, 8, 10, 12])
        Lh = rng.choice([50, 100, 150, 200, 250])
        ans = unit(num(Lh * p / 100, 1), "m")
        wrongs = [(unit(num(Lh * p / 1000, 2), "m"), "% は 100 m あたり。‰(1000 m あたり)と混ざっていないか。"), (unit(str(p), "m"), "水平距離をかけよう。"),
                  (unit(num(Lh / p, 1), "m"), "高さ $=$ 水平距離 $\\times\\tan\\theta=$ 水平距離 $\\times\\dfrac{p}{100}$。"), (unit(num(Lh * p / 10, 1), "m"), "$p$ % は $\\dfrac{p}{100}$。")]
        st = rf"勾配 ${p}$ % の坂を、水平距離で ${Lh}$ m 進んだ。何 m 上がったか。"
        sol = [rf"$$\text{{高さ}}={Lh}\times\frac{{{p}}}{{100}}={num(Lh * p / 100, 1)}\ \text{{m}}$$"]
        val = Lh * p / 100
    else:
        n = rng.choice([8, 10, 12, 15, 20])
        ans = unit(num(100 / n, 1), "\\%")
        wrongs = [(unit(str(n), "\\%"), "比 $1:n$ は、高さ 1 に対して水平が $n$。勾配は $\\dfrac1n\\times100$ %。"),
                  (unit(num(1000 / n, 1), "\\%"), "それは ‰(パーミル)の値。"), (unit(num(1 / n, 3), "\\%"), "100 をかけて % にする。"),
                  (unit(num(100 / (n + 1), 1), "\\%"), "勾配は 高さ ÷ 水平距離。")]
        st = rf"高さ 1 に対して水平距離 ${n}$ の割合($1/{n}$)のスロープの勾配は何 % か(小数第 1 位まで)。"
        sol = [rf"$$\frac{{1}}{{{n}}}\times100\approx{num(100 / n, 1)}\ \%$$"]
        val = 100 / n
    return Problem("【都市】勾配", "基本", st, assemble(ans, wrongs, value=val),
                   hints=[r"勾配 $\tan\theta=\dfrac{\text{高さ}}{\text{水平距離}}$。% は $100\tan\theta$、‰ は $1000\tan\theta$。"],
                   solution=sol, meta=dict(kind=kind))


REGISTRY = [
    ProblemType("ferris", "【共通】観覧車の高さ", "基本", g_ferris),
    ProblemType("rpm", "【機械】回転数と角速度", "基本", g_rpm),
    ProblemType("gear", "【機械】歯車の回転数", "基本", g_gear),
    ProblemType("friction", "【機械】摩擦角", "基本", g_friction),
    ProblemType("ac_peak", "【電気】交流の最大値と実効値", "基本", g_ac_peak),
    ProblemType("ac_omega", "【電気】交流の周期・角周波数", "基本", g_ac_omega),
    ProblemType("three", "【電気】三相交流の線間電圧", "基本", g_three_phase),
    ProblemType("power", "【電気】交流の電力", "基本", g_power),
    ProblemType("molecule", "【化学】結合角と原子間の距離", "基本", g_molecule),
    ProblemType("bragg", "【化学】ブラッグの法則", "基本", g_bragg),
    ProblemType("noon", "【都市】南中高度", "基本", g_noon),
    ProblemType("shadow", "【都市】影の長さ", "基本", g_shadow),
    ProblemType("survey", "【都市】仰角で高さを測る", "基本", g_survey),
    ProblemType("slope", "【都市】勾配", "基本", g_slope),
    ProblemType("ferris_t", "【共通】観覧車で高い所にいる時間", "標準", g_ferris_time),
    ProblemType("crank", "【機械】ピストンの位置(余弦定理)", "標準", g_crank),
]

TITLE = "学科別の応用"


def tab():
    render("applied", REGISTRY, TITLE)
