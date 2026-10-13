#!/bin/bash
# Resummation of the fermion terms y^4/lambda^2 near lambda = 0 (research note models/yukawa_ps, step (11)).
#   the large-|w| fermion determinant against the derivative expansion (CW potential + Z term); the constrained bounce on S^4
#   (Gegenbauer basis, f(eps) = 1 + 13 eps^2/90 + ...); the leading and next-to-leading exponent along the benchmark; the leading-log
#   running inside the bounce; the resummed cutoff bound for Gamma/V < H0^4 (Higgs-like reading) and the (y, lambda) scan
#   -> results/resum.csv, ../figs/resum_d4.pdf                                                         (resum_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" resum_numeric.py
