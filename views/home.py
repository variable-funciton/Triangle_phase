"""ホーム（各ページへの案内）"""

import streamlit as st

st.title("📈 三角関数の動くグラフ")
st.markdown(
    "パラメータを動かして、三角関数のグラフがどう変わるかを自分の目で確かめるためのアプリです。"
    "左のメニュー、または下のリンクから各ページへ移動できます。"
)

with st.container(border=True):
    st.subheader("✏️ 演習（各単元の練習問題）")
    st.markdown(
        "各単元の最後に「演習」のページがあります。難易度（基本／標準）と問題の型を選ぶと、数値を変えた 4 択の類題が何度でも作れます。"
        "答えを選ぶと正誤と、まちがえたときはまちがえやすい点が表示されます。ヒントは 1 段ずつ、解答・解説も見られます。"
        "「セット番号」が同じなら同じ問題が出ます。紙で解きたいときは LaTeX 一式や PDF（問題 → 解答・解説）をダウンロードできます。"
    )
    ex_cols = st.columns(4)
    for i, (path, label) in enumerate([
        ("views/ex_basics.py", "基礎"), ("views/ex_graph.py", "グラフ"), ("views/ex_transform.py", "変換と合成"),
        ("views/ex_addition.py", "加法定理の応用"), ("views/ex_physics.py", "物理への応用"), ("views/ex_applied.py", "学科別の応用"),
        ("views/ex_advanced.py", "発展"),
    ]):
        ex_cols[i % 4].page_link(path, label=f"演習（{label}）", icon="✏️")

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

with st.container(border=True):
    st.subheader("➕ 加法定理とその証明")
    st.markdown(
        r"$\sin(\alpha \pm \beta),\ \cos(\alpha \pm \beta),\ \tan(\alpha \pm \beta)$ の公式と、単位円上の 2 点の距離を使った証明（角を動かして確かめられる図つき）。"
        r"$\sin 75^\circ = \sin(45^\circ + 30^\circ)$ のような例題も。合成・積和・和積の公式のもとになる。"
    )
    st.caption("関連: 後期課題7（加法定理）")
    st.page_link("views/addition_theorem.py", label="ページを開く", icon="➡️")

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

with st.container(border=True):
    st.subheader("➰ 媒介変数表示とリサージュ図形")
    st.markdown(
        r"$x = A\sin(at + \delta),\ y = B\sin bt$ で動く点の軌跡。振動数の比 $a : b$ と位相差 $\delta$ を"
        "スライダーで連続的に変え、横・縦の波形と図形の関係を見る。オシロスコープでの周波数・位相差の測定にも。"
    )
    st.caption("関連: 後期課題4〜6（周期・位相）・課題7（2倍角の公式）")
    st.page_link("views/lissajous.py", label="ページを開く", icon="➡️")

st.markdown("#### 学科別の応用")
st.caption("それぞれの学科の専門につながる三角関数の使われ方。どの学科の学生が見てもかまいません。")
DEPTS = [
    ("学科共通", [("views/ferris.py", "🎡 観覧車の高さ", "一般形のパラメータ＝半径・周期・中心の高さ。高さ H 以上の時間"),
                  ("views/seasons.py", "🌡️ 季節の変化", "実際の気温に sin を合わせる。昼の長さの 1 年の変化")]),
    ("機械", [("views/crank.py", "⚙️ クランク機構", "回転→往復運動。余弦定理でピストンの位置"),
              ("views/rotation.py", "🛞 回転と弧度法", "弧の長さ rθ、rpm と角速度、歯車・ベルト"),
              ("views/incline.py", "📦 斜面と力の分解", "mg sin θ と mg cos θ、摩擦角 tan θ = μ")]),
    ("電気", [("views/ac.py", "🔌 交流と三角関数", "50/60 Hz、実効値 100 V と最大値 141 V"),
              ("views/three_phase.py", "⚡ 三相交流", "120° ずれた 3 つの sin の和が 0"),
              ("views/ac_power.py", "💡 電力と力率", "積和の公式で平均の電力 VI cos φ")]),
    ("化学", [("views/molecule.py", "🧪 分子の形と結合角", "余弦定理で原子間の距離。メタンの 109.5°"),
              ("views/bragg.py", "💎 X 線回折", "2d sin θ = nλ で結晶の原子の間隔")]),
    ("都市", [("views/shadow.py", "🏢 日影と建物の間隔", "南中高度と影の長さ H / tan h"),
              ("views/survey.py", "📏 測量", "仰角で高さ、正弦定理で川幅、トラバース"),
              ("views/slope.py", "⛰️ 勾配の表し方", "%・‰・寸勾配はどれも tan θ")]),
]
dcols = st.columns(len(DEPTS))
for col, (dept, pages) in zip(dcols, DEPTS):
    with col, st.container(border=True):
        st.markdown(f"**{dept}**")
        for path, label, desc in pages:
            st.page_link(path, label=label)
            st.caption(desc)

st.markdown("#### 発展（逆関数・微分への入り口）")
c5, c6, c7 = st.columns(3)
with c5:
    with st.container(border=True):
        st.subheader("↩️ 逆三角関数と主値")
        st.markdown(
            r"$y = \sin x$ を $y = x$ で折り返して $\arcsin x$ を作る。なぜ範囲（主値）を制限するのか、"
            "三角方程式の解と主値の関係を見る。"
        )
        st.caption("関連: 後期課題3・6（三角方程式）")
        st.page_link("views/inverse_trig.py", label="ページを開く", icon="➡️")
with c6:
    with st.container(border=True):
        st.subheader("📐 接線の傾きと cos x")
        st.markdown(
            r"$\sin x$ のグラフ上を動く接線の傾きを点で打っていくと、$\cos x$ のグラフが現れる。"
            "割線から接線へ近づける様子も。"
        )
        st.caption("微分の入り口（公式は使わない）")
        st.page_link("views/tangent_slope.py", label="ページを開く", icon="➡️")
with c7:
    with st.container(border=True):
        st.subheader("🧮 テイラー展開")
        st.markdown(
            r"$\sin x,\ \cos x$ を $x = x_0$ のまわりで多項式で近似。次数を上げると重なる範囲が広がる様子と、"
            "展開した式を表示する。"
        )
        st.caption("微分の入り口（電卓の中の計算のしくみ）")
        st.page_link("views/taylor.py", label="ページを開く", icon="➡️")

st.divider()
with st.expander("使い方のヒント"):
    st.markdown(
        "- スライダーは左側のサイドバーにあります（スマートフォンでは左上の **>** を押すと開きます）。\n"
        "- グラフ上の点にカーソルを合わせる（タップする）と座標が表示されます。\n"
        "- グラフ右上のボタンで拡大・縮小や画像の保存ができます。ダブルクリックで元の表示に戻ります。"
    )
