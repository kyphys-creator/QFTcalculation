"""Stage 3 of the EFT and dark-matter tools (environment.pdf), MadDM's continuum indirect detection at tree level: the sigma v of
each channel of real scalar dark matter with a Higgs portal (the model of run_stage3.sh, unitary gauge), against own formulas.

Own sigma v_rel (CM frame, as test_maddm.py; v = (sqrt2 G_F)^-1/2 of the UFO, Yukawa masses ym_f in the couplings and m_f in the
kinematics, the Higgs width in the s-channel propagator D = s - m_h^2 + i m_h Gamma_h):
  S S -> W W, Z Z, f fbar: 2 lam^2 v^2 Gamma(h* -> X; sqrt s)/(sqrt s |D|^2)        (test_maddm.Model.sigmav_cm);
  S S -> h h: contact (-i lam), s-channel h (h h h: -3 i m_h^2/v) and the t and u channels of S (h S S: -i lam v),
      M = -lam [1 + 3 m_h^2/D + lam v^2/(t - m_S^2) + lam v^2/(u - m_S^2)],
      t, u = m_S^2 + m_h^2 - s/2 -+ 2 p k cos(theta),
      sigma v_rel = beta_h/(16 pi s) (1/2) int_{-1}^{1} |M|^2 dcos(theta)   (1/2 of the identical Higgs bosons included).
MadDM's sigma v (maddm_run_interface.py, launch_indirect): sigma x 2 v x pb2cm3, sigma = MadEvent's cross section at
ebeam = m sqrt(1 + v^2), v = sqrt(3)/2 vave_indirect_cont (default 2e-5), pb2cm3 = 2.99e-26; own: sigma v_rel sqrt(1 + v^2) with
v_rel = 2 v/sqrt(1 + v^2) and MadEvent's GeV^-2 -> pb (389379.66e3).  MadEvent's sigma of each channel from its channel results
(Indirect_tree_cont/SubProcesses/P*/G*/results.dat, 5 digits: the bound printed is their rounding plus the MC error, and the
test allows 1e-6 more: at v = 1.7e-5 the momentum p = sqrt(E^2 - m^2) = m v of the beams loses about 1e-7..1e-6 in double precision)
and MadDM's printed values (3 digits); the total Total_xsec.
Usage: python3 test_maddm_id.py --collect M   (after the MadDM launch at m_S = M: copies the results to out/maddm_id/runs/mM)
       python3 test_maddm_id.py               (the comparison, over out/maddm_id/runs/m*)
"""
import json
import math
import re
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_maddm import Model, read_card  # noqa: E402

OUT = HERE / "out" / "maddm_id"
RUNS = OUT / "runs"
CONV = 389379.66e3                 # MadEvent's GeV^-2 -> pb (auto_dsig.f)
PB2CM3 = 2.99e-26
# MadDM's channel name -> the key of test_maddm.Model.gammas, or "hh"
CHANNELS = {"wpwm": "wpwm", "zz": "zz", "hh": "hh", "ttx": "t", "bbx": "b", "ccx": "c", "ssx": "s", "uux": "u", "ddx": "d",
            "tamtap": "tau", "mummup": "mu", "emep": "e"}


def sigmav_hh(md, s):
    """sigma v_rel [GeV^-2] of S S -> h h"""
    m, mh, lam, v = md.m, md.MH, md.lam, md.v
    if s <= 4 * mh**2:
        return 0.0
    p, k = math.sqrt(s / 4 - m * m), math.sqrt(s / 4 - mh * mh)
    D = complex(s - mh**2, mh * md.WH)
    c, w = np.polynomial.legendre.leggauss(64)
    t = m * m + mh * mh - s / 2 + 2 * p * k * c
    u = m * m + mh * mh - s / 2 - 2 * p * k * c
    M = -lam * (1 + 3 * mh**2 / D + lam * v * v / (t - m * m) + lam * v * v / (u - m * m))
    avg = 0.5 * np.sum(w * np.abs(M)**2)
    return math.sqrt(1 - 4 * mh**2 / s) / (16 * math.pi * s) * avg


def own_sigmav(md, ch, s):
    key = CHANNELS[ch]
    return sigmav_hh(md, s) if key == "hh" else md.sigmav_cm(s, key)


def velocity(card_text):
    """MadDM's v = sqrt(3)/2 vave_indirect_cont (launch_indirect)"""
    return math.sqrt(3) / 2 * float(re.search(r"^\s*(\S+)\s*=\s*vave_indirect_cont", card_text, re.M).group(1))


