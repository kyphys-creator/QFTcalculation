#!/bin/bash
# The thermal potential of the phi^3 + phi^4 model from its own loops (high T + daisy, and full one loop), the odd part
# h chi, the spinodal temperature, the phase history and the strength of the step at b = 0 (research note
# models/phi34_thermal, steps (4), (6))
# -> results/thermal_single.csv, ../figs/thermal_single.pdf                                      (thermal_single.py)
cd "$(dirname "$0")"
mkdir -p results ../figs
"$HOME/miniforge3/envs/qft/bin/python" thermal_single.py
