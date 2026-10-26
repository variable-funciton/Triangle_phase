"""加法定理の公式とその証明（後期課題7 対応）

単位円上の 2 点の距離を 2 通りに表して cos(α − β) を導き、そこから残りの公式を導く。
"""

import math

import plotly.graph_objects as go
import streamlit as st


st.title("加法定理とその証明")
st.markdown(
    r"2 つの角の和・差の三角関数を、それぞれの角の三角関数で表す公式が **加法定理** です。"
    r"$\sin 75^\circ = \sin(45^\circ + 30^\circ)$、$\sin\frac{5\pi}{12} = \sin\left(\frac{\pi}{4} + \frac{\pi}{6}\right)$ のように、有名角の組み合わせで表せる角の値を求められます。"
    "合成・積和・和積・2 倍角など、この単元の公式はすべて加法定理から導かれます。"
)

# ---------------- 公式 ----------------
with st.container(border=True):
    st.subheader("加法定理")
    c1, c2 = st.columns(2)
    with c1:
        st.latex(r"\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta")
        st.latex(r"\sin(\alpha - \beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta")
    with c2:
        st.latex(r"\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta")
        st.latex(r"\cos(\alpha - \beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta")
    st.latex(r"\tan(\alpha + \beta) = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta},\qquad"
             r"\tan(\alpha - \beta) = \frac{\tan\alpha - \tan\beta}{1 + \tan\alpha\tan\beta}")
    st.caption("覚え方の例：sin は「サイン・コサイン、コサイン・サイン」で符号はそのまま、"
               "cos は「コサイン・コサイン、サイン・サイン」で符号が反対になる。")
    st.warning(r"$\sin(\alpha + \beta) \neq \sin\alpha + \sin\beta$ に注意。たとえば $\sin(30^\circ + 60^\circ) = \sin 90^\circ = 1$ だが、"
               r"$\sin 30^\circ + \sin 60^\circ = \frac{1 + \sqrt{3}}{2} \approx 1.37$。")

# ---------------- 証明（図つき） ----------------
st.subheader("証明：単位円上の 2 点の距離を 2 通りに表す")
s1, s2 = st.columns(2)
a_deg = s1.slider("α [°]", 0, 360, 110, 5, key="at_a")
b_deg = s2.slider("β [°]", 0, 360, 30, 5, key="at_b")
a, b = math.radians(a_deg), math.radians(b_deg)
d_deg = a_deg - b_deg

P = (math.cos(a), math.sin(a))
Q = (math.cos(b), math.sin(b))
P2 = (math.cos(a - b), math.sin(a - b))
A = (1.0, 0.0)
t = [i * 2 * math.pi / 200 for i in range(201)]


def circle_fig(points, chord, title, arcs):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[math.cos(x) for x in t], y=[math.sin(x) for x in t], mode="lines",
                             line=dict(color="#9aa0a6", width=1.5), hoverinfo="skip"))
    for (r, th0, th1, color, label) in arcs:
        n = 40
        ths = [th0 + (th1 - th0) * i / n for i in range(n + 1)]
        fig.add_trace(go.Scatter(x=[r * math.cos(x) for x in ths], y=[r * math.sin(x) for x in ths], mode="lines",
                                 line=dict(color=color, width=2), hoverinfo="skip"))
        mid = (th0 + th1) / 2
        fig.add_annotation(x=(r + 0.12) * math.cos(mid), y=(r + 0.12) * math.sin(mid), text=label, showarrow=False,
                           font=dict(color=color, size=14))
    for name, (x, y), color in points:
        fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode="lines", line=dict(color=color, width=1.5, dash="dot"), hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[name], textposition="top right",
                                 marker=dict(color=color, size=10), textfont=dict(size=14, color=color), hoverinfo="skip"))
    (x0, y0), (x1, y1) = chord
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color="#d62728", width=3), hoverinfo="skip"))
    fig.update_layout(title=dict(text=title, x=0.5, xanchor="center"), height=380, showlegend=False, template="plotly_white",
                      margin=dict(l=10, r=10, t=40, b=10))
    fig.update_xaxes(range=[-1.35, 1.35], zeroline=True, zerolinecolor="black", fixedrange=True)
    fig.update_yaxes(range=[-1.35, 1.35], zeroline=True, zerolinecolor="black", scaleanchor="x", fixedrange=True)
    return fig


g1, g2 = st.columns(2)
g1.plotly_chart(circle_fig([("P(α)", P, "#1f77b4"), ("Q(β)", Q, "#ff7f0e")], (P, Q), "① P と Q",
                           [(0.25, 0, a, "#1f77b4", "α"), (0.4, 0, b, "#ff7f0e", "β")]), key="at_fig1")
