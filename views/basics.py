"""三角比・三角関数の基礎知識まとめ（有名角・ラジアン・扇形・相互関係・正弦/余弦定理・加法定理と派生公式）"""

import math
from fractions import Fraction as F

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.angles import deg_text, pi_latex, pi_text
from utils.exact import Q236, cos_deg, sin_deg, tan_deg
from utils.formulas import FORMULAS, GROUPS, triangle_from_sas

FAMOUS = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
C_SIN, C_COS, C_TAN, C_R = "#ff7f0e", "#2ca02c", "#9467bd", "#1f77b4"


def val_tex(q):
    """課題と同じ書き方（1/√2, 1/√3）で表示"""
    if q is None:
        return r"\text{なし}"
    special = {Q236.sqrt_of(2, F(1, 2)): r"\frac{1}{\sqrt{2}}", Q236.sqrt_of(3, F(1, 3)): r"\frac{1}{\sqrt{3}}"}
    for v, s in special.items():
        if q == v:
            return s
        if q == -v:
            return "-" + s
    return q.latex()


def rad_tex(d):
    return pi_latex(F(d, 180))


def quadrant(d):
    d %= 360
    if d % 90 == 0:
        return "軸上"
    return f"第{d // 90 + 1}象限"


st.title("三角比・三角関数の基礎知識まとめ")
st.markdown("三角関数の単元で使う定義と公式を 1 ページにまとめました。図は値を変えると動きます。"
            "公式は「⑥ 数値で確かめる」で、好きな角を入れて両辺が等しくなることを確かめられます。")

tabs = st.tabs(["① 有名角と三角関数の値", "② ラジアンと扇形", "③ 三角比と相互関係", "④ 正弦定理・余弦定理",
                "⑤ 加法定理とそこから導く公式", "⑥ 数値で確かめる"])

# =====================================================================
# ① 有名角
# =====================================================================
with tabs[0]:
    st.markdown("#### 60分法（度数法）と弧度法")
    st.latex(r"180^\circ = \pi\ \text{rad},\qquad x^\circ = x\times\frac{\pi}{180}\ \text{rad},\qquad"
             r"\theta\ \text{rad} = \theta\times\frac{180^\circ}{\pi}")
    st.markdown("#### 有名角の三角関数の値")
    head = "| 度 | " + " | ".join(f"${d}^\\circ$" for d in FAMOUS[:9]) + " |\n|:--|" + ":--:|" * 9 + "\n"
    head2 = "| 度 | " + " | ".join(f"${d}^\\circ$" for d in FAMOUS[9:]) + " |\n|:--|" + ":--:|" * 8 + "\n"

    def rows(ds):
        return ("| 弧度 | " + " | ".join(f"${rad_tex(d)}$" for d in ds) + " |\n"
                "| $\\sin$ | " + " | ".join(f"${val_tex(sin_deg(d))}$" for d in ds) + " |\n"
                "| $\\cos$ | " + " | ".join(f"${val_tex(cos_deg(d))}$" for d in ds) + " |\n"
                "| $\\tan$ | " + " | ".join(f"${val_tex(tan_deg(d))}$" for d in ds) + " |\n")
    st.markdown(head + rows(FAMOUS[:9]))
    st.markdown(head2 + rows(FAMOUS[9:]))
    st.caption("1/√2 = √2/2、1/√3 = √3/3（分母を有理化した形）。tan の「なし」は、cos = 0 で定義されないことを表す。")

    st.markdown("#### 単位円で見る")
    c1, c2 = st.columns([3, 2])
    with c2:
        d = st.select_slider("角 θ", options=list(range(-360, 721, 15)), value=150, key="bs_deg",
                             format_func=lambda v: f"{v}°（{pi_text(F(v, 180))}）")
        s, c, t = sin_deg(d), cos_deg(d), tan_deg(d)
        st.latex(rf"\theta = {d}^\circ = {rad_tex(d)}")
        st.latex(rf"\sin\theta = {val_tex(s)},\quad \cos\theta = {val_tex(c)}")
        st.latex(rf"\tan\theta = {val_tex(t) if t is not None else r'\text{定義されない}'}")
        if d % 360 != d:
            st.caption(f"{d}° は {d % 360}° と同じ位置（2π の整数倍ずれた角は動径が同じ）。")
        st.markdown(f"動径は **{quadrant(d)}**")
        st.caption("cos θ = 点 P の x 座標（緑）、sin θ = y 座標（橙）、tan θ = 直線 OP と直線 x = 1 の交点の y 座標（紫）。")
    with c1:
        th = math.radians(d)
        cx, sy = math.cos(th), math.sin(th)
        fig = go.Figure()
        u = np.linspace(0, 2 * np.pi, 200)
        fig.add_trace(go.Scatter(x=np.cos(u), y=np.sin(u), mode="lines", line=dict(color="#bbbbbb"), hoverinfo="skip",
                                 showlegend=False))
        arc = np.linspace(0, th, 100)
        fig.add_trace(go.Scatter(x=0.22 * np.cos(arc), y=0.22 * np.sin(arc), mode="lines", line=dict(color="black", width=1.5),
                                 hoverinfo="skip", showlegend=False))
        if t is not None and abs(float(t)) < 3:
            tv = float(t)
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, tv], mode="lines", line=dict(color=C_TAN, dash="dot"),
                                     hoverinfo="skip", showlegend=False))
            fig.add_trace(go.Scatter(x=[1, 1], y=[0, tv], mode="lines", name="tan θ", line=dict(color=C_TAN, width=4)))
        fig.add_trace(go.Scatter(x=[0, cx], y=[0, 0], mode="lines", name="cos θ", line=dict(color=C_COS, width=5)))
        fig.add_trace(go.Scatter(x=[cx, cx], y=[0, sy], mode="lines", name="sin θ", line=dict(color=C_SIN, width=5)))
        fig.add_trace(go.Scatter(x=[0, cx], y=[0, sy], mode="lines+markers", name="動径 OP（長さ 1）",
                                 line=dict(color=C_R, width=3), marker=dict(size=[0, 12])))
        fig.add_annotation(x=cx, y=sy, text=f"P({c.text()}, {s.text()})", showarrow=False,
                           xshift=55 if cx >= 0 else -55, yshift=14 if sy >= 0 else -14)
        fig.add_vline(x=1, line_color="#dddddd", line_dash="dash")
        fig.update_layout(height=470, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                          legend=dict(orientation="h", y=1.08))
        fig.update_xaxes(range=[-1.5, 1.7], zeroline=True, zerolinecolor="black", dtick=0.5)
        fig.update_yaxes(range=[-1.5, 1.5], zeroline=True, zerolinecolor="black", dtick=0.5, scaleanchor="x", scaleratio=1)
        st.plotly_chart(fig, key="bs_unit")

