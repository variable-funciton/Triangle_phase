"""演習：発展（逆三角関数・接線・テイラー展開）（逆三角関数の主値、接線の傾き、テイラー展開）

問題は exercises/advanced.py の生成関数で作る。画面・LaTeX・PDF は exercises/core.py（応用数学ラボと同じしくみ）。
"""

import streamlit as st

from exercises import advanced as ex
from exercises.core import render

st.title('演習：発展（逆三角関数・接線・テイラー展開）')
st.caption('逆三角関数の主値、接線の傾き、テイラー展開')
render('advanced', ex.REGISTRY, ex.TITLE)
