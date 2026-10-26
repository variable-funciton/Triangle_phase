"""演習の問題生成のテスト:  python -m tests.test_exercises

すべての型について、たくさんのセット番号で問題を作り、
  - 選択肢が 4 つで重ならず、正解がちょうど 1 つ
  - 正解の値が、独立に計算した値と一致する(meta を使って確かめられる型)
  - LaTeX 一式・印刷用 HTML が作れる
ことを確かめる。streamlit がなくても動くように、最小限の代わりを入れる。
"""
import math
import sys
import types
from fractions import Fraction as F

if "streamlit" not in sys.modules:
    st = types.ModuleType("streamlit")
    st.cache_data = lambda *a, **k: (a[0] if a and callable(a[0]) else (lambda f: f))
    sys.modules["streamlit"] = st

from exercises import addition, advanced, applied, basics, graph, physics, transform  # noqa: E402
from exercises.core import build, latex_files, rng_for, student_html, student_tex  # noqa: E402

MODULES = [basics, graph, transform, addition, physics, applied, advanced]
N = 150


def correct(p):
    return [c for c in p.choices if c.correct][0]


def near(a, b, tol=1e-9):
    assert abs(a - b) < tol, (a, b)


def check_values(t, p):
    m, v = p.meta, correct(p).value
    k = t.key
    if k == "value" or k == "value_ext":
        fn = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[m["fn"]]
        near(v, fn(math.radians(m["deg"])), 1e-9)
    elif k == "deg2rad":
        near(v, m["deg"] / 180)
    elif k == "addition" and t.name.startswith("加法"):
        near(v, (math.sin if m["fn"] == "sin" else math.cos)(math.radians(m["deg"])))
    elif k == "synth":
        (a, ra), (b, rb), al = m["a"], m["b"], m["al"]
        A, B = a * math.sqrt(ra), b * math.sqrt(rb)
        R = math.hypot(A, B)
        for x in (0.3, 1.1, 2.5):
            near(A * math.sin(x) + B * math.cos(x), R * math.sin(x + math.radians(al)), 1e-9)
    elif k == "range":
        near(v, m["v0"] ** 2 * math.sin(math.radians(2 * m["th"])) / 9.8, 1e-9)
    elif k == "time":
        near(v, 2 * m["v0"] * math.sin(math.radians(m["th"])) / 9.8, 1e-9)
    elif k == "height":
        near(v, (m["v0"] * math.sin(math.radians(m["th"]))) ** 2 / (2 * 9.8), 1e-9)
    elif k == "shm":
        near(v, 2 * math.pi * math.sqrt(m["m"] / m["k"]), 1e-9)
    elif k == "ferris":
        near(v, m["r"] + m["a"] - m["r"] * math.cos(2 * math.pi * (m["T"] * m["k"] / 12) / m["T"]), 1e-9)
    elif k == "power":
        near(v, m["V"] * m["I"] * math.cos(math.radians(m["ph"])), 1e-9)
    elif k == "shadow":
        near(v, m["H"] / math.tan(math.radians(m["h"])), 1e-9)
    elif k == "survey":
        near(v, m["d"] * math.tan(math.radians(m["th"])) + m["e"], 1e-9)
    elif k == "slope" and t.name == "接線の傾き":
        fn = math.cos if m["fn"] == "sin" else (lambda x: -math.sin(x))
        near(v, fn(math.radians(m["deg"])), 1e-9)
    elif k in ("add_value", "add_value2"):
        fn = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[m["fn"]]
        near(v, fn(math.radians(m["deg"])), 1e-9)
    elif k == "add_from":
        sa, ca, sb, cb = (float(F(m[x])) for x in ("sa", "ca", "sb", "cb"))
        near(sa * sa + ca * ca, 1); near(sb * sb + cb * cb, 1)
        al, be = math.atan2(sa, ca), math.atan2(sb, cb)
        ang = al + be if m["op"] == "+" else al - be
        near(v, (math.sin if m["fn"] == "sin" else math.cos)(ang), 1e-9)
    elif k == "sph_xyz":
        r, th, ph = m["r"], math.radians(m["th"]), math.radians(m["ph"])
        near(v, {"x": r * math.sin(th) * math.cos(ph), "y": r * math.sin(th) * math.sin(ph), "z": r * math.cos(th)}[m["comp"]], 1e-9)
    elif k == "lat_circle":
        near(v, 2 * math.pi * 6400 * math.cos(math.radians(m["lat"])), 1e-6)
    elif k == "gc_dist":
        near(v, 6400 * math.radians(m["d"]), 1e-6)
        assert 0 < m["d"] <= 180
    elif k == "girard":
        near(v, math.radians(sum(m["angs"])) - math.pi, 1e-9)
        assert v > 0
    elif k == "sph_cos":
        a, b, g = (math.radians(m[x]) for x in ("a", "b", "g"))
        near(v, math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b) * math.cos(g), 1e-9)
    elif k == "compose":
        pass  # 下の個別テストで確かめる


