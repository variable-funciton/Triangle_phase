"""三角関数の合成  a sin x + b cos x = R sin(x + α) = R cos(x + β)（後期課題8 対応）"""

import math
from fractions import Fraction as F

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.angles import angle_latex, angle_text, pi_ticks
from utils.exact import Q236, cos_deg, sin_deg, sqrt_text
from utils.plotting import COLORS, curve, style_axes, x_grid
from utils.synthesis import COEF_OPTIONS, Synthesis, coef_latex

S2, S3 = Q236.sqrt_of(2), Q236.sqrt_of(3)
PRESETS = {
    "自由に設定": None,
    "√3 sin x + cos x": (S3, Q236(1)),
    "sin x + √3 cos x": (Q236(1), S3),
    "√3 sin x − cos x": (S3, Q236(-1)),
    "sin x + cos x": (Q236(1), Q236(1)),
    "sin x − cos x": (Q236(1), Q236(-1)),
    "−sin x + √3 cos x": (Q236(-1), S3),
    "−√3 sin x − cos x": (-S3, Q236(-1)),
    "3 sin x + 4 cos x（α がきれいな角にならない例）": (Q236(3), Q236(4)),
    "cos x だけ（a = 0）": (Q236(0), Q236(1)),
}
st.session_state.setdefault("syn_a", S3)
st.session_state.setdefault("syn_b", Q236(1))


def apply_preset():
    p = PRESETS[st.session_state["syn_preset"]]
    if p:
        st.session_state["syn_a"], st.session_state["syn_b"] = p


# ---------------- サイドバー ----------------
st.sidebar.header("係数")
st.sidebar.selectbox("例を読み込む", list(PRESETS), key="syn_preset", on_change=apply_preset)
a = st.sidebar.select_slider("a（sin x の係数）", options=COEF_OPTIONS, key="syn_a", format_func=Q236.text)
b = st.sidebar.select_slider("b（cos x の係数）", options=COEF_OPTIONS, key="syn_b", format_func=Q236.text)
unit = st.sidebar.radio("角度の単位", ["rad", "deg"], horizontal=True,
                        format_func=lambda u: "弧度法" if u == "rad" else "度数法")
mode = st.sidebar.radio("α・β の範囲", ["pm", "pos"],
                        format_func=lambda m: "−π < α ≤ π" if m == "pm" else "0 ≤ α < 2π")

st.title("三角関数の合成")
st.latex(r"a\sin x + b\cos x = R\sin(x + \alpha) = R\cos(x + \beta)")
st.latex(r"R = \sqrt{a^2 + b^2},\qquad \cos\alpha = \frac{a}{R},\ \ \sin\alpha = \frac{b}{R},\qquad \beta = \alpha - \frac{\pi}{2}")

if a.is_zero() and b.is_zero():
    st.warning("a = b = 0 のときは 0 になるだけなので、合成できません。a か b を 0 以外にしてください。")
    st.stop()

s = Synthesis(a, b, mode)
st.markdown("#### いまの式")
st.latex(rf"{s.lhs_latex()} \;=\; {s.sin_form_latex(unit)} \;=\; {s.cos_form_latex(unit)}")
m = st.columns(4)
m[0].metric("振幅 R", sqrt_text(s.R2))
m[1].metric("α", angle_text(s.alpha_pi, unit) if s.alpha_pi is not None else f"≈ {math.degrees(s.alpha):.2f}°")
m[2].metric("β = α − π/2", angle_text(s.beta_pi, unit) if s.beta_pi is not None else f"≈ {math.degrees(s.beta):.2f}°")
m[3].metric("最大値 / 最小値", f"{s.R:.4g} / {-s.R:.4g}")
if s.alpha_pi is None:
    st.info(r"α は有名角になりません。このようなときは「$\cos\alpha = \frac{a}{R},\ \sin\alpha = \frac{b}{R}$ を満たす角 α」"
            "と書いたまま答えます（グラフや最大値・最小値は同じように求められます）。")

