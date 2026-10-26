"""三角関数の動くグラフ（数学IB 後期）— エントリーポイント

Streamlit Community Cloud では Main file path に このファイル (streamlit_app.py) を指定する。
ページを増やすときは views/ にファイルを作り、下の PAGES に 1 行追加する。
"""

import streamlit as st

st.set_page_config(page_title="三角関数の動くグラフ", page_icon="📈", layout="wide")

PAGES = {
    "はじめに": [
        st.Page("views/home.py", title="ホーム", icon="🏠", default=True),
    ],
    "基礎知識": [
        st.Page("views/basics.py", title="三角比・三角関数の公式まとめ", icon="📚", url_path="basics"),
        st.Page("views/ex_basics.py", title="演習（基礎）", icon="✏️", url_path="ex_basics"),
    ],
    "三角関数のグラフ": [
        st.Page("views/general_form.py", title="一般形 y = A sin B(x − α) + β", icon="🌊",
                url_path="general_form"),
        st.Page("views/phase_shift.py", title="sin と cos の位相差", icon="🔁", url_path="phase_shift"),
        st.Page("views/ex_graph.py", title="演習（グラフ）", icon="✏️", url_path="ex_graph"),
    ],
    "グラフの変換と合成": [
        st.Page("views/tent_map.py", title="テントマップの変換と合成", icon="⛺", url_path="tent_map"),
        st.Page("views/ex_transform.py", title="演習（変換と合成）", icon="✏️", url_path="ex_transform"),
    ],
    "加法定理の応用": [
        st.Page("views/addition_theorem.py", title="加法定理とその証明", icon="➕", url_path="addition_theorem"),
        st.Page("views/synthesis.py", title="三角関数の合成", icon="🧭", url_path="synthesis"),
        st.Page("views/product_sum.py", title="積和・和積の公式", icon="🔀", url_path="product_sum"),
        st.Page("views/ex_addition.py", title="演習（加法定理の応用）", icon="✏️", url_path="ex_addition"),
    ],
    "三角関数の応用": [
        st.Page("views/projectile.py", title="斜方投射（45° で最も遠くへ）", icon="🏀", url_path="projectile"),
        st.Page("views/fourier.py", title="三角関数の足し合わせ（フーリエ級数）", icon="🎼", url_path="fourier"),
        st.Page("views/monkey.py", title="モンキーハンティング", icon="🐒", url_path="monkey"),
        st.Page("views/spring.py", title="バネの単振動と波", icon="〰️", url_path="spring"),
        st.Page("views/lissajous.py", title="媒介変数表示とリサージュ図形", icon="➰", url_path="lissajous"),
        st.Page("views/ex_physics.py", title="演習（物理への応用）", icon="✏️", url_path="ex_physics"),
    ],
    "学科共通の応用": [
        st.Page("views/ferris.py", title="観覧車の高さ", icon="🎡", url_path="ferris"),
        st.Page("views/seasons.py", title="季節の変化（気温・昼の長さ）", icon="🌡️", url_path="seasons"),
        st.Page("views/ex_applied.py", title="演習（学科別の応用）", icon="✏️", url_path="ex_applied"),
    ],
    "機械系のための三角関数": [
        st.Page("views/crank.py", title="クランク機構", icon="⚙️", url_path="crank"),
        st.Page("views/rotation.py", title="回転と弧度法（車輪・歯車・ベルト）", icon="🛞", url_path="rotation"),
        st.Page("views/incline.py", title="斜面と力の分解（摩擦角）", icon="📦", url_path="incline"),
    ],
    "電気系のための三角関数": [
        st.Page("views/ac.py", title="交流と三角関数", icon="🔌", url_path="ac"),
        st.Page("views/three_phase.py", title="三相交流", icon="⚡", url_path="three_phase"),
        st.Page("views/ac_power.py", title="交流の電力と力率", icon="💡", url_path="ac_power"),
    ],
    "化学系のための三角関数": [
        st.Page("views/molecule.py", title="分子の形と結合角", icon="🧪", url_path="molecule"),
        st.Page("views/bragg.py", title="X 線回折（ブラッグの法則）", icon="💎", url_path="bragg"),
    ],
    "都市系のための三角関数": [
        st.Page("views/shadow.py", title="日影と建物の間隔", icon="🏢", url_path="shadow"),
        st.Page("views/survey.py", title="測量（高さ・川幅・トラバース）", icon="📏", url_path="survey"),
        st.Page("views/slope.py", title="勾配の表し方（%・‰・寸）", icon="⛰️", url_path="slope"),
    ],
    "発展（逆関数・微分・球面への入り口）": [
        st.Page("views/inverse_trig.py", title="逆三角関数と主値", icon="↩️", url_path="inverse_trig"),
        st.Page("views/tangent_slope.py", title="接線の傾きと cos x", icon="📐", url_path="tangent_slope"),
        st.Page("views/taylor.py", title="テイラー展開（多項式で近似）", icon="🧮", url_path="taylor"),
        st.Page("views/spherical_coords.py", title="球面座標と緯度・経度", icon="🌐", url_path="spherical_coords"),
        st.Page("views/spherical_triangle.py", title="球面三角形（球面三角法）", icon="🔺", url_path="spherical_triangle"),
        st.Page("views/ex_advanced.py", title="演習（発展）", icon="✏️", url_path="ex_advanced"),
    ],
}

st.navigation(PAGES).run()
