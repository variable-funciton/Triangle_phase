"""球面三角形（球面三角法）（発展）

グラフと操作はブラウザ側で動かす（assets/spherical_triangle.html, assets/spherical_triangle_core.js）。
参考：河瀬和重「球面三角法の簡潔かつ体系的な理解への試み」国土地理院時報 132 (2019)
"""

import streamlit as st

from utils.widget import render

PAPER_PAGE = "https://www.gsi.go.jp/REPORT/JIHO/vol132-abst-18.html"
PAPER_PDF = "https://www.gsi.go.jp/common/000213916.pdf"

st.title("球面三角形（球面三角法）")
st.markdown(
    r"球面上の 3 点を **大円の弧**（球面上の最短の道）で結んだ図形が **球面三角形** です。"
    r"辺も角も「角度」で表され、角の和は 180° より大きくなります。"
    r"平面の三角比と同じように、辺と角の関係を表す公式（**球面三角法**）があり、"
    r"どれも **加法定理** と、それから導いた公式だけで証明できます。"
)

render("spherical_triangle", height=1300)

with st.expander("📖 球面の余弦法則を導く（加法定理の証明と同じ方法）", expanded=False):
    st.markdown(
        r"""
半径 1 の球（単位球）で考える。辺の長さ ＝ 中心角（ラジアン）。頂点 C を **北極** $(0,\ 0,\ 1)$ に置き、
$\mathrm{CB} = a$、$\mathrm{CA} = b$、C での角を $\gamma$、求めたい辺を $\mathrm{AB} = c$ とする。

A を $xz$ 平面にとると、前のページの球面座標（$\theta$ = 北極からの角）で

$$\mathrm{A}(\sin b,\ 0,\ \cos b),\qquad \mathrm{B}(\sin a\cos\gamma,\ \sin a\sin\gamma,\ \cos a)$$

**① A と B を結ぶ線分（弦）の長さの 2 乗を成分で計算する**

$$\mathrm{AB}^2 = (\sin a\cos\gamma - \sin b)^2 + (\sin a\sin\gamma)^2 + (\cos a - \cos b)^2$$
$$= (\sin^2 a + \cos^2 a) + (\sin^2 b + \cos^2 b) - 2(\cos a\cos b + \sin a\sin b\cos\gamma)$$
$$= 2 - 2(\cos a\cos b + \sin a\sin b\cos\gamma)$$

**② 同じ長さを中心角 $c$ で表す**　三角形 OAB は $\mathrm{OA} = \mathrm{OB} = 1$、$\angle\mathrm{AOB} = c$ なので
（「加法定理とその証明」の $\mathrm{P'A}^2$ と同じ計算）

$$\mathrm{AB}^2 = (\cos c - 1)^2 + \sin^2 c = 2 - 2\cos c$$

**③ ① = ② より　球面の余弦法則**

$$\cos c = \cos a\cos b + \sin a\sin b\cos\gamma$$

- $\gamma = 0$（A, B が同じ経線上）なら $\cos c = \cos a\cos b + \sin a\sin b = \cos(a - b)$。これは **加法定理そのもの**。
- 三角形が小さいとき、$\cos x \approx 1 - \dfrac{x^2}{2}$、$\sin x \approx x$（「テイラー展開」のページ）を代入して、
  小さい項 $\dfrac{a^2b^2}{4}$ を無視すると $c^2 \approx a^2 + b^2 - 2ab\cos\gamma$。**平面の余弦定理** にもどる。
- 前のページの 2 都市の距離の式は、C を北極、$a = 90^\circ - \varphi_2$、$b = 90^\circ - \varphi_1$、$\gamma = \lambda_2 - \lambda_1$ としたもの。
"""
    )

with st.expander("📖 角の和と面積：ジラールの定理"):
    st.markdown(
        r"""
2 つの大円で球面を切ると、みかんの房のような **月形**（2 つの頂点が球の反対側にある）ができる。
角が $\alpha$ の月形の面積は、球面全体 $4\pi$ の $\dfrac{\alpha}{2\pi}$ なので $2\alpha$。

球面三角形 ABC の 3 辺をのばして大円にすると、角 $\alpha, \beta, \gamma$ の月形と、その反対側の月形が 1 組ずつできる。
この 6 つの月形で球面全体がおおわれ、三角形 ABC とその反対側の三角形だけが 3 回ずつ（2 回よけいに）数えられるので、三角形の面積を $S$ とすると

$$2(2\alpha + 2\beta + 2\gamma) = 4\pi + 4S\qquad\Longrightarrow\qquad S = \alpha + \beta + \gamma - \pi$$

半径 $R$ の球では面積は $R^2$ 倍。$E = \alpha + \beta + \gamma - \pi$ を **球過量** という。
"""
    )

