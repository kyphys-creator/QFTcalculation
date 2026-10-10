#!/bin/bash
# Decay of the false vacuum phi = 0 (research note, step (13)).
#   O(d) bounce by shooting (d = 3, 4) and by relaxation, the massless d = 6 instanton, and S_B (d = 4) at the limits
#   of step (12) -> results/bounce.csv, ../figs/bounce_d4.pdf                                         (bounce_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" bounce_numeric.py
