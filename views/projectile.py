"""斜方投射のシミュレーション — 三角関数の応用（2倍角の公式で 45° が最大になる理由）"""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.projectile import G, flight_time, max_height, position, range_, trajectory, velocity

ANGLE_COLORS = {15: "#9467bd", 30: "#1f77b4", 45: "#d62728", 60: "#2ca02c", 75: "#ff7f0e"}


def deg_label(th: float) -> str:
    """角度の表示（有名角は π 表記も添える）"""
    pi = {15: "π/12", 30: "π/6", 45: "π/4", 60: "π/3", 75: "5π/12", 90: "π/2"}
    return f"{th:g}°" + (f"（{pi[int(th)]}）" if float(th).is_integer() and int(th) in pi else "")


def animated_figure(balls, v0, show_velocity=False, height=480, key_scale=1.0):
    """balls: [dict(theta, name, color, width)] を同じ時間軸で同時に投げるアニメーション"""
    T_all = max(flight_time(v0, b["theta"]) for b in balls)
    n = 90
    times = np.linspace(0, T_all, n)
    L_max = v0 ** 2 / G
    H_max = max(max_height(v0, b["theta"]) for b in balls)

    static = []
    for b in balls:
        x, y = trajectory(v0, b["theta"])
        static.append(go.Scatter(x=x, y=y, mode="lines", name=b["name"], legendgroup=b["name"],
                                 line=dict(color=b["color"], width=1.2, dash="dot"), opacity=0.6,
                                 hoverinfo="skip"))

    def dynamic(t):
        out = []
        for b in balls:
            ts = np.linspace(0, min(t, flight_time(v0, b["theta"])), 80)
            x, y = position(v0, b["theta"], ts)
            out.append(go.Scatter(x=x, y=y, mode="lines", line=dict(color=b["color"], width=b["width"]),
                                  showlegend=False, legendgroup=b["name"], hoverinfo="skip"))
            out.append(go.Scatter(x=[x[-1]], y=[y[-1]], mode="markers", showlegend=False, legendgroup=b["name"],
                                  marker=dict(color=b["color"], size=13, line=dict(color="white", width=1.5)),
                                  hovertemplate=f"{b['name']}<br>x = %{{x:.1f}} m<br>y = %{{y:.1f}} m<extra></extra>"))
        if show_velocity:
            b = balls[0]
            px, py = position(v0, b["theta"], t)
            vx, vy = velocity(v0, b["theta"], t)
            s = 0.25 * key_scale * L_max / v0  # 矢印の長さの倍率
            px, py = float(px), float(py)
            out.append(go.Scatter(x=[px, px + vx * s], y=[py, py], mode="lines",
                                  line=dict(color="#2ca02c", width=3), showlegend=False, hoverinfo="skip"))
            out.append(go.Scatter(x=[px, px], y=[py, py + vy * s], mode="lines",
                                  line=dict(color="#ff7f0e", width=3), showlegend=False, hoverinfo="skip"))
            out.append(go.Scatter(x=[px, px + vx * s], y=[py, py + vy * s], mode="lines",
                                  line=dict(color="black", width=2), showlegend=False, hoverinfo="skip"))
        return out

    first = dynamic(0.0)
    idx = list(range(len(static), len(static) + len(first)))
    fig = go.Figure(data=static + first,
                    frames=[go.Frame(name=str(i), data=dynamic(t), traces=idx) for i, t in enumerate(times)])
    dur = max(20, int(T_all / n * 1000))   # 実時間に近い速さ
    step = dict(frame=dict(duration=0, redraw=False), transition=dict(duration=0), mode="immediate")
    fig.update_layout(
        height=height, template="plotly_white", margin=dict(l=10, r=10, t=30, b=100),
        legend=dict(orientation="h", y=1.1),
        updatemenus=[dict(type="buttons", direction="left", showactive=False, x=0, xanchor="left", y=-0.14,
                          yanchor="top", pad=dict(t=10, r=10), buttons=[
                              dict(label="▶ 投げる", method="animate",
                                   args=[None, dict(frame=dict(duration=dur, redraw=False),
                                                    transition=dict(duration=0), mode="immediate", fromcurrent=True)]),
                              dict(label="⏸ 停止", method="animate", args=[[None], step]),
                          ])],
        sliders=[dict(active=0, x=0.2, len=0.8, y=-0.14, yanchor="top", pad=dict(t=10),
                      currentvalue=dict(prefix="t = ", suffix=" 秒", font=dict(size=14)),
                      font=dict(color="rgba(0,0,0,0)"), ticklen=2,
                      steps=[dict(method="animate", label=f"{t:.2f}", args=[[str(i)], step])
                             for i, t in enumerate(times)])],
    )
    fig.update_xaxes(range=[-0.02 * L_max, 1.08 * L_max], title_text="水平距離 x [m]", zeroline=True,
                     zerolinecolor="black")
    fig.update_yaxes(range=[-0.02 * L_max, max(H_max * 1.25, 0.15 * L_max)], title_text="高さ y [m]",
                     scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="black")
    return fig


