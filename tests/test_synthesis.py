"""厳密計算・合成・積和和積のテスト（課題8 の数値でも確認）"""
import math
from fractions import Fraction as F
from utils.exact import Q236, sin_deg, cos_deg, sqrt_latex
from utils.synthesis import Synthesis, COEF_OPTIONS

S2, S3 = Q236.sqrt_of(2), Q236.sqrt_of(3)

def test_q236():
    assert S2 * S3 == Q236.sqrt_of(6) and S2 * S2 == 2 and Q236.sqrt_of(6) * S3 == Q236.sqrt_of(2, 3)
    for d in range(0, 360, 15):
        assert abs(float(sin_deg(d)) - math.sin(math.radians(d))) < 1e-12
        assert abs(float(cos_deg(d)) - math.cos(math.radians(d))) < 1e-12
        assert sin_deg(d) * sin_deg(d) + cos_deg(d) * cos_deg(d) == 1
    assert sin_deg(15).latex() == r"\frac{\sqrt{6} - \sqrt{2}}{4}"
    assert sin_deg(75).latex() == r"\frac{\sqrt{6} + \sqrt{2}}{4}"
    assert (1 - S2).latex() == r"1 - \sqrt{2}" and (-1 - S3).latex() == r"-(\sqrt{3} + 1)"
    assert (-1 - S3).text() == "−(√3 + 1)" and ((S3 - 1) / 2).latex() == r"\frac{\sqrt{3} - 1}{2}"
    assert (-S2 / 2).latex() == r"-\frac{\sqrt{2}}{2}"
    assert sin_deg(75).text() == "(√6 + √2)/4" and (-S3 / 2).text() == "−√3/2"
    assert sqrt_latex(F(5)) == r"\sqrt{5}" and sqrt_latex(F(12)) == r"2\sqrt{3}" and sqrt_latex(F(1, 2)) == r"\frac{\sqrt{2}}{2}"

def test_product_sum_kadai8():
    # 第1問: sin37.5° cos7.5° = ½(sin45° + sin30°) = (√2+1)/4
    assert ((sin_deg(45) + sin_deg(30)) / 2).latex() == r"\frac{\sqrt{2} + 1}{4}"
    assert abs(math.sin(math.radians(37.5)) * math.cos(math.radians(7.5)) - (math.sqrt(2) + 1) / 4) < 1e-12
    # 第2問: cos15° cos75° = 1/4（左辺も厳密に計算できる）
    assert cos_deg(15) * cos_deg(75) == F(1, 4)
    # 第4問・第5問
    assert sin_deg(75) + sin_deg(15) == Q236.sqrt_of(6, F(1, 2))
    assert cos_deg(15) - cos_deg(75) == Q236.sqrt_of(2, F(1, 2))
    # 積和の公式は 15° の倍数で厳密に成り立つ
    for A in range(0, 360, 15):
        for B in range(0, 360, 45):
            assert sin_deg(A) * cos_deg(B) == (sin_deg(A + B) + sin_deg(A - B)) / 2
            assert sin_deg(A) * sin_deg(B) == -(cos_deg(A + B) - cos_deg(A - B)) / 2

def test_synthesis_kadai8():
    s = Synthesis(S3, Q236(-1))                      # 第7問
    assert s.R2 == 4 and s.alpha_pi == F(-1, 6)
    assert s.sin_form_latex() == r"2\sin\left(x - \frac{\pi}{6}\right)"
    assert s.cos_form_latex() == r"2\cos\left(x - \frac{2\pi}{3}\right)"
    assert s.lhs_latex() == r"\sqrt{3}\sin x - \cos x"
    s8 = Synthesis(Q236(1), S3)                      # 第8問: 0 ≤ x ≤ π
    e = s8.extrema(F(0), F(1))
    assert e["max"][0] == "2" and e["max"][2] == [r"\frac{\pi}{6}"]
    assert e["min"][0] == r"-\sqrt{3}" and e["min"][2] == [r"\pi"]
    s9 = Synthesis(Q236(1), Q236(-1))                # 第9問
    assert s9.R_latex() == r"\sqrt{2}" and s9.alpha_pi == F(-1, 4)
    s34 = Synthesis(Q236(3), Q236(4))                # きれいでない角
    assert s34.R2 == 25 and s34.alpha_pi is None and s34.alpha_latex() == r"\alpha \approx 53.13^\circ"
    assert s34.cos_form_latex() == r"5\cos\left(x + \beta\right)" and s34.beta_rel() == r"\approx -36.87^\circ"
    assert Synthesis(Q236(-1), Q236(0), "pos").alpha_pi == 1 and Synthesis(Q236(-1), Q236(0), "pm").alpha_pi == 1
    assert Synthesis(Q236(0), Q236(-1), "pos").alpha_pi == F(3, 2)
    # すべての組で R sin(x+α) = R cos(x+β) = a sin x + b cos x
    for a in COEF_OPTIONS:
        for b in COEF_OPTIONS:
            if a.is_zero() and b.is_zero():
                continue
            for mode in ("pm", "pos"):
                s = Synthesis(a, b, mode)
                for x in (0.3, 1.7, -2.2, 5.0):
                    v = s.value(x)
                    assert abs(s.R * math.sin(x + s.alpha) - v) < 1e-9
                    assert abs(s.R * math.cos(x + s.beta) - v) < 1e-9
                e = s.extrema(F(0), F(2), include_hi=False)
                assert abs(e["max"][1] - s.R) < 1e-9 and abs(e["min"][1] + s.R) < 1e-9

if __name__ == "__main__":
    for f in [test_q236, test_product_sum_kadai8, test_synthesis_kadai8]:
        f(); print(f.__name__, "ok")
