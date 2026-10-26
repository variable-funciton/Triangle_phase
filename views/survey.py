"""測量（高さ・川幅・トラバース）

グラフと操作はブラウザ側で動かす（assets/survey.html, assets/survey_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('測量（高さ・川幅・トラバース）')
st.markdown(
    r"""測量は三角比の代表的な応用です。仰角から高さを求める（tan）、川を渡らずに川幅を求める（**正弦定理**）、距離と方位角から座標を求める（cos・sin）の 3 つを体験しよう。"""
)

render('survey', height=860)

with st.expander("📖 解説"):
    st.markdown(
        r"""**① 高さ**　水平距離 $d$、仰角 $\theta$、器械の高さ $e$ から $H = d\tan\theta + e$。

**② 川幅（三角測量）**　こちらの岸の基線 AB $= c$ と、向こう岸の点 C を見る角 $\alpha$、$\beta$ を測る。
$\angle C = 180^\circ - \alpha - \beta$、正弦定理 $\dfrac{AC}{\sin\beta} = \dfrac{c}{\sin C}$ より $AC = \dfrac{c\sin\beta}{\sin(\alpha + \beta)}$、川幅 $= AC\sin\alpha$。

**③ トラバース測量**　測点を順に結び、各辺の距離 $L$ と方位角 $a$（**北から時計回り**）を測る。座標の変化は

$$\Delta x = L\cos a\ (\text{北向き}),\qquad \Delta y = L\sin a\ (\text{東向き})$$

測量の座標は、数学と x・y が入れかわる（x が北、y が東）。一周して出発点にもどらないずれを閉合誤差といい、
一周の長さとの比（閉合比、例えば 1/5000）で精度を表す。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 建物から 30 m はなれた所で、目の高さ 1.5 m から屋上を見上げた角が 35° だった。建物の高さを求めよ（$\tan 35^\circ = 0.700$）。
2. 基線 AB = 50 m、$\alpha = 70^\circ$、$\beta = 60^\circ$ のとき、川幅を求めよ。
3. 方位角 30°、距離 100 m の辺の $\Delta x$、$\Delta y$ を求めよ。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $30\times 0.700 + 1.5 = 22.5$ m
2. $AC = \frac{50\sin 60^\circ}{\sin 130^\circ} \approx 56.53$ m、川幅 $= 56.53\sin 70^\circ \approx 53.1$ m
3. $\Delta x = 100\cos 30^\circ \approx 86.6$ m（北へ）、$\Delta y = 100\sin 30^\circ = 50$ m（東へ）"""
        )

with st.expander("🔗 参考リンク・関連ページ"):
    st.markdown(
        """- [国土地理院「三角点の役割」](https://www.gsi.go.jp/sokuchikijun/sankaku-role.html)：地図や測量の基準になる三角点の役割
- [国土地理院 中部地方測量部「基準点とは」](https://www.gsi.go.jp/chubu/profile-kijunten-kijunten.html)：電子基準点・三角点・水準点など、位置と高さの基準"""
    )
    st.caption("外部サイトのリンクは 2026 年 10 月に確認したものです。")
    st.page_link('views/basics.py', label='公式まとめ（正弦定理・余弦定理）', icon="➡️")
