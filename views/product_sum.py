"""三角関数の積和公式・和積公式（後期課題8 対応）"""

from fractions import Fraction as F

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.exact import Q236, cos_deg, is_nice_deg, sin_deg
from utils.plotting import COLORS, curve, style_axes, x_grid

# =====================================================================
# 公式の定義
#   左辺・右辺を ("prod", 係数, f1, 角1, f2, 角2) または ("sum", 係数, [(符号, f, 角), ...]) で表す。
#   角は x, y（度）から計算する式の名前。
# =====================================================================
ANG = {
    "x": lambda x, y: x, "y": lambda x, y: y,
    "x+y": lambda x, y: x + y, "x-y": lambda x, y: x - y,
    "(x+y)/2": lambda x, y: (x + y) / 2, "(x-y)/2": lambda x, y: (x - y) / 2,
}
FORMULAS = {
    "sc": dict(group="積→和", lhs=("prod", 1, "sin", "x", "cos", "y"),
               rhs=("sum", F(1, 2), [(1, "sin", "x+y"), (1, "sin", "x-y")]),
               tex=r"\sin\alpha\cos\beta = \frac{1}{2}\{\sin(\alpha+\beta) + \sin(\alpha-\beta)\}"),
    "cs": dict(group="積→和", lhs=("prod", 1, "cos", "x", "sin", "y"),
               rhs=("sum", F(1, 2), [(1, "sin", "x+y"), (-1, "sin", "x-y")]),
               tex=r"\cos\alpha\sin\beta = \frac{1}{2}\{\sin(\alpha+\beta) - \sin(\alpha-\beta)\}"),
    "cc": dict(group="積→和", lhs=("prod", 1, "cos", "x", "cos", "y"),
               rhs=("sum", F(1, 2), [(1, "cos", "x+y"), (1, "cos", "x-y")]),
               tex=r"\cos\alpha\cos\beta = \frac{1}{2}\{\cos(\alpha+\beta) + \cos(\alpha-\beta)\}"),
    "ss": dict(group="積→和", lhs=("prod", 1, "sin", "x", "sin", "y"),
               rhs=("sum", F(-1, 2), [(1, "cos", "x+y"), (-1, "cos", "x-y")]),
               tex=r"\sin\alpha\sin\beta = -\frac{1}{2}\{\cos(\alpha+\beta) - \cos(\alpha-\beta)\}"),
    "s+s": dict(group="和→積", lhs=("sum", 1, [(1, "sin", "x"), (1, "sin", "y")]),
                rhs=("prod", 2, "sin", "(x+y)/2", "cos", "(x-y)/2"),
                tex=r"\sin A + \sin B = 2\sin\frac{A+B}{2}\cos\frac{A-B}{2}"),
    "s-s": dict(group="和→積", lhs=("sum", 1, [(1, "sin", "x"), (-1, "sin", "y")]),
                rhs=("prod", 2, "cos", "(x+y)/2", "sin", "(x-y)/2"),
                tex=r"\sin A - \sin B = 2\cos\frac{A+B}{2}\sin\frac{A-B}{2}"),
    "c+c": dict(group="和→積", lhs=("sum", 1, [(1, "cos", "x"), (1, "cos", "y")]),
                rhs=("prod", 2, "cos", "(x+y)/2", "cos", "(x-y)/2"),
                tex=r"\cos A + \cos B = 2\cos\frac{A+B}{2}\cos\frac{A-B}{2}"),
    "c-c": dict(group="和→積", lhs=("sum", 1, [(1, "cos", "x"), (-1, "cos", "y")]),
                rhs=("prod", -2, "sin", "(x+y)/2", "sin", "(x-y)/2"),
                tex=r"\cos A - \cos B = -2\sin\frac{A+B}{2}\sin\frac{A-B}{2}"),
}
PAIR = {"sc": "s+s", "cs": "s-s", "cc": "c+c", "ss": "c-c"}  # 積→和 と 和→積 の対応

