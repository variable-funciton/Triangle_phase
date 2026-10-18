import math
from utils.monkey import G, Shot, aim_angle_deg, hit_height, v_min

def test_monkey():
    # 狙いどおり・同時なら、v0 > v_min でいつも当たる
    for a in (5, 12, 20, 30):
        for b in (2, 6, 10, 20):
            vm = v_min(a, b)
            for k in (1.01, 1.3, 2, 4):
                s = Shot(a, b, vm * k)
                r = s.result()
                assert r["hit"], (a, b, k, r)
                assert abs(r["y"] - hit_height(a, b, vm * k)) < 1e-9
                assert abs(r["t"] - math.hypot(a, b) / (vm * k)) < 1e-9
                # 当たった瞬間の A と B の位置が一致
                ax, ay = s.pos_a(r["t"]); bx, by = s.pos_b(r["t"])
                assert abs(ax - bx) < 1e-9 and abs(ay - by) < 1e-9
                # 重力なしの位置からのずれは A も B も ½gt²
                gx, gy = s.ghost_a(r["t"] / 2)
                assert abs((gy - s.pos_a(r["t"] / 2)[1]) - (b - s.pos_b(r["t"] / 2)[1])) < 1e-9
            # 初速度が足りないと外れる
            assert not Shot(a, b, vm * 0.8).result()["hit"]
            assert abs(hit_height(a, b, vm)) < 1e-9
    # 例: a=20, b=10 → v_min = √245
    assert abs(v_min(20, 10) - math.sqrt(245)) < 1e-12
    assert abs(aim_angle_deg(1, 1) - 45) < 1e-12
    # 条件を崩すと外れる
    assert not Shot(20, 10, 25, delay=0.3).result()["hit"]
    assert Shot(20, 10, 25, delay=0.3).result()["reason"] == "below"   # B が高い位置に残るので A は下を通る
    assert not Shot(20, 10, 25, offset_deg=5).result()["hit"]
    assert not Shot(20, 10, 25, offset_deg=-5).result()["hit"]
    assert Shot(20, 10, 12).result()["reason"] in ("A_landed", "B_landed")

if __name__ == "__main__":
    test_monkey(); print("test_monkey ok")
