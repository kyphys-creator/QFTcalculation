#!/bin/bash
# Step (3) of the SM note: one-loop tadpole and self-energies, conventions, Slavnov-Taylor identities, finite parts.
#   1. oneloop_conv.wl    : all 88 non-gluon vertex classes of the FeynRules model vs SM.mod (incl. 23 ghost classes)
#   2. oneloop_feyncalc.wl: (b) Feynman gauge vs Eqs. (T)-(SH); (c) FeynRules vs SM.mod at xi = 1 per diagram group;
#                           (d) general R_xi (SM.mod): Slavnov-Taylor identities, Sigma^AA(0), Sigma^AZ(0), on-shell xi
#                           independence, UV poles; (e) B0 values from LoopTools and Package-X -> results/oneloop_*.csv
#   3. oneloop_collier.f90: the same B0 functions from COLLIER -> results/oneloop_collier.csv
#   4. oneloop_numeric.py : comparison with mpmath integrals -> results/oneloop_comparison.csv
# Needs Src/generated/ (run run_model_check.sh first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== vertex classes vs SM.mod"
wolframscript -file oneloop_conv.wl > work/oneloop_conv.log 2>&1
grep -E '^\(a\)' work/oneloop_conv.log

echo "=== self-energies (FeynCalc, LoopTools, Package-X)"
wolframscript -file oneloop_feyncalc.wl > work/oneloop_feyncalc.log 2>&1
grep -E '^\((b|c|d|e)\)' work/oneloop_feyncalc.log

echo "=== COLLIER"
MU2=$(grep -o 'mu^2 = [0-9.]*' work/oneloop_feyncalc.log | head -1 | awk '{print $3}')
gfortran -I"$HOME/hep/include" oneloop_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/oneloop_collier &&
  (cd work && ./oneloop_collier ../results/oneloop_b0.csv ../results/oneloop_collier.csv "$MU2" | grep wrote)

echo "=== comparison with mpmath"
"$PY" oneloop_numeric.py