tabs = st.tabs(["① 点 (a, b) で角を読む", "② 2つの波をたす", "③ 回転するベクトル",
                "④ sin の形と cos の形", "⑤ 区間での最大・最小"])

# =====================================================================
# ① 点 (a, b) で角を読む
# =====================================================================
with tabs[0]:
    c1, c2 = st.columns([3, 2])
    with c1:
        A, B, R = float(a), float(b), s.R
        lim = R * 1.35
        fig = go.Figure()
        t = np.linspace(0, 2 * np.pi, 200)
        fig.add_trace(go.Scatter(x=R * np.cos(t), y=R * np.sin(t), mode="lines", name=f"半径 R の円",
                                 line=dict(color="#bbbbbb", dash="dot"), hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[A, A], y=[0, B], mode="lines", line=dict(color=COLORS["steps"][1], dash="dash"),
                                 showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[0, A], y=[B, B], mode="lines", line=dict(color="#ff7f0e", dash="dash"),
                                 showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[0, A], y=[0, 0], mode="lines", line=dict(color=COLORS["steps"][1], width=5),
                                 name=f"a = {a.text()}", hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, B], mode="lines", line=dict(color="#ff7f0e", width=5),
                                 name=f"b = {b.text()}", hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[0, A], y=[0, B], mode="lines+markers", name="R",
                                 line=dict(color=COLORS["wave"], width=4),
                                 marker=dict(size=[0, 12], color=COLORS["key"]), hoverinfo="skip"))
        arc = np.linspace(0, s.alpha, 60)
        rr = R * 0.32
        fig.add_trace(go.Scatter(x=rr * np.cos(arc), y=rr * np.sin(arc), mode="lines", name="α",
                                 line=dict(color=COLORS["key"], width=2.5), hoverinfo="skip"))
        mid = s.alpha / 2
        fig.add_annotation(x=rr * 1.45 * math.cos(mid), y=rr * 1.45 * math.sin(mid), text="α", showarrow=False,
                           font=dict(size=18, color=COLORS["key"]))
        fig.add_annotation(x=A, y=B, text=f"P({a.text()}, {b.text()})", showarrow=False,
                           xshift=40 if A >= 0 else -40, yshift=14 if B >= 0 else -14, font=dict(size=14))
        fig.add_annotation(x=A / 2, y=B / 2, text=f"R = {s.R:.4g}", showarrow=False,
                           xshift=-30 if A * B >= 0 else 30, yshift=12, font=dict(color=COLORS["wave"], size=13))
        fig.update_layout(height=470, template="plotly_white", margin=dict(l=10, r=10, t=30, b=10),
                          legend=dict(orientation="h", y=1.08))
        fig.update_xaxes(range=[-lim, lim], zeroline=True, zerolinecolor="black", title_text="x")
        fig.update_yaxes(range=[-lim, lim], zeroline=True, zerolinecolor="black", scaleanchor="x", scaleratio=1,
                         title_text="y")
        st.plotly_chart(fig, key="syn_point")
    with c2:
        st.markdown(r"座標平面に点 $\mathrm{P}(a, b)$ をとると、")
        st.latex(rf"R = \mathrm{{OP}} = \sqrt{{a^2 + b^2}} = \sqrt{{{(a * a).latex()} + {(b * b).latex()}}} = {s.R_latex()}")
        st.markdown(r"OP が $x$ 軸の正の向きとなす角が $\alpha$ です。")
        st.latex(rf"\cos\alpha = \frac{{a}}{{R}} = {s.ratio_latex(a)},\qquad \sin\alpha = \frac{{b}}{{R}} = {s.ratio_latex(b)}")
        if not a.is_zero():
            tan = (b * a / (a * a).as_rational())
            st.latex(rf"\tan\alpha = \frac{{b}}{{a}} = {tan.latex()}")
        st.latex(s.alpha_latex(unit))
        st.caption("点 P が第何象限にあるかで α の範囲が決まる。tan α だけで判断すると、反対側の角と取り違えやすいので注意。")

