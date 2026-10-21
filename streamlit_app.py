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
    ],
    "三角関数のグラフ": [
        st.Page("views/general_form.py", title="一般形 y = A sin B(x − t) + β", icon="🌊",
                url_path="general_form"),
        st.Page("views/phase_shift.py", title="sin と cos の位相差", icon="🔁", url_path="phase_shift"),
    ],
    "グラフの変換と合成": [
        st.Page("views/tent_map.py", title="テントマップの変換と合成", icon="⛺", url_path="tent_map"),
    ],
    "加法定理の応用": [
        st.Page("views/synthesis.py", title="三角関数の合成", icon="🧭", url_path="synthesis"),
        st.Page("views/product_sum.py", title="積和・和積の公式", icon="🔀", url_path="product_sum"),
    ],
    "三角関数の応用": [
        st.Page("views/projectile.py", title="斜方投射（45° で最も遠くへ）", icon="🏀", url_path="projectile"),
        st.Page("views/fourier.py", title="三角関数の足し合わせ（フーリエ級数）", icon="🎼", url_path="fourier"),
        st.Page("views/monkey.py", title="モンキーハンティング", icon="🐒", url_path="monkey"),
        st.Page("views/spring.py", title="バネの単振動と波", icon="〰️", url_path="spring"),
    ],
}

st.navigation(PAGES).run()
