#!/bin/bash
# The single-field model in the nonperturbative phase diagram of the 3D EFT (Gould 2021): the shifted linear coefficient at
# NLO equals the T-independent b, r - r* is mu3-independent, the second-order point tau* at b = 0, the reduced field h
# for b != 0 (research note models/phi34_thermal, step (10)) -> results/nonpert_single.csv          (nonpert_single.py)
# The symbolic NLO check with DRalgo is section (d) of dralgo_check.wl (run_thermal_tools_check.sh).
# Needs results/thermal_single.csv (step (4)).
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" nonpert_single.py
