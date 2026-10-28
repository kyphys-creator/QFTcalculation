#!/bin/bash
# Step (8) of the abelian Higgs note: the Coleman-Weinberg mechanism (m^2 = 0).
#   1. cw.wl    : leading order (minimum, MH^2/MA^2 = 3 e^2/(8 pi^2), dimensional transmutation), the scheme of Coleman and
#                 Weinberg (-25/6, lam_CW = 33 e^4/(8 pi^2)), the exact one-loop ratio in five gauges against the
#                 numerical minimum, the mu dependence with running couplings -> results/cw_ratio.csv, cw_mu.csv, cw_points.csv
#   2. cw_rg.py : CosmoTransitions generic_potential.V1 against cw.wl; RG improvement (running to mu* = MA) against fixed
#                 order -> results/cw_rg.csv, ../figs/cw.pdf
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p results ../figs
wolframscript -file cw.wl 2>&1 | grep -E "^\("
"$PY" cw_rg.py 2>&1 | grep -v Warning
