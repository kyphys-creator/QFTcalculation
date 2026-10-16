#!/bin/bash
# Premise of the SM note (V_CKM = 1): size of the CKM effects on the computed quantities.
#   ckm_estimate.wl reads results/oneloop_sigma.m (run run_oneloop_check.sh first) and puts the PDG 2024 CKM matrix
#   into the 1PI W and top self-energies (unitarity of the W pole, beta_{y_t} for the top pole, xi independence of
#   the top pole mass, shifts of DeltaHat, M_W, m_t, beta_{y_t} at the benchmark)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file ckm_estimate.wl 2>&1 | grep -E "^\||^    |^\(|Summary"
