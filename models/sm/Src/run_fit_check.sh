#!/bin/bash
# Step (7) of the SM note: MS-bar parameters from measured quantities at one loop (FJ tadpoles).
#   msbar_fit.wl reads results/oneloop_sigma.m (run_oneloop_check.sh), mudecay_deltahat_finite.m and alpha_deltae.m
#   (run_gf_check.sh); compares with Buttazzo et al. (NLO, NNLO) and Martin-Robertson, and gives the PDG 2024 values
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file msbar_fit.wl 2>&1 | grep -E "^\(|^    |Summary"
