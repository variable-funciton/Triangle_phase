"""テントマップの変換と合成（後期課題5 対応）— Expand_transform/tent_map_transform.py を移植して拡張"""

from fractions import Fraction as F

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.tent import (compose, dense_grid, iterate_fn, iterate_vertices, orbit, tent, transformed,
                        transformed_vertices, trapezoid)

C_BASE, C_MAIN, C_IN, C_OUT = "gray", "#d62728", "#1f77b4", "#2ca02c"


def num(v: float) -> str:
    """0.5 → 1/2 のように、きりのよい値は分数で表示"""
    fr = F(v).limit_denominator(24)
    if abs(float(fr) - v) > 1e-9:
        return f"{v:.3g}"
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{'−' if fr < 0 else ''}{abs(fr.numerator)}/{fr.denominator}"


def square_axes(fig, xr, yr, height=560, dtick=None):
    span = max(xr[1] - xr[0], yr[1] - yr[0])
    d = dtick or (0.25 if span <= 2.5 else 0.5 if span <= 5 else 1)
    fig.update_layout(height=height, template="plotly_white", margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=1.08),
                      font=dict(family="Noto Sans CJK JP, IPAexGothic, Meiryo, 'Yu Gothic', sans-serif"))
    fig.update_xaxes(range=xr, dtick=d, zeroline=True, zerolinecolor="black", zerolinewidth=1.5,
                     gridcolor="rgba(0,0,0,0.1)")
    fig.update_yaxes(range=yr, dtick=d, zeroline=True, zerolinecolor="black", zerolinewidth=1.5,
                     gridcolor="rgba(0,0,0,0.1)", scaleanchor="x", scaleratio=1)
    return fig


def download_buttons(fig, name):
    c1, c2 = st.columns(2)
    c1.download_button("🌐 グラフを HTML で保存", fig.to_html(include_plotlyjs="cdn"),
                       file_name=f"{name}.html", mime="text/html", key=f"dl_html_{name}")
    try:
        pdf = fig.to_image(format="pdf")
        c2.download_button("📄 グラフを PDF で保存", pdf, file_name=f"{name}.pdf",
                           mime="application/pdf", key=f"dl_pdf_{name}")
    except Exception:
        c2.caption("PDF 保存は、サーバーに kaleido と Chromium が入っているときだけ使えます（HTML 保存はいつでも使えます）。")


st.title("テントマップの変換と合成")
st.markdown(r"""
基本となるテントマップ $f(x)$ は区間 $0 \le x \le 1$ で定義された「山形」の関数です。
$$ f(x) = \begin{cases} 2x & (0\leq x\leq \frac{1}{2}) \\ 2-2x & (\frac{1}{2} < x\leq 1)\\ 0 & (\text{それ以外}) \end{cases} $$
""")

# ---------------- サイドバー（① の変換パラメータ。② でも使う） ----------------
st.sidebar.header("変換 y = a·f(b(x − p)) + q")
a = st.sidebar.slider("縦の倍率 a（マイナスで上下反転）", -3.0, 3.0, 1.0, 0.1, key="tm_a")
b = st.sidebar.slider("横の倍率 b（マイナスで左右反転）", -3.0, 3.0, 1.0, 0.1, key="tm_b")
p = st.sidebar.slider("横の移動 p（x 方向）", -2.0, 2.0, 0.0, 0.1, key="tm_p")
q = st.sidebar.slider("縦の移動 q（y 方向）", -2.0, 2.0, 0.0, 0.1, key="tm_q")
if b == 0:
    st.sidebar.warning("b = 0 だと関数が定義できないため、b = 0.1 に補正します。")
    b = 0.1

tab1, tab2, tab3 = st.tabs(["① 拡大・縮小・平行移動・反転", "② 合成関数 f(g(x)) と g(f(x))", "③ f を何回も合成する"])

