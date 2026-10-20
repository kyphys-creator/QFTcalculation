"""Stage 3 of the EFT and dark-matter tools (environment.pdf): MadDM 3.3 (rc/3.3) on real scalar dark matter with a
Higgs portal (model/SingletDM.fr + FeynRules' SM, unitary gauge), against own formulas with MadDM's own inputs
(the param_card of the run, MadDM's nucleon form factors, its g_* and constants).

  Couplings: h S S: -i lambda v, h h S S: -i lambda; v = 2 M_W s_W/e of the UFO (inputs aEWM1, Gf, MZ).
  (a) DM-quark couplings that MadDM extracts at zero momentum (maddm.out, Dirac-normalized):
        alpha_q = lambda m_q/(4 m_h^2 m_S)            (m_q: the Yukawa mass ym_q of the UFO)
  (b) sigma_SI^N = lambda^2 mu_N^2 m_N^2 f_N^2/(4 pi m_h^4 m_S^2),  f_N = sum_{u,d,s} f_Tq^N + (2/9) f_TG^N,
      with MadDM's f_Tq (maddm_run_interface.py: SPu = 0.0153, ...) and RAPIDD's m_p = 0.938, m_n = 0.94;
  (c) sigma v (CM frame) = 2 lambda^2 v^2 sum_X Gamma(h* -> X; sqrt s)/(sqrt s [(s - m_h^2)^2 + m_h^2 Gamma_h^2]),
        Gamma(h* -> W W) = M^3/(16 pi v^2) sqrt(1-x)(1 - x + 3x^2/4), x = 4 M_W^2/M^2, Z Z: half that with M_Z,
        Gamma(h* -> f fbar) = N_c M ym_f^2 beta^3/(8 pi v^2);
      <sigma v>(x) = int ds sigma(s) (s - 4m^2) sqrt(s) K_1(sqrt(s)/T)/(8 m^4 T K_2(x)^2), sigma = sigma v/(2 beta)
      (Gondolo-Gelmini); MadDM prints sigmav(x_f) = <sigma v>/2 for self-conjugate DM (its Boltzmann equation has 2 taacs);
  (d) the channel shares MadDM prints: sigma_X/sigma at sqrt s = 2 sqrt(m^2 + p^2), p = m/x_f (tests.f, cross_check_process);
  (e) Omega h^2 from dY/dx = -sqrt(pi/(45 g_*)) g_*S M_Pl m <sigma v> (Y^2 - Y_eq^2)/x^2,
      Y_eq = 45/(4 pi^4) (1/g_*S) x^2 K_2(x), with MadDM's g_*(T) (init.f, get_gstar: its particle table model_info.txt and
      the boson/fermion tables), M_Pl = 1.2209e19 GeV, Omega h^2 = Y_inf 2889.2 m/1.05e-5; MadDM's own ODE tolerance is
      eps_ode = 0.01 (relative change between starting points); run_02 repeats the run with eps_ode = 1e-4.
Usage: python3 test_maddm.py      (reads out/maddm_hp, written by run_stage3.sh)
"""
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import k1e, kve

HERE = Path(__file__).resolve().parent
RUN = HERE / "out" / "maddm_hp"
GEV2CM2 = 0.3893794e-27
# MadDM's nucleon inputs (maddm_run_interface.py, MadDMCard) and RAPIDD's nucleon masses (rapidd/alpha_map.py)
FT = {"p": {"u": 0.0153, "d": 0.0191, "s": 0.0447}, "n": {"u": 0.0110, "d": 0.0273, "s": 0.0447}}
MN = {"p": 0.938, "n": 0.94}
MPL, S0, RHOC = 1.2209e19, 2889.2, 1.05e-5


def read_card(path):
    card = {}
    for line in open(path):
        m = re.match(r"\s+(\d+)\s+([-+0-9.eE]+)\s+#\s+(\S+)", line)
        if m:
            card[m.group(3).lower()] = float(m.group(2))
        m = re.match(r"DECAY\s+(\d+)\s+([-+0-9.eE]+)", line)
        if m:
            card["w" + m.group(1)] = float(m.group(2))
    return card


