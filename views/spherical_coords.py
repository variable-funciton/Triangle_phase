"""球面座標と緯度・経度（発展）

グラフと操作はブラウザ側で動かす（assets/spherical_coords.html, assets/spherical_coords_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title("球面座標と緯度・経度")
st.markdown(
    r"平面の点は $(x, y)$ のかわりに「原点からの距離 $r$ と角 $\theta$」でも表せます（**極座標**）。"
    r"空間の点も、距離と **2 つの角** で表せます（**球面座標**）。地球上の位置を表す **緯度・経度** はその一例です。"
    r"どれも、直角三角形の $\cos$・$\sin$ をくり返し使うだけで $(x, y, z)$ に直せます。"
)

render("spherical_coords", height=1240)

with st.expander("📖 解説：極座標から球面座標へ"):
    st.markdown(
        r"""
**平面の極座標**　原点からの距離 $r$ と、$x$ 軸から測った角 $\theta$ で点を表す。

$$x = r\cos\theta,\qquad y = r\sin\theta\qquad\left(r = \sqrt{x^2 + y^2}\right)$$

**球面座標**　原点からの距離 $r$、$z$ 軸から測った角 $\theta$（$0 \le \theta \le \pi$）、
$x$ 軸から測った角 $\varphi$（$0 \le \varphi < 2\pi$）で点 P を表す。P から $xy$ 平面に下ろした点を P' とすると

1. **縦の直角三角形** OPP'：$\;z = r\cos\theta,\quad \mathrm{OP'} = \rho = r\sin\theta$
2. **床の直角三角形**（$xy$ 平面の極座標）：$\;x = \rho\cos\varphi,\quad y = \rho\sin\varphi$

まとめると

$$x = r\sin\theta\cos\varphi,\qquad y = r\sin\theta\sin\varphi,\qquad z = r\cos\theta$$

確かめ：$x^2 + y^2 + z^2 = r^2\sin^2\theta(\cos^2\varphi + \sin^2\varphi) + r^2\cos^2\theta = r^2$

**緯度・経度**　地理では角を **赤道から** 測る（緯度）。緯度 $= 90^\circ - \theta$、経度 $= \varphi$（東経を ＋、西経を −）。
余角の公式 $\sin(90^\circ - \theta) = \cos\theta$ により sin と cos が入れかわり、半径 $R$ の地球の上の点は

$$x = R\cos(\text{緯度})\cos(\text{経度}),\quad y = R\cos(\text{緯度})\sin(\text{経度}),\quad z = R\sin(\text{緯度})$$

緯度 $\varphi$ の緯線は半径 $R\cos\varphi$ の円なので、その長さは $2\pi R\cos\varphi$。
"""
    )

with st.expander("📖 解説：2 都市の距離（大円距離）"):
    st.markdown(
        r"""
球面上の 2 点を結ぶ最短の道は、球の中心 O を通る平面で切った円（**大円**）の弧。
中心角を $\theta$（ラジアン）とすると、弧の長さは扇形と同じく $R\theta$。

$\theta$ は、2 点の位置ベクトルの内積（2 年生で学ぶ）から求められる。緯度 $\varphi_1, \varphi_2$、経度 $\lambda_1, \lambda_2$ のとき

$$\cos\theta = \sin\varphi_1\sin\varphi_2 + \cos\varphi_1\cos\varphi_2\cos(\lambda_2 - \lambda_1)$$

（成分を代入して、加法定理 $\cos\lambda_1\cos\lambda_2 + \sin\lambda_1\sin\lambda_2 = \cos(\lambda_2 - \lambda_1)$ でまとめると出てくる。）
これは、北極と 2 都市でできる **球面三角形の余弦法則** と同じ式。次のページ「球面三角形」で、内積を使わずに導く。

**特別な場合**
- 同じ経線上（$\lambda_1 = \lambda_2$）：$\cos\theta = \cos(\varphi_1 - \varphi_2)$ より、$\theta = |\varphi_1 - \varphi_2|$（緯度の差）
- 両方とも赤道上（$\varphi_1 = \varphi_2 = 0$）：$\theta = |\lambda_1 - \lambda_2|$（経度の差、180° 以下のとき）
"""
    )

with st.expander("🔧 どこで使われている？"):
    st.markdown(
        r"""
- **GPS・地図アプリ**：位置は緯度・経度（と高さ）で表され、2 地点の距離は上の大円距離の式（やその改良版）で計算される。
- **飛行機・船の航路**：東京からヨーロッパや北米へ向かう便が北極に近いルートを通るのは、大円が最短だから。
- **測量**：国土地理院の測量計算サイトでは、2 地点の緯度・経度から距離と方位角を計算できる（[距離と方位角の計算](https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2sth.html)）。
  地球を少しつぶれた回転楕円体として計算するので、球として計算したこのページの値とは少し（0.5% 以内）ちがう。
- **3D の CG・ロボット・電波**：アンテナの向き、カメラの向き、ロボットアームの関節の角度なども球面座標で表すことが多い。
"""
    )

with st.expander("📝 考えてみよう"):
    st.markdown(
        r"""
1. 球面座標 $r = 2,\ \theta = 60^\circ,\ \varphi = 90^\circ$ の点の $(x, y, z)$ を求めよう。
2. 地球を半径 6400 km の球とするとき、北緯 60° の緯線の長さは赤道の何倍か。
3. 北緯 30°・東経 135° の地点と、北緯 60°・東経 135° の地点の大円距離を求めよう（R = 6400 km）。
"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""
1. $x = 2\sin 60^\circ\cos 90^\circ = 0,\ y = 2\sin 60^\circ\sin 90^\circ = \sqrt{3},\ z = 2\cos 60^\circ = 1$
2. $\cos 60^\circ = \dfrac{1}{2}$ 倍（$6400\pi \approx 20100$ km）
3. 同じ経線上なので中心角は $30^\circ = \dfrac{\pi}{6}$。距離は $6400\times\dfrac{\pi}{6} = \dfrac{3200}{3}\pi \approx 3350$ km
"""
        )

st.page_link("views/spherical_triangle.py", label="次へ：球面三角形（球面三角法）", icon="➡️")
st.page_link("views/ex_advanced.py", label="演習（発展）へ", icon="✏️")
