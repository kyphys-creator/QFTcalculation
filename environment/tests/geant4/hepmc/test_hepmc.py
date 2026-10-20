"""The stage-3 LHC events (p p -> e+ e-, 13 TeV, MG5 + Pythia 8, HepMC 2) through Geant4's HepMCEx02 (run_hepmc.sh).
Usage: test_hepmc.py <events.hepmc> <primaries.csv> <calo_entry.csv> <events.csv>

  1. import: every final-state particle (status 1) of the HepMC file against the Geant4 primaries of the same event
     (PDG code, momentum, vertex), and the sum of their momenta against the two 6.5 TeV beams
  2. field: where the primary e+- with pT > 10 GeV and |eta| < 0.8 enter the barrel calorimeter (r = 2 m), against an
     own extrapolation: a helix in HepMCEx02's field (Bz = 3 T for r < 1 m and |z| < 1 m, H02Field.cc) up to the edge of
     the field, then a straight line (air in between, no energy loss); the spread against multiple scattering
"""
import csv
import math
import statistics
import sys
from collections import defaultdict

B_T, K = 3.0, 0.299792458          # Bz in tesla; pT [GeV] = K * B [T] * rho [m]
R_FIELD, Z_FIELD, R_CAL, Z_CAL = 1.0, 1.0, 2.0, 5.0   # m (H02Field.cc, H02DetectorConstruction.cc)
R_HALL, Z_HALL = 5000.0, 10000.0                       # mm, the world (EXP_HALL)
X0_AIR = 303.9e3                                       # mm, radiation length of dry air at 20 C, 1 atm (PDG)


def read_hepmc(path):
    """{event index: [(pdg, px, py, pz, e, x, y, z)]} of the status-1 particles (GeV, mm), in file order."""
    events, cur, vtx, orphans = [], None, None, 0
    for line in open(path):
        t = line.split()
        if not t:
            continue
        if t[0] == "E":
            cur = []
            events.append(cur)
        elif t[0] == "U":
            assert t[1:3] == ["GEV", "MM"], line
        elif t[0] == "V":
            vtx = tuple(float(v) for v in t[3:6])
            orphans = int(t[7])          # the first n_orphan P lines are incoming particles without a production vertex
        elif t[0] == "P":
            if orphans > 0:
                orphans -= 1
                continue
            if int(t[8]) == 1:
                cur.append((int(t[2]), float(t[3]), float(t[4]), float(t[5]), float(t[6])) + vtx)
    return events


def check_import(hep, g4rows):
    """Match each final-state particle to a Geant4 primary of the same event with the same PDG code and momentum."""
    g4 = defaultdict(lambda: defaultdict(list))
    for r in g4rows:
        p = (float(r["px_GeV"]), float(r["py_GeV"]), float(r["pz_GeV"]))
        x = (float(r["x_mm"]), float(r["y_mm"]), float(r["z_mm"]))
        g4[int(r["event"])][(int(r["pdg"]),) + tuple(round(c, 6) for c in p)].append(p + x)
    npart = nmatch = 0
    dp = dx = 0.0
    outside, inside_missing, sums = [], [], []
    for i, ev in enumerate(hep):
        sums.append([sum(p[k] for p in ev) for k in (1, 2, 3, 4)])
        for p in ev:
            npart += 1
            key = (p[0],) + tuple(round(c, 6) for c in p[1:4])
            if g4[i][key]:
                u = g4[i][key].pop()
                nmatch += 1
                dp = max(dp, max(abs(u[k] - p[1 + k]) for k in range(3)) / math.hypot(*p[1:4]))
                dx = max(dx, max(abs(u[3 + k] - p[5 + k]) for k in range(3)))
            elif math.hypot(p[5], p[6]) >= R_HALL or abs(p[7]) >= Z_HALL:
                outside.append(p)
            else:
                inside_missing.append(p)
    extra = sum(len(v) for ev in g4.values() for v in ev.values())
    print(f"hepmc import: {len(hep)} events, {npart} final-state particles ({npart / len(hep):.0f} per event); "
          f"{nmatch} found among the Geant4 primaries (same PDG code; momenta equal to {dp:.0e} relative, "
          f"vertices to {dx:.0e} mm); {extra} Geant4 primaries without a HepMC partner")
    zs = sorted(abs(p[7]) / 1000 for p in outside)
    print(f"hepmc import: {len(outside)} not imported because their production vertex is outside HepMCEx02's hall "
          f"(r < 5 m, |z| < 10 m; HepMCG4Interface::CheckVertexInsideWorld), up to |z| = {zs[-1]:.0f} m, "
          f"{len(outside) / len(hep):.1f} per event, {sum(p[4] for p in outside) / len(hep):.0f} GeV per event; "
          f"not imported with the vertex inside: {len(inside_missing)}" if outside else
          f"hepmc import: not imported: {len(inside_missing)}")
    print(f"hepmc import: sum of the final-state momenta of each event (Pythia): |px|, |py| <= "
          f"{max(max(abs(s[0]), abs(s[1])) for s in sums):.0e} GeV, |pz| <= {max(abs(s[2]) for s in sums):.0e} GeV, "
          f"|E - 13000 GeV| <= {max(abs(s[3] - 13000) for s in sums):.0e} GeV")