# =====================================================================
# ② 2つの波をたす
# =====================================================================
with tabs[1]:
    o = st.columns(3)
    show_parts = o[0].checkbox("a sin x と b cos x を表示", value=True)
    show_rsin = o[1].checkbox("R sin(x + α) を重ねる", value=True)
    show_max = o[2].checkbox("最大の点を表示", value=True)
    lo, hi = -0.5, 2.5
    x = x_grid(lo, hi)
    fig2 = go.Figure()
    if show_parts:
        fig2.add_trace(curve(x, float(a) * np.sin(x), f"{a.text()} sin x", COLORS["steps"][1], dash="dash", width=2))
        fig2.add_trace(curve(x, float(b) * np.cos(x), f"{b.text()} cos x", "#ff7f0e", dash="dash", width=2))
    fig2.add_trace(curve(x, float(a) * np.sin(x) + float(b) * np.cos(x),
                         "a sin x + b cos x", COLORS["wave"], width=4))
    if show_rsin:
        xs = x[::18]
        fig2.add_trace(go.Scatter(x=xs, y=s.R * np.sin(xs + s.alpha), mode="markers", name="R sin(x + α)",
                                  marker=dict(color=COLORS["key"], size=7, symbol="circle-open", line=dict(width=2)),
                                  hoverinfo="skip"))
    for v in (s.R, -s.R):
        fig2.add_hline(y=v, line_dash="dot", line_color="#2ca02c",
                       annotation_text=f"{'' if v > 0 else '−'}R = {v:.4g}", annotation_position="right")
    if show_max:
        x0 = (math.pi / 2 - s.alpha) % (2 * math.pi)
        q0 = None if s.alpha_pi is None else (F(1, 2) - s.alpha_pi) % 2
        fig2.add_trace(go.Scatter(x=[x0], y=[s.R], mode="markers+text", name="最大の点",
                                  marker=dict(color=COLORS["key"], size=13, symbol="star"),
                                  text=[f"x = {angle_text(q0, unit) if q0 is not None else f'{math.degrees(x0):.1f}°'}"],
                                  textposition="top center", hoverinfo="skip"))
    style_axes(fig2, lo, hi, s.R + 0.8, unit, height=460)
    st.plotly_chart(fig2, key="syn_waves")
    st.markdown(r"振幅の違う 2 つの波 $a\sin x$ と $b\cos x$ をたすと、**振幅 $R$ の 1 つの sin 波** になります。"
                r"グラフは $y = R\sin x$ を $x$ 軸方向に $-\alpha$ だけ平行移動したものです。")

    st.markdown("##### x の値を入れて確かめる")
    xq = st.select_slider("x", options=[F(k, 12) for k in range(0, 25)], value=F(1, 3),
                          format_func=lambda q: angle_text(q, unit), key="syn_xq")
    va = a * sin_deg(xq * 180)
    vb = b * cos_deg(xq * 180)
    ta, tb = coef_latex(a, "sin", True), coef_latex(b, "cos", True)
    parts = [rf"{ta} = {va.latex()}" if ta else "", rf"{tb} = {vb.latex()}" if tb else ""]
    st.latex(rf"x = {angle_latex(xq, unit)}:\quad " + r",\quad ".join(p for p in parts if p)
             + rf",\quad \text{{和}} = {(va + vb).latex()}")
    st.latex(rf"{s.sin_form_latex(unit)} \text{{ に代入すると }} \approx {s.R * math.sin(float(xq) * math.pi + s.alpha):.6f}"
             rf"\quad(\text{{和}} \approx {float(va + vb):.6f})")

