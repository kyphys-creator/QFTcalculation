#!/bin/bash
# d = 4 one-loop check (research note, step (3)).
#   1. FeynArts + FeynCalc: diagrams, normalization, UV poles, MS-bar counterterms; MS-bar finite
#      parts via Package-X and LoopTools -> results/oneloop4_mathematica.csv (oneloop4_feyncalc.wl)
#   2. COLLIER MS-bar finite parts -> results/oneloop4_collier.csv     (oneloop4_collier.f90)
#   3. comparison with closed forms / Feynman-parameter integrals, optical theorem, figure
#      -> results/oneloop4_comparison.csv, ../figs/b0_d4.pdf             (oneloop4_numeric.py)
# Needs Src/generated/ (run generate_Phi3.wl first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file oneloop4_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" oneloop4_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/oneloop4_collier &&
  (cd work && ./oneloop4_collier ../results/oneloop4_collier.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" oneloop4_numeric.py