# =====================================================================
# サイドバー
# =====================================================================
st.sidebar.header("投げ方")
v0 = st.sidebar.slider("初速度 v₀ [m/s]", 5, 40, 20, key="pj_v0")
theta = st.sidebar.slider("投げ上げる角度 θ [°]（水平方向とのなす角）", 1, 89, 30, key="pj_theta")
st.sidebar.caption(f"重力加速度 g = {G} m/s²、空気抵抗は考えない。地面の高さから投げる。")

T, H, L = flight_time(v0, theta), max_height(v0, theta), range_(v0, theta)
L45 = range_(v0, 45)

st.title("斜方投射：45° で投げると一番遠くまで飛ぶのはなぜ？")
st.markdown(
    r"初速度 $v_0$ を **水平方向** と **鉛直方向** に分けると、$v_0\cos\theta$ と $v_0\sin\theta$。"
    r"水平方向は等速、鉛直方向は重力で減速します。"
)
st.latex(r"x = v_0\cos\theta \cdot t,\qquad y = v_0\sin\theta \cdot t - \frac{1}{2}g t^2")

m = st.columns(4)
m[0].metric("角度 θ", deg_label(theta))
m[1].metric("飛距離 L", f"{L:.2f} m", delta=f"45° との差 {L - L45:+.2f} m", delta_color="off")
m[2].metric("最高点の高さ H", f"{H:.2f} m")
m[3].metric("滞空時間 T", f"{T:.2f} 秒")
if theta == 45:
    st.success(f"θ = 45°（π/4）は、この初速度で投げられる **最大の飛距離 {L45:.2f} m** です。")
else:
    st.info(f"同じ初速度 {v0} m/s でも、45° で投げれば {L45:.2f} m まで飛びます（今の角度では {L / L45:.1%}）。"
            f"　また、{90 - theta}° で投げても飛距離は同じ {L:.2f} m です。")

tab1, tab2, tab3, tab4 = st.tabs(["① 投げてみる", "② 角度を変えて比べる", "③ 飛距離のグラフ", "④ 式で確かめる"])

# ---------------- ① 投げてみる ----------------
with tab1:
    o1, o2 = st.columns(2)
    with45 = o1.checkbox("45° のボールも同時に投げる", value=theta != 45, key="pj_with45")
    show_v = o2.checkbox("速度ベクトル（水平・鉛直成分）を表示", value=True, key="pj_showv")
    balls = [dict(theta=theta, name=f"θ = {theta}°", color=ANGLE_COLORS.get(theta, "#1f77b4"),
                  width=3.5)]
    if with45 and theta != 45:
        balls.append(dict(theta=45, name="θ = 45°", color=ANGLE_COLORS[45], width=3))
    fig = animated_figure(balls, v0, show_velocity=show_v)
    fig.add_vline(x=L, line_dash="dash", line_color=balls[0]["color"],
                  annotation_text=f"L = {L:.1f} m", annotation_position="top")
    if len(balls) > 1:
        fig.add_vline(x=L45, line_dash="dash", line_color=ANGLE_COLORS[45],
                      annotation_text=f"45°: {L45:.1f} m", annotation_position="top right")
    st.plotly_chart(fig, key=f"pj_anim_{v0}_{theta}_{with45}_{show_v}")
    if show_v:
        st.caption("緑：水平方向の速度 v₀cosθ（ずっと一定）、橙：鉛直方向の速度 v₀sinθ − gt（最高点で 0、そのあと下向き）、"
                   "黒：実際の速度。")

