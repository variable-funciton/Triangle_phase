"""バネの単振動（摩擦・抵抗あり）と横波・縦波 — 三角関数の応用"""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.oscillation import (G, damped_envelope, damped_motion, damped_turning_points, free_motion,
                               friction_motion, friction_turning_points, omega, period, wave_displacement)

C_BLOCK, C_SPRING, C_X, C_ENV, C_CIRCLE = "#1f77b4", "#555555", "#d62728", "#ff7f0e", "#2ca02c"
MODELS = {"none": "摩擦・抵抗なし", "friction": "床との動摩擦あり（μ）", "viscous": "空気・水の抵抗あり（速さに比例）"}


def add_player(fig, labels, dur, prefix="", suffix="", y=-0.08):
    step = dict(frame=dict(duration=0, redraw=False), transition=dict(duration=0), mode="immediate")
    fig.update_layout(
        updatemenus=[dict(type="buttons", direction="left", showactive=False, x=0, xanchor="left", y=y,
                          yanchor="top", pad=dict(t=10, r=10), buttons=[
                              dict(label="▶ 再生", method="animate",
                                   args=[None, dict(frame=dict(duration=dur, redraw=False), transition=dict(duration=0),
                                                    mode="immediate", fromcurrent=True)]),
                              dict(label="⏸ 停止", method="animate", args=[[None], step]),
                          ])],
        sliders=[dict(active=0, x=0.2, len=0.8, y=y, yanchor="top", pad=dict(t=10),
                      currentvalue=dict(prefix=prefix, suffix=suffix, font=dict(size=14)),
                      font=dict(color="rgba(0,0,0,0)"), ticklen=2,
                      steps=[dict(method="animate", label=lb, args=[[str(i)], step]) for i, lb in enumerate(labels)])],
    )


def spring_xy(x_left, x_right, y, coils=12, amp=0.022):
    """ばねのギザギザ線"""
    n = coils * 2
    lead = 0.03 * (x_right - x_left)
    xs = [x_left, x_left + lead]
    ys = [y, y]
    for i in range(1, n):
        xs.append(x_left + lead + (x_right - x_left - 2 * lead) * i / n)
        ys.append(y + (amp if i % 2 else -amp))
    xs += [x_right - lead, x_right]
    ys += [y, y]
    return xs, ys


# =====================================================================
# サイドバー
# =====================================================================
st.sidebar.header("ばねとおもり")
m = st.sidebar.slider("おもりの質量 m [kg]", 0.1, 2.0, 0.5, 0.1, key="sp_m")
k = st.sidebar.slider("ばね定数 k [N/m]", 5.0, 100.0, 20.0, 1.0, key="sp_k")
x0 = st.sidebar.slider("はじめに引っぱる長さ x₀ [m]", 0.05, 0.30, 0.20, 0.01, key="sp_x0")
model = st.sidebar.radio("摩擦・抵抗", list(MODELS), format_func=MODELS.get, key="sp_model")
w = omega(k, m)
T = period(k, m)
mu = gamma = 0.0
if model == "friction":
    mu = st.sidebar.slider("動摩擦係数 μ", 0.01, 0.25, 0.08, 0.005, key="sp_mu")
elif model == "viscous":
    gamma = st.sidebar.slider("抵抗の強さ γ [1/s]", 0.05, round(0.6 * w, 2), min(0.3, round(0.6 * w, 2)), 0.05,
                              key="sp_gamma")
speed = st.sidebar.select_slider("再生の速さ", options=[0.25, 0.5, 1.0], value=1.0, key="sp_speed",
                                 format_func=lambda s: {0.25: "1/4（スロー）", 0.5: "1/2", 1.0: "実際の速さ"}[s])

st.title("バネの単振動と波")
st.markdown(
    r"ばねにつけたおもりを引っぱって放すと、位置は $x = x_0\cos\omega t$ という **三角関数** で表される往復運動（**単振動**）をします。"
    r"$\omega = \sqrt{k/m}$ を **角振動数**、$T = 2\pi/\omega$ を **周期** といいます。"
)
mt = st.columns(4)
mt[0].metric("角振動数 ω = √(k/m)", f"{w:.2f} rad/s")
mt[1].metric("周期 T = 2π√(m/k)", f"{T:.3f} 秒")
mt[2].metric("振動数 f = 1/T", f"{1 / T:.3f} Hz")
mt[3].metric("振幅（はじめ）", f"{x0:.2f} m")

