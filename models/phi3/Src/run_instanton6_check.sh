#!/bin/bash
# Decay of the false vacuum in d = 6 (research note, step (15)).
#   Spectrum of the fluctuations around the massless instanton (map to S^6, closed-form Gel'fand-Yaglom ratios),
#   zero-mode norms, counterterms on the instanton, and the instanton-size integral
#   -> results/instanton6.csv, ../figs/instanton6_d6.pdf                                    (instanton6_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" instanton6_numeric.py
