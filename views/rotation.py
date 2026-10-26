"""回転と弧度法（車輪・歯車・ベルト）

グラフと操作はブラウザ側で動かす（assets/rotation.html, assets/rotation_core.js）。
"""

import streamlit as st

from utils.widget import render

st.title('回転と弧度法（車輪・歯車・ベルト）')
st.markdown(
    r"""回転する機械では、角度を **弧度法（ラジアン）** で表すと、弧の長さ $r\theta$・周速 $v = r\omega$ が簡単に書けます。車輪・歯車・ベルト車のアニメーションで確かめよう。"""
)

render('rotation', height=970)

with st.expander("📖 解説"):
    st.markdown(
        r"""**弧の長さ**　半径 $r$、中心角 $\theta$ [rad] の弧の長さは $r\theta$。すべらずに転がる車輪は、回った角 $\theta$ に対して $r\theta$ だけ進む。

**回転数と角速度**　1 分間に $N$ 回転（$N$ rpm）すると、1 秒間に回る角（角速度）は

$$\omega = \frac{2\pi N}{60}\ \text{[rad/s]}$$

**周速**　円周上の点の速さ $v = r\omega$。車なら、タイヤの半径と回転数から速さがわかる。

**歯車**　かみ合う点の速さが同じなので $r_1\omega_1 = r_2\omega_2$。歯の大きさがそろっていれば半径は歯数に比例するので

$$N_2 = N_1\times\frac{z_1}{z_2}\quad(\text{回る向きは反対})$$

**ベルト車**　ベルトがすべらなければ $r_1\theta_1 = r_2\theta_2$、$N_2 = N_1\times\dfrac{r_1}{r_2}$（回る向きは同じ）。"""
    )

with st.expander("📝 練習問題"):
    st.markdown(
        r"""1. 半径 30 cm の車輪が 120 rpm で回っている。角速度 $\omega$ と、すべらずに転がるときの速さ [km/h] を求めよ。
2. 歯数 15 の歯車が 1200 rpm で回り、歯数 45 の歯車とかみ合っている。歯数 45 の歯車の回転数を求めよ。
3. 1 rad とはどんな角か、弧の長さを使って説明せよ。"""
    )
    with st.popover("答え"):
        st.markdown(
            r"""1. $\omega = \frac{2\pi\times 120}{60} = 4\pi \approx 12.57$ rad/s。$v = 0.3\times 4\pi \approx 3.77$ m/s $\approx 13.6$ km/h
2. $1200\times\frac{15}{45} = 400$ rpm（反対向き）
3. 弧の長さが半径と等しくなるときの中心角（約 57.3°）"""
        )

with st.expander("🔗 参考リンク・関連ページ"):
    st.markdown(
        """- [コトバンク「ラジアン」](https://kotobank.jp/word/%E3%83%A9%E3%82%B8%E3%82%A2%E3%83%B3-147143)：弧の長さが半径に等しいときの中心角。辞典・百科事典の解説"""
    )
    st.caption("外部サイトのリンクは 2026 年 10 月に確認したものです。")
    st.page_link('views/basics.py', label='公式まとめ（ラジアンと扇形）', icon="➡️")
