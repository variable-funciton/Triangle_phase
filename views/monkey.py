"""モンキーハンティング — 狙って投げると、同時に落ちる物体に必ず当たる？"""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.monkey import G, HIT_RADIUS, Shot, aim_angle_deg, hit_height, v_min
from explain.monkey import render as render_explain

C_A, C_B, C_GHOST, C_FALL = "#1f77b4", "#d62728", "#9aa0a6", "#2ca02c"


def animated(shot: Shot, speed: float = 1.0, show_ghost: bool = True, height: int = 520):
    """A と B を同時に動かすアニメーション（当たったらその瞬間で止める）"""
    a, b = shot.a, shot.b
    T = shot.end_time()
    n = 80
    times = np.linspace(0, T, n)
    res = shot.result()
    peak = max(shot.pos_a(t)[1] for t in np.linspace(0, shot.a_landing_time(), 60))
    y_top = max(b, peak) * 1.2 + 0.5
    x_right = max(a * 1.12, a + 2)

    # 静止した部分：狙いの直線、B の最初の位置、B がいる柱
    ext = 1.08
    static = [
        go.Scatter(x=[0, a * ext], y=[0, b * ext], mode="lines", name="狙いの直線（O → (a, b)）",
                   line=dict(color=C_GHOST, dash="dash", width=1.5), hoverinfo="skip"),
        go.Scatter(x=[a, a], y=[0, b], mode="lines", showlegend=False,
                   line=dict(color="#c8b89a", width=6), opacity=0.5, hoverinfo="skip"),
        go.Scatter(x=[a], y=[b], mode="markers", name="B の最初の位置 (a, b)",
                   marker=dict(color="white", size=14, line=dict(color=C_B, width=2)), hoverinfo="skip"),
    ]

    def dyn(t):
        ts = np.linspace(0, min(t, shot.a_landing_time()), 60)
        path = np.array([shot.pos_a(s) for s in ts])
        ax, ay = shot.pos_a(t)
        bx, by = shot.pos_b(t)
        gx, gy = shot.ghost_a(t)
        fall_a, fall_b = gy - ay, b - by
        hit_now = res["hit"] and t >= res["t"] - 1e-9
        vis = 1.0 if show_ghost else 0.0
        return [
            go.Scatter(x=path[:, 0], y=path[:, 1], mode="lines", line=dict(color=C_A, width=3),
                       showlegend=False, hoverinfo="skip"),
            go.Scatter(x=[ax], y=[ay], mode="markers", showlegend=False,
                       marker=dict(color=C_A, size=15, line=dict(color="white", width=1.5)),
                       hovertemplate="A (%{x:.2f}, %{y:.2f})<extra></extra>"),
            go.Scatter(x=[bx], y=[by], mode="markers", showlegend=False,
                       marker=dict(color=C_B, size=17, symbol="square", line=dict(color="white", width=1.5)),
                       hovertemplate="B (%{x:.2f}, %{y:.2f})<extra></extra>"),
            go.Scatter(x=[gx], y=[gy], mode="markers", showlegend=False, opacity=vis,
                       marker=dict(color="white", size=12, line=dict(color=C_A, width=2, )), hoverinfo="skip"),
            go.Scatter(x=[gx, ax], y=[gy, ay], mode="lines", showlegend=False, opacity=vis,
                       line=dict(color=C_FALL, width=3), hoverinfo="skip"),
            go.Scatter(x=[a, bx], y=[b, by], mode="lines", showlegend=False, opacity=vis,
                       line=dict(color=C_FALL, width=3), hoverinfo="skip"),
            go.Scatter(x=[gx, a], y=[(gy + ay) / 2, (b + by) / 2], mode="text", showlegend=False, opacity=vis,
                       text=[f"{fall_a:.2f} m", f"{fall_b:.2f} m"] if t > 0 else ["", ""],
                       textposition=["middle left", "middle right"],
                       textfont=dict(color=C_FALL, size=13), hoverinfo="skip"),
            go.Scatter(x=[ax] if hit_now else [], y=[ay] if hit_now else [], mode="markers+text",
                       showlegend=False, text=["命中！"], textposition="top center",
                       textfont=dict(size=18, color="#d62728"),
                       marker=dict(symbol="star", size=34, color="#ffbf00", line=dict(color="#d62728", width=2)),
                       hoverinfo="skip"),
        ]

    first = dyn(0.0)
    idx = list(range(len(static), len(static) + len(first)))
    fig = go.Figure(data=static + first,
                    frames=[go.Frame(name=str(i), data=dyn(t), traces=idx) for i, t in enumerate(times)])
    # 凡例用のダミー（動く要素の説明）
    for name, kw in [("A（投げた物体）", dict(color=C_A, size=12)),
                     ("B（自由落下する物体）", dict(color=C_B, size=12, symbol="square")),
                     ("重力がないときの A", dict(color="white", size=10, line=dict(color=C_A, width=2))),
                     ]:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name=name, marker=kw))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="重力で落ちた距離 ½gt²",
                             line=dict(color=C_FALL, width=3)))
    dur = max(20, int(T / n * 1000 / speed))
    step = dict(frame=dict(duration=0, redraw=False), transition=dict(duration=0), mode="immediate")
    fig.update_layout(
        height=height, template="plotly_white", margin=dict(l=10, r=10, t=40, b=100),
        legend=dict(orientation="h", y=1.12, font=dict(size=12)),
        updatemenus=[dict(type="buttons", direction="left", showactive=False, x=0, xanchor="left", y=-0.14,
                          yanchor="top", pad=dict(t=10, r=10), buttons=[
                              dict(label="▶ 発射", method="animate",
                                   args=[None, dict(frame=dict(duration=dur, redraw=False),
                                                    transition=dict(duration=0), mode="immediate", fromcurrent=True)]),
                              dict(label="⏸ 停止", method="animate", args=[[None], step]),
                          ])],
        sliders=[dict(active=0, x=0.2, len=0.8, y=-0.14, yanchor="top", pad=dict(t=10),
                      currentvalue=dict(prefix="t = ", suffix=" 秒", font=dict(size=14)),
                      font=dict(color="rgba(0,0,0,0)"), ticklen=2,
                      steps=[dict(method="animate", label=f"{t:.3f}", args=[[str(i)], step])
                             for i, t in enumerate(times)])],
    )
    fig.update_xaxes(range=[-0.04 * x_right, x_right], title_text="x [m]", zeroline=True, zerolinecolor="black")
    fig.update_yaxes(range=[-0.04 * y_top, y_top], title_text="y [m]", scaleanchor="x", scaleratio=1,
                     zeroline=True, zerolinecolor="black")
    return fig