class Model:
    def __init__(self, card):
        c = card
        self.MZ, self.MH, self.WH = c["mz"], c["mh"], c["w25"]
        aEW = 1 / c["aewm1"]
        self.MW = math.sqrt(self.MZ ** 2 / 2 + math.sqrt(self.MZ ** 4 / 4 - aEW * math.pi * self.MZ ** 2 / (c["gf"] * math.sqrt(2))))
        ee, sw = math.sqrt(4 * math.pi * aEW), math.sqrt(1 - self.MW ** 2 / self.MZ ** 2)
        self.v = 2 * self.MW * sw / ee
        self.lam, self.m = c["lamhs"], c["ms0"]
        self.ferm = {"b": (3, c["ymb"], c["mb"]), "c": (3, c["ymc"], c["mc"]), "s": (3, c["yms"], c["ms"]),
                     "d": (3, c["ymdo"], c["md"]), "u": (3, c["ymup"], c["mu"]), "t": (3, c["ymt"], c["mt"]),
                     "tau": (1, c["ymtau"], c["mta"]), "mu": (1, c["ymm"], c["mmu"]), "e": (1, c["yme"], c["me"])}

    def gammas(self, M):
        """partial widths of an off-shell Higgs of mass M"""
        g = {}
        for name, mv, f in [("wpwm", self.MW, 16), ("zz", self.MZ, 32)]:
            x = 4 * mv ** 2 / M ** 2
            g[name] = M ** 3 / (f * math.pi * self.v ** 2) * math.sqrt(1 - x) * (1 - x + 0.75 * x * x) if x < 1 else 0.0
        for name, (nc, y, mk) in self.ferm.items():
            b2 = 1 - 4 * mk ** 2 / M ** 2
            g[name] = nc * M * y ** 2 / (8 * math.pi * self.v ** 2) * b2 ** 1.5 if b2 > 0 else 0.0
        return g

    def sigmav_cm(self, s, ch=None):
        g = self.gammas(math.sqrt(s))
        G = sum(g.values()) if ch is None else g[ch]
        return 2 * self.lam ** 2 * self.v ** 2 * G / (math.sqrt(s) * ((s - self.MH ** 2) ** 2 + self.MH ** 2 * self.WH ** 2))

    def taacs(self, x, ch=None):
        """<sigma v> (Gondolo-Gelmini) with exponentially scaled Bessel functions; s = 4 m^2 (1 + e)"""
        m = self.m

        def f(e):
            s = 4 * m * m * (1 + e)
            beta = math.sqrt(e / (1 + e))
            return self.sigmav_cm(s, ch) / (2 * beta) * (4 * m * m * e) * math.sqrt(s) * k1e(2 * x * math.sqrt(1 + e)) \
                * math.exp(-2 * x * (math.sqrt(1 + e) - 1)) * 4 * m * m
        eres = (self.MH / (2 * m)) ** 2 - 1
        pts = [eres] if 0 < eres < 50 / x else None
        I = quad(f, 0, 50 / x, limit=400, epsrel=1e-11, points=pts)[0] + quad(f, 50 / x, np.inf, limit=200, epsrel=1e-11)[0]
        return I / (8 * m ** 4 * (m / x) * kve(2, x) ** 2)


def gstar_maddm(run):
    """MadDM's get_gstar (init.f) from the run's include/model_info.txt and boson/fermion tables"""
    rows = [l.split() for l in open(run / "include" / "model_info.txt").read().split("\n")[1:] if l.strip()]
    parts = [(float(a), float(b), int(c)) for a, b, c in rows]
    tb = np.loadtxt(run / "include" / "boson.txt")
    tf = np.loadtxt(run / "include" / "fermion.txt")

    def g(T):
        tot = 0.0
        for mass, dof, isf in parts:
            r = mass / T
            if r < 1e-2:
                tot += dof * (7 / 8) ** isf
            elif r < 1e2:
                t = tf if isf == 1 else tb
                tot += dof * np.interp(r, t[:, 0], t[:, 1])
        return tot
    return g


def relic(model, gstar):
    m = model.m
    xgrid = np.concatenate([np.linspace(3, 60, 115), np.geomspace(60.5, 1000, 60)])
    svgrid = np.array([model.taacs(x) for x in xgrid])
    svi = lambda x: math.exp(np.interp(x, xgrid, np.log(svgrid)))

    def yeq(x):
        return 45 / (4 * math.pi ** 4) / gstar(m / x) * x * x * kve(2, x) * math.exp(-x)

    def rhs(x, y):
        g = gstar(m / x)
        return [-math.sqrt(math.pi / (45 * g)) * g * MPL * m / x ** 2 * svi(x) * (y[0] ** 2 - yeq(x) ** 2)]
    sol = solve_ivp(rhs, (3, 1000), [yeq(3)], method="Radau", rtol=1e-10, atol=1e-25)
    return sol.y[0, -1] * S0 * m / RHOC


def maddm_out(run, name="run_01"):
    out = {}
    for line in open(run / "output" / name / "maddm.out"):
        p = line.split(":")
        if len(p) >= 2:
            key = p[0].strip() if p[0].strip() != "%" else "%" + p[1].split()[0]
            try:
                out[key] = [float(x.split()[0]) for x in (p[1:] if p[0].strip() != "%" else [p[1].split()[1]])]
            except ValueError:
                pass
    return out


