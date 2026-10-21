"""三角関数の公式の一覧（表示用の LaTeX と、数値で確かめるための左辺・右辺の関数）。

各公式は dict(group, name, tex, lhs, rhs, vars) で表す。lhs, rhs は角 a, b [rad] の関数。
vars は使う角の数（1 なら α だけ、2 なら α と β）。
"""

from __future__ import annotations

import math

sin, cos, tan = math.sin, math.cos, math.tan

FORMULAS = [
    # ---------- 相互関係 ----------
    dict(group="相互関係", name="tan の定義", vars=1,
         tex=r"\tan\alpha = \frac{\sin\alpha}{\cos\alpha}",
         lhs=lambda a, b: tan(a), rhs=lambda a, b: sin(a) / cos(a)),
    dict(group="相互関係", name="sin² + cos² = 1", vars=1,
         tex=r"\sin^2\alpha + \cos^2\alpha = 1",
         lhs=lambda a, b: sin(a) ** 2 + cos(a) ** 2, rhs=lambda a, b: 1.0),
    dict(group="相互関係", name="1 + tan² = 1/cos²", vars=1,
         tex=r"1 + \tan^2\alpha = \frac{1}{\cos^2\alpha}",
         lhs=lambda a, b: 1 + tan(a) ** 2, rhs=lambda a, b: 1 / cos(a) ** 2),
    # ---------- 加法定理 ----------
    dict(group="加法定理", name="sin(α+β)", vars=2,
         tex=r"\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta",
         lhs=lambda a, b: sin(a + b), rhs=lambda a, b: sin(a) * cos(b) + cos(a) * sin(b)),
    dict(group="加法定理", name="sin(α−β)", vars=2,
         tex=r"\sin(\alpha - \beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta",
         lhs=lambda a, b: sin(a - b), rhs=lambda a, b: sin(a) * cos(b) - cos(a) * sin(b)),
    dict(group="加法定理", name="cos(α+β)", vars=2,
         tex=r"\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta",
         lhs=lambda a, b: cos(a + b), rhs=lambda a, b: cos(a) * cos(b) - sin(a) * sin(b)),
    dict(group="加法定理", name="cos(α−β)", vars=2,
         tex=r"\cos(\alpha - \beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta",
         lhs=lambda a, b: cos(a - b), rhs=lambda a, b: cos(a) * cos(b) + sin(a) * sin(b)),
    dict(group="加法定理", name="tan(α+β)", vars=2,
         tex=r"\tan(\alpha + \beta) = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta}",
         lhs=lambda a, b: tan(a + b), rhs=lambda a, b: (tan(a) + tan(b)) / (1 - tan(a) * tan(b))),
    dict(group="加法定理", name="tan(α−β)", vars=2,
         tex=r"\tan(\alpha - \beta) = \frac{\tan\alpha - \tan\beta}{1 + \tan\alpha\tan\beta}",
         lhs=lambda a, b: tan(a - b), rhs=lambda a, b: (tan(a) - tan(b)) / (1 + tan(a) * tan(b))),
    # ---------- 2倍角・3倍角・半角 ----------
    dict(group="2倍角", name="sin 2α", vars=1,
         tex=r"\sin 2\alpha = 2\sin\alpha\cos\alpha",
         lhs=lambda a, b: sin(2 * a), rhs=lambda a, b: 2 * sin(a) * cos(a)),
    dict(group="2倍角", name="cos 2α", vars=1,
         tex=r"\cos 2\alpha = \cos^2\alpha - \sin^2\alpha = 2\cos^2\alpha - 1 = 1 - 2\sin^2\alpha",
         lhs=lambda a, b: cos(2 * a), rhs=lambda a, b: 1 - 2 * sin(a) ** 2),
    dict(group="2倍角", name="tan 2α", vars=1,
         tex=r"\tan 2\alpha = \frac{2\tan\alpha}{1 - \tan^2\alpha}",
         lhs=lambda a, b: tan(2 * a), rhs=lambda a, b: 2 * tan(a) / (1 - tan(a) ** 2)),
    dict(group="3倍角", name="sin 3α", vars=1,
         tex=r"\sin 3\alpha = 3\sin\alpha - 4\sin^3\alpha",
         lhs=lambda a, b: sin(3 * a), rhs=lambda a, b: 3 * sin(a) - 4 * sin(a) ** 3),
    dict(group="3倍角", name="cos 3α", vars=1,
         tex=r"\cos 3\alpha = 4\cos^3\alpha - 3\cos\alpha",
         lhs=lambda a, b: cos(3 * a), rhs=lambda a, b: 4 * cos(a) ** 3 - 3 * cos(a)),
    dict(group="半角", name="sin²(α/2)", vars=1,
         tex=r"\sin^2\frac{\alpha}{2} = \frac{1 - \cos\alpha}{2}",
         lhs=lambda a, b: sin(a / 2) ** 2, rhs=lambda a, b: (1 - cos(a)) / 2),
    dict(group="半角", name="cos²(α/2)", vars=1,
         tex=r"\cos^2\frac{\alpha}{2} = \frac{1 + \cos\alpha}{2}",
         lhs=lambda a, b: cos(a / 2) ** 2, rhs=lambda a, b: (1 + cos(a)) / 2),
    dict(group="半角", name="tan²(α/2)", vars=1,
         tex=r"\tan^2\frac{\alpha}{2} = \frac{1 - \cos\alpha}{1 + \cos\alpha}",
         lhs=lambda a, b: tan(a / 2) ** 2, rhs=lambda a, b: (1 - cos(a)) / (1 + cos(a))),
    # ---------- 合成 ----------
    dict(group="合成", name="a sin α + b cos α（a = √3, b = 1 の例）", vars=1,
         tex=r"a\sin\alpha + b\cos\alpha = \sqrt{a^2 + b^2}\,\sin(\alpha + \gamma),\quad \cos\gamma = \frac{a}{\sqrt{a^2+b^2}},\ \sin\gamma = \frac{b}{\sqrt{a^2+b^2}}",
         lhs=lambda a, b: math.sqrt(3) * sin(a) + cos(a), rhs=lambda a, b: 2 * sin(a + math.pi / 6)),
    # ---------- 積和 ----------
    dict(group="積→和", name="sin α cos β", vars=2,
         tex=r"\sin\alpha\cos\beta = \frac{1}{2}\{\sin(\alpha+\beta) + \sin(\alpha-\beta)\}",
         lhs=lambda a, b: sin(a) * cos(b), rhs=lambda a, b: (sin(a + b) + sin(a - b)) / 2),
    dict(group="積→和", name="cos α sin β", vars=2,
         tex=r"\cos\alpha\sin\beta = \frac{1}{2}\{\sin(\alpha+\beta) - \sin(\alpha-\beta)\}",
         lhs=lambda a, b: cos(a) * sin(b), rhs=lambda a, b: (sin(a + b) - sin(a - b)) / 2),
    dict(group="積→和", name="cos α cos β", vars=2,
         tex=r"\cos\alpha\cos\beta = \frac{1}{2}\{\cos(\alpha+\beta) + \cos(\alpha-\beta)\}",
         lhs=lambda a, b: cos(a) * cos(b), rhs=lambda a, b: (cos(a + b) + cos(a - b)) / 2),
    dict(group="積→和", name="sin α sin β", vars=2,
         tex=r"\sin\alpha\sin\beta = -\frac{1}{2}\{\cos(\alpha+\beta) - \cos(\alpha-\beta)\}",
         lhs=lambda a, b: sin(a) * sin(b), rhs=lambda a, b: -(cos(a + b) - cos(a - b)) / 2),
    # ---------- 和積 ----------
    dict(group="和→積", name="sin A + sin B", vars=2,
         tex=r"\sin A + \sin B = 2\sin\frac{A+B}{2}\cos\frac{A-B}{2}",
         lhs=lambda a, b: sin(a) + sin(b), rhs=lambda a, b: 2 * sin((a + b) / 2) * cos((a - b) / 2)),
    dict(group="和→積", name="sin A − sin B", vars=2,
         tex=r"\sin A - \sin B = 2\cos\frac{A+B}{2}\sin\frac{A-B}{2}",
         lhs=lambda a, b: sin(a) - sin(b), rhs=lambda a, b: 2 * cos((a + b) / 2) * sin((a - b) / 2)),
    dict(group="和→積", name="cos A + cos B", vars=2,
         tex=r"\cos A + \cos B = 2\cos\frac{A+B}{2}\cos\frac{A-B}{2}",
         lhs=lambda a, b: cos(a) + cos(b), rhs=lambda a, b: 2 * cos((a + b) / 2) * cos((a - b) / 2)),
    dict(group="和→積", name="cos A − cos B", vars=2,
         tex=r"\cos A - \cos B = -2\sin\frac{A+B}{2}\sin\frac{A-B}{2}",
         lhs=lambda a, b: cos(a) - cos(b), rhs=lambda a, b: -2 * sin((a + b) / 2) * sin((a - b) / 2)),
    # ---------- 角の変換 ----------
    dict(group="角の変換", name="−α", vars=1,
         tex=r"\sin(-\alpha) = -\sin\alpha,\quad \cos(-\alpha) = \cos\alpha,\quad \tan(-\alpha) = -\tan\alpha",
         lhs=lambda a, b: sin(-a), rhs=lambda a, b: -sin(a)),
    dict(group="角の変換", name="π − α", vars=1,
         tex=r"\sin(\pi - \alpha) = \sin\alpha,\quad \cos(\pi - \alpha) = -\cos\alpha,\quad \tan(\pi - \alpha) = -\tan\alpha",
         lhs=lambda a, b: cos(math.pi - a), rhs=lambda a, b: -cos(a)),
    dict(group="角の変換", name="π + α", vars=1,
         tex=r"\sin(\pi + \alpha) = -\sin\alpha,\quad \cos(\pi + \alpha) = -\cos\alpha,\quad \tan(\pi + \alpha) = \tan\alpha",
         lhs=lambda a, b: sin(math.pi + a), rhs=lambda a, b: -sin(a)),
    dict(group="角の変換", name="π/2 − α", vars=1,
         tex=r"\sin\left(\frac{\pi}{2} - \alpha\right) = \cos\alpha,\quad \cos\left(\frac{\pi}{2} - \alpha\right) = \sin\alpha,\quad \tan\left(\frac{\pi}{2} - \alpha\right) = \frac{1}{\tan\alpha}",
         lhs=lambda a, b: sin(math.pi / 2 - a), rhs=lambda a, b: cos(a)),
    dict(group="角の変換", name="π/2 + α", vars=1,
         tex=r"\sin\left(\frac{\pi}{2} + \alpha\right) = \cos\alpha,\quad \cos\left(\frac{\pi}{2} + \alpha\right) = -\sin\alpha,\quad \tan\left(\frac{\pi}{2} + \alpha\right) = -\frac{1}{\tan\alpha}",
         lhs=lambda a, b: cos(math.pi / 2 + a), rhs=lambda a, b: -sin(a)),
    dict(group="角の変換", name="α + 2nπ", vars=1,
         tex=r"\sin(\alpha + 2n\pi) = \sin\alpha,\quad \cos(\alpha + 2n\pi) = \cos\alpha,\quad \tan(\alpha + n\pi) = \tan\alpha",
         lhs=lambda a, b: sin(a + 4 * math.pi), rhs=lambda a, b: sin(a)),
]

GROUPS = list(dict.fromkeys(f["group"] for f in FORMULAS))


# ---------------- 三角形 ----------------
def triangle_from_sas(b: float, c: float, A_deg: float):
    """2 辺 b, c とその間の角 A から、残りを求める（余弦定理・正弦定理）"""
    A = math.radians(A_deg)
    a = math.sqrt(b * b + c * c - 2 * b * c * math.cos(A))
    cosB = (a * a + c * c - b * b) / (2 * a * c)
    B = math.degrees(math.acos(max(-1.0, min(1.0, cosB))))
    C = 180 - A_deg - B
    R = a / (2 * math.sin(A))
    S = 0.5 * b * c * math.sin(A)
    return dict(a=a, b=b, c=c, A=A_deg, B=B, C=C, R=R, S=S)
