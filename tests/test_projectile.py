import math
import numpy as np
from utils.projectile import G, flight_time, max_height, range_, position, trajectory, velocity

def test_projectile():
    v0 = 20
    assert abs(range_(v0, 45) - v0 ** 2 / G) < 1e-12                 # 45° で v0²/g
    for th in range(1, 90):
        assert range_(v0, th) <= range_(v0, 45) + 1e-12               # 45° が最大
        assert abs(range_(v0, th) - range_(v0, 90 - th)) < 1e-9       # 余角で同じ飛距離
        x, y = position(v0, th, flight_time(v0, th))
        assert abs(float(x) - range_(v0, th)) < 1e-9 and abs(float(y)) < 1e-9
        tm = flight_time(v0, th) / 2
        assert abs(float(position(v0, th, tm)[1]) - max_height(v0, th)) < 1e-9
        assert abs(velocity(v0, th, tm)[1]) < 1e-9                    # 最高点で鉛直速度 0
    x, y = trajectory(v0, 30)
    assert np.all(y >= 0) and abs(x[-1] - range_(v0, 30)) < 1e-9
    # 数値的に最大を探しても 45°
    ths = np.linspace(0.1, 89.9, 8981)
    assert abs(ths[np.argmax([range_(v0, t) for t in ths])] - 45) < 0.02

if __name__ == "__main__":
    test_projectile(); print("test_projectile ok")