def row(n, what, result, verdict):
    print(f"{n:2d}  {what:56s} {result:64s} {verdict}")


def main():
    card = read_card(RUN / "Cards" / "param_card.dat")
    md = Model(card)
    out = maddm_out(RUN)
    res = open(RUN / "output" / "run_01" / "MadDM_results.txt").read()
    print(f"{'':2s}  {'check':56s} {'result':64s} verdict")
    # (a)
    d = max(abs(out["alpha_" + q][0] / (md.lam * md.ferm[q][1] / (4 * md.MH ** 2 * md.m)) - 1) for q in "udscbt")
    row(1, "DM-quark couplings alpha_q (u, d, s, c, b, t) vs own", f"max rel. diff {d:.1e}", "agree" if d < 1e-5 else "see text")
    # (b) MadDM's sigma_SI with its own formula (RAPIDD's alpha_map) at full precision, and the printed values
    sig = {}
    for N in "pn":
        alpha = {q: out["alpha_" + q][0] for q in "udscbt"}
        c1 = sum(alpha[q] * MN[N] * FT[N][q] / md.ferm[q][1] for q in "uds") \
            + sum(alpha[q] * 2 / 27 * MN[N] * (1 - sum(FT[N].values())) / {"c": 1.27, "b": 4.7, "t": 172.0}[q] for q in "cbt")
        mu = md.m * MN[N] / (md.m + MN[N])
        sig[N] = 4 * mu ** 2 * c1 ** 2 / math.pi * GEV2CM2
    printed = {N: float(re.search(r"SigmaN_SI_%s\s*=\s*\[([0-9.eE+-]+)" % N, res).group(1)) for N in "pn"}
    own = {}
    for N in "pn":
        fN = sum(FT[N].values()) + 2 / 9 * (1 - sum(FT[N].values()))
        mu = md.m * MN[N] / (md.m + MN[N])
        own[N] = md.lam ** 2 * mu ** 2 * MN[N] ** 2 * fN ** 2 / (4 * math.pi * md.MH ** 4 * md.m ** 2) * GEV2CM2
    d = max(abs(sig[N] / own[N] - 1) for N in "pn")
    dp = max(abs(printed[N] / own[N] - 1) for N in "pn")
    row(2, "sigma_SI^{p,n} vs own (MadDM's f_Tq, m_N)", f"p {own['p']:.4e}, n {own['n']:.4e} cm^2; full {d:.1e}, printed (3 digits) {dp:.1e}",
        "agree" if d < 1e-6 and dp < 5e-3 else "see text")
    # (c), (d)
    xf = out["x_f"][0]
    sv_own = md.taacs(xf)
    d = sv_own / (2 * out["sigmav(xf)"][0]) - 1
    row(3, f"<sigma v>(x_f = {xf:g}) vs own (MadDM prints <sigma v>/2)", f"own {sv_own:.6e} GeV^-2 = 2 x MadDM x (1 {d:+.1e})",
        "agree" if abs(d) < 1e-4 else "see text")
    p = md.m / xf
    rs = 2 * math.sqrt(md.m ** 2 + p ** 2)
    g = md.gammas(rs)
    tot = sum(g.values())
    worst = max(((abs(out["%xsdmxsdm_" + ch][0] - 100 * g[k] / tot), ch) for ch, k in
                 [("wpwm", "wpwm"), ("zz", "zz"), ("bbx", "b"), ("ccx", "c"), ("tamtap", "tau")]))
    row(4, f"channel shares at sqrt(s) = {rs:.3f} GeV vs own", f"max abs. diff {worst[0]:.1e} % ({worst[1]}); W W {100*g['wpwm']/tot:.4f} %",
        "agree" if worst[0] < 1e-4 else "see text")
    # (e)
    oh2 = relic(md, gstar_maddm(RUN))
    d = out["Omegah^2"][0] / oh2 - 1
    row(5, "Omega h^2 vs own Boltzmann solution (MadDM's g_*)", f"MadDM {out['Omegah^2'][0]:.6f}, own {oh2:.6f} ({d:+.1e})",
        "agree" if abs(d) < 0.01 else "see text")
    out2 = maddm_out(RUN, "run_02")
    d2 = out2["Omegah^2"][0] / oh2 - 1
    row(6, "   MadDM with eps_ode = 1e-4 instead of 0.01", f"MadDM {out2['Omegah^2'][0]:.6f} ({d2:+.1e}), x_f = {out2['x_f'][0]:g}",
        "agree" if abs(d2) < abs(d) and abs(d2) < 3e-3 else "see text")


if __name__ == "__main__":
    main()