g2.plotly_chart(circle_fig([("P'(α−β)", P2, "#1f77b4"), ("A", A, "#ff7f0e")], (P2, A), "② 全体を −β 回転すると",
                           [(0.3, 0, a - b, "#1f77b4", "α−β")]), key="at_fig2")

pq2 = (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
pa2 = (P2[0] - 1) ** 2 + P2[1] ** 2
st.markdown(
    rf"""
**考え方**　単位円上に $\mathrm{{P}}(\cos\alpha,\ \sin\alpha)$、$\mathrm{{Q}}(\cos\beta,\ \sin\beta)$ をとる（図①）。
全体を原点のまわりに $-\beta$ だけ回転すると、Q は $\mathrm{{A}}(1,\ 0)$ に、P は $\mathrm{{P'}}(\cos(\alpha-\beta),\ \sin(\alpha-\beta))$ に移る（図②）。
回転しても 2 点の距離は変わらないので **$\mathrm{{PQ}} = \mathrm{{P'A}}$**（赤い線分）。

**① PQ² を計算する**（2 点間の距離の公式）

$$\mathrm{{PQ}}^2 = (\cos\alpha - \cos\beta)^2 + (\sin\alpha - \sin\beta)^2$$
$$= (\cos^2\alpha + \sin^2\alpha) + (\cos^2\beta + \sin^2\beta) - 2(\cos\alpha\cos\beta + \sin\alpha\sin\beta)$$
$$= 2 - 2(\cos\alpha\cos\beta + \sin\alpha\sin\beta)$$

**② P'A² を計算する**

$$\mathrm{{P'A}}^2 = (\cos(\alpha-\beta) - 1)^2 + \sin^2(\alpha-\beta) = 2 - 2\cos(\alpha-\beta)$$

**③ PQ² = P'A² より**

$$\cos(\alpha - \beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta$$

いまの角では：$\mathrm{{PQ}}^2 \approx {pq2:.4f}$、$\mathrm{{P'A}}^2 \approx {pa2:.4f}$（等しい）、
$\cos(\alpha-\beta) = \cos {d_deg}^\circ \approx {math.cos(a - b):.4f}$、
$\cos\alpha\cos\beta + \sin\alpha\sin\beta \approx {math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b):.4f}$
"""
)
with st.expander("別の証明：余弦定理を使う（0° < α − β < 180° のとき）"):
    st.markdown(
        r"""
三角形 OPQ で、OP = OQ = 1、$\angle\mathrm{POQ} = \alpha - \beta$ なので、余弦定理より

$$\mathrm{PQ}^2 = 1^2 + 1^2 - 2\cdot1\cdot1\cdot\cos(\alpha - \beta) = 2 - 2\cos(\alpha - \beta)$$

これを ① と比べても同じ式が得られる。ただし三角形ができる角に限られるので、どんな角でも成り立つことを示すには、上の回転の方法がよい。
"""
    )

st.subheader("残りの公式を導く")
st.markdown(
    r"""
**cos(α + β)**　$\cos(\alpha - \beta)$ の式で $\beta$ を $-\beta$ にする。$\cos(-\beta) = \cos\beta$、$\sin(-\beta) = -\sin\beta$ より

$$\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta$$

**sin(α + β)**　$\sin\theta = \cos\left(\dfrac{\pi}{2} - \theta\right)$ を使う。

$$\sin(\alpha + \beta) = \cos\left(\left(\frac{\pi}{2} - \alpha\right) - \beta\right) = \cos\left(\frac{\pi}{2} - \alpha\right)\cos\beta + \sin\left(\frac{\pi}{2} - \alpha\right)\sin\beta = \sin\alpha\cos\beta + \cos\alpha\sin\beta$$

**sin(α − β)**　上の式で $\beta$ を $-\beta$ にする：$\sin(\alpha - \beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta$

**tan(α + β)**　$\tan = \dfrac{\sin}{\cos}$ に代入し、分母・分子を $\cos\alpha\cos\beta$ で割る。

$$\tan(\alpha + \beta) = \frac{\sin\alpha\cos\beta + \cos\alpha\sin\beta}{\cos\alpha\cos\beta - \sin\alpha\sin\beta} = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta}$$
"""
)

st.info("sin 75° = sin(45° + 30°) のように値を求める問題は、「演習（加法定理の応用）」の「加法定理で値を求める」「加法定理の公式」などで練習できます（度数法・弧度法の両方）。"
        "合成・積和・和積の公式のページでは、加法定理から導かれる公式を扱います。")
st.page_link("views/ex_addition.py", label="演習（加法定理の応用）へ", icon="✏️")
