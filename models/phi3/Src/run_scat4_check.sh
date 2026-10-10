#!/bin/bash
# One-loop phi phi -> phi phi in d = 4 (research note, step (5)).
#   1. FeynArts + FeynCalc: 12 diagrams, Eq. (17) (eq:M1), UV poles and MS-bar counterterm; M1 with Package-X
#      and LoopTools -> results/scat4_feyncalc.csv                      (scat4_feyncalc.wl)
#   2. unpatched FeynArts + FormCalc (separate kernel): Eq. (17) (eq:M1), Delta-independence; M1 with LoopTools
#      -> results/scat4_formcalc.csv                                    (scat4_formcalc.wl)
#   3. COLLIER: M1 at the comparison points and a cos(theta) scan at sqrt(s) = 5
#      -> results/scat4_collier.csv, results/scat4_collier_scan.csv      (scat4_collier.f90)
#   4. comparison, s-channel unitarity for Im M1, figure
#      -> results/scat4_comparison.csv, ../figs/scat4_d4.pdf             (scat4_numeric.py)
# Needs Src/generated/ (run generate_Phi3.wl first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file scat4_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== FormCalc / LoopTools"
wolframscript -file scat4_formcalc.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" scat4_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/scat4_collier &&
  (cd work && ./scat4_collier ../results/scat4_collier.csv ../results/scat4_collier_scan.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" scat4_numeric.py
