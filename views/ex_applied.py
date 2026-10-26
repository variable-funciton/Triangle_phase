"""演習：学科別の応用（学科共通・機械・電気・化学・都市）

問題は exercises/applied.py の生成関数で作る。学科を選ぶと、その学科の問題の型だけにしぼれる。
"""

import streamlit as st

from exercises import applied as ex
from exercises.core import render

st.title("演習：学科別の応用")
DEPTS = ["すべて", "共通", "機械", "電気", "化学", "都市"]
dept = st.radio("学科", DEPTS, horizontal=True, key="ex_applied_dept")
reg = ex.REGISTRY if dept == "すべて" else [t for t in ex.REGISTRY if t.name.startswith(f"【{dept}】")]
render(f"applied_{DEPTS.index(dept)}", reg, ex.TITLE if dept == "すべて" else f"{ex.TITLE}（{dept}）")
