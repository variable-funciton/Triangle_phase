"""交流と三角関数

グラフと操作はブラウザ側で動かす（assets/ac.html, assets/ac_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('交流と三角関数')
st.markdown(
    r"""コンセントの電気（交流）の電圧は $v = V_m\sin 2\pi f t$ と表されます。周波数 50 Hz と 60 Hz、最大値と **実効値**（100 V）、回転するベクトルとの関係を見てみよう。"""
)

render('ac', height=1200)

with st.expander("📖 解説"):
    st.markdown(
        r"""**交流の式**　$v = V_m\sin\omega t$、$\omega = 2\pi f$（角周波数）、周期 $T = \dfrac{1}{f}$。
日本では東日本が $f = 50$ Hz、西日本が $f = 60$ Hz（明治時代に輸入した発電機のちがいによる）。

**回転するベクトル**　長さ $V_m$ の矢印が角速度 $\omega$ で回るとき、その先端の高さが $v$。等速円運動の影が単振動になるのと同じ。

**実効値**　抵抗に交流を流したときの平均の電力が、直流 $V$ [V] と同じになる電圧。電力は $v^2$ に比例するので、
2 倍角の公式 $\sin^2\omega t = \dfrac{1 - \cos 2\omega t}{2}$ を使うと

$$\overline{v^2} = \frac{V_m^2}{2}\quad\Rightarrow\quad V = \sqrt{\overline{v^2}} = \frac{V_m}{\sqrt{2}}$$

家庭の「100 V」は実効値で、最大値は約 141 V。

**位相**　電流 $i = I_m\sin(\omega t - \varphi)$ が電圧より $\varphi$ 遅れる（コイル）・進む（コンデンサ）ことがある。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 実効値 100 V の交流の最大値を求めよ。実効値 200 V ではどうか。
2. 60 Hz の交流の周期 [ms] と角周波数 $\omega$ を求めよ。
3. 50 Hz の交流 $v = 141\sin 100\pi t$ で、$t = 2.5$ ms のときの $v$ を求めよ。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $100\sqrt{2} \approx 141$ V、$200\sqrt{2} \approx 283$ V
2. $T = \frac{1}{60}$ s $\approx 16.7$ ms、$\omega = 120\pi \approx 377$ rad/s
3. $100\pi\times 0.0025 = \frac{\pi}{4}$ なので $v = 141\sin\frac{\pi}{4} \approx 99.7$ V（$\approx 100$ V）"""
        )