# =====================================================================
# ① 変換
# =====================================================================
with tab1:
    st.latex(rf"y = a\,f(b(x-p)) + q = {num(a)}\,f\left({num(b)}\left(x {'-' if p >= 0 else '+'} {num(abs(p))}\right)\right)"
             rf" {'+' if q >= 0 else '-'} {num(abs(q))}")
    verts = transformed_vertices(a, b, p, q)
    xs_v = [v[0] for v in verts] + [0, 1]
    ys_v = [v[1] for v in verts] + [0, 1]
    xr = [min(xs_v) - 0.7, max(xs_v) + 0.7]
    yr = [min(ys_v) - 0.7, max(ys_v) + 0.7]
    span = max(xr[1] - xr[0], yr[1] - yr[0])   # 1:1 の比率で両方が収まるよう、短い方を広げる
    cx, cy = sum(xr) / 2, sum(yr) / 2
    xr, yr = [cx - span / 2, cx + span / 2], [cy - span / 2, cy + span / 2]
    x = dense_grid(xr[0], xr[1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=tent(x, outside=np.nan), mode="lines", name="元のテントマップ: y = f(x)",
                             line=dict(color=C_BASE, width=2, dash="dash"), opacity=0.7))
    fig.add_trace(go.Scatter(x=x, y=transformed(x, a, b, p, q, outside=np.nan), mode="lines",
                             name="変換後: y = a f(b(x − p)) + q", line=dict(color=C_MAIN, width=3)))
    fig.add_trace(go.Scatter(x=[0, 0.5, 1], y=[0, 1, 0], mode="markers", marker=dict(color=C_BASE, size=7),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[v[0] for v in verts], y=[v[1] for v in verts], mode="markers+text",
                             marker=dict(color=C_MAIN, size=11), showlegend=False,
                             text=[f"({num(v[0])}, {num(v[1])})" for v in verts], textposition="top center",
                             hoverinfo="skip"))
    for (x0, y0), (x1, y1) in zip([(0, 0), (0.5, 1), (1, 0)], verts):
        if abs(x0 - x1) + abs(y0 - y1) > 1e-9:
            fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", text="",
                               showarrow=True, arrowhead=2, arrowwidth=1.3, arrowcolor=C_MAIN, opacity=0.6)
    square_axes(fig, xr, yr)
    st.plotly_chart(fig, key="tm_transform")

    st.markdown("**両端と頂点の移り先**")
    st.markdown(
        "| 元の点 | (0, 0) | (1/2, 1) | (1, 0) |\n|:--|:--:|:--:|:--:|\n"
        "| 変換後 (p + x₀/b, a·y₀ + q) | " + " | ".join(f"({num(v[0])}, {num(v[1])})" for v in verts) + " |"
    )
    st.markdown("### 💾 グラフのダウンロード")
    download_buttons(fig, "tent_map_graph")
    with st.expander("📝 パラメータによる変化の仕組み"):
        c1, c2 = st.columns(2)
        c1.markdown(r"""
**拡大・縮小・反転（$a, b$）**
* **$a$**：縦方向の倍率。$a=-1$ にすると**上下反転**し、山が谷になる。
* **$b$**：横方向の倍率。$b=2$ にすると横幅は**半分**（$\frac{1}{2}$ 倍）になる。$b$ をマイナスにすると**左右反転**する。
""")
        c2.markdown(r"""
**平行移動（$p, q$）**
* **$p$**：$x$ 軸方向の平行移動。
* **$q$**：$y$ 軸方向の平行移動。
* 頂点 $(\frac{1}{2}, 1)$ は $(p + \frac{1}{2b},\ a + q)$ に移る。
""")

