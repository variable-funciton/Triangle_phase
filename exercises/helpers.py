"""演習の問題づくりで共通に使う道具(三角関数用)"""
from fractions import Fraction as F

from exercises.core import Choice, Retry, tex_fr, tex_root
from utils.angles import pi_latex
from utils.exact import Q236, cos_deg, sin_deg, tan_deg

NICE_DEG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def pi_tex(q):
    """π の何倍か(Fraction)→ \\frac{5\\pi}{6} など"""
    return pi_latex(F(q))


def deg_to_pi(deg):
    return F(deg, 180)


def trig_tex(fn, deg):
    """有名角の sin / cos / tan の値の LaTeX(tan が定義されないときは None)"""
    if fn == "sin":
        return sin_deg(deg).latex()
    if fn == "cos":
        return cos_deg(deg).latex()
    t = tan_deg(deg)
    return None if t is None else t.latex()


def trig_val(fn, deg):
    if fn == "sin":
        return sin_deg(deg)
    if fn == "cos":
        return cos_deg(deg)
    return tan_deg(deg)


def neg_tex(t):
    """LaTeX の値の符号を反対に"""
    if t == "0":
        return "0"
    if t.startswith("-"):
        return t[1:]
    if " + " in t or " - " in t:
        return "-(" + t + ")"
    return "-" + t


def assemble(correct, wrongs, fillers=(), value=None):
    """正解 1 つと誤答(tex, why)から、重ならない 4 つの選択肢を作る。足りなければ fillers から補う"""
    out = [Choice(correct, True, value=value)]
    seen = {correct}
    for t, why in list(wrongs) + list(fillers):
        if t is None or t in seen:
            continue
        out.append(Choice(t, why=why))
        seen.add(t)
        if len(out) == 4:
            return out
    raise Retry


def q236_from_float_guess(x):
    """(テスト用)Q236 を float に"""
    return float(x)


def frac_or_root(num, den, root=1):
    """num·√root / den を簡単にした LaTeX"""
    from exercises.core import tex_frac_root
    return tex_frac_root(num, den, root)


__all__ = ["F", "Choice", "Retry", "tex_fr", "tex_root", "pi_tex", "deg_to_pi", "trig_tex", "trig_val", "neg_tex",
           "assemble", "frac_or_root", "NICE_DEG", "Q236", "sin_deg", "cos_deg", "tan_deg"]
