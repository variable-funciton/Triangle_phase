"""モンキーハンティングの詳しい解説（三角比・等加速度運動・相対運動の考え方で説明する）"""

import math

import streamlit as st

G = 9.8


def render(a: float, b: float, v0: float):
    r = math.hypot(a, b)
    th = math.degrees(math.atan2(b, a))
    ts = r / v0
    fall = 0.5 * G * ts ** 2
    h = b - fall
    vmin = math.sqrt(G * (a * a + b * b) / (2 * b))
    tb = math.sqrt(2 * b / G)

    st.markdown("### 0. どんな問題か")
    st.markdown(
        "猟師が木の上のサル（B）を狙って弾（A）を撃つ。サルは銃口が光ったのを見た瞬間に手を放して落ちる（光はほぼ一瞬で届くので「同時」とみなせる。音だと遅れて届くので同時にならない）。"
        "サルは助かるだろうか？——という話から **モンキーハンティング** と呼ばれます。\n\n"
        "**結論**：まっすぐサルを狙って撃てば、弾が地面に落ちる前に届くかぎり **必ず当たる**。"
        "「サルは落ちるのだから、少し下を狙うべき」という直感は間違いです。"
    )

    st.markdown("### 1. 準備")
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**A（斜方投射）**：初速度 $v_0$、角度 $\\theta$")
        st.latex(r"x_A = v_0\cos\theta\cdot t,\qquad y_A = v_0\sin\theta\cdot t - \frac{1}{2}gt^2")
    with c2, st.container(border=True):
        st.markdown("**B（自由落下）**：高さ $b$ から静かに落ちる")
        st.latex(r"x_B = a,\qquad y_B = b - \frac{1}{2}gt^2")
    st.caption("どちらも「斜方投射」のページと同じ等加速度運動の式。B は初速度 0 の等加速度運動。")

    st.markdown("### 2. 狙う角度 θ（三角比）")
    st.markdown(r"原点 O から点 $(a, b)$ を見上げる角が $\theta$。O と $(a, b)$ の距離は三平方の定理で $\sqrt{a^2 + b^2}$。")
    st.latex(r"\tan\theta = \frac{b}{a},\qquad \cos\theta = \frac{a}{\sqrt{a^2 + b^2}},\qquad \sin\theta = \frac{b}{\sqrt{a^2 + b^2}}")
    st.latex(rf"\text{{いまの設定：}}\ \tan\theta = \frac{{{b}}}{{{a}}},\quad \sqrt{{{a}^2 + {b}^2}} \approx {r:.3f},\quad \theta \approx {th:.2f}^\circ")

    st.markdown("### 3. A が B の真下（真上）に来る時刻")
    st.latex(r"x_A = a \;\Longrightarrow\; v_0\cos\theta\cdot t^* = a \;\Longrightarrow\; t^* = \frac{a}{v_0\cos\theta} = \frac{a}{v_0}\cdot\frac{\sqrt{a^2+b^2}}{a} = \frac{\sqrt{a^2+b^2}}{v_0}")
    st.markdown(r"$t^*$ は「O から B までの距離 ÷ 初速度」。重力がなければ、A がまっすぐ B に着く時刻と同じです。")

    st.markdown("### 4. そのときの高さをくらべる")
    st.latex(r"y_A = v_0\sin\theta\cdot t^* - \frac{1}{2}g{t^*}^2 = v_0\cdot\frac{b}{\sqrt{a^2+b^2}}\cdot\frac{\sqrt{a^2+b^2}}{v_0} - \frac{1}{2}g{t^*}^2 = b - \frac{1}{2}g{t^*}^2")
    st.latex(r"y_B = b - \frac{1}{2}g{t^*}^2")
    st.markdown(r"**$y_A = y_B$**。同じ時刻に同じ場所 → ぶつかる。$v_0$ がいくつでも（地面に落ちる前なら）成り立ちます。")

    st.markdown("### 5. なぜ必ず当たるのか（考え方）")
    st.markdown(
        "A の動きは、次の 2 つを **たし合わせた** ものと考えられます。\n\n"
        "1. 重力がないときの動き：狙いの直線の上を、まっすぐ等速で B に向かう\n"
        "2. 重力による落下：真下に $\\frac{1}{2}gt^2$ だけずれる\n\n"
        "B も同じで、「重力がなければ (a, b) に止まっている」位置から、真下に $\\frac{1}{2}gt^2$ だけずれます。\n\n"
        "**A も B も、同じ時刻には同じ長さ $\\frac{1}{2}gt^2$ だけ落ちている** ので、"
        "重力がない場合に出会う時刻（$t^*$）に、重力があってもやはり出会います。"
        "① のアニメーションの緑の線（落ちた距離）がいつも同じ長さなのは、このためです。"
    )
    with st.expander("別の見方：B と一緒に落ちる人から見ると（相対運動）"):
        st.markdown(
            "B と一緒に自由落下するエレベーターの中にいる人を考えます。この人から見ると、重力の影響は A にも B にも、"
            "自分にも同じだけはたらくので **打ち消されて** 見えます（無重力のように見える）。\n\n"
            "その人から見ると B は止まっていて、A は最初の向き（B の方向）にまっすぐ等速で進んでくる。"
            "だから必ず当たります。宇宙ステーションの中で物が浮いて見えるのと同じ理由です。"
        )

    st.markdown("### 6. 当たる条件（初速度はどれだけ必要？）")
    st.markdown(r"ぶつかる前に B（と A）が地面に着いてしまうと外れます。ぶつかる高さが 0 より大きければよいので")
    st.latex(r"b - \frac{1}{2}g{t^*}^2 > 0 \;\Longleftrightarrow\; b - \frac{g(a^2+b^2)}{2v_0^2} > 0 \;\Longleftrightarrow\; v_0^2 > \frac{g(a^2+b^2)}{2b}")
    st.latex(r"v_0 > \sqrt{\frac{g(a^2+b^2)}{2b}}")
    st.markdown(
        r"- B が地面に着く時刻は $\sqrt{2b/g}$。$t^* < \sqrt{2b/g}$ という条件を整理しても同じ式になる。" "\n"
        r"- A が先に地面に着く条件（$t^*$ が A の滞空時間 $2v_0\sin\theta/g$ より長い）を整理しても同じ式になる。" "\n"
        r"- 遠い（$a$ が大きい）ほど、また低い（$b$ が小さい）ほど、速く撃つ必要がある。"
    )

    st.markdown(f"### 7. 例題（いまの設定：a = {a} m、b = {b} m、v₀ = {v0} m/s）")
    st.latex(rf"t^* = \frac{{\sqrt{{{a}^2 + {b}^2}}}}{{{v0}}} \approx \frac{{{r:.3f}}}{{{v0}}} \approx {ts:.3f}\ \text{{s}}")
    st.latex(rf"\frac{{1}}{{2}}g{{t^*}}^2 \approx \frac{{1}}{{2}}\times 9.8\times {ts:.3f}^2 \approx {fall:.3f}\ \text{{m}}"
             rf"\quad\Longrightarrow\quad \text{{ぶつかる高さ}}\ {b} - {fall:.3f} \approx {h:.3f}\ \text{{m}}")
    st.latex(rf"v_{{\min}} = \sqrt{{\frac{{9.8\times({a}^2 + {b}^2)}}{{2\times {b}}}}} \approx {vmin:.3f}\ \text{{m/s}},\qquad"
             rf"\text{{B が地面に着く時刻}}\ \sqrt{{2\times {b}/9.8}} \approx {tb:.3f}\ \text{{s}}")
    if v0 > vmin:
        st.success(f"v₀ = {v0} m/s は v_min ≈ {vmin:.2f} m/s より大きいので、高さ {h:.2f} m の位置で当たります。")
    else:
        st.error(f"v₀ = {v0} m/s は v_min ≈ {vmin:.2f} m/s 以下なので、空中では当たりません。")

    st.markdown("### 8. よくある間違い")
    st.markdown(
        "- **落ちるぶん下を狙う** → 下を狙うと、A は B の下を通りすぎる（③ のタブで確かめられる）。狙うのは B そのもの。\n"
        "- **速く撃てばいつでも当たる／遅くても当たる** → 当たるのは v₀ > v_min のときだけ。"
        "遅すぎると、出会う前に地面に落ちる。\n"
        "- **B を放すのが少し遅れても当たる** → B が高い位置に残り、A は B の下を通る。「同時に」が必要。\n"
        "- **空気抵抗があっても当たる** → 空気抵抗は A と B で同じではない（速さが違う）ので、厳密には当たらない。"
    )

    st.markdown("### 9. 練習問題")
    p_vmin = math.sqrt(G * 500 / 20)
    p_t = math.sqrt(500) / 20
    p_h = 10 - 0.5 * G * p_t ** 2
    with st.expander("問1　a = 20 m、b = 10 m のとき、当たるための初速度の最小値を求めよ。"):
        st.latex(rf"v_0 > \sqrt{{\frac{{9.8\times(400 + 100)}}{{2\times 10}}}} = \sqrt{{245}} \approx {p_vmin:.2f}\ \text{{m/s}}")
    with st.expander("問2　問1 の状況で v₀ = 20 m/s のとき、ぶつかる時刻と高さを求めよ。"):
        st.latex(rf"t^* = \frac{{\sqrt{{500}}}}{{20}} \approx {p_t:.3f}\ \text{{s}},\qquad y = 10 - \frac{{1}}{{2}}\times 9.8\times\frac{{500}}{{400}} = {p_h:.3f}\ \text{{m}}")
    p_v5 = math.sqrt(G * 500 / (2 * 5))
    with st.expander("問3　問1 の状況で、高さ 5 m 以上の位置で当てたい。初速度はいくら以上必要か。"):
        st.latex(rf"10 - \frac{{9.8\times 500}}{{2v_0^2}} \ge 5 \;\Longrightarrow\; v_0^2 \ge \frac{{9.8\times 500}}{{10}} = 490"
                 rf"\;\Longrightarrow\; v_0 \ge {p_v5:.2f}\ \text{{m/s}}")
    with st.expander("問4　狙う角度 θ を、tan を使わずに sin と cos で答えよ（a = 20 m、b = 10 m）。"):
        st.latex(r"\sqrt{20^2 + 10^2} = 10\sqrt{5},\qquad \cos\theta = \frac{20}{10\sqrt{5}} = \frac{2}{\sqrt{5}},\qquad \sin\theta = \frac{10}{10\sqrt{5}} = \frac{1}{\sqrt{5}}")
        st.markdown("θ ≈ 26.57° は有名角ではないので、このように sin・cos の値で表す。")
