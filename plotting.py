"""Plotly 描画の共通部品。"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import plotly.graph_objects as go

from .angles import angle_text, frac_text, pi_ticks
from .trig import Wave

COLORS = {
    "base": "#9aa0a6",
    "wave": "#1f77b4",
    "key": "#d62728",
    "steps": ["#9aa0a6", "#2ca02c", "#ff7f0e", "#9467bd", "#1f77b4"],
}

HOVER_CURVE = "x ≈ %{customdata:.3f}π<br>y = %{y:.3f}<extra>%{fullData.name}</extra>"


def x_grid(lo_pi: float, hi_pi: float, n: int = 900) -> np.ndarray:
    return np.linspace(lo_pi * np.pi, hi_pi * np.pi, n)


def y_limit(waves, margin: float = 0.4, minimum: float = 1.4) -> float:
    m = max(max(abs(float(w.y_max)), abs(float(w.y_min))) for w in waves)
    return max(minimum, m + margin)


def x_range_pi(waves, default=(-1, 3), cap: float = 9.0):
    """全ての波の 1 周期 [t, t+周期] が収まる x の範囲（π 単位）"""
    lo = min([default[0]] + [float(w.t) for w in waves])
    hi = max([default[1]] + [float(w.t + w.period) for w in waves])
    return np.floor(lo * 2) / 2, min(np.ceil(hi * 2) / 2, cap)


def curve(x, y, name, color, dash=None, width=2.5, opacity=1.0, showlegend=True) -> go.Scatter:
    return go.Scatter(
        x=x, y=y, name=name, mode="lines",
        line=dict(color=color, width=width, dash=dash),
        opacity=opacity, customdata=x / np.pi, hovertemplate=HOVER_CURVE,
        showlegend=showlegend,
    )


def key_marker(points, name, color, unit="rad", size=10, symbol="circle") -> go.Scatter:
    xs = [float(q) * np.pi for q, _ in points]
    ys = [float(v) for _, v in points]
    labels = [f"({angle_text(q, unit)}, {frac_text(v)})" for q, v in points]
    return go.Scatter(
        x=xs, y=ys, name=name, mode="markers",
        marker=dict(color=color, size=size, symbol=symbol, line=dict(color="white", width=1)),
        text=labels, hovertemplate="%{text}<extra></extra>",
    )


def add_shift_arrows(fig: go.Figure, src_points, dst_points, color=COLORS["key"]):
    """対応するキーポイント同士を矢印で結ぶ（変形で点がどこへ動いたか）"""
    for (x0, y0), (x1, y1) in zip(src_points, dst_points):
        if x0 == x1 and y0 == y1:
            continue
        fig.add_annotation(
            x=float(x1) * np.pi, y=float(y1), ax=float(x0) * np.pi, ay=float(y0),
            xref="x", yref="y", axref="x", ayref="y", text="",
            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=1.5,
            arrowcolor=color, opacity=0.75,
        )


def style_axes(fig: go.Figure, lo_pi, hi_pi, ylim, unit="rad", height=470):
    span = hi_pi - lo_pi
    step = Fraction(1, 2) if span <= 6 else Fraction(1)
    tickvals, ticktext = pi_ticks(Fraction(lo_pi).limit_denominator(4),
                                  Fraction(hi_pi).limit_denominator(4), step, unit)
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="closest",
    )
    fig.update_xaxes(
        range=[lo_pi * np.pi, hi_pi * np.pi], tickvals=tickvals, ticktext=ticktext,
        zeroline=True, zerolinecolor="black", zerolinewidth=1.2,
        gridcolor="rgba(0,0,0,0.08)", title_text="x",
    )
    fig.update_yaxes(
        range=[-ylim, ylim], zeroline=True, zerolinecolor="black", zerolinewidth=1.2,
        gridcolor="rgba(0,0,0,0.08)", dtick=1 if ylim > 2 else 0.5, title_text="y",
    )
    return fig


def add_period_band(fig: go.Figure, w: Wave, unit="rad"):
    x0, x1 = float(w.t) * np.pi, float(w.t + w.period) * np.pi
    fig.add_vrect(
        x0=x0, x1=x1, fillcolor=COLORS["wave"], opacity=0.07, line_width=0,
        annotation_text=f"1周期: {angle_text(w.t, unit)} 〜 {angle_text(w.t + w.period, unit)}",
        annotation_position="top left", annotation_font_size=12,
    )


def add_range_lines(fig: go.Figure, w: Wave):
    for val, label in [(w.y_max, "最大値"), (w.y_min, "最小値")]:
        fig.add_hline(
            y=float(val), line_dash="dot", line_color="#2ca02c", line_width=1.2,
            annotation_text=f"{label} {frac_text(val)}", annotation_position="right",
            annotation_font_color="#2ca02c",
        )
    if w.beta != 0:
        fig.add_hline(
            y=float(w.beta), line_dash="dash", line_color="#ff7f0e", line_width=1,
            annotation_text=f"中心線 y = {frac_text(w.beta)}", annotation_position="left",
            annotation_font_color="#ff7f0e",
        )