# =====================================================================
# ③ 回転するベクトル（アニメーション）
# =====================================================================
with tabs[2]:
    st.markdown(
        r"長さ $a$ のベクトルと長さ $b$ のベクトルを直角につなぎ、角 $x$ だけ回転させます。"
        r"先端の **高さ（$y$ 座標）** がちょうど $a\sin x + b\cos x$ です。"
        r"2 本をまとめた長さ $R$ のベクトルは、はじめ角 $\alpha$ の向きにあり、そこから $x$ だけ回るので $R\sin(x+\alpha)$ になります。"
    )
    A, B, R = float(a), float(b), s.R
    cx = -(R + 0.6)          # 円の中心（グラフの左側に置く）
    T = np.linspace(0, 2 * np.pi, 73)
    xfull = np.linspace(0, 2 * np.pi, 300)
    yfull = A * np.sin(xfull) + B * np.cos(xfull)

    def frame_traces(tt):
        p1 = (cx + A * math.cos(tt), A * math.sin(tt))                       # a ベクトルの先
        p2 = (p1[0] - B * math.sin(tt), p1[1] + B * math.cos(tt))            # さらに b ベクトルの先
        yv = p2[1]
        trace_x = np.linspace(0, tt, max(2, int(tt / (2 * np.pi) * 300)))
        return [
            go.Scatter(x=[cx, p1[0]], y=[0, p1[1]], mode="lines", line=dict(color=COLORS["steps"][1], width=4)),
            go.Scatter(x=[p1[0], p2[0]], y=[p1[1], p2[1]], mode="lines", line=dict(color="#ff7f0e", width=4)),
            go.Scatter(x=[cx, p2[0]], y=[0, p2[1]], mode="lines", line=dict(color=COLORS["wave"], width=3, dash="dot")),
            go.Scatter(x=[p2[0], tt], y=[yv, yv], mode="lines", line=dict(color="#999999", width=1, dash="dash")),
            go.Scatter(x=trace_x, y=A * np.sin(trace_x) + B * np.cos(trace_x), mode="lines",
                       line=dict(color=COLORS["wave"], width=4)),
            go.Scatter(x=[p2[0], tt], y=[yv, yv], mode="markers", marker=dict(color=COLORS["key"], size=10)),
        ]

    th = np.linspace(0, 2 * np.pi, 120)
    static = [
        go.Scatter(x=cx + R * np.cos(th), y=R * np.sin(th), mode="lines", line=dict(color="#cccccc", dash="dot"),
                   hoverinfo="skip"),
        go.Scatter(x=xfull, y=yfull, mode="lines", line=dict(color="#d0d7e2", width=2), hoverinfo="skip"),
    ]
    names = ["円（半径 R）", "a sin x + b cos x", f"a = {a.text()}", f"b = {b.text()}", "R", "", "", ""]
    first = frame_traces(0.0)
    fig3 = go.Figure(data=static + first,
                     frames=[go.Frame(name=str(i), data=frame_traces(tt), traces=list(range(2, 8)))
                             for i, tt in enumerate(T)])
    for i, tr in enumerate(fig3.data):
        tr.name = names[i]
        tr.showlegend = bool(names[i])
        tr.hoverinfo = "skip"
    step_args = dict(frame=dict(duration=0, redraw=False), transition=dict(duration=0), mode="immediate")
    fig3.update_layout(
        height=480, template="plotly_white", margin=dict(l=10, r=10, t=30, b=100),
        legend=dict(orientation="h", y=1.08),
        updatemenus=[dict(type="buttons", direction="left", showactive=False, x=0, xanchor="left",
                          y=-0.12, yanchor="top", pad=dict(t=10, r=10), buttons=[
                              dict(label="▶ 再生", method="animate",
                                   args=[None, dict(frame=dict(duration=60, redraw=False), transition=dict(duration=0),
                                                    mode="immediate", fromcurrent=True)]),
                              dict(label="⏸ 停止", method="animate", args=[[None], step_args]),
                          ])],
        sliders=[dict(active=0, x=0.18, len=0.82, y=-0.12, yanchor="top", pad=dict(t=10),
                      currentvalue=dict(prefix="x = ", font=dict(size=15, color=COLORS["wave"])),
                      font=dict(color="rgba(0,0,0,0)"), ticklen=2,
                      steps=[dict(method="animate", label=f"{math.degrees(tt):.0f}°",
                                  args=[[str(i)], step_args]) for i, tt in enumerate(T)])],
    )
    tv, tt_ = pi_ticks(0, 2, F(1, 2), unit)
    fig3.update_xaxes(range=[cx - R - 0.3, 2 * np.pi + 0.3], tickvals=tv, ticktext=tt_, zeroline=False,
                      gridcolor="rgba(0,0,0,0.06)")
    fig3.update_yaxes(range=[-R - 0.4, R + 0.4], scaleanchor="x", scaleratio=1, zeroline=True,
                      zerolinecolor="black", gridcolor="rgba(0,0,0,0.06)")
    fig3.add_vline(x=0, line_color="black", line_width=1)
    st.plotly_chart(fig3, key="syn_phasor")
    st.caption("緑：長さ a のベクトル、橙：長さ b のベクトル（緑に直角）、点線：まとめた長さ R のベクトル。"
               "x = 0 のとき点線の向きが角 α です。")

