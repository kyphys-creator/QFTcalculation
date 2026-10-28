# %% [markdown]
# # Step (6): the one-loop beta functions of the abelian Higgs model from the general formulas
#
# Research note models/abelian_higgs, step (6).  The general one-loop formulas of Machacek and Vaughn (Nucl. Phys. B 222
# (1983) 83, B 249 (1985) 70) in the form of Luo, Wang and Xiao (Phys. Rev. D 67 (2003) 065019), for a gauge theory with
# real scalars phi_a and no fermions,
#     beta_g        = (g^3/K) S2(S)/6                                  (U(1): C2(G) = 0),
#     beta_lam_abcd = (1/K) [Lambda^2_abcd - 3 g^2 Lambda^S_abcd + 3 g^4 A_abcd],
#     beta_m2_ab    = (1/K) [m2_ef lam_abef - 3 g^2 (C2(a) + C2(b)) m2_ab],
# with Lambda^2_abcd = (1/8) sum_perm lam_abef lam_efcd, Lambda^S_abcd = sum_{i = a,b,c,d} C2(i) lam_abcd,
# A_abcd = (1/8) sum_perm {theta, theta}_ab {theta, theta}_cd, are evaluated with the explicit fields of the note:
# Phi = (phi_1 + i phi_2)/sqrt 2 of charge 1, i.e. the generator theta = [[0, -i], [i, 0]] on (phi_1, phi_2), and
#     V = -m^2 |Phi|^2 + lam |Phi|^4 = (1/2) m2_ab phi_a phi_b + (1/24) lam_abcd phi_a phi_b phi_c phi_d,
#     m2_ab = -m^2 delta_ab,   lam_abcd = 2 lam (d_ab d_cd + d_ac d_bd + d_ad d_bc).
# The tensors are built component by component (sympy), not from the closed forms, and the results are compared with
# Eq. (rge) of the note.  The two-loop gauge term -(g^5/K^2)[-2 C2(S) S2(S)] = 4 g^5/K^2 is printed as well.
# Batch: python3 rg_general.py  (sympy)

# %%
import itertools

import sympy as sp

lam, m2, g = sp.symbols("lam m2 g", positive=True)
K = sp.Symbol("K", positive=True)
N = 2
theta = sp.Matrix([[0, -sp.I], [sp.I, 0]])
d = sp.eye(N)

# quartic and mass tensors from the potential, by differentiation (independent of the closed form above)
phi = sp.symbols("phi1:3", real=True)
Phi2 = (phi[0] ** 2 + phi[1] ** 2) / 2
V = -m2 * Phi2 + lam * Phi2 ** 2
lam4 = {(a, b, c, e): sp.diff(V, phi[a], phi[b], phi[c], phi[e]) for a, b, c, e in itertools.product(range(N), repeat=4)}
mass2 = {(a, b): sp.diff(V, phi[a], phi[b]).subs({phi[0]: 0, phi[1]: 0}) for a, b in itertools.product(range(N), repeat=2)}

# group theory: C2 of each real component, S2(S) = Tr(theta theta) (one U(1) generator)
C2 = [sp.simplify((theta * theta)[i, i]) for i in range(N)]
S2S = sp.simplify((theta * theta).trace())
anti = theta * theta + theta * theta

# %%
def perms(idx):
    return list(itertools.permutations(idx))


beta_lam = {}
for a, b, c, e in itertools.product(range(N), repeat=4):
    L2 = sp.Rational(1, 8) * sum(lam4[(p[0], p[1], x, y)] * lam4[(x, y, p[2], p[3])]
                                 for p in perms((a, b, c, e)) for x in range(N) for y in range(N))
    LS = sum(C2[i] for i in (a, b, c, e)) * lam4[(a, b, c, e)]
    A = sp.Rational(1, 8) * sum(anti[p[0], p[1]] * anti[p[2], p[3]] for p in perms((a, b, c, e)))
    beta_lam[(a, b, c, e)] = sp.expand((L2 - 3 * g ** 2 * LS + 3 * g ** 4 * A) / K)
beta_m2 = {(a, b): sp.expand((sum(mass2[(x, y)] * lam4[(a, b, x, y)] for x in range(N) for y in range(N))
                              - 3 * g ** 2 * (C2[a] + C2[b]) * mass2[(a, b)]) / K) for a, b in itertools.product(range(N), repeat=2)}

# read off beta_lam and beta_{m^2}: lam_1111 = 6 lam, m2_11 = -m^2
beta_lam_note = (20 * lam ** 2 - 12 * g ** 2 * lam + 6 * g ** 4) / K
beta_m2_note = m2 * (8 * lam - 6 * g ** 2) / K
bl = sp.simplify(beta_lam[(0, 0, 0, 0)] / 6)
bm = sp.simplify(-beta_m2[(0, 0)])
print("theta theta = ", (theta * theta).tolist(), ", C2 =", C2, ", S2(S) =", S2S)
print("beta_g = g^3 S2(S)/(6K) =", sp.simplify(g ** 3 * S2S / (6 * K)), "  (note: g^3/(3K))")
print("beta_lam from lam_1111/6 =", sp.factor(bl), "  minus Eq. (rge):", sp.simplify(bl - beta_lam_note))
print("beta_m2 from -m2_11      =", sp.factor(bm), "  minus Eq. (rge):", sp.simplify(bm - beta_m2_note))
# the whole tensor is again of the symmetric form 2 beta_lam (dd + dd + dd): checks the structure, not only one component
bad = [k for k in beta_lam if sp.simplify(beta_lam[k] - 2 * beta_lam_note * (d[k[0], k[1]] * d[k[2], k[3]] + d[k[0], k[2]] * d[k[1], k[3]]
                                                                             + d[k[0], k[3]] * d[k[1], k[2]])) != 0]
print("components of beta_lam_abcd not of the form 2 beta_lam (dd + dd + dd):", bad)
print("two-loop gauge term: -(g^5/K^2)(-2 C2(S) S2(S)) =", sp.simplify(2 * C2[0] * S2S * g ** 5 / K ** 2))
