"""三相交流（3 つの sin の和が 0）

グラフと操作はブラウザ側で動かす（assets/three_phase.html, assets/three_phase_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('三相交流（3 つの sin の和が 0）')
st.markdown(
    r"""発電所では 120° ずつずれた 3 つの交流（**三相交流**）を作って送ります。$\sin\theta + \sin(\theta - 120^\circ) + \sin(\theta - 240^\circ) = 0$ を、グラフと回転するベクトルで確かめよう。"""
)

render('three_phase', height=920)

with st.expander("📖 解説"):
    st.markdown(
        r"""**和が 0 になる理由（加法定理）**　$\sin(\theta - 240^\circ) = \sin(\theta + 120^\circ)$ なので

$$\sin(\theta - 120^\circ) + \sin(\theta + 120^\circ) = 2\sin\theta\cos 120^\circ = -\sin\theta$$

よって 3 つの和は $\sin\theta - \sin\theta = 0$。（加法定理で 2 つを展開して足しても同じ）

**回転するベクトルで見ると**　120° ずつ開いた同じ長さの 3 本の矢印をつなげると正三角形になり、出発点にもどる → 和は 0。

**なぜ便利か**　3 つの電流の和がいつも 0 なので、もどりの電線がいらず、3 本の電線で送電できる。
また、3 つのコイルに流すと回転する磁界ができ、モーターをなめらかに回せる。

**線間電圧**　2 本の電線の間の電圧は

$$\sin\theta - \sin(\theta - 120^\circ) = \sqrt{3}\sin(\theta + 30^\circ)$$

（和積の公式または三角関数の合成）で、相の電圧の $\sqrt{3}$ 倍。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 加法定理を使って $\sin\theta + \sin(\theta - 120^\circ) + \sin(\theta + 120^\circ) = 0$ を示せ。
2. $\sin\theta - \sin(\theta - 120^\circ) = \sqrt{3}\sin(\theta + 30^\circ)$ を示せ。
3. 相の電圧（実効値）が約 115 V の三相交流で、線間電圧（実効値）はおよそ何 V か。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $\sin(\theta \mp 120^\circ) = \sin\theta\cos 120^\circ \mp \cos\theta\sin 120^\circ = -\frac{1}{2}\sin\theta \mp \frac{\sqrt{3}}{2}\cos\theta$。2 つの和は $-\sin\theta$ なので、全体は 0。
2. 左辺 $= \sin\theta + \frac{1}{2}\sin\theta + \frac{\sqrt{3}}{2}\cos\theta = \frac{3}{2}\sin\theta + \frac{\sqrt{3}}{2}\cos\theta = \sqrt{3}\left(\frac{\sqrt{3}}{2}\sin\theta + \frac{1}{2}\cos\theta\right) = \sqrt{3}\sin(\theta + 30^\circ)$
3. $115\times\sqrt{3} \approx 199$ V（三相 200 V）"""
        )
