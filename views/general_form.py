"""三角関数の一般形 y = A f(B(x − α)) + β の動くグラフ（後期課題4〜6 対応）

スライダーをドラッグしている間もグラフと式が連続的に変わるように、操作部分とグラフは
ブラウザ側（HTML + JavaScript、Plotly.js と KaTeX）で動かしている。
Streamlit のスライダーは手を離したときにしか値が送られないため。サーバーへの通信も起きないので、
クラス全員が同時に動かしても負荷はかからない。

  assets/general_form_core.js  計算と式の組み立て（テスト: node tests/test_general_form_js.js）
  assets/general_form.html     画面（表示の設定・パラメータ・式・グラフ）
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ASSETS = Path(__file__).resolve().parent.parent / "assets"


@st.cache_data
def build_html() -> str:
    core = (ASSETS / "general_form_core.js").read_text(encoding="utf-8")
    page = (ASSETS / "general_form.html").read_text(encoding="utf-8")
    return page.replace("/*__CORE__*/", core)


st.title("三角関数の一般形と平行移動")
st.markdown(
    r"$y = A\sin B(x - \alpha) + \beta$ の 4 つのパラメータを動かして、"
    r"**振幅・周期・平行移動** がグラフにどう表れるか確かめよう。"
    "スライダーを動かすと、グラフと式がそのまま連続的に変わります。"
)

components.html(build_html(), height=1260, scrolling=True)

with st.expander("使い方のヒント"):
    st.markdown(
        "- **表示の設定**（上の囲み）で、基本の関数（sin / cos）、角度の単位（弧度法 / 度数法）、"
        "α の入れ方（π の倍数 / 小数）を選びます。\n"
        "- **パラメータ**（下の囲み）の 4 つのスライダーで A, B, α, β を動かします。"
        "スライダーの両側の −／＋ ボタンで少しずつ動かすこともできます"
        "（パソコンではスライダーをクリックしてから矢印キーでも動かせます）。\n"
        "- 「① 重ねて比較」の **キーポイントと矢印** にチェックを入れると、"
        "基本形の 5 つの点が変形後にどこへ移ったかが矢印で見られます。\n"
        "- **Bx − α の形と比べる** にチェックを入れると、"
        r"$\sin B(x-\alpha)$ と $\sin(Bx-\alpha)$ の平行移動の量の違い（後期課題6）を比べられます。" "\n"
        "- 「② 段階的に変形」では、基本形から ①→⑤ の順に 1 つずつ変形していく様子を確かめられます。"
    )
