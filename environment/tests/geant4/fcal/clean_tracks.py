"""Copy the track files of lAr_calorimeter (event number, x, y, z in cm, cosX, cosY, cosZ) without the lines that have a
non-finite number or a direction whose length is not 1 (run_fcal.sh).  Usage: clean_tracks.py <data-tracks> <copy>"""
import math
import os
import sys

src, dst = sys.argv[1:3]
os.makedirs(dst, exist_ok=True)
for name in sorted(os.listdir(src)):
    t = open(os.path.join(src, name)).read().split()
    rows = [t[i:i + 7] for i in range(0, len(t) - len(t) % 7, 7)]
    good = []
    for r in rows:
        v = [float(x) for x in r[1:]]
        if all(math.isfinite(x) for x in v) and abs(math.hypot(*v[3:]) - 1) < 1e-6:
            good.append(r)
        else:
            print(f"{name}: dropped line {r[0]}: {' '.join(r[1:])}")
    with open(os.path.join(dst, name), "w") as f:
        for i, r in enumerate(good, 1):
            f.write(f"{i} {' '.join(r[1:])}\n")
    print(f"{name}: {len(good)} of {len(rows)} lines kept")
