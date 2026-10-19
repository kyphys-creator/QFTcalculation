"""Stage 2 of the LHC tools (environment.pdf): Pythia 8 and HepMC 2 through MG5 (the runs of run_stage2.sh in out/).

  shower:   p p -> e+ e- showered by Pythia 8.  Pythia's cross section against the LHE one (no matching: every event is kept);
            in every HepMC event, the sum of the final-state (status 1) four-momenta against (0, 0, 0, sqrt s), the charge
            against +2 and the baryon number against 2 (the charges and baryon numbers from the PDG codes: quark digits of
            the hadrons, a table for the leptons and bosons).
  matching: MLM matching of p p -> e+ e- + 0, 1, 2 jets: xqcut = 15, 20, 30 GeV with NNPDF4.0 (runs 1-3) and xqcut = 20 GeV
            with MG5's internal nn23lo1 (run 4, the LO set of Pythia's default ISR PDF), qCut = 1.5 xqcut.  MG5 3.8.1 showers
            with Pythia's own main164 in parallel jobs (not MG5aMC_PY8_interface) and writes no DJR histograms.  So:
            (i) the matched cross section: MG5's value against sigma_LHE sum(n_acc)/sum(n_try) from all the Pythia::stat tables
                of the log, with the acceptance per jet multiplicity (the user classification codes 0, 1, 2);
            (ii) own DJRs: each run's LHE split by its number of final-state partons, showered again by main164 at parton
                level (MPI, beam remnants and hadronization off, the same JetMatching settings), and the final-state partons
                clustered by own exclusive kT algorithm with R = 1 (d_ij = min(pT_i^2, pT_j^2) dR^2, d_iB = pT_i^2, E-scheme);
            (iii) the matching's own DJRs: MG5aMC_PY8_interface run directly on the LHE (getDJR of JetMatchingMadgraph), the
                same parton-level settings; own against these bin by bin (chi^2 per bin of the summed histograms);
            (iv) the smoothness at qCut: log of the summed histogram fitted by a line on each side (0.06 to 0.36 from
                log10 qCut), the ratio of the two lines at log10 qCut ("step"; 1 if smooth);
            (v) the consistency of the shower with the matrix elements: MG5 does not pass its PDF to Pythia, whose ISR
                uses its default NNPDF2.3 LO; run 2 again through the interface with PDF:pSet = LHAPDF6:NNPDF40_nlo_as_01180,
                and with that and the shower alpha_s = 0.118 at two loops.
Usage: python3 test_pythia.py [shower | matching]
"""
import gzip
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SQRTS = 13000.0
QCH = {1: -1, 2: 2, 3: -1, 4: 2, 5: -1, 6: 2}          # three times the quark charges
LEPTON = {11: -3, 13: -3, 15: -3, 12: 0, 14: 0, 16: 0}   # three times the charges
BOSON = {21: 0, 22: 0, 23: 0, 25: 0, 24: 3}


