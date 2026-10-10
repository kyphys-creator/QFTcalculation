#!/bin/bash
# One-loop prefactor of the false-vacuum decay rate in d = 4 (research note, step (14)).
#   Gel'fand-Yaglom partial waves with Born subtraction, zero and negative modes, MS-bar second-order term in
#   momentum space, the local formula of Dunne-Min as a check, and the rate at the limits of step (12)
#   -> results/prefactor.csv, ../figs/prefactor_d4.pdf                                       (prefactor_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" prefactor_numeric.py
