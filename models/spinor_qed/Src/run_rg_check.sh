#!/bin/bash
# Renormalization group of spinor QED (research note models/spinor_qed, step (7)).
#   1. FeynArts + FeynCalc: the 1PI functions (as in step (3)) and their symbolic mu-dependence with Package-X, the residue
#      through the exact A0 relations of B0', B1'; the 1PI brackets at mu = 1/2, 1, 2 with Package-X and LoopTools; K W of
#      e+ e- -> mu+ mu- (as in step (4)) at the nine points for mu = 1/2, 1, 2 with LoopTools
#      -> results/rg_feyncalc_onepi.csv, results/rg_feyncalc.csv                                       (rg_feyncalc.wl)
#   2. COLLIER: the same 1PI brackets and K W, and a mu scan at sqrt(s) = 6, t = -8 (built here, run by rg_numeric.py)
#                                                                                                       (rg_collier.f90)
#   3. MadLoop of step (5) (MS-bar charge and alpha(0), mu_R = mu), slopes in ln mu, gamma_A, gamma_psi, gamma_m (1PI and pole
#      mass), beta_e (S-matrix element); figure -> results/rg_collier_*.csv, results/rg_comparison.csv, ../figs/rg_running.pdf
#                                                                                                       (rg_numeric.py)
# Needs Src/generated/ (run_model_check.sh) and work/ml_<MS|a0> (run_madloop_check.sh).  wolframscript may print
# "libc++abi: ... MathLink::MLException" when LoopTools is unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
[ -x work/ml_a0/SubProcesses/P0_emep_mummup/check ] || ./run_madloop_check.sh

echo "=== FeynCalc / Package-X / LoopTools (about 2 min)"
wolframscript -file rg_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" rg_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/rg_collier && echo "built work/rg_collier"

echo "=== MadLoop, slopes, fits, figure"
"$PY" rg_numeric.py