# ---------------- ② 角度を変えて比べる ----------------
with tab2:
    st.markdown(f"初速度 {v0} m/s のまま、15° きざみの 5 つの角度で **同時に** 投げます。")
    balls2 = [dict(theta=a, name=f"{a}°", color=c, width=4 if a == 45 else 2.5) for a, c in ANGLE_COLORS.items()]
    fig2 = animated_figure(balls2, v0, height=500)
    for a in ANGLE_COLORS:
        fig2.add_trace(go.Scatter(x=[range_(v0, a)], y=[0], mode="markers", showlegend=False,
                                  marker=dict(color=ANGLE_COLORS[a], size=9, symbol="x"), hoverinfo="skip"))
    st.plotly_chart(fig2, key=f"pj_compare_{v0}")
    rows = "| 角度 θ | 滞空時間 T | 最高点 H | 飛距離 L |\n|:--:|:--:|:--:|:--:|\n"
    for a in ANGLE_COLORS:
        mark = " ⭐ **最大**" if a == 45 else ""
        rows += f"| {deg_label(a)} | {flight_time(v0, a):.2f} 秒 | {max_height(v0, a):.2f} m | {range_(v0, a):.2f} m{mark} |\n"
    st.markdown(rows)
    st.markdown(
        "- **45° が一番遠い**。\n"
        "- **30° と 60°、15° と 75° は同じ場所に落ちる**（足して 90° になる角＝余角）。高く上がる 60° のほうが滞空時間は長い。\n"
        "- 角度を大きくすると高く・長く飛ぶが、横に進む速さ v₀cosθ が小さくなるので、遠くへは行かない。"
    )

# ---------------- ③ 飛距離のグラフ ----------------
with tab3:
    ths = np.linspace(0, 90, 361)
    Ls = [range_(v0, t) for t in ths]
    Hs = [max_height(v0, t) for t in ths]
    show_h = st.checkbox("最高点の高さ H(θ) も表示", value=False, key="pj_showh")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=ths, y=Ls, mode="lines", name="飛距離 L(θ) = v₀² sin 2θ / g",
                              line=dict(color="#1f77b4", width=3),
                              hovertemplate="θ = %{x:.1f}°<br>L = %{y:.2f} m<extra></extra>"))
    if show_h:
        fig3.add_trace(go.Scatter(x=ths, y=Hs, mode="lines", name="最高点 H(θ) = v₀² sin²θ / 2g",
                                  line=dict(color="#2ca02c", width=2, dash="dash"),
                                  hovertemplate="θ = %{x:.1f}°<br>H = %{y:.2f} m<extra></extra>"))
    fig3.add_trace(go.Scatter(x=[45], y=[L45], mode="markers+text", name="最大（θ = 45°）",
                              marker=dict(color="#d62728", size=15, symbol="star"),
                              text=[f"45° で最大 {L45:.1f} m"], textposition="top center", hoverinfo="skip"))
    fig3.add_trace(go.Scatter(x=[theta, 90 - theta], y=[L, L], mode="markers", name=f"{theta}° と {90 - theta}°",
                              marker=dict(color="black", size=11), hoverinfo="skip"))
    fig3.add_shape(type="line", x0=theta, x1=90 - theta, y0=L, y1=L, line=dict(color="black", dash="dot"))
    fig3.add_vline(x=45, line_dash="dash", line_color="#d62728", line_width=1)
    fig3.update_layout(height=430, template="plotly_white", margin=dict(l=10, r=10, t=40, b=10),
                       legend=dict(orientation="h", y=1.12))
    fig3.update_xaxes(title_text="角度 θ [°]", range=[0, 90], tickvals=[0, 15, 30, 45, 60, 75, 90],
                      ticktext=["0", "15°", "30°", "45°<br>(π/4)", "60°", "75°", "90°"])
    fig3.update_yaxes(title_text="[m]", range=[0, L45 * 1.2])
    st.plotly_chart(fig3, key="pj_rangecurve")
    st.markdown(
        r"飛距離のグラフは $\sin 2\theta$ の形（**$\theta = 45^\circ$ を軸に左右対称な山**）。"
        r"山の頂上が $45^\circ$、同じ高さの点の組（黒い点）が余角 $\theta$ と $90^\circ - \theta$ です。"
    )

