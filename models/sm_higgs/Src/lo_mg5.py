"""Step (1) of the Higgs note: MadGraph's tree H decays against the hand forms and FeynCalc.

All with the values of the H card (work/card_H.dat; the NLO note's H card: M_Z pole, M_W = M_Z c(M_H), 1/aEWM1 = alpha(M_H),
alpha_s(M_H), the pole masses, V(M_H)), in which the UFO's couplings are e from aEWM1, s_W^2 = 1 - M_W^2/M_Z^2, v = 2 M_W s_W/e
and the Yukawa coupling sqrt(2) m/v with the kinematic mass:
  (a) compute_widths h (two-body) against Eq. (lo) with y = sqrt(2) m/v;
  (b) the standalone sum|M|^2 (MadGraph's unitary gauge) of H -> W+ tau- nutaubar, W+ b cbar, Z nue nuebar, Z b bbar against
      FeynCalc's Feynman-gauge form with the masses (work/me_hvff.txt, lo_feyncalc.wl; times |V_cb|^2 of the card) at Dalitz
      points (no widths in the card: FeynCalc's off-shell propagator has none), and of H -> nue e+ mu- numubar,
      e- e+ mu- mu+ (e, mu massless in the card) against the hand form of Appendix A with fixed-width Breit-Wigner
      propagators at four-body points (Gamma_W, Gamma_Z in the card: the LO widths in the card's couplings with massless
      fermions);
  (c) madevent's widths of H -> nue e+ mu- numubar and H -> e- e+ mu- mu+ (no cuts) against the factorised integral of
      lo_widths.py with the card's couplings and widths.
The values are written with 14 digits as MadGraph's reader keeps them (the NLO note's set_card); the hand forms take the
rounded values and the invariants of the momenta exactly as written (mpmath, 40 digits).
Usage (from Src/): python3 lo_mg5.py --prepare   (writes work/card_H.dat and work/mg5run/lo_mg5.mg5; run mg5_aMC on it there)
                   python3 lo_mg5.py --events    (runs madevent in work/ev_hww, work/ev_hzz; a few minutes)
                   python3 lo_mg5.py             (the comparisons; writes results/lo_mg5.csv)
"""
import csv
import math
import re
import subprocess
import sys
from pathlib import Path

import mpmath
import numpy as np

import lo_widths as lw
from nlo_inputs import POLE, at, std_params

mpmath.mp.dps = 40
HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
RUN = WORK / "mg5run"
ME = WORK / "me_h"
EV = {"ww": WORK / "ev_hww", "zz": WORK / "ev_hzz"}
# name (me_hvff.txt), MadGraph process, V mass key, (m_f, m_fbar') keys, N_c, |V|^2 from the card
PROCS3 = [("W+ tau- nutaubar", "h > w+ ta- vt~", "MW", ("MTA", None), 1, lambda v: 1),
          ("W+ b cbar", "h > w+ b c~", "MW", ("MB", "MC"), 3, lambda v: v["s23"]**2 * (1 - v["s13"]**2)),
          ("Z nue nuebar", "h > z ve ve~", "MZ", (None, None), 1, lambda v: 1),
          ("Z b bbar", "h > z b b~", "MZ", ("MB", "MB"), 3, lambda v: 1)]
PROCS4 = [("nue e+ mu- numubar", "h > ve e+ mu- vm~", "ww"), ("e- e+ mu- mu+", "h > e- e+ mu- mu+", "zz")]
PTS3 = [(0.5, 0.5), (0.1, 0.2), (0.9, 0.8), (0.02, 0.5), (0.98, 0.5), (0.5, 0.001), (0.5, 0.999)]
PTS4 = [(80.0, 30.0), (40.0, 40.0), (20.0, 90.0), (79.0, 45.0), (10.0, 10.0), (90.5, 30.0)]


def card_values():
    p = at(POLE["MH"])
    MZ = POLE["MZ"]
    vals = {"aEWM1": 1 / p["alpha"], "aS": p["alphas"], "MZ": MZ, "MW": MZ * math.sqrt(1 - p["s2"]), "MH": POLE["MH"],
            "MT": POLE["MT"], "MB": POLE["MB"], "MC": POLE["MC"], "MS": POLE["MS"], "MD": POLE["MD"], "MU": POLE["MU"],
            "MTA": POLE["MTA"], "MMU": POLE["MMU"], "Me": POLE["Me"]}
    s12, s23, s13, dl = std_params(p["V"])
    vals.update({"s12": s12, "s23": s23, "s13": s13, "dCKM": dl})
    return vals