# 加法定理からの導き方
DERIVE = {
    "sc": (r"\sin(\alpha+\beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta",
           r"\sin(\alpha-\beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta",
           "辺々 **たす** と、$\\cos\\alpha\\sin\\beta$ が消える",
           r"\sin(\alpha+\beta) + \sin(\alpha-\beta) = 2\sin\alpha\cos\beta"),
    "cs": (r"\sin(\alpha+\beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta",
           r"\sin(\alpha-\beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta",
           "辺々 **ひく** と、$\\sin\\alpha\\cos\\beta$ が消える",
           r"\sin(\alpha+\beta) - \sin(\alpha-\beta) = 2\cos\alpha\sin\beta"),
    "cc": (r"\cos(\alpha+\beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta",
           r"\cos(\alpha-\beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta",
           "辺々 **たす** と、$\\sin\\alpha\\sin\\beta$ が消える",
           r"\cos(\alpha+\beta) + \cos(\alpha-\beta) = 2\cos\alpha\cos\beta"),
    "ss": (r"\cos(\alpha+\beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta",
           r"\cos(\alpha-\beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta",
           "辺々 **ひく** と、$\\cos\\alpha\\cos\\beta$ が消える（**符号に注意**）",
           r"\cos(\alpha+\beta) - \cos(\alpha-\beta) = -2\sin\alpha\sin\beta"),
}


# =====================================================================
# 値の計算（15° の倍数なら厳密、そうでなければ小数）
# =====================================================================
def fval(func, deg):
    if is_nice_deg(deg):
        return sin_deg(deg) if func == "sin" else cos_deg(deg)
    return float(np.sin(np.radians(float(deg))) if func == "sin" else np.cos(np.radians(float(deg))))


def evaluate(side, x, y):
    if side[0] == "prod":
        _, k, f1, a1, f2, a2 = side
        v1, v2 = fval(f1, ANG[a1](x, y)), fval(f2, ANG[a2](x, y))
        if isinstance(v1, Q236) and isinstance(v2, Q236):
            return v1 * v2 * k
        return float(v1) * float(v2) * float(k)
    _, k, terms = side
    vals = [sg * fval(f, ANG[a](x, y)) for sg, f, a in terms]
    if all(isinstance(v, Q236) for v in vals):
        return (vals[0] + vals[1]) * k
    return float(k) * sum(float(v) for v in vals)


def deg_tex(d):
    d = F(d)
    s = str(d.numerator) if d.denominator == 1 else f"{float(d):g}"
    return rf"{s}^\circ"


def fn_tex(f, d):
    d = F(d)
    return rf"\{f} {deg_tex(d)}" if d >= 0 else rf"\{f}({deg_tex(d)})"


def coef_tex(k):
    k = F(k)
    if k == 1:
        return ""
    if k == -1:
        return "-"
    if k.denominator == 1:
        return str(k.numerator)
    return ("-" if k < 0 else "") + rf"\frac{{{abs(k.numerator)}}}{{{k.denominator}}}"


def side_tex(side, x, y, values=False):
    """values=False: sin 37.5° などの式、True: 値を代入した式"""
    def one(f, d):
        if values:
            v = fval(f, d)
            if isinstance(v, Q236):
                t = v.latex()
                return f"\\left({t}\\right)" if (" " in t or t.startswith("-")) else t
            return f"{v:.6f}"
        return fn_tex(f, d)

    if side[0] == "prod":
        _, k, f1, a1, f2, a2 = side
        sep = r" \cdot " if values else ""
        c = coef_tex(k)
        if values and c not in ("", "-"):
            c += r" \cdot "
        return c + one(f1, ANG[a1](x, y)) + sep + one(f2, ANG[a2](x, y))
    _, k, terms = side
    body = ""
    for i, (sg, f, a) in enumerate(terms):
        t = one(f, ANG[a](x, y))
        body += (("-" if sg < 0 else "") if i == 0 else (" - " if sg < 0 else " + ")) + t
    return body if k == 1 else rf"{coef_tex(k)}\left\{{{body}\right\}}"


def value_tex(v):
    return v.latex() if isinstance(v, Q236) else rf"\approx {v:.6f}"


# =====================================================================
# 画面
# =====================================================================
st.title("積和公式・和積公式")
st.markdown("加法定理を **たしたり・ひいたり** するだけで作れる公式です。"
            "「積 → 和」は **½**、「和 → 積」は **2** がつくことと、**cos − cos だけマイナス** がつくことに注目しよう。")

c1, c2 = st.columns(2)
with c1, st.container(border=True):
    st.markdown("**積 → 和**（かけ算をたし算に直す）")
    for k in ("sc", "cs", "cc", "ss"):
        st.latex(FORMULAS[k]["tex"])
