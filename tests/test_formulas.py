import math, random
from utils.formulas import FORMULAS, GROUPS, triangle_from_sas
from utils.exact import sin_deg, cos_deg

def test_formulas():
    random.seed(0)
    for f in FORMULAS:
        for _ in range(200):
            a, b = random.uniform(-3, 3), random.uniform(-3, 3)
            try:
                l, r = f["lhs"](a, b), f["rhs"](a, b)
            except ZeroDivisionError:
                continue
            if abs(l) > 1e6 or abs(r) > 1e6:   # tan の発散付近は除く
                continue
            assert abs(l - r) < 1e-7 * max(1, abs(l)), (f["name"], a, b, l, r)
    assert GROUPS[0] == "相互関係" and "和→積" in GROUPS
    t = triangle_from_sas(3, 4, 90)
    assert abs(t["a"] - 5) < 1e-12 and abs(t["S"] - 6) < 1e-12 and abs(t["R"] - 2.5) < 1e-12
    for b, c, A in [(2, 7, 30), (5, 5, 60), (3, 8, 150)]:
        t = triangle_from_sas(b, c, A)
        sA, sB, sC = (math.sin(math.radians(t[k])) for k in "ABC")
        assert abs(t["a"] / sA - 2 * t["R"]) < 1e-9 and abs(t["b"] / sB - 2 * t["R"]) < 1e-9
        assert abs(t["c"] / sC - 2 * t["R"]) < 1e-9 and abs(t["A"] + t["B"] + t["C"] - 180) < 1e-9
    # 有名角の値（厳密値）
    assert sin_deg(30).latex() == r"\frac{1}{2}" and cos_deg(45).latex() == r"\frac{\sqrt{2}}{2}"

if __name__ == "__main__":
    test_formulas(); print("test_formulas ok")