# =====================================================================
# ② ラジアンと扇形
# =====================================================================
with tabs[1]:
    st.markdown("#### ラジアン（弧度）の定義")
    st.markdown("半径 r の円で、**半径と同じ長さの弧** に対する中心角を **1 ラジアン** という。"
                "半径の大きさによらず同じ角になる。円周は 2πr なので、1 周 360° は 2π ラジアン。")
    st.latex(r"1\ \text{rad} = \frac{180^\circ}{\pi} \approx 57.3^\circ,\qquad 360^\circ = 2\pi\ \text{rad}")
    st.markdown("#### 扇形の弧の長さと面積（中心角 θ はラジアン）")
    st.latex(r"\ell = r\theta,\qquad S = \frac{1}{2}r^2\theta = \frac{1}{2}r\ell")
    c1, c2 = st.columns([2, 3])
    with c1:
        r = st.slider("半径 r", 1.0, 5.0, 3.0, 0.5, key="bs_r")
        k = st.select_slider("中心角 θ", options=list(range(1, 25)), value=4, key="bs_th",
                             format_func=lambda v: f"{pi_text(F(v, 12))}（{deg_text(F(v, 12))}）")
        theta = k * math.pi / 12
        show_unit = st.checkbox("1 ラジアン（弧の長さ = 半径）を表示", value=True, key="bs_1rad")
        q = F(k, 12)
        st.latex(rf"\ell = {r:g}\times {pi_latex(q)} \approx {r * theta:.3f}")
        st.latex(rf"S = \frac{{1}}{{2}}\times {r:g}^2 \times {pi_latex(q)} \approx {0.5 * r * r * theta:.3f}")
        st.caption("円全体（θ = 2π）なら ℓ = 2πr（円周）、S = πr²（円の面積）になる。")
    with c2:
        u = np.linspace(0, theta, 200)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=np.concatenate([[0], r * np.cos(u), [0]]), y=np.concatenate([[0], r * np.sin(u), [0]]),
                                  fill="toself", fillcolor="rgba(31,119,180,0.18)", line=dict(color=C_R, width=1.5),
                                  name=f"扇形 S ≈ {0.5 * r * r * theta:.2f}"))
        fig2.add_trace(go.Scatter(x=r * np.cos(u), y=r * np.sin(u), mode="lines", line=dict(color=C_SIN, width=5),
                                  name=f"弧 ℓ ≈ {r * theta:.2f}"))
        if show_unit:
            u1 = np.linspace(0, 1, 60)
            fig2.add_trace(go.Scatter(x=(r + 0.35) * np.cos(u1), y=(r + 0.35) * np.sin(u1), mode="lines",
                                      line=dict(color=C_TAN, width=3), name="長さ r の弧 → 1 ラジアン"))
            fig2.add_trace(go.Scatter(x=[0, (r + 0.35) * math.cos(1)], y=[0, (r + 0.35) * math.sin(1)], mode="lines",
                                      line=dict(color=C_TAN, dash="dot"), showlegend=False, hoverinfo="skip"))
        lim = r + 0.8
        fig2.update_layout(height=430, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                           legend=dict(orientation="h", y=1.1))
        fig2.update_xaxes(range=[-lim, lim], zeroline=True, zerolinecolor="black")
        fig2.update_yaxes(range=[-lim, lim], zeroline=True, zerolinecolor="black", scaleanchor="x", scaleratio=1)
        st.plotly_chart(fig2, key="bs_sector")