with c2, st.container(border=True):
    st.markdown("**和 → 積**（たし算をかけ算に直す）")
    for k in ("s+s", "s-s", "c+c", "c-c"):
        st.latex(FORMULAS[k]["tex"])

tab1, tab2, tab3, tab4 = st.tabs(["① 加法定理から導く", "② 数値で確かめる", "③ グラフで見る（うなり）", "④ 類題と解き方"])

# ---------------- ① 導き方 ----------------
with tab1:
    LABEL = {"sc": "sin α cos β", "cs": "cos α sin β", "cc": "cos α cos β", "ss": "sin α sin β"}
    key = st.radio("導く公式", list(DERIVE), horizontal=True, format_func=lambda k: LABEL[k], key="ps_derive")
    e1, e2, how, res = DERIVE[key]
    st.markdown("**手順1** 加法定理を 2 つ並べる")
    st.latex(e1)
    st.latex(e2)
    st.markdown(f"**手順2** {how}")
    st.latex(res)
    st.markdown("**手順3** 両辺を 2 で割る → **積 → 和** の公式")
    st.latex(FORMULAS[key]["tex"])
    st.markdown(r"**手順4** $\alpha + \beta = A,\ \alpha - \beta = B$ とおくと "
                r"$\alpha = \dfrac{A+B}{2},\ \beta = \dfrac{A-B}{2}$。代入して両辺を 2 倍 → **和 → 積** の公式")
    st.latex(FORMULAS[PAIR[key]]["tex"])
    st.caption("公式を忘れても、加法定理から 1 分で作り直せる。丸暗記より「作り方」を覚えよう。")

# ---------------- ② 数値で確かめる ----------------
with tab2:
    EXAMPLES = {
        "自由に設定": None,
        "sin 52.5° cos 7.5°（積 → 和）": ("sc", F(105, 2), F(15, 2)),
        "sin 75° sin 15°（積 → 和）": ("ss", F(75), F(15)),
        "cos 82.5° cos 37.5°（積 → 和）": ("cc", F(165, 2), F(75, 2)),
        "sin 105° + sin 15°（和 → 積）": ("s+s", F(105), F(15)),
        "cos 105° − cos 15°（和 → 積）": ("c-c", F(105), F(15)),
        "sin 165° − sin 75°（和 → 積）": ("s-s", F(165), F(75)),
    }
    st.session_state.setdefault("ps_f", "sc")
    st.session_state.setdefault("ps_x", F(105, 2))
    st.session_state.setdefault("ps_y", F(15, 2))

    def apply_example():
        ex = EXAMPLES[st.session_state["ps_ex"]]
        if ex:
            st.session_state["ps_f"], st.session_state["ps_x"], st.session_state["ps_y"] = ex

    st.selectbox("例を読み込む", list(EXAMPLES), key="ps_ex", on_change=apply_example)
    fkey = st.radio("公式", list(FORMULAS), horizontal=True, key="ps_f",
                    format_func=lambda k: {"sc": "sin·cos", "cs": "cos·sin", "cc": "cos·cos", "ss": "sin·sin",
                                           "s+s": "sin+sin", "s-s": "sin−sin", "c+c": "cos+cos",
                                           "c-c": "cos−cos"}[k])
    fm = FORMULAS[fkey]
    is_prod = fm["group"] == "積→和"
    deg_opts = [F(k, 2) for k in range(-360, 721, 15)]   # −180° 〜 360° を 7.5° 刻み
    fmt = lambda d: f"{float(d):g}°"
    cA, cB = st.columns(2)
    x = cA.select_slider("α" if is_prod else "A", options=deg_opts, key="ps_x", format_func=fmt)
    y = cB.select_slider("β" if is_prod else "B", options=deg_opts, key="ps_y", format_func=fmt)

    st.latex(fm["tex"])
    lv, rv = evaluate(fm["lhs"], x, y), evaluate(fm["rhs"], x, y)
    st.markdown("**代入する**")
    st.latex(rf"{side_tex(fm['lhs'], x, y)} = {side_tex(fm['rhs'], x, y)}")
    st.markdown("**値を入れて計算する**")
    st.latex(rf"{side_tex(fm['rhs'], x, y)} = {side_tex(fm['rhs'], x, y, values=True)} = {value_tex(rv)}")
    if isinstance(lv, Q236):
        st.latex(rf"\text{{左辺を直接計算：}}\ {side_tex(fm['lhs'], x, y, values=True)} = {lv.latex()}")
    else:
        st.latex(rf"\text{{左辺を電卓で計算：}}\ {side_tex(fm['lhs'], x, y)} \approx {float(lv):.6f}")
    if abs(float(lv) - float(rv)) < 1e-9:
        if isinstance(rv, Q236) and not isinstance(lv, Q236):
            st.success("左辺の角は有名角ではないのに、公式で変形すると **有名角だけ** になり、正確な値が求められました。これが公式の使いどころです。")
        else:
            st.success("左辺と右辺の値が一致しました。")
    else:
        st.error("値が一致しません（公式の定義に誤りがあります）。")
    if not isinstance(rv, Q236):
        st.caption("右辺の角が 15° の倍数でないため、小数で表示しています。α, β（A, B）を変えて、右辺が有名角になる組を探してみよう。")

