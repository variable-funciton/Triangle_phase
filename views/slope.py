"""勾配の表し方（%・‰・寸勾配と tan）

グラフと操作はブラウザ側で動かす（assets/slope.html, assets/slope_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('勾配の表し方（%・‰・寸勾配と tan）')
st.markdown(
    r"""道路の「10%」、鉄道の「80‰」、屋根の「4 寸勾配」、スロープの「1/12」——どれも $\tan\theta$（高さ ÷ 水平距離）で坂の急さを表しています。"""
)

render('slope', height=920)

with st.expander("📖 解説"):
    st.markdown(
        r"""**いろいろな勾配の表し方**（どれも $\tan\theta$ を使う）

| 表し方 | 式 | 使われる場面 |
|:--|:--:|:--|
| パーセント | $100\tan\theta$ [%] | 道路 |
| パーミル | $1000\tan\theta$ [‰] | 鉄道 |
| 寸勾配 | $10\tan\theta$ [寸] | 建築の屋根 |
| 比 $1 : n$ | $n = \dfrac{1}{\tan\theta}$ | スロープ、土木の法面（のりめん） |

**角度との関係**　$\theta = \arctan(\text{勾配})$。100% は 45°。% と角度は比例しないが、小さい角では $\tan\theta \approx \theta$ [rad] なのでほぼ比例する。

**斜距離と水平距離**　坂に沿った長さ $s$ に対して、水平距離 $= s\cos\theta$、高さ $= s\sin\theta$。地図上の距離は水平距離。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 「10%」の坂の角度は約何度か。
2. 車いす用スロープの基準「1/12」は何 % か。角度は約何度か。
3. 10% の坂を 200 m 進んだ。上がった高さと水平距離を求めよ。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $\tan\theta = 0.1$ より $\theta \approx 5.7^\circ$
2. $\frac{1}{12} \approx 8.3\%$、$\theta \approx 4.8^\circ$
3. $\theta \approx 5.71^\circ$ なので、高さ $200\sin 5.71^\circ \approx 19.9$ m、水平距離 $200\cos 5.71^\circ \approx 199.0$ m"""
        )