def result_message(shot: Shot):
    r = shot.result()
    if r["hit"]:
        st.success(f"**命中！**　t = {r['t']:.3f} 秒、高さ {r['y']:.2f} m の位置でぶつかりました。")
    elif r["reason"] == "A_landed":
        st.error(f"**外れ**　A は x = a に届く前に地面に落ちました（t = {r['t']:.3f} 秒、x = {r['x']:.2f} m）。"
                 "B も地面に落ちてしまい、空中でぶつかれません。初速度が足りません。")
    elif r["reason"] == "B_landed":
        st.error("**外れ**　A が x = a に届く前に、B が地面に着いてしまいました。")
    elif r["reason"] == "above":
        st.warning(f"**外れ**　A は B の **上** を {r['gap']:.2f} m 離れて通りすぎました（t = {r['t']:.3f} 秒）。")
    else:
        st.warning(f"**外れ**　A は B の **下** を {-r['gap']:.2f} m 離れて通りすぎました（t = {r['t']:.3f} 秒）。")


# =====================================================================
# サイドバー
# =====================================================================
st.sidebar.header("設定")
a = st.sidebar.slider("B までの水平距離 a [m]", 5, 30, 20, key="mk_a")
b = st.sidebar.slider("B の高さ b [m]", 2, 20, 10, key="mk_b")
v0 = st.sidebar.slider("A の初速度 v₀ [m/s]", 5, 50, 20, key="mk_v0")
speed = st.sidebar.select_slider("再生の速さ", options=[0.25, 0.5, 1.0], value=0.5, key="mk_speed",
                                 format_func=lambda s: {0.25: "1/4（スロー）", 0.5: "1/2", 1.0: "実際の速さ"}[s])
vm = v_min(a, b)
theta = aim_angle_deg(a, b)
st.sidebar.metric("当たるための最小の初速度", f"{vm:.2f} m/s")
st.sidebar.caption(f"g = {G} m/s²、空気抵抗なし。高さの差が {HIT_RADIUS} m 以内なら「当たり」とする。")

