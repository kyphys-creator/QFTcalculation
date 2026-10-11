#!/bin/bash
# Perturbative unitarity of phi phi -> phi phi in phi^3 + phi^4 (research note models/phi34, step (8)).
#   J = 0, 2 partial waves at tree level and one loop (the coupling structures P, Q, R of M1 from COLLIER at Gauss-Legendre
#   nodes, work/pw_collier, plus the conversion terms of Eq. (12)), the projected unitarity relation for each structure,
#   and the bounds (A) tree, (B) high-energy perturbativity of lambda, (C) one-loop unitarity near threshold in the
#   (g/m, lambda) = (kappa_3, kappa_4) plane -> results/pw.csv, ../figs/pw_d4.pdf                     (pw_numeric.py)
# Compares lambda = 0 with the phi^3 note (models/phi3/Src/results/pw4.csv).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
gfortran -I"$HOME/hep/include" pw_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/pw_collier
"$HOME/miniforge3/envs/qft/bin/python" pw_numeric.py
