"""Stage 3 of the EFT and dark-matter tools (environment.pdf), MadDM's loop-induced lines: real scalar dark matter with a Higgs
portal, S S -> gamma gamma and Z gamma at one loop, with the NLO UFO of model/make_nlo_ufo.wl (FeynRules SM + SingletDM.fr in
Feynman gauge, NLOCT's R2 vertices and its on-shell h Z gamma counterterm), against the Higgs note's one-loop amplitudes.

Own result.  In Feynman gauge the one-loop S S -> V gamma (V = gamma, Z) has s-channel diagrams (h S S: -i lam v, then the loops of
h* -> V gamma) and contact diagrams (S S G+ G-: -i lam, then the G+ G- loops that h -> V gamma also has behind h G+ G-: -i M_H^2/v;
S S G0 G0 cannot reach a photon at one loop).  With B the G+ G- loops without their vertex, the two add up to
   (-i lam v) i/(s - M_H^2) (-i M_H^2/v) B + (-i lam) B = (-i lam v) i/(s - M_H^2) (-i s/v) B,
the s-channel amplitude with M_H^2 replaced by s in the h G+ G- vertex, i.e. the on-shell h -> V gamma amplitude of a Higgs boson
of mass sqrt(s) (no other loop of h -> V gamma contains M_H).  So, with Gamma_H = 0 (a width in the s-channel propagator alone would
replace M_H^2 by s + i M_H Gamma_H instead; the runs set WH = 0),
   sigma v_rel = 2 lam^2 v^2 Gamma(h* -> V gamma; sqrt s)/(sqrt s (s - M_H^2)^2),
   sum|M|^2   = lam^2 v^2 2 sqrt(s) Gamma(h* -> V gamma; sqrt s)/((s - M_H^2)^2 Phi_2 S),  Phi_2 = (1 - M_V^2/s)/(8 pi),
(S = 1/2 for gamma gamma) with the Higgs note's LO widths (the loop functions of models/sm_higgs/Src/loopind_widths.py, read from that
file; checked there against FeynCalc + Package-X in a general R_xi gauge and against MadLoop) at M_H -> sqrt(s), with the UFO's
param_card: alpha = 1/aEWM1, G_F, M_W from them, v = (sqrt2 G_F)^-1/2, the Yukawa masses ym_f in the h f f couplings and the masses
m_f in the loops (all nine charged fermions), no width in the loop propagators (MadLoop's default).  h -> Z gamma includes the
photon-Z mixing on the external photon (Higgs note, step (2)), which MadLoop takes from the UV vertex h Z gamma of the UFO.

Checks per mass point (run_stage3_line.sh calls this script with --collect after each MadDM launch: MadEvent and the standalone
check use the parameters compiled in at the launch, Source/param_card.inc):
  (a) MadLoop's |M|^2 in MadDM's own loop directories (Indirect_LI_line/SubProcesses/PV*: the standalone check, its check_sa.f
      edited to read the point from PS.input and mu_R from MU_R.input, as models/sm/Src/patch_check_sa.py, and restored; MadEvent's
      initialization edits READPS and NPSPOINTS of that file at each launch), "finite" = sum|M|^2/IDEN (IDEN = 2 for gamma gamma),
      at mu_R = 91.188 (the UFO's MU_R, which MadEvent keeps for the loops) and 1000 GeV, two scattering angles;
  (b) MadDM's sigma v = sigma x 2 v x pb2cm3, sigma: MadEvent's cross section at ebeam = m sqrt(1 + v^2), v = sqrt(3)/2
      vave_indirect_line, pb2cm3 = 2.99e-26 (maddm_run_interface.py, launch_indirect); own: sigma v_rel sqrt(1 + v^2) with the relative
      velocity v_rel = 2 v/sqrt(1 + v^2) and MadEvent's GeV^-2 -> pb (389379.66e3); MadEvent's per-process sigma from its channel
      results (G*/results.dat, 5 digits, with their MC error, which can be several times smaller than the spread of MadEvent's
      results: tolerance 2e-3) and the printed value (3 digits);
  (c) MadDM's pb2cm3 against c x 1 pb = 2.99792458e-26 cm^3/s.
Usage: python3 test_maddm_line.py --collect M   (after the MadDM launch at m_S = M: copies the results to out/maddm_line/runs/mM
                                                and runs the MadLoop checks)
       python3 test_maddm_line.py               (the comparison, over out/maddm_line/runs/m*)
"""
import ast
import cmath
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_maddm import read_card  # noqa: E402

