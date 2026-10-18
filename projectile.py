"""斜方投射（空気抵抗なし・地面から投げる）の計算。

    x(t) = v0 cosθ · t
    y(t) = v0 sinθ · t − g t² / 2
    滞空時間 T = 2 v0 sinθ / g
    最高点   H = v0² sin²θ / (2g)   （t = T/2 のとき）
    飛距離   L = v0 cosθ · T = 2 v0² sinθ cosθ / g = v0² sin2θ / g   ← 2倍角の公式
"""

from __future__ import annotations

import math

import numpy as np

G = 9.8  # 重力加速度 [m/s²]


def flight_time(v0: float, theta_deg: float, g: float = G) -> float:
    return 2 * v0 * math.sin(math.radians(theta_deg)) / g


def max_height(v0: float, theta_deg: float, g: float = G) -> float:
    return (v0 * math.sin(math.radians(theta_deg))) ** 2 / (2 * g)


def range_(v0: float, theta_deg: float, g: float = G) -> float:
    return v0 ** 2 * math.sin(math.radians(2 * theta_deg)) / g


def position(v0: float, theta_deg: float, t, g: float = G):
    """時刻 t（配列可）での位置。着地後は着地点にとどまる。"""
    th = math.radians(theta_deg)
    t = np.minimum(np.asarray(t, dtype=float), flight_time(v0, theta_deg, g))
    x = v0 * math.cos(th) * t
    y = v0 * math.sin(th) * t - 0.5 * g * t ** 2
    return x, np.maximum(y, 0.0)


def velocity(v0: float, theta_deg: float, t, g: float = G):
    th = math.radians(theta_deg)
    t = min(float(t), flight_time(v0, theta_deg, g))
    return v0 * math.cos(th), v0 * math.sin(th) - g * t


def trajectory(v0: float, theta_deg: float, n: int = 200, g: float = G):
    t = np.linspace(0, flight_time(v0, theta_deg, g), n)
    return position(v0, theta_deg, t, g)


def best_angle_deg() -> float:
    """sin 2θ = 1 となる θ（0° < θ < 90°）"""
    return 45.0
