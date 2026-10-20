"""Geant4's example advanced/composite_calorimeter (the CMS HCAL test beam of 1996) for run_ccal.sh.
Run with ~/hep/opt/lhc/bin/python (uproot).

  test_ccal.py dist <run dir>                       the distributed test.g4mac (100 GeV pi-, ECAL + HCAL)
  test_ccal.py scan <example dir> <out dir>         HCAL only: own MIP sampling fraction from tbhcal96hcal.geom against
                                                    20 GeV muons; e- and pi- from 20 to 300 GeV (response, e/pi, resolution)
"""
import math
import os
import random
import re
import statistics
import sys

import numpy as np
import uproot

# minimum dE/dx (PDG, MeV cm2/g): Cu, Al, plastic scintillator (vinyltoluene; the example's C19H21 "Polystyrene"), air
DEDX = {"Copper": 1.403, "Aluminium": 1.615, "Scint": 1.956, "Air": 1.815}
# for the mean ionization loss at a given muon energy: Z/A and Sternheimer's I (eV), -C, x0, x1, a, k, delta0 (PDG)
STERN = {"Copper": (29 / 63.546, 322.0, 4.4190, -0.0254, 3.2792, 0.1434, 2.9044, 0.08),
         "Aluminium": (13 / 26.98, 166.0, 4.2395, 0.1708, 3.0127, 0.0802, 3.6345, 0.12),
         "Scint": (0.54141, 64.7, 3.1997, 0.1464, 2.4855, 0.1610, 3.2393, 0.0),
         "Air": (0.49919, 85.7, 10.5961, 1.7418, 4.2759, 0.1091, 3.3994, 0.0)}


def bethe_mean(mat, e_mu):
    """Mean ionization loss (MeV cm2/g) of a muon of total energy e_mu (MeV): Bethe with the full T_max, the density
    effect (Sternheimer) and the spin-1/2 term (T_max/E)^2/8; radiative losses not included."""
    za, i_ev, cbar, x0, x1, a, k, d0 = STERN[mat]
    m_mu, m_e, kk = 105.6584, 0.51099895, 0.307075
    gam = e_mu / m_mu
    bg2 = gam * gam - 1
    b2 = bg2 / (gam * gam)
    tmax = 2 * m_e * bg2 / (1 + 2 * gam * m_e / m_mu + (m_e / m_mu) ** 2)
    x = 0.5 * math.log10(bg2)
    if x >= x1:
        delta = 2 * math.log(10) * x - cbar
    elif x >= x0:
        delta = 2 * math.log(10) * x - cbar + a * (x1 - x) ** k
    else:
        delta = d0 * 10 ** (2 * (x - x0))
    l = 0.5 * math.log(2 * m_e * 1e6 * bg2 * tmax * 1e6 / (i_ev * i_ev)) - b2 - delta / 2 + (tmax / e_mu) ** 2 / 8
    return kk * za / b2 * l


def ntuple(path):
    t = uproot.open(path)["ntuple1"]
    return t.arrays(["ELAB", "EDEP", "EDEC", "EHDC"], library="np")


def core(v):
    """Half-width of the central 68.27 % with a bootstrap error."""
    def hw(x):
        x = np.sort(x)
        n = len(x)
        return (x[min(n - 1, int(0.84135 * n))] - x[int(0.15865 * n)]) / 2
    rng = random.Random(1)
    v = np.asarray(v)
    boot = [hw(v[[rng.randrange(len(v)) for _ in range(len(v))]]) for _ in range(200)]
    return hw(v), float(np.std(boot, ddof=1))


def dist(rundir):
    a = ntuple(os.path.join(rundir, "ccal.root"))
    log = open(os.path.join(rundir, "dist.log"), errors="replace").read()
    n_ev = len(re.findall(r"--- End of event", log))
    print(f"test.g4mac (100 GeV pi-, ECAL + HCAL): {n_ev} events ended, {len(a['EDEP'])} ntuple rows; visible energy "
          f"EDEP mean {a['EDEP'].mean():.3f} GeV (ECAL crystals {a['EDEC'].mean():.3f}, HCAL scintillators "
          f"{a['EHDC'].mean():.3f}); exceptions in the log: {log.count('G4Exception-START')}. The reference output has "
          f"no per-event numbers (20 events, begin and end of event only).")


