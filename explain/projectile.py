"""斜方投射の詳しい解説（微分積分を使わず、等加速度運動の式・三角比・2次関数・2倍角の公式で説明する）"""

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.exact import cos_deg, sin_deg

G = 9.8


def num(v: float) -> str:
    """整数になる値は整数で、そうでない値は小数第 3 位まで"""
    return str(round(v)) if abs(v - round(v)) < 1e-9 else f"{v:.3f}"


def component_tex(v0: float, theta: float, func: str) -> str:
    """v0 sinθ / v0 cosθ の値。15° の倍数なら厳密値を「=」で、割り切れない値だけ「≈」をつける"""
    if float(theta).is_integer() and int(theta) % 15 == 0 and float(v0).is_integer():
        q = (sin_deg(int(theta)) if func == "sin" else cos_deg(int(theta))) * int(v0)
        if q.is_rational():
            return f"= {q.latex()}"
        return rf"= {q.latex()} \approx {float(q):.3f}"
    val = v0 * (math.sin(math.radians(theta)) if func == "sin" else math.cos(math.radians(theta)))
    return rf"\approx {val:.3f}"


def _vector_figure(v0: float, theta: float):
    th = math.radians(theta)
    vx, vy = v0 * math.cos(th), v0 * math.sin(th)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, vx], y=[0, 0], mode="lines", line=dict(color="#2ca02c", width=5),
                             name=f"水平成分 v₀cosθ ≈ {vx:.2f}"))
    fig.add_trace(go.Scatter(x=[vx, vx], y=[0, vy], mode="lines", line=dict(color="#ff7f0e", width=5),
                             name=f"鉛直成分 v₀sinθ ≈ {vy:.2f}"))
    fig.add_trace(go.Scatter(x=[0, vx], y=[0, vy], mode="lines+markers", line=dict(color="#1f77b4", width=4),
                             marker=dict(size=[0, 10]), name=f"初速度 v₀ = {v0}"))
    arc = np.linspace(0, th, 40)
    r = 0.25 * v0
    fig.add_trace(go.Scatter(x=r * np.cos(arc), y=r * np.sin(arc), mode="lines", line=dict(color="black"),
                             showlegend=False, hoverinfo="skip"))
    fig.add_annotation(x=r * 1.25 * math.cos(th / 2), y=r * 1.25 * math.sin(th / 2), text=f"θ = {theta}°",
                       showarrow=False)
    fig.update_layout(height=320, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                      legend=dict(orientation="h", y=1.15))
    fig.update_xaxes(range=[-0.05 * v0, 1.1 * v0], title_text="[m/s]")
    fig.update_yaxes(range=[-0.05 * v0, 1.05 * v0], scaleanchor="x", scaleratio=1)
    return fig


