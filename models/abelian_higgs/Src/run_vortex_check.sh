#!/bin/bash
# Step (11) of the abelian Higgs note: the Abrikosov-Nielsen-Olesen vortex.
#   1. vortex.py      : the Euler-Lagrange boundary-value problem with scipy solve_bvp for n = 1, 2, 3 and beta = 0.05 ... 10^4;
#                       BPS tension, first-order equations, virial identity, asymptotic decay, large-beta slope, type I/II
#                       -> results/vortex.csv, results/vortex_profiles.csv
#   2. vortex.wl      : the Bogomolny identity (symbolic) and the tension by direct minimization of the discretized energy
#                       (FindMinimum, Richardson) -> results/vortex_min.csv
#   3. vortex_plot.py : ../figs/vortex.pdf
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p results ../figs
"$PY" vortex.py
wolframscript -file vortex.wl 2>&1 | grep -E "^\("
"$PY" vortex_plot.py 2>&1 | grep -v Warning