# =====================================================================
# ④ sin の形と cos の形
# =====================================================================
with tabs[3]:
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown(r"**sin の形** $R\sin(x+\alpha)$")
        st.latex(r"R\sin(x+\alpha) = (R\cos\alpha)\sin x + (R\sin\alpha)\cos x")
        st.markdown(r"係数を比べて $a = R\cos\alpha,\ b = R\sin\alpha$ → **点 $(a,\ b)$** の角が $\alpha$")
        st.latex(s.alpha_latex(unit))
    with c2, st.container(border=True):
        st.markdown(r"**cos の形** $R\cos(x+\beta)$")
        st.latex(r"R\cos(x+\beta) = (-R\sin\beta)\sin x + (R\cos\beta)\cos x")
        st.markdown(r"係数を比べて $b = R\cos\beta,\ a = -R\sin\beta$ → **点 $(b,\ -a)$** の角が $\beta$")
        st.latex(s.beta_latex(unit))
    st.markdown(
        r"$\sin\theta = \cos\left(\theta - \dfrac{\pi}{2}\right)$ なので "
        r"$R\sin(x+\alpha) = R\cos\left(x + \alpha - \dfrac{\pi}{2}\right)$。"
        r"つまり **$\beta = \alpha - \dfrac{\pi}{2}$**（範囲に入るよう $2\pi$ を足し引きする）。"
    )
    if s.alpha_pi is not None:
        st.latex(rf"\beta = {angle_latex(s.alpha_pi, unit)} - {angle_latex(F(1, 2), unit)} {s.beta_rel(unit)}")
    else:
        st.latex(rf"\beta = \alpha - {angle_latex(F(1, 2), unit)} {s.beta_rel(unit)}")
    with st.expander("⚠️ よくある間違い"):
        st.markdown(
            r"""
- **点を $(b, a)$ にとる**：sin の形では $\sin x$ の係数 $a$ が **$x$ 座標**、$\cos x$ の係数 $b$ が **$y$ 座標**。
- **$R$ を $a + b$ にする**：$R = \sqrt{a^2 + b^2}$（三平方の定理）。
- **$\tan\alpha = \dfrac{b}{a}$ だけで $\alpha$ を決める**：$\tan$ は $\pi$ ずれた角でも同じ値。点 $(a, b)$ の **象限** を必ず確認する。
- **cos の形の符号**：$\cos(x+\beta)$ を展開すると $\sin x$ の係数は **$-R\sin\beta$**。
"""
        )

