from fractions import Fraction as F
import numpy as np
from utils.angles import pi_text, pi_latex, deg_text, frac_text, pi_ticks
from utils.trig import Wave

def test_angles():
    assert pi_text(F(1,2)) == "π/2"
    assert pi_text(F(-3,2)) == "−3π/2"
    assert pi_text(F(2)) == "2π" and pi_text(F(-1)) == "−π" and pi_text(0) == "0"
    assert pi_latex(F(1,3)) == r"\frac{\pi}{3}"
    assert pi_latex(F(-5,6)) == r"-\frac{5\pi}{6}"
    assert deg_text(F(1,2)) == "90°" and deg_text(F(1,8)) == "22.5°" and deg_text(F(-1,4)) == "−45°"
    assert frac_text(F(-3,2)) == "−3/2"
    vals, labs = pi_ticks(-1, 2, F(1,2))
    assert labs == ["−π","−π/2","0","π/2","π","3π/2","2π"]
    assert np.isclose(vals[0], -np.pi)

def test_wave_values():
    w = Wave("sin", F(2), F(2), F(1,3), F(1))
    x = np.linspace(-3, 9, 50)
    assert np.allclose(w.y(x), 2*np.sin(2*(x-np.pi/3))+1)
    assert w.period == F(1) and w.y_max == 3 and w.y_min == -1
    # キーポイントは実際の関数値と一致
    for xq, yq in w.key_points():
        assert np.isclose(w.y(np.array([float(xq)*np.pi]))[0], float(yq))
    wc = Wave("cos", F(-1,2), F(1,2), F(-1,4), F(0))
    for xq, yq in wc.key_points():
        assert np.isclose(wc.y(np.array([float(xq)*np.pi]))[0], float(yq))
    assert wc.period == 4

def test_latex():
    assert Wave().latex() == r"y = \sin x"
    assert Wave("cos", 2, 1, 0, -1).latex() == r"y = 2\cos x - 1"
    assert Wave("sin", 1, 2, 0, 0).latex() == r"y = \sin 2x"
    assert Wave("sin", -1, 1, F(-1,4), 0).latex() == r"y = -\sin\left(x + \frac{\pi}{4}\right)"
    w = Wave("sin", 2, 2, F(1,6), F(1,2))
    assert w.latex() == r"y = 2\sin 2\left(x - \frac{\pi}{6}\right) + \frac{1}{2}"
    assert w.latex("expanded") == r"y = 2\sin\left(2x - \frac{\pi}{3}\right) + \frac{1}{2}"
    assert Wave("cos", F(3,2), F(1,2), 0, 0).latex() == r"y = \frac{3}{2}\cos \frac{1}{2}x"

def test_decimal_t_and_text():
    import math
    from utils.angles import pi_text, deg_text, pi_latex
    assert pi_text(1.25 / math.pi) == "1.25" and pi_text(-0.5 / math.pi) == "−0.5"
    assert deg_text(0.25) == "45°" and pi_latex(2.5 / math.pi) == "2.5"
    w = Wave("sin", 2, 2, 1.25 / math.pi, 1)
    assert isinstance(w.t, float)
    x = np.linspace(-3, 3, 13)
    assert np.allclose(w.y(x), 2 * np.sin(2 * (x - 1.25)) + 1)
    assert w.text() == "y = 2 sin 2(x − 1.25) + 1" and w.text("expanded") == "y = 2 sin(2x − 2.5) + 1"
    assert w.latex() == r"y = 2\sin 2\left(x - 1.25\right) + 1"
    assert Wave("sin", 2, 2, F(1, 3), 1).text() == "y = 2 sin 2(x − π/3) + 1"
    assert Wave("cos", F(-1, 2), 1, F(-1, 4), F(-3, 2)).text() == "y = −1/2 cos(x + π/4) − 3/2"
    assert Wave().text() == "y = sin x"
    kp = w.key_points()
    assert abs(float(kp[0][0]) * math.pi - 1.25) < 1e-12


if __name__ == "__main__":
    for f in [test_angles, test_wave_values, test_latex, test_decimal_t_and_text]:
        f(); print(f.__name__, "ok")
