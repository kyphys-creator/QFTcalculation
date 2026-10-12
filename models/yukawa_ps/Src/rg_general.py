# %% [markdown]
# # Step (7): the one-loop RG coefficients from the general formulas of Machacek and Vaughn (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (7), App. rgfit.  Independent check of Eq. (8) (eq:rge) with the general one-loop
# formulas for a theory of real scalars phi_a and two-component (Weyl) fermions psi_i (Machacek and Vaughn, Nucl. Phys.
# B 222 (1983) 83, B 236 (1984) 221, B 249 (1985) 70; masses by the dummy-field method, Luo, Wang and Xiao, Phys. Rev. D 67
# (2003) 065019), in the convention
#     L = ... - (1/2)(Y^a_ij phi_a psi_i psi_j + h.c.) - (1/2)(m_ij psi_i psi_j + h.c.) - (1/2) m2_ab phi_a phi_b
#         - (1/4!) lambda_abcd phi_a phi_b phi_c phi_d,      kappa = 1/2 (two-component fermions),
# and, times (4 pi)^2 (beta = d/d ln mu):
#     gamma^S_ab = 2 kappa Y2S_ab,   gamma^F = (1/2) Y2F,   Y2F = Y^b+ Y^b,   Y2S_ab = (1/2) tr(Y^a+ Y^b + Y^b+ Y^a),
#     beta_Y^a = (1/2)(Y2F^T Y^a + Y^a Y2F) + 2 Y^b Y^a+ Y^b + 2 kappa Y^b (1/2) tr(Y^b+ Y^a + Y^a+ Y^b),
#     beta_lambda_abcd = Lambda2_abcd - 8 kappa H_abcd + 2 kappa LambdaY_abcd,
#         Lambda2 = (1/8) sum_perm lambda_abef lambda_efcd,  H = (1/4) sum_perm tr(Y^a Y^b+ Y^c Y^d+),
#         LambdaY = sum_i Y2S_ai lambda_ibcd + (the same for b, c, d).
# Dummy fields: the fermion mass m is a Yukawa coupling of a non-propagating scalar, the scalar mass enters as
# lambda_{ab d d} = 2 m2_ab (two dummy legs); sums over internal scalars run over the propagating phi only, and the dummy
# legs carry no anomalous dimension.  phi phi^3 and tadpole terms vanish here (no cubic coupling, parity).
#
# Dirac psi = (chi, eta^dagger) in the chiral basis (gamma^5 = diag(-1, 1)):  psibar psi = eta chi + h.c.,
# psibar gamma5 psi = -eta chi + chi^dagger eta^dagger, so  -M psibar psi - i y phi psibar gamma5 psi gives
#     m = M sigma_1,   Y = -i y sigma_1      (scalar Yukawa -y phi psibar psi would be Y = y sigma_1)
# in the basis (chi, eta).  Prints the coefficients and compares them with Eq. (8).
# Batch: ~/miniforge3/envs/qft/bin/python rg_general.py   Interactive: "Run Cell" in VS Code.

# %%
import itertools

import sympy as sp

y, lam, M, m = sp.symbols("y lambda M m", positive=True)
KAPPA = sp.Rational(1, 2)
SIGMA1 = sp.Matrix([[0, 1], [1, 0]])


def dag(a):
    return a.conjugate().T


def tr(a):
    return sp.expand(a.trace())


