"""Similar triangles: which test applies, and the proof lines.

Triangle ABC has sides a = BC, b = CA, c = AB (each opposite its vertex) and angles A, B, C.
Triangle PQR is matched to it in order: A to P, B to Q, C to R. Give what is known;
anything left out is None. Angles are in degrees.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from typing import Optional


def _f(x):
    return None if x is None else F(x)


@dataclass(frozen=True)
class Triangle:
    names: str = "ABC"
    a: Optional[F] = None
    b: Optional[F] = None
    c: Optional[F] = None
    A: Optional[F] = None
    B: Optional[F] = None
    C: Optional[F] = None

    def __post_init__(self):
        for k in "abcABC":
            object.__setattr__(self, k, _f(getattr(self, k)))
        for k in "abc":
            v = getattr(self, k)
            if v is not None and v <= 0:
                raise ValueError("a side must be positive")
        angles = [x for x in (self.A, self.B, self.C) if x is not None]
        if any(x <= 0 or x >= 180 for x in angles):
            raise ValueError("an angle must be between 0 and 180 degrees")
        if len(angles) == 3 and sum(angles) != 180:
            raise ValueError("the angles must add to 180")
        if len(angles) == 2 and sum(angles) >= 180:
            raise ValueError("two angles must add to less than 180")
        s = [x for x in (self.a, self.b, self.c)]
        if all(x is not None for x in s):
            x, y, z = sorted(s)
            if x + y <= z:
                raise ValueError("these sides do not make a triangle")

    def angle(self, i):
        """Angle i (0, 1, 2), computed from the other two if only they are known."""
        v = (self.A, self.B, self.C)[i]
        if v is not None:
            return v
        others = [x for j, x in enumerate((self.A, self.B, self.C)) if j != i]
        if all(x is not None for x in others):
            return 180 - sum(others)
        return None

    def side(self, i):
        return (self.a, self.b, self.c)[i]


def _show(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def prove(t1: Triangle, t2: Triangle):
    """Return (criterion or None, list of proof lines) for t1 ~ t2 with A-P, B-Q, C-R."""
    n1, n2 = t1.names, t2.names
    lines = [f"To show: triangle {n1} is similar to triangle {n2} with {n1[0]}{n1[1]}{n1[2]} matched to {n2[0]}{n2[1]}{n2[2]}."]

    # AA
    ang = [(i, t1.angle(i), t2.angle(i)) for i in range(3)]
    known = [(i, x, y) for i, x, y in ang if x is not None and y is not None]
    if len(known) >= 2:
        if all(x == y for _, x, y in known):
            for i, x, y in known[:2]:
                lines.append(f"Angle {n1[i]} = {_show(x)} and angle {n2[i]} = {_show(y)}, so angle {n1[i]} = angle {n2[i]}.")
            lines.append("Two angles of one triangle equal two angles of the other, so the third angles are equal too.")
            lines.append(f"Hence triangle {n1} is similar to triangle {n2} (AA).")
            return "AA", lines
        i, x, y = next((i, x, y) for i, x, y in known if x != y)
        lines.append(f"Angle {n1[i]} = {_show(x)} but angle {n2[i]} = {_show(y)}: not equal, so AA fails.")

    # SSS
    sides = [(i, t1.side(i), t2.side(i)) for i in range(3)]
    if all(x is not None and y is not None for _, x, y in sides):
        ratios = [y / x for _, x, y in sides]
        names = [f"{n2[(i + 1) % 3]}{n2[(i + 2) % 3]}/{n1[(i + 1) % 3]}{n1[(i + 2) % 3]}" for i in range(3)]
        for nm, (i, x, y), r in zip(names, sides, ratios):
            lines.append(f"{nm} = {_show(y)}/{_show(x)} = {_show(r)}")
        if len(set(ratios)) == 1:
            lines.append(f"All three ratios are equal to {_show(ratios[0])}.")
            lines.append(f"Hence triangle {n1} is similar to triangle {n2} (SSS).")
            return "SSS", lines
        lines.append("The three ratios are not all equal, so SSS fails.")

    # SAS: two sides in proportion and the angle between them equal
    for i in range(3):
        j, k = (i + 1) % 3, (i + 2) % 3  # sides j and k meet at vertex i
        s1j, s2j, s1k, s2k = t1.side(j), t2.side(j), t1.side(k), t2.side(k)
        if None in (s1j, s2j, s1k, s2k):
            continue
        a1, a2 = t1.angle(i), t2.angle(i)
        if a1 is None or a2 is None:
            continue
        rj, rk = s2j / s1j, s2k / s1k
        lines.append(
            f"Sides around {n1[i]}: {_show(s2j)}/{_show(s1j)} = {_show(rj)} and {_show(s2k)}/{_show(s1k)} = {_show(rk)}."
        )
        if rj == rk and a1 == a2:
            lines.append(f"The ratios are equal and the angle between them is the same ({_show(a1)} degrees).")
            lines.append(f"Hence triangle {n1} is similar to triangle {n2} (SAS).")
            return "SAS", lines
        lines.append("SAS fails here (ratios differ or the included angles differ).")
        break

    lines.append("The given facts do not show similarity.")
    return None, lines


def missing_side(t1: Triangle, t2: Triangle, side_index: int):
    """If the triangles are similar, find side `side_index` (0=a, 1=b, 2=c) of t2 from t1.

    Uses any other pair of corresponding sides known in both triangles. Returns a Fraction.
    """
    crit, _ = prove(t1, t2)
    if crit is None:
        raise ValueError("the triangles are not shown to be similar")
    known1 = t1.side(side_index)
    if known1 is None:
        raise ValueError("side is unknown in the first triangle")
    for i in range(3):
        if i != side_index and t1.side(i) is not None and t2.side(i) is not None:
            return known1 * t2.side(i) / t1.side(i)
    raise ValueError("no pair of corresponding sides is known in both triangles")