# ---- 運動の計算 ----
if model == "none":
    t_end = 3 * T
    motion = lambda t: free_motion(x0, k, m, t)
    pts = [(n * T / 2, x0 * (-1) ** n) for n in range(7)]
    d = 0.0
elif model == "friction":
    pts, t_stop, d = friction_turning_points(x0, k, m, mu)
    t_end = min(max(t_stop + T / 2, T), 24 * T)
    motion = lambda t: friction_motion(x0, k, m, mu, t)
else:
    n_half = int(min(20, max(4, math.ceil(math.log(20) / (gamma * T / 2)))))
    pts = damped_turning_points(x0, k, m, gamma, n_half)
    t_end = min(pts[-1][0], 10 * T)
    pts = [p for p in pts if p[0] <= t_end + 1e-9]
    motion = lambda t: damped_motion(x0, k, m, gamma, t)
    d = 0.0

tab1, tab2, tab3, tab4 = st.tabs(["① ばねの振動", "② 振幅の減り方（数列で見る）", "③ 横波と縦波", "④ 式で確かめる"])

# =====================================================================
# ① ばねの振動
# =====================================================================
with tab1:
    if model == "none":
        show_circle = st.checkbox("等速円運動の「影」として見る（円の上を回る点の x 座標 = おもりの位置）", value=True,
                                  key="sp_circle")
    else:
        show_circle = False
    if model == "friction":
        if len(pts) == 1:
            st.warning(f"ばねの力 kx₀ = {k * x0:.2f} N が最大の摩擦力 μmg = {mu * m * G:.2f} N 以下なので、おもりは動きません。")
        else:
            if pts[-1][0] > t_end:
                st.caption(f"※ 止まるまで時間がかかるため、アニメーションは最初の {t_end:.1f} 秒分だけ表示しています。")
            st.info(f"{len(pts) - 1} 回折り返して、t = {pts[-1][0]:.2f} 秒に x = {pts[-1][1]:+.3f} m で止まります。"
                    f"（灰色の帯 |x| ≤ μmg/k = {d:.3f} m に入って速さが 0 になると、ばねの力が摩擦に負けて止まる）")
    elif model == "viscous":
        st.info("振れ幅（オレンジの線）が一定の割合で小さくなりながら、いつまでも振動を続けます（だんだん止まって見える）。")

    wall = -0.55
    bw, bh = 0.10, 0.08
    cy = 0.48
    times = np.linspace(0, t_end, min(360, max(150, int(t_end / T * 18))))
    tf = np.linspace(0, t_end, 1500)
    xf = motion(tf)

    fig = make_subplots(rows=2, cols=1, row_heights=[0.48, 0.52], vertical_spacing=0.1,
                        subplot_titles=("おもりの動き（横から見た図）", "位置 x の時間変化"))
    # --- 静止した部分（上段） ---
    fig.add_trace(go.Scatter(x=[wall, wall], y=[0, 0.16], mode="lines", line=dict(color="black", width=6),
                             showlegend=False, hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[wall, 0.45], y=[0, 0], mode="lines", line=dict(color="black", width=2),
                             showlegend=False, hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-0.03, 0.16 if not show_circle else cy + x0 + 0.03], mode="lines",
                             line=dict(color="gray", dash="dot", width=1), showlegend=False, hoverinfo="skip"),
                  row=1, col=1)
    if model == "friction" and d > 0:
        fig.add_trace(go.Scatter(x=[-d, d, d, -d, -d], y=[-0.02, -0.02, 0.0, 0.0, -0.02], fill="toself",
                                 fillcolor="rgba(120,120,120,0.35)", line=dict(width=0), showlegend=False,
                                 hoverinfo="skip"), row=1, col=1)
    if show_circle:
        th = np.linspace(0, 2 * np.pi, 120)
        fig.add_trace(go.Scatter(x=x0 * np.cos(th), y=cy + x0 * np.sin(th), mode="lines",
                                 line=dict(color=C_CIRCLE, dash="dot"), showlegend=False, hoverinfo="skip"), row=1, col=1)
    # --- 静止した部分（下段） ---
    fig.add_trace(go.Scatter(x=tf, y=xf, mode="lines", line=dict(color="#d9d9d9", width=2), showlegend=False,
                             hoverinfo="skip"), row=2, col=1)
    if model == "viscous":
        env = damped_envelope(x0, gamma, tf)
        for sgn in (1, -1):
            fig.add_trace(go.Scatter(x=tf, y=sgn * env, mode="lines", line=dict(color=C_ENV, dash="dash", width=1.5),
                                     showlegend=False, hoverinfo="skip"), row=2, col=1)
    if model == "friction" and len(pts) > 1:
        fig.add_trace(go.Scatter(x=[p[0] for p in pts], y=[abs(p[1]) for p in pts], mode="lines+markers",
                                 line=dict(color=C_ENV, dash="dash", width=1.5), marker=dict(size=6),
                                 showlegend=False, hoverinfo="skip"), row=2, col=1)
        fig.add_trace(go.Scatter(x=[0, t_end], y=[d, d], mode="lines", line=dict(color="gray", dash="dot", width=1),
                                 showlegend=False, hoverinfo="skip"), row=2, col=1)
        fig.add_trace(go.Scatter(x=[0, t_end], y=[-d, -d], mode="lines", line=dict(color="gray", dash="dot", width=1),
                                 showlegend=False, hoverinfo="skip"), row=2, col=1)
    n_static = len(fig.data)

    def dyn(t):
        xv = float(motion([t])[0])
        sx, sy = spring_xy(wall, xv - bw / 2, bh / 2)
        tr = np.linspace(0, t, max(2, int(200 * t / t_end) + 2))
        out = [
            go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=C_SPRING, width=2)),
            go.Scatter(x=[xv - bw / 2, xv + bw / 2, xv + bw / 2, xv - bw / 2, xv - bw / 2],
                       y=[0, 0, bh, bh, 0], fill="toself", fillcolor=C_BLOCK, line=dict(color=C_BLOCK)),
            go.Scatter(x=tr, y=motion(tr), mode="lines", line=dict(color=C_X, width=3)),
            go.Scatter(x=[t], y=[xv], mode="markers", marker=dict(color=C_X, size=10)),
        ]
        if show_circle:
            px, py = x0 * math.cos(w * t), cy + x0 * math.sin(w * t)
            out += [
                go.Scatter(x=[0, px], y=[cy, py], mode="lines", line=dict(color=C_CIRCLE, width=2)),
                go.Scatter(x=[px], y=[py], mode="markers", marker=dict(color=C_CIRCLE, size=10)),
                go.Scatter(x=[px, xv], y=[py, bh], mode="lines", line=dict(color=C_CIRCLE, width=1, dash="dash")),
            ]
        return out

    first = dyn(0.0)
    rows = [1, 1, 2, 2] + ([1, 1, 1] if show_circle else [])
    for trc, r in zip(first, rows):
        trc.showlegend = False
        trc.hoverinfo = "skip"
        fig.add_trace(trc, row=r, col=1)
    idx = list(range(n_static, n_static + len(first)))
    fig.frames = [go.Frame(name=str(i), data=dyn(t), traces=idx) for i, t in enumerate(times)]
    add_player(fig, [f"{t:.2f}" for t in times], max(20, int(t_end / len(times) * 1000 / speed)),
               prefix="t = ", suffix=" 秒", y=-0.06)
    fig.update_layout(height=720, template="plotly_white", margin=dict(l=10, r=10, t=40, b=90))
    fig.update_xaxes(range=[wall - 0.03, 0.45], row=1, col=1, title_text="x [m]")
    fig.update_yaxes(range=[-0.05, (cy + x0 + 0.06) if show_circle else 0.2], row=1, col=1, scaleanchor="x",
                     scaleratio=1, showticklabels=False)
    fig.update_xaxes(range=[0, t_end], row=2, col=1, title_text="時刻 t [秒]")
    fig.update_yaxes(range=[-x0 * 1.15, x0 * 1.15], row=2, col=1, title_text="x [m]", zeroline=True,
                     zerolinecolor="black")
    st.plotly_chart(fig, key=f"sp_anim_{m}_{k}_{x0}_{model}_{mu}_{gamma}_{speed}_{show_circle}")
    if show_circle:
        st.caption("緑の点は半径 x₀ の円の上を角速度 ω で回る。その点の x 座標（影）が、ちょうどおもりの位置 x = x₀ cos ωt になる。")

