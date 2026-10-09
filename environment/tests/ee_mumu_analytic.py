"""LO sigma(e+ e- -> mu+ mu-) with gamma + Z exchange, |eta_l| < 2.5, sqrt(s) = 1 TeV,
MG5 'sm' parameters (aEWM1, Gf, MZ, WZ).  See Appendix B of environment.pdf."""
import math
aEWM1, Gf, MZ, WZ = 132.507, 1.16639e-5, 91.188, 2.441404
alpha = 1 / aEWM1
MW = math.sqrt(MZ**2 / 2 + math.sqrt(MZ**4 / 4 - math.pi * alpha * MZ**2 / (math.sqrt(2) * Gf)))
sw2 = 1 - MW**2 / MZ**2
cw2 = 1 - sw2
s = 1000.0**2
chi = s / (s - MZ**2 + 1j * MZ * WZ) / (4 * sw2 * cw2)
v, a = -0.5 + 2 * sw2, -0.5
A0 = 1 + 2 * chi.real * v * v + abs(chi)**2 * (v * v + a * a)**2
c0 = math.tanh(2.5)
GeV2pb = 0.3893794e9
sigma = math.pi * alpha**2 / (2 * s) * A0 * (2 * c0 + 2 * c0**3 / 3) * GeV2pb
print(f"MW = {MW:.4f} GeV, sin^2 thetaW = {sw2:.5f}, A0 = {A0:.5f}, c0 = {c0:.5f}")
print(f"sigma = {sigma:.5f} pb")
