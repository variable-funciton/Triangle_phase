"""交流の電力と力率（積和の公式）

グラフと操作はブラウザ側で動かす（assets/ac_power.html, assets/ac_power_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('交流の電力と力率（積和の公式）')
st.markdown(
    r"""電力は電圧と電流の積 $p = vi$。電圧と電流がずれていると、**積和の公式** から平均の電力が $VI\cos\varphi$ に減ることがわかります。"""
)

render('ac_power', height=1150)

with st.expander("📖 解説"):
    st.markdown(
        r"""**積和の公式で変形**　$v = V_m\sin\omega t$、$i = I_m\sin(\omega t - \varphi)$ のとき、
$\sin A\sin B = -\dfrac{1}{2}\{\cos(A + B) - \cos(A - B)\}$ より

$$p = vi = \frac{V_mI_m}{2}\{\cos\varphi - \cos(2\omega t - \varphi)\}$$

第 2 項は 2 倍の速さで振動し、平均すると 0。よって平均の電力（有効電力）は

$$P = \frac{V_mI_m}{2}\cos\varphi = VI\cos\varphi\qquad(V = \tfrac{V_m}{\sqrt{2}},\ I = \tfrac{I_m}{\sqrt{2}})$$

**力率**　$\cos\varphi$ を力率という。抵抗（電熱線）だけなら $\varphi = 0$ で力率 1。
コイルだけ・コンデンサだけなら $\varphi = \pm 90^\circ$ で、平均の電力は 0（送った電力がそのままもどってくる）。
モーターや蛍光灯の安定器などはコイルを含むので力率が 1 より小さく、工場などではコンデンサを入れて力率を改善する。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 電圧 100 V、電流 5 A（ともに実効値）、電流の遅れ 60° のとき、平均の電力と力率を求めよ。
2. 同じ 100 V・5 A で、力率を 0.5 から 1 にすると、平均の電力は何倍になるか。
3. 積和の公式を使って $\sin\omega t\sin(\omega t - \varphi) = \frac{1}{2}\{\cos\varphi - \cos(2\omega t - \varphi)\}$ を確かめよ。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $P = 100\times 5\times\cos 60^\circ = 250$ W、力率 0.5
2. 250 W → 500 W で 2 倍
3. $A = \omega t$、$B = \omega t - \varphi$ とすると $A + B = 2\omega t - \varphi$、$A - B = \varphi$ なので、公式からそのまま得られる。"""
        )
