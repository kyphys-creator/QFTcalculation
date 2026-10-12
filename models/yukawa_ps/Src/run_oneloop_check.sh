#!/bin/bash
# One-loop 1PI functions of the pseudoscalar Yukawa + phi^4 model in d = 4 (research note models/yukawa_ps, step (3)).
#   1. FeynArts + FeynCalc: diagrams (1, 2, 1, 1, 9; phi 3-point 2), amplitudes vs Eq. (4), box-trace identity,
#      UV poles and MS-bar counterterms (Eq. (5)); brackets of Eqs. (6), (7) via Package-X and LoopTools
#      -> results/oneloop_mathematica.csv                                                    (oneloop_feyncalc.wl)
#   2. COLLIER, the note's formulas -> results/oneloop_collier.csv                           (oneloop_collier.f90)
#   3. comparison, with mpmath Feynman-parameter integrals for the two-point functions
#      -> results/oneloop_comparison.csv                                                     (oneloop_numeric.py)
#   4. gamma5 scheme: BMHV - NDR for the same diagrams                                       (oneloop_bmhv.wl)
# Needs Src/generated/ (run run_model_check.sh first).  LoopTools prints "Discrepancy in C0" and FF errors at the V_y
# point (p^2, k^2, p'^2) = (M^2, m^2, M^2): its returned C0 is wrong there (recorded, not a script error).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file oneloop_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" oneloop_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/oneloop_collier &&
  (cd work && ./oneloop_collier ../results/oneloop_collier.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" oneloop_numeric.py | tail -12

echo "=== gamma5: BMHV vs NDR"
wolframscript -file oneloop_bmhv.wl 2>&1 | grep -E '^\(d\)'
