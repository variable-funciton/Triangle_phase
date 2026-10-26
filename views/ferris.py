"""観覧車の高さ（三角関数のグラフ）

グラフと操作はブラウザ側で動かす（assets/ferris.html, assets/ferris_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('観覧車の高さ（三角関数のグラフ）')
st.markdown(
    r"""観覧車のゴンドラの高さは、時間 $t$ の三角関数 $h = h_0 - r\cos\frac{2\pi t}{T}$ で表せます。半径・1 周の時間・乗り場の高さを変えて、一般形 $y = A\sin B(x - \alpha) + \beta$ の各パラメータが何を表すか確かめよう。"""
)

render('ferris', height=1040)

with st.expander("📖 解説"):
    st.markdown(
        r"""**式の作り方**　観覧車の中心（軸）の高さを $h_0$、半径を $r$ とする。乗り場（いちばん下）から反時計回りに角 $\theta$ だけ回ると、
ゴンドラは中心より $r\cos\theta$ だけ下にあるので $h = h_0 - r\cos\theta$。1 周 $T$ 分で $2\pi$ 回るので $\theta = \dfrac{2\pi t}{T}$。

**一般形との対応**　$-\cos\theta = \sin\left(\theta - \dfrac{\pi}{2}\right)$ を使うと

$$h = r\sin\frac{2\pi}{T}\left(t - \frac{T}{4}\right) + h_0$$

| 一般形 | 観覧車では |
|:--:|:--|
| 振幅 $A$ | 半径 $r$ |
| 周期 $\frac{2\pi}{B}$ | 1 周の時間 $T$ |
| 平行移動 $\alpha$ | $\frac{T}{4}$（中心の高さを上向きに通る時刻） |
| $\beta$ | 中心の高さ $h_0$ |

**高さ $H$ 以上にいる時間**　$h \ge H$ ⇔ $\cos\theta \le \dfrac{h_0 - H}{r}$。この不等式の解の範囲が、下のグラフのオレンジの帯です。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""半径 50 m、1 周 16 分、いちばん下のゴンドラの高さ 5 m の観覧車（中心の高さ 55 m）について：

1. 乗ってから 4 分後の高さを求めよ。
2. 乗ってから初めて高さ 80 m になるのは何分後か。
3. 1 周のうち、高さ 80 m 以上にいるのは何分間か。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $\theta = \frac{2\pi\cdot 4}{16} = \frac{\pi}{2}$ なので $h = 55 - 50\cos\frac{\pi}{2} = 55$ m（中心と同じ高さ）
2. $55 - 50\cos\theta = 80$ ⇔ $\cos\theta = -\frac{1}{2}$ ⇔ $\theta = \frac{2\pi}{3}$。$t = 16\times\frac{1}{3} = \frac{16}{3} \approx 5.33$ 分後
3. $\frac{2\pi}{3} \le \theta \le \frac{4\pi}{3}$ の間なので、$16\times\frac{1}{3} = \frac{16}{3} \approx 5.33$ 分間"""
        )

with st.expander("🔗 参考リンク・関連ページ"):
    st.page_link('views/general_form.py', label='一般形 y = A sin B(x − α) + β', icon="➡️")
    st.page_link('views/inverse_trig.py', label='逆三角関数と主値（cos θ = c をみたす θ）', icon="➡️")
