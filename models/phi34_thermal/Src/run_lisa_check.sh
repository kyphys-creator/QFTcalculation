#!/bin/bash
# Where the general form reaches LISA: scalings in D at fixed (E, lambda_T), scan A in (D, T0) for the (E, lambda_T) of
# BP1-BP4, scan B in (E, D) at lambda_T = 0.02, 0.05, 0.1146 with the T0 of the largest SNR
# (research note models/phi34_thermal, step (9)) -> results/lisa_scan.csv, ../figs/lisa_scan.pdf          (lisa_scan.py)
# Needs results/dine_form.csv and results/strong_pt.csv.  About 2 minutes.
cd "$(dirname "$0")"
mkdir -p results ../figs
"$HOME/miniforge3/envs/qft/bin/python" lisa_scan.py
