"""X 線回折（ブラッグの法則）

グラフと操作はブラウザ側で動かす（assets/bragg.html, assets/bragg_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('X 線回折（ブラッグの法則）')
st.markdown(
    r"""結晶に X 線を当てると、特定の角度でだけ強く反射します。原子の面の間隔 $d$、角度 $\theta$、波長 $\lambda$ の関係 $2d\sin\theta = n\lambda$（**ブラッグの法則**）を、波の重ね合わせで確かめよう。"""
)

render('bragg', height=1340)

with st.expander("📖 解説"):
    st.markdown(
        r"""**道のりの差**　間隔 $d$ でならんだ原子の面に、角度 $\theta$ で X 線が入って反射する。
下の面で反射する X 線は、上の面で反射する X 線より、図の赤い部分 $d\sin\theta$ を 2 回、つまり $2d\sin\theta$ だけ長く進む。

**強め合う条件**　道のりの差が波長の整数倍なら、2 つの波の山と山がそろって強め合う：

$$2d\sin\theta = n\lambda\qquad(n = 1, 2, 3, \dots)$$

2 つの波の和は、三角関数の和（和積の公式）で $\sin x + \sin(x - \delta) = 2\cos\frac{\delta}{2}\sin\left(x - \frac{\delta}{2}\right)$ となり、
振幅 $2\left|\cos\frac{\delta}{2}\right|$ は $\delta$ が $2\pi$ の整数倍のとき最大になる。

**結晶の構造を調べる**　強く反射した角度 $\theta$ を測れば、$d = \dfrac{n\lambda}{2\sin\theta}$ で原子の面の間隔がわかる。
材料の分析、薬やタンパク質の構造の決定などに使われている。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 塩化ナトリウム（$d = 0.282$ nm）に波長 0.154 nm の X 線を当てる。$n = 1$、$n = 2$ で強め合う角度を求めよ。
2. 波長 0.154 nm の X 線で、$\theta = 20^\circ$ のとき $n = 1$ の強い反射があった。面の間隔 $d$ を求めよ。
3. $\lambda > 2d$ のとき、強め合う角度がないのはなぜか。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $\sin\theta_1 = \frac{0.154}{0.564} \approx 0.273$ → $\theta_1 \approx 15.8^\circ$、$\sin\theta_2 \approx 0.546$ → $\theta_2 \approx 33.1^\circ$
2. $d = \frac{0.154}{2\sin 20^\circ} \approx 0.225$ nm
3. $\sin\theta = \frac{n\lambda}{2d} > 1$ となり、$\sin\theta \le 1$ をみたす $\theta$ がないから。"""
        )
