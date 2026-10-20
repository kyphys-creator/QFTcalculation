"""Checks of Geant4 11.4.3 (environment.pdf): own runs of the distributed examples against the reference outputs that
come with them, and against the data files and known values.  Called by run_geant4.sh:

  test_geant4.py table <label> <mine> <ref> <start>   every number from the line containing <start> on (no random numbers)
  test_geant4.py b1 <ref> <mine> [<mine> ...]          the dose of each run, within the statistical errors
  test_geant4.py rdecay01 <mine> <ref>                 the particle counts of each run; Co60 against ENSDF
  test_geant4.py thermal <hp.out> <nohp.out>           neutron capture at 0.0253 eV: G4NDL file, Atlas of Neutron Resonances
  test_geant4.py tendl <allhp.out> <nohp.out>          p + Al inelastic: the G4TENDL file below 20 MeV, the same list above
"""
import difflib
import math
import os
import re
import sys
import zlib

DATA = os.path.expanduser("~/hep/geant4-11.4.3/share/Geant4/data")
NUM = re.compile(r"^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$")
# timing, memory pools, thread banners: they change from run to run
VOLATILE = ("User=", "Real=", "memory pool", "pools deleted", "Total memory freed", "Number of memory pools")


def isnum(t):
    return bool(NUM.match(t))


def lines_from(path, start):
    lines = open(path, errors="replace").read().splitlines()
    i = next((k for k, l in enumerate(lines) if start in l), None)
    if i is None:
        sys.exit(f"'{start}' not found in {path}")
    return [l for l in lines[i:] if l.strip() and not any(v in l for v in VOLATILE)]


def table(label, mine, ref, start):
    """Align the two outputs line by line on their text (numbers masked), then compare every number."""
    a, b = lines_from(mine, start), lines_from(ref, start)
    shape = lambda l: " ".join("#" if isnum(t) else t for t in l.replace(";", " ").split())
    sm = difflib.SequenceMatcher(None, [shape(x) for x in a], [shape(x) for x in b], autojunk=False)
    n = same = 0
    worst = (0.0, "", "")
    only_a, only_b = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            only_a += a[i1:i2]
            only_b += b[j1:j2]
            continue
        for x, y in zip(a[i1:i2], b[j1:j2]):
            for s, t in zip(x.replace(";", " ").split(), y.replace(";", " ").split()):
                if not isnum(s):
                    continue
                n += 1
                u, v = float(s), float(t)
                same += s == t
                d = 0.0 if u == v else abs(u - v) / max(abs(u), abs(v))
                if d > worst[0]:
                    worst = (d, x.strip(), y.strip())
    print(f"{label}: {len(a)} lines, {n} numbers, {same} identical to the reference; "
          f"largest relative difference {worst[0]:.1e}")
    if worst[0] > 0:
        print(f"    mine: {worst[1]}\n    ref : {worst[2]}")
    for tag, rows in (("only in mine", only_a), ("only in the reference", only_b)):
        if rows:
            print(f"  {len(rows)} line(s) {tag}:")
            for r in rows[:6]:
                print("    " + r.strip()[:150])


DOSE = {"picoGy": 1e-12, "nanoGy": 1e-9, "microGy": 1e-6, "milliGy": 1e-3, "Gy": 1.0}


def b1_runs(path):
    """[(particle, energy, dose, rms)] of the global runs; rms = sqrt(sum e^2 - (sum e)^2/N) is the error of the dose."""
    runs, head, glob = [], None, False
    for l in open(path, errors="replace"):
        if "End of Global Run" in l or "End of Local Run" in l:  # worker threads print their local runs too
            glob = "Global" in l
        m = re.search(r"The run is (\d+)\s*(?:(\S+) of (.+))?$", l.rstrip())
        if m and glob:  # in MT the master has no gun and prints only the number of events
            head = (m.group(2) or "", (m.group(3) or "").strip())
        m = re.search(r"Absorbed dose per run in scoring volume = edep/mass = ([\d.eE+-]+) (\w+)\s*;?\s*rms = ([\d.eE+-]+) (\w+)", l)
        if m and head:
            runs.append((*head, float(m.group(1)) * DOSE[m.group(2)], float(m.group(3)) * DOSE[m.group(4)]))
            head = None
    return runs


def b1(ref, *mine):
    r = b1_runs(ref)
    for path in mine:
        label = os.path.basename(path)
        for (_, _, d, s), (p0, e0, d0, s0) in zip(b1_runs(path), r):
            p, e = p0, e0
            pull = (d - d0) / math.hypot(s, s0)
            print(f"B1 {label}: {p} {e}: dose {d:.5g} +- {s:.2g} Gy, reference {d0:.5g} +- {s0:.2g} Gy, pull {pull:+.2f}")


def rdecay_runs(path):
    """[(N, primary, {particle: count}, half-life in days or None)] of the run summaries."""
    runs, cur, inlist = [], None, False
    for l in open(path, errors="replace"):
        m = re.search(r"The run was (\d+) (\S+) of", l)
        if m:
            cur = [int(m.group(1)), m.group(2), {}, None]
            runs.append(cur)
            continue
        if cur is None:
            continue
        if "Nb of generated particles" in l:
            inlist = True
            continue
        m = re.match(r"\s*(\S+):\s+(\d+)\s+Emean", l)
        if inlist and m:
            cur[2][m.group(1)] = int(m.group(2))
            continue
        m = re.search(r"half-life =\s+([\d.eE+-]+) (\w+)", l)
        if m:
            inlist = False
            unit = {"y": 365.0, "d": 1.0, "h": 1 / 24, "min": 1 / 1440, "s": 1 / 86400}[m.group(2)]  # CLHEP year = 365 d
            cur[3] = float(m.group(1)) * unit
    return runs


