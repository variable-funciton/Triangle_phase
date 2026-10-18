import math
import numpy as np
from utils.fourier import WAVES, partial_sum, terms, amplitudes, custom_sum

def test_fourier():
    for key, w in WAVES.items():
        x = np.linspace(-2 * np.pi, 2 * np.pi, 2001)
        if w["discontinuous"]:
            # とぎれる点（矩形波は kπ、のこぎり波は (2k+1)π）から離れたところで比べる
            jumps = np.pi * (np.arange(-3, 4) if key == "square" else np.arange(-3, 4, 2))
            mask = np.min(np.abs(x[:, None] - jumps[None, :]), axis=1) > 0.3
            err = np.max(np.abs(partial_sum(key, x[mask], 400) - w["func"](x[mask])))
            assert err < 0.03, (key, err)
        else:
            err = np.max(np.abs(partial_sum(key, x, 200) - w["func"](x)))
            assert err < 0.01, (key, err)
        # 項が増えるほど誤差が小さくなる（平均二乗誤差）
        e = [np.mean((partial_sum(key, x, N) - w["func"](x)) ** 2) for N in (1, 5, 25)]
        assert e[0] >= e[1] >= e[2], (key, e)
    # 矩形波: 奇数倍だけ、ギブズ現象で約 1.18 まで行き過ぎる
    assert [n for n, _, _ in terms("square", 9)] == [1, 3, 5, 7, 9]
    xs = np.linspace(0.0001, 0.3, 30000)
    peak = partial_sum("square", xs, 199).max()
    assert 1.17 < peak < 1.19, peak
    assert abs(amplitudes("saw", 3)[2] - 2 / 3) < 1e-12
    assert np.allclose(custom_sum([0.5], [1, 0, 1 / 3]), math.sin(0.5) + math.sin(1.5) / 3)

if __name__ == "__main__":
    test_fourier(); print("test_fourier ok")