def coefficients(Y, mf):
    """one-loop coefficients (times (4 pi)^2) for one real scalar with Yukawa matrix Y, fermion mass matrix mf,
    quartic lambda and scalar mass m^2; the dummy field d carries mf (Yukawa) and m^2 (quartic with two dummy legs)."""
    y2f = dag(Y) * Y
    y2s = sp.Rational(1, 2) * tr(dag(Y) * Y + dag(Y) * Y)
    gam_s = 2 * KAPPA * y2s
    gam_f = sp.Rational(1, 2) * y2f
    # Yukawa coupling and fermion mass: the same formula, with X = Y or X = mf in the external-scalar slot
    def beta_yuk(X):
        # Y2F^T on the left (Y^a symmetric); here Y2F = y^2 1 either way
        return sp.expand(sp.Rational(1, 2) * (y2f.T * X + X * y2f) + 2 * Y * dag(X) * Y
                         + 2 * KAPPA * Y * sp.Rational(1, 2) * tr(dag(Y) * X + dag(X) * Y))
    bY, bm = beta_yuk(Y), beta_yuk(mf)
    # quartic: lambda_{phi phi phi phi} = lambda
    lam2 = sp.Rational(1, 8) * 24 * lam ** 2
    H = sp.Rational(1, 4) * sum(tr(Y * dag(Y) * Y * dag(Y)) for _ in itertools.permutations(range(4)))
    lamY = 4 * y2s * lam
    b_lam = sp.expand(lam2 - 8 * KAPPA * H + 2 * KAPPA * lamY)
    # scalar mass: beta of lambda_{phi phi d d} = 2 m^2 with two dummy legs
    lam_ffdd = 2 * m ** 2
    # Lambda2: (ab)(dd) channel lambda_{ab e f} lambda_{e f d d} (8 of the 24 permutations, times 1/8); the (ad)(bd)
    # channels need a cubic coupling lambda_{a d e f}, which is zero
    lam2_m = lam * lam_ffdd
    mats = {"a": Y, "b": Y, "d1": mf, "d2": mf}
    H_m = sp.Rational(1, 4) * sum(tr(mats[p[0]] * dag(mats[p[1]]) * mats[p[2]] * dag(mats[p[3]]))
                                  for p in itertools.permutations(["a", "b", "d1", "d2"]))
    lamY_m = 2 * y2s * lam_ffdd                # only the two propagating legs
    b_lam_ffdd = sp.expand(lam2_m - 8 * KAPPA * H_m + 2 * KAPPA * lamY_m)
    return {"gamma_phi": gam_s, "gamma_psi": gam_f, "beta_Y": bY, "beta_mf": bm, "beta_lambda": b_lam,
            "beta_m2": sp.expand(b_lam_ffdd / 2)}


# %% [markdown]
# ## Pseudoscalar Yukawa coupling (this note) and, for comparison, the scalar coupling

# %%
ps = coefficients(-sp.I * y * SIGMA1, M * SIGMA1)
sc = coefficients(y * SIGMA1, M * SIGMA1)


def proportional(mat, ref):
    """c with mat = c ref (2x2), or None"""
    c = sp.simplify(mat[0, 1] / ref[0, 1])
    return c if sp.simplify(mat - c * ref) == sp.zeros(2, 2) else None


# expected (note Eq. (8), times (4 pi)^2)
expect = {"beta_y": 5 * y ** 3, "beta_lambda": 3 * lam ** 2 + 8 * lam * y ** 2 - 48 * y ** 4,
          "gamma_m": lam * m ** 2 + 4 * y ** 2 * m ** 2 - 8 * y ** 2 * M ** 2, "gamma_M": -y ** 2 * M,
          "gamma_phi": 2 * y ** 2, "gamma_psi": y ** 2 / 2}
got = {"beta_y": proportional(ps["beta_Y"], -sp.I * SIGMA1),        # beta_Y = beta_y (-i sigma_1)
       "beta_lambda": ps["beta_lambda"], "gamma_m": ps["beta_m2"],
       "gamma_M": proportional(ps["beta_mf"], SIGMA1),               # beta_m = gamma_M sigma_1
       "gamma_phi": ps["gamma_phi"], "gamma_psi": proportional(ps["gamma_psi"] * SIGMA1, SIGMA1)}   # gamma^F = gamma_psi 1
for k in expect:
    print(f"{k:12s} general formulas: {str(got[k]):32s}  Eq. (8): {str(sp.expand(expect[k])):32s}  "
          f"difference: {sp.simplify(got[k] - expect[k])}")

# %%
print("scalar Yukawa (-y phi psibar psi) with the same formulas:")
print("  beta_y    ", proportional(sc["beta_Y"], SIGMA1), "   beta_lambda", sc["beta_lambda"])
print("  gamma_M   ", proportional(sc["beta_mf"], SIGMA1), "   (of which the fermion-loop tadpole term 2 kappa Y tr(...) gives 2 y^2 M)")