OUT = HERE / "out" / "maddm_line"
RUNS = OUT / "runs"
QFT = HERE.parents[2]
NOTE = QFT / "models" / "sm_higgs" / "Src" / "loopind_widths.py"
CONV = 389379.66e3                 # MadEvent's GeV^-2 -> pb (auto_dsig.f)
PB2CM3, C_CMS = 2.99e-26, 2.99792458e10
MUS, ANGLES = (91.188, 1000.0), (0.7, 2.1)
PROCS = {"aa": "xsdmxsdm_aa", "az": "xsdmxsdm_az"}
# name, N_c, T3, Q, mass, Yukawa mass (param_card names, lower case)
FERM = [("t", 3, 0.5, 2 / 3, "mt", "ymt"), ("c", 3, 0.5, 2 / 3, "mc", "ymc"), ("u", 3, 0.5, 2 / 3, "mu", "ymup"),
        ("b", 3, -0.5, -1 / 3, "mb", "ymb"), ("s", 3, -0.5, -1 / 3, "ms", "yms"), ("d", 3, -0.5, -1 / 3, "md", "ymdo"),
        ("tau", 1, -0.5, -1, "mta", "ymtau"), ("mu", 1, -0.5, -1, "mmu", "ymm"), ("e", 1, -0.5, -1, "me", "yme")]


def note_functions(cw, s2):
    """the loop functions of the Higgs note's loopind_widths.py (f, g, A_1/2, A_1, I_1, I_2, A^Zgamma), with this card's c_W, s_W^2"""
    tree = ast.parse(NOTE.read_text())
    keep = [n for n in tree.body if isinstance(n, ast.FunctionDef)
            and n.name in ("f", "g", "a_half", "a_one", "i1", "i2", "azg_half", "azg_one")]
    ns = {"math": math, "cmath": cmath, "CW": cw, "S2": s2}
    exec(compile(ast.Module(body=keep, type_ignores=[]), str(NOTE), "exec"), ns)
    return ns


class Own:
    def __init__(self, card):
        c = card
        self.MZ, self.MH, self.WH = c["mz"], c["mh"], c["w25"]
        self.alpha, self.GF = 1 / c["aewm1"], c["gf"]
        self.MW = math.sqrt(self.MZ**2 / 2 + math.sqrt(self.MZ**4 / 4 - self.alpha * math.pi * self.MZ**2 / (self.GF * math.sqrt(2))))
        self.s2 = 1 - self.MW**2 / self.MZ**2
        self.cw = math.sqrt(1 - self.s2)
        self.v = 2 * self.MW * math.sqrt(self.s2) / math.sqrt(4 * math.pi * self.alpha)
        self.lam, self.m = c["lamhs"], c["ms0"]
        self.fn = note_functions(self.cw, self.s2)
        self.ferm = [(nc, t3, q, c[mk], c[yk]) for _, nc, t3, q, mk, yk in FERM]

    def amp(self, final, M):
        """the sum of Eq. (loop) (gamma gamma) or of the Z gamma form of the Higgs note at M_H -> M"""
        fn = self.fn
        if final == "aa":
            F = fn["a_one"](M**2 / (4 * self.MW**2))
            for nc, t3, q, m, ym in self.ferm:
                F += ym / m * nc * q**2 * fn["a_half"](M**2 / (4 * m**2))
            return F
        F = fn["azg_one"](4 * self.MW**2 / M**2, 4 * self.MW**2 / self.MZ**2)
        for nc, t3, q, m, ym in self.ferm:
            F += ym / m * nc * q * (2 * t3 - 4 * q * self.s2) / self.cw * fn["azg_half"](4 * m**2 / M**2, 4 * m**2 / self.MZ**2)
        return F

    def width(self, final, M):
        F = self.amp(final, M)
        if final == "aa":
            return self.alpha**2 * M**3 / (256 * math.pi**3 * self.v**2) * abs(F)**2
        return self.GF**2 * self.MW**2 * self.alpha * M**3 / (64 * math.pi**4) * (1 - self.MZ**2 / M**2)**3 * abs(F)**2

    def prop2(self, s):
        return (s - self.MH**2)**2 + self.MH**2 * self.WH**2

    def sigmav(self, final, s):
        """sigma v_rel [GeV^-2]"""
        return 2 * self.lam**2 * self.v**2 * self.width(final, math.sqrt(s)) / (math.sqrt(s) * self.prop2(s))

    def me2(self, final, s):
        """sum |M|^2 over the photon (and Z) helicities"""
        mv2 = 0.0 if final == "aa" else self.MZ**2
        phi2 = (1 - mv2 / s) / (8 * math.pi)
        sym = 0.5 if final == "aa" else 1.0
        return self.lam**2 * self.v**2 * 2 * math.sqrt(s) * self.width(final, math.sqrt(s)) / (self.prop2(s) * phi2 * sym)

    def momenta(self, final, s, theta):
        """S S -> a V in the CM frame, the photon (particle 3) at the angle theta"""
        E = math.sqrt(s) / 2
        p = math.sqrt(E * E - self.m**2)
        mv2 = 0.0 if final == "aa" else self.MZ**2
        k = (s - mv2) / (2 * math.sqrt(s))
        st, ct = math.sin(theta), math.cos(theta)
        return [(E, 0, 0, p), (E, 0, 0, -p), (k, k * st, 0, k * ct), (math.sqrt(k * k + mv2), -k * st, 0, -k * ct)]


