"""ブラウザ側で動く画面（assets/*.html）を Streamlit のページに埋め込む。

スライダーをドラッグしている間もグラフを連続的に変えたいページは、操作部分とグラフを
HTML + JavaScript（Plotly.js・KaTeX）で作り、ここから埋め込む。計算はすべて生徒のブラウザで行うので、
クラス全員が同時に動かしてもサーバーには負荷がかからない。

HTML の中の次の目印を、ファイルの中身に置きかえる。
  /*__CSS__*/     assets/common.css
  /*__COMMON__*/  assets/common_core.js と assets/common_ui.js
  /*__CORE__*/    assets/<name>_core.js（あれば）
"""

from __future__ import annotations

from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def build_html(name: str) -> str:
    def read(fname: str) -> str:
        p = ASSETS / fname
        return p.read_text(encoding="utf-8") if p.exists() else ""

    page = read(f"{name}.html")
    if not page:
        raise FileNotFoundError(f"assets/{name}.html がありません")
    return (page
            .replace("/*__CSS__*/", read("common.css"))
            .replace("/*__COMMON__*/", read("common_core.js") + "\n" + read("common_ui.js"))
            .replace("/*__CORE__*/", read(f"{name}_core.js")))


def render(name: str, height: int, scrolling: bool = True) -> None:
    import streamlit as st
    import streamlit.components.v1 as components

    @st.cache_data(show_spinner=False)
    def cached(n: str) -> str:
        return build_html(n)

    components.html(cached(name), height=height, scrolling=scrolling)