# =====================================================================
# ② 合成関数
# =====================================================================
with tab2:
    FUNCS = {
        "f（テントマップ）": (tent, r"f(x)"),
        "g（台形・課題5）": (trapezoid, r"g(x)"),
        "h（① で変換したテント）": (lambda x: transformed(x, a, b, p, q), r"h(x)"),
    }
    st.markdown(r"""
台形の関数 $g(x)$（課題5 と同じ）と、① のパラメータで変換したテント $h(x) = a f(b(x-p)) + q$ も使えます。
$$ g(x) = \begin{cases} 3x & (0 \le x < \frac{1}{3}) \\ 1 & (\frac{1}{3} \le x < \frac{2}{3}) \\ 3 - 3x & (\frac{2}{3} \le x < 1) \\ 0 & (\text{それ以外}) \end{cases} $$
""")
    st.caption("※ 課題5 と同じく、定義した区間の外では値を 0 とします（内側の関数の値が区間の外に出ても合成できるようにするため）。")
    c1, c2 = st.columns(2)
    outer_k = c1.selectbox("外側の関数", list(FUNCS), index=0, key="tm_outer")
    inner_k = c2.selectbox("内側の関数", list(FUNCS), index=1, key="tm_inner")
    fo, lo_ = FUNCS[outer_k]
    fi, li_ = FUNCS[inner_k]
    o_name, i_name = lo_[0], li_[0]
    xr2 = [-0.25, 1.25]
    x = dense_grid(xr2[0], xr2[1])
    y_in, y_comp, y_rev = fi(x), compose(fo, fi)(x), compose(fi, fo)(x)

    x0 = st.slider("x の値で追いかける", 0.0, 1.0, 0.25, 0.01, key="tm_x0")
    u0 = float(fi(np.array([x0]))[0])
    w0 = float(fo(np.array([u0]))[0])
    st.latex(rf"x = {x0:.2f} \;\xrightarrow{{\ {i_name}\ }}\; {i_name}(x) = {u0:.3f} \;\xrightarrow{{\ {o_name}\ }}\;"
             rf" {o_name}({i_name}(x)) = {w0:.3f}")

    g1, g2 = st.columns(2)
    with g1:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=x, y=y_in, mode="lines", name=f"内側 {i_name}(x)",
                                  line=dict(color=C_IN, width=2, dash="dash")))
        fig2.add_trace(go.Scatter(x=x, y=y_comp, mode="lines", name=f"{o_name}({i_name}(x))",
                                  line=dict(color=C_MAIN, width=3.5)))
        fig2.add_trace(go.Scatter(x=[x0, x0, x0], y=[0, u0, w0], mode="markers+lines", showlegend=False,
                                  line=dict(color="black", width=1, dash="dot"),
                                  marker=dict(color=["black", C_IN, C_MAIN], size=[6, 10, 12]), hoverinfo="skip"))
        square_axes(fig2, xr2, [-0.25, 1.25] if max(y_comp.max(), y_in.max()) <= 1.2 else
                    [min(y_comp.min(), y_in.min(), 0) - 0.25, max(y_comp.max(), y_in.max()) + 0.25], height=430)
        fig2.update_layout(title=dict(text=f"y = {o_name}({i_name}(x))", x=0.5))
        st.plotly_chart(fig2, key="tm_comp")
    with g2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=x, y=fo(x), mode="lines", name=f"{o_name}(x)",
                                  line=dict(color=C_OUT, width=2, dash="dash")))
        fig3.add_trace(go.Scatter(x=x, y=y_rev, mode="lines", name=f"{i_name}({o_name}(x))",
                                  line=dict(color="#9467bd", width=3.5)))
        square_axes(fig3, xr2, [-0.25, 1.25] if max(y_rev.max(), 1) <= 1.2 else
                    [min(y_rev.min(), 0) - 0.25, y_rev.max() + 0.25], height=430)
        fig3.update_layout(title=dict(text=f"順番を入れかえると y = {i_name}({o_name}(x))", x=0.5))
        st.plotly_chart(fig3, key="tm_comp_rev")
    if outer_k != inner_k:
        same = np.allclose(y_comp, y_rev)
        st.info("2 つのグラフは同じになりました。" if same else
                f"**{o_name}({i_name}(x)) と {i_name}({o_name}(x)) は違うグラフ** です。合成は順番を入れかえると結果が変わります。")
    with st.expander("合成関数のグラフの考え方"):
        st.markdown(
            f"1. まず **内側** の {i_name}(x) を計算する（青い破線）。\n"
            f"2. その値を **外側** の関数 {o_name} に入れる。\n"
            f"3. 内側の値が 0 → 1 → 0 と動くと、外側のテント f は 0 → 1 → 0 をそのたびにたどるので、山の数が増える。\n"
            "4. 内側の値が一定（台形 g の平らな部分 = 1）なら、合成も一定（f(1) = 0）になる。"
        )

