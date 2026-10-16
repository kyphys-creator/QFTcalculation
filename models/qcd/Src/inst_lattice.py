# %% [markdown]
# # Step (10): the BPST instanton on a lattice (Wilson action and clover charge)
#
# Research note models/qcd, step (10).  rho = 1, g = 1, regular gauge, box [-B, B]^4 with open boundaries, spacing a.
# Exact links: along mu the colour direction 2 eta_{a mu nu} x_nu T^a of A_mu is constant, so U_mu(x) = exp(-i (v.sigma)/2) with
# v^a = 2 eta_{a mu nu} x_nu int_0^a ds/((x_mu+s)^2 + c^2), c^2 = rho^2 + sum_{nu != mu} x_nu^2 (D = d - i A).
# Wilson action S_W = sum_p 2 (2 - Re tr U_p) -> (1/2) int tr F^2; clover field strength F_mu nu = (i/8a^2)[(C - C^+) - traceless part], charge
# (1/32 pi^2) sum eps tr F F.  Compared with the continuum density summed over the same plaquettes (centres) / sites: the difference is the
# discretization error, O(a^2): -(1/5)(a/rho)^2 for S_W (inst_bpst.wl; Garcia Perez et al.), -(4/5)(a/rho)^2 for Q.  -> results/inst_lattice.csv
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python inst_lattice.py   (about 1 minute, 3 GB)

# %%
import csv, itertools, os, time
import numpy as np
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
B = 3.0
eps3 = np.zeros((3, 3, 3)); eps3[0, 1, 2] = eps3[1, 2, 0] = eps3[2, 0, 1] = 1; eps3[0, 2, 1] = eps3[2, 1, 0] = eps3[1, 0, 2] = -1
eta = np.zeros((3, 4, 4))
for a in range(3):
    eta[a, :3, :3] = eps3[a]; eta[a, a, 3] = 1; eta[a, 3, a] = -1

def su2_exp(v):
    """exp(i v.sigma/2)"""
    th = np.linalg.norm(v, axis=-1); c = np.cos(th/2); s = np.where(th > 0, np.sin(th/2)/np.where(th > 0, th, 1), 0.5)
    Um = np.empty(v.shape[:-1] + (2, 2), dtype=complex)
    Um[..., 0, 0] = c + 1j*s*v[..., 2]; Um[..., 1, 1] = c - 1j*s*v[..., 2]
    Um[..., 0, 1] = 1j*s*(v[..., 0] - 1j*v[..., 1]); Um[..., 1, 0] = 1j*s*(v[..., 0] + 1j*v[..., 1])
    return Um

def dag(M):
    return np.conj(np.swapaxes(M, -1, -2))

def sh(F, mu, k):
    return np.roll(F, -k, axis=mu)

def measure(a):
    n = int(round(2*B/a)) + 1
    x = -B + a*np.arange(n)
    X = np.meshgrid(x, x, x, x, indexing="ij")
    U = []
    for mu in range(4):
        c = np.sqrt(sum(X[nu]**2 for nu in range(4) if nu != mu) + 1.0)
        I = (np.arctan((X[mu] + a)/c) - np.arctan(X[mu]/c))/c
        v = np.stack([2*sum(eta[b, mu, nu]*X[nu] for nu in range(4)) for b in range(3)], axis=-1)*I[..., None]
        U.append(su2_exp(-v))
    S = Sc = 0.0; P = {}
    inner_p = tuple(slice(0, n - 1) for _ in range(4))
    for mu in range(4):
        for nu in range(mu + 1, 4):
            Pm = U[mu] @ sh(U[nu], mu, 1) @ dag(sh(U[mu], nu, 1)) @ dag(U[nu])
            S += np.sum(2*(2 - np.real(np.trace(Pm[inner_p], axis1=-2, axis2=-1))))
            xc2 = sum((X[k] + (a/2 if k in (mu, nu) else 0.0))**2 for k in range(4))
            Sc += np.sum((a**4*8*np.sum(eta[:, mu, nu]**2)/(xc2 + 1)**4)[inner_p])     # (1/2) tr F^2 of the (mu nu) and (nu mu) terms
            P[(mu, nu)] = Pm
    def clover(mu, nu):
        Um, Un = U[mu], U[nu]
        L1 = P[(mu, nu)] if mu < nu else dag(P[(nu, mu)])
        L2 = Un @ dag(sh(sh(Um, mu, -1), nu, 1)) @ dag(sh(Un, mu, -1)) @ sh(Um, mu, -1)
        L3 = dag(sh(Um, mu, -1)) @ dag(sh(sh(Un, mu, -1), nu, -1)) @ sh(sh(Um, mu, -1), nu, -1) @ sh(Un, nu, -1)
        L4 = dag(sh(Un, nu, -1)) @ sh(Um, nu, -1) @ sh(sh(Un, mu, 1), nu, -1) @ dag(Um)
        C = L1 + L2 + L3 + L4; A = C - dag(C)
        return 1j/(8*a*a)*(A - np.trace(A, axis1=-2, axis2=-1)[..., None, None]/2*np.eye(2))
    Fh = {(mu, nu): clover(mu, nu) for mu in range(4) for nu in range(4) if mu != nu}
    q = 0.0
    for perm in itertools.permutations(range(4)):
        sgn = round(np.linalg.det(np.eye(4)[list(perm)]))
        q = q + sgn*np.real(np.trace(Fh[perm[0], perm[1]] @ Fh[perm[2], perm[3]], axis1=-2, axis2=-1))
    inner_s = tuple(slice(1, n - 1) for _ in range(4))
    Q = np.sum(q[inner_s])*a**4/(32*np.pi**2)
    Qc = np.sum((6/np.pi**2/(sum(Xk**2 for Xk in X) + 1)**4)[inner_s])*a**4
    return n, S/(8*np.pi**2), Sc/(8*np.pi**2), Q, Qc

# %%
if __name__ == "__main__":
    rows = []
    for a in (1/2, 1/3, 1/4, 1/5):
        t0 = time.time()
        n, s, sc, Q, Qc = measure(a)
        rows.append([a, n, s, sc, Q, Qc])
        print(f"a/rho = {a:.4f} ({n}^4): S_W/8pi^2 = {s:.8f}, continuum (same plaquettes) {sc:.8f}, diff/a^2 = {(s - sc)/a**2:+.5f};  "
              f"Q_clover = {Q:.8f}, continuum (same sites) {Qc:.8f}, diff/a^2 = {(Q - Qc)/a**2:+.5f}  ({time.time()-t0:.0f}s)", flush=True)
    r = np.array(rows)
    for col, cc, name in ((2, 3, "S_W/8pi^2"), (4, 5, "Q")):
        A = np.array([r[:, 0]**2, r[:, 0]**4]).T
        c, *_ = np.linalg.lstsq(A, r[:, col] - r[:, cc], rcond=None)
        print(f"{name} - continuum = {c[0]:+.5f} (a/rho)^2 {c[1]:+.4f} (a/rho)^4" + ("   (expected -1/5)" if col == 2 else "   (expected -4/5)"))
    with open(os.path.join(HERE, "results", "inst_lattice.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["a_over_rho", "n", "S_W_over_8pi2", "S_continuum_same_plaquettes", "Q_clover", "Q_continuum_same_sites"])
        w.writerows([[f"{x:.10g}" for x in row] for row in rows])
    print("wrote results/inst_lattice.csv")
