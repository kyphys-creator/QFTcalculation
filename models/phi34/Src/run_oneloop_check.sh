#!/bin/bash
# One-loop 1PI functions of phi^3 + phi^4 in d = 4 (research note models/phi34, step (3)).
#   1. FeynArts + FeynCalc: diagrams (1, 2, 4, 12), amplitudes vs Eq. (4), UV poles and MS-bar counterterms (Eq. (5));
#      brackets b_n of Eq. (6) via Package-X and LoopTools -> results/oneloop_mathematica.csv   (oneloop_feyncalc.wl)
#   2. COLLIER, the note's formula                       -> results/oneloop_collier.csv       (oneloop_collier.f90)
#   3. comparison                                        -> results/oneloop_comparison.csv    (oneloop_numeric.py)
# Needs Src/generated/ (run run_model_check.sh first).  LoopTools prints FF errors at the Euclidean V3 point (its C0
# fails there; recorded, not a script error).
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
"$HOME/miniforge3/envs/qft/bin/python" oneloop_numeric.py | tail -10
