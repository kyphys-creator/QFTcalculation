#!/bin/bash
# Step (4) of the CKM note: the Yukawa-matrix beta functions and the running of the masses, V and J.
#   1. rg_ckm_feyncalc.wl : beta_Y from the note's model (ubar_i d_j G+ vertex poles, G+ and quark field renormalizations;
#                           needs results/oneloop_ckm_sigma.m of step (3)) against Eq. (betaY), exactly for a rational
#                           unitary V and in 50 digits for the benchmark V; xi independence (about 10 minutes)
#   2. rg_ckm_general.py  : the general one-loop formulas with complex Yukawa matrices against Eq. (betaY); Eqs. (yrun),
#                           (Vrun) against the integrated matrix RGEs (double precision and 50 digits); rephasing
#   3. ckm_rg_handcheck.py: the benchmark numbers of the note's Sec. rg
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
wolframscript -file rg_ckm_feyncalc.wl > work/rg_ckm_feyncalc.out 2>&1
grep -E "^\(|Summary|WARNING" work/rg_ckm_feyncalc.out | cut -c1-300
python3 rg_ckm_general.py
python3 ckm_rg_handcheck.py