# =====================================================================
# ③ 三角比と相互関係
# =====================================================================
with tabs[2]:
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**直角三角形での定義（三角比）**")
        st.latex(r"\sin\theta = \frac{\text{対辺}}{\text{斜辺}},\quad \cos\theta = \frac{\text{隣辺}}{\text{斜辺}},\quad"
                 r"\tan\theta = \frac{\text{対辺}}{\text{隣辺}}")
        st.caption("0° < θ < 90° のときに使える定義。")
    with c2, st.container(border=True):
        st.markdown("**座標での定義（一般角の三角関数）**")
        st.latex(r"\sin\theta = \frac{y}{r},\quad \cos\theta = \frac{x}{r},\quad \tan\theta = \frac{y}{x}")
        st.caption("動径上の点 (x, y)、r = √(x² + y²)。どんな角でも使える。x = 0 のとき tan は定義されない。")
    st.markdown("#### 符号（動径がどの象限にあるか）")
    st.markdown("| | 第1象限 | 第2象限 | 第3象限 | 第4象限 |\n|:--:|:--:|:--:|:--:|:--:|\n"
                "| sin | ＋ | ＋ | − | − |\n| cos | ＋ | − | − | ＋ |\n| tan | ＋ | − | ＋ | − |")
    st.markdown("#### 相互関係")
    st.latex(r"\tan\theta = \frac{\sin\theta}{\cos\theta},\qquad \sin^2\theta + \cos^2\theta = 1,\qquad 1 + \tan^2\theta = \frac{1}{\cos^2\theta}")
    with st.expander("導き方"):
        st.markdown(r"- 単位円上の点 $(\cos\theta, \sin\theta)$ と原点の距離は 1。三平方の定理から $\cos^2\theta + \sin^2\theta = 1$。")
        st.markdown(r"- 両辺を $\cos^2\theta$ で割ると $1 + \tan^2\theta = \dfrac{1}{\cos^2\theta}$。")
        st.markdown(r"- 1 つの値（例：$\sin\theta$）と象限が分かれば、残りの値がすべて求められる。")
    st.markdown("#### 角の変換公式")
    for f in [f for f in FORMULAS if f["group"] == "角の変換"]:
        st.latex(f["tex"])
    st.markdown("#### グラフの性質")
    st.markdown(
        "| | y = sin θ | y = cos θ | y = tan θ |\n|:--:|:--:|:--:|:--:|\n"
        "| 周期 | 2π | 2π | π |\n| 値域 | −1 ≤ y ≤ 1 | −1 ≤ y ≤ 1 | すべての実数 |\n"
        "| 対称性 | 原点対称（奇関数） | y 軸対称（偶関数） | 原点対称（奇関数） |\n"
        "| y = A sin B(θ − p) + q | 振幅 \\|A\\|、周期 2π/\\|B\\| | ← 同じ | 周期 π/\\|B\\| |"
    )
    st.page_link("views/general_form.py", label="グラフの変形は「一般形」のページで", icon="🌊")