def velocity(card_text):
    """MadDM's v = sqrt(3)/2 vave_indirect_line (launch_indirect)"""
    return math.sqrt(3) / 2 * float(re.search(r"^\s*(\S+)\s*=\s*vave_indirect_line", card_text, re.M).group(1))


def madloop(pv, runs):
    """MadLoop's "finite" for each (point, mu) of runs, with the standalone check of the loop directory pv"""
    f = pv / "check_sa.f"
    orig = f.read_text()
    old = "        MU_R=SQRTS\n"
    new = (old + "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n        READ(968,*) MU_R\n"
           "        CLOSE(968)\n 9979   CONTINUE\n")
    try:
        s = re.sub(r"PARAMETER \(READPS = \.\w+\.\)", "PARAMETER (READPS = .TRUE.)", orig)
        s = re.sub(r"PARAMETER \(NPSPOINTS = \d+\)", "PARAMETER (NPSPOINTS = 1)", s)
        if "MU_R.input" not in s:
            assert s.count(old) == 1
            s = s.replace(old, new)
        f.write_text(s)
        (pv / "check").unlink(missing_ok=True)
        subprocess.run(["make", "check"], cwd=pv, capture_output=True, text=True, check=True)
        out = []
        for pts, mu in runs:
            (pv / "PS.input").write_text("".join("%.17e %.17e %.17e %.17e\n" % q for q in pts))
            (pv / "MU_R.input").write_text("%.17e\n" % mu)
            o = subprocess.run(["./check"], cwd=pv, capture_output=True, text=True, check=True).stdout
            out.append(float(re.search(r"Matrix element finite\s*=\s*(\S+)", o).group(1)))
        return out
    finally:
        f.write_text(orig)
        for name in ("PS.input", "MU_R.input", "check"):
            (pv / name).unlink(missing_ok=True)


