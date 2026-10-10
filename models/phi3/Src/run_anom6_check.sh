#!/bin/bash
# Field anomalous dimension in d = 6 and comparison with the literature (research note, step (10)).
#   1. FeynArts + FeynCalc: the d = 6 MS-bar finite parts B0^(6), C0^(6) of the 1PI two- and three-point functions
#      with Package-X and LoopTools for mu = 1, 1/2, 2 -> results/anom6_feyncalc.csv          (anom6_feyncalc.wl)
#   2. COLLIER (B00, C00) at the same points -> results/anom6_collier.csv                    (anom6_collier.f90)
#   3. slopes in ln(mu), the fit of (gamma_phi, mass running) to the two-point function, beta from the three-point
#      function, comparison with step (9) and with Borinsky et al. (2021); figure
#      -> results/anom6_comparison.csv, ../figs/anom6_d6.pdf                                 (anom6_numeric.py)
# Needs Src/generated/ (generate_Phi3.wl) and results/rg4_comparison.csv (run_rg4_check.sh).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file anom6_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)' | cut -c1-200

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" anom6_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/anom6_collier &&
  (cd work && ./anom6_collier ../results/anom6_collier.csv | grep wrote)

echo "=== fits"
"$HOME/miniforge3/envs/qft/bin/python" anom6_numeric.py