# =====================================================================
# ④ 正弦定理・余弦定理
# =====================================================================
with tabs[3]:
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**正弦定理**（R は外接円の半径）")
        st.latex(r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R")
    with c2, st.container(border=True):
        st.markdown("**余弦定理**")
        st.latex(r"a^2 = b^2 + c^2 - 2bc\cos A,\qquad \cos A = \frac{b^2 + c^2 - a^2}{2bc}")
    st.markdown("**三角形の面積**")
    st.latex(r"S = \frac{1}{2}bc\sin A = \frac{1}{2}ca\sin B = \frac{1}{2}ab\sin C")
    st.markdown("##### 2 辺とその間の角から三角形を決める")
    c1, c2 = st.columns([2, 3])
    with c1:
        b = st.slider("辺 b（= CA）", 1.0, 8.0, 4.0, 0.5, key="bs_b")
        c = st.slider("辺 c（= AB）", 1.0, 8.0, 5.0, 0.5, key="bs_c")
        A = st.slider("角 A [°]", 10, 170, 60, 5, key="bs_A")
        tr = triangle_from_sas(b, c, A)
        st.latex(rf"a = \sqrt{{{b:g}^2 + {c:g}^2 - 2\cdot {b:g}\cdot {c:g}\cos {A}^\circ}} \approx {tr['a']:.3f}")
        st.latex(rf"B \approx {tr['B']:.2f}^\circ,\quad C \approx {tr['C']:.2f}^\circ")
        st.latex(rf"2R = \frac{{a}}{{\sin A}} \approx {2 * tr['R']:.3f},\quad S = \frac{{1}}{{2}}bc\sin A \approx {tr['S']:.3f}")
        st.caption(f"確認：b / sin B ≈ {b / math.sin(math.radians(tr['B'])):.3f}、"
                   f"c / sin C ≈ {c / math.sin(math.radians(tr['C'])):.3f}（どれも 2R と等しい）")
    with c2:
        Ar = math.radians(A)
        PA, PB, PC = (0.0, 0.0), (c, 0.0), (b * math.cos(Ar), b * math.sin(Ar))
        # 外心
        ax_, ay_ = PA
        bx_, by_ = PB
        cx_, cy_ = PC
        dd = 2 * (ax_ * (by_ - cy_) + bx_ * (cy_ - ay_) + cx_ * (ay_ - by_))
        ox = ((ax_**2 + ay_**2) * (by_ - cy_) + (bx_**2 + by_**2) * (cy_ - ay_) + (cx_**2 + cy_**2) * (ay_ - by_)) / dd
        oy = ((ax_**2 + ay_**2) * (cx_ - bx_) + (bx_**2 + by_**2) * (ax_ - cx_) + (cx_**2 + cy_**2) * (bx_ - ax_)) / dd
        R = tr["R"]
        u = np.linspace(0, 2 * np.pi, 200)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ox + R * np.cos(u), y=oy + R * np.sin(u), mode="lines", name=f"外接円（R ≈ {R:.2f}）",
                                  line=dict(color="#bbbbbb", dash="dot")))
        fig3.add_trace(go.Scatter(x=[PA[0], PB[0], PC[0], PA[0]], y=[PA[1], PB[1], PC[1], PA[1]], fill="toself",
                                  fillcolor="rgba(31,119,180,0.12)", line=dict(color=C_R, width=3), name="三角形 ABC"))
        for (px, py), lab in [(PA, "A"), (PB, "B"), (PC, "C")]:
            fig3.add_annotation(x=px, y=py, text=f"<b>{lab}</b>", showarrow=False,
                                xshift=-12 if px < ox else 12, yshift=-12 if py < oy else 12, font=dict(size=16))
        for (p1, p2), lab in [((PB, PC), f"a ≈ {tr['a']:.2f}"), ((PC, PA), f"b = {b:g}"), ((PA, PB), f"c = {c:g}")]:
            fig3.add_annotation(x=(p1[0] + p2[0]) / 2, y=(p1[1] + p2[1]) / 2, text=lab, showarrow=False,
                                font=dict(color=C_R), bgcolor="rgba(255,255,255,0.7)")
        xs = [PA[0], PB[0], PC[0], ox - R, ox + R]
        ys = [PA[1], PB[1], PC[1], oy - R, oy + R]
        span = max(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 0.6
        mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        fig3.update_layout(height=440, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                           legend=dict(orientation="h", y=1.08))
        fig3.update_xaxes(range=[mx - span, mx + span], showgrid=False, zeroline=False)
        fig3.update_yaxes(range=[my - span, my + span], showgrid=False, zeroline=False, scaleanchor="x", scaleratio=1)
        st.plotly_chart(fig3, key="bs_triangle")
    st.caption("A = 90° にすると余弦定理は三平方の定理 a² = b² + c² になる（cos 90° = 0）。")

# =====================================================================
# ⑤ 加法定理とそこから導く公式
# =====================================================================
with tabs[4]:
    def show(group):
        for f in FORMULAS:
            if f["group"] == group:
                st.latex(f["tex"])

    st.markdown("#### 加法定理（すべての公式のもと）")
    show("加法定理")
    st.markdown("#### 2倍角の公式")
    show("2倍角")
    with st.expander("導き方"):
        st.markdown(r"加法定理で $\beta = \alpha$ とおく。cos 2α の 3 つの形は $\sin^2\alpha + \cos^2\alpha = 1$ で書きかえたもの。")
    st.markdown("#### 3倍角の公式")
    show("3倍角")
    with st.expander("導き方"):
        st.latex(r"\sin 3\alpha = \sin(2\alpha + \alpha) = \sin 2\alpha\cos\alpha + \cos 2\alpha\sin\alpha"
                 r" = 2\sin\alpha\cos^2\alpha + (1 - 2\sin^2\alpha)\sin\alpha")
        st.latex(r"= 2\sin\alpha(1 - \sin^2\alpha) + \sin\alpha - 2\sin^3\alpha = 3\sin\alpha - 4\sin^3\alpha")
    st.markdown("#### 半角の公式")
    show("半角")
    with st.expander("導き方"):
        st.markdown(r"$\cos 2\theta = 1 - 2\sin^2\theta = 2\cos^2\theta - 1$ で $\theta = \dfrac{\alpha}{2}$ とおいて変形する。"
                    r"平方根をとるときは $\dfrac{\alpha}{2}$ の範囲から符号を決める。")
    st.markdown("#### 三角関数の合成")
    show("合成")
    st.page_link("views/synthesis.py", label="図とアニメーションは「三角関数の合成」のページで", icon="🧭")
    st.markdown("#### 積 → 和の公式")
    show("積→和")
    st.markdown("#### 和 → 積の公式")
    show("和→積")
    st.page_link("views/product_sum.py", label="導き方と数値の確認は「積和・和積の公式」のページで", icon="🔀")
    with st.expander("公式どうしのつながり"):
        st.markdown(
            "- **加法定理** → β = α とおく → **2倍角** → さらに α を足す → **3倍角**\n"
            "- **2倍角（cos 2α）** → 変形 → **半角**\n"
            "- **加法定理** を 2 つたす・ひく → **積→和** → 角をおきかえる → **和→積**\n"
            "- **加法定理** を逆向きに使う → **合成**"
        )

# =====================================================================
# ⑥ 数値で確かめる
# =====================================================================
with tabs[5]:
    st.markdown("公式を選び、角を入れて **左辺と右辺の値が等しくなる** ことを確かめよう。")
    g = st.selectbox("分類", GROUPS, key="bs_group")
    flist = [f for f in FORMULAS if f["group"] == g]
    names = [f["name"] for f in flist]
    nm = st.radio("公式", names, horizontal=True, key=f"bs_f_{g}")
    f = flist[names.index(nm)]
    st.latex(f["tex"])
    c1, c2 = st.columns(2)
    da = c1.slider("α（A）[°]", -360, 360, 50, 1, key="bs_a")
    db = c2.slider("β（B）[°]", -360, 360, 20, 1, key="bs_bb") if f["vars"] == 2 else 0
    ar, br = math.radians(da), math.radians(db)
    try:
        lv, rv = f["lhs"](ar, br), f["rhs"](ar, br)
        big = max(abs(lv), abs(rv)) > 1e8
    except ZeroDivisionError:
        lv = rv = None
        big = True
    if big:
        st.warning("この角では tan や分母が定義されない（0 で割ることになる）ので、別の角で試してください。")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("左辺", f"{lv:.10f}")
        m2.metric("右辺", f"{rv:.10f}")
        m3.metric("差", f"{abs(lv - rv):.2e}")
        if abs(lv - rv) < 1e-9 * max(1, abs(lv)):
            st.success("左辺と右辺が一致しました（差は計算機の丸め誤差だけ）。")
    if f["group"] == "合成":
        st.caption("合成は a = √3, b = 1 の例（√3 sin α + cos α = 2 sin(α + 30°)）で確かめています。")
    if f["group"] == "角の変換":
        st.caption("角の変換公式は、表示した式のうち 1 つ（sin か cos）を確かめています。")
