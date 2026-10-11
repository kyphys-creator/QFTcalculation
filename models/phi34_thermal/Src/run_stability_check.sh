#!/bin/bash
# Generic O(d) bounce solver (checked against the zero-temperature note and steps (1), (2)), and the thermal decay of
# the false vacuum phi = 0 of the single-field model: S_3/T, T_dec (Gamma = H^4) and T_sp along kappa_3 at
# kappa_4 = 0.5, 1, 2, 4 (research note models/phi34_thermal, step (5))
# -> results/stability_single.csv, ../figs/stability_single.pdf                                  (stability_single.py)
# Needs results/dine_form.csv, results/strong_pt.csv, ../../phi34/Src/results/{bounce,prefactor}.csv.  About 10 minutes.
cd "$(dirname "$0")"
mkdir -p results ../figs
"$HOME/miniforge3/envs/qft/bin/python" stability_single.py
