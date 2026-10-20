"""Stage 2 of the LHC tools (environment.pdf): Pythia 8 and HepMC 2 through MG5 (the runs of run_stage2.sh in out/).

  shower:   p p -> e+ e- showered by Pythia 8.  Pythia's cross section against the LHE one (no matching: every event is kept);
            in every HepMC event, the sum of the final-state (status 1) four-momenta against (0, 0, 0, sqrt s), the charge
            against +2 and the baryon number against 2 (the charges and baryon numbers from the PDG codes: quark digits of
            the hadrons, a table for the leptons and bosons).
  matching: MLM matching of p p -> e+ e- + 0, 1, 2 jets, qCut = 1.5 xqcut.  MG5 does not pass its PDF to Pythia (whose ISR
            then uses its default NNPDF2.3 LO): runs 1-3 (NNPDF4.0 matrix elements, xqcut = 15, 20, 30 GeV) and run 4 (MG5's
            internal nn23lo1, xqcut 20) keep MG5's default; runs 5-7 (xqcut 15, 20, 30) set Pythia's PDF to the matrix
            elements' (PDF:pSet = LHAPDF6:NNPDF40_nlo_as_01180), and run 8 repeats run 6 with 200000 events.  MG5 3.8.1
            showers with Pythia's own main164 in parallel jobs (not MG5aMC_PY8_interface) and writes no DJR histograms.  So:
            (i) the matched cross section: MG5's value against sigma_LHE sum(n_acc)/sum(n_try) from all the Pythia::stat tables
                of the log, the acceptance per jet multiplicity, and the spread over xqcut (the merging-scale uncertainty);
            (ii) the DJRs of MG5aMC_PY8_interface run directly on each LHE (parton level: MPI and hadronization off).  Its DJR
                is not the matching's internal measure: SlowJet kT with R = 0.4 on the final-state coloured particles (beam
                remnants included) with |eta| < 4.4, as in its source;
            (iii) own DJRs of the same definition: each LHE split by its number of partons, showered again by main164 with the
                same settings, the final-state coloured partons (quarks, gluons, diquarks) with |eta| < 4.4 clustered by own
                exclusive kT algorithm (d_ij = min(pT_i^2, pT_j^2) dR^2/R^2 with dR in (y, phi), d_iB = pT_i^2, E-scheme);
                own against the interface bin by bin (chi^2 of the summed histograms);
            (iv) the smoothness at qCut: log of the summed histogram over |x| < 0.36 (x = log10 sqrt(d) - log10 qCut) fitted
                by a quadratic in x plus a step s theta(x); "step" = exp(s), 1 if smooth.  The same fit at log10 qCut -+ 0.45,
                where no boundary is, checks the method ("control", 1 expected);
            (v) run 6 again through the interface with the shower alpha_s = 0.118 at two loops as well;
            (vi) run 8 (200000 events, xqcut 20) again through the interface with qCut = 25 and 40 GeV, and with the
                shower-kT scheme (JetMatching:doShowerKt = on, qCut 30).
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
RUNS = (("run_01", 15, "NNPDF4.0, Pythia's default PDF", 1), ("run_02", 20, "NNPDF4.0, Pythia's default PDF", 1),
        ("run_03", 30, "NNPDF4.0, Pythia's default PDF", 1), ("run_04", 20, "nn23lo1 (= Pythia's default PDF)", 1),
        ("run_05", 15, "NNPDF4.0 in both", 1), ("run_06", 20, "NNPDF4.0 in both", 1), ("run_07", 30, "NNPDF4.0 in both", 1),
        ("run_08", 20, "NNPDF4.0 in both, 200000 events", 0))       # last: 1 = own reshower and DJRs too
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


def kt_djr(parts, R=0.4, etamax=4.4):
    """exclusive kT clustering (E-scheme) of the particles with |eta| < etamax; returns sqrt(d) of the steps n+1 -> n for
    n = 0, 1, 2 (d01, d12, d23), None where the event has fewer objects.  d_ij = min(pT_i^2, pT_j^2) dR^2/R^2, d_iB = pT_i^2"""
    import numpy as np
    sel = []
    for px, py, pz, e in parts:
        pp = math.sqrt(px * px + py * py + pz * pz)
        if pp - abs(pz) <= 0:
            continue
        if abs(0.5 * math.log((pp + pz) / (pp - pz))) < etamax:
            sel.append((px, py, pz, e))
    if not sel:
        return [None, None, None]
    p = np.array(sel, dtype=float)
    res = {}
    while len(p):
        pt2 = p[:, 0]**2 + p[:, 1]**2
        y = 0.5 * np.log(np.maximum(p[:, 3] + p[:, 2], 1e-300) / np.maximum(p[:, 3] - p[:, 2], 1e-300))
        phi = np.arctan2(p[:, 1], p[:, 0])
        n = len(p)
        if n > 1:
            dphi = np.abs(phi[:, None] - phi[None, :])
            dphi = np.minimum(dphi, 2 * np.pi - dphi)
            dij = np.minimum(pt2[:, None], pt2[None, :]) * ((y[:, None] - y[None, :])**2 + dphi**2) / R**2
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


def coloured(pid):
    """quarks, gluons and diquarks (the coloured final-state partons of a parton-level event, beam remnants included)"""
    a = abs(pid)
    return a <= 6 or a == 21 or (1000 <= a < 10000 and (a // 10) % 10 == 0)


def hepmc_partons(path):
    for fs in hepmc_events(path):
        yield [x[1:] for x in fs if coloured(x[0])]


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


def step(tot, err, q, half=0.36):
    """log tot = a + b x + c x^2 + s theta(x) over |x| < half, x = c - q; returns exp(s) and its error"""
    import numpy as np
    e = np.array(EDGES)
    x = 0.5 * (e[1:] + e[:-1]) - q
    m = (np.abs(x) < half) & (tot > 0)
    X = np.vstack([np.ones(m.sum()), x[m], x[m]**2, (x[m] > 0).astype(float)]).T
    sig = err[m] / tot[m]
    A = X / sig[:, None]
    coef = np.linalg.lstsq(A, np.log(tot[m]) / sig, rcond=None)[0]
    r = math.exp(coef[3])
    return r, r * math.sqrt(np.linalg.inv(A.T @ A)[3, 3])


def steps(tot, err, q):
    """the step at q and the two controls at q -+ 0.45"""
    return [step(tot, err, q + dq) for dq in (0.0, -0.45, 0.45)]


def fmt_steps(st):
    return "%.3f +- %.3f (control %.3f +- %.3f, %.3f +- %.3f)" % (st[0] + st[1] + st[2])


def matching():
    import numpy as np
    from concurrent.futures import ThreadPoolExecutor
    import subprocess
    mg = [(float(a), float(b)) for a, b in re.findall(r"Matched cross-section :\s+([0-9.eE+-]+)\s+\+-\s+([0-9.eE+-]+)\s+pb",
                                                       (OUT / "mlm.log").read_text())]
    print("(b) MLM matching of p p -> e+ e- + 0, 1, 2 jets (qCut = 1.5 xqcut), MG5's showers (MPI and hadronization on)")
    msig = {}
    for (run, xq, pdf, _), (m, merr) in zip(RUNS, mg):
        log = sorted(run_dir("mlm_proc", run).glob("*pythia8*.log"))[-1]
        (n_try, n_acc), per = py8_counts(log)
        lhe = lhe_sigma("mlm_proc", run)
        own = lhe * n_acc / n_try
        msig[run] = (own, own * math.sqrt((1 - n_acc / n_try) / n_acc))
        print("  %s %s xqcut %2d: LHE %.2f pb;  MG5 matched %.2f +- %.2f pb;  own sigma_LHE n_acc/n_try = %.2f pb (%d/%d);  "
              "acceptance %s" % (run, pdf, xq, lhe, m, merr, own, n_acc, n_try,
                                 ", ".join("%dj %.3f" % (c, a / t) for c, (t, a) in sorted(per.items()))))
    for label, runs in (("Pythia's default PDF", ("run_01", "run_02", "run_03")), ("NNPDF4.0 in both", ("run_05", "run_06", "run_07"))):
        v = [msig[r][0] for r in runs]
        print("  %s: the matched cross section over xqcut 15, 20, 30 GeV: %s pb;  spread (max - min)/middle = %.1f%%"
              % (label, ", ".join("%.1f +- %.1f" % msig[r] for r in runs), 100 * (max(v) - min(v)) / v[1]))
    djr = OUT / "djr"
    djr.mkdir(exist_ok=True)
    jobs, meta = [], {}
    skip = {"Main:HepMC", "HepMC:output", "Main:subrun", "Beams:LHEF", "Main:numberOfEvents"}
    for run, xq, pdf, doown in RUNS:
        rd = run_dir("mlm_proc", run)
        parts, ntot, full = split_lhe(rd / "unweighted_events.lhe.gz", str(djr / run))
        meta[run] = (ntot, {n: c for n, (p, c) in parts.items()})
        base = mg5_lines(rd / "tag_1_pythia8.cmd", skip)
        if doown:                            # main164 refuses Main:numberOfEvents = -1 (MG5 fills in the count)
            for n, (p, c) in parts.items():
                hep = djr / ("%s_n%d.hepmc" % (run, n))
                cmd = djr / ("%s_n%d.cmnd" % (run, n))
                cmd.write_text("\n".join(base + PARTON + ["Main:HepMC = on", "HepMC:output = %s" % hep,
                                                          "Main:numberOfEvents = %d" % c, "Beams:LHEF = %s" % p]) + "\n")
                jobs.append(([str(MAIN164), "-c", str(cmd)], str(hep) + ".log"))
        lhe = djr / ("%s_full.lhe" % run)
        lhe.write_text(full)
        variants = [("", [])]
        if run == "run_06":
            variants.append(("as", ["SpaceShower:alphaSvalue = 0.118", "TimeShower:alphaSvalue = 0.118",
                                    "SpaceShower:alphaSorder = 2", "TimeShower:alphaSorder = 2"]))
        if run == "run_08":
            variants += [("q25", ["JetMatching:qCut = 25.0"]), ("q40", ["JetMatching:qCut = 40.0"]),
                         ("skt", ["JetMatching:doShowerKt = on"])]
        for tag, add in variants:
            keys = {a.split("=")[0].strip() for a in add}
            b0 = [l for l in base if l.split("=")[0].strip() not in keys]
            cmd = djr / ("%s%s_iface.cmnd" % (run, tag))
            cmd.write_text("\n".join(b0 + PARTON + add + ["Main:numberOfEvents = %d" % ntot, "HEPMCoutput:file = void",
                                                            "HistFile:name = %s%s_" % (run, tag), "LHEFInputs:nSubruns = 1",
                                                            "Main:subrun = 0", "Beams:LHEF = %s" % lhe]) + "\n")
            jobs.append(([str(IFACE), str(cmd)], str(djr / ("%s%s_iface.log" % (run, tag)))))

    def go(job):
        args, log = job
        with open(log, "w") as fh:
            subprocess.run(args, cwd=djr, stdout=fh, stderr=subprocess.STDOUT, check=True)

    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(go, jobs))

    def sums(it, name):
        return (sum(it[(n, name)][0] for n in (0, 1, 2) if (n, name) in it),
                np.sqrt(sum(it[(n, name)][1]**2 for n in (0, 1, 2) if (n, name) in it)))

    print("  DJRs at parton level (MPI, hadronization off) of MG5aMC_PY8_interface (SlowJet kT, R = 0.4, |eta| < 4.4) and own of "
          "the same definition; step = exp(s) of log N = quadratic + s theta(x) around qCut (1 if smooth)")
    for run, xq, pdf, doown in RUNS:
        ntot, counts = meta[run]
        w = lhe_sigma("mlm_proc", run) / ntot
        q = math.log10(1.5 * xq)
        it = read_djrs(djr / ("%s_djrs.dat" % run))
        own = {k: np.zeros(100) for k in (0, 1)}
        nacc = 0
        if doown:
            for n in counts:
                for ev in hepmc_partons(djr / ("%s_n%d.hepmc" % (run, n))):
                    nacc += 1
                    d = kt_djr(ev)
                    for k in (0, 1):
                        if d[k]:
                            b = int(math.log10(d[k]) / 0.03)
                            if 0 <= b < 100:
                                own[k][b] += w
        isig = float(re.findall(r"Inclusive cross section:\s+([0-9.eE+-]+)",
                                (djr / ("%s_iface.log" % run)).read_text())[-1]) * 1e9
        print("  %s %s xqcut %2d (log10 qCut %.3f): matched, interface %.2f pb%s"
              % (run, pdf, xq, q, isig, (", own reshower %.2f pb" % (w * nacc)) if doown else ""))
        for k, name in ((0, "d01"), (1, "d12")):
            tot, err = sums(it, name)
            line = "    %s: step %s (interface)" % (name, fmt_steps(steps(tot, err, q)))
            if doown:
                eo = np.sqrt(np.maximum(own[k] * w, w * w))
                m = (tot > 0) | (own[k] > 0)
                chi2 = float((((own[k] - tot)**2) / (eo**2 + err**2))[m].sum())
                r_o, dr_o = step(own[k], eo, q)
                line += ", %.3f +- %.3f (own);  own against interface chi^2/bins = %.0f/%d" % (r_o, dr_o, chi2, int(m.sum()))
            print(line)
        if run == "run_06":
            ita = read_djrs(djr / "run_06as_djrs.dat")
            res = ["%s step %.3f +- %.3f" % ((name,) + step(*sums(ita, name), q)) for name in ("d01", "d12")]
            print("    and with the shower alpha_s = 0.118 (2 loops): %s" % ";  ".join(res))
        if run == "run_08":
            for tag, qc, label in (("q25", 25.0, "qCut 25 GeV"), ("q40", 40.0, "qCut 40 GeV"),
                                   ("skt", 30.0, "the shower-kT scheme, qCut 30 GeV")):
                itv = read_djrs(djr / ("run_08%s_djrs.dat" % tag))
                sv = float(re.findall(r"Inclusive cross section:\s+([0-9.eE+-]+)",
                                      (djr / ("run_08%s_iface.log" % tag)).read_text())[-1]) * 1e9
                res = ["%s step %.3f +- %.3f" % ((name,) + step(*sums(itv, name), math.log10(qc))) for name in ("d01", "d12")]
                print("    with %-34s matched %.1f pb;  %s" % (label + ":", sv, ";  ".join(res)))


if __name__ == "__main__":
    for w in sys.argv[1:] or ["shower", "matching"]:
        {"shower": shower, "matching": matching}[w]()