st.title("モンキーハンティング")
st.markdown(
    "原点 O から物体 A を **点 (a, b) に向けて** 投げます。投げると **同時に**、(a, b) にいる物体 B が自由落下を始めます。"
    "A は B に当たるでしょうか？"
)
m = st.columns(4)
m[0].metric("狙う角度 θ", f"{theta:.1f}°", help="tan θ = b / a")
m[1].metric("O から (a, b) までの距離", f"{math.hypot(a, b):.2f} m")
m[2].metric("ぶつかるまでの時間 t*", f"{math.hypot(a, b) / v0:.3f} 秒", help="t* = √(a² + b²) / v₀")
m[3].metric("ぶつかる高さ", f"{hit_height(a, b, v0):.2f} m" if hit_height(a, b, v0) >= 0 else "地面より下（外れ）")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["① 発射してみる", "② 当たる条件", "③ 条件を崩すと？", "④ 式で確かめる", "⑤ 📖 詳しい解説"])

# ---------------- ① 発射してみる ----------------
with tab1:
    show_ghost = st.checkbox("重力がないときの A の位置と、落ちた距離 ½gt² を表示", value=True, key="mk_ghost")
    shot = Shot(a, b, v0)
    result_message(shot)
    st.plotly_chart(animated(shot, speed, show_ghost), key=f"mk_main_{a}_{b}_{v0}_{speed}_{show_ghost}")
    st.markdown(
        "- 白い丸は **重力がなかったら A がいる位置**（狙いの直線の上をまっすぐ進む）。\n"
        "- 緑の線が **重力で落ちた距離**。A も B も、同じ時刻には **同じ長さ ½gt²** だけ落ちている。\n"
        "- だから、A がちょうど x = a に着いたとき、A と B は **同じ高さ** にいる → ぶつかる。"
    )
    if v0 < vm:
        st.info(f"初速度を {vm:.2f} m/s より大きくすると、地面に落ちる前にぶつかります。")

# ---------------- ② 当たる条件 ----------------
with tab2:
    st.markdown(r"狙いどおり・同時に放せば、ぶつかる高さは $\;h = b - \dfrac{g(a^2 + b^2)}{2v_0^2}\;$。"
                r"これが **0 より大きい**（地面より上）なら空中で当たります。")
    vs = np.linspace(max(1.0, vm * 0.45), vm * 3, 300)
    hs = [hit_height(a, b, v) for v in vs]
    fig2 = go.Figure()
    fig2.add_hrect(y0=min(hs) - 1, y1=0, fillcolor="#d62728", opacity=0.07, line_width=0,
                   annotation_text="外れ（地面より下）", annotation_position="bottom right")
    fig2.add_trace(go.Scatter(x=vs, y=hs, mode="lines", name="ぶつかる高さ h", line=dict(color=C_A, width=3),
                              hovertemplate="v₀ = %{x:.2f} m/s<br>h = %{y:.2f} m<extra></extra>"))
    fig2.add_hline(y=b, line_dash="dot", line_color=C_B, annotation_text=f"B の最初の高さ b = {b} m",
                   annotation_position="top left")
    fig2.add_vline(x=vm, line_dash="dash", line_color="#2ca02c",
                   annotation_text=f"v_min = {vm:.2f} m/s", annotation_position="top right")
    h_now = hit_height(a, b, v0)
    if vs[0] <= v0 <= vs[-1]:
        fig2.add_trace(go.Scatter(x=[v0], y=[h_now], mode="markers", name="いまの初速度",
                                  marker=dict(color=C_B, size=13), hoverinfo="skip"))
    fig2.update_layout(height=420, template="plotly_white", margin=dict(l=10, r=10, t=40, b=10),
                       legend=dict(orientation="h", y=1.12))
    fig2.update_xaxes(title_text="初速度 v₀ [m/s]")
    fig2.update_yaxes(title_text="ぶつかる高さ h [m]", range=[min(min(hs), -b * 0.5), b * 1.15])
    st.plotly_chart(fig2, key="mk_cond")
    st.markdown("**当たる条件**（h > 0）を整理すると")
    st.latex(r"v_0 > \sqrt{\frac{g(a^2 + b^2)}{2b}}")
    st.latex(rf"\text{{いまの設定：}}\ \sqrt{{\frac{{{G}\times({a}^2 + {b}^2)}}{{2\times {b}}}}} \approx {vm:.2f}\ \text{{m/s}}")
    st.markdown(
        "- 初速度が大きいほど早く着くので、B があまり落ちないうちに **高い位置** でぶつかる。\n"
        "- 初速度を限りなく大きくすると、ぶつかる高さは b に近づく（グラフの点線）。\n"
        "- 初速度が v_min より小さいと、空中でぶつかる前に地面に落ちてしまう。"
    )

