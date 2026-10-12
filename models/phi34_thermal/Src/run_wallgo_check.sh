#!/bin/bash
# The bubble-wall speed in local thermal equilibrium (research note models/phi34_thermal, step (12)):
#   1. wallgo_check.py (env qft): WallGo 1.1.2, v_w(LTE) for BP1-BP4 at TransitionListener's T_perc, for the SM-like
#      coefficients and BP1-BP4 at T_n with the LISA SNR, and for the SNR = 10 points of step (9) -> results/wallgo_check.csv
#   2. review_tools/transitionlistener_lte.py (env tl): TransitionListener's LTE matching with its fixed-phi sound speeds
#      (reproduces its v_wall of step (11)) and with the sound speeds along the phase -> results/transitionlistener_lte.csv
# Needs results/{dine_form,strong_pt,lisa_scan,transitionlistener_check}.csv.  About 2 minutes.
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" wallgo_check.py
cd review_tools && "$HOME/miniforge3/envs/tl/bin/python" transitionlistener_lte.py