def charge3(pid):
    """three times the charge of a particle from its PDG code"""
    a, s = abs(pid), (1 if pid > 0 else -1)
    if a in LEPTON:
        return s * LEPTON[a]
    if a in BOSON:
        return s * BOSON[a]
    if a in QCH:
        return s * QCH[a]
    q1, q2, q3 = (a // 1000) % 10, (a // 100) % 10, (a // 10) % 10
    if q1 == 0:                                            # meson q2 q3bar: the heavier q2 down-type means it is the antiquark
        c = QCH[q2] - QCH[q3]
        return s * (-c if q2 % 2 == 1 else c)
    return s * (QCH[q1] + QCH[q2] + QCH[q3])               # baryon (or diquark)


def baryon3(pid):
    """three times the baryon number"""
    a, s = abs(pid), (1 if pid > 0 else -1)
    if a in QCH:
        return s
    if a < 100:
        return 0
    return 3 * s if (a // 1000) % 10 else 0


def hepmc_events(path):
    """yield the status-1 particles (pid, px, py, pz, e) of each event of a HepMC 2 file"""
    fs, started = [], False
    with gzip.open(path, "rt") if str(path).endswith(".gz") else open(path) as fh:
        for line in fh:
            if line.startswith("E "):
                if started:
                    yield fs
                fs, started = [], True
            elif line.startswith("P "):
                f = line.split()
                if int(f[8]) == 1:
                    fs.append((int(f[2]), float(f[3]), float(f[4]), float(f[5]), float(f[6])))
    if started:
        yield fs


def run_dir(proc, run):
    return OUT / proc / "Events" / run


def lhe_sigma(proc, run):
    banner = sorted(run_dir(proc, run).glob("*banner.txt"))[-1].read_text()
    return float(re.search(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)", banner).group(1))


def py8_inclusive(log):
    """the 'Inclusive cross section' [pb] that main164 prints for each parallel job"""
    return [float(x) * 1e9 for x in re.findall(r"Inclusive cross section:\s+([0-9.eE+-]+)\s+\+-", Path(log).read_text())]


def py8_counts(log):
    """n_try, n_acc summed over all the Pythia::stat tables of a log, in total and per user classification code"""
    txt = Path(log).read_text()
    tot = [0, 0]
    for t, _, a in re.findall(r"\|\s*sum\s*\|\s*(\d+)\s+(\d+)\s+(\d+)\s*\|", txt):
        tot[0] += int(t); tot[1] += int(a)
    per = {}
    for c, t, _, a in re.findall(r"user classification code\s+(\d+)\s*\|\s*(\d+)\s+(\d+)\s+(\d+)\s*\|", txt):
        x = per.setdefault(int(c), [0, 0]); x[0] += int(t); x[1] += int(a)
    return tot, per


def shower():
    rd = run_dir("shower_proc", "run_01")
    hep = sorted(rd.glob("*.hepmc*"))[-1]
    log = sorted(rd.glob("*pythia8*.log"))[-1]
    lhe = lhe_sigma("shower_proc", "run_01")
    inc = py8_inclusive(log)
    (n_try, n_acc), _ = py8_counts(log)
    print("(a) p p -> e+ e- showered by Pythia 8 (main164, %d parallel jobs): LHE %.6f pb;  Pythia's inclusive cross sections "
          "%.6f .. %.6f pb (max |Pythia/LHE - 1| = %.1e);  events tried %d, accepted %d"
          % (len(inc), lhe, min(inc), max(inc), max(abs(x / lhe - 1) for x in inc), n_try, n_acc))
    n, dmax, charges, baryons, nfs = 0, 0.0, set(), set(), 0
    for fs in hepmc_events(hep):
        n += 1
        nfs += len(fs)
        p = [sum(x[i] for x in fs) for i in (1, 2, 3, 4)]
        dmax = max(dmax, max(abs(p[0]), abs(p[1]), abs(p[2]), abs(p[3] - SQRTS)) / SQRTS)
        charges.add(sum(charge3(x[0]) for x in fs))
        baryons.add(sum(baryon3(x[0]) for x in fs))
    print("    %d HepMC events (%s), %.0f final-state particles per event;  max |sum p - (0, 0, 0, sqrt s)|/sqrt s = %.1e;"
          "  charges %s (expect {+2}), baryon numbers %s (expect {2})"
          % (n, hep.name, nfs / n, dmax, sorted(c / 3 for c in charges), sorted(b / 3 for b in baryons)))


# ---------------------------------------------------------------------------------------------------- the DJRs
MAIN164 = Path.home() / "hep/MG5_aMC_v3_8_1/HEPTools/pythia8/share/Pythia8/examples/main164"
IFACE = Path.home() / "hep/MG5_aMC_v3_8_1/HEPTools/MG5aMC_PY8_interface/MG5aMC_PY8_interface"
RUNS = (("run_01", 15, "NNPDF4.0"), ("run_02", 20, "NNPDF4.0"), ("run_03", 30, "NNPDF4.0"), ("run_04", 20, "nn23lo1"))
EDGES = [0.03 * k for k in range(101)]          # the interface's binning of log10 sqrt(d)
PARTON = ["PartonLevel:MPI = off", "HadronLevel:all = off", "Next:numberCount = 0", "Next:numberShowEvent = 0",
          "Next:numberShowInfo = 0", "Next:numberShowProcess = 0"]


def mg5_lines(mg5_cmd, skip):
    return [l for l in Path(mg5_cmd).read_text().splitlines()
            if l.strip() and not l.strip().startswith("!") and l.split("=")[0].strip() not in skip]


def split_lhe(src, dst_prefix):
    """split an LHE file by the number of final-state partons (status 1, |id| <= 5 or 21); returns {n: (path, count)}, total"""
    text = gzip.open(src, "rt").read()
    i0 = text.index("<event")
    header, body = text[:i0], text[i0:]
    events = re.findall(r"<event.*?</event>", body, re.S)
    out = {}
    for ev in events:
        n = 0
        for line in ev.splitlines()[2:]:
            f = line.split()
            if len(f) >= 13 and f[1] == "1" and (abs(int(f[0])) <= 5 or f[0] == "21"):
                n += 1
        out.setdefault(n, []).append(ev)
    res = {}
    for n, evs in out.items():
        p = Path("%s_n%d.lhe" % (dst_prefix, n))
        p.write_text(header + "\n".join(evs) + "\n</LesHouchesEvents>\n")
        res[n] = (p, len(evs))
    return res, len(events), header + body


def kt_djr(parts):
    """exclusive kT clustering with R = 1 (E-scheme); returns sqrt(d) of the steps n+1 -> n for n = 0, 1, 2 (d01, d12, d23)"""
    import numpy as np
    if not parts:
        return [None, None, None]
    p = np.array(parts, dtype=float)           # px, py, pz, e
    res = {}
    while len(p):
        pt2 = p[:, 0]**2 + p[:, 1]**2
        y = 0.5 * np.log(np.maximum(p[:, 3] + p[:, 2], 1e-300) / np.maximum(p[:, 3] - p[:, 2], 1e-300))
        phi = np.arctan2(p[:, 1], p[:, 0])
        n = len(p)
        if n > 1:
            dphi = np.abs(phi[:, None] - phi[None, :])
            dphi = np.minimum(dphi, 2 * np.pi - dphi)
            dij = np.minimum(pt2[:, None], pt2[None, :]) * ((y[:, None] - y[None, :])**2 + dphi**2)
            dij[np.diag_indices(n)] = np.inf
            i, j = divmod(int(np.argmin(dij)), n)
            dmin_ij = dij[i, j]
        else:
            dmin_ij = np.inf
        ib = int(np.argmin(pt2))
        if n - 1 <= 2:
            res[n - 1] = math.sqrt(min(dmin_ij, pt2[ib]))
        if dmin_ij < pt2[ib]:
            p[i] = p[i] + p[j]
            p = np.delete(p, j, axis=0)
        else:
            p = np.delete(p, ib, axis=0)
    return [res.get(k) for k in (0, 1, 2)]


def hepmc_partons(path):
    for fs in hepmc_events(path):
        yield [x[1:] for x in fs if abs(x[0]) <= 5 or x[0] == 21]


def read_djrs(path):
    """the interface's djrs.dat: {(njet, 'd01'): (content, error)} in pb per bin"""
    import numpy as np
    txt = Path(path).read_text()
    out = {}
    for nj, block in re.findall(r'<jethistograms njet="(\d)">(.*?)</jethistograms>', txt, re.S):
        for name, body in re.findall(r'<histogram name="log10(d\d\d)"[^>]*>(.*?)</histogram>', block, re.S):
            a = np.array([[float(x) for x in l.split()] for l in body.strip().splitlines()])
            out[(int(nj), name)] = (a[:, 2] * 1e9, a[:, 3] * 1e9)
    return out


def step(tot, err, q, gap=0.06, width=0.3):
    """ratio at q of the lines fitted to log(tot) on each side of q; returns step, its error"""
    import numpy as np
    e = np.array(EDGES)
    c = 0.5 * (e[1:] + e[:-1])
    fits = []
    for sel in ((c < q - gap) & (c > q - gap - width), (c > q + gap) & (c < q + gap + width)):
        m = sel & (tot > 0)
        x, y, s = c[m] - q, np.log(tot[m]), err[m] / tot[m]
        A = np.vstack([np.ones_like(x), x]).T / s[:, None]
        coef = np.linalg.lstsq(A, y / s, rcond=None)[0]
        fits.append((coef[0], math.sqrt(np.linalg.inv(A.T @ A)[0, 0])))
    r = math.exp(fits[1][0] - fits[0][0])
    return r, r * math.hypot(fits[0][1], fits[1][1])


def matching():
    import numpy as np
    from concurrent.futures import ThreadPoolExecutor
    import subprocess
    mg = [(float(a), float(b)) for a, b in re.findall(r"Matched cross-section :\s+([0-9.eE+-]+)\s+\+-\s+([0-9.eE+-]+)\s+pb",
                                                       (OUT / "mlm.log").read_text())]
    print("(b) MLM matching of p p -> e+ e- + 0, 1, 2 jets (qCut = 1.5 xqcut), MG5's showers (MPI and hadronization on)")
    for (run, xq, pdf), (msig, merr) in zip(RUNS, mg):
        log = sorted(run_dir("mlm_proc", run).glob("*pythia8*.log"))[-1]
        (n_try, n_acc), per = py8_counts(log)
        lhe = lhe_sigma("mlm_proc", run)
        print("  %s xqcut %2d: LHE %.2f pb;  MG5 matched %.2f +- %.2f pb;  own sigma_LHE n_acc/n_try = %.2f pb (%d/%d);  "
              "acceptance %s" % (pdf, xq, lhe, msig, merr, lhe * n_acc / n_try, n_acc, n_try,
                                 ", ".join("%dj %.3f" % (c, a / t) for c, (t, a) in sorted(per.items()))))
    nn = [m for (_, _, pdf), (m, _) in zip(RUNS, mg) if pdf == "NNPDF4.0"]
    print("  NNPDF4.0: the matched cross section over xqcut 15, 20, 30 GeV: %s pb (spread %.1f%% of the middle one)"
          % (", ".join("%.0f" % m for m in nn), 100 * (max(nn) - min(nn)) / nn[1]))
    djr = OUT / "djr"
    djr.mkdir(exist_ok=True)
    jobs, meta = [], {}
    for run, xq, pdf in RUNS:
        rd = run_dir("mlm_proc", run)
        parts, ntot, full = split_lhe(rd / "unweighted_events.lhe.gz", str(djr / run))
        meta[run] = (ntot, {n: c for n, (p, c) in parts.items()})
        base = mg5_lines(rd / "tag_1_pythia8.cmd", {"Main:HepMC", "HepMC:output", "Main:subrun", "Beams:LHEF",
                                                     "Main:numberOfEvents"})
        for n, (p, c) in parts.items():      # main164 refuses Main:numberOfEvents = -1 (MG5 fills in the count)
            hep = djr / ("%s_n%d.hepmc" % (run, n))
            cmd = djr / ("%s_n%d.cmnd" % (run, n))
            cmd.write_text("\n".join(base + PARTON + ["PartonLevel:Remnants = off", "Check:event = off", "Main:HepMC = on",
                                                      "HepMC:output = %s" % hep, "Main:numberOfEvents = %d" % c,
                                                      "Beams:LHEF = %s" % p]) + "\n")
            jobs.append(([str(MAIN164), "-c", str(cmd)], str(hep) + ".log"))
        lhe = djr / ("%s_full.lhe" % run)
        lhe.write_text(full)
        cmd = djr / ("%s_iface.cmnd" % run)
        cmd.write_text("\n".join(base + PARTON + ["Main:numberOfEvents = %d" % ntot, "HEPMCoutput:file = void",
                                                  "HistFile:name = %s_" % run, "LHEFInputs:nSubruns = 1", "Main:subrun = 0",
                                                  "Beams:LHEF = %s" % lhe]) + "\n")
        jobs.append(([str(IFACE), str(cmd)], str(djr / ("%s_iface.log" % run))))

    def go(job):
        args, log = job
        with open(log, "w") as fh:
            subprocess.run(args, cwd=djr, stdout=fh, stderr=subprocess.STDOUT, check=True)

    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(go, jobs))
    print("  DJRs at parton level (MPI, hadronization off): own (main164 reshowers, own kT) and the matching's own "
          "(MG5aMC_PY8_interface); step = ratio at qCut of the lines fitted on each side (1 if smooth)")
    for run, xq, pdf in RUNS:
        ntot, counts = meta[run]
        lhe = lhe_sigma("mlm_proc", run)
        w = lhe / ntot
        q = math.log10(1.5 * xq)
        own = {k: np.zeros(100) for k in (0, 1)}
        nacc = 0
        for n in counts:
            for ev in hepmc_partons(djr / ("%s_n%d.hepmc" % (run, n))):
                nacc += 1
                d = kt_djr(ev)
                for k in (0, 1):
                    if d[k]:
                        b = int(math.log10(d[k]) / 0.03)
                        if 0 <= b < 100:
                            own[k][b] += w
        it = read_djrs(djr / ("%s_djrs.dat" % run))
        isig = float(re.findall(r"Inclusive cross section:\s+([0-9.eE+-]+)", (djr / ("%s_iface.log" % run)).read_text())[-1]) * 1e9
        print("  %s xqcut %2d (log10 qCut %.3f): matched, own %.2f pb, interface %.2f pb" % (pdf, xq, q, w * nacc, isig))
        for k, name in ((0, "d01"), (1, "d12")):
            tot = sum(it[(n, name)][0] for n in (0, 1, 2))
            err = np.sqrt(sum(it[(n, name)][1]**2 for n in (0, 1, 2)))
            eo = np.sqrt(np.maximum(own[k] * w, w * w))
            m = (tot > 0) | (own[k] > 0)
            chi2 = float((((own[k] - tot)**2) / (eo**2 + err**2))[m].sum())
            r_i, dr_i = step(tot, err, q)
            r_o, dr_o = step(own[k], eo, q)
            print("    %s: own against interface chi^2/bins = %.0f/%d;  step: interface %.3f +- %.3f, own %.3f +- %.3f"
                  % (name, chi2, int(m.sum()), r_i, dr_i, r_o, dr_o))
    print("  run 2 (NNPDF4.0, xqcut 20) through the interface with the shower made consistent with the matrix elements")
    base = (djr / "run_02_iface.cmnd").read_text().splitlines()
    for tag, extra in (("pdf", ["PDF:pSet = LHAPDF6:NNPDF40_nlo_as_01180"]),
                       ("pdfas", ["PDF:pSet = LHAPDF6:NNPDF40_nlo_as_01180", "SpaceShower:alphaSvalue = 0.118",
                                  "TimeShower:alphaSvalue = 0.118", "SpaceShower:alphaSorder = 2", "TimeShower:alphaSorder = 2"])):
        lines = [l.replace("HistFile:name = run_02_", "HistFile:name = run_02%s_" % tag) for l in base]
        i = lines.index("LHEFInputs:nSubruns = 1")
        lines[i:i] = extra
        cmd = djr / ("run_02%s_iface.cmnd" % tag)
        cmd.write_text("\n".join(lines) + "\n")
        go(([str(IFACE), str(cmd)], str(djr / ("run_02%s_iface.log" % tag))))
        it = read_djrs(djr / ("run_02%s_djrs.dat" % tag))
        res = []
        for name in ("d01", "d12"):
            tot = sum(it[(n, name)][0] for n in (0, 1, 2))
            err = np.sqrt(sum(it[(n, name)][1]**2 for n in (0, 1, 2)))
            res.append("%s step %.3f +- %.3f" % ((name,) + step(tot, err, math.log10(30.0))))
        print("    %-58s %s" % ("Pythia's PDF NNPDF4.0" if tag == "pdf" else "Pythia's PDF NNPDF4.0, shower alpha_s 0.118 (2 loops)",
                                 ";  ".join(res)))


if __name__ == "__main__":
    for w in sys.argv[1:] or ["shower", "matching"]:
        {"shower": shower, "matching": matching}[w]()
