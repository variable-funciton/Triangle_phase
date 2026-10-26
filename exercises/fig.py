"""演習の図:同じ仕様(dict)から、Web 用の plotly 図と LaTeX 用の TikZ を作る

仕様の例
  {"kind": "trig", "func": "sin", "A": 2, "B": 2, "alpha": Fraction(1, 6), "beta": 0, "xr": (-1, 2)}
    y = A func(B(x − απ)) + β のグラフ(alpha と xr は π の何倍か)
"""
import math
from fractions import Fraction as F

import numpy as np

from utils.angles import pi_latex, pi_text


def _f(spec, x):
    fn = np.sin if spec["func"] == "sin" else np.cos
    return float(spec["A"]) * fn(float(spec["B"]) * (x - float(spec["alpha"]) * math.pi)) + float(spec.get("beta", 0))


def _yrange(spec):
    m = abs(float(spec["A"])) + abs(float(spec.get("beta", 0)))
    return math.ceil(m + 0.5)


def plotly_fig(spec, height=360):
    if spec is None:
        return None
    import plotly.graph_objects as go
    lo, hi = spec["xr"]
    x = np.linspace(float(lo) * math.pi, float(hi) * math.pi, 600)
    fig = go.Figure(go.Scatter(x=x, y=_f(spec, x), mode="lines", line=dict(color="#1f77b4", width=3), hoverinfo="skip"))
    step = F(1, 2)
    k0, k1 = math.ceil(F(lo) / step), math.floor(F(hi) / step)
    qs = [k * step for k in range(k0, k1 + 1)]
    Y = _yrange(spec)
    fig.update_layout(height=height, margin=dict(l=40, r=10, t=10, b=30), template="plotly_white", showlegend=False)
    fig.update_xaxes(tickvals=[float(q) * math.pi for q in qs], ticktext=[pi_text(q) for q in qs], zeroline=True,
                     zerolinecolor="black", range=[float(lo) * math.pi, float(hi) * math.pi], title_text="x", fixedrange=True)
    fig.update_yaxes(range=[-Y, Y], dtick=1, zeroline=True, zerolinecolor="black", title_text="y", fixedrange=True)
    return fig


def tikz(spec):
    """LaTeX 用の図(TikZ)。仕様がなければ空文字"""
    if spec is None or spec.get("kind") != "trig":
        return ""
    lo, hi = float(spec["xr"][0]) * math.pi, float(spec["xr"][1]) * math.pi
    xs = 14.0 / (hi - lo)          # 横幅を約 14 cm に
    Y = _yrange(spec)
    ys = 0.7 if Y <= 3 else 2.1 / Y
    A, B, al, be = float(spec["A"]), float(spec["B"]), float(spec["alpha"]) * math.pi, float(spec.get("beta", 0))
    fn = spec["func"]
    out = [rf"\begin{{center}}\begin{{tikzpicture}}[xscale={xs:.4f}, yscale={ys:.3f}]"]
    out.append(rf"\draw[->] ({lo - 0.2:.3f},0) -- ({hi + 0.4:.3f},0) node[right] {{$x$}};")
    out.append(rf"\draw[->] (0,{-Y - 0.3}) -- (0,{Y + 0.4}) node[above] {{$y$}};")
    step = F(1, 2)
    for k in range(math.ceil(F(spec["xr"][0]) / step), math.floor(F(spec["xr"][1]) / step) + 1):
        q = k * step
        if q == 0:
            continue
        xv = float(q) * math.pi
        out.append(rf"\draw[gray!40] ({xv:.4f},{-Y}) -- ({xv:.4f},{Y}); \node[below, fill=white, inner sep=1pt, font=\scriptsize] at ({xv:.4f},0) {{${pi_latex(q)}$}};")
    for yv in range(-Y, Y + 1):
        if yv == 0:
            continue
        out.append(rf"\draw[gray!40] ({lo:.3f},{yv}) -- ({hi:.3f},{yv}); \node[left, font=\scriptsize] at (0,{yv}) {{${yv}$}};")
    out.append(r"\node[below left, font=\scriptsize] at (0,0) {$O$};")
    out.append(rf"\draw[thick, domain={lo:.4f}:{hi:.4f}, samples=200] plot (\x, {{{A}*{fn}(deg({B}*(\x-({al:.6f}))))+({be})}});")
    out.append(r"\end{tikzpicture}\end{center}")
    return "\n".join(out)


def same_graph(s1, s2):
    """2 つの仕様が同じグラフになるか(数値で比べる)"""
    x = np.linspace(-7, 7, 400)
    return bool(np.allclose(_f(s1, x), _f(s2, x), atol=1e-9))
