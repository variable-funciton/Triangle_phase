"""逆三角関数の主値（arcsin, arccos, arctan）の視覚化

グラフと操作はブラウザ側で動かす（assets/inverse_trig.html, assets/inverse_trig_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title("逆三角関数と主値")
st.markdown(
    r"$y = \sin x$ のグラフを直線 $y = x$ で折り返すと、逆関数 $y = \arcsin x$ のグラフになります。"
    "ただし、そのまま折り返すと 1 つの x に y がたくさん対応してしまうので、"
    "**x の範囲を制限（主値）** してから折り返します。k を動かして確かめよう。"
)

render("inverse_trig", height=1070)

with st.expander("📖 解説：逆関数と主値"):
    st.markdown(
        r"""
**逆関数とは**　$y = f(x)$ の $x$ と $y$ の役割を入れかえたもの。点 $(a, b)$ がもとのグラフ上にあれば、
点 $(b, a)$ は逆関数のグラフ上にある。$(a, b)$ と $(b, a)$ は **直線 $y = x$ に関して対称** なので、
逆関数のグラフはもとのグラフを $y = x$ で折り返したものになる。

**なぜ制限が必要か**　逆関数が「関数」であるためには、$x$ を 1 つ決めたら $y$ が 1 つに決まらなければならない。
$y = \sin x$ は同じ値を何度もとる（周期関数）ので、そのまま折り返すと 1 つの $x$ に無数の $y$ が対応してしまう
（「制限しないで折り返すと？」にチェックを入れると、赤い × がたくさん並ぶ）。
そこで、**値をちょうど 1 回ずつとる区間** に制限する。これを **主値** という。

| 関数 | もとの関数を制限する区間 | 逆関数の定義域 | 逆関数の値域（主値） |
|:--|:--:|:--:|:--:|
| $\arcsin x = \sin^{-1}x$ | $-\frac{\pi}{2} \le x \le \frac{\pi}{2}$ | $-1 \le x \le 1$ | $-\frac{\pi}{2} \le y \le \frac{\pi}{2}$ |
| $\arccos x = \cos^{-1}x$ | $0 \le x \le \pi$ | $-1 \le x \le 1$ | $0 \le y \le \pi$ |
| $\arctan x = \tan^{-1}x$ | $-\frac{\pi}{2} < x < \frac{\pi}{2}$ | すべての実数 | $-\frac{\pi}{2} < y < \frac{\pi}{2}$ |

**読み方**　$\arcsin\frac{1}{2}$ は「sin の値が $\frac{1}{2}$ になる角のうち、主値の範囲にあるもの」なので $\frac{\pi}{6}$。

**注意**　$\sin^{-1}x$ は $\dfrac{1}{\sin x}$ ではない（$-1$ 乗の記号を使っているが、逆数ではなく逆関数の意味）。
"""
    )

with st.expander("📝 三角方程式の解と主値"):
    st.markdown(
        r"""
方程式 $\sin x = k$（$-1 \le k \le 1$）の解は、主値 $\theta = \arcsin k$ を使って

$$x = \theta + 2n\pi,\qquad x = (\pi - \theta) + 2n\pi \qquad (n \text{ は整数})$$

と全部書ける。単位円で y 座標が $k$ の点は 2 つあり、1 つが $\theta$、もう 1 つが $\pi - \theta$。

同じように、

- $\cos x = k$ の解：$x = \pm\theta + 2n\pi$（$\theta = \arccos k$）
- $\tan x = k$ の解：$x = \theta + n\pi$（$\theta = \arctan k$、tan の周期は $\pi$）

「$0 \le x < 2\pi$ の範囲で解け」のように範囲が決まっているときは、一般解の $n$ に整数を入れて範囲内のものを選ぶ。
グラフでは、緑の点線 $y = k$ と灰色の曲線の交点が解、そのうち青い部分（主値の範囲）にある交点 P が主値。

**練習**　グラフで確かめながら答えよう。

1. $\arcsin\left(-\frac{\sqrt{3}}{2}\right)$、$\arccos\left(-\frac{\sqrt{3}}{2}\right)$、$\arctan(-1)$ を求めよ。
2. $0 \le x < 2\pi$ のとき、$\sin x = -\frac{1}{2}$ を解け。
3. $\arcsin x + \arccos x$ はいつも同じ値になる。いくつか試して値を予想せよ。
"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""
1. $-\frac{\pi}{3}$、$\frac{5\pi}{6}$、$-\frac{\pi}{4}$
2. $x = \frac{7\pi}{6},\ \frac{11\pi}{6}$（主値は $-\frac{\pi}{6}$ で範囲外。$-\frac{\pi}{6} + 2\pi$ と $\pi - (-\frac{\pi}{6})$）
3. いつも $\frac{\pi}{2}$（$\sin\theta = \cos\left(\frac{\pi}{2} - \theta\right)$ から）
"""
        )
