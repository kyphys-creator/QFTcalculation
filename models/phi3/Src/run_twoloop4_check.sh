#!/bin/bash
# d = 4 two-loop self-energy (research note, step (16)).
#   1. FeynArts + FeynCalc: diagrams, mapping onto the integral families, IBP reduction with Kira 3.1 and FIRE 7.1
#      (FeynHelpers 2), the two reductions compared -> results/twoloop4_reduction.m           (twoloop4_feyncalc.wl)
#   2. AMFlow 2.0 (Kira 3.1): the master integrals at s = -1, 1, 5, 12, the poles of the self-energy, its finite part
#      -> results/twoloop4_amflow.csv, results/twoloop4_sigma.csv                            (twoloop4_amflow.wl)
#   3. TSIL 1.46, pySecDec 1.6.6, feyntrop 1.1.0 against AMFlow; MR05's self-energy and the pole mass; figure
#      -> results/twoloop4_tsil.csv, results/twoloop4_comparison.csv, ../figs/twoloop4_d4.pdf (twoloop4_tsil.c,
#         twoloop4_numeric.py)
# Needs Src/generated/ (run generate_Phi3.wl first) and the two-loop tools of environment.pdf (Sec. 8).  About 12 minutes.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynArts + FeynCalc, Kira, FIRE"
wolframscript -file twoloop4_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d)\)'

echo "=== AMFlow"
wolframscript -file twoloop4_amflow.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== TSIL, pySecDec, feyntrop"
"$HOME/miniforge3/envs/qft/bin/python" twoloop4_numeric.py 2>&1 | grep -v -i "warning"