# =====================================================================
# ⑤ 区間での最大・最小
# =====================================================================
with tabs[4]:
    INTERVALS = {
        "0 ≤ x < 2π（1周期）": (F(0), F(2), False),
        "0 ≤ x ≤ π": (F(0), F(1), True),
        "0 ≤ x ≤ π/2": (F(0), F(1, 2), True),
        "−π/2 ≤ x ≤ π/2": (F(-1, 2), F(1, 2), True),
        "π/2 ≤ x ≤ 3π/2": (F(1, 2), F(3, 2), True),
    }
    iv = st.radio("x の範囲", list(INTERVALS), horizontal=True, key="syn_iv")
    lo_q, hi_q, inc = INTERVALS[iv]
    ex = s.extrema(lo_q, hi_q, inc, unit)
    st.markdown("**手順1** 合成する")
    st.latex(rf"y = {s.lhs_latex()} = {s.sin_form_latex(unit)}")
    st.markdown(r"**手順2** $u = x + \alpha$ のとりうる範囲を求める")
    rel = r"\le" if inc else "<"
    if s.alpha_pi is not None:
        lo_u, hi_u = lo_q + s.alpha_pi, hi_q + s.alpha_pi
        sign = "+" if s.alpha_pi >= 0 else "-"
        st.latex(rf"{angle_latex(lo_u, unit)} \le x {sign} {angle_latex(abs(s.alpha_pi), unit)} {rel} {angle_latex(hi_u, unit)}")
    else:
        lo_t = r"\alpha" if lo_q == 0 else rf"{angle_latex(lo_q, unit)} + \alpha"
        st.latex(rf"{lo_t} \le x + \alpha {rel} {angle_latex(hi_q, unit)} + \alpha")
    st.markdown(r"**手順3** 単位円（または $\sin u$ のグラフ）で $\sin u$ の最大・最小を読み、$R$ 倍する")
    mx, mn = ex["max"], ex["min"]
    c = st.columns(2)
    sep = r",\ "
    c[0].success(f"**最大値** ${mx[0]}$（$x = {sep.join(mx[2])}$ のとき）")
    c[1].info(f"**最小値** ${mn[0]}$（$x = {sep.join(mn[2])}$ のとき）")

    lo_f, hi_f = float(lo_q), float(hi_q)
    xx = x_grid(lo_f - 0.5, hi_f + 0.5)
    inside = (xx >= lo_f * np.pi) & (xx <= hi_f * np.pi)
    yy = float(a) * np.sin(xx) + float(b) * np.cos(xx)
    fig5 = go.Figure()
    fig5.add_trace(curve(xx, yy, "区間の外", "#cccccc", width=2))
    fig5.add_trace(curve(xx[inside], yy[inside], "区間の中", COLORS["wave"], width=4))
    for (val, label, color) in ((mx[1], "最大", COLORS["key"]), (mn[1], "最小", "#2ca02c")):
        mask = inside & (np.abs(yy - val) < 1e-3 * max(1, s.R))
        if not mask.any():   # 端点で最大・最小になる場合
            cand = [lo_f * np.pi, hi_f * np.pi]
            xs_pts = [xv for xv in cand if abs(s.value(xv) - val) < 1e-9]
        else:
            idx = np.where(mask)[0]
            xs_pts = [xx[idx[np.argmin(np.abs(yy[idx] - val))]]]
            # 同じ値をとる別の点（周期の端など）も拾う
            for xv in (lo_f * np.pi, hi_f * np.pi):
                if abs(s.value(xv) - val) < 1e-9:
                    xs_pts.append(xv)
        fig5.add_trace(go.Scatter(x=xs_pts, y=[val] * len(xs_pts), mode="markers", name=label,
                                  marker=dict(color=color, size=13, symbol="star"), hoverinfo="skip"))
    fig5.add_vrect(x0=lo_f * np.pi, x1=hi_f * np.pi, fillcolor=COLORS["wave"], opacity=0.06, line_width=0)
    style_axes(fig5, lo_f - 0.5, hi_f + 0.5, s.R + 0.6, unit, height=380)
    st.plotly_chart(fig5, key="syn_extrema")
    st.caption("区間の中に「x + α = π/2（sin が 1）」の点があればそこで最大 R。なければ区間の端で最大になる。最小も同様。")