def collect(mass):
    """after the launch at m_S = mass: copy MadDM's results, run the MadLoop checks"""
    dest = RUNS / ("m%03d" % mass)
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    run = max((OUT / "output").glob("run_*"), key=lambda p: int(p.name.split("_")[1]))
    for name in ("MadDM_results.txt", "maddm_card.dat"):
        shutil.copy(run / name, dest / name)
    shutil.copy(OUT / "Cards" / "param_card.dat", dest / "param_card.dat")
    sub = OUT / "Indirect_LI_line" / "SubProcesses"
    card = read_card(dest / "param_card.dat")
    assert abs(card["ms0"] / mass - 1) < 1e-12, "the param_card is not at m_S = %s" % mass
    own = Own(card)
    v = velocity((dest / "maddm_card.dat").read_text())
    s = 4 * own.m**2 * (1 + v * v)
    res = {"run": run.name, "v": v, "s": s, "madevent": {}, "madloop": {}}
    for fs, tag in PROCS.items():
        pdir = next(p for p in sub.iterdir() if p.name.startswith("P1") and p.name.endswith(tag))
        # the channels of symfact.dat and their factors, as MadEvent's sum_html.collect_result
        chans = []
        for line in (pdir / "symfact.dat").read_text().split("\n"):
            if line.strip() and int(line.split()[1]) > 0:
                x, e = map(float, (pdir / ("G" + line.split()[0]) / "results.dat").read_text().split()[:2])
                chans.append([int(line.split()[1]) * x, int(line.split()[1]) * e])
        res["madevent"][fs] = {"xsec": sum(c[0] for c in chans), "err": math.sqrt(sum(c[1]**2 for c in chans)), "channels": chans}
        pv = next(p for p in sub.iterdir() if p.name.startswith("PV") and p.name.endswith(tag))
        cases = [(mu, th) for mu in MUS for th in ANGLES]
        vals = madloop(pv, [(own.momenta(fs, s, th), mu) for mu, th in cases])
        res["madloop"][fs] = [[mu, th, val] for (mu, th), val in zip(cases, vals)]
    (dest / "collected.json").write_text(json.dumps(res, indent=1))
    print("collected m_S = %s GeV (%s): MadEvent sigma %s pb" % (mass, run.name,
          ", ".join("%s %.5e" % (k, x["xsec"]) for k, x in res["madevent"].items())))


def row(n, what, result, verdict):
    print(f"{n:2d}  {what:50s} {result:78s} {verdict}")


def main():
    print(f"{'':2s}  {'check':50s} {'result':78s} verdict")
    n = 0
    for dest in sorted(RUNS.glob("m*")):
        res = json.loads((dest / "collected.json").read_text())
        own = Own(read_card(dest / "param_card.dat"))
        s, v = res["s"], res["v"]
        printed = {fs: float(re.search(r"%s\s*=\s*\[([0-9.eE+-]+)" % tag, (dest / "MadDM_results.txt").read_text()).group(1))
                   for fs, tag in PROCS.items()}
        for fs in PROCS:
            iden = 2 if fs == "aa" else 1
            ref = own.me2(fs, s)
            d = max(abs(iden * val / ref - 1) for mu, th, val in res["madloop"][fs])
            n += 1
            row(n, f"m_S = {own.m:g}: {fs}  MadLoop sum|M|^2 vs own",
                f"own {ref:.10e}; max rel. diff {d:.1e} (mu_R = {MUS[0]:g}, {MUS[1]:g}; 2 angles)",
                "agree" if d < 1e-8 else "see text")
            sig_own = own.sigmav(fs, s) / (2 * v / math.sqrt(1 + v * v)) * CONV       # pb
            me = res["madevent"][fs]
            # MadEvent's error, with the rounding of the 5-digit channel results added
            err = math.sqrt(me["err"]**2 + sum((0.5e-4 * 10**math.floor(math.log10(abs(x))))**2 for x, e in me["channels"]))
            d = me["xsec"] / sig_own - 1
            sv_own = sig_own * 2 * v * PB2CM3
            dp = printed[fs] / sv_own - 1
            n += 1
            row(n, f"   {fs}  MadDM sigma v vs own (MadDM's v, pb2cm3)",
                f"own {sv_own:.5e} cm^3/s; MadEvent {d:+.1e} (its error {err / sig_own:.1e}), printed {printed[fs]:.2e} ({dp:+.1e})",
                "agree" if abs(d) < 2e-3 and abs(dp) < 5e-3 else "see text")
    n += 1
    row(n, "MadDM's pb2cm3 vs c x 1 pb", f"{PB2CM3:.3e} vs {C_CMS * 1e-36:.6e} cm^3/s ({PB2CM3 / (C_CMS * 1e-36) - 1:+.2%})", "note")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--collect":
        collect(float(sys.argv[2]))
    else:
        main()
