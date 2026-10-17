"""Hand results of the CKM note, Sec. 3.3 (research note models/sm_ckm): the running of V from the matrix Yukawa RGEs.

Checks, with numpy only (no model file involved; step (4) derives Eq. (betaY) from the note's model):
  (1) The closed form Eq. (Vrun), K dV/dln mu = -K A_u V + K V A_d, against the derivative of |V_ij| and J obtained by
      integrating Eq. (betaY) for the matrices Y_u, Y_d (RK4, steps +-h) and diagonalizing Y Y^dagger at each end.
      Done at a point with enlarged Yukawas (every term of Eq. (Vrun) matters); expect relative differences ~1e-8
      (the central difference).  The gauge and Tr terms multiply Y by a number and do not rotate V, so they are left out.
  (2) The benchmark of Eq. (bench): |V|, J, unitarity, K dln|V_ij|/dln mu, K dlnJ/dln mu and the hierarchical limits
      (3/2)(yt^2 + yb^2), 3(yt^2 + yb^2) of Eq. (Vhier); lambda_k = V_ki^* V_kj for b -> s, b -> d, s -> d.
Writes results/ckm_rg_handcheck.csv.  Usage: python3 ckm_rg_handcheck.py
"""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
K = 16 * np.pi**2


def ckm(s12, s23, s13, dl):
    """PDG standard parametrization, Eq. (Vstd) (rows: u, c, t; columns: d, s, b)."""
    c12, c23, c13 = (np.sqrt(1 - x**2) for x in (s12, s23, s13))
    e = np.exp(1j * dl)
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


def jarlskog(V):
    return np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]))


# %% [markdown]
# ## Eq. (Vrun) in closed form

# %%
def dV_closed(V, yu, yd):
    """K dV/dln mu of Eq. (Vrun): -K A_u V + K V A_d, generators with zero diagonal."""
    Du, Dd = np.diag(yu**2), np.diag(yd**2)
    Hd_u, Hu_d = V @ Dd @ V.conj().T, V.conj().T @ Du @ V
    KAu, KAd = np.zeros((3, 3), complex), np.zeros((3, 3), complex)
    for i in range(3):
        for k in range(3):
            if i != k:
                KAu[i, k] = -1.5 * (yu[i]**2 + yu[k]**2) / (yu[k]**2 - yu[i]**2) * Hd_u[i, k]
                KAd[i, k] = -1.5 * (yd[i]**2 + yd[k]**2) / (yd[k]**2 - yd[i]**2) * Hu_d[i, k]
    return -KAu @ V + V @ KAd


def dabs_dJ(V, KdV):
    """K d|V_ij|/dln mu and K dJ/dln mu from K dV/dln mu."""
    dabs = np.real(np.conj(V) * KdV) / np.abs(V)
    d = KdV
    dJ = np.imag(d[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]) + V[0, 1] * d[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])
                 + V[0, 1] * V[1, 2] * np.conj(d[0, 2]) * np.conj(V[1, 1]) + V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(d[1, 1]))
    return dabs, dJ


# %% [markdown]
# ## Eq. (betaY) integrated as matrices (Yukawa part; the rest does not rotate V)

# %%
def beta_Y(Yu, Yd):
    Hu, Hd = Yu @ Yu.conj().T, Yd @ Yd.conj().T
    T = np.trace(3 * Hu + 3 * Hd).real
    return (1.5 * (Hu - Hd) @ Yu + T * Yu) / K, (1.5 * (Hd - Hu) @ Yd + T * Yd) / K


def rk4(Yu, Yd, h):
    k1 = beta_Y(Yu, Yd)
    k2 = beta_Y(Yu + h / 2 * k1[0], Yd + h / 2 * k1[1])
    k3 = beta_Y(Yu + h / 2 * k2[0], Yd + h / 2 * k2[1])
    k4 = beta_Y(Yu + h * k3[0], Yd + h * k3[1])
    return (Yu + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            Yd + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))


def abs_and_J(Yu, Yd):
    """|V| and J from the eigenvectors of Y_u Y_u^dagger, Y_d Y_d^dagger (ascending masses)."""
    _, Uu = np.linalg.eigh(Yu @ Yu.conj().T)
    _, Ud = np.linalg.eigh(Yd @ Yd.conj().T)
    W = Uu.conj().T @ Ud
    return np.abs(W), jarlskog(W)


# %% [markdown]
# ## (1) closed form against the matrix integration

