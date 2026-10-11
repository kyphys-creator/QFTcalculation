#!/bin/bash
# Cross-check with CosmoTransitions 2.0.7 (pip, qft environment): bounce actions, phases, T_c and T_n of the Dine form,
# and the phase structure of the single-field model (research note models/phi34_thermal, step (7))
# -> results/cosmotransitions_check.csv                                                  (cosmotransitions_check.py)
# Needs results/dine_form.csv and results/strong_pt.csv.  About 15 minutes.
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" cosmotransitions_check.py
