"""分子の形と結合角（余弦定理）

グラフと操作はブラウザ側で動かす（assets/molecule.html, assets/molecule_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('分子の形と結合角（余弦定理）')
st.markdown(
    r"""水やメタンなどの分子では、原子が決まった角度（**結合角**）で結びついています。結合角と結合距離から、余弦定理で原子どうしの距離を求め、メタンの 109.5° がどこから来るかを立方体で考えよう。"""
)

render('molecule', height=830)

with st.expander("📖 解説"):
    st.markdown(
        r"""**原子どうしの距離**　中心の原子 O から 2 つの原子 H までの距離（結合距離）を $a$、結合角を $\theta$ とすると、
三角形 HOH に余弦定理を使って

$$d^2 = a^2 + a^2 - 2a\cdot a\cos\theta,\qquad d = \sqrt{2a^2(1 - \cos\theta)} = 2a\sin\frac{\theta}{2}$$

（最後の変形は半角の公式 $1 - \cos\theta = 2\sin^2\frac{\theta}{2}$）

**いろいろな分子の形**

| 分子 | 結合角 | 形 |
|:--|:--:|:--|
| 二酸化炭素 CO₂ | 180° | 直線形 |
| 三フッ化ホウ素 BF₃ | 120° | 平面三角形 |
| メタン CH₄ | 109.5° | 正四面体形 |
| アンモニア NH₃ | 約 107° | 三角錐形 |
| 水 H₂O | 約 104.5° | 折れ線形 |

**メタンの 109.5°**　立方体の中心に C、となり合わない 4 頂点に H を置くと正四面体になる。
立方体の 1 辺を 2 とすると C−H $= \sqrt{3}$、H−H $= 2\sqrt{2}$ なので、余弦定理から $\cos\theta = -\dfrac{1}{3}$、$\theta \approx 109.47^\circ$。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 水分子の O−H を 0.096 nm、結合角を 104.5° として、H と H の距離を求めよ。
2. BF₃（B−F 0.131 nm、120°）で、F と F の距離を求めよ。
3. CO₂（C=O 0.116 nm、180°）で、O と O の距離を求めよ。余弦定理を使うとどうなるか。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $d = 2\times 0.096\times\sin 52.25^\circ \approx 0.152$ nm
2. $d = \sqrt{3}\times 0.131 \approx 0.227$ nm（$\cos 120^\circ = -\frac{1}{2}$ より $d^2 = 3a^2$）
3. $\cos 180^\circ = -1$ より $d^2 = 4a^2$、$d = 2a = 0.232$ nm（一直線なので単純に 2 倍）"""
        )
