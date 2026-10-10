#!/bin/bash
# Asymptotic freedom in d = 6 phi phi -> phi phi scattering (research note, step (11)).
#   1. Package-X (analytic C0, D0, 30 digits) and LoopTools: M1 in 90-degree scattering up to sqrt(s) = 1.45e6 m,
#      mu = m and sqrt(s) -> results/af6_feyncalc.csv                                        (af6_feyncalc.wl)
#   2. COLLIER, branches COLI and DD, up to sqrt(s) = 1e4 m -> results/af6_collier.csv        (af6_collier.f90)
#   3. tools against Package-X, the one-loop coefficients and their logarithms, the effective coupling at fixed
#      order and RG-improved; figure -> results/af6_comparison.csv, ../figs/af6_d6.pdf         (af6_numeric.py)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== Package-X / LoopTools"
wolframscript -file af6_feyncalc.wl 2>&1 | grep -E '^\((a|b)\)' | cut -c1-220

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" af6_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/af6_collier &&
  (cd work && ./af6_collier ../results/af6_collier.csv | grep wrote)

echo "=== analysis"
"$HOME/miniforge3/envs/qft/bin/python" af6_numeric.py
