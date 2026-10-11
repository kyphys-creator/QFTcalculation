#!/bin/bash
# Strength alpha_theta (Caprini et al. 2020) and beta/H of the transition in the high-temperature potential of Dine et al.:
# closed form of Delta theta vs numerical minima, scan in E at lambda_T = 0.02, 0.05, 0.1146, benchmarks BP1-BP4
# (research note models/phi34_thermal, step (2)) -> results/strong_pt.csv, ../figs/strong_pt.pdf      (strong_pt.py)
# Needs results/dine_form.csv (step (1)) and ../../phi34/Src/results/bounce.csv (the zero-temperature note, step (9)).
cd "$(dirname "$0")"
mkdir -p results ../figs
"$HOME/miniforge3/envs/qft/bin/python" strong_pt.py