# ---------------- ④ 式で確かめる ----------------
with tab4:
    st.markdown("**手順1** 地面に落ちる時刻 T を求める（y = 0）")
    st.latex(r"v_0\sin\theta\cdot t - \frac{1}{2}g t^2 = 0 \;\Longrightarrow\; t\left(v_0\sin\theta - \frac{g}{2}t\right) = 0"
             r"\;\Longrightarrow\; T = \frac{2v_0\sin\theta}{g}")
    st.markdown("**手順2** その間に水平に進む距離が飛距離 L")
    st.latex(r"L = v_0\cos\theta \cdot T = \frac{2v_0^2\sin\theta\cos\theta}{g}")
    st.markdown(r"**手順3** **2倍角の公式** $\sin 2\theta = 2\sin\theta\cos\theta$ を使う（後期課題7）")
    st.latex(r"L = \frac{v_0^2}{g}\,\sin 2\theta")
    st.markdown(r"**手順4** $0^\circ < \theta < 90^\circ$ のとき $0^\circ < 2\theta < 180^\circ$。"
                r"$\sin 2\theta$ が最大値 $1$ をとるのは $2\theta = 90^\circ$、つまり")
    st.latex(r"\theta = 45^\circ = \frac{\pi}{4} \text{ のとき最大}\qquad L_{\max} = \frac{v_0^2}{g}")
    st.latex(rf"\text{{いまの初速度}}\ v_0 = {v0}\ \text{{のとき}}\quad L_{{\max}} = \frac{{{v0}^2}}{{{G}}} \approx {L45:.2f}\ \text{{m}}")
    st.markdown(r"**手順5** 余角で飛距離が同じになる理由：$\sin(180^\circ - 2\theta) = \sin 2\theta$ より")
    st.latex(r"L(90^\circ - \theta) = \frac{v_0^2}{g}\sin(180^\circ - 2\theta) = \frac{v_0^2}{g}\sin 2\theta = L(\theta)")
    st.latex(rf"\text{{いまの値：}}\ L({theta}^\circ) = \frac{{{v0}^2}}{{{G}}}\sin {2 * theta}^\circ \approx {L:.2f}\ \text{{m}}")
    with st.expander("最高点の高さ H も求めてみよう"):
        st.latex(r"t = \frac{T}{2} = \frac{v_0\sin\theta}{g}\ \text{で最高点}\quad\Longrightarrow\quad "
                 r"H = \frac{v_0^2\sin^2\theta}{2g}")
        st.markdown(r"$H$ は $\theta$ が大きいほど高い（$\theta = 90^\circ$ の真上投げで最大）。"
                    r"**遠くへ飛ばす角（45°）と高く上げる角（90°）は違う** ことに注意。")
    with st.expander("現実のスポーツでは？"):
        st.markdown(
            "- 実際は **空気抵抗** があるので、最も遠くへ飛ぶ角度は 45° より小さくなることが多い。\n"
            "- 砲丸投げのように **高い位置から投げる** 場合も、最適な角度は 45° より小さくなる。\n"
            "- このページは「空気抵抗なし・地面から投げる」という理想化したモデルで考えている。"
        )
