#!/bin/bash
# One-loop prefactor of the false-vacuum decay rate of phi^3 + phi^4 in d = 4 as a function of alpha, and the vacuum-
# stability bound in (kappa_3, kappa_4) (research note models/phi34, step (10)).
#   bounce (bisection + two-sided matching), Gel'fand-Yaglom partial waves with Born subtraction, zero and negative
#   modes, MS-bar first- and second-order terms, Dunne-Min's local formula, mu-independence, thin-wall limit, the
#   cosmological condition -> results/prefactor.csv, ../figs/prefactor_alpha.pdf, ../figs/stability.pdf  (prefactor_numeric.py)
# Needs results/bounce.csv (run_bounce_check.sh).  About 4 minutes.
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" prefactor_numeric.py 2>&1 | grep -v -E 'RuntimeWarning|d2 = norm|c_zero = S4'
