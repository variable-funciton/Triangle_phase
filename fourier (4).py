"""フーリエ級数 — sin, cos を足し合わせて周期関数を作る（微分積分なしで見る入門）"""

import math
from fractions import Fraction

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.fourier import WAVES, amplitudes, custom_sum, partial_sum, term_values, terms
from utils.plotting import style_axes, x_grid

C_TARGET, C_SUM, C_TERM = "#7f7f7f", "#d62728", "#1f77b4"
TERM_COLORS = ["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#e377c2"]
YR = {"square": (-1.6, 1.6), "saw": (-4.0, 4.0), "triangle": (-0.6, 3.8), "half": (-0.7, 1.4), "full": (-0.7, 1.4)}


def coef_tex(c: float) -> str:
    """係数を約分した分数（p/q または p/(qπ)）で表示。どちらでもなければ小数"""
    sign = "-" if c < 0 else ""
    m = abs(c)
    r = Fraction(m).limit_denominator(1000)
    if abs(float(r) - m) < 1e-12:
        if r.denominator == 1:
            return sign + str(r.numerator)
        return sign + rf"\frac{{{r.numerator}}}{{{r.denominator}}}"
    r = Fraction(m * math.pi).limit_denominator(1000)    # c = p / (q π)
    if abs(float(r) - m * math.pi) < 1e-9:
        den = r"\pi" if r.denominator == 1 else rf"{r.denominator}\pi"
        return sign + rf"\frac{{{r.numerator}}}{{{den}}}"
    return f"{c:.3f}"


def sum_tex(key: str, N: int, max_terms: int = 4) -> str:
    w = WAVES[key]
    parts = []
    if w["a0"]:
        a0 = {math.pi / 2: r"\frac{\pi}{2}", 1 / math.pi: r"\frac{1}{\pi}", 2 / math.pi: r"\frac{2}{\pi}"}.get(w["a0"], f"{w['a0']:.3f}")
        parts.append(a0)
    ts = terms(key, N)
    for i, (n, kind, c) in enumerate(ts[:max_terms]):
        body = rf"\{kind} {'' if n == 1 else n}x"
        ct = coef_tex(c)
        if ct.startswith("-"):
            parts.append(rf" - {ct[1:]}\,{body}" if ct[1:] != "1" else rf" - {body}")
        else:
            parts.append((" + " if parts else "") + (rf"{ct}\,{body}" if ct != "1" else body))
    if len(ts) > max_terms:
        parts.append(r" + \cdots" if len(ts) > max_terms + 1 else "")
        n, kind, c = ts[-1]
        ct = coef_tex(c)
        parts.append((" - " if ct.startswith("-") else " + ") + rf"{ct.lstrip('-')}\,\{kind} {n}x")
    return "".join(parts) if parts else "0"


# ---------------- サイドバー ----------------
st.sidebar.header("波の選択")
key = st.sidebar.radio("近づけたい波", list(WAVES), format_func=lambda k: WAVES[k]["name"], key="fo_wave")
N = st.sidebar.slider("何倍の波まで足すか（n の最大）", 1, 50, 5, key="fo_N")
w = WAVES[key]
ts = terms(key, N)

st.title("三角関数を足して、いろいろな周期関数を作る（フーリエ級数）")
st.markdown(
    r"$\sin x,\ \sin 2x,\ \sin 3x,\ \dots$ や $\cos x,\ \cos 2x,\ \dots$ を、それぞれ **ちょうどよい大きさ** にして足し合わせると、"
    "矩形波やのこぎり波のような **角ばった波** まで作ることができます。これを **フーリエ級数** といいます。"
)

tab1, tab2, tab3, tab4 = st.tabs(["① 項を足していく", "② 足していく様子（アニメーション）", "③ 自分で波を作る", "④ しくみと使いみち"])

