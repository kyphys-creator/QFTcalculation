#!/bin/bash
# One-loop 1PI functions of QCD in a general covariant gauge (research note models/qcd, step (3)).
#   1. FeynArts + FeynCalc: diagrams (gluon, ghost, u, t two-point 9, 1, 1, 1; u, t, ghost vertices 2, 2, 2; three- and
#      four-gluon vertices 18, 54), the two-point functions vs Eq. (5) exactly in D dimensions (per diagram), transversality,
#      the vertex poles vs Eq. (6) by Taylor expansion + infrared rearrangement, counterterms Eq. (7), delta_g from all
#      four vertices (Eq. (4)), the TID + PaVeUVPart comparison; brackets via Package-X and LoopTools
#      -> results/oneloop_mathematica.csv                                                        (oneloop_feyncalc.wl)
#   2. COLLIER, Eq. (8) -> results/oneloop_collier.csv                                           (oneloop_collier.f90)
#   3. comparison with mpmath integrals of Eq. (8) -> results/oneloop_comparison.csv              (oneloop_numeric.py)
# Needs Src/generated/ (run run_model_check.sh first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file oneloop_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" oneloop_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/oneloop_collier &&
  (cd work && ./oneloop_collier ../results/oneloop_collier.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" oneloop_numeric.py | tail -40
