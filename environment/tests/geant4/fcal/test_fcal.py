"""Geant4's example advanced/lAr_calorimeter (the ATLAS FCAL in its CERN test beam) for run_fcal.sh.

  test_fcal.py ref <mine.log> <lAr_calorimeter.out>   the 18 events of run1.mac against the reference output (means)
  test_fcal.py scan <electrodes.dat> <data-tracks> <muon.log> <e_20.log> <e_40.log> ...
      own MIP sampling fraction of FCAL1 from its electrode lattice; the muons' visible fraction against it; for the
      electrons, the energy deposited in FCAL1 (copper + liquid argon), the visible energy (liquid argon only), e/mip,
      and the resolution of the visible energy, fitted to a/sqrt(E) (+) b and shown next to the ATLAS test-beam result
"""
import math
import random
import re
import statistics
import sys

# example's materials (FCALMaterialConsultant.cc): Cu 8.96, LAr 1.40 g/cm3; minimum dE/dx (PDG): Cu 1.403, LAr 1.519 MeV cm2/g
RHO_CU, RHO_LAR, DEDX_CU, DEDX_LAR = 8.96, 1.40, 1.403, 1.519
R_IN, R_OUT = 0.236, 0.263          # cm, the liquid-argon gap around each rod (FCALEMModuleParameters.input)
ATLAS = (0.286, 0.036)              # electrons, FCal 2003 test beam, noise subtracted (P. Krieger, ICATPP 2007)
Z_PB, R_HOLE = 290.5, 2.75          # cm, the hole counter's 0.5 cm lead with its 2.75 cm hole on the beam axis


def beam_at_lead(tracks, n):
    """Distance from the axis (cm) where each of the first n beam particles crosses the hole counter's lead.  The serial
    run takes the lines of the (cleaned) track file in order; the direction is (-cosX, cosY, -cosZ) as in
    FCALPrimaryGeneratorAction.cc."""
    t = open(tracks).read().split()
    r = []
    for i in range(n):
        x, y, z, cx, cy, cz = (float(v) for v in t[7 * i + 1:7 * i + 7])
        s = (Z_PB - z) / (-cz)
        r.append(math.hypot(x - cx * s, y + cy * s))
    return r


def events(path):
    """Per-event values in file order (serial runs): EmEdep, HadEdep, tracks out of world, secondaries, visible energy."""
    keys = {"em": r"EmEdep is=([-\d.eE+]+) MeV", "had": r"HadEdep is=([-\d.eE+]+) MeV", "out": r"N Tracks out of world (\d+)",
            "sec": r"N Secondaries (\d+)", "vis": r"FCAL1 LAr visible energy \(MeV\): ([-\d.eE+]+)"}
    out = {k: [] for k in keys}
    for line in open(path, errors="replace"):
        for k, rx in keys.items():
            m = re.search(rx, line)
            if m:
                out[k].append(float(m.group(1)))
    return out


def core_sigma(v):
    """Half-width of the central 68.27 % (a Gaussian's sigma, insensitive to the tails), with a bootstrap error."""
    def hw(x):
        x = sorted(x)
        n = len(x)
        return (x[min(n - 1, int(0.84135 * n))] - x[int(0.15865 * n)]) / 2
    rng = random.Random(1)
    boot = [hw([rng.choice(v) for _ in v]) for _ in range(200)]
    return hw(v), statistics.stdev(boot)


def mean_err(v):
    return statistics.mean(v), statistics.stdev(v) / math.sqrt(len(v))


def ref(mine, reference):
    a, b = events(mine), events(reference)
    for k, label in (("em", "energy in FCAL1 (MeV)"), ("had", "energy in FCAL2 (MeV)"),
                     ("out", "tracks out of the world"), ("sec", "secondaries")):
        (m1, e1), (m2, e2) = mean_err(a[k]), mean_err(b[k])
        print(f"run1.mac, {len(a[k])} events of 20 GeV e-: {label}: mean {m1:.4g} +- {e1:.2g}, reference {m2:.4g} +- {e2:.2g}"
              f" ({len(b[k])} events), pull {(m1 - m2) / math.hypot(e1, e2):+.2f}")


def f_mip(electrodes):
    t = open(electrodes).read().split()
    xy = [(float(t[i + 1]), float(t[i + 2])) for i in range(0, len(t) - 5, 6)]
    nn = []
    for i, (x, y) in enumerate(xy[:400]):
        nn.append(min(math.hypot(x - u, y - v) for j, (u, v) in enumerate(xy) if j != i))
    d = statistics.median(nn)
    cell = math.sqrt(3) / 2 * d * d                          # hexagonal lattice: area per electrode
    lar = math.pi * (R_OUT ** 2 - R_IN ** 2)
    a = lar / cell
    s_lar, s_cu = a * RHO_LAR * DEDX_LAR, (1 - a) * RHO_CU * DEDX_CU
    f = s_lar / (s_lar + s_cu)
    print(f"FCAL1 geometry: {len(xy)} electrodes, nearest-neighbour distance {d:.4f} cm (spread {min(nn):.4f} to "
          f"{max(nn):.4f}), {cell:.5f} cm2 per electrode, liquid argon {100 * a:.3f} % of the area; own MIP sampling "
          f"fraction f_mip = {100 * f:.4f} %")
    return f


