"""python -m similarproof "A=50,B=60" "A=50,B=60"   or   "a=3,b=4,c=5" "a=6,b=8,c=10"
Optionally add --find a|b|c to find that side of the second triangle."""
import sys

from .core import Triangle, missing_side, prove, _show


def parse(text):
    d = {}
    for part in text.split(","):
        k, v = part.split("=")
        d[k.strip()] = v.strip()
    return Triangle(**d)


def main(argv=None) -> int:
    a = sys.argv[1:] if argv is None else argv
    find = None
    if "--find" in a:
        i = a.index("--find")
        find, a = a[i + 1], a[:i] + a[i + 2:]
    if len(a) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        t1, t2 = parse(a[0]), parse(a[1])
        t2 = Triangle("PQR", **{k: getattr(t2, k) for k in "abcABC"})
        crit, lines = prove(t1, t2)
        print("\n".join(lines))
        if find is not None:
            print(f"Side {find} of PQR = {_show(missing_side(t1, t2, 'abc'.index(find)))}")
    except (ValueError, TypeError) as e:
        print(f"Cannot do that: {e}", file=sys.stderr)
        return 1
    return 0 if crit else 1


if __name__ == "__main__":
    sys.exit(main())