def rdecay01(mine, ref):
    a, b = rdecay_runs(mine), rdecay_runs(ref)
    for k, (ra, rb) in enumerate(zip(a, b)):
        if ra[0] < 1000:
            continue
        pulls = []
        for name in sorted(set(ra[2]) | set(rb[2])):
            x, y = ra[2].get(name, 0), rb[2].get(name, 0)
            pulls.append(((x - y) / math.sqrt(x + y) if x + y else 0.0, name, x, y))
        worst = max(pulls, key=lambda t: abs(t[0]))
        chi2 = sum(p[0] ** 2 for p in pulls)
        if all(x == y for _, _, x, y in pulls):
            print(f"rdecay01 run {k} ({ra[0]} {ra[1]}): all {len(pulls)} particle counts identical to the reference")
            continue
        print(f"rdecay01 run {k} ({ra[0]} {ra[1]}): {len(pulls)} particle counts against the reference, "
              f"chi2 = {chi2:.1f}, largest pull {worst[0]:+.2f} ({worst[1]}: {worst[2]} vs {worst[3]})")
    # Co60 -> Ni60, first decay only (the first run of 100000 Co60): ENSDF T1/2 = 1925.28(14) d,
    # beta- to the 2505.753 keV level 99.88 %, to the 1332.514 keV level 0.12 %
    co = next(r for r in a if r[1] == "Co60" and r[0] >= 1000)
    n, t = co[0], co[3]
    tl = 1925.28
    print(f"rdecay01 Co60: sampled half-life {t:.1f} d, ENSDF {tl} d, pull {(t - tl) / (tl / math.sqrt(n)):+.2f} "
          f"(error of the mean of {n} exponential lifetimes)")
    for lev, p in (("Ni60[2505.75300]", 0.9988), ("Ni60[1332.51400]", 0.0012)):
        k = co[2].get(lev, 0)
        print(f"rdecay01 Co60 -> {lev}: {k} of {n}, ENSDF {100 * p:.2f} %, pull {(k - n * p) / math.sqrt(n * p * (1 - p)):+.2f}")


def endf_table(path):
    """(E in eV, sigma in b) pairs of a G4ParticleHP data file (zlib-compressed text, three header numbers)."""
    v = [float(x) for x in zlib.decompress(open(path, "rb").read()).decode().split()]
    return list(zip(v[3::2], v[4::2]))


def interp(tab, e):
    for (e1, s1), (e2, s2) in zip(tab, tab[1:]):
        if e1 <= e <= e2:
            return s1 + (s2 - s1) * (e - e1) / (e2 - e1)
    raise ValueError(e)


def hadr00_tables(path):
    """{element: [row]} of Hadr00's cross-section tables; row = the numbers of one line."""
    out, cur = {}, None
    for l in open(path, errors="replace"):
        m = re.search(r"### Fill Cross Sections for (\S+) off (\S+)", l)
        if m:
            cur = out.setdefault(m.group(2), [])
            continue
        t = l.split()
        if cur is not None and len(t) >= 4 and all(isnum(x) for x in t):
            cur.append([float(x) for x in t])
    return out


def thermal(hp, nohp):
    """Capture at 0.0253 eV.  Hadr00 columns: N, E(MeV), elastic, inelastic, capture, fission, total (b)."""
    e = 0.0253
    cap = os.path.join(DATA, "G4NDL4.7.1/Capture/CrossSection")
    # Atlas of Neutron Resonances (Mughabghab, 6th ed., 2018): 197Au 98.65(9) b, 1H 0.3326(7) b
    atlas = {"Au": (98.65, 0.09), "H": (0.3326, 0.0007)}
    # natural composition as in Geant4's NIST elements (H: 99.989 % 1H, 0.011 % 2H)
    files = {"Au": [("79_197_Gold.z", 1.0)], "H": [("1_1_Hydrogen.z", 0.99989), ("1_2_Hydrogen.z", 0.00011)]}
    a, b = hadr00_tables(hp), hadr00_tables(nohp)
    for el in ("Au", "H"):
        row, row0 = a[el][0], b[el][0]
        g4ndl = sum(w * interp(endf_table(os.path.join(cap, f)), e) for f, w in files[el])
        s, ds = atlas[el]
        print(f"thermal capture on {el} at {row[1] * 1e6:.4g} eV: QGSP_BIC_HP {row[4]:.4g} b; G4NDL file {g4ndl:.4g} b "
              f"(ratio {row[4] / g4ndl:.4f}); Atlas {s} +- {ds} b (pull {(row[4] - s) / ds:+.1f}); "
              f"QGSP_BIC without HP {row0[4]:.4g} b")


def tendl(allhp, nohp):
    """p + Al (100 % 27Al) inelastic.  Hadr00 columns for protons: N, E(MeV), elastic, inelastic, total (b)."""
    tab = endf_table(os.path.join(DATA, "G4TENDL1.4/Proton/Inelastic/CrossSection/13_27_Aluminum.z"))
    a, b = hadr00_tables(allhp)["Al"], hadr00_tables(nohp)["Al"]
    for row, row0 in zip(a, b):
        e = row[1]
        ref = f"G4TENDL file {interp(tab, e * 1e6):.4g} b" if e < 20 else "above 20 MeV: Binary cascade with BGG cross sections"
        print(f"p + Al inelastic at {e:.4g} MeV: QGSP_BIC_AllHP {row[3]:.4g} b; {ref}; QGSP_BIC {row0[3]:.4g} b")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"table": table, "b1": b1, "rdecay01": rdecay01, "thermal": thermal, "tendl": tendl}[cmd](*args)