def scan(electrodes, tracks, muon, *elogs):
    f = f_mip(electrodes)
    mu = events(muon)
    n = min(len(mu["vis"]), len(mu["em"]))
    fmu = sum(mu["vis"][:n]) / sum(mu["em"][:n])
    print(f"muons (20 GeV, {n} events): visible / deposited in FCAL1 = {100 * fmu:.4f} %, mu/mip = {fmu / f:.3f} "
          f"(mean deposited {statistics.mean(mu['em'][:n]):.0f} MeV)")
    pts, pts_in = [], []
    for path in elogs:
        e_gev = float(re.search(r"(\d+)\.log$", path).group(1))
        ev = events(path)
        n = min(len(ev["vis"]), len(ev["em"]))
        em, vis = ev["em"][:n], ev["vis"][:n]
        m_em = statistics.mean(em)
        tail = sum(1 for x in em if x < 0.9 * 1000 * e_gev) / n
        rb = beam_at_lead(f"{tracks}/tracks-{e_gev:.0f}GeV.dat", n)
        hit = [x < 0.9 * 1000 * e_gev for x in em]
        n_out = sum(1 for r in rb if r > R_HOLE)
        t_out = sum(1 for r, h in zip(rb, hit) if r > R_HOLE and h)
        t_in = sum(1 for r, h in zip(rb, hit) if r <= R_HOLE and h)
        m_vis = statistics.median(vis)
        rms = statistics.stdev(vis) / statistics.mean(vis)
        c, dc = core_sigma(vis)
        r, dr = c / m_vis, dc / m_vis
        fe = sum(vis) / sum(em)
        pts.append((e_gev, r, dr))
        atlas = math.hypot(ATLAS[0] / math.sqrt(e_gev), ATLAS[1])
        print(f"e- {e_gev:5.0f} GeV ({n} events): in FCAL1 {100 * m_em / (1000 * e_gev):.2f} % of E (median "
              f"{100 * statistics.median(em) / (1000 * e_gev):.2f} %, below 90 % in {100 * tail:.1f} % of the events); "
              f"visible {100 * m_vis / (1000 * e_gev):.4f} % of E (median), e/mip {fe / f:.3f}; sigma/E of the visible "
              f"energy: core {100 * r:.2f} +- {100 * dr:.2f} %, rms {100 * rms:.1f} % (ATLAS {100 * atlas:.2f} %)")
        vin = [v for v, r in zip(vis, rb) if r <= R_HOLE]
        ci, dci = core_sigma(vin)
        mi = statistics.median(vin)
        pts_in.append((e_gev, ci / mi, dci / mi))
        print(f"      beam through the hole only ({len(vin)} events): sigma/E core {100 * ci / mi:.2f} +- {100 * dci / mi:.2f} %, "
              f"rms {100 * statistics.stdev(vin) / statistics.mean(vin):.1f} %")
        print(f"      beam outside the {R_HOLE} cm hole of the lead at z = {Z_PB} cm: {n_out} events, {t_out} of them below "
              f"90 %; inside: {n - n_out} events, {t_in} below 90 %")
    fit(pts, "all events")
    fit(pts_in, "beam through the hole (the hole counter as a veto, as in the test beam)")


def fit(pts, label):
    """Weighted least squares of (sigma/E)^2 = a^2/E + b^2."""
    w = [1 / (2 * r * dr) ** 2 for _, r, dr in pts]
    x = [1 / e for e, _, _ in pts]
    y = [r * r for _, r, _ in pts]
    sw, sx, sy = sum(w), sum(wi * xi for wi, xi in zip(w, x)), sum(wi * yi for wi, yi in zip(w, y))
    sxx, sxy = sum(wi * xi * xi for wi, xi in zip(w, x)), sum(wi * xi * yi for wi, xi, yi in zip(w, x, y))
    det = sw * sxx - sx * sx
    a2, b2 = (sw * sxy - sx * sy) / det, (sxx * sy - sx * sxy) / det
    chi2 = sum(wi * (yi - a2 * xi - b2) ** 2 for wi, xi, yi in zip(w, x, y))
    a, b = math.sqrt(max(a2, 0)), math.sqrt(max(b2, 0))
    da, db = math.sqrt(sw / det) / (2 * a), math.sqrt(sxx / det) / (2 * b)   # from the covariance of (a^2, b^2)
    print(f"fit of the core sigma/E = a/sqrt(E) (+) b, {label}: a = {100 * a:.1f} +- {100 * da:.1f} %, "
          f"b = {100 * b:.2f} +- {100 * db:.2f} % (chi2 = "
          f"{chi2:.1f} for {len(pts) - 2} d.o.f.); ATLAS FCal1 test beam: a = {100 * ATLAS[0]:.1f} %, "
          f"b = {100 * ATLAS[1]:.1f} % (reference)")

if __name__ == "__main__":
    {"ref": ref, "scan": scan}[sys.argv[1]](*sys.argv[2:])
