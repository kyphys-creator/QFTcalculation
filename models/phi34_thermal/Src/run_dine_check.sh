#!/bin/bash
# The high-temperature potential of Dine et al.: critical temperatures, nucleation temperature, beta/H with the SM-like
# coefficients (research note models/phi34_thermal, step (1)) -> results/dine_form.csv               (dine_form.py)
# Needs ../../phi34/Src/results/bounce.csv (the zero-temperature note, step (9)).
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" dine_form.py
