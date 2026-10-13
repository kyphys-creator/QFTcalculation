#!/bin/bash
# One-loop e+ e- -> mu+ mu- in spinor QED (research note models/spinor_qed, step (4)).
#   1. FeynArts + FeynCalc: 6 diagrams, each against its hand formula (Eqs. (5), (15), App. H), the box numerator
#      (Table 2), gauge-parameter independence, UV cancellation; LoopTools numbers per class, IR pole vs Eq. (16)
#      -> results/scat_mathematica.csv                                                        (scat_feyncalc.wl)
#   2. FeynArts + FormCalc (own kernel, unpatched FeynArts): four-dimensional spin sums, LoopTools
#      -> results/scat_formcalc.csv                                                          (scat_formcalc.wl)
#   3. COLLIER, the note's formulas -> results/scat_collier.csv                               (scat_collier.f90)
#   4. comparison, Eq. (16) with mpmath, the scheme relation Eq. (17), unitarity of the boxes (the gamma gamma cut)
#      -> results/scat_comparison.csv                                                        (scat_numeric.py)
# Needs Src/generated/ (run run_model_check.sh first).  The LoopTools link prints "libc++abi: terminating ...
# MathLink::MLException" when the kernel exits; the results are written before that (not a script error).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / LoopTools (about 5 min)"
wolframscript -file scat_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d|e|f)\)'

echo "=== FormCalc / LoopTools"
wolframscript -file scat_formcalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" scat_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/scat_collier &&
  (cd work && ./scat_collier ../results/scat_collier.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" scat_numeric.py
