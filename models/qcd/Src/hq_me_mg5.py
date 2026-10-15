# %% [markdown]
# # Step (9): tree-level 2 -> 3 matrix elements from MadGraph5 standalone (check of hq_real.wl at D = 4)
#
# Research note models/qcd, step (9).  Generates u u~ > t t~ g, g g > t t~ g, u g > t t~ u with the LO UFO (m_t = 1, aS = 1/(4 pi),
# written as a plain decimal: MadGraph reads a longer mantissa with an exponent wrongly), builds a small driver that reads momenta
# and calls SMATRIX (averaged over initial spins and colours), and evaluates 12 random points at sqrt(s)^2 = 5.3, 9.1, 30, 120.
# Writes results/hq_me_mg5.csv: channel, s, x1..x4 (x1 = -2 p1.k1, x2 = -2 p2.k1, x3 = -2 p2.k2, x4 = -2 p1.k2), |M|^2 (averaged).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python hq_me_mg5.py   (about 1 minute)

# %%
import os, shutil, subprocess
import numpy as np
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
WORK = os.path.join(HERE, "work", "hq")
os.makedirs(WORK, exist_ok=True)
ENV = dict(os.environ, PATH=os.path.expanduser("~/hep/bin") + ":" + os.environ["PATH"])
if "SDKROOT" not in ENV:
    ENV["SDKROOT"] = subprocess.run(["xcrun", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()
SA = os.path.join(WORK, "me_sa")
PROCS = (("qq", "P1_uux_ttxg"), ("gg", "P2_gg_ttxg"), ("qg", "P3_ug_ttxu"))
DRIVER = """      PROGRAM DRV
      IMPLICIT NONE
      INCLUDE 'nexternal.inc'
      REAL*8 P(0:3,NEXTERNAL), ANS
      INTEGER I,J,N
      CALL SETPARA('../../Cards/param_card.dat')
      READ(*,*) N
      DO J=1,N
        DO I=1,NEXTERNAL
          READ(*,*) P(0,I),P(1,I),P(2,I),P(3,I)
        ENDDO
        CALL SMATRIX(P,ANS)
        WRITE(*,'(E26.17)') ANS
      ENDDO
      END
"""

# %% [markdown]
# ## Standalone output and drivers

# %%
ufo = os.path.join(WORK, "QCD_UFO")
if os.path.isdir(ufo):
    shutil.rmtree(ufo)
shutil.copytree(os.path.join(HERE, "generated", "QCD_UFO"), ufo)
with open(os.path.join(WORK, "me_sa.mg5"), "w") as fh:
    fh.write(f"set automatic_html_opening False\nimport model {ufo}\ngenerate u u~ > t t~ g\nadd process g g > t t~ g\n"
             f"add process u g > t t~ u\noutput standalone {SA} -f\n")
subprocess.run([os.path.expanduser("~/hep/bin/mg5_aMC"), os.path.join(WORK, "me_sa.mg5")], cwd=WORK, env=ENV,  # MG5 drops nsqso_born.inc in cwd
               stdout=open(os.path.join(WORK, "me_sa.log"), "w"), stderr=subprocess.STDOUT, check=True)
card = os.path.join(SA, "Cards", "param_card.dat")
txt = open(card).read()
import re
txt = re.sub(r"(\n +3 +)7\.957747e-02( +# aS)", r"\g<1>0.07957747154594767\g<2>", txt)
open(card, "w").write(txt)
for _, P in PROCS:
    d = os.path.join(SA, "SubProcesses", P)
    subprocess.run(["make", "check"], cwd=d, env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    open(os.path.join(d, "drv.f"), "w").write(DRIVER)
    subprocess.run(["gfortran", "-O", "-o", "drv", "drv.f", "matrix.o", "-L../../lib", "-ldhelas", "-lmodel"], cwd=d, env=ENV, check=True)

# %% [markdown]
# ## Random points (m = 1): (k1 k3) system of random mass, then two-body decays

# %%
rng = np.random.default_rng(7)
def boost(p, b):
    b2 = b @ b; g = 1/np.sqrt(1 - b2); bp = b @ p[1:]
    return np.concatenate([[g*(p[0] + bp)], p[1:] + ((g - 1)*bp/b2 + g*p[0])*b])
def two(M, m1, m2):
    k = np.sqrt((M*M - (m1 + m2)**2)*(M*M - (m1 - m2)**2))/(2*M)
    c = rng.uniform(-1, 1); ph = rng.uniform(0, 2*np.pi); st = np.sqrt(1 - c*c)
    n = np.array([st*np.cos(ph), st*np.sin(ph), c])
    return np.concatenate([[np.sqrt(k*k + m1*m1)], k*n]), np.concatenate([[np.sqrt(k*k + m2*m2)], -k*n])
def point(s):
    W = np.sqrt(s); m = 1.0
    M13 = rng.uniform(m, W - m)
    q13, k2 = two(W, M13, m)
    k1, k3 = two(M13, m, 0.0)
    b = q13[1:]/q13[0]
    return np.array([W/2, 0, 0, W/2]), np.array([W/2, 0, 0, -W/2]), boost(k1, b), k2, boost(k3, b)
def dot(a, b):
    return a[0]*b[0] - a[1:] @ b[1:]
pts = [point(s) for s in (5.3, 9.1, 30.0, 120.0) for _ in range(3)]
rows = []
for chan, P in PROCS:
    inp = f"{len(pts)}\n" + "".join("".join("%.17e %.17e %.17e %.17e\n" % tuple(p) for p in pt) for pt in pts)
    out = subprocess.run(["./drv"], cwd=os.path.join(SA, "SubProcesses", P), input=inp, capture_output=True, text=True, check=True).stdout.split()
    for (p1, p2, k1, k2, k3), v in zip(pts, out):
        rows.append([chan, dot(p1 + p2, p1 + p2), -2*dot(p1, k1), -2*dot(p2, k1), -2*dot(p2, k2), -2*dot(p1, k2), float(v)])
with open(os.path.join(HERE, "results", "hq_me_mg5.csv"), "w") as fh:
    for r in rows:
        fh.write(r[0] + "," + ",".join("%.17e" % x for x in r[1:]) + "\n")
print(f"wrote results/hq_me_mg5.csv ({len(rows)} rows)")
