"""演習：三角関数の応用（物理）（斜方投射、バネの単振動、波、モンキーハンティング、リサージュ図形）

問題は exercises/physics.py の生成関数で作る。画面・LaTeX・PDF は exercises/core.py（応用数学ラボと同じしくみ）。
"""

import streamlit as st

from exercises import physics as ex
from exercises.core import render

st.title('演習：三角関数の応用（物理）')
st.caption('斜方投射、バネの単振動、波、モンキーハンティング、リサージュ図形')
render('physics', ex.REGISTRY, ex.TITLE)