# =====================================================================
# ③ f を何回も合成する
# =====================================================================
with tab3:
    n = st.slider("合成する回数 n（f∘f∘…∘f）", 1, 7, 2, key="tm_n")
    x = dense_grid(0, 1, depth=n + 2)
    fn = iterate_fn(n)
    fig4 = go.Figure()
    if n > 1:
        fig4.add_trace(go.Scatter(x=x, y=iterate_fn(n - 1)(x), mode="lines", name=f"f を {n - 1} 回",
                                  line=dict(color=C_BASE, width=1.5, dash="dash"), opacity=0.7))
    fig4.add_trace(go.Scatter(x=x, y=fn(x), mode="lines", name=f"f を {n} 回",
                              line=dict(color=C_MAIN, width=2.5)))
    vs = iterate_vertices(n)
    fig4.add_trace(go.Scatter(x=[float(v[0]) for v in vs if v[1] == 1], y=[1] * (2 ** (n - 1)), mode="markers",
                              name="山の頂上", marker=dict(color=C_MAIN, size=8 if n <= 5 else 5)))
    square_axes(fig4, [-0.05, 1.05], [-0.05, 1.15], height=470, dtick=0.25 if n <= 2 else 0.125)
    st.plotly_chart(fig4, key="tm_iter")
    st.markdown(
        f"- **山の数は {2 ** (n - 1)} 個**（1 回合成するごとに 2 倍）、**傾きは ±{2 ** n}**。\n"
        f"- 折れ目は x = k / {2 ** n}（k = 0, 1, …, {2 ** n}）で、そこでの値は 0 と 1 が交互に並ぶ。\n"
        "- 理由：f の値が 0 → 1 → 0 と一往復するたびに、外側の f も 0 → 1 → 0 を一往復するから。"
    )
    st.latex(r"\underbrace{f(f(\cdots f}_{n\text{ 回}}(x)\cdots)) \text{ の山の数} = 2^{\,n-1},\qquad \text{傾き} = \pm 2^{\,n}")

    st.markdown("#### 漸化式として見る：$x_{k+1} = f(x_k)$")
    st.markdown("f を何回も合成することは、数列の漸化式 $x_{k+1} = f(x_k)$ で次々に値を求めることと同じです。"
                "直線 $y = x$ を使って、点の動きを **蜘蛛の巣図** でたどってみよう。")
    PRESET = {"1/5（周期 2）": F(1, 5), "1/3（2/3 で止まる）": F(1, 3), "1/7（周期 3）": F(1, 7),
              "3/8（0 に落ちる）": F(3, 8), "0.23": F(23, 100), "0.231（0.23 と少しだけ違う）": F(231, 1000)}
    c1, c2 = st.columns(2)
    start = c1.selectbox("初めの値 x₀", list(PRESET), index=0, key="tm_x0_orbit")
    steps = c2.slider("くり返す回数", 1, 30, 10, key="tm_steps")
    orb = orbit(PRESET[start], steps)
    xs_c, ys_c = [float(orb[0])], [0.0]
    for k in range(steps):
        xk, xk1 = float(orb[k]), float(orb[k + 1])
        xs_c += [xk, xk1]
        ys_c += [xk1, xk1]
    xx = np.linspace(0, 1, 401)
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=xx, y=tent(xx), mode="lines", name="y = f(x)", line=dict(color=C_MAIN, width=2.5)))
    fig5.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="y = x", line=dict(color=C_BASE, dash="dash")))
    fig5.add_trace(go.Scatter(x=xs_c, y=ys_c, mode="lines+markers", name="x₀ → x₁ → x₂ → …",
                              line=dict(color=C_IN, width=1.5), marker=dict(size=4)))
    square_axes(fig5, [-0.03, 1.03], [-0.03, 1.08], height=470)
    st.plotly_chart(fig5, key="tm_cobweb")

    def fr(v):
        return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"
    st.markdown("**数列の値**（分数で正確に計算）")
    st.markdown(" → ".join(f"x{k}={fr(v)}" for k, v in enumerate(orb[:16])) + (" → …" if len(orb) > 16 else ""))
    st.caption(
        "x₀ を分数にすると、値はいつか 0 になるか、同じ値をくり返す（周期的になる）。"
        "0.23 と 0.231 のように少しだけ違う値から始めると、差が 1 回ごとに 2 倍に広がり、10 回ほどで全く違う値になる（カオス：初めの値のわずかな違いが大きく広がる）。"
        "（差 0.001 も、10 回で約 1000 倍 ≒ 1 になる。）"
    )
