"""斜面と力の分解（摩擦角）

グラフと操作はブラウザ側で動かす（assets/incline.html, assets/incline_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('斜面と力の分解（摩擦角）')
st.markdown(
    r"""斜面の上の物体にはたらく重力 $mg$ を、斜面に平行な成分 $mg\sin\theta$ と垂直な成分 $mg\cos\theta$ に分けます。どの角度ですべり出すか（**摩擦角** $\tan\theta = \mu$）を確かめよう。"""
)

render('incline', height=940)

with st.expander("📖 解説"):
    st.markdown(
        r"""**力の分解**　重力 $mg$（真下向き）を、斜面に沿った向きと斜面に垂直な向きに分ける。斜面の角を $\theta$ とすると、
重力と斜面に垂直な方向のなす角も $\theta$ になるので

- 斜面に平行な成分（すべらせる力）：$mg\sin\theta$
- 斜面に垂直な成分（斜面を押す力）：$mg\cos\theta$　→ 垂直抗力 $N = mg\cos\theta$

**摩擦力**　止まっている物体にはたらく摩擦力の最大値は $\mu N = \mu mg\cos\theta$（$\mu$：静止摩擦係数）。

**すべり出す条件**　$mg\sin\theta > \mu mg\cos\theta$ ⇔ $\tan\theta > \mu$。
ちょうどすべり出す角 $\theta_0$（$\tan\theta_0 = \mu$）を **摩擦角** という。質量に関係しない。

**すべるときの加速度**　$a = g(\sin\theta - \mu'\cos\theta)$（$\mu'$：動摩擦係数。このページでは簡単のため $\mu' = \mu$）"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 摩擦係数 $\mu = 0.5$ の斜面で、物体がすべり出す角度を求めよ。
2. 質量 2 kg の物体を角度 30° の斜面に置いた。重力の斜面に平行な成分と垂直な成分を求めよ（$g = 9.8$ m/s²）。
3. 2. で $\mu = 0.4$ のとき、物体はすべるか。すべるなら加速度はいくらか。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $\tan\theta = 0.5$ より $\theta \approx 26.6^\circ$
2. 平行：$2\times 9.8\times\sin 30^\circ = 9.8$ N、垂直：$2\times 9.8\times\cos 30^\circ = 9.8\sqrt{3} \approx 16.97$ N
3. $\tan 30^\circ \approx 0.577 > 0.4$ なのですべる。$a = 9.8(0.5 - 0.4\times 0.866) \approx 1.50$ m/s²"""
        )
