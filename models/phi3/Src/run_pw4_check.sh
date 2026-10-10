#!/bin/bash
# Perturbative unitarity and perturbativity of phi phi -> phi phi in d = 4 (research note, step (12)).
#   J = 0, 2 partial waves at tree level and one loop (M1 from COLLIER at Gauss-Legendre nodes, work/xsec_collier),
#   the projected unitarity relation, and the bounds on g/m -> results/pw4.csv, ../figs/pw4_d4.pdf   (pw4_numeric.py)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
gfortran -I"$HOME/hep/include" xsec_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/xsec_collier
"$HOME/miniforge3/envs/qft/bin/python" pw4_numeric.py
