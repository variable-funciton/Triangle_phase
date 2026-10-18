"""モンキーハンティング（空気抵抗なし）の計算。

原点 O から物体 A を点 (a, b) に向けて初速度 v0 で投げ、同時に (a, b) から物体 B を自由落下させる。
    A: x = v0 cosθ · t,  y = v0 sinθ · t − g t²/2      （tanθ = b/a）
    B: x = a,            y = b − g (t − τ)²/2          （τ: B を放すのが遅れる時間。通常は 0）
A が x = a に達する時刻 t* = a / (v0 cosθ)。狙いどおり（θ = 狙いの角）なら t* = √(a² + b²)/v0 で、
そのとき A と B の高さはどちらも b − g t*²/2 になる。
B が地面に着く前（t* < √(2b/g)）にぶつかる条件は  v0 > √( g(a² + b²) / (2b) )。
"""

from __future__ import annotations

import math
from dataclasses import dataclass

G = 9.8
HIT_RADIUS = 0.3   # A と B の高さの差がこれ以下なら「当たり」とみなす [m]


def aim_angle_deg(a: float, b: float) -> float:
    return math.degrees(math.atan2(b, a))


def v_min(a: float, b: float, g: float = G) -> float:
    """B が地面に着く前にぶつかるための最小の初速度"""
    return math.sqrt(g * (a * a + b * b) / (2 * b))


def hit_height(a: float, b: float, v0: float, g: float = G) -> float:
    """狙いどおり・同時に放したときの、ぶつかる高さ（負なら地面より下＝実際には外れ）"""
    t = math.hypot(a, b) / v0
    return b - 0.5 * g * t * t


@dataclass
class Shot:
    a: float
    b: float
    v0: float
    offset_deg: float = 0.0   # 狙いからのずれ（上向きが正）
    delay: float = 0.0        # B を放すのが遅れる時間 [s]
    g: float = G

    @property
    def theta_deg(self) -> float:
        return aim_angle_deg(self.a, self.b) + self.offset_deg

    @property
    def theta(self) -> float:
        return math.radians(self.theta_deg)

    # ---- 位置 ----
    def a_landing_time(self) -> float:
        return max(2 * self.v0 * math.sin(self.theta) / self.g, 0.0)

    def b_landing_time(self) -> float:
        return self.delay + math.sqrt(2 * self.b / self.g)

    def pos_a(self, t: float):
        t = min(max(t, 0.0), self.a_landing_time())
        x = self.v0 * math.cos(self.theta) * t
        y = self.v0 * math.sin(self.theta) * t - 0.5 * self.g * t * t
        return x, max(y, 0.0)

    def ghost_a(self, t: float):
        """重力がなかったときの A の位置（狙いの直線上）"""
        return self.v0 * math.cos(self.theta) * t, self.v0 * math.sin(self.theta) * t

    def pos_b(self, t: float):
        s = min(max(t - self.delay, 0.0), math.sqrt(2 * self.b / self.g))
        return self.a, max(self.b - 0.5 * self.g * s * s, 0.0)

    def fall(self, t: float) -> float:
        """½ g t²"""
        return 0.5 * self.g * t * t

    # ---- 判定 ----
    def t_reach(self) -> float:
        """A が x = a に達する時刻"""
        return self.a / (self.v0 * math.cos(self.theta))

    def result(self) -> dict:
        tc = self.t_reach()
        ta, tb = self.a_landing_time(), self.b_landing_time()
        if ta < tc - 1e-12:
            return dict(hit=False, reason="A_landed", t=ta, x=self.pos_a(ta)[0], y=0.0, gap=None)
        ya = self.v0 * math.sin(self.theta) * tc - 0.5 * self.g * tc * tc
        yb = self.pos_b(tc)[1]
        if tb < tc - 1e-12 and abs(ya - yb) > HIT_RADIUS:
            return dict(hit=False, reason="B_landed", t=tc, x=self.a, y=ya, gap=ya - yb)
        gap = ya - yb
        if abs(gap) <= HIT_RADIUS and ya >= -1e-9:
            return dict(hit=True, reason="hit", t=tc, x=self.a, y=max(ya, 0.0), gap=gap)
        return dict(hit=False, reason="above" if gap > 0 else "below", t=tc, x=self.a, y=ya, gap=gap)

    def end_time(self) -> float:
        """アニメーションを止める時刻"""
        r = self.result()
        if r["hit"]:
            return r["t"]
        return max(self.a_landing_time(), self.b_landing_time(), r["t"]) if r["reason"] != "A_landed" \
            else max(self.a_landing_time(), self.b_landing_time())
