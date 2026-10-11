#!/bin/bash
# One-loop phi phi -> phi phi of phi^3 + phi^4 in d = 4 (research note models/phi34, step (4)).
#   1. FeynArts + FeynCalc: 42 diagrams, Eq. (9) (eq:M1), UV poles and MS-bar counterterms (Eq. (5)); M1 with Package-X
#      and LoopTools -> results/scat_feyncalc.csv                        (scat_feyncalc.wl)
#   2. unpatched FeynArts + FormCalc (separate kernel): Eq. (9), Delta-independence; M1 with LoopTools
#      -> results/scat_formcalc.csv                                      (scat_formcalc.wl)
#   3. COLLIER: M1 at the comparison points and a cos(theta) scan at sqrt(s) = 5
#      -> results/scat_collier.csv, results/scat_collier_scan.csv        (scat_collier.f90)
#   4. comparison, s-channel unitarity for Im M1 (Eq. (10)), figure
#      -> results/scat_comparison.csv, ../figs/scat_d4.pdf               (scat_numeric.py)
# Needs Src/generated/ (run run_model_check.sh first).  wolframscript may print "libc++abi: ... MathLink::MLException"
# when LoopTools is unloaded at the end (also with the phi^3 scripts); the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file scat_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== FormCalc / LoopTools"
wolframscript -file scat_formcalc.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" scat_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/scat_collier &&
  (cd work && ./scat_collier ../results/scat_collier.csv ../results/scat_collier_scan.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" scat_numeric.py
