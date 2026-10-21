"""ばねの単振動・摩擦・抵抗・波の詳しい解説（微分を使わず、等速円運動の影とエネルギーで説明する）"""

import math

import streamlit as st

G = 9.8


def render(m: float, k: float, x0: float, model: str, mu: float, gamma: float):
    w = math.sqrt(k / m)
    T = 2 * math.pi / w

    st.markdown("### 0. ばねの力（フックの法則）")
    st.markdown(
        "ばねを自然の長さから $x$ だけ伸ばす（縮める）と、ばねは **もとに戻そうとする向き** に、"
        "ずれ $x$ に比例する力を出します。"
    )
    st.latex(r"F = -kx\qquad(k:\ \text{ばね定数 [N/m]})")
    st.markdown("マイナスは「ずれと反対向き」を表します。この「ずれに比例して、もとに戻そうとする力」がはたらくと、"
                "おもりは自然の長さの位置（つり合いの位置）を中心に往復運動します。これが **単振動** です。")

    st.caption("※ 1〜3 は摩擦や空気抵抗がない理想的な場合。摩擦・抵抗があるときは 4・5 を見よう。")
    st.markdown("### 1. 等速円運動の影として見る")
    st.markdown(
        r"半径 $A$ の円の上を、一定の角速度 $\omega$ [rad/s]（1 秒間に回る角）で回る点 P を考えます。"
        r"時刻 $t$ に回った角は $\omega t$ なので、三角関数の定義から P の座標は $(A\cos\omega t,\ A\sin\omega t)$。"
        r"P に横から光を当てたときの **影（x 座標）** の動きが単振動です。"
    )
    st.latex(r"x = A\cos\omega t,\qquad T = \frac{2\pi}{\omega}\quad(\text{1 周 } 2\pi \text{ rad 回る時間}),\qquad f = \frac{1}{T}")
    st.markdown(
        "- 影は中心を通るときに **いちばん速く**、両端で **一瞬止まって** 折り返す。ばねのおもりと同じ動き。\n"
        r"- P の速さは $A\omega$（円周 $2\pi A$ を時間 $T$ で回る）。影の速さはその x 方向の成分で $v = -A\omega\sin\omega t$。"
        r" 最大の速さは中心で $A\omega$。"
    )

    st.markdown("### 2. なぜ ω = √(k/m) になるのか（微分なしの説明）")
    st.markdown(
        r"等速円運動をする点 P には、円の **中心向き** に大きさ $A\omega^2$ の加速度（向心加速度）があります（物理で学ぶ）。"
        r"その x 方向の成分（影の加速度）は、P の位置の x 座標に比例して中心向きなので"
    )
    st.latex(r"a = -\omega^2 x")
    st.markdown(r"一方、ばねのおもりは運動方程式 $ma = F = -kx$ より $a = -\dfrac{k}{m}x$。2 つの式をくらべると")
    st.latex(r"\omega^2 = \frac{k}{m}\quad\Longrightarrow\quad \omega = \sqrt{\frac{k}{m}},\qquad T = 2\pi\sqrt{\frac{m}{k}}")
    st.markdown(
        "- **重いほど**（m が大きいほど）ゆっくり振動する。**ばねが強いほど**（k が大きいほど）速く振動する。\n"
        "- 周期は **振幅 A によらない**（等時性）。大きく振っても小さく振っても往復の時間は同じ。"
    )

    st.markdown("### 3. エネルギーで見る")
    st.latex(r"\frac{1}{2}kx^2 + \frac{1}{2}mv^2 = \frac{1}{2}kA^2\quad(\text{一定})")
    st.markdown(
        r"ばねにたくわえられたエネルギー $\frac{1}{2}kx^2$ と、運動エネルギー $\frac{1}{2}mv^2$ が入れかわりながら、"
        r"合計は変わりません。$x = A\cos\omega t,\ v = -A\omega\sin\omega t$ を代入すると、"
        r"$\sin^2\omega t + \cos^2\omega t = 1$（相互関係）と $m\omega^2 = k$ から確かめられます。"
    )

    st.markdown("### 4. 動摩擦があるとき：振幅は等差数列で減る")
    st.markdown(
        r"床との間に動摩擦があると、おもりが動いている間、動く向きと反対に一定の力 $\mu mg$（$\mu$：動摩擦係数）がはたらきます。"
        r"片道（ある折り返し点から反対側の折り返し点まで）でのエネルギーの減り方を考えます。"
    )
    st.latex(r"\underbrace{\frac{1}{2}ka_n^2 - \frac{1}{2}ka_{n+1}^2}_{\text{ばねのエネルギーの減少}} = \underbrace{\mu mg\,(a_n + a_{n+1})}_{\text{摩擦が奪うエネルギー（力}\times\text{動いた距離）}}")
    st.markdown(r"左辺を因数分解すると $\frac{1}{2}k(a_n + a_{n+1})(a_n - a_{n+1})$。両辺を $a_n + a_{n+1}$ で割って")
    st.latex(r"a_n - a_{n+1} = \frac{2\mu mg}{k}\quad(\text{一定})\qquad\Longrightarrow\qquad a_n = x_0 - n\cdot\frac{2\mu mg}{k}")
    st.markdown(
        r"- 振幅は片道ごとに同じ量ずつ減る **等差数列**（後期課題9）。" "\n"
        r"- 折り返し点では一瞬止まる。そのときばねの力 $ka_n$ が最大の静止摩擦力 $\mu mg$ 以下（$a_n \le \dfrac{\mu mg}{k}$）なら、"
        r"もう動き出せずに **止まる**。だから有限の回数で止まる。" "\n"
        r"- 往復の時間（周期）は摩擦がないときと同じ $2\pi\sqrt{m/k}$。つり合いの位置が $\pm\dfrac{\mu mg}{k}$ だけずれた単振動を半周期ずつつなげた動きになる。"
    )

    st.markdown("### 5. 速さに比例する抵抗（空気・水）があるとき：振幅は等比数列で減る")
    st.markdown(
        "空気や水の抵抗は、おおよそ **速さに比例** します。振幅が大きいときは速く動くので抵抗も大きく、"
        "振幅が小さくなると抵抗も小さくなります。その結果、1 回の往復で失われるエネルギーは、そのときのエネルギーの "
        "**一定の割合** になり、振幅は折り返すたびに同じ **倍率** で小さくなります。"
    )
    st.latex(r"a_n = x_0\,r^{\,n}\quad(0 < r < 1)\qquad(\text{等比数列、後期課題10})")
    st.markdown("等比数列なので 0 に近づくがちょうど 0 にはならない（いつまでも小さく振動する）。"
                "グラフのオレンジの線（振れ幅の包み）は、時間とともに一定の割合で減る **指数関数** の形になります。")

    st.markdown("### 6. 波：単振動が伝わっていく")
    st.markdown(
        "ひもやばねの 1 か所を単振動させると、その振動がとなりへ、となりへと伝わります。これが **波** です。"
        "各点はその場で単振動するだけで、物が流れていくわけではありません（進むのは **振動の形** と **エネルギー**）。"
    )
    st.latex(r"y = A\sin 2\pi\left(\frac{t}{T} - \frac{x}{\lambda}\right),\qquad v = \frac{\lambda}{T} = f\lambda")
    st.markdown(
        "**注意：x–t グラフと y–x グラフの区別**\n\n"
        "- **単振動の x–t グラフ**は、1 つのおもりの位置を時間を追ってかいたもの（横軸は時刻 t）。\n"
        "- **波の y–x グラフ（波形）**は、ある瞬間のたくさんの点の位置を写真のように写したもの（横軸は場所 x）。\n\n"
        r"波の式で場所 $x$ を固定すると、その点の x–t グラフ（単振動）になり、時刻 $t$ を固定すると y–x グラフ（波形）になる。"
        "形が似ていても、何を横軸にとったグラフなのかを必ず確認しよう。"
    )
    st.markdown(
        r"- 原点の点は $y = A\sin\dfrac{2\pi}{T}t$ で振動する。場所 $x$ の点は、振動が届くまでの時間 $\dfrac{x}{v}$ だけ **遅れて** 同じ振動をする。" "\n"
        r"  $\sin\dfrac{2\pi}{T}\left(t - \dfrac{x}{v}\right) = \sin 2\pi\left(\dfrac{t}{T} - \dfrac{x}{\lambda}\right)$（$vT = \lambda$）。" "\n"
        "- **横波**：振動の向きが進む向きと垂直。例：ひも・弦の波、光（電磁波）、地震の S 波。\n"
        "- **縦波**：振動の向きが進む向きと平行（密と疎ができる＝ **疎密波**）。例：音（空気中で約 340 m/s）、地震の P 波。\n"
        "- 地震では P 波（縦波、速い）が先に届き、S 波（横波、遅い）があとから届く。その時間差で震源までの距離がわかる。"
    )

    st.markdown(f"### 7. 例題（いまの設定：m = {m:g} kg、k = {k:g} N/m、x₀ = {x0:g} m）")
    st.latex(rf"\omega = \sqrt{{\frac{{{k:g}}}{{{m:g}}}}} \approx {w:.3f}\ \text{{rad/s}},\qquad T = \frac{{2\pi}}{{\omega}} \approx {T:.3f}\ \text{{s}},"
             rf"\qquad f = \frac{{1}}{{T}} \approx {1 / T:.3f}\ \text{{Hz}}")
    st.latex(rf"v_{{\max}} = x_0\,\omega \approx {x0 * w:.3f}\ \text{{m/s}},\qquad a_{{\max}} = x_0\,\omega^2 \approx {x0 * w * w:.3f}\ \text{{m/s}}^2,"
             rf"\qquad E = \frac{{1}}{{2}}kx_0^2 \approx {0.5 * k * x0 * x0:.4f}\ \text{{J}}")
    if model == "friction":
        d = mu * m * G / k
        n_stop = 0 if x0 <= d else math.ceil((x0 - d) / (2 * d) - 1e-12)
        a_last = x0 - 2 * d * n_stop
        st.latex(rf"\frac{{2\mu mg}}{{k}} = \frac{{2\times {mu:g}\times {m:g}\times 9.8}}{{{k:g}}} \approx {2 * d:.4f}\ \text{{m}},"
                 rf"\qquad \frac{{\mu mg}}{{k}} \approx {d:.4f}\ \text{{m}}")
        if n_stop == 0:
            st.markdown(f"kx₀ = {k * x0:.3f} N が μmg = {mu * m * G:.3f} N 以下なので、はじめから動きません。")
        else:
            st.markdown(rf"$a_n = {x0:g} - {2 * d:.4f}\,n \le {d:.4f}$ となる最小の $n$ は **{n_stop}**。"
                        f"{n_stop} 回目の折り返し（位置 {a_last:.4f} m）で止まります。")
    elif model == "viscous":
        wd = math.sqrt(w * w - gamma * gamma)
        ratio = math.exp(-gamma * math.pi / wd)
        st.latex(rf"r = e^{{-\gamma\pi/\omega'}} \approx {ratio:.4f}\quad(\text{{折り返すたびに振幅が }} {ratio:.4f} \text{{ 倍}})")

    st.markdown("### 8. よくある間違い")
    st.markdown(
        "- **大きく振ると周期が長くなる** → 単振動の周期は振幅によらない（等時性）。\n"
        "- **端で速さが最大** → 端では一瞬止まる。速さが最大なのは中心（つり合いの位置）、加速度が最大なのは端。\n"
        "- **ω（角振動数）と f（振動数）の混同** → ω = 2πf。ω は rad/s、f は Hz（1 秒間の往復の回数）。\n"
        "- **摩擦があると周期が変わる** → 動摩擦（一定の力）では周期は変わらず、振幅だけが等差数列で減る。\n"
        "- **波では物が流れていく** → 各点はその場で振動するだけ。伝わるのは振動の形とエネルギー。"
    )

    st.markdown("### 9. 練習問題")
    p1 = 2 * math.pi * math.sqrt(0.5 / 20)
    with st.expander("問1　質量 0.5 kg のおもりを、ばね定数 20 N/m のばねにつけた。周期を求めよ。"):
        st.latex(rf"T = 2\pi\sqrt{{\frac{{0.5}}{{20}}}} = 2\pi\times 0.158\cdots \approx {p1:.3f}\ \text{{s}}")
    with st.expander("問2　おもりの質量を 4 倍にすると周期は何倍になるか。ばね定数を 4 倍にしたときはどうか。"):
        st.markdown(r"$T = 2\pi\sqrt{m/k}$ より、$m$ を 4 倍 → $\sqrt{4} = 2$ 倍。$k$ を 4 倍 → $\dfrac{1}{2}$ 倍。")
    p3 = 0.2 * math.sqrt(20 / 0.5)
    with st.expander("問3　問1 のばねで、0.2 m 引いて放した。おもりの最大の速さを求めよ。"):
        st.latex(rf"v_{{\max}} = A\omega = 0.2\times\sqrt{{40}} \approx {p3:.3f}\ \text{{m/s}}")
        st.markdown(r"エネルギーで求めてもよい：$\frac{1}{2}\times 20\times 0.2^2 = \frac{1}{2}\times 0.5\times v^2$。")
    d4 = 0.1 * 0.5 * G / 20
    n4 = math.ceil((0.2 - d4) / (2 * d4) - 1e-12)
    with st.expander("問4　問3 で、床との動摩擦係数が 0.1（静止摩擦係数も 0.1）のとき、3 回折り返したあとの振幅と、何回目の折り返しで止まるかを求めよ。"):
        st.latex(rf"\frac{{2\mu mg}}{{k}} = \frac{{2\times 0.1\times 0.5\times 9.8}}{{20}} = {2 * d4:.3f},\qquad a_3 = 0.2 - 3\times {2 * d4:.3f} = {0.2 - 6 * d4:.3f}\ \text{{m}}")
        st.latex(rf"a_n = 0.2 - {2 * d4:.3f}n \le \frac{{\mu mg}}{{k}} = {d4:.4f} \;\Longrightarrow\; n \ge {(0.2 - d4) / (2 * d4):.2f}"
                 rf"\;\Longrightarrow\; {n4}\ \text{{回目で止まる（位置 }} {0.2 - 2 * d4 * n4:.4f}\ \text{{m）}}")
    with st.expander("問5　振動数 440 Hz の音（ラの音）の、空気中での波長を求めよ。音の速さは 340 m/s とする。"):
        st.latex(rf"\lambda = \frac{{v}}{{f}} = \frac{{340}}{{440}} \approx {340 / 440:.3f}\ \text{{m}}")
