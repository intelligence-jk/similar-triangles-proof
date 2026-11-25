from fractions import Fraction as F

import pytest

from similarproof import Triangle, missing_side, prove
from similarproof.__main__ import main


def T(names="ABC", **k):
    return Triangle(names, **k)


def test_sss_345_and_678():
    crit, lines = prove(T(a=3, b=4, c=5), T("PQR", a=6, b=8, c=10))
    assert crit == "SSS"
    assert "All three ratios are equal to 2." in lines


def test_sss_fraction_ratio():
    crit, _ = prove(T(a=6, b=8, c=10), T("PQR", a=3, b=4, c=5))
    assert crit == "SSS"


def test_sss_fails_and_no_other_info():
    crit, lines = prove(T(a=3, b=4, c=5), T("PQR", a=6, b=8, c=11))
    assert crit is None and "SSS fails" in " ".join(lines)


def test_aa_with_third_angle_derived():
    crit, lines = prove(T(A=50, B=60), T("PQR", A=50, C=70))
    assert crit == "AA"  # A = P, and B = 60 = Q = 180 - 50 - 70


def test_aa_mismatch():
    crit, lines = prove(T(A=50, B=60), T("PQR", A=50, B=65))
    assert crit is None and any("AA fails" in l for l in lines)


def test_sas():
    # sides b, c meet at A. b/q = 4/8, c/r = 6/12, A = P
    t1 = T(b=4, c=6, A=40)
    t2 = T("PQR", b=8, c=12, A=40)
    assert prove(t1, t2)[0] == "SAS"


def test_sas_wrong_included_angle():
    t1 = T(b=4, c=6, A=40)
    t2 = T("PQR", b=8, c=12, A=41)
    assert prove(t1, t2)[0] is None


def test_missing_side_exact():
    t1c = T(A=50, B=60, a=3, b=4)
    t2c = T("PQR", A=50, B=60, a=F(9, 2))
    assert missing_side(t1c, t2c, 1) == 6  # 4 * (9/2) / 3


def test_missing_side_needs_similarity():
    with pytest.raises(ValueError):
        missing_side(T(a=3, b=4, c=5), T("PQR", a=6, b=8, c=11), 0)


def test_invalid_triangles():
    for bad in (dict(a=1, b=1, c=2), dict(A=100, B=80), dict(A=0), dict(A=60, B=60, C=70), dict(a=-1)):
        with pytest.raises(ValueError):
            Triangle("ABC", **bad)


def test_cli(capsys):
    assert main(["a=3,b=4,c=5", "a=6,b=8,c=10"]) == 0
    assert "(SSS)" in capsys.readouterr().out
    assert main(["A=50,B=60,a=3,b=4", "A=50,B=60,a=9/2", "--find", "b"]) == 0
    assert "Side b of PQR = 6" in capsys.readouterr().out
    assert main(["A=50,B=60", "A=50,B=65"]) == 1
