"""演習：三角比・三角関数の基礎（弧度法、有名角の値、扇形、相互関係、正弦定理・余弦定理、加法定理、2倍角の公式）

問題は exercises/basics.py の生成関数で作る。画面・LaTeX・PDF は exercises/core.py（応用数学ラボと同じしくみ）。
"""

import streamlit as st

from exercises import basics as ex
from exercises.core import render

st.title('演習：三角比・三角関数の基礎')
st.caption('弧度法、有名角の値、扇形、相互関係、正弦定理・余弦定理、加法定理、2倍角の公式')
render('basics', ex.REGISTRY, ex.TITLE)
