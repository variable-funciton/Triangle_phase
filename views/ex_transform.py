"""演習：グラフの変換と合成（合成関数の値、変換したグラフの頂点、合成のくり返し、漸化式）

問題は exercises/transform.py の生成関数で作る。画面・LaTeX・PDF は exercises/core.py（応用数学ラボと同じしくみ）。
"""

import streamlit as st

from exercises import transform as ex
from exercises.core import render

st.title('演習：グラフの変換と合成')
st.caption('合成関数の値、変換したグラフの頂点、合成のくり返し、漸化式')
render('transform', ex.REGISTRY, ex.TITLE)
