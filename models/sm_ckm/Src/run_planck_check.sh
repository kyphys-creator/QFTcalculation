#!/bin/bash
# Step (10) of the CKM note: V and J from M_t to the Planck scale.
#   1. rg2_ckm_general.py: the two-loop beta functions of the Yukawa matrices from the general formulas (Luo-Wang-Xiao) with
#      the explicit field content and complex matrices; the coefficients of the matrix structures fitted and checked
#      (against Eq. (betaY) at one loop, the SM note's two-loop gaugeless terms from its model, the diagonal limit of
#      Buttazzo et al.) -> results/rg2_ckm_coeffs.csv, rg2_ckm_general.csv
#   2. ckm_planck.py: the running from the SM note's step (7) values at M_t with the MS-bar V(M_t) of step (6), one loop
#      (the note's Eq. (betaY)) and two loops; the closed forms Eq. (yrun), (Vrun), a rotation of the generation bases, the
#      hierarchical limit -> results/ckm_planck.csv, ../ResearchNote/fig_vrun.pdf
# Needs the SM note's results (models/sm/Src/results/msbar_fit.csv, twoloop_sym_beta.csv).  About 20 seconds.
cd "$(dirname "$0")"
python3 rg2_ckm_general.py
python3 ckm_planck.py
