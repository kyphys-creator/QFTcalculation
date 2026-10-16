#!/bin/bash
# Step (8) of the SM note: two-loop beta functions and the running of the couplings.
#   1. rg_twoloop.py (points 1, 2): general two-loop formulas (Luo-Wang-Xiao) with the explicit SM field content
#                                   against the SM RGEs of Buttazzo et al. (sm_rge.py)
#   2. rg_run.py: running to M_Pl from Buttazzo et al., Martin-Robertson and the step (7) values (needs
#                 results/msbar_fit.csv from run_fit_check.sh); zero of lambda; FJ versus beta_t masses; fig_rg.pdf
cd "$(dirname "$0")"
python3 rg_twoloop.py 1 | tail -3
python3 rg_twoloop.py 2 | tail -1
python3 rg_run.py
