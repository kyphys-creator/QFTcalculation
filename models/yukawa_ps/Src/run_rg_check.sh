#!/bin/bash
# Renormalization group of the pseudoscalar Yukawa + phi^4 model (research note models/yukawa_ps, step (7)).
#   1. general one-loop formulas (Machacek-Vaughn, two-component fermions, dummy-field masses) vs Eq. (8)  (rg_general.py)
#   2. FeynArts + FeynCalc: the explicit mu-dependence of the amplitudes of step (4) and of the self-energies (Package-X,
#      symbolic scale), and their values at mu = 1/2, 1, 2 with Package-X and LoopTools
#      -> results/rg_feyncalc.csv, results/rg_feyncalc_pole.csv                                       (rg_feyncalc.wl)
#   3. COLLIER: the same amplitudes at the same points and scales and a mu scan, the pole-mass loop functions
#      (built here, run by rg_numeric.py)                                                              (rg_collier.f90)
#   4. MadLoop (pole-only MS-bar and NLOCT on-shell counterterms, mu_R = mu), slopes in ln(mu), fits of beta_lambda, beta_y,
#      gamma_M (S-matrix elements) and gamma_m, gamma_M (pole masses); figure
#      -> results/rg_collier*.csv, results/rg_comparison.csv, ../figs/rg_d4.pdf                        (rg_numeric.py)
#   5. RG flow of (y^2, lambda) -> ../figs/rgflow.pdf                                                   (rgflow.py)
# Needs Src/generated/ (run_model_check.sh) and work/ml_<MSbar|OS>_<A|B> (run_madloop_check.sh).  wolframscript may print
# "libc++abi: ... MathLink::MLException" when LoopTools is unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
[ -x work/ml_OS_B/SubProcesses/P0_psipsix_phiphi/check ] || ./run_madloop_check.sh

echo "=== general formulas"
"$PY" rg_general.py

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file rg_feyncalc.wl 2>&1 | grep -E '^\((a|b)\)|^numbers'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" rg_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/rg_collier && echo "built work/rg_collier"

echo "=== MadLoop, fits, figure"
"$PY" rg_numeric.py

echo "=== RG flow"
"$PY" rgflow.py
