#!/bin/bash
# Step (7) of the abelian Higgs note: the effective potential and the Nielsen identity.
#   1. effpot.wl          : V1 in Fermi and background R_xi gauges, RG equation (running of the background, v_beta and
#                           Sperling-Stoeckinger-Voigt), Nielsen coefficient C against the one-loop Nielsen function,
#                           tadpole, curvature, hbar expansion of the minimum -> results/effpot*.csv
#   2. nielsen_feyncalc.wl: K_h and K_hh from the Feynman rules (FeynCalc, D dimensions); d T/d xi and d Sigma^H/d xi of
#                           step (3) against the Nielsen identity -> results/nielsen_k.m
#   3. nielsen_numeric.wl : the same with Package-X (C0 of the repeated propagator, central differences in xi)
#                           -> results/nielsen.csv
#   4. effpot_plot.py     : ../figs/effpot.pdf
# Needs results/oneloop_sigma.m (run_oneloop_check.sh).
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p results ../figs
wolframscript -file effpot.wl 2>&1 | grep -E "^\("
wolframscript -file nielsen_feyncalc.wl 2>&1 | grep -E "^\(|^K K|^Summary"
wolframscript -file nielsen_numeric.wl 2>&1 | grep -E "^\("
"$PY" effpot_plot.py 2>&1 | grep -v Warning
