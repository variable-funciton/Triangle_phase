"""三角関数の一般形 y = A f(B(x − t)) + β の動くグラフ（後期課題4〜6 対応）"""

from fractions import Fraction as F

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.angles import angle_latex, angle_text, frac_latex, frac_text, pi_latex
from utils.plotting import (
    COLORS, add_period_band, add_range_lines, add_shift_arrows, curve, key_marker,
    style_axes, x_grid, x_range_pi, y_limit,
)
from utils.trig import Wave

# ---------------- パラメータの選択肢 ----------------
A_OPTIONS = [F(-3), F(-2), F(-3, 2), F(-1), F(-1, 2), F(1, 2), F(1), F(3, 2), F(2), F(3)]
B_OPTIONS = [F(1, 3), F(1, 2), F(2, 3), F(1), F(3, 2), F(2), F(3), F(4)]
T_OPTIONS = [F(k, 12) for k in range(-24, 25)]          # −2π 〜 2π を π/12 刻み
BETA_OPTIONS = [F(k, 2) for k in range(-4, 5)]           # −2 〜 2 を 1/2 刻み
DEFAULTS = {"gf_A": F(1), "gf_B": F(1), "gf_t": F(0), "gf_t_rad": 0.0, "gf_t_deg": 0, "gf_beta": F(0)}

for key, val in DEFAULTS.items():
    st.session_state.setdefault(key, val)


def reset_params():
    for key, val in DEFAULTS.items():
        st.session_state[key] = val


def symbolic_latex(wv: Wave, param: str) -> str:
    """アニメーションで動かすパラメータだけ文字（A, B, t, β）のまま残した式"""
    fn = rf"\{wv.func}"
    As = "A" if param == "A" else ("" if wv.A == 1 else "-" if wv.A == -1 else frac_latex(wv.A))
    Bs = "B" if param == "B" else ("" if wv.B == 1 else frac_latex(wv.B))
    if param == "t":
        xs = "x - t"
    elif wv.t == 0:
        xs = "x"
    else:
        xs = "x" + (" - " if wv.t > 0 else " + ") + pi_latex(abs(wv.t))
    inner = (f" {Bs}x" if Bs else " x") if xs == "x" else (f" {Bs}" if Bs else "") + rf"\left({xs}\right)"
    cs = r" + \beta" if param == "beta" else (
        "" if wv.beta == 0 else (" + " if wv.beta > 0 else " - ") + frac_latex(abs(wv.beta)))
    return rf"y = {As}{fn}{inner}{cs}"


st.title("三角関数の一般形と平行移動")
st.markdown(
    r"$y = A\sin B(x - t) + \beta$ の 4 つのパラメータを動かして、"
    r"**振幅・周期・平行移動** がグラフにどう表れるか確かめよう。"
)

# ---------------- パラメータ（グラフのすぐ上に置く。スマートフォンでも見えるように） ----------------
with st.container(border=True):
    r1 = st.columns([2, 2, 3, 1.4])
    func = r1[0].radio("基本の関数", ["sin", "cos"], horizontal=True, format_func=lambda s: f"{s} x", key="gf_func")
    unit = r1[1].radio("角度の単位", ["rad", "deg"], horizontal=True, key="gf_unit",
                       format_func=lambda u: "弧度法" if u == "rad" else "度数法")
    t_mode = r1[2].radio("t の入れ方", ["pi", "dec"], horizontal=True, key="gf_tmode",
                         format_func=lambda m: ("π の倍数（π/12 きざみ）" if unit == "rad" else "15° きざみ")
                         if m == "pi" else ("小数（ラジアン）" if unit == "rad" else "1° きざみ"))
    r1[3].button("初期値に戻す", on_click=reset_params)
    r2 = st.columns(4)
    A = r2[0].select_slider("A（y 方向の倍率・振幅）", options=A_OPTIONS, key="gf_A", format_func=frac_text)
    B = r2[1].select_slider("B（x 方向の倍率 → 周期）", options=B_OPTIONS, key="gf_B", format_func=frac_text)
    if t_mode == "pi":
        t = r2[2].select_slider("t（x 方向の平行移動）", options=T_OPTIONS, key="gf_t",
                                format_func=lambda q: angle_text(q, unit))
    elif unit == "rad":
        t_rad = r2[2].slider("t（x 方向の平行移動）[rad]", -6.28, 6.28, step=0.01, key="gf_t_rad")
        t = t_rad / np.pi                                   # π 単位の小数
    else:
        t_deg = r2[2].slider("t（x 方向の平行移動）[°]", -360, 360, step=1, key="gf_t_deg")
        t = F(t_deg, 180)                                   # 度数は π の分数で正確に表せる
    beta = r2[3].select_slider("β（y 方向の平行移動）", options=BETA_OPTIONS, key="gf_beta", format_func=frac_text)