def render(v0: float, theta: float):
    th = math.radians(theta)
    c, s = math.cos(th), math.sin(th)
    vx, vy = v0 * c, v0 * s
    T = 2 * vy / G
    H = vy ** 2 / (2 * G)
    L = vx * T

    st.markdown("### 0. この運動の考え方")
    st.markdown(
        "斜めに投げた物体の運動は、そのままだと複雑に見えます。そこで **水平方向** と **鉛直方向** に分けて考えます。\n\n"
        "- **水平方向**：力がはたらかない（空気抵抗を無視）→ 速さが変わらない **等速直線運動**\n"
        "- **鉛直方向**：重力だけがはたらく → 下向きに一定の加速度 $g = 9.8\\ \\text{m/s}^2$ の **等加速度直線運動**\n\n"
        "2 つの方向の運動は、おたがいに影響しない（**運動の独立性**）ので、別々に計算してから組み合わせればよい。"
    )

    st.markdown("### 1. 準備：使う物理の式")
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**等速直線運動**（速さ $v$ が一定）")
        st.latex(r"x = vt")
        st.caption("時間 t に比例 → 1 次関数")
    with c2, st.container(border=True):
        st.markdown("**等加速度直線運動**（上向きを正、加速度 −g）")
        st.latex(r"v = v_0 - gt,\qquad y = v_0 t - \frac{1}{2}gt^2")
        st.caption("速度は t の 1 次関数、位置は t の 2 次関数（これは y と t の関係。"
                   "実際の軌跡が放物線になることは、4. で y を x の式で表して初めて示される）")
    st.markdown("これらは物理の授業で学ぶ式です。ここではこの 2 つの式と三角関数だけを使います。")

    st.markdown("### 2. 初速度を分ける（ここで三角比を使う）")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(_vector_figure(v0, theta), key="ex_pj_vec")
    with c2:
        st.markdown(r"初速度の矢印を斜辺とする直角三角形を考えると、三角比の定義から")
        st.latex(r"\cos\theta = \frac{\text{水平成分}}{v_0},\qquad \sin\theta = \frac{\text{鉛直成分}}{v_0}")
        st.latex(r"\text{水平成分} = v_0\cos\theta,\qquad \text{鉛直成分} = v_0\sin\theta")
        st.latex(rf"{v0}\cos {theta}^\circ {component_tex(v0, theta, 'cos')},\qquad "
                 rf"{v0}\sin {theta}^\circ {component_tex(v0, theta, 'sin')}\ [\text{{m/s}}]")

    st.markdown("### 3. 時刻 t での位置と速度")
    st.latex(r"\text{水平：}\ x = v_0\cos\theta\cdot t,\qquad v_x = v_0\cos\theta\ (\text{一定})")
    st.latex(r"\text{鉛直：}\ y = v_0\sin\theta\cdot t - \frac{1}{2}gt^2,\qquad v_y = v_0\sin\theta - gt")
    st.markdown("水平方向の速さはずっと同じで、鉛直方向の速さだけが 1 秒ごとに 9.8 m/s ずつ減っていきます"
                "（最高点を過ぎると下向きになって増えていく）。")

    st.markdown("### 4. 軌跡の式：放物線になる")
    st.markdown(r"水平の式から $t = \dfrac{x}{v_0\cos\theta}$。これを鉛直の式に代入して $t$ を消すと")
    st.latex(r"y = x\tan\theta - \frac{g}{2v_0^2\cos^2\theta}\,x^2")
    st.markdown(r"$x$ の **2 次関数**（上に凸の放物線）です。さらに相互関係 $\dfrac{1}{\cos^2\theta} = 1 + \tan^2\theta$ を使うと、"
                r"$\tan\theta$ だけで書けます。")
    st.latex(r"y = x\tan\theta - \frac{g(1 + \tan^2\theta)}{2v_0^2}\,x^2")

    st.markdown("### 5. 最高点")
    st.markdown(r"最高点では、上に向かう速さがちょうど 0 になります（$v_y = 0$）。")
    st.latex(r"v_0\sin\theta - gt = 0 \;\Longrightarrow\; t_{\text{最高点}} = \frac{v_0\sin\theta}{g}")
    st.latex(r"H = v_0\sin\theta\cdot\frac{v_0\sin\theta}{g} - \frac{1}{2}g\left(\frac{v_0\sin\theta}{g}\right)^2 = \frac{v_0^2\sin^2\theta}{2g}")
    st.caption("2 次関数 y = v₀sinθ·t − ½gt² を平方完成して、頂点の座標を求めても同じ結果になる。")

    st.markdown("### 6. 滞空時間と飛距離（ここで 2倍角の公式を使う）")
    st.markdown(r"地面（$y = 0$）に戻る時刻は、最高点までの時間の 2 倍（放物線は左右対称）。")
    st.latex(r"T = \frac{2v_0\sin\theta}{g},\qquad L = v_0\cos\theta\cdot T = \frac{2v_0^2\sin\theta\cos\theta}{g} = \frac{v_0^2\sin 2\theta}{g}")
    st.markdown(
        r"- $\sin 2\theta$ が最大値 1 をとるのは $2\theta = 90^\circ$、つまり **$\theta = 45^\circ\ \left(\dfrac{\pi}{4}\right)$ のとき飛距離が最大**：$L_{\max} = \dfrac{v_0^2}{g}$。" "\n"
        r"- $\sin(180^\circ - 2\theta) = \sin 2\theta$ なので、**$\theta$ と $90^\circ - \theta$（余角）は同じ飛距離** になる。" "\n"
        r"- 角度を大きくすると高く・長く飛ぶが、横に進む速さ $v_0\cos\theta$ が小さくなる。"
        r"「高さ（滞空時間）」と「横の速さ」の **かけ算** が最大になるちょうどよいところが 45°。"
    )

    st.markdown(f"### 7. 例題（いまの設定：v₀ = {v0} m/s、θ = {theta}°）")
    st.latex(rf"v_0\cos\theta {component_tex(v0, theta, 'cos')},\qquad v_0\sin\theta {component_tex(v0, theta, 'sin')}")
    st.latex(rf"t_{{\text{{最高点}}}} = \frac{{{num(vy)}}}{{9.8}} \approx {vy / G:.3f}\ \text{{s}},\qquad "
             rf"H = \frac{{{num(vy)}^2}}{{2\times 9.8}} \approx {H:.3f}\ \text{{m}}")
    st.latex(rf"T = \frac{{2\times {num(vy)}}}{{9.8}} \approx {T:.3f}\ \text{{s}},\qquad L = v_0\cos\theta\times T \approx {num(vx)}\times {T:.3f} \approx {L:.3f}\ \text{{m}}")
    st.latex(rf"L = \frac{{{v0}^2\sin {2 * theta}^\circ}}{{9.8}} \approx {v0 ** 2 * math.sin(2 * th) / G:.3f}\ \text{{m}}"
             r"\quad(\text{2倍角の公式を使った式でも同じ})")
    st.markdown(f"最高点での速さは 0 ではなく、水平成分の **{vx:.2f} m/s** が残っています。")

    st.markdown("### 8. よくある間違い")
    st.markdown(
        "- **最高点で速さが 0 になる** → 0 になるのは鉛直成分だけ。水平成分 v₀cosθ は残る。\n"
        "- **sin と cos の取り違え** → θ は「水平方向とのなす角」。水平成分が cos、鉛直成分が sin。"
        "問題によっては「鉛直方向とのなす角」で与えられることもあるので、図をかいて確認する。\n"
        "- **電卓の角度モード** → 度数法（DEG）と弧度法（RAD）を確認する。sin 30 を RAD で計算すると −0.988 になってしまう。\n"
        "- **45° がいつも最も遠い** → 「空気抵抗なし」かつ「投げた高さと着地の高さが同じ」ときだけ。"
        "高い所から投げる（砲丸投げなど）・空気抵抗がある（ボール投げなど）ときは 45° より小さい角が最適になる。"
    )

    st.markdown("### 9. 練習問題")
    q1T, q1H, q1L = 2 * 20 * 0.5 / G, (20 * 0.5) ** 2 / (2 * G), 400 * math.sin(math.radians(60)) / G
    with st.expander(r"問1　初速度 20 m/s、角度 30° で投げた。滞空時間・最高点の高さ・飛距離を求めよ（g = 9.8 m/s²）。"):
        st.latex(rf"v_0\sin 30^\circ = 10,\quad v_0\cos 30^\circ = 10\sqrt{{3}} \approx 17.32")
        st.latex(rf"T = \frac{{2\times 10}}{{9.8}} \approx {q1T:.2f}\ \text{{s}},\quad H = \frac{{10^2}}{{2\times 9.8}} \approx {q1H:.2f}\ \text{{m}},"
                 rf"\quad L = \frac{{20^2\sin 60^\circ}}{{9.8}} \approx {q1L:.1f}\ \text{{m}}")
    with st.expander("問2　初速度を変えずに 20° で投げたときと同じ飛距離になる、もう 1 つの角度を答えよ。"):
        st.markdown(r"余角の $90^\circ - 20^\circ = \mathbf{70^\circ}$。$\sin 40^\circ = \sin 140^\circ$ だから。"
                    "70° のほうが高く上がり、滞空時間は長い。")
    vmin = math.sqrt(40 * G)
    with st.expander("問3　40 m 先まで届かせるには、初速度は少なくとも何 m/s 必要か。"):
        st.latex(rf"L_{{\max}} = \frac{{v_0^2}}{{g}} \ge 40 \;\Longrightarrow\; v_0 \ge \sqrt{{40\times 9.8}} \approx {vmin:.1f}\ \text{{m/s}}")
        st.markdown("このとき 45° で投げる。これより遅いと、どの角度で投げても届かない。")
    with st.expander("問4　軌跡の式 y = x tanθ − g x² / (2v₀²cos²θ) で、y = 0 とおいて飛距離を求めよ。"):
        st.latex(r"x\left(\tan\theta - \frac{g}{2v_0^2\cos^2\theta}x\right) = 0 \;\Longrightarrow\; x = \frac{2v_0^2\sin\theta\cos\theta}{g} = \frac{v_0^2\sin 2\theta}{g}")
        st.markdown(r"$\tan\theta\cdot 2v_0^2\cos^2\theta = 2v_0^2\sin\theta\cos\theta$（$\tan\theta = \sin\theta/\cos\theta$）を使った。6 の結果と一致する。")
