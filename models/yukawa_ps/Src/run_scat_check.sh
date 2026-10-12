#!/bin/bash
# One-loop phi phi -> phi phi and psi psibar -> phi phi (research note models/yukawa_ps, step (4)).
#   1. FeynArts + FeynCalc: 9 and 11 diagrams, Eq. (13) and eq:M1B class by class, UV poles vs the counterterms of Eq. (5);
#      values with Package-X and LoopTools -> results/scat_feyncalc.csv                    (scat_feyncalc.wl)
#   2. unpatched FeynArts + FormCalc (separate kernel): Eq. (13), the spinor chains, Delta-independence; LoopTools values
#      -> results/scat_formcalc.csv                                                         (scat_formcalc.wl)
#   3. COLLIER, the note's formulas, at the points and a cos(theta) scan
#      -> results/scat_collier.csv, results/scat_collier_scan.csv                           (scat_collier.f90)
#   4. comparison, unitarity (Eqs. (14), eq:unitB) with explicit spinors, figure
#      -> results/scat_comparison.csv, ../figs/scat_d4.pdf                                  (scat_numeric.py)
# Needs Src/generated/ (run run_model_check.sh first).  wolframscript may print "libc++abi: ... MathLink::MLException"
# when LoopTools is unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file scat_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d)\)'

echo "=== FormCalc / LoopTools"
wolframscript -file scat_formcalc.wl 2>&1 | grep -E '^\((a|b|c)\)' | cut -c1-400

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" scat_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/scat_collier &&
  (cd work && ./scat_collier ../results/scat_collier.csv ../results/scat_collier_scan.csv | grep wrote)

echo "=== comparison and unitarity"
"$HOME/miniforge3/envs/qft/bin/python" scat_numeric.py | grep -E '^\((A|B)\)|max deviation|^  \(|wrote'