# =====================================================================
# ① 項を足していく
# =====================================================================
with tab1:
    st.markdown(f"**{w['name']}** は、次のように表されます。{w['note']}")
    st.latex(r"y = " + w["tex"])
    st.markdown(f"いまは **{N} 倍の波まで**（0 でない項 {len(ts)} 個{' + 定数' if w['a0'] else ''}）を足しています。")
    st.latex(r"y \approx " + sum_tex(key, N))

    show_terms = st.checkbox("足している 1 つ 1 つの波も表示（最初の 6 個まで）", value=N <= 7, key="fo_terms")
    x = x_grid(-2, 2, n=2400)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=w["func"](x), mode="lines", name="目標の波", line=dict(color=C_TARGET, width=2, dash="dash")))
    if show_terms:
        for i, (n, kind, c) in enumerate(ts[:6]):
            fig.add_trace(go.Scatter(x=x, y=term_values(x, n, kind, c), mode="lines", opacity=0.6,
                                     name=f"{c:+.3f} {kind} {'' if n == 1 else n}x",
                                     line=dict(color=TERM_COLORS[i % 6], width=1.3)))
    fig.add_trace(go.Scatter(x=x, y=partial_sum(key, x, N), mode="lines", name=f"{N} 倍の波までの和",
                             line=dict(color=C_SUM, width=3)))
    style_axes(fig, -2, 2, max(abs(YR[key][0]), abs(YR[key][1])), "rad", height=470)
    fig.update_yaxes(range=list(YR[key]), dtick=0.5 if YR[key][1] < 2 else 1)
    st.plotly_chart(fig, key="fo_main")
    if w["discontinuous"]:
        st.caption("※ 波がとぎれる（とび上がる）所のすぐ近くでは、いくら項を増やしても和が約 9% 行き過ぎる「とんがり」が残ります"
                   "（ギブズ現象）。とんがりの幅はどんどん細くなります。")

    st.markdown("##### どの n 倍の波がどれだけ入っているか")
    amps = amplitudes(key, N)
    fig2 = go.Figure(go.Bar(x=list(range(1, N + 1)), y=amps, marker_color=C_TERM,
                            hovertemplate="%{x} 倍の波：大きさ %{y:.4f}<extra></extra>"))
    fig2.update_layout(height=230, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10))
    fig2.update_xaxes(title_text="n（何倍の波か）", dtick=1 if N <= 20 else 5)
    fig2.update_yaxes(title_text="大きさ")
    st.plotly_chart(fig2, key="fo_spec")
    st.caption("このような棒グラフを **スペクトル** という。音なら「どの高さの音がどれだけ混ざっているか」を表す。")

# =====================================================================
# ② アニメーション
# =====================================================================
with tab2:
    st.markdown(f"**{w['name']}** に向かって、1 倍、2 倍、3 倍 … の波を順に足していきます。")
    NMAX = 30
    x = x_grid(-2, 2, n=1200)
    target = go.Scatter(x=x, y=w["func"](x), mode="lines", name="目標の波", line=dict(color=C_TARGET, width=2, dash="dash"))

    def frame_traces(k):
        new = [t for t in terms(key, k) if t[0] == k]
        y_new = sum((term_values(x, n, kind, c) for n, kind, c in new), np.zeros_like(x))
        return [
            go.Scatter(x=x, y=y_new, mode="lines", line=dict(color=C_TERM, width=1.5), opacity=0.8),
            go.Scatter(x=x, y=partial_sum(key, x, k), mode="lines", line=dict(color=C_SUM, width=3)),
        ]

    first = frame_traces(1)
    first[0].name, first[1].name = "いま足した波", "ここまでの和"
    fig3 = go.Figure(data=[target] + first,
                     frames=[go.Frame(name=str(k), data=frame_traces(k), traces=[1, 2]) for k in range(1, NMAX + 1)])
    step = dict(frame=dict(duration=0, redraw=False), transition=dict(duration=0), mode="immediate")
    fig3.update_layout(
        updatemenus=[dict(type="buttons", direction="left", showactive=False, x=0, xanchor="left", y=-0.12,
                          yanchor="top", pad=dict(t=10, r=10), buttons=[
                              dict(label="▶ 足していく", method="animate",
                                   args=[None, dict(frame=dict(duration=450, redraw=False), transition=dict(duration=0),
                                                    mode="immediate", fromcurrent=True)]),
                              dict(label="⏸ 停止", method="animate", args=[[None], step]),
                          ])],
        sliders=[dict(active=0, x=0.22, len=0.78, y=-0.12, yanchor="top", pad=dict(t=10),
                      currentvalue=dict(prefix="", suffix=" 倍の波まで", font=dict(size=15, color=C_SUM)),
                      steps=[dict(method="animate", label=str(k), args=[[str(k)], step]) for k in range(1, NMAX + 1)])],
    )
    style_axes(fig3, -2, 2, max(abs(YR[key][0]), abs(YR[key][1])), "rad", height=520)
    fig3.update_layout(margin=dict(l=10, r=10, t=40, b=110))
    fig3.update_yaxes(range=list(YR[key]), dtick=0.5 if YR[key][1] < 2 else 1)
    st.plotly_chart(fig3, key=f"fo_anim_{key}")
    st.caption("青い線は、その回に新しく足した n 倍の波。0 の回（矩形波の偶数倍など）は何も足されない。")