def write_card(path, vals):   # as the NLO note's lo_widths.py
    blocks = [("CKMBLOCK", [(1, "s12"), (2, "s23"), (3, "s13"), (4, "dCKM")]),
              ("GAUGE", [(1, "xiA"), (2, "xiZ"), (3, "xiW"), (4, "xiG")]),
              ("MASS", [(1, "MD"), (2, "MU"), (3, "MS"), (4, "MC"), (5, "MB"), (6, "MT"), (11, "Me"), (13, "MMU"), (15, "MTA"),
                        (23, "MZ"), (24, "MW"), (25, "MH")]),
              ("SMINPUTS", [(1, "aEWM1"), (3, "aS")])]
    v = dict(vals, xiA=1.0, xiZ=1.0, xiW=1.0, xiG=1.0)
    with open(path, "w") as fh:
        for name, entries in blocks:
            fh.write("BLOCK %s\n" % name)
            for code, key in entries:
                fh.write("    %d %.16e # %s\n" % (code, v[key], key))
        for pdg in (6, 23, 24, 25):
            fh.write("DECAY %d 0.000000e+00\n" % pdg)


def card():
    vals = {}
    for line in open(WORK / "card_H.dat"):
        m = re.match(r"\s+\d+\s+(\S+)\s+#\s+(\S+)", line)
        if m:
            vals[m.group(2)] = float("%.13e" % float(m.group(1)))   # what set_card writes
    return vals


def set_card(src, dst, vals, widths):
    s = open(src).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s(?:\s[^\n]*)?\n)" % k, lambda m: m.group(1) + "%.13e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg, w in widths.items():
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "%.13e" % w, s)
        assert n == 1, pdg
    open(dst, "w").write(s)


def couplings(v):
    """the card's tree couplings: e, s^2, g, gZ, g_HWW = g MW, g_HZZ = gZ MZ, the LO widths of W and Z (massless fermions)"""
    ee = math.sqrt(4 * math.pi / v["aEWM1"])
    s2 = 1 - v["MW"]**2 / v["MZ"]**2
    g, gz = ee / math.sqrt(s2), ee / math.sqrt(s2) / math.sqrt(1 - s2)
    gw = lw.NWD * g**2 * v["MW"] / (48 * math.pi)
    gzw = sum(nc * lw.cz2(gz, s2, t3, q) for nc, t3, q in lw.ZF) * v["MZ"] / (24 * math.pi)
    return dict(ee=ee, s2=s2, g=g, gz=gz, ghww=g * v["MW"], ghzz=gz * v["MZ"], GW=float("%.13e" % gw), GZ=float("%.13e" % gzw))


def card_massless(v):
    return dict(v, Me=0.0, MMU=0.0)


def widths_of(c):
    return {6: 0.0, 23: c["GZ"], 24: c["GW"], 25: 0.0}


# %% phase-space points
def rotation(seed):
    rng = np.random.default_rng(seed)
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q @ np.diag(np.sign(np.diag(r)))
    return q if np.linalg.det(q) > 0 else -q


def dalitz_point(M, m1, m2, m3, xi, f):
    """s23 = (m2 + m3)^2 + xi [(M - m1)^2 - (m2 + m3)^2], s12 = lo + f (hi - lo) at that s23"""
    s23 = (m2 + m3)**2 + xi * ((M - m1)**2 - (m2 + m3)**2)
    r = math.sqrt(s23)
    e2, e1 = (s23 - m3**2 + m2**2) / (2 * r), (M**2 - s23 - m1**2) / (2 * r)
    a, b = math.sqrt(e1**2 - m1**2), math.sqrt(e2**2 - m2**2)
    lo, hi = (e1 + e2)**2 - (a + b)**2, (e1 + e2)**2 - (a - b)**2
    s12 = lo + f * (hi - lo)
    return s12, M**2 + m1**2 + m2**2 + m3**2 - s12 - s23