def materials(exdir):
    """Densities (g/cm3) of the example's materials (dataglobal/material.cms)."""
    rho = {}
    for line in open(os.path.join(exdir, "dataglobal/material.cms"), errors="replace"):
        m = re.match(r'"(Copper|Aluminium)"\s+\S+\s+[\d.]+\s+[\d.]+\s+([\d.]+)', line)
        if m:
            rho[m.group(1)] = float(m.group(2))
        m = re.match(r'"(Polystyrene|Air)"\s+\d+\s+([\d.eE+-]+)', line)
        if m:
            rho[m.group(1)] = float(m.group(2))
    return rho


def f_mip(exdir):
    """Own MIP sampling fraction of the HCAL along the beam line, from datageom/tbhcal96hcal.geom: per layer type the
    thicknesses of the active scintillator, the passive plastic, the aluminium wrapper and air; the copper absorbers;
    the two aluminium boxes with a wall at each end (CCalG4Hcal.cc)."""
    lines = [l.split("#.")[0].strip() for l in open(os.path.join(exdir, "datageom/tbhcal96hcal.geom"))]
    lines = [l for l in lines if l]
    i = next(k for k, l in enumerate(lines) if l.startswith('"Aluminium"'))
    nbox, wall = int(lines[i].split()[1]), float(lines[i].split()[4])
    def layers(tag):
        k = next(k for k, l in enumerate(lines) if l.startswith(f'"{tag}"'))
        n = int(lines[k].split()[1])
        vals = " ".join(lines[k + 1:k + 1 + (n + 1) // 2]).split()
        return [int(vals[3 * j]) for j in range(n)]
    scnt, absr = layers("ScintillatorLayer"), layers("AbsorberLayer")
    k = next(k for k, l in enumerate(lines) if l.startswith('"Copper"'))
    cu_half = [float(x) for x in lines[k].split()[3:]]
    k = next(k for k, l in enumerate(lines) if l.startswith('"Scintillator"'))
    types = [[float(x) for x in lines[k + 1 + j].split()] for j in range(int(lines[k].split()[3]))]
    rho = materials(exdir)
    s = {"Copper": rho["Copper"] * DEDX["Copper"], "Aluminium": rho["Aluminium"] * DEDX["Aluminium"],
         "Scint": rho["Polystyrene"] * DEDX["Scint"], "Air": rho["Air"] * DEDX["Air"]}      # MeV/cm
    t = {"active": 0.0, "plastic": 0.0, "Aluminium": 2 * nbox * wall, "Air": 0.0, "Copper": 0.0}   # mm
    for ty in scnt:
        _, lay, wrap, fp, bp, sc = types[ty]
        t["active"] += 2 * sc
        t["plastic"] += 2 * fp + 2 * bp
        t["Aluminium"] += 4 * wrap
        t["Air"] += 2 * lay - 4 * wrap - 2 * fp - 2 * bp - 2 * sc
    for ty in absr:
        t["Copper"] += 2 * cu_half[ty]
    vis = t["active"] / 10 * s["Scint"]
    tot = vis + t["plastic"] / 10 * s["Scint"] + sum(t[m] / 10 * s[m] for m in ("Aluminium", "Air", "Copper"))
    print(f"HCAL along the beam: {len(scnt)} scintillator layers ({t['active']:.0f} mm active, {t['plastic']:.0f} mm "
          f"passive plastic; README: 189 mm of plastic in all), {t['Copper']:.0f} mm copper, {t['Aluminium']:.0f} mm "
          f"aluminium; MIP deposit {tot:.1f} MeV, of it {vis:.2f} MeV visible: own f_mip = {100 * vis / tot:.4f} %")
    # per-layer MIP weights: each scintillator layer samples the absorbers and box walls upstream of it (back to the
    # previous layer) and itself; global position = box offset + position in the box
    i = next(k for k, l in enumerate(lines) if l.startswith('"Aluminium"'))
    box_x = [float(x) for x in lines[i].split()[5:5 + nbox]]
    half_box = float(lines[i].split()[3])
    def pos(tag):
        k = next(k for k, l in enumerate(lines) if l.startswith(f'"{tag}"'))
        n = int(lines[k].split()[1])
        v = " ".join(lines[k + 1:k + 1 + (n + 1) // 2]).split()
        return [(int(v[3 * j]), int(v[3 * j + 1]), float(v[3 * j + 2])) for j in range(n)]
    gx = lambda mother, x: x + (box_x[mother] if 0 <= mother < nbox else 0.0)
    sl = [(gx(m, x), j, ty) for j, (ty, m, x) in enumerate(pos("ScintillatorLayer"))]
    ab = [(gx(m, x), 2 * cu_half[ty] / 10 * s["Copper"]) for ty, m, x in pos("AbsorberLayer")]
    walls = [(bx + sgn * (half_box - wall / 2), wall / 10 * s["Aluminium"]) for bx in box_x for sgn in (-1, 1)]
    sl.sort()
    w, prev, unsampled = [0.0] * len(sl), -1e9, 0.0
    for gxi, j, ty in sl:
        _, lay, wrap, fp, bp, sc = types[ty]
        own = (2 * sc + 2 * fp + 2 * bp) / 10 * s["Scint"] + 4 * wrap / 10 * s["Aluminium"]
        cell = own + sum(d for x, d in ab + walls if prev < x < gxi)
        w[j] = cell / (2 * sc / 10 * s["Scint"])
        prev = gxi
    unsampled = sum(d for x, d in ab + walls if x > prev)
    print(f"per-layer MIP weights (cell / visible): {min(w):.1f} to {max(w):.1f}; MIP deposit behind the last layer "
          f"(not sampled): {unsampled:.1f} MeV")
    return vis / tot, tot, t, rho, w


def scan(exdir, outdir):
    f, tot_mip, t, rho, w = f_mip(exdir)
    # muons: visible = sum of EHDC; all deposits = sum over the lateral-profile histograms h500-h569 of their sum of
    # fills (fTsumwx counts in-range fills only, so the overflow must be empty)
    path = os.path.join(outdir, "mu_20", "ccal.root")
    fr = uproot.open(path)
    a = ntuple(path)
    hs = [fr[f"h{500 + i}"] for i in range(70)]
    tot = sum(h.member("fTsumwx") for h in hs)
    ovf = sum(h.values(flow=True)[-1] for h in hs)
    fmu = a["EHDC"].sum() / tot
    print(f"muons (20 GeV, {len(a['EHDC'])} events): visible {1000 * a['EHDC'].mean():.2f} MeV, all deposits "
          f"{1000 * tot / len(a['EHDC']):.0f} MeV per event (lateral-profile overflow entries: {ovf:.0f}); "
          f"visible fraction {100 * fmu:.4f} %, mu/mip = {fmu / f:.3f}")
    # own estimate at 20 GeV: the mean ionization loss instead of the minimum (radiative losses not included)
    e_mu = 20000 + 105.6584
    sm = {m: rho[r] * bethe_mean(m, e_mu) for m, r in (("Copper", "Copper"), ("Aluminium", "Aluminium"),
                                                         ("Scint", "Polystyrene"), ("Air", "Air"))}
    vis20 = t["active"] / 10 * sm["Scint"]
    tot20 = vis20 + t["plastic"] / 10 * sm["Scint"] + sum(t[m] / 10 * sm[m] for m in ("Aluminium", "Air", "Copper"))
    print(f"own estimate at 20 GeV (mean ionization loss, Bethe with density effect): Cu {bethe_mean('Copper', e_mu):.3f}"
          f", plastic {bethe_mean('Scint', e_mu):.3f} MeV cm2/g ({100 * (bethe_mean('Copper', e_mu) / DEDX['Copper'] - 1):.0f}"
          f" % and {100 * (bethe_mean('Scint', e_mu) / DEDX['Scint'] - 1):.0f} % above the minimum); all deposits "
          f"{tot20:.0f} MeV (Geant4 {1000 * tot / len(a['EHDC']):.0f} MeV, ratio {1000 * tot / len(a['EHDC']) / tot20:.3f}), "
          f"visible fraction {100 * vis20 / tot20:.4f} % (Geant4 {100 * fmu:.4f} %, ratio {fmu / (vis20 / tot20):.3f})")
    res = {}
    for p in ("e", "pi"):
        for e in (20, 50, 100, 300):
            path = os.path.join(outdir, f"{p}_{e}", "ccal.root")
            if not os.path.exists(path):
                continue
            tr = uproot.open(path)["ntuple1"]
            lay = np.vstack([tr[f"hcal{j}"].array(library="np") for j in range(28)])
            v = (np.array(w)[:, None] * lay).sum(axis=0)          # energy at the MIP scale, GeV
            c, dc = core(v)
            med = float(np.median(v))
            res[(p, e)] = (v.mean(), med, c / med, dc / med, len(v), float(lay.sum(axis=0).mean()))
    for e in (20, 50, 100, 300):
        if ("e", e) in res and ("pi", e) in res:
            me, mp = res[("e", e)][0], res[("pi", e)][0]
            print(f"{e:3d} GeV: e/pi = {res[('e', e)][5] / res[('pi', e)][5]:.3f} from the plain sum of the layers, "
                  f"{me / mp:.3f} with own MIP weights per layer (e/mip {me / e:.3f}, pi/mip {mp / e:.3f}); "
                  f"sigma/E (core) e- {100 * res[('e', e)][2]:.2f} +- {100 * res[('e', e)][3]:.2f} %, pi- "
                  f"{100 * res[('pi', e)][2]:.2f} +- {100 * res[('pi', e)][3]:.2f} %")
    for p, name in (("e", "e-"), ("pi", "pi-")):
        pts = [(e, r[2], r[3]) for (q, e), r in sorted(res.items()) if q == p]
        if len(pts) >= 3:
            a2, b2, da, db, chi2 = fit(pts)
            print(f"fit {name}: sigma/E = a/sqrt(E) (+) b with a = {100 * a2:.1f} +- {100 * da:.1f} %, b = {100 * b2:.2f} "
                  f"+- {100 * db:.2f} % (chi2 = {chi2:.1f} for {len(pts) - 2} d.o.f.)")


def fit(pts):
    w = [1 / (2 * r * dr) ** 2 for _, r, dr in pts]
    x = [1 / e for e, _, _ in pts]
    y = [r * r for _, r, _ in pts]
    sw, sx, sy = sum(w), sum(wi * xi for wi, xi in zip(w, x)), sum(wi * yi for wi, yi in zip(w, y))
    sxx, sxy = sum(wi * xi * xi for wi, xi in zip(w, x)), sum(wi * xi * yi for wi, xi, yi in zip(w, x, y))
    det = sw * sxx - sx * sx
    a2, b2 = (sw * sxy - sx * sy) / det, (sxx * sy - sx * sxy) / det
    chi2 = sum(wi * (yi - a2 * xi - b2) ** 2 for wi, xi, yi in zip(w, x, y))
    a, b = math.sqrt(max(a2, 0)), math.sqrt(max(b2, 0))
    da = math.sqrt(sw / det) / (2 * a) if a > 0 else float("nan")
    db = math.sqrt(sxx / det) / (2 * b) if b > 0 else float("nan")
    return a, b, da, db, chi2


if __name__ == "__main__":
    {"dist": dist, "scan": scan}[sys.argv[1]](*sys.argv[2:])