def test_all_types():
    count = 0
    for mod in MODULES:
        names = [t.name for t in mod.REGISTRY]
        assert len(names) == len(set(names)), mod.__name__
        assert mod.TITLE
        for t in mod.REGISTRY:
            assert t.level in ("基本", "標準"), t.name
            for s in range(N):
                p = build(t, rng_for(s, 0, 0, t.key))
                texs = [c.tex for c in p.choices]
                assert len(texs) == 4 and len(set(texs)) == 4, (t.name, texs)
                assert sum(c.correct for c in p.choices) == 1
                assert all(c.why for c in p.choices if not c.correct), (t.name, [c.tex for c in p.choices if not c.why])
                assert p.hints and p.solution and p.statement
                assert "**" not in p.statement
                check_values(t, p)
                count += 1
    print(f"  {count} 問を生成して確認")


def test_equation_solutions():
    """三角方程式の正解の x を代入すると、方程式をみたす"""
    import re
    vals = {"0": 0, r"\frac{1}{2}": .5, r"\frac{\sqrt{2}}{2}": math.sqrt(2) / 2, r"\frac{\sqrt{3}}{2}": math.sqrt(3) / 2, "1": 1,
            r"\sqrt{3}": math.sqrt(3), r"\frac{1}{\sqrt{3}}": 1 / math.sqrt(3)}
    t = [t for t in graph.REGISTRY if t.key == "equation"][0]
    for s in range(200):
        p = build(t, rng_for(s, 0, 0, t.key))
        fn = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[p.meta["fn"]]
        kt = p.meta["k"]
        k = -vals[kt[1:]] if kt.startswith("-") else vals[kt]
        sols = correct(p).tex[2:].split(r",\ ")
        for st_ in sols:
            mm = re.fullmatch(r"(-?)(?:\\frac\{(\d*)\\pi\}\{(\d+)\}|(\d*)\\pi|0)", st_)
            assert mm, st_
            if st_ == "0":
                x = 0
            elif mm.group(3):
                x = (int(mm.group(2) or 1) / int(mm.group(3))) * math.pi
            else:
                x = int(mm.group(4) or 1) * math.pi
            near(fn(x), k, 1e-9)
            assert 0 <= x < 2 * math.pi


def test_addition_both_units():
    """加法定理の値の問題は、度数法と弧度法の両方が出る"""
    for mod, key in [(addition, "add_value"), (addition, "add_value2"), (basics, "addition")]:
        t = [t for t in mod.REGISTRY if t.key == key][0]
        sts = [build(t, rng_for(s, 0, 0, key)).statement for s in range(60)]
        assert any(r"\pi" in x for x in sts) and any(r"^\circ" in x for x in sts), key


def test_div_q3():
    from exercises.addition import div_q3
    from utils.exact import Q236
    x = div_q3(Q236(1, 0, 1, 0), Q236(1, 0, -1, 0))      # (1+√3)/(1−√3) = −2 − √3
    near(float(x), (1 + math.sqrt(3)) / (1 - math.sqrt(3)))
    assert x == Q236(-2, 0, -1, 0)


def test_compose_values():
    from exercises.transform import f_exact, g_exact
    assert f_exact(F(1, 4)) == F(1, 2) and f_exact(F(3, 4)) == F(1, 2) and f_exact(F(2)) == 0
    assert g_exact(F(1, 2)) == 1 and g_exact(F(5, 6)) == F(1, 2) and g_exact(F(1)) == 0


def test_latex_and_html():
    for mod in MODULES:
        probs = [build(t, rng_for(3, i, 0, t.key)) for i, t in enumerate(mod.REGISTRY)]
        files = latex_files(probs, mod.TITLE, 3)
        assert set(files) == {"数学IB演習.tex", "数学IB演習-Ans.tex", "problems.tex", "answers.tex"}
        assert r"\input{problems.tex}" in files["数学IB演習.tex"]
        assert files["problems.tex"].count(r"\item") == len(probs)
        assert "解答・解説" in files["answers.tex"]
        tex = student_tex(probs, mod.TITLE, 3)
        assert tex.count(r"\begin{document}") == 1
        assert "数学IB" in student_html(probs, mod.TITLE, 3)
    # 図のある問題は TikZ が入る
    t = [t for t in graph.REGISTRY if t.key == "graph"][0]
    p = build(t, rng_for(1, 0, 0, t.key))
    assert r"\begin{tikzpicture}" in latex_files([p], "x", 1)["problems.tex"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("exercises: all tests passed")