# =====================================================================
# ③ 自分で波を作る
# =====================================================================
with tab3:
    st.markdown(r"$y = b_1\sin x + b_2\sin 2x + \cdots + b_6\sin 6x$ の係数を自分で決めて、どんな波ができるか試してみよう。")
    PRESETS = {
        "自由に設定": None,
        "sin x だけ": [1, 0, 0, 0, 0, 0],
        "矩形波に近づける": [4 / (math.pi * n) if n % 2 else 0 for n in range(1, 7)],
        "のこぎり波に近づける": [2 * (-1) ** (n + 1) / n for n in range(1, 7)],
        "2 倍・3 倍の波だけ": [0, 1, 0.6, 0, 0, 0],
        "すべて 0 に戻す": [0] * 6,
    }
    for i in range(6):
        st.session_state.setdefault(f"fo_b{i + 1}", 1.0 if i == 0 else 0.0)

    def apply_preset():
        p = PRESETS[st.session_state["fo_preset"]]
        if p:
            for i, v in enumerate(p):
                st.session_state[f"fo_b{i + 1}"] = round(float(v), 2)

    st.selectbox("例を読み込む", list(PRESETS), key="fo_preset", on_change=apply_preset)
    cols = st.columns(6)
    bs = [cols[i].slider(f"b{i + 1}（sin {'' if i == 0 else i + 1}x）", -1.5, 1.5, step=0.01, key=f"fo_b{i + 1}")
          for i in range(6)]
    x = x_grid(-2, 2, n=1600)
    fig4 = go.Figure()
    for i, c in enumerate(bs):
        if c:
            fig4.add_trace(go.Scatter(x=x, y=c * np.sin((i + 1) * x), mode="lines", opacity=0.55,
                                      name=f"{c:+.2f} sin {'' if i == 0 else i + 1}x",
                                      line=dict(color=TERM_COLORS[i], width=1.3)))
    ysum = custom_sum(x, bs)
    fig4.add_trace(go.Scatter(x=x, y=ysum, mode="lines", name="和", line=dict(color=C_SUM, width=3.5)))
    lim = max(1.2, float(np.abs(ysum).max()) + 0.3)
    style_axes(fig4, -2, 2, lim, "rad", height=460)
    st.plotly_chart(fig4, key="fo_custom")
    terms_txt = " + ".join(f"{c:.2f}\\sin {'' if i == 0 else i + 1}x" for i, c in enumerate(bs) if c).replace("+ -", "- ")
    st.latex(r"y = " + (terms_txt or "0"))
    st.caption("どんな係数にしても、和の波は 2π ごとに同じ形をくり返す（どの sin nx も 2π ごとにもとに戻るから）。")

# =====================================================================
# ④ しくみと使いみち
# =====================================================================
with tab4:
    st.markdown("#### なぜ足すと周期関数になるの？")
    st.markdown(
        r"$\sin nx$ の周期は $\dfrac{2\pi}{n}$（「一般形」のページの $B = n$ の場合）。"
        r"$n = 1, 2, 3, \dots$ のどれも、$2\pi$ 進めば **ちょうど整数回** くり返してもとに戻ります。"
        r"だから、それらを足した波も $2\pi$ ごとに同じ形をくり返す **周期 $2\pi$ の周期関数** になります。"
    )
    st.latex(r"\sin x\ (\text{周期 } 2\pi),\quad \sin 2x\ (\text{周期 } \pi),\quad \sin 3x\ \left(\text{周期 } \tfrac{2\pi}{3}\right),\ \dots"
             r"\;\Longrightarrow\; \text{和の周期は } 2\pi")
    st.markdown("#### 矩形波ができるまで（イメージ）")
    st.markdown(
        r"- まず $\sin x$ だけでは、山がまるい。\n"
        r"- $\frac{1}{3}\sin 3x$ を足すと、山の真ん中がへこみ、両側が持ち上がって **平らに近づく**。\n"
        r"- さらに $\frac{1}{5}\sin 5x,\ \frac{1}{7}\sin 7x,\ \dots$ と、細かい波を小さく足していくと、角がどんどん鋭くなる。"
    )
    st.markdown("#### 係数はどうやって決めるの？")
    st.markdown(
        "どの n 倍の波をどれだけ足せばよいか（係数）は、**積分** という計算で求めます。"
        "積分は今後の授業（微分積分）で学ぶ内容なので、このページでは結果の係数を使っています。"
        "「三角関数を足すと、どんな形の周期関数でも作れる」ことを、まずはグラフで実感しておこう。"
    )
    st.markdown("#### どこで使われている？")
    st.markdown(
        "- **音**：同じ「ド」でも、ピアノとバイオリンで音色が違うのは、混ざっている **倍音（2 倍・3 倍…の波）の大きさ** が違うから。\n"
        "- **電気**：交流をダイオードで整流した電圧（半波整流・全波整流）を、直流成分（定数）と交流成分に分けて考える。\n"
        "- **画像・音声の圧縮**：JPEG や MP3 は、波を周波数ごとに分け、目や耳で気づきにくい成分を省いてデータを小さくしている。\n"
        "- **通信・信号処理**：雑音を取り除く（フィルター）、電波に情報をのせる、などの基本になっている。"
    )
