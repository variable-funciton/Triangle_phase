"""ホーム（各ページへの案内）"""

import streamlit as st

st.title("📈 三角関数の動くグラフ")
st.markdown(
    "パラメータを動かして、三角関数のグラフがどう変わるかを自分の目で確かめるためのアプリです。"
    "左のメニュー、または下のリンクから各ページへ移動できます。"
)

with st.container(border=True):
    st.subheader("📚 三角比・三角関数の公式まとめ（基礎知識）")
    st.markdown(
        "有名角の度数法・弧度法と三角関数の値、ラジアンと扇形、相互関係、正弦定理・余弦定理、"
        "加法定理と 2 倍角・3 倍角・半角・合成・積和・和積の公式を 1 ページに。単位円・扇形・三角形の図と、公式を数値で確かめる機能つき。"
    )
    st.caption("関連: 後期課題1〜3・7・8")
    st.page_link("views/basics.py", label="ページを開く", icon="➡️")

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.subheader("🌊 一般形のグラフ")
        st.markdown(
            r"$y = A\sin B(x - \alpha) + \beta$ の **振幅・周期・平行移動** を調べる。"
            "スライダーを動かすとグラフと式が連続的に変わる。段階的な変形もあります。"
        )
        st.caption("関連: 後期課題4（グラフ）・課題5（グラフの変形）・課題6（位相がずれた方程式）")
        st.page_link("views/general_form.py", label="ページを開く", icon="➡️")
with c2:
    with st.container(border=True):
        st.subheader("🔁 sin と cos の位相差")
        st.markdown(
            r"$\sin(x - t)$ と $\cos x$ を重ねて、"
            r"**$\frac{\pi}{2}$ ずらすと一致する** ことと周期性を確かめる。"
        )
        st.caption("関連: 後期課題3（角の変換公式）・課題4・課題5")
        st.page_link("views/phase_shift.py", label="ページを開く", icon="➡️")

with st.container(border=True):
    st.subheader("⛺ テントマップの変換と合成")
    st.markdown(
        r"山形の関数 $f(x)$ を $y = a f(b(x-p)) + q$ で拡大・縮小・平行移動・反転する。"
        r"合成関数 $f(g(x))$ と $g(f(x))$ の違い、$f$ を何回も合成したグラフ、漸化式 $x_{k+1} = f(x_k)$ の蜘蛛の巣図も。"
    )
    st.caption("関連: 後期課題5（グラフの変形・合成関数）・課題12（漸化式）")
    st.page_link("views/tent_map.py", label="ページを開く", icon="➡️")

c3, c4 = st.columns(2)
with c3:
    with st.container(border=True):
        st.subheader("🧭 三角関数の合成")
        st.markdown(
            r"$a\sin x + b\cos x = R\sin(x+\alpha) = R\cos(x+\beta)$ を、点 $(a, b)$ の図・波の重ね合わせ・"
            "回転するベクトルのアニメーションで確かめる。区間での最大・最小も。"
        )
        st.caption("関連: 後期課題8（三角関数の合成）・課題6")
        st.page_link("views/synthesis.py", label="ページを開く", icon="➡️")
with c4:
    with st.container(border=True):
        st.subheader("🔀 積和・和積の公式")
        st.markdown(
            "加法定理から公式を導き、有名角でない角の計算を数値で確かめる。"
            "2 つの波の和が「うなり」になる様子もグラフで見る。"
        )
        st.caption("関連: 後期課題7（加法定理）・課題8（積和・和積）")
        st.page_link("views/product_sum.py", label="ページを開く", icon="➡️")

with st.container(border=True):
    st.subheader("🎼 三角関数の足し合わせ（フーリエ級数）")
    st.markdown(
        r"$\sin x,\ \sin 2x,\ \sin 3x, \dots$ をちょうどよい大きさで足していくと、矩形波・のこぎり波・三角波などの"
        "周期関数に近づいていく様子をアニメーションで見る。自分で係数を決めて波を作ることもできる。"
    )
    st.caption("関連: 後期課題4（周期関数）・課題5（周期の変化）。微分積分は使わない入門。")
    st.page_link("views/fourier.py", label="ページを開く", icon="➡️")

with st.container(border=True):
    st.subheader("🏀 斜方投射（物理への応用）")
    st.markdown(
        r"初速度と角度を変えてボールを投げるアニメーション。飛距離 $L = \dfrac{v_0^2}{g}\sin 2\theta$ から、"
        r"**$\theta = 45^\circ\ (\frac{\pi}{4})$ で最も遠くへ飛ぶ** ことと、余角で同じ距離になることを確かめる。"
    )
    st.caption("関連: 後期課題7（2倍角の公式）・課題1〜2（三角関数の値）")
    st.page_link("views/projectile.py", label="ページを開く", icon="➡️")

with st.container(border=True):
    st.subheader("🐒 モンキーハンティング（物理への応用）")
    st.markdown(
        "点 (a, b) を狙って投げると同時に、そこにいる物体を落とすと必ず当たる？ "
        "重力がないときの位置からのずれ ½gt² が両方で等しいことをアニメーションで確かめ、"
        r"当たるための初速度の条件 $v_0 > \sqrt{g(a^2+b^2)/2b}$ を導く。"
    )
    st.caption("関連: 後期課題1〜3（三角比の定義 tan θ = b/a）・斜方投射のページ")
    st.page_link("views/monkey.py", label="ページを開く", icon="➡️")

with st.container(border=True):
    st.subheader("〰️ バネの単振動と波（物理への応用）")
    st.markdown(
        r"ばねの単振動 $x = x_0\cos\omega t$ を等速円運動の影として見る。動摩擦や空気の抵抗があると振幅が"
        "等差数列・等比数列で減っていく様子、横波と縦波が伝わる様子をアニメーションで見る。"
    )
    st.caption("関連: 後期課題1〜5（三角関数の定義・グラフ）・課題9〜10（等差・等比数列）")
    st.page_link("views/spring.py", label="ページを開く", icon="➡️")

st.divider()
with st.expander("使い方のヒント"):
    st.markdown(
        "- スライダーは左側のサイドバーにあります（スマートフォンでは左上の **>** を押すと開きます）。\n"
        "- グラフ上の点にカーソルを合わせる（タップする）と座標が表示されます。\n"
        "- グラフ右上のボタンで拡大・縮小や画像の保存ができます。ダブルクリックで元の表示に戻ります。"
    )
