#!/bin/bash
# d = 6 one-loop check (research note, step (4)).
#   1. FeynArts + FeynCalc: diagrams; Feynman parametrization in D = 6 - 2 eps, UV poles, MS-bar
#      counterterms, beta(g); Package-X and LoopTools through the dimension shift
#      PaVe^(D+2) = -2 pi PaVe_00^(D) -> results/oneloop6_mathematica.csv   (oneloop6_feyncalc.wl)
#   2. COLLIER A00, B00, C00 -> results/oneloop6_collier.csv               (oneloop6_collier.f90)
#   3. comparison with closed forms / Feynman-parameter integrals, optical theorem, figure
#      -> results/oneloop6_comparison.csv, ../figs/b0_d6.pdf               (oneloop6_numeric.py)
# Needs Src/generated/ (run generate_Phi3.wl first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file oneloop6_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" oneloop6_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/oneloop6_collier &&
  (cd work && ./oneloop6_collier ../results/oneloop6_collier.csv | grep wrote)

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" oneloop6_numeric.py
