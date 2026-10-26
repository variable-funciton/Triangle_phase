"""演習：三角関数のグラフ（周期、最大値・最小値、平行移動、グラフから式を読む、三角方程式・不等式、角の変換）

問題は exercises/graph.py の生成関数で作る。画面・LaTeX・PDF は exercises/core.py（応用数学ラボと同じしくみ）。
"""

import streamlit as st

from exercises import graph as ex
from exercises.core import render

st.title('演習：三角関数のグラフ')
st.caption('周期、最大値・最小値、平行移動、グラフから式を読む、三角方程式・不等式、角の変換')
render('graph', ex.REGISTRY, ex.TITLE)