w = Wave(func, A, B, t, beta)
base = Wave(func)

# ---------------- 数式と特徴量 ----------------
formula = w.latex()
if B != 1 and t != 0:
    formula += r"\;=\; " + w.latex("expanded")[4:]
st.latex(formula)

c = st.columns(6)
c[0].metric("振幅 |A|", frac_text(w.amplitude))
c[1].metric("周期 2π/B", angle_text(w.period, unit))
c[2].metric("最大値", frac_text(w.y_max))
c[3].metric("最小値", frac_text(w.y_min))
c[4].metric("x 方向の移動 t", angle_text(t, unit))
c[5].metric("y 方向の移動 β", frac_text(beta))

tab1, tab2, tab3 = st.tabs(["① 重ねて比較", "② 段階的に変形", "③ アニメーション"])

# =====================================================================
# ① 元のグラフと重ねて比較
# =====================================================================
with tab1:
    o = st.columns(4)
    show_base = o[0].checkbox(f"y = {func} x を表示", value=True)
    show_keys = o[1].checkbox("キーポイントと矢印", value=True)
    show_band = o[2].checkbox("1周期の区間", value=True)
    show_range = o[3].checkbox("最大値・最小値の線", value=True)

    lo, hi = x_range_pi([w, base])
    x = x_grid(lo, hi)
    fig = go.Figure()
    if show_base:
        fig.add_trace(curve(x, base.y(x), f"y = {func} x", COLORS["base"], dash="dash", width=2))
    fig.add_trace(curve(x, w.y(x), "変形後のグラフ", COLORS["wave"], width=3))
    if show_keys:
        if show_base:
            fig.add_trace(key_marker(base.base_key_points(), "元のキーポイント", COLORS["base"], unit, size=8))
            add_shift_arrows(fig, base.base_key_points(), w.key_points())
        fig.add_trace(key_marker(w.key_points(), "変形後のキーポイント", COLORS["key"], unit))
    if show_band:
        add_period_band(fig, w, unit)
    if show_range:
        add_range_lines(fig, w)
    style_axes(fig, lo, hi, y_limit([w, base]), unit)
    fig.update_layout(title=dict(text=w.text(), x=0.5, xanchor="center", font=dict(size=20, color=COLORS["wave"])),
                      margin=dict(t=90))
    st.plotly_chart(fig, key="compare_chart")

    with st.expander("キーポイント（1周期を4等分した点）の対応表"):
        st.markdown(
            "元のグラフで $x_0$ にあった点は、変形後に $x = t + \\dfrac{x_0}{B}$、"
            "$y = A\\,y_0 + \\beta$ に移ります。"
        )
        head = "| | " + " | ".join(f"点{k + 1}" for k in range(5)) + " |\n"
        head += "|:--|" + ":--:|" * 5 + "\n"
        rows = [
            ("元の $x_0$", [angle_latex(q, unit) for q, _ in base.base_key_points()]),
            ("元の $y_0$", [frac_latex(v) for _, v in base.base_key_points()]),
            ("変形後の $x$", [angle_latex(q, unit) for q, _ in w.key_points()]),
            ("変形後の $y$", [frac_latex(v) for _, v in w.key_points()]),
        ]
        body = "".join(f"| {name} | " + " | ".join(f"${s}$" for s in vals) + " |\n" for name, vals in rows)
        st.markdown(head + body)

