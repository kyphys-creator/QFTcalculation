"""Compare the vertex particle content of two UFO models (vertices.py)."""
import collections, re, sys

def load(path):
    out = collections.Counter()
    for v in re.findall(r"particles = \[([^\]]*)\]", open(path).read()):
        out[tuple(sorted(x.strip().replace("P.", "") for x in v.split(",")))] += 1
    return out

a, b = load(sys.argv[1]), load(sys.argv[2])
print(f"vertices: {sum(a.values())} (FeynRules) vs {sum(b.values())} (MG5 sm)")
print("missing from FeynRules output:", sorted(set(b) - set(a)))
print("only in FeynRules output:", sorted(set(a) - set(b)))