def predict(vx, vy, vz, px, py, pz, q, field=True):
    """Entry point (m) into the barrel calorimeter: helix while r < R_FIELD and |z| < Z_FIELD, then a line to r = R_CAL."""
    pt = math.hypot(px, py)
    phi0, tz = math.atan2(py, px), pz / pt
    if field:
        w = q * K * B_T / pt                      # signed curvature (1/m): phi(s) = phi0 - w s for Bz > 0
        x = lambda s: vx + (math.sin(phi0) - math.sin(phi0 - w * s)) / w
        y = lambda s: vy + (math.cos(phi0 - w * s) - math.cos(phi0)) / w
        sz = (math.copysign(Z_FIELD, tz) - vz) / tz if tz != 0 else math.inf
        lo, hi = 0.0, min(sz, math.pi / abs(w))   # r(s) grows up to s = pi/|w|
        if x(hi) ** 2 + y(hi) ** 2 < R_FIELD ** 2:
            s1 = hi
        else:
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if x(mid) ** 2 + y(mid) ** 2 < R_FIELD ** 2 else (lo, mid)
            s1 = 0.5 * (lo + hi)
        x1, y1, z1, phi1 = x(s1), y(s1), vz + tz * s1, phi0 - w * s1
    else:
        x1, y1, z1, phi1 = vx, vy, vz, phi0
    ux, uy = math.cos(phi1), math.sin(phi1)
    b, c = x1 * ux + y1 * uy, x1 * x1 + y1 * y1 - R_CAL ** 2
    t = -b + math.sqrt(b * b - c)
    return x1 + t * ux, y1 + t * uy, z1 + tz * t


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def check_field(hep, entries):
    vertex = {}
    for i, ev in enumerate(hep):
        for p in ev:
            if abs(p[0]) == 11:
                vertex[(i, p[0], round(p[1], 9), round(p[2], 9), round(p[3], 9))] = p[5:8]
    dphi, dz, bend, eloss, pull, n_sel = [], [], [], [], [], 0
    for r in entries:
        pdg = int(r["pdg"])
        px, py, pz = float(r["px0_GeV"]), float(r["py0_GeV"]), float(r["pz0_GeV"])
        pt = math.hypot(px, py)
        eta = math.asinh(pz / pt)
        if pt < 10 or abs(eta) > 0.8:
            continue
        n_sel += 1
        v = [c / 1000 for c in vertex[(int(r["event"]), pdg, round(px, 9), round(py, 9), round(pz, 9))]]
        q = -1 if pdg == 11 else 1
        x2, y2, z2 = predict(*v, px, py, pz, q)
        xs, ys, _ = predict(*v, px, py, pz, q, field=False)
        xg, yg, zg = float(r["x_mm"]) / 1000, float(r["y_mm"]) / 1000, float(r["z_mm"]) / 1000
        dphi.append(R_CAL * 1000 * wrap(math.atan2(yg, xg) - math.atan2(y2, x2)))    # mm along the cylinder
        dz.append(1000 * (zg - z2))
        bend.append(R_CAL * 1000 * abs(wrap(math.atan2(y2, x2) - math.atan2(ys, xs))))
        p0, p1 = math.hypot(px, py, pz), math.hypot(float(r["px_GeV"]), float(r["py_GeV"]), float(r["pz_GeV"]))
        eloss.append(1 - p1 / p0)
        # multiple scattering in the air (Highland, X0 = 303.9 m): sigma of the displacement after a path L is L theta0/sqrt3
        path = math.hypot(R_CAL, z2 - v[2]) * 1000                     # mm
        t = path / X0_AIR
        theta0 = 0.0136 / p0 * math.sqrt(t) * (1 + 0.038 * math.log(t))
        if eloss[-1] < 1e-3:
            pull.append(dphi[-1] / (path * theta0 / math.sqrt(3)))
    if not dphi:
        print("field: no primary e+- with pT > 10 GeV and |eta| < 0.8 reached the barrel calorimeter")
        return
    q = lambda v, f: sorted(v)[min(len(v) - 1, int(f * len(v)))]
    print(f"field: {n_sel} primary e+- with pT > 10 GeV, |eta| < 0.8 entered the barrel calorimeter; bending by the 3 T "
          f"field at r = 2 m: {statistics.median(bend):.1f} mm (median; {min(bend):.1f} to {max(bend):.1f} mm)")
    print(f"field: Geant4 - own helix-plus-line, r dphi: median {statistics.median(dphi):+.3f} mm, central 90% "
          f"[{q(dphi, 0.05):+.3f}, {q(dphi, 0.95):+.3f}] mm, largest |r dphi| {max(map(abs, dphi)):.2f} mm")
    print(f"field: Geant4 - own, dz: median {statistics.median(dz):+.4f} mm, central 90% [{q(dz, 0.05):+.4f}, "
          f"{q(dz, 0.95):+.4f}] mm; momentum lost in the air before r = 2 m: median {statistics.median(eloss):.1e}, "
          f"largest {max(eloss):.1e}")
    big = [(abs(d), l) for d, l in zip(dphi, eloss) if abs(d) > 1.0]
    print(f"field: |r dphi| > 1 mm: {len(big)} e+-, {sum(1 for _, l in big if l > 1e-2)} of them lost more than 1% of "
          f"their momentum in the air (bremsstrahlung: a softer track bends more)")
    print(f"field: r dphi / sigma of the multiple scattering in the air (Highland) for the {len(pull)} e+- that lost "
          f"< 1e-3: median {statistics.median(pull):+.2f}, half-width of the central 68% "
          f"{(q(pull, 0.84) - q(pull, 0.16)) / 2:.2f} (1 if multiple scattering alone)")


if __name__ == "__main__":
    hepfile, prim, calo, evs = sys.argv[1:5]
    hep = read_hepmc(hepfile)
    check_import(hep, list(csv.DictReader(open(prim))))
    check_field(hep, list(csv.DictReader(open(calo))))
    ev = list(csv.DictReader(open(evs)))
    print(f"muon chambers: {sum(int(r['muon_hits']) for r in ev)} hits in {len(ev)} events "
          f"(HepMCEx02 kills every secondary but muons in the calorimeters)")