# =====================================================================
# ② 振幅の減り方
# =====================================================================
with tab2:
    amps = [abs(p[1]) for p in pts]
    ns = list(range(len(amps)))
    if model == "none":
        st.markdown("摩擦も抵抗もないので、振幅は **ずっと同じ**（エネルギーが減らない）。")
    elif model == "friction":
        st.markdown(rf"動摩擦があると、折り返すたびに振幅が **一定の量 $2d = \dfrac{{2\mu mg}}{{k}} = {2 * d:.4f}$ m ずつ** 減ります。"
                    r"→ 振幅は **等差数列**（後期課題9）")
        st.latex(rf"a_n = x_0 - n\cdot\frac{{2\mu mg}}{{k}} = {x0:.2f} - {2 * d:.4f}\,n")
    else:
        r = math.exp(-gamma * math.pi / math.sqrt(w * w - gamma * gamma))
        st.markdown(rf"速さに比例する抵抗があると、折り返すたびに振幅が **一定の割合（{r:.4f} 倍）** になります。"
                    r"→ 振幅は **等比数列**（後期課題10）")
        st.latex(rf"a_n = x_0\, r^{{\,n}} = {x0:.2f}\times {r:.4f}^{{\,n}}")
    fig2 = go.Figure(go.Bar(x=ns, y=amps, marker_color=C_ENV, text=[f"{a:.3f}" for a in amps], textposition="outside",
                            hovertemplate="n = %{x}：振幅 %{y:.4f} m<extra></extra>"))
    if model == "friction" and d > 0:
        fig2.add_hline(y=d, line_dash="dot", line_color="gray", annotation_text=f"d = μmg/k = {d:.3f} m（これ以下で止まる）",
                       annotation_position="top right")
    fig2.update_layout(height=360, template="plotly_white", margin=dict(l=10, r=10, t=30, b=10))
    fig2.update_xaxes(title_text="n（何回目の折り返しか。0 ははじめ）", dtick=1)
    fig2.update_yaxes(title_text="振幅 a_n [m]", range=[0, x0 * 1.2])
    st.plotly_chart(fig2, key="sp_amps")
    if model == "friction" and len(amps) > 1:
        st.caption(f"差：{', '.join(f'{amps[i] - amps[i + 1]:.4f}' for i in range(min(5, len(amps) - 1)))} …（どれも同じ = 公差）")
    if model == "viscous":
        st.caption(f"比：{', '.join(f'{amps[i + 1] / amps[i]:.4f}' for i in range(min(5, len(amps) - 1)))} …（どれも同じ = 公比）")
    st.markdown(
        "| | 摩擦・抵抗なし | 動摩擦（床） | 速さに比例する抵抗（空気・水） |\n|:--|:--:|:--:|:--:|\n"
        "| 振幅の減り方 | 減らない | 一定の **量** ずつ（等差数列） | 一定の **割合** で（等比数列） |\n"
        "| 止まるか | 止まらない | 有限の時間で **止まる** | 止まらない（限りなく 0 に近づく） |\n"
        "| 周期 | 2π√(m/k) | **変わらない** | わずかに長くなる |"
    )