def momenta3(M, ms, s12, s13, rot):
    m1, m2, m3 = ms
    s23 = M**2 + m1**2 + m2**2 + m3**2 - s12 - s13
    E1, E2, E3 = (M**2 + m1**2 - s23) / (2 * M), (M**2 + m2**2 - s13) / (2 * M), (M**2 + m3**2 - s12) / (2 * M)
    a1, a3 = math.sqrt(E1**2 - m1**2), math.sqrt(E3**2 - m3**2)
    c13 = (2 * E1 * E3 - (s13 - m1**2 - m3**2)) / (2 * a1 * a3)
    p1 = np.array([0.0, 0.0, a1])
    p3 = a3 * np.array([math.sqrt(max(0.0, 1 - c13**2)), 0.0, c13])
    p2 = -p1 - p3
    assert abs(math.sqrt(p2 @ p2 + m2**2) - E2) < 1e-10 * M
    return [(M, 0.0, 0.0, 0.0)] + [(E, *(rot @ p)) for E, p in ((E1, p1), (E2, p2), (E3, p3))]


def boost(p, b):
    """boost the four-vector p by the velocity b"""
    b2 = b @ b
    if b2 == 0:
        return p
    gam = 1 / math.sqrt(1 - b2)
    bp = b @ p[1:]
    e = gam * (p[0] + bp)
    vec = p[1:] + ((gam - 1) * bp / b2 + gam * p[0]) * b
    return np.array([e, *vec])


def momenta4(M, w1, w2, seed):
    """H -> V1(w1) V2(w2), V1 -> p1 p2, V2 -> p3 p4, all massless, random angles"""
    rng = np.random.default_rng(100 + seed)
    def unit():
        c, ph = rng.uniform(-1, 1), rng.uniform(0, 2 * math.pi)
        s = math.sqrt(1 - c * c)
        return np.array([s * math.cos(ph), s * math.sin(ph), c])
    pp = math.sqrt((M**2 - (w1 + w2)**2) * (M**2 - (w1 - w2)**2)) / (2 * M)
    n = unit()
    out = []
    for w, sgn in ((w1, 1), (w2, -1)):
        e = math.sqrt(w**2 + pp**2)
        b = sgn * pp / e * n
        d = unit()
        for s in (1, -1):
            out.append(boost(np.array([w / 2, *(s * w / 2 * d)]), b))
    return [(M, 0.0, 0.0, 0.0)] + [tuple(x) for x in out]


def run_check(d, pts):
    lines = ["%.17e %.17e %.17e %.17e" % tuple(p) for p in pts]
    with open(d / "PS.input", "w") as fh:
        fh.writelines(l + "\n" for l in lines)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    mom = [[mpmath.mpf(x) for x in l.split()] for l in lines]
    return float(re.search(r"Matrix element =\s*(\S+)", o).group(1)), mom


def dot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def hand4(mom, kind, v, c):
    """Appendix A, H -> f1 fbar2 f3 fbar4 with |D|^2 = (s - M^2)^2 + M^2 Gamma^2"""
    p1, p2, p3, p4 = mom[1:]
    if kind == "ww":
        gh, mv, gam = c["ghww"], v["MW"], c["GW"]
        c1 = c3 = (mpmath.mpf(c["g"])**2 / 2, 0)
    else:
        gh, mv, gam = c["ghzz"], v["MZ"], c["GZ"]
        gz, s2 = mpmath.mpf(c["gz"]), mpmath.mpf(c["s2"])
        c1 = c3 = (gz**2 * (-mpmath.mpf(1) / 2 + s2)**2, gz**2 * s2**2)
    num = 16 * mpmath.mpf(gh)**2 * ((c1[0] * c3[0] + c1[1] * c3[1]) * dot(p1, p3) * dot(p2, p4)
                                    + (c1[0] * c3[1] + c1[1] * c3[0]) * dot(p1, p4) * dot(p2, p3))
    bw = lambda s: (s - mpmath.mpf(mv)**2)**2 + mpmath.mpf(mv)**2 * mpmath.mpf(gam)**2
    return num / (bw(dot(add(p1, p2), add(p1, p2))) * bw(dot(add(p3, p4), add(p3, p4))))


def ev_result(d):
    """madevent's width (the banner's integrated weight, in GeV for a decay) and its error (SubProcesses/results.dat)"""
    b = sorted((d / "Events").glob("run_*/run_*_banner.txt"))
    if not b:
        return None
    m = re.search(r"Integrated weight \(pb\)\s*:\s*(\S+)", b[-1].read_text())
    err = float(open(d / "SubProcesses" / "results.dat").readline().split()[1])
    return (float(m.group(1)), err) if m else None


