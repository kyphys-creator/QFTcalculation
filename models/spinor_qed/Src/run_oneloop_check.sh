#!/bin/bash
# One-loop 1PI functions of spinor QED in a general covariant gauge (research note models/spinor_qed, step (3)).
#   1. FeynArts + FeynCalc: diagrams (photon 1-, 2-, 3-, 4-point 2, 2, 4, 12; e and mu self-energies 1, 1; vertex 1),
#      amplitudes vs Eq. (5) (incl. the IBP relation for the doubled photon propagator), Furry, the UV pole of the photon
#      4-point function, poles and MS-bar counterterms (Eq. (6)), Ward identities, R F1^R(0) = 1, the pole mass;
#      brackets via Package-X and LoopTools -> results/oneloop_mathematica.csv                 (oneloop_feyncalc.wl)
#   2. COLLIER, the note's PaVe forms -> results/oneloop_collier.csv                          (oneloop_collier.f90)
#   3. comparison with mpmath integrals of the note's formulas -> results/oneloop_comparison.csv (oneloop_numeric.py)
# Needs Src/generated/ (run run_model_check.sh first).  The LoopTools link prints "libc++abi: terminating ...
# MathLink::MLException" when the kernel exits; the results are written before that (not a script error).
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
