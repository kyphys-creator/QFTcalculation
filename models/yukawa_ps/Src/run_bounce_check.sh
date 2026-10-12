#!/bin/bash
# RG-improved effective potential and the lambda < 0 bounce (research note models/yukawa_ps, step (9)).
#   one-loop running of (y^2, lambda, m^2, M) against the closed forms; the RG-improved Delta V(phi) for four scale choices and the
#   field where it turns negative; the Fubini bounce (radial equation, action), the mass term, S(R) = 16 pi^2/|lambda(kappa/R)|
#   -> results/bounce.csv, ../figs/bounce_d4.pdf                                                       (bounce_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" bounce_numeric.py