def read_widths(path):   # as the NLO note's lo_widths.py
    out, parent = {}, None
    for line in open(path):
        m = re.match(r"DECAY\s+(\d+)\s+(\S+)", line)
        if m:
            parent = int(m.group(1)); out[(parent, "total")] = float(m.group(2)); continue
        m = re.match(r"\s+(\S+)\s+2\s+(-?\d+)\s+(-?\d+)\s+#\s+(\S+)", line)
        if m and parent is not None:
            out[(parent, tuple(sorted((int(m.group(2)), int(m.group(3))))))] = float(m.group(4))
    return out


if len(sys.argv) > 1 and sys.argv[1] == "--prepare":
    RUN.mkdir(parents=True, exist_ok=True)
    write_card(WORK / "card_H.dat", card_values())
    with open(RUN / "lo_mg5.mg5", "w") as fh:
        fh.write("set automatic_html_opening False\nimport model ../SM_CKM_UFO\n")
        fh.write("compute_widths h --body_decay=2 --min_br=0 --path=../card_H.dat --output=../widths_H.dat\n")
        fh.write("generate %s\n" % PROCS3[0][1])
        for p in PROCS3[1:] + PROCS4:
            fh.write("add process %s\n" % p[1])
        fh.write("output standalone ../me_h -f\n")
        for name, proc, kind in PROCS4:
            fh.write("generate %s\noutput ../ev_h%s -f\n" % (proc, kind))
    print("wrote work/card_H.dat and work/mg5run/lo_mg5.mg5")
    sys.exit(0)

v = card()
c = couplings(v)
v0 = card_massless(v)

if len(sys.argv) > 1 and sys.argv[1] == "--events":
    for kind, d in EV.items():
        set_card(d / "Cards" / "param_card_default.dat", d / "Cards" / "param_card.dat", v0, widths_of(c))
        rc = open(d / "Cards" / "run_card_default.dat").read()
        sets = {"nevents": "20000", "iseed": "11", "use_syst": "False", "ptl": "0.0", "etal": "-1.0", "drll": "0.0",
                "mmll": "0.0", "cut_decays": "False", "sde_strategy": "1", "hard_survey": "1"}
        for k, x in sets.items():
            rc, n = re.subn(r"\n(\s*)\S+(\s*=\s*%s\b)" % k, lambda m: "\n" + m.group(1) + x + m.group(2), rc)
            print("  run_card %s = %s (%d)" % (k, x, n))
        open(d / "Cards" / "run_card.dat", "w").write(rc)
        o = subprocess.run(["./bin/generate_events", "-f"], cwd=d, capture_output=True, text=True)
        open(WORK / ("ev_h%s.log" % kind), "w").write(o.stdout + o.stderr)
        print("  %s: %s" % (kind, ev_result(d) or "no result (see work/ev_h%s.log)" % kind))
    sys.exit(0)

rows = []
# (a) two-body widths
print("(a) compute_widths h against Eq. (lo) with y = sqrt(2) m/v, v = 2 M_W s_W/e of the card:")
mg = read_widths(WORK / "widths_H.dat")
vcard = 2 * v["MW"] * math.sqrt(c["s2"]) / c["ee"]
worst = 0.0
for f, nc, mk, pid in (("b", 3, "MB", 5), ("c", 3, "MC", 4), ("tau", 1, "MTA", 15), ("mu", 1, "MMU", 13)):
    m = v[mk]
    mine = nc * (math.sqrt(2) * m / vcard)**2 * v["MH"] / (16 * math.pi) * (1 - 4 * m**2 / v["MH"]**2)**1.5
    got = mg.get((25, (-pid, pid)))
    rel = got / mine - 1
    worst = max(worst, abs(rel))
    print("  H -> %-4s MadGraph %.12e, Eq. (lo) %.12e, rel %+.1e" % (f, got, mine, rel))
    rows.append(["two-body", f, "", "%.16e" % got, "%.16e" % mine, "%.3e" % rel])
print("  largest |rel|: %.1e" % worst)

