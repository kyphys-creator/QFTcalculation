#!/bin/bash
# Step (5) of the SM note: one-loop pole masses (QCD part of the top, beta_t-scheme masses, RG check).
#   pole_numeric.wl reads results/oneloop_sigma.m and results/oneloop_numeric.csv (run run_oneloop_check.sh first)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file pole_numeric.wl 2>&1 | grep -E "^\(|spread|mu = |      NumberForm"