# =====================================================================
# ② 段階的に変形
# =====================================================================
with tab2:
    steps = [
        (base, rf"基本形 $y = \{func} x$（周期 $2\pi$、振幅 $1$）", True),
        (base.with_(B=B), rf"$x$ 軸方向に $\dfrac{{1}}{{B}} = {frac_latex(1 / B)}$ 倍 → 周期が "
                          rf"${angle_latex(w.period, unit)}$ になる", B != 1),
        (base.with_(B=B, t=t), rf"$x$ 軸方向に $t = {angle_latex(t, unit)}$ だけ平行移動", t != 0),
        (base.with_(B=B, t=t, A=A), rf"$y$ 軸方向に $A = {frac_latex(A)}$ 倍 → 振幅 ${frac_latex(abs(A))}$"
                                    + ("（$A<0$ なので $x$ 軸に関して上下反転）" if A < 0 else ""), A != 1),
        (w, rf"$y$ 軸方向に $\beta = {frac_latex(beta)}$ だけ平行移動", beta != 0),
    ]
    step = st.select_slider(
        "どこまで変形するか", options=list(range(5)), value=4,
        format_func=lambda i: "①②③④⑤"[i],
    )

    lo, hi = x_range_pi([s[0] for s in steps])
    x = x_grid(lo, hi)
    fig2 = go.Figure()
    for i in range(step + 1):
        wi = steps[i][0]
        if i == step:
            fig2.add_trace(curve(x, wi.y(x), f"{'①②③④⑤'[i]}", COLORS["steps"][i], width=3.2))
        elif i == step - 1:
            fig2.add_trace(curve(x, wi.y(x), f"{'①②③④⑤'[i]}", COLORS["steps"][i], dash="dash", width=2))
        else:
            fig2.add_trace(curve(x, wi.y(x), f"{'①②③④⑤'[i]}", COLORS["steps"][i], width=1.5, opacity=0.3))
    cur = steps[step][0]
    if step > 0:
        prev = steps[step - 1][0]
        fig2.add_trace(key_marker(prev.key_points(), "1つ前の点", COLORS["base"], unit, size=8))
        add_shift_arrows(fig2, prev.key_points(), cur.key_points())
    fig2.add_trace(key_marker(cur.key_points(), "現在の点", COLORS["key"], unit))
    style_axes(fig2, lo, hi, y_limit([s[0] for s in steps]), unit)
    fig2.update_layout(title=dict(text=f"{'①②③④⑤'[step]}  {cur.text()}", x=0.5, xanchor="center",
                                  font=dict(size=20, color=COLORS["steps"][step])), margin=dict(t=90))
    st.plotly_chart(fig2, key="steps_chart")

    for i, (wi, desc, changed) in enumerate(steps):
        mark = "👉 " if i == step else ""
        note = "" if changed else "（このパラメータでは変化なし）"
        text = f"{mark}**{'①②③④⑤'[i]}** {desc}{note}　→　${wi.latex()}$"
        st.markdown(text if i <= step else f":gray[{text}]")

    with st.expander("⚠️ よくある間違い：sin(Bx − t) は t だけ平行移動？（後期課題6 の位相移動型）"):
        if B == 1 or t == 0:
            st.info("B ≠ 1 かつ t ≠ 0 に設定すると、2 つのグラフの違いを比べられます。")
        else:
            wrong = w.with_(t=t / B)  # A f(Bx − t) + β と同じ
            st.markdown(
                rf"${w.latex('factored')}$ は **$x$ 方向に ${angle_latex(t, unit)}$** の移動ですが、"
                rf"${wrong.latex('expanded')}$ は $B$ でくくると "
                rf"$x$ 方向に $\dfrac{{t}}{{B}} = {angle_latex(t / B, unit)}$ の移動です。"
            )
            lo3, hi3 = x_range_pi([w, wrong])
            x3 = x_grid(lo3, hi3)
            fig3 = go.Figure()
            fig3.add_trace(curve(x3, w.y(x3), f"B(x − t) の形（移動 {angle_text(t, unit)}）", COLORS["wave"], width=3))
            fig3.add_trace(curve(x3, wrong.y(x3), f"Bx − t の形（移動 {angle_text(t / B, unit)}）",
                                 "#ff7f0e", dash="dash", width=2.5))
            fig3.add_trace(key_marker(w.key_points()[:1], "B(x − t) の始点", COLORS["wave"], unit, size=11))
            fig3.add_trace(key_marker(wrong.key_points()[:1], "Bx − t の始点", "#ff7f0e", unit, size=11))
            style_axes(fig3, lo3, hi3, y_limit([w]), unit, height=380)
            st.plotly_chart(fig3, key="mistake_chart")