def collect(mass):
    """after the launch at m_S = mass: copy MadDM's results and MadEvent's channel results"""
    dest = RUNS / ("m%03d" % mass)
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    run = max((OUT / "output").glob("run_*"), key=lambda p: int(p.name.split("_")[1]))
    for name in ("MadDM_results.txt", "maddm_card.dat"):
        shutil.copy(run / name, dest / name)
    shutil.copy(OUT / "Cards" / "param_card.dat", dest / "param_card.dat")
    assert abs(read_card(dest / "param_card.dat")["ms0"] / mass - 1) < 1e-12, "the param_card is not at m_S = %s" % mass
    sub = OUT / "Indirect_tree_cont" / "SubProcesses"
    res = {"run": run.name, "madevent": {}}
    for ch in CHANNELS:
        pdir = next(p for p in sub.iterdir() if p.name.startswith("P") and p.name.endswith("_xsdmxsdm_" + ch))
        # the channels of symfact.dat and their factors, as MadEvent's sum_html.collect_result
        chans = []
        for line in (pdir / "symfact.dat").read_text().split("\n"):
            if line.strip() and int(line.split()[1]) > 0:
                x, e = map(float, (pdir / ("G" + line.split()[0]) / "results.dat").read_text().split()[:2])
                chans.append([int(line.split()[1]) * x, int(line.split()[1]) * e])
        res["madevent"][ch] = chans
    (dest / "collected.json").write_text(json.dumps(res, indent=1))
    print("collected m_S = %s GeV (%s)" % (mass, run.name))


def row(n, what, result, verdict):
    print(f"{n:2d}  {what:40s} {result:88s} {verdict}")


def main():
    print(f"{'':2s}  {'check':40s} {'result':88s} verdict")
    n = 0
    for dest in sorted(RUNS.glob("m*")):
        res = json.loads((dest / "collected.json").read_text())
        md = Model(read_card(dest / "param_card.dat"))
        v = velocity((dest / "maddm_card.dat").read_text())
        s = 4 * md.m**2 * (1 + v * v)
        text = (dest / "MadDM_results.txt").read_text()
        printed = {ch: float(re.search(r"xsdmxsdm_%s\s*=\s*\[([0-9.eE+-]+)" % ch, text).group(1)) for ch in CHANNELS}
        tot_own, rows, closed, closed_ok = 0.0, [], [], True
        for ch in CHANNELS:
            sig_own = own_sigmav(md, ch, s) / (2 * v / math.sqrt(1 + v * v)) * CONV       # pb
            sv_own = sig_own * 2 * v * PB2CM3
            tot_own += sv_own
            chans = res["madevent"][ch]
            x = sum(c[0] for c in chans)
            if sig_own == 0:
                closed.append(ch)
                closed_ok = closed_ok and x == 0 and printed[ch] == 0
                continue
            # the rounding of the 5-digit channel results, and their MC error
            bound = (sum(0.5e-4 * 10**math.floor(math.log10(abs(c[0]))) for c in chans if c[0])
                     + math.sqrt(sum(c[1]**2 for c in chans))) / sig_own
            rows.append((ch, x / sig_own - 1, bound, printed[ch] / sv_own - 1))
        worst = max(rows, key=lambda r: abs(r[1]) - r[2])
        worst_p = max(rows, key=lambda r: abs(r[3]))
        main_ch = max(CHANNELS, key=lambda ch: printed[ch])
        n += 1
        row(n, f"m_S = {md.m:g}: MadEvent sigma per channel",
            f"{len(rows)} open channels, closest to its bound: {worst[0]} {worst[1]:+.1e} (bound {worst[2]:.1e}); "
            f"closed: {' '.join(closed) or '-'} (0)",
            "agree" if closed_ok and all(abs(d) <= b + 1e-6 for _, d, b, _ in rows) else "see text")
        n += 1
        row(n, "   MadDM printed sigma v per channel",
            f"largest {worst_p[3]:+.1e} ({worst_p[0]}); {main_ch} {printed[main_ch]:.2e} cm^3/s",
            "agree" if abs(worst_p[3]) < 5e-3 else "see text")
        tot = float(re.search(r"Total_xsec\s*=\s*\[([0-9.eE+-]+)", text).group(1))
        n += 1
        shares = ", ".join(f"{ch} {100 * own_sigmav(md, ch, s) / sum(own_sigmav(md, c, s) for c in CHANNELS):.2f} %"
                           for ch in sorted(CHANNELS, key=lambda c: -own_sigmav(md, c, s))[:3])
        row(n, "   Total_xsec", f"own {tot_own:.5e} cm^3/s, MadDM {tot:.2e} ({tot / tot_own - 1:+.1e}); {shares}",
            "agree" if abs(tot / tot_own - 1) < 5e-3 else "see text")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--collect":
        collect(float(sys.argv[2]))
    else:
        main()
