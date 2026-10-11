#!/bin/bash
# Bounce action of the false vacuum phi = 0 of phi^3 + phi^4 as a function of alpha (research note models/phi34, step (9)).
#   O(d) bounce by shooting in d = 4 and d = 3 (h = f - f_- near the thin-wall limit), Derrick's relation, dS/dalpha,
#   relaxation, the phi^3 limit, the thin-wall limits, Dine et al. (1992) for d = 3, and the Higgs reading without
#   prefactor -> results/bounce.csv, ../figs/bounce_alpha.pdf                                       (bounce_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" bounce_numeric.py 2>&1 | grep -v -E 'RuntimeWarning|d2 = norm'
