#!/bin/bash
# Renormalization group of the one-loop phi phi -> phi phi amplitude of phi^3 + phi^4 (research note models/phi34, step (7)).
#   1. FeynArts + FeynCalc: the MS-bar amplitude of step (4), its explicit mu-dependence (App. J), M1 with Package-X and
#      LoopTools at the six points for mu = 1, 1/2, 2 -> results/rg_feyncalc.csv                    (rg_feyncalc.wl)
#   2. COLLIER: the same points (with the three coupling structures) and a mu scan
#      -> results/rg_collier*.csv                                                                    (rg_collier.f90)
#   3. MadLoop (pole-only MS-bar and NLOCT on-shell counterterms, mu_R = mu), the slopes in ln(mu), the three-parameter
#      fits (gamma, beta_g, beta_lambda) and the four-coefficient fit; figure
#      -> results/rg_comparison.csv, ../figs/rg_d4.pdf                                               (rg_numeric.py)
#   4. RG flow of (lambda, alpha) with the fitted coefficients -> ../figs/rgflow.pdf                 (rgflow.py)
# Needs Src/generated/ (run_model_check.sh) and work/ml_MSbar, work/ml_OS (run_madloop_check.sh).  wolframscript may print
# "libc++abi: ... MathLink::MLException" when LoopTools is unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file rg_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" rg_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/rg_collier &&
  (cd work && ./rg_collier ../results | grep wrote)

echo "=== MadLoop, fits"
"$HOME/miniforge3/envs/qft/bin/python" rg_numeric.py

echo "=== RG flow"
"$HOME/miniforge3/envs/qft/bin/python" rgflow.py
