#!/bin/bash
# Step (6) of the abelian Higgs note: the renormalization group.
#   1. rg_general.py  : the general one-loop formulas (Machacek-Vaughn, Luo-Wang-Xiao) with the explicit real components of
#                       Phi against Eq. (rge); the two-loop gauge term
#   2. rg_numeric.wl  : beta_e, beta_m2, beta_lam from the mu dependence of M_h,p, M_A,p and Gamma(h -> A A) (general xi);
#                       the pole masses and the width with running parameters at mu = 1/2, 1, 2, 4 -> results/rg_numeric.csv
#   3. rgflow.py      : the one-loop flow of e and lambda, Landau poles, the triviality bound -> results/rgflow.csv,
#                       ../figs/rgflow.pdf
# Needs results/oneloop_sigma.m (run_oneloop_check.sh) and results/nlo_width_sigma.m (run_width_check.sh).
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p results ../figs
"$PY" rg_general.py
wolframscript -file rg_numeric.wl 2>&1 | grep -E "^\("
"$PY" rgflow.py 2>&1 | grep -v Warning
