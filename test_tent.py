from fractions import Fraction as F
import numpy as np
from utils.tent import (tent, trapezoid, transformed, transformed_vertices, compose, iterate_fn,
                        iterate_vertices, orbit, dense_grid)

def at(fn, xs):
    return list(np.round(fn(np.array(xs, dtype=float)), 12))

def test_tent():
    assert at(tent, [-1, 0, 0.25, 0.5, 0.75, 1, 2]) == [0, 0, 0.5, 1, 0.5, 0, 0]
    assert at(trapezoid, [0, 1/6, 0.5, 5/6, 1]) == [0, 0.5, 1, 0.5, 0]
    # 課題5 第8問: y = 2f(x−1) は (1,0)-(1.5,2)-(2,0)
    h = lambda x: transformed(x, 2, 1, 1, 0)
    assert at(h, [1, 1.5, 2, 0.5]) == [0, 2, 0, 0]
    assert transformed_vertices(2, 1, 1, 0) == [(1, 0), (1.5, 2), (2, 0)]
    # 課題5 第9問: f(g(x)) は (0,0)-(1/6,1)-(1/3,0)-(2/3,0)-(5/6,1)-(1,0)
    fg = compose(tent, trapezoid)
    assert at(fg, [0, 1/6, 1/3, 0.5, 2/3 - 1e-9, 5/6, 1]) == [0, 1, 0, 0, 0, 1, 0]
    # 課題5 第10問: g(f(x)) は (0,0)-(1/6,1)-(1/3,1)-(1/2,0)-(2/3,1)-(5/6,1)-(1,0)
    gf = compose(trapezoid, tent)
    assert at(gf, [0, 1/6, 0.25, 1/3, 0.5, 2/3, 0.75, 5/6, 1]) == [0, 1, 1, 1, 0, 1, 1, 1, 0]
    # f の n 回合成は x = k/2^n で 0 と 1 が交互
    for n in range(1, 7):
        fn = iterate_fn(n)
        for xq, v in iterate_vertices(n):
            assert abs(float(fn(np.array([float(xq)]))[0]) - v) < 1e-9
    # 分数での軌道（漸化式）
    assert orbit(F(1, 3), 3) == [F(1, 3), F(2, 3), F(2, 3), F(2, 3)]       # 不動点 2/3
    assert orbit(F(1, 5), 4) == [F(1, 5), F(2, 5), F(4, 5), F(2, 5), F(4, 5)]  # 周期 2
    assert orbit(F(1, 8), 4)[-1] == 0
    g = dense_grid(0, 1)
    assert 1/3 in g or np.isclose(g, 1/3).any()

if __name__ == "__main__":
    test_tent(); print("test_tent ok")