# (b) standalone matrix elements
me = dict(line.strip().split("|", 1) for line in open(WORK / "me_hvff.txt") if "|" in line)
NOWIDTH = {6: 0.0, 23: 0.0, 24: 0.0, 25: 0.0}
set_card(ME / "Cards" / "param_card_default.dat", ME / "Cards" / "param_card.dat", v0, NOWIDTH)   # read by ./check at run time
vm = {k: mpmath.mpf(repr(x)) for k, x in v0.items()}
subs = sorted(p.name for p in (ME / "SubProcesses").iterdir() if p.is_dir() and p.name.startswith("P"))
ns = {"Power": lambda a, b: a**b, "Sqrt": mpmath.sqrt}
worst3, worst4 = 0.0, 0.0
print("(b) standalone sum|M|^2 against FeynCalc (three-body) and the Breit-Wigner hand form (four-body):")
for i, (name, proc, mvk, (k2, k3), nc, vf) in enumerate(PROCS3):
    d = ME / "SubProcesses" / next(s for s in subs if s.startswith("P%d_" % (i + 1)))
    (d / "check").unlink(missing_ok=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    ms = (v[mvk], v[k2] if k2 else 0.0, v[k3] if k3 else 0.0)
    code = compile(me[name], name, "eval")
    for j, (xi, f) in enumerate(PTS3):
        s12, s13 = dalitz_point(v["MH"], *ms, xi, f)
        got, mom = run_check(d, momenta3(v["MH"], ms, s12, s13, rotation(j)))
        s12x, s13x = dot(add(mom[1], mom[2]), add(mom[1], mom[2])), dot(add(mom[1], mom[3]), add(mom[1], mom[3]))
        loc = dict(vm, ee=mpmath.sqrt(4 * mpmath.pi / vm["aEWM1"]), s12=s12x, s13=s13x)
        hd = float(eval(code, ns, loc) * vf(vm))
        rel = got / hd - 1
        worst3 = max(worst3, abs(rel))
        print("  %-18s %-16s point %d: MadGraph %.15e, FeynCalc %.15e, rel %+.1e" % (name, d.name, j, got, hd, rel))
        rows.append(["three-body", name, j, "%.16e" % got, "%.16e" % hd, "%.3e" % rel])
set_card(ME / "Cards" / "param_card_default.dat", ME / "Cards" / "param_card.dat", v0, widths_of(c))
for i, (name, proc, kind) in enumerate(PROCS4):
    d = ME / "SubProcesses" / next(s for s in subs if s.startswith("P%d_" % (len(PROCS3) + i + 1)))
    (d / "check").unlink(missing_ok=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    for j, (w1, w2) in enumerate(PTS4):
        got, mom = run_check(d, momenta4(v["MH"], w1, w2, j))
        hd = float(hand4(mom, kind, v0, c))
        rel = got / hd - 1
        worst4 = max(worst4, abs(rel))
        print("  %-18s %-16s m12 = %5.1f, m34 = %5.1f: MadGraph %.15e, hand %.15e, rel %+.1e" % (name, d.name, w1, w2, got, hd, rel))
        rows.append(["four-body", name, j, "%.16e" % got, "%.16e" % hd, "%.3e" % rel])
print("  largest |rel|: three-body %.1e, four-body %.1e" % (worst3, worst4))

# (c) madevent widths against the factorised integral
print("(c) madevent widths (no cuts) against the factorised integral with the card's couplings and widths:")
for name, proc, kind in PROCS4:
    m = ev_result(EV[kind])
    if kind == "ww":
        mine = lw.four_f(c["ghww"], v["MW"], c["GW"], lw.gv_of(c["g"]**2 / 2), lw.gv_of(c["g"]**2 / 2))
    else:
        cz = lw.cz2(c["gz"], c["s2"], -0.5, -1)
        mine = lw.four_f(c["ghzz"], v["MZ"], c["GZ"], lw.gv_of(cz), lw.gv_of(cz))
    if m:
        got, err = m
        print("  H -> %-18s madevent %.6e +- %.1e GeV, integral %.8e GeV, rel %+.2e = %+.2f sigma"
              % (name, got, err, mine, got / mine - 1, (got - mine) / err))
        rows.append(["madevent", name, "", "%.8e" % got, "%.10e" % mine, "%.3e" % (got / mine - 1)])
    else:
        print("  H -> %-18s no madevent result; integral %.8e GeV" % (name, mine))
print("  card: Gamma_W = %.10f, Gamma_Z = %.10f GeV (LO, massless fermions, the card's couplings)" % (c["GW"], c["GZ"]))
with open(HERE / "results" / "lo_mg5.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["check", "channel", "point", "madgraph", "hand", "rel"])
    w.writerows(rows)
print("wrote results/lo_mg5.csv")