# ---------------- ③ 条件を崩すと？ ----------------
with tab3:
    st.markdown("モンキーハンティングで当たるには **「B を狙って投げる」「B と同時に放す」** の 2 つが必要です。片方を崩してみよう。")
    c1, c2 = st.columns(2)
    off = c1.slider("狙いのずれ（上向きが＋）[°]", -10, 10, 3, key="mk_off")
    delay = c2.select_slider("B を放すのが遅れる時間 [秒]", options=[round(0.05 * k, 2) for k in range(0, 21)],
                             value=0.0, key="mk_delay")
    shot3 = Shot(a, b, max(v0, math.ceil(vm) + 2), offset_deg=off, delay=delay)
    if v0 < vm:
        st.caption(f"※ 初速度が足りないので、このタブでは v₀ = {shot3.v0:.0f} m/s で試しています。")
    result_message(shot3)
    st.plotly_chart(animated(shot3, speed, True), key=f"mk_break_{a}_{b}_{shot3.v0}_{off}_{delay}_{speed}")
    st.markdown(
        "- **狙いが上にずれる** → A は B の上を通る。**下にずれる** → 下を通る。\n"
        "- **B を放すのが遅れる** → B が落ち始めるのが遅いぶん高い位置に残り、A は B の下を通る。\n"
        "- どちらも 0 にすると、必ず当たる（初速度が十分なら）。"
    )

# ---------------- ④ 式で確かめる ----------------
with tab4:
    st.markdown(r"**手順1** 狙う角度 $\theta$ は、点 $(a, b)$ を見上げる角")
    st.latex(r"\tan\theta = \frac{b}{a},\qquad \cos\theta = \frac{a}{\sqrt{a^2 + b^2}},\qquad \sin\theta = \frac{b}{\sqrt{a^2 + b^2}}")
    st.markdown("**手順2** A と B の運動")
    st.latex(r"\text{A：}\ x = v_0\cos\theta\cdot t,\quad y = v_0\sin\theta\cdot t - \frac{1}{2}gt^2"
             r"\qquad \text{B：}\ x = a,\quad y = b - \frac{1}{2}gt^2")
    st.markdown("**手順3** A が x = a に着く時刻 t*")
    st.latex(r"v_0\cos\theta\cdot t^* = a \;\Longrightarrow\; t^* = \frac{a}{v_0\cos\theta} = \frac{\sqrt{a^2 + b^2}}{v_0}")
    st.markdown("**手順4** そのときの A の高さ")
    st.latex(r"y_A = v_0\sin\theta\cdot t^* - \frac{1}{2}g{t^*}^2 = v_0\cdot\frac{b}{\sqrt{a^2+b^2}}\cdot\frac{\sqrt{a^2+b^2}}{v_0}"
             r" - \frac{1}{2}g{t^*}^2 = b - \frac{1}{2}g{t^*}^2")
    st.markdown(r"これは **B の高さ $y_B = b - \frac{1}{2}g{t^*}^2$ と同じ**。よって A と B は同じ位置にいる → ぶつかる。")
    st.markdown(r"**手順5** ただし、ぶつかる高さが地面より上（$y_A > 0$）でなければならない")
    st.latex(r"b - \frac{1}{2}g\cdot\frac{a^2 + b^2}{v_0^2} > 0 \;\Longleftrightarrow\; v_0 > \sqrt{\frac{g(a^2+b^2)}{2b}}")
    st.latex(rf"\text{{いまの値：}}\ t^* = \frac{{\sqrt{{{a}^2 + {b}^2}}}}{{{v0}}} \approx {math.hypot(a, b) / v0:.3f}\ \text{{秒}},"
             rf"\quad y = {b} - \frac{{1}}{{2}}\cdot {G}\cdot {math.hypot(a, b) / v0:.3f}^2 \approx {hit_height(a, b, v0):.2f}\ \text{{m}}")
    with st.expander("別の見方：B と一緒に落ちる人から見ると？"):
        st.markdown(
            "B と一緒に自由落下する人から見ると、重力の影響は A にも B にも同じようにはたらくので打ち消し合い、"
            "**A は B に向かってまっすぐ等速で進んでくる** ように見えます。"
            "最初に B を狙って投げているので、必ず B に届きます（ただし、それまでに地面に着かなければ）。"
        )

# =====================================================================
# ⑤ 詳しい解説
# =====================================================================
with tab5:
    render_explain(a, b, v0)
