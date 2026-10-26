"""球面三角形のページの「発展」の表にのせた公式を、ランダムな球面三角形で数値的に確かめる。

python -m tests.test_spherical
"""
import math
import random


def unit(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def dot(p, q):
    return sum(a * b for a, b in zip(p, q))


def cross(p, q):
    return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])


def norm(p):
    return math.sqrt(dot(p, p))


def arc(p, q):
    return math.atan2(norm(cross(p, q)), dot(p, q))


def angle(p, q, r):
    """頂点 p で q, r へ向かう大円のなす角"""
    def tan_(p, q):
        d = dot(p, q)
        v = tuple(b - d * a for a, b in zip(p, q))
        n = norm(v)
        return tuple(x / n for x in v)
    u, w = tan_(p, q), tan_(p, r)
    return math.atan2(norm(cross(u, w)), dot(u, w))


def triangles(n=500, seed=1):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        V = [unit(math.degrees(math.asin(2 * rng.random() - 1)), rng.uniform(-180, 180)) for _ in range(3)]
        A, B, C = V
        a, b, c = arc(B, C), arc(C, A), arc(A, B)
        if min(a, b, c) < 0.05 or abs(dot(A, cross(B, C))) < 1e-3:
            continue
        out.append((a, b, c, angle(A, B, C), angle(B, C, A), angle(C, A, B)))
    return out


def close(x, y, eps=1e-8):
    assert abs(x - y) < eps, (x, y)


def test_formulas():
    for a, b, c, al, be, ga in triangles():
        s = (a + b + c) / 2
        # 余弦法則
        close(math.cos(a), math.cos(b) * math.cos(c) + math.sin(b) * math.sin(c) * math.cos(al))
        close(math.cos(c), math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b) * math.cos(ga))
        # 正弦法則
        close(math.sin(al) / math.sin(a), math.sin(be) / math.sin(b))
        close(math.sin(al) / math.sin(a), math.sin(ga) / math.sin(c))
        # 正接法則
        if abs(math.tan((a + b) / 2)) > 1e-3 and abs(math.tan((al + be) / 2)) > 1e-3:
            close(math.tan((al - be) / 2) / math.tan((al + be) / 2), math.tan((a - b) / 2) / math.tan((a + b) / 2), 1e-6)
        # 半角公式
        close(math.tan(al / 2), math.sqrt(math.sin(s - b) * math.sin(s - c) / (math.sin(s) * math.sin(s - a))), 1e-6)
        # ドランブル（ガウス）の公式
        close(math.sin((al + be) / 2) / math.cos(ga / 2), math.cos((a - b) / 2) / math.cos(c / 2), 1e-7)
        close(math.cos((al + be) / 2) / math.sin(ga / 2), math.cos((a + b) / 2) / math.cos(c / 2), 1e-7)
        # ジラール = リュイリエ
        E = al + be + ga - math.pi
        t = math.tan(s / 2) * math.tan((s - a) / 2) * math.tan((s - b) / 2) * math.tan((s - c) / 2)
        close(math.tan(E / 4), math.sqrt(t), 1e-7)


def test_pole_distance():
    """北極を C とした成分計算：AB の弦の 2 乗 = 2 − 2(cos a cos b + sin a sin b cos γ)"""
    rng = random.Random(3)
    for _ in range(200):
        a, b, g = rng.uniform(0.1, 3), rng.uniform(0.1, 3), rng.uniform(0, 2 * math.pi)
        A = (math.sin(b), 0, math.cos(b))
        B = (math.sin(a) * math.cos(g), math.sin(a) * math.sin(g), math.cos(a))
        chord2 = sum((x - y) ** 2 for x, y in zip(A, B))
        close(chord2, 2 - 2 * (math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b) * math.cos(g)))
        close(chord2, 2 - 2 * math.cos(arc(A, B)))


if __name__ == "__main__":
    test_formulas()
    test_pole_distance()
    print("spherical formulas: ok")
