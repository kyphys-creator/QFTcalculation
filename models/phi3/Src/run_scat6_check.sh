#!/bin/bash
# One-loop phi phi -> phi phi in d = 6 (research note, step (8)).
#   1. FeynArts + FeynCalc: amplitude, poles through the dimension shift and the MS-bar counterterms of Eq. (8),
#      Eq. (M6); M1 with Package-X and LoopTools for mu = 1, 1/2, 2 -> results/scat6_feyncalc.csv (scat6_feyncalc.wl)
#   2. COLLIER (D00, C00, B00): M1 at the points, a cos(theta) scan and a mu scan -> results/scat6_collier*.csv
#                                                                                       (scat6_collier.f90)
#   3. comparison, d = 6 unitarity for Im M1, beta function from the mu-dependence of the S-matrix element, figure
#      -> results/scat6_comparison.csv, ../figs/scat6_d6.pdf                            (scat6_numeric.py)
# Needs Src/generated/ (run generate_Phi3.wl first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file scat6_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" scat6_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/scat6_collier &&
  (cd work && ./scat6_collier ../results | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" scat6_numeric.py