# =====================================================================
# ③ アニメーション（ブラウザ側で再生するのでサーバー負荷が小さい）
# =====================================================================
with tab3:
    t_values = ([k * 0.1 / np.pi for k in range(-63, 64)] if (t_mode == "dec" and unit == "rad")
                else [F(k, 24) for k in range(-48, 49)])
    PARAMS = {
        "t": ("t（x 方向の平行移動）", t_values, lambda q: angle_text(q, unit)),
        "A": ("A（振幅）", [F(k, 4) for k in range(-12, 13)], frac_text),
        "B": ("B（周期）", [F(k, 8) for k in range(2, 33)], frac_text),
        "beta": ("β（y 方向の平行移動）", [F(k, 4) for k in range(-8, 9)], frac_text),
    }
    a1, a2, a3 = st.columns([3, 2, 2])
    param = a1.radio("動かすパラメータ", list(PARAMS), horizontal=True, format_func=lambda p: PARAMS[p][0])
    speed = a2.select_slider("速さ", options=["ゆっくり", "ふつう", "はやい"], value="ふつう")
    anim_base = a3.checkbox(f"y = {func} x も表示", value=True, key="anim_base")
    duration = {"ゆっくり": 160, "ふつう": 80, "はやい": 35}[speed]

    label, values, fmt = PARAMS[param]
    others = {k: v for k, v in dict(A=A, B=B, t=t, beta=beta).items() if k != param}
    st.caption("他のパラメータは現在の値で固定: " + "、".join(
        f"{'β' if k == 'beta' else k} = {angle_text(v, unit) if k == 't' else frac_text(v)}"
        for k, v in others.items()
    ))
    waves = [w.with_(**{param: v}) for v in values]
    lo, hi = x_range_pi(waves, cap=6.0)
    x = x_grid(lo, hi, n=600)
    ylim = y_limit(waves)
    current = {"A": A, "B": B, "t": t, "beta": beta}[param]
    init = min(range(len(values)), key=lambda i: abs(float(values[i]) - float(current)))

    st.markdown("動かしているパラメータを文字のまま残した式：")
    st.latex(symbolic_latex(w, param))

    def wave_traces(wv):
        kp = wv.key_points()
        return [
            curve(x, wv.y(x), "変形後のグラフ", COLORS["wave"], width=3),
            go.Scatter(x=[float(q) * np.pi for q, _ in kp], y=[float(v) for _, v in kp],
                       mode="markers", name="キーポイント",
                       marker=dict(color=COLORS["key"], size=10, line=dict(color="white", width=1)),
                       hoverinfo="skip"),
            # そのコマの式（パラメータに合わせて変わる）
            go.Scatter(x=[lo * np.pi + 0.05 * (hi - lo) * np.pi], y=[ylim * 0.86], mode="text",
                       text=[wv.text()], textposition="middle right", showlegend=False, hoverinfo="skip",
                       textfont=dict(size=20, color=COLORS["wave"])),
        ]

    base_trace = curve(x, base.y(x), f"y = {func} x", COLORS["base"], dash="dash", width=2,
                       opacity=1.0 if anim_base else 0.0, showlegend=anim_base)
    fig4 = go.Figure(
        data=[base_trace] + wave_traces(waves[init]),
        frames=[go.Frame(name=str(i), data=wave_traces(wv), traces=[1, 2, 3]) for i, wv in enumerate(waves)],
    )
    anim_opts = dict(frame=dict(duration=duration, redraw=False), transition=dict(duration=0), mode="immediate")
    fig4.update_layout(
        updatemenus=[dict(
            type="buttons", direction="left", showactive=False,
            x=0, xanchor="left", y=-0.12, yanchor="top", pad=dict(t=10, r=10),
            buttons=[
                dict(label="▶ 再生", method="animate",
                     args=[None, dict(anim_opts, fromcurrent=True)]),
                dict(label="⏸ 停止", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate",
                                        transition=dict(duration=0))]),
            ],
        )],
        sliders=[dict(
            active=init, x=0.18, len=0.82, y=-0.12, yanchor="top", pad=dict(t=10),
            currentvalue=dict(prefix=f"{'β' if param == 'beta' else param} = ",
                              font=dict(size=16, color=COLORS["wave"])),
            font=dict(color="rgba(0,0,0,0)"),  # 目盛りラベルは重なるので非表示
            ticklen=3,
            steps=[dict(method="animate", label=fmt(v),
                        args=[[str(i)], dict(frame=dict(duration=0, redraw=False),
                                             transition=dict(duration=0), mode="immediate")])
                   for i, v in enumerate(values)],
        )],
    )
    style_axes(fig4, lo, hi, ylim, unit, height=540)
    fig4.update_layout(margin=dict(l=10, r=10, t=40, b=110))
    st.plotly_chart(fig4, key=f"anim_chart_{param}")
    st.caption("▶ 再生 でパラメータが自動で変化します。下のスライダーをドラッグしてコマ送りもできます。")