# ---------------- ③ グラフで見る ----------------
with tab3:
    mode = st.radio("見るもの", ["和 → 積（うなり）", "積 → 和（2 つの波に分ける）"], horizontal=True, key="ps_mode")
    g1, g2, g3 = st.columns(3)
    mm = g1.slider("m", 1, 20, 11, key="ps_m")
    nn = g2.slider("n", 1, 20, 9, key="ps_n")
    span = g3.select_slider("表示範囲", options=[2, 4, 6], value=4, format_func=lambda v: f"0〜{v}π", key="ps_span")
    xg = x_grid(0, span, n=3000)
    fig = go.Figure()
    if mode.startswith("和"):
        kind = st.radio("式", ["sin + sin", "cos + cos"], horizontal=True, key="ps_kind")
        f = np.sin if kind.startswith("sin") else np.cos
        yy = f(mm * xg) + f(nn * xg)
        p, q = (mm + nn) / 2, (mm - nn) / 2
        env = 2 * np.cos(q * xg)
        fig.add_trace(curve(xg, yy, f"{kind.split()[0]} {mm}x + {kind.split()[0]} {nn}x", COLORS["wave"], width=2))
        fig.add_trace(curve(xg, env, f"±2cos({q:g}x)（包絡線）", COLORS["key"], dash="dash", width=2))
        fig.add_trace(curve(xg, -env, "", COLORS["key"], dash="dash", width=2, showlegend=False))
        style_axes(fig, 0, span, 2.4, "rad", height=420)
        st.plotly_chart(fig, key="ps_beat")
        inner = "sin" if kind.startswith("sin") else "cos"
        st.latex(rf"\{inner} {mm}x + \{inner} {nn}x = 2\{inner} {p:g}x\,\cos {q:g}x")
        st.markdown(
            rf"速く振動する $\{inner} {p:g}x$ の振幅が、ゆっくり変わる $2\cos {q:g}x$（赤い点線）で決まります。"
            "m と n が近いほど包絡線がゆっくりになり、**うなり**（音が大きくなったり小さくなったりする現象）になります。"
        )
    else:
        kind = st.radio("式", ["sin·cos", "cos·cos", "sin·sin"], horizontal=True, key="ps_kind2")
        f1, f2 = {"sin·cos": (np.sin, np.cos), "cos·cos": (np.cos, np.cos), "sin·sin": (np.sin, np.sin)}[kind]
        yy = f1(mm * xg) * f2(nn * xg)
        if kind == "sin·cos":
            w1, w2, t1, t2 = 0.5 * np.sin((mm + nn) * xg), 0.5 * np.sin((mm - nn) * xg), "½sin", "½sin"
        elif kind == "cos·cos":
            w1, w2, t1, t2 = 0.5 * np.cos((mm + nn) * xg), 0.5 * np.cos((mm - nn) * xg), "½cos", "½cos"
        else:
            w1, w2, t1, t2 = -0.5 * np.cos((mm + nn) * xg), 0.5 * np.cos((mm - nn) * xg), "−½cos", "½cos"
        fig.add_trace(curve(xg, w1, f"{t1}({mm + nn}x)", COLORS["steps"][1], dash="dot", width=1.5))
        fig.add_trace(curve(xg, w2, f"{t2}({mm - nn}x)", "#ff7f0e", dash="dash", width=2))
        fig.add_trace(curve(xg, yy, f"積 {kind.replace('·', f' {mm}x · ')} {nn}x", COLORS["wave"], width=2.5))
        style_axes(fig, 0, span, 1.4, "rad", height=420)
        st.plotly_chart(fig, key="ps_prod")
        st.markdown("青い積のグラフは、点線（周波数 m + n）と破線（周波数 m − n）の **2 つの波の和** にちょうど一致します。")