# %%
V0 = ckm(0.22501, 0.04183, 0.003732, 1.147)
yu_big = np.sqrt(2) * np.array([0.05, 20.0, 165.0]) / 246.0
yd_big = np.sqrt(2) * np.array([0.3, 5.0, 60.0]) / 246.0
Yu, Yd = np.diag(yu_big).astype(complex), V0 @ np.diag(yd_big)
h = 1e-3
Ap, Jp = abs_and_J(*rk4(Yu, Yd, h))
Am, Jm = abs_and_J(*rk4(Yu, Yd, -h))
num_dabs, num_dJ = (Ap - Am) / (2 * h), (Jp - Jm) / (2 * h)
f_dabs, f_dJ = dabs_dJ(V0, dV_closed(V0, yu_big, yd_big) / K)
rel_abs = np.max(np.abs((num_dabs - f_dabs) / num_dabs))
rel_J = abs(num_dJ - f_dJ) / abs(num_dJ)
print("(1) Eq. (Vrun) against the integrated matrix RGEs (enlarged Yukawas): max relative difference of d|V_ij|/dln mu",
      "%.1e, of dJ/dln mu %.1e (expect ~1e-8, the central difference)" % (rel_abs, rel_J))

# %% [markdown]
# ## (2) the benchmark

# %%
ee, sw, MW = np.sqrt(4 * np.pi / 128), np.sqrt(1881 / 8281), 80.0
v = 2 * MW * sw / ee
yu = np.sqrt(2) * np.array([0.00127, 0.619, 165.0]) / v
yd = np.sqrt(2) * np.array([0.00271, 0.0546, 2.86]) / v
V = V0
J = jarlskog(V)
dabs, dJ = dabs_dJ(V, dV_closed(V, yu, yd))       # K d|V|/dln mu, K dJ/dln mu
Kdln = dabs / np.abs(V)
hier1, hier2 = 1.5 * (yu[2]**2 + yd[2]**2), 3 * (yu[2]**2 + yd[2]**2)
print("(2) benchmark: |V| =\n", np.array2string(np.abs(V), precision=6))
print("    J = %.5e;  unitarity |V^dagger V - 1| = %.1e;  yt = %.4f, yb = %.5f" %
      (J, np.max(np.abs(V.conj().T @ V - np.eye(3))), yu[2], yd[2]))
print("    K dln|V_ij|/dln mu =\n", np.array2string(Kdln, precision=5))
print("    K dlnJ/dln mu = %.4f;  Eq. (Vhier): (3/2)(yt^2+yb^2) = %.5f, 3(yt^2+yb^2) = %.4f" % (dJ / J, hier1, hier2))
lams = {}
for (i, j, name) in [(1, 2, "b_to_s"), (0, 2, "b_to_d"), (0, 1, "s_to_d")]:
    lams[name] = [np.conj(V[k, i]) * V[k, j] for k in range(3)]
    print("    %s: lambda_u, lambda_c, lambda_t = %s (sum %.1e)" %
          (name, ", ".join("%.5f%+.5fi" % (z.real, z.imag) for z in lams[name]), abs(sum(lams[name]))))

RES.mkdir(exist_ok=True)
rows = [("quantity", "value"),
        ("rel_diff_dabs_closed_vs_matrix", "%.3e" % rel_abs), ("rel_diff_dJ_closed_vs_matrix", "%.3e" % rel_J),
        ("J", "%.6e" % J), ("yt", "%.6f" % yu[2]), ("yb", "%.6f" % yd[2]),
        ("hier_3/2(yt2+yb2)", "%.6f" % hier1), ("hier_3(yt2+yb2)", "%.6f" % hier2), ("KdlnJ", "%.6f" % (dJ / J))]
names = ["u", "c", "t"], ["d", "s", "b"]
rows += [("absV_%s%s" % (names[0][i], names[1][j]), "%.6f" % abs(V[i, j])) for i in range(3) for j in range(3)]
rows += [("Kdln_absV_%s%s" % (names[0][i], names[1][j]), "%.6e" % Kdln[i, j]) for i in range(3) for j in range(3)]
rows += [("lambda_%s_%s" % (name, q), "%.6e%+.6ej" % (z.real, z.imag)) for name, l in lams.items()
         for q, z in zip("uct", l)]
with open(RES / "ckm_rg_handcheck.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)
print("wrote", RES / "ckm_rg_handcheck.csv")