with st.expander("📖 発展：球面三角法の公式とその導き方"):
    st.markdown(
        r"""
下の公式はすべて、余弦法則から出発して **加法定理・和積公式・半角公式・比の性質（合除比の理）** だけで導ける
（河瀬 2019）。$s = \dfrac{a + b + c}{2}$。このアプリでは、すべての公式が成り立つことを数値で確かめている。

| 公式 | 式 | 主に使うもの |
|:--|:--|:--|
| 余弦法則 | $\cos a = \cos b\cos c + \sin b\sin c\cos\alpha$ | 距離の 2 乗（上の方法）、または内積 |
| 正弦法則 | $\dfrac{\sin\alpha}{\sin a} = \dfrac{\sin\beta}{\sin b} = \dfrac{\sin\gamma}{\sin c}$ | 余弦法則、$\sin^2 = 1 - \cos^2$ |
| 正接法則 | $\dfrac{\tan\frac{\alpha - \beta}{2}}{\tan\frac{\alpha + \beta}{2}} = \dfrac{\tan\frac{a - b}{2}}{\tan\frac{a + b}{2}}$ | 正弦法則、合除比の理、和積公式 |
| 半角公式 | $\tan\dfrac{\alpha}{2} = \sqrt{\dfrac{\sin(s - b)\sin(s - c)}{\sin s\,\sin(s - a)}}$ | 余弦法則、半角公式、和積公式 |
| ドランブルの公式 | $\dfrac{\sin\frac{\alpha + \beta}{2}}{\cos\frac{\gamma}{2}} = \dfrac{\cos\frac{a - b}{2}}{\cos\frac{c}{2}},\ \ \dfrac{\cos\frac{\alpha + \beta}{2}}{\sin\frac{\gamma}{2}} = \dfrac{\cos\frac{a + b}{2}}{\cos\frac{c}{2}}$ | 半角公式、加法定理 |
| ジラールの定理 | $S = \alpha + \beta + \gamma - \pi$ | 月形の面積 |
| リュイリエの公式 | $\tan\dfrac{E}{4} = \sqrt{\tan\dfrac{s}{2}\tan\dfrac{s - a}{2}\tan\dfrac{s - b}{2}\tan\dfrac{s - c}{2}}$ | ドランブルの公式、和積公式 |

平面の三角形の公式（正弦定理・余弦定理・ヘロンの公式）と見比べてみよう。三角形が小さいときは、それぞれ平面の公式に近づく。
"""
    )
    st.markdown(
        f"- 河瀬和重「[球面三角法の簡潔かつ体系的な理解への試み]({PAPER_PAGE})」国土地理院時報 132 集（2019）（[PDF]({PAPER_PDF})）\n"
        "  　加法定理と比例式だけを使って、上の公式を短く体系的に導いている。詳しい導き方は原文を参照。"
    )

with st.expander("🔧 どこで使われている？"):
    st.markdown(
        r"""
- **航海・航空**：出発地と目的地の緯度・経度から、北極を頂点とする球面三角形を解いて、**距離**（余弦法則）と **出発する方向**（正弦法則など）を求める。
- **測量・地図**：広い範囲の面積は、地球を平面とみなすと誤差が出る。地球の表面での面積は、球面三角形の面積（ジラール・リュイリエの公式）をもとに計算する。
  逆に、小さい範囲なら平面とみなしてよい（② のタブで、三角形を小さくすると角の和が 180° に近づく）。
- **天文学**：星の位置を天球（大きな球）の上の点と考え、星と星の間の角距離などを球面三角法で計算する。
"""
    )
    st.page_link("views/survey.py", label="都市系：測量と三角比", icon="📐")

with st.expander("📝 考えてみよう"):
    st.markdown(
        r"""
1. 北極と赤道上の経度 0°・経度 90° の 3 点でできる球面三角形の角の和を求めよう。面積は球面全体の何分の 1 か。
2. 単位球の上で、角が $90^\circ, 60^\circ, 60^\circ$ の球面三角形の面積を求めよう。
3. 余弦法則 $\cos c = \cos a\cos b + \sin a\sin b\cos\gamma$ で $a = b = 90^\circ$ とすると、$c$ と $\gamma$ の関係はどうなるか。図で意味を考えよう。
"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""
1. 角はすべて $90^\circ$ なので和は $270^\circ$。$E = \dfrac{3\pi}{2} - \pi = \dfrac{\pi}{2}$ で、球面全体 $4\pi$ の $\dfrac{1}{8}$
2. $\dfrac{\pi}{2} + \dfrac{\pi}{3} + \dfrac{\pi}{3} - \pi = \dfrac{\pi}{6}$
3. $\cos c = \cos\gamma$ より $c = \gamma$。C が北極、A, B が赤道上の点なので、赤道上の弧 AB の中心角は、経度の差（北極での角 $\gamma$）に等しい。
"""
        )

st.page_link("views/spherical_coords.py", label="前へ：球面座標と緯度・経度", icon="⬅️")
st.page_link("views/ex_advanced.py", label="演習（発展）へ", icon="✏️")
