"""演習：加法定理の応用（三角関数の合成、合成と最大・最小、積和・和積の公式）

問題は exercises/addition.py の生成関数で作る。画面・LaTeX・PDF は exercises/core.py（応用数学ラボと同じしくみ）。
"""

import streamlit as st

from exercises import addition as ex
from exercises.core import render

st.title('演習：加法定理の応用')
st.caption('三角関数の合成、合成と最大・最小、積和・和積の公式')
render('addition', ex.REGISTRY, ex.TITLE)