# ---------------- ④ 類題と解き方 ----------------
with tab4:
    st.caption("課題と同じ型の類題です。まず自分で解いてから「解き方」を開こう。")
    PROBLEMS = [
        (r"\sin 52.5^\circ \cos 7.5^\circ \text{ の値}",
         [r"= \frac{1}{2}\{\sin(52.5^\circ + 7.5^\circ) + \sin(52.5^\circ - 7.5^\circ)\}",
          r"= \frac{1}{2}(\sin 60^\circ + \sin 45^\circ) = \frac{1}{2}\left(\frac{\sqrt{3}}{2} + \frac{\sqrt{2}}{2}\right)",
          r"= \frac{\sqrt{3} + \sqrt{2}}{4}"]),
        (r"\sin 75^\circ \sin 15^\circ \text{ の値}",
         [r"= -\frac{1}{2}\{\cos 90^\circ - \cos 60^\circ\} = -\frac{1}{2}\left(0 - \frac{1}{2}\right)", r"= \frac{1}{4}"]),
        (r"\cos 3\theta\cos\theta \text{ を和の形に}",
         [r"= \frac{1}{2}\{\cos(3\theta + \theta) + \cos(3\theta - \theta)\}", r"= \frac{1}{2}(\cos 4\theta + \cos 2\theta)"]),
        (r"\sin 105^\circ + \sin 15^\circ \text{ の値}",
         [r"= 2\sin\frac{105^\circ + 15^\circ}{2}\cos\frac{105^\circ - 15^\circ}{2} = 2\sin 60^\circ\cos 45^\circ",
          r"= 2\cdot\frac{\sqrt{3}}{2}\cdot\frac{\sqrt{2}}{2} = \frac{\sqrt{6}}{2}"]),
        (r"\cos 105^\circ - \cos 15^\circ \text{ の値}",
         [r"= -2\sin\frac{105^\circ + 15^\circ}{2}\sin\frac{105^\circ - 15^\circ}{2} = -2\sin 60^\circ\sin 45^\circ",
          r"= -2\cdot\frac{\sqrt{3}}{2}\cdot\frac{\sqrt{2}}{2} = -\frac{\sqrt{6}}{2}"]),
        (r"\cos\theta + \cos 3\theta + \cos 5\theta \text{ を積の形に}",
         [r"\cos\theta + \cos 5\theta = 2\cos 3\theta\cos 2\theta \quad(\text{両端を組にする})",
          r"\text{与式} = 2\cos 3\theta\cos 2\theta + \cos 3\theta = \cos 3\theta\,(2\cos 2\theta + 1)"]),
        (r"0 \le \theta < \pi \text{ のとき } \sin 3\theta + \sin\theta = 0 \text{ を解く}",
         [r"\sin 3\theta + \sin\theta = 2\sin 2\theta\cos\theta = 0",
          r"\sin 2\theta = 0 \ \text{または}\ \cos\theta = 0",
          r"0 \le 2\theta < 2\pi \text{ より } \theta = 0, \frac{\pi}{2}\quad/\quad \cos\theta = 0 \text{ より } \theta = \frac{\pi}{2}",
          r"\theta = 0,\ \frac{\pi}{2}"]),
    ]
    for i, (q, steps) in enumerate(PROBLEMS, start=1):
        st.markdown(f"**類題{i}**")
        st.latex(q)
        with st.expander("解き方"):
            for line in steps:
                st.latex(line)
    st.divider()
    st.markdown(
        "**どこで使う？**\n"
        "- 有名角でない角の積や和を、有名角に直して値を求める（類題1・4）\n"
        "- 方程式を「積 = 0」の形にして解く（類題7）\n"
        "- 物理：2 つの音のうなり、交流の電力（電圧 × 電流 = sin × sin）の計算"
    )
