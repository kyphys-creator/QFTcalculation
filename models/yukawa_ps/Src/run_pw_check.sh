#!/bin/bash
# Perturbative unitarity of the coupled phi phi and psi psibar partial waves (research note models/yukawa_ps, step (8)).
#   1. COLLIER: the one-loop amplitudes of Eqs. (13), (18) split into coupling structures                 (pw_collier.f90)
#   2. helicity partial waves J = 0, 1/2, 1, 3/2, 2 at tree level (explicit spinors), their high-energy limits, the bounds
#      (A) tree unitarity, (B) with running couplings, (C) one-loop unitarity of the elements with phi phi, the projected
#      one-loop unitarity check -> results/pw.csv, ../figs/pw_d4.pdf                                       (pw_numeric.py)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" pw_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/pw_collier && echo "built work/pw_collier"

echo "=== partial waves and bounds"
"$HOME/miniforge3/envs/qft/bin/python" pw_numeric.py