# =====================================================================
# ③ 横波と縦波
# =====================================================================
with tab3:
    st.markdown(
        r"ばねの単振動が、となりへとなりへと伝わっていくのが **波** です。各点はその場で単振動するだけで、進んでいくのは **振動の形** です。"
    )
    c1, c2, c3, c4 = st.columns(4)
    A = c1.slider("振幅 A [m]", 0.05, 0.40, 0.25, 0.05, key="wv_A")
    lam = c2.slider("波長 λ [m]", 1.0, 4.0, 2.0, 0.5, key="wv_lam")
    Tw = c3.slider("周期 T [秒]", 0.5, 4.0, 2.0, 0.5, key="wv_T")
    dirn = c4.radio("進む向き", [1, -1], format_func=lambda s: "+x 向き →" if s > 0 else "← −x 向き", key="wv_dir")
    st.latex(rf"y = A\sin 2\pi\left(\frac{{t}}{{T}} {'-' if dirn > 0 else '+'} \frac{{x}}{{\lambda}}\right),"
             rf"\qquad \text{{波の速さ}}\ v = \frac{{\lambda}}{{T}} = {lam / Tw:.2f}\ \text{{m/s}},\quad f = \frac{{1}}{{T}} = {1 / Tw:.2f}\ \text{{Hz}}")
    L = 6.0
    xs = np.linspace(0, L, 49)
    hi = 12                                    # 目印にする点
    A_long = min(A, 0.8 * lam / (2 * np.pi))   # 縦波は点が追い越さないように振幅を制限して表示
    xx = np.linspace(0, L, 400)
    times_w = np.linspace(0, 2 * Tw, 61)

    fig3 = make_subplots(rows=3, cols=1, vertical_spacing=0.11, row_heights=[0.36, 0.28, 0.36],
                         subplot_titles=("横波（振動の向き ⟂ 進む向き）：ひも・弦の波",
                                         "縦波（振動の向き ∥ 進む向き）：音・ばねの波（密と疎）",
                                         "縦波を横波のように表したグラフ（右向きのずれを上に描く）"))
    def wdyn(t):
        y = wave_displacement(xs, t, A, lam, Tw, dirn)
        u = wave_displacement(xs, t, A_long, lam, Tw, dirn)
        uu = wave_displacement(xx, t, A_long, lam, Tw, dirn)
        return [
            go.Scatter(x=xx, y=wave_displacement(xx, t, A, lam, Tw, dirn), mode="lines", line=dict(color="#9ecae1", width=2)),
            go.Scatter(x=xs, y=y, mode="markers", marker=dict(color=C_BLOCK, size=7)),
            go.Scatter(x=[xs[hi]], y=[y[hi]], mode="markers", marker=dict(color=C_X, size=13)),
            go.Scatter(x=xs + u, y=np.zeros_like(xs), mode="markers",
                       marker=dict(color=C_BLOCK, size=22, symbol="line-ns", line=dict(width=2.5, color=C_BLOCK))),
            go.Scatter(x=[xs[hi] + u[hi]], y=[0], mode="markers",
                       marker=dict(color=C_X, size=26, symbol="line-ns", line=dict(width=4, color=C_X))),
            go.Scatter(x=xx, y=uu, mode="lines", line=dict(color=C_CIRCLE, width=2.5)),
            go.Scatter(x=[xs[hi]], y=[u[hi]], mode="markers", marker=dict(color=C_X, size=11)),
        ]
    first = wdyn(0.0)
    for trc, r in zip(first, [1, 1, 1, 2, 2, 3, 3]):
        trc.showlegend = False
        trc.hoverinfo = "skip"
        fig3.add_trace(trc, row=r, col=1)
    fig3.add_trace(go.Scatter(x=[xs[hi], xs[hi]], y=[-A * 1.2, A * 1.2], mode="lines", showlegend=False,
                              line=dict(color=C_X, dash="dot", width=1), hoverinfo="skip"), row=1, col=1)
    fig3.frames = [go.Frame(name=str(i), data=wdyn(t), traces=list(range(7))) for i, t in enumerate(times_w)]
    add_player(fig3, [f"{t:.2f}" for t in times_w], max(30, int(2 * Tw / 60 * 1000 / speed)), prefix="t = ",
               suffix=" 秒", y=-0.05)
    fig3.update_layout(height=760, template="plotly_white", margin=dict(l=10, r=10, t=40, b=80))
    fig3.update_xaxes(range=[-0.2, L + 0.2])
    fig3.update_xaxes(title_text="x [m]", row=3, col=1)
    fig3.update_yaxes(range=[-0.5, 0.5], row=1, col=1, title_text="y [m]")
    fig3.update_yaxes(range=[-0.5, 0.5], row=2, col=1, showticklabels=False)
    fig3.update_yaxes(range=[-max(A_long, 0.1) * 1.4, max(A_long, 0.1) * 1.4], row=3, col=1, title_text="ずれ [m]")
    fig3.add_annotation(x=L * 0.85, y=0.42, xref="x", yref="y", text="進む向き " + ("→" if dirn > 0 else "←"),
                        showarrow=False, font=dict(size=14))
    st.plotly_chart(fig3, key=f"sp_wave_{A}_{lam}_{Tw}_{dirn}_{speed}")
    st.markdown(
        "- **赤い点** に注目：どちらの波でも、点はその場で **単振動するだけ**。右へ流れていくわけではない。\n"
        "- 横波は上下に、縦波は左右（進む向きと同じ向き）に振動する。縦波では点が集まった **密** と、まばらな **疎** が進んでいく。\n"
        "- 一番下のグラフは、縦波の各点の **右へのずれを上向き** に描き直したもの。縦波も横波と同じ sin のグラフで表せる。"
    )
    if A_long < A:
        st.caption(f"※ 縦波は点どうしが追い越さないよう、振幅を {A_long:.2f} m に小さくして表示しています。")

