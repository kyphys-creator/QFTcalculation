#!/bin/bash
# Renormalization group of the one-loop phi phi -> phi phi amplitude (research note, step (9)).
#   1. FeynArts + FeynCalc: the d = 4 MS-bar amplitude of step (5), M1 with Package-X and LoopTools at the six points
#      for mu = 1, 1/2, 2 -> results/rg4_feyncalc.csv                                   (rg4_feyncalc.wl)
#   2. COLLIER: the same points and a mu scan -> results/rg4_collier*.csv                (rg4_collier.f90)
#   3. MadLoop (pole-only MS-bar counterterms, mu_R = mu), the slopes in ln(mu) and the two-parameter fits
#      (mass running, beta) in d = 4 and, from the step (8) results, in d = 6; figure
#      -> results/rg4_comparison.csv, ../figs/rg4_d4.pdf                                (rg4_numeric.py)
#   4. RG flow of the dimensionless parameters with the fitted coefficients -> ../figs/rgflow.pdf   (rgflow.py)
# Needs Src/generated/ (generate_Phi3.wl), work/ml_MSbar (run_madloop_check.sh) and
# results/scat6_*.csv (run_scat6_check.sh).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file rg4_feyncalc.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" rg4_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/rg4_collier &&
  (cd work && ./rg4_collier ../results | grep wrote)

echo "=== MadLoop, fits"
"$HOME/miniforge3/envs/qft/bin/python" rg4_numeric.py

echo "=== RG flow"
"$HOME/miniforge3/envs/qft/bin/python" rgflow.py
