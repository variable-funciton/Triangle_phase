"""クランク機構（回転と往復運動）

グラフと操作はブラウザ側で動かす（assets/crank.html, assets/crank_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('クランク機構（回転と往復運動）')
st.markdown(
    r"""エンジンのピストンとクランクのしくみ。クランクの回転角 $\theta$ からピストンの位置 $x$ を、**余弦定理** で求めます。単振動 $x = l + r\cos\theta$ とのちがいも見てみよう。"""
)

render('crank', height=1180)

with st.expander("📖 解説"):
    st.markdown(
        r"""**しくみ**　クランク（半径 $r$）が回転すると、連接棒（長さ $l$）でつながったピストンが往復する。
エンジンでは逆に、燃料の爆発でピストンが押され、その往復運動を回転に変える。

**ピストンの位置**　三角形 OPQ（O：クランクの中心、P：クランクピン、Q：ピストンピン）で、OP $= r$、PQ $= l$、OQ $= x$、∠POQ $= \theta$。
余弦定理より

$$l^2 = r^2 + x^2 - 2rx\cos\theta$$

これを $x$ の 2 次方程式として解くと（正の解）

$$x = r\cos\theta + \sqrt{l^2 - r^2\sin^2\theta}$$

**単振動との比較**　$l$ が $r$ に比べてとても長いと、$\sqrt{l^2 - r^2\sin^2\theta} \approx l$ となり、$x \approx l + r\cos\theta$（単振動）。
実際のエンジンでは $l/r$ は 3〜4 くらいで、単振動から少しずれる。

**連接棒の傾き**　正弦定理 $\dfrac{r}{\sin\varphi} = \dfrac{l}{\sin\theta}$ から $\sin\varphi = \dfrac{r\sin\theta}{l}$。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""$r = 4$ cm、$l = 12$ cm のクランク機構について：

1. ストローク（ピストンが往復する長さ）を求めよ。
2. $\theta = 90^\circ$ のときのピストンの位置 $x$ を求め、単振動 $l + r\cos\theta$ の値と比べよ。
3. $\theta = 60^\circ$ のときの $x$ を求めよ。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $2r = 8$ cm（上死点 $l + r = 16$ cm、下死点 $l - r = 8$ cm）
2. $x = 0 + \sqrt{144 - 16} = \sqrt{128} = 8\sqrt{2} \approx 11.31$ cm。単振動では 12 cm なので、約 0.69 cm ずれる。
3. $x = 4\times\frac{1}{2} + \sqrt{144 - 16\times\frac{3}{4}} = 2 + \sqrt{132} \approx 13.49$ cm"""
        )

with st.expander("🔗 参考リンク・関連ページ"):
    st.markdown(
        """- [東京理科大学「機構学」講義資料 第 1 章 機械と機構（PDF）](https://www.rs.noda.tus.ac.jp/nog/documents/kikougaku/kikou02.pdf)：ピストン・クランク機構を例に、機構の基本（リンクと対偶）を説明"""
    )
    st.caption("外部サイトのリンクは 2026 年 10 月に確認したものです。")
    st.page_link('views/basics.py', label='公式まとめ（正弦定理・余弦定理）', icon="➡️")
    st.page_link('views/spring.py', label='バネの単振動', icon="➡️")
