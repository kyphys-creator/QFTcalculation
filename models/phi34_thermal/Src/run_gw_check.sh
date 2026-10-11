#!/bin/bash
# Gravitational waves from sound waves and turbulence at the benchmarks of step (2), the LISA sensitivity and the SNR
# (research note models/phi34_thermal, step (3)) -> results/gw_spectrum.csv, ../figs/gw_spectrum.pdf    (gw_spectrum.py)
# Needs results/strong_pt.csv (step (2)).
cd "$(dirname "$0")"
mkdir -p results ../figs
"$HOME/miniforge3/envs/qft/bin/python" gw_spectrum.py