# =====================================================================
# ④ 式で確かめる
# =====================================================================
with tab4:
    st.markdown("#### 単振動は等速円運動の影")
    st.markdown(
        r"半径 $x_0$ の円の上を、角速度 $\omega$ [rad/s] で回る点を考えます。時刻 $t$ で回った角は $\omega t$ なので、"
        r"その点の座標は $(x_0\cos\omega t,\ x_0\sin\omega t)$（三角関数の定義そのもの）。"
        r"この点の **$x$ 座標だけ** を見たものが単振動です。"
    )
    st.latex(r"x = x_0\cos\omega t,\qquad T = \frac{2\pi}{\omega}\quad(\text{1 周 } 2\pi \text{ を回るのにかかる時間})")
    st.markdown(
        r"ばねの場合 $\omega = \sqrt{\dfrac{k}{m}}$ になることは物理で学びます（導くには微分を使う）。"
        r"おもりが重いほど（$m$ が大きいほど）ゆっくり、ばねが強いほど（$k$ が大きいほど）速く振動します。"
    )
    st.latex(rf"\text{{いまの値：}}\ \omega = \sqrt{{\frac{{{k:g}}}{{{m:g}}}}} \approx {w:.3f}\ \text{{rad/s}},\qquad "
             rf"T = \frac{{2\pi}}{{\omega}} \approx {T:.3f}\ \text{{秒}}")
    st.markdown("#### 動摩擦があるとき")
    st.markdown(
        r"動く向きと反対に一定の摩擦力 $\mu mg$ がはたらくので、つり合いの位置が $d = \dfrac{\mu mg}{k}$ だけずれた単振動を、"
        r"半周期ごとにつなげた動きになります（周期は変わらない）。片道ごとに振幅が $2d$ 減り、"
        r"折り返した位置が $|x| \le d$ の範囲に入ると、ばねの力 $k|x|$ が摩擦力 $\mu mg$ 以下になって止まります。"
    )
    st.latex(r"a_0 = x_0,\quad a_{n+1} = a_n - \frac{2\mu mg}{k}\quad(\text{等差数列})")
    st.markdown("#### 速さに比例する抵抗があるとき")
    st.latex(r"x = x_0\,e^{-\gamma t}\left(\cos\omega' t + \frac{\gamma}{\omega'}\sin\omega' t\right),\qquad \omega' = \sqrt{\omega^2 - \gamma^2}")
    st.markdown(r"$e^{-\gamma t}$ は時間とともに一定の割合で小さくなる数（指数関数）。折り返すたびに振幅は同じ割合で小さくなる（**等比数列**）。"
                r"この式の後ろの部分は、三角関数の合成（$a\sin + b\cos$）の形になっている。")
    st.markdown("#### 波の式")
    st.latex(r"y = A\sin 2\pi\left(\frac{t}{T} - \frac{x}{\lambda}\right)")
    st.markdown(
        r"- 場所 $x$ を決めると、時間 $t$ について周期 $T$ の単振動。\n"
        r"- 時刻 $t$ を決めると、場所 $x$ について周期 $\lambda$（波長）の sin のグラフ（波形）。\n"
        r"- 波形は 1 周期 $T$ の間に 1 波長 $\lambda$ 進むので、波の速さは $v = \dfrac{\lambda}{T} = f\lambda$。\n"
        r"- 「一般形」のページの $y = A\sin B(x - t_0)$ で、ずらす量 $t_0$ が時間とともに増えていくのが進む波。"
    )
